import requests
from bs4 import BeautifulSoup  # for web extraction, scraping etc
import json
from typing import List
import streamlit as st


NEWS_API_KEY = st.secrets["NEWS_API_KEY"]  
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"


class News:
    """Class to hold structured news article data."""
    def __init__(self, headline, url, publisher, description="", content="", pubDate=""):
        self.headline = headline
        self.url = url
        self.publisher = publisher
        self.description = description
        self.content = content
        self.pubDate = pubDate
    
    def __repr__(self):
        return (f"headline={self.headline},\n url={self.url},\n "
                f"publisher={self.publisher},\n description={self.description},\n "
                f"content={self.content},\n pubDate={self.pubDate}\n")

# GOOGLE NEWS SCRAPING 

def _extract_google_content(url):
    """Scrapes content from a single article link found by Google News scraper."""
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        masterjson = {}
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')           
            
            # Find JSON ld metadata which contains clean article content
            for script in soup.find_all('script', {"type": "application/ld+json"}):                
                masterjson.update(json.loads(script.string))

        return masterjson

    except Exception as e:
        # print(f"Error during Google content extraction: {e}")
        return {}


def _scrape_google_news(query: str, limit: int = 5) -> List[News]:
    """Tries to fetch high-quality articles using Google News scraping."""
    query = query.replace(" ","%20")
    url = f"https://news.google.com/search?q={query}&hl=en-IN&gl=IN&ceid=IN%3Aen"
    result = []
    
    try:
        response = requests.get(url, allow_redirects=True)
        if response.status_code != 200:
            return [] # Fail fast if status code is bad

        soup = BeautifulSoup(response.content, 'html.parser')
        # Target the specific script tag that holds article data
        datascript = soup.find('script', {"class": "ds:2"})

        if datascript:
            data = datascript.string
            start = data.find('data:[')
            end = data.rfind(']')

            if start != -1 and end != -1:
                list_data_str = data[start+5:end+1]
                list_data = json.loads(list_data_str)

                # Process first 25 items found in the data structure
                for news_item in list_data[1][0][:25]:
                    
                    # Logic to extract URL based on structure variations
                    if len(news_item) == 2:
                        link = news_item[1][2][0][6]
                    elif len(news_item) == 8:
                        link = news_item[0][6]
                    else:
                        continue # Skip unknown structure

                    # Extract full content using JSON-LD scraper
                    masterjson = _extract_google_content(link)

                    if masterjson and "articleBody" in masterjson:
                        result.append(News(
                            masterjson.get('headline', 'N/A'),
                            masterjson.get('url', 'N/A'),
                            masterjson.get('publisher', {}).get('url', 'N/A'),
                            masterjson.get('description', 'N/A'),
                            masterjson.get('articleBody', 'N/A'),
                            masterjson.get('datePublished', 'N/A')
                        ))
                        limit -= 1
                        if limit == 0:
                            break
                        
        return result
    except Exception as e:
        print(f"Google News Scraper Error: {e}")
        return []

# NEWSaPI HELPER FUNCTIONS High Coverage

def _scrape_full_article_body(url: str) -> str:
    """Fetches the URL and attempts to scrape the main article text."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, 'html.parser')

        # look for common article containers and then paragraphs
        article_block = soup.find('article') or soup.find('main') or soup.find('div', class_='content')
        
        paragraphs = []
        if article_block:
             paragraphs = article_block.find_all('p')
        else:
             # Fallback to all paragraphs if no specific block is found
             paragraphs = soup.find_all('p')

        # Filter shortjunk paragraphs and combine text
        full_text = ' '.join([p.text for p in paragraphs if len(p.text.split()) > 10]) 
             
        return full_text.strip()

    except requests.exceptions.RequestException as e:
        # print(f"Error scraping article at {url}: {e}")
        return ""
    except Exception as e:
        # print(f"General error during scraping: {e}")
        return ""


def _api_fetch_articles(query: str, limit: int = 5) -> List[News]:
    """Fetches articles using NewsAPI as a fallback."""
    if NEWS_API_KEY == st.secrets["NEWS_API_KEY"]:
        print("NewsAPI key is not configured. Skipping fallback.")
        return []
        
    params = {
        'q': query,
        'apiKey': NEWS_API_KEY,
        'sortBy': 'relevancy',
        'language': 'en',
        'pageSize': limit
    }
    
    results = []
    
    try:
        response = requests.get(NEWS_API_ENDPOINT, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'ok' and data['articles']:
            for article in data['articles']:
                url = article.get('url', 'N/A')
                
                # Scrape the full article content
                full_content_text = _scrape_full_article_body(url)

                results.append(
                    News(
                        headline=article.get('title', 'N/A'),
                        url=url,
                        publisher=article.get('source', {}).get('name', 'N/A'),
                        description=article.get('description', ''),
                        # Store the scraped full text, falling back to API content snippet
                        content=full_content_text or article.get('content', ''), 
                        pubDate=article.get('publishedAt', 'N/A')
                    )
                )
        return results
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from NewsAPI: {e}")
        return []
    except Exception as e:
        print(f"General error processing API response: {e}")
        return []

# MASTER FUNCTION WITH FALLBACK LOGI

def get_news_list(query: str, limit: int = 5) -> List[News]:
    """
    Tries Google News scraping first for high accuracy. 
    If that fails or returns zero results, it falls back to NewsAPI for better coverage.
    """
    
    # 1 Try Google News Scraping ( Accuracy
    print(f"Attempting Google News scrape for query: '{query}'")
    results = _scrape_google_news(query, limit)
    
    if len(results) < limit and len(results) == 0:
        # 2 Fallback to NewsAPI (Highest Coverage)
        print("Google News scraping failed or returned insufficient results. Falling back to NewsAPI.")
        fallback_results = _api_fetch_articles(query, limit)
        
        # Merge or replace (since Google failed)
        if fallback_results:
             print(f"Successfully fetched {len(fallback_results)} articles from NewsAPI.")
             return fallback_results
        
    if not results:
         print("No news context found after trying both sources.")
         
    return results