import streamlit as st
import csv
from module import nextractor as nx
import pandas as pd
from module import translate as tst
import os 
# Import the News class from the module to resolve NameError
from module.nextractor import News


st.set_page_config(page_title="Actual Context Report", layout="wide", initial_sidebar_state="expanded")


st.markdown("""
    <style>
        /* 1. GAP REDUCTION & MAIN CONTAINER STYLING */
        .block-container {
            padding-top: 0rem !important; 
            padding-bottom: 0rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }

        /* 2. SIDEBAR BACKGROUND */
        [data-testid="stSidebar"] {
            background-color: #1f2937; /* Dark background remains for contrast */
            color: white;
        }

        /* 3. FIXED LOGO INJECTION (Top Left Sidebar) */
        [data-testid="stSidebar"]::before {
            content: "NetShield 🛡️";
            display: block;
            font-size: 26px;
            font-weight: bold;
            color: #ffffff;
            text-align: left;
            padding: 20px 0 10px 20px;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 10px;
        }
        
        /* 4. SIDEBAR FOOTER (Navigation Text at Bottom) */
        [data-testid="stSidebar"]::after {
            content: "Use the sidebar to navigate through NetShield features.";
            position: absolute;
            bottom: 10px; 
            left: 0;
            right: 0;
            padding: 10px 15px;
            text-align: center;
            font-size: 14px;
            color: rgba(255, 255, 255, 0.5); 
            z-index: 10000;
        }
        
        /* Custom style for the Description Box (MATCHING Content Forensic style) */
        .context-description-box {
            background-color: #333d47; /* Matching dark background */
            padding: 15px;
            border-radius: 5px;
            border-left: 5px solid #ffa500; /* Matching orange accent */
            margin-bottom: 30px; 
        }
        
        .context-description-box strong {
            font-size: 18px;
            display: block; 
            margin-bottom: 5px; 
            color: #ffffff; /* Matching light text color */
        }
        
        .context-description-box ul {
            margin: 5px 0 0 0; 
            color: #f0f0f0; /* Light text color for list items */
            padding-left: 20px;
            list-style-type: disc;
            font-size: 16px;
        }
        
        /* Custom style for article separator between articles in the expander */
        .article-separator {
            margin-top: 10px;
            margin-bottom: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.1); 
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div style="display: none;">
        NetShield🛡️
    </div>
""", unsafe_allow_html=True)



st.title("Actual Context Report")


st.markdown("""
    <div class="context-description-box">
        <strong>Contextual Analysis Overview:</strong>
        <ul>
            <li>This page uses the video titles to search for related news articles from external web sources.</li>
            <li>The process involves translating the title (using LLMs).</li>
            <li>Videos that yield matching news articles are displayed below, providing a factual baseline against which the video content can be compared.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)



# page
try:
    file_path = os.path.join(os.getcwd(), "video_data.csv") 
    
    if not os.path.exists(file_path):
        st.error("Data file (video_data.csv) not found. Please ensure data has been fetched on the previous analysis page.")
        st.stop()
        
    df = pd.read_csv(file_path) 
    
    # Check if expected columns exist or infer
    video_titles = df.iloc[:, df.columns.get_loc('Video Title')] if 'Video Title' in df.columns else df.iloc[:, 1]
    
    if video_titles.empty:
         st.warning("The data file is empty or missing expected column for video titles.")
         st.stop()


    video_title_list=[]
    newslist=[]
    k=0
    
    st.subheader("Related Context Extraction Results")
    st.markdown("---")
    
    for i in video_titles:
        
        # -LOADING INDICATOR
        with st.spinner(f"Translating and searching external context for video {k+1}..."):
            try:
                query = tst.trans(i)
            except NameError:
                st.error("Error: `tst.trans` module not found or failed to load. Using raw title as query.")
                query = i # Fallback
                
            # 2. Get news list (returns list of News objects)
            ns = nx.get_news_list(query)
        # --- END

        if ns:
            st.markdown(f"### Video: {i}") 
            
            # Display Count and Related News
            st.markdown(f"**Total Articles Found:** {len(ns)}") 
            st.markdown("**Related News Articles (Click to expand):**")
            
      #  ORGANIZED ARTICLE DISPLAY
            
            for idx, news_obj in enumerate(ns):
                
                # Format date to show only yyyymmdd
                raw_date = news_obj.pubDate 
                date_published = raw_date.split('T')[0].split(' ')[0] if raw_date else 'N/A'
                
                # Use st.expander for a cleaner view
                # We need a unique key here too, based on the video title (i) and article index (idx)
                with st.expander(f"**Article {idx + 1}:** {news_obj.headline}", expanded=False):
                    st.markdown(f"* **Source:** {news_obj.publisher}")
                    st.markdown(f"* **Date Published:** {date_published}") 
                    st.markdown(f"* **URL:** [View Full Article]({news_obj.url})")
                    
                    # FIX: Add unique key based on the news article's URL
                    unique_key = f"content_area_{news_obj.url}_{i}_{idx}"
                    
                    st.markdown(f"#### Article Content")
                    st.text_area(f"Content for {news_obj.headline[:80]}....", 
                                 news_obj.content, 
                                 height=300, 
                                 key=unique_key) # <-- THE FIX IS HERE
                    

                # Separator is outside the expander
                if idx < len(ns) - 1:
                     st.markdown('<div class="article-separator"></div>', unsafe_allow_html=True)

            #  END ORGANIZED ARTICLE DISPLAY

            # - Data Stora
            video_title_list.append(i)
            newslist.append(ns)
            st.markdown("---") # Final separator after the entire video block

        k=k+1 


    # FINAL DATA STORAGE
    data={
       'video title':video_title_list,
       'news':newslist
    }
    
    if video_title_list:
        st.success(f"Contextual data extracted for {len(video_title_list)} videos.")


except FileNotFoundError:
    st.error("Critical error: Could not load data file.")
except Exception as e:
    st.error(f"An unhandled application error occurred: {e}. Check your 'nextractor.py' file is correct.")