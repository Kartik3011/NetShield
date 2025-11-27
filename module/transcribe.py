import assemblyai as aai
import streamlit as st
# import yt_dlp # CRITICAL: No longer needed!
# import os 
# import tempfile 
# import time 

# Set the AssemblyAI API key from Streamlit secrets
try:
    aai.settings.api_key = st.secrets["ASSEMBLYAI_API_KEY"]
except KeyError:
    # Handle this gracefully if key is missing, though Streamlit will error later
    st.error("ASSEMBLYAI_API_KEY not found in st.secrets.")
    aai.settings.api_key = "DUMMY_KEY" 


# Remove the download_youtube_audio function completely.


@st.cache_data(show_spinner=False)
def transcript(url, video_index): # video_index is kept to align with calling code but is now redundant for caching
    """
    Transcribes audio directly from a YouTube URL using AssemblyAI.
    """
    print(f"Starting remote transcription for URL: {url}")
    
    # 1. Configuration for transcription
    try:
        transcriber = aai.Transcriber()
        
        # NOTE: AssemblyAI handles the media download from the URL itself, 
        # bypassing local issues and the need for yt-dlp/cookies.
        config = aai.TranscriptionConfig(language_code="en")
        
        # CRITICAL: Pass the URL directly to the transcribe method
        transcript_obj = transcriber.transcribe(url, config=config)
        
        if transcript_obj.status == aai.TranscriptStatus.error:
             return f"Transcription failed with error: {transcript_obj.error}"
        
        return transcript_obj.text if transcript_obj.text else "Transcription returned empty text."
        
    except Exception as e:
        print(f"AssemblyAI transcription failed: {e}")
        return f"Transcription service error: {e}"
        
# 2. No 'finally' block needed, as no local files are created!
