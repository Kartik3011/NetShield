import requests
from bs4 import BeautifulSoup  #for web extraction ,scraping etc
import json

class News:

    def __init__(self, headline, url, publisher, description="", content="", pubDate=""):
        self.headline = headline
        self.url = url
        self.publisher = publisher
        self.description = description
        self.content = content
        self.pubDate = pubDate
    
    def __repr__(self):
        return f"headline={self.headline},\n url={self.url},\n publisher={self.publisher},\n description={self.description},\n content={self.content},\n pubDate={self.pubDate}\n"

def get_news_list(query:str, limit:int = 5) -> list[News]:
    
    query = query.replace(" ","%20") # assigns result back to query for correct URL encoding
    url = f"https://news.google.com/search?q={query}&hl=en-IN&gl=IN&ceid=IN%3Aen"

    # print(f"URL: {url}")

    try:
        response = requests.get(url, allow_redirects=True)
        # print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            datascript = soup.find('script', {"class": "ds:2"})

            # print(f"is datascript: {datascript is not None}")

            result = []
            if datascript:
                data = datascript.string

                # print(f"datalength: {len(data)}") ^^

                start = data.find('data:[')
                end = data.rfind(']')
                # print(f"start end: {start,end}") ^^^


                list_data_str = data[start+5:end+1]
                list_data = json.loads(list_data_str)

                # print(f"no of articles: {len(list_data[1][0])}")

                for news in list_data[1][0][:25]:

                    # print(f"type: {len(news)}")

                    if len(news) == 2:
                        # news = news[1]
                        link = news[1][2][0][6]
                        
                    elif len(news) == 8:
                        # print(news[0][1])

                        link = news[0][6]
                        # print(link)

                    masterjson = extract_news_content(link)
                    # print(masterjson)

                    if(masterjson == {}):
                        # print("empty")
                        continue
                    if("articleBody" not in masterjson):
                        # print("no body")
                        continue
                    result.append(News(masterjson.get('headline', 'N/A'),
                                       masterjson.get('url', 'N/A'),
                                       masterjson.get('publisher', {}).get('url', 'N/A'),
                                       masterjson.get('description', 'N/A'),
                                       masterjson.get('articleBody', 'N/A'),
                                       masterjson.get('datePublished', 'N/A')))
                    limit -= 1
                    if(limit == 0):
                        break
                        
            return result
        else:
            # print(f"Error: Unable to fetch data. Status Code: {response.status_code}")

            return []
    except Exception as e:
        # print(e)
        return []

def extract_news_content(url):

    try :
        # print(f"getting content for: {url}")

        response = requests.get(url, allow_redirects=True, timeout=10)

        # print(f"URL: {url}")
        # print(f"Status code: {response.status_code}")

        masterjson = {}
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')           
            
            for script in soup.find_all('script', {"type": "application/ld+json"}):                
                
                 # print(f"script: {script.string}")

                masterjson.update(json.loads(script.string))

        # with open("newsjson.json","w") as f:
        #     json.dump(masterjson,f,indent=2)
             # print("written to file")
        # print()
        return masterjson

    except Exception as e:
        # print(e)
        return {}

# Example usage
# url = input("Enter the URL of the news article: ")
# news_data = extract_news_content(url)
# # print(news_data)
# # print("Title:", news_data.get('title', 'N/A'))
# # print("Content:", news_data.get('content', 'N/A'))
'''
query = input("Enter a search query: ")
get_news_list(query)
for news in get_news_list(query):
     print(news)
     print()

'''