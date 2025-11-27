import assemblyai as aai
import streamlit as st

# Set the AssemblyAI API key from Streamlit secrets
try:
    aai.settings.api_key = st.secrets["ASSEMBLYAI_API_KEY"]
except KeyError:
    st.error("ASSEMBLYAI_API_KEY not found in st.secrets.")
    aai.settings.api_key = "DUMMY_KEY" 

# Note: The download_youtube_audio function is now completely removed.

@st.cache_data(show_spinner=False)
def transcript(url, video_index): 
    """
    Transcribes audio directly from a YouTube URL using AssemblyAI's remote fetching feature.
    """
    print(f"Starting remote transcription for URL: {url}")
    
    try:
        transcriber = aai.Transcriber()
        
        # AssemblyAI handles the media download from the URL itself.
        # This is the fix for the yt-dlp/cookie/transcoding errors.
        config = aai.TranscriptionConfig(language_code="en")
        
        # Pass the URL directly to the transcribe method
        transcript_obj = transcriber.transcribe(url, config=config)
        
        if transcript_obj.status == aai.TranscriptStatus.error:
             return f"Transcription failed with error: {transcript_obj.error}"
        
        return transcript_obj.text if transcript_obj.text else "Transcription returned empty text."
        
    except Exception as e:
        print(f"AssemblyAI transcription failed: {e}")
        return f"Transcription service error: {e}"
        
# No file cleanup or local resource management is required.
