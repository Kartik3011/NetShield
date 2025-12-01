import streamlit as st
import csv
from module import nextractor as nx
import pandas as pd
from module import transcribe as ts
import os 

st.set_page_config(page_title="Content Forensic", layout="wide", initial_sidebar_state="expanded")

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
        
        /* New custom style for the Description Box (Warning/Info style) */
        .forensic-description-box {
            background-color: #333d47; /* Slightly lighter dark background */
            padding: 15px;
            border-radius: 5px;
            border-left: 5px solid #ffa500; /* Orange/Warning accent */
            margin-bottom: 30px; /* Space after the description box */
        }
        
        .forensic-description-box ul {
            /* Ensures list starts cleanly inside the box */
            margin: 5px 0 0 0; 
            color: #f0f0f0; /* Light text color */
            padding-left: 20px;
            list-style-type: disc;
        }
        
        .forensic-description-box strong {
            color: #ffffff; /* White text for bold elements */
            font-size: 16px;
            display: block; /* Allows margin-bottom to work on the heading */
            margin-bottom: 5px; /* Adds space after the heading */
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div style="display: none;">
        NetShield🛡️
    </div>
""", unsafe_allow_html=True)



st.title("Content Forensic")


st.markdown("""
    <div class="forensic-description-box">
        <strong style="font-size: 18px;">Forensic Analysis Overview </strong>
        <ul style="font-size: 16px; margin: 0; color: #fff; padding-left: 20px;">
            <li>This page performs content analysis by extracting transcripts from each video link.</li>
            <li>The process utilizes different LLMs and may take a significant amount of time to complete.</li>
            <li>Results are displayed below, where the speech content of each video is shown and saved to a .txt file.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)



# Page Logic
try:
    file_path = os.path.join(os.getcwd(), "video_data.csv") 
    
    if not os.path.exists(file_path):
        st.error("Data file (video_data.csv) not found. Please ensure data has been fetched on the previous analysis page.")
        st.stop()
        
    df = pd.read_csv(file_path) 
    
    # Standardize column name
    video_titles = df.iloc[:, df.columns.get_loc('Video Title')] if 'Video Title' in df.columns else df.iloc[:, 1]
    video_Link = df.iloc[:, df.columns.get_loc('Video URL')] if 'Video URL' in df.columns else df.iloc[:, 0]
    
    if video_Link.empty or video_titles.empty:
         st.warning("The data file is empty or missing expected columns for video links and titles.")
         st.stop()


    k=0
    
    st.subheader("Transcript Extraction Results")
    st.markdown("---")
    
    for i,j in zip(video_Link,video_titles):
        file_name = f"transcript_{k}.txt" 
        
        #  START OF VIDEO BLOCK 
        st.markdown(f"### Video {k+1}: {j}") 
        st.markdown(f"Video URL: `{i}`")
        
        # Ensure transcribe module is available and works as expected
        try:
            #loading incdicator
            with st.spinner(f"Downloading and transcribing video {k+1}. This might take a while for longer videos...") :
                content = ts.transcript(i,k) 
            # --- END 
        except Exception as e:
            content = None
            st.error(f"An unexpected error occurred during transcription setup for video '{j}': {e}")
            
        
        if content is not None and content.strip():
            st.markdown("**Video Content (Transcript)**")
            
            # imppp: We keep the unique key here to avoid the Streamlit widget error.
            st.text_area(f"Transcript for {j}", content, height=200, key=f"transcript_{k}") 
            
            if isinstance(content, str):
                try:
                    # RESTORED ORIGINAL LOCAL FILE SAVING LOGIC 
                    with open(file_name, "w", encoding="utf-8") as file:
                        file.write(content)
                    st.success(f"Transcript saved to {file_name}")
                except Exception as file_error:
                    st.error(f"Could not save file {file_name}: {file_error}")
        else:
            st.info("Transcript not available for this video (or returned empty content).")
            
    
        st.markdown("---") 
        
        k = k + 1

except FileNotFoundError:
    st.error("Critical error: Could not load data file.")
except Exception as e:
    st.error(f"An unhandled application error occurred: {e}")