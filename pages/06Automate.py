
#most imp pageeeeee
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from module import yextractor as youtube
import requests
from module import nextractor as nx
from module import summarize as sumz
from module import translate as tst
from module import identifier as idefy
import altair as alt
import os 


st.set_page_config(page_title="NetShield Automation", layout="wide", initial_sidebar_state="expanded")



st.markdown("""
    <style>
        /* 1. GAP REDUCTION: Main content block padding */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }

        /* 2. SIDEBAR BACKGROUND */
        [data-testid="stSidebar"] {
            background-color: #1f2937; /* Dark background */
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
        
        /* 5. Custom style for the description box (MATCHING #333d47) */
        .description-box-v2 {
            background-color: #333d47; /* CORRECTED: Dark gray/blue background from your Account Report CSS */
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid #3498db; /* Blue accent color */
            margin-bottom: 20px; /* Space after the description box */
        }
        
        .description-box-v2 h3 {
             color: #ffffff; 
             margin-top: 0;
        }
        
        .description-box-v2 p, .description-box-v2 li {
             color: #f0f0f0; /* Slightly lighter text for contrast against #333d47 */
             font-size: 15px; 
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div style="display: none;">
        NetShield🛡️
    </div>
""", unsafe_allow_html=True)


# Ensure sidebar is empty (or contains placeholder) to allow CSS injection  

with st.sidebar:
    pass

filename = "Accountreport.csv"

st.title("NetShield Content Automation Analysis") 



st.markdown("""
    <div class="description-box-v2">
        <h3>AI Verification Pipeline:</h3>
        <p>
        This page performs the full AI analysis on the fetched videos, executing the core NetShield process:
        </p>
        <ol style="padding-left: 20px;">
            <li><strong>Content Extraction:</strong> Uses Title, Description, Audio as the source text.</li>
            <li><strong>Context Fetch:</strong> Finds and scrapes related news articles.</li>
            <li><strong>Summarization:</strong> Uses LLMs to create summaries of both video content and news.</li>
            <li><strong>Validation:</strong> Uses Meta/Llama 3 70B to compare summaries and assign a status.</li>
        </ol>
        <p style="font-weight: bold;">Final Output: A comprehensive report of Green (Accurate), Yellow (Inconclusive), or Red (Misinformation/Abuse).</p>
    </div>
""", unsafe_allow_html=True)



# DATA LOAD AND PROCESSING START


st.subheader("1. Data Loading")
st.write("Loading fetched YouTube Data for analysis...")

def load_data():
   
    file_path = os.path.join(os.getcwd(), "video_data.csv") 
    
    # Check if file exists before trying to read it
    if not os.path.exists(file_path):
        st.error("Error: video_data.csv not found. Please run 'Just Fetch Data' first.")
        return pd.DataFrame()
        
    return pd.read_csv(file_path)

# Load the data
df = load_data()

if df.empty:
    st.warning("No video data found to process. Stopping automation.")
    st.stop()


# Get all necessary columns for the loop
video_titles = df['Video Title']
video_Link = df['Video URL']
video_descriptions = df['Description']
channel_titles = df['Channel Title'] 
subscriber_counts = df['Subscriber Count']

k=0
Finalaclist=[]
processing_bar = st.progress(0)
total_videos = len(video_titles)
progress_increment = 100 / total_videos

st.subheader(f"2. Processing {total_videos} Videos")

# Initialize container for detailed output display

details_container = st.container()

# Update the loop to include new metadata columns
for k, (link, title, description, channel_title, subscriber_count) in enumerate(zip(video_Link, video_titles, video_descriptions, channel_titles, subscriber_counts)):
    with details_container:
        st.markdown(f"---")
        st.markdown(f"### 🎬 Video {k+1}: {title}")
        
        
        # 2 Content Source (ENRICHED METADATA)
        
        # CRITICAL imppp '
        # Using Title and Description as the sole content source for the LLM
        content = f"""
Video Title: {title}
Video Description: {description}
"""
        
        st.markdown("#### Raw Video Content")
        
        # Only exit if absolutely no content exists (Title and Description are both empty)
        if not title.strip() and not description.strip(): 
            Finalaclist.append('Yellow')
            st.warning("Status: Yellow (No content at all: Title and Description were empty.)")
            processing_bar.progress(int(((k + 1) * progress_increment)))
            continue
            
        st.expander("View Full Content").text(content)


        # 2 Structured Claim Extraction & Context Fetch
     
        st.markdown("#### LLM Claim Extraction")
        
        #  Extract the claim (Using the new extract_claim function)
        with st.spinner("Extracting factual claim and source authority ..."):
            try:
                # Use the 'content' (Metadata Rich) as input for extraction
                contentsum=sumz.extract_claim(content)
            except AttributeError:
                st.error("Error: `sumz.extract_claim` not found. Assuming 'sumup' was intended.")
                contentsum=sumz.sumup(content) 
            except NameError:
                st.error("Error: `sumz` module failed to load.")
                contentsum = "IRRELEVANT_CONTENT_FLAG" 
        
        st.markdown(f"**Video Claim (Mistral):**")
        st.info(contentsum)

        #  Fetch News Context
        st.markdown("#### Contextual News Search")
        
        # Ensure the module function exists and works
        try:
            initial_query = tst.trans(title)
        except NameError:
            st.error("Error: `tst.trans` module not found or failed to load. Using raw title as query.")
            initial_query = title # Fallback to raw title
        
      
        with st.spinner(f"Fetching and Summarizing Context for: '{initial_query}'..."):
            
            try:
                 # 1. Try the concise query first
                ns=nx.get_news_list(initial_query, limit=5)
            except NameError:
                st.error("Error: `nx.get_news_list` module not found or failed to load.")
                ns = []

            # 2. Add RobustnessIf no resultstry the full video title as a broad query
            if not ns:
                 # Removed st.info line as requested, using print for log only
                 print(f"INFO: Query fallback executed for video {k+1}. Retrying with full video title.")
                 
                 try:
                     # Use the full, original title as the search query
                     ns_retry=nx.get_news_list(title, limit=5) 
                     # Assign the results of the retry to ns
                     if ns_retry:
                          ns = ns_retry
                 except NameError:
                     pass

            if not ns:
                Finalaclist.append('Yellow')
                st.warning("Status: Yellow (News Context Missing/Scrape Failed)")
                k+=1
                processing_bar.progress(int((k * progress_increment)))
                continue
            
            # 3 Summarize News Content
            try:
                # The spinner is still active during this step
                newssum=sumz.sumup(ns)
            except NameError:
                newssum = "NO_NEWS_SUMMARY" # Fallback if module fails

        # -END OF SPINNER BLOCK 
        
        st.markdown(f"**{len(ns)} Related News Articles Found.** (Full article on **Current Context Report** page)")
        
        st.markdown(f"**News Summary (Mistral):**")
        st.success(newssum)

      
        #  Final Validation
   
        st.markdown("#### Final Validation Status")

        with st.spinner("Running Llama 3 for Final Validation. This might take a while..."):
            try:
                # The validator compares the claim (contentsum) against the news (newssum)
                state=idefy.validator(contentsum,newssum).strip() # .strip() ensures no leading/trailing spaces
            except NameError:
                st.error("Error: `idefy.validator` module not found or failed to load.")
                state = "YELLOW (Module Error)"
        
        
        # Clean up output and assign final status

        if "RED" in state.upper():
            Finalaclist.append('Red')
            st.error(f"Status: **RED** (Misinformation/Content Abuse Detected)")
        elif "YELLOW" in state.upper():
            Finalaclist.append('Yellow')
            st.warning(f"Status: **YELLOW** (Partial Accuracy/Discrepancies Found)")
        elif "GREEN" in state.upper():
            Finalaclist.append('Green')
            st.success(f"Status: **GREEN** (High Alignment/Accurate)")
        else:
            # Fallback for unexpected LLM output
            Finalaclist.append('Yellow')
            st.warning(f"Status: YELLOW (LLM returned ambiguous status: {state})")

        k += 1
        processing_bar.progress(int((k * progress_increment)))


#  Final Report Generation  !!!!!!!!!!


processing_bar.progress(100)

st.subheader("3. Final Account Report")
st.success(f"Analysis Complete! {len(Finalaclist)} videos processed.")

data={
    'Video Title': df['Video Title'].head(len(Finalaclist)),                      # Only include titles that were processed
    'Video Link': df['Video URL'].head(len(Finalaclist)),
    'Status': Finalaclist
}

df2 = pd.DataFrame(data)

st.write("Detail Report ")
st.dataframe(df2)
df2.to_csv(filename, index=False)

st.success(f"Report saved to **{filename}**. View full summary in the **Account Report** tab.")