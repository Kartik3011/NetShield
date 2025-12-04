
import streamlit as st
import csv
import pandas as pd
import os 
import re 

from module import summarize as sumz 


#Cleaning Function 
def clean_video_description(description: str) -> str:
    """Removes only structural junk like hashtags and links from a description."""
    if not isinstance(description, str):
        return "Description not available or invalid format."
    
    #  Remove hashtags  #delhi etc
    cleaned_text = re.sub(r'#\w+', '', description)
    
    # 2. Remove URLs (http/https links)
    cleaned_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', cleaned_text)
    
    # 3. Structural Cleanup only (RELAXED): Remove trailing empty lines and excessive whitespace
    
    # Remove multiple empty lines
    cleaned_text = re.sub(r'\n\s*\n\s*', '\n', cleaned_text, flags=re.IGNORECASE).strip()
    
    # Remove trailing newlines/returns
    cleaned_text = re.sub(r'[\r\n]+$', '', cleaned_text).strip()
    
    # 4. Remove excessive spacing within text
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()
    
    return cleaned_text if cleaned_text else "Description contained only tags or structural junk."
# End Cleaning Function 


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
            <li>This page extracts the video Description and audio and cleans it by removing hashtags and external links.</li>
            <li>The cleaned description and the Channel Description and audio are combined, and the result is summarized to provide a concise context for manual review.</li>
            <li>The summarized description is displayed below and saved to a .txt file.</li>
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
    
    # Standardize column name extraction
    video_titles = df.iloc[:, df.columns.get_loc('Video Title')] if 'Video Title' in df.columns else df.iloc[:, 1]
    video_Link = df.iloc[:, df.columns.get_loc('Video URL')] if 'Video URL' in df.columns else df.iloc[:, 0]
    
    # Get the description column
    video_descriptions = df.iloc[:, df.columns.get_loc('Description')] if 'Description' in df.columns else pd.Series([''] * len(df))
    
    
    channel_descriptions = df.iloc[:, df.columns.get_loc('Channel Description')] if 'Channel Description' in df.columns else pd.Series([''] * len(df))
    
    if video_Link.empty or video_titles.empty:
         st.warning("The data file is empty or missing expected columns for video links and titles.")
         st.stop()


    k=0
    
    st.subheader("Transcription Results")
    st.markdown("---")
    
    # Iterate through all necessary columns
    for k, (link, title, desc, channel_desc) in enumerate(zip(video_Link, video_titles, video_descriptions, channel_descriptions)):
        
        file_name = f"summarized_content_{k}.txt" 
        
        # --- LOGIC: Clean and Summarize the content ---
        with st.spinner(f"Cleaning and Summarizing content for video {k+1}...") :
            
            
            cleaned_video_content = clean_video_description(str(desc))
            
            #Combine the cleaned video content and the channel description for a richer source text
            combined_content = f"""
            Video Description: {cleaned_video_content}
            ---
            Channel Bio/Description: {channel_desc}
            """
            
            summary_content = ""
            
            # Use a threshold: Check if the combination is meaningful ( more than 20 words)
            # This prevents wasting LLM calls on empty data
            if len(combined_content.split()) > 20 and cleaned_video_content.strip() != "Description contained only tags or structural junk.":
                try:
                    # 3. Summarize using Mistral (via sumz.sumup)
                    summary_content = sumz.sumup(combined_content)
                except Exception as sum_error:
                    st.error(f"Summarization failed: {sum_error}. Using cleaned video text instead.")
                    summary_content = cleaned_video_content
            else:
                 # If the content is too sparse use the cleaned video content as a fallback
                 summary_content = cleaned_video_content
                 
            
        # ------ 
            
        
        if summary_content and summary_content.strip() != "Description contained only tags or structural junk.":
            # Display the video header
            st.markdown(f"### Video {k+1}: {title}") 
            st.markdown(f"Video URL: `{link}`")
            
            # Display the cleaned/summarized text
            st.markdown("**Video Content (Summarized Description)**")
            
            st.text_area(f"Summary for {title}", summary_content, height=200, key=f"cleaned_desc_{k}") 
            
            if isinstance(summary_content, str):
                try:
                    # Save the summarized content
                    with open(file_name, "w", encoding="utf-8") as file:
                        file.write(summary_content) 
                    st.success(f"Content saved to {file_name}")
                except Exception as file_error:
                    st.error(f"Could not save file {file_name}: {file_error}")
        else:
            # Only display the video header/URL if the content was NOT empty
            st.markdown(f"### Video {k+1}: {title}")
            st.info("Content source was too sparse to summarize.")
            
    
        st.markdown("---") 
        

except FileNotFoundError:
    st.error("Critical error: Could not load data file.")
except Exception as e:
    st.error(f"An unhandled application error occurred: {e}")