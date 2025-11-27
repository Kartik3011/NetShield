import assemblyai as aai
import streamlit as st
# The following modules are no longer required for cloud deployment
# import yt_dlp 
# import os 
# import tempfile 
# import time 

# Set the AssemblyAI API key from Streamlit secrets
try:
    aai.settings.api_key = st.secrets["ASSEMBLYAI_API_KEY"]
except KeyError:
    st.error("ASSEMBLYAI_API_KEY not found in st.secrets.")
    aai.settings.api_key = "DUMMY_KEY" 

# The local file download function has been removed.


@st.cache_data(show_spinner=False, ttl=3600)
# CRITICAL: Added cache_version=1 to force a cache reset when the code changes
def transcript(url, video_index, cache_version=1): 
    """
    Transcribes audio directly from a YouTube URL using AssemblyAI's remote fetching feature.
    """
    print(f"Starting remote transcription for URL: {url} (v{cache_version})")
    
    try:
        transcriber = aai.Transcriber()
        
        # AssemblyAI handles the media download from the URL itself, 
        # bypassing local issues like yt-dlp, cookies, and FFmpeg transcoding.
        config = aai.TranscriptionConfig(language_code="en")
        
        # Pass the URL directly to the transcribe method
        transcript_obj = transcriber.transcribe(url, config=config)
        
        if transcript_obj.status == aai.TranscriptStatus.error:
             return f"Transcription failed with error: {transcript_obj.error}"
        
        return transcript_obj.text if transcript_obj.text else "Transcription returned empty text."
        
    except Exception as e:
        print(f"AssemblyAI transcription failed: {e}")
        return f"Transcription service error: {e}"
        
# No local file cleanup is needed.
