import assemblyai as aai
import streamlit as st
import time # Needed for polling logic

# Set the AssemblyAI API key from Streamlit secrets
try:
    aai.settings.api_key = st.secrets["ASSEMBLYAI_API_KEY"]
except KeyError:
    st.error("ASSEMBLYAI_API_KEY not found in st.secrets.")
    aai.settings.api_key = "DUMMY_KEY" 

@st.cache_data(show_spinner=False, ttl=3600)
# CRITICAL: Added cache_version=2 to force a NEW cache reset
def transcript(url, video_index, cache_version=2): 
    """
    Transcribes audio directly from a YouTube URL using AssemblyAI's remote fetching feature.
    """
    print(f"Starting remote transcription for URL: {url} (v{cache_version})")
    
    try:
        transcriber = aai.Transcriber()
        config = aai.TranscriptionConfig(language_code="en")
        
        # 1. Submit the URL for transcription
        transcript_obj = transcriber.submit(url, config=config)
        
        # 2. Poll the status for the result
        status = transcript_obj.status
        while status not in ('completed', 'error'):
            time.sleep(5)
            transcript_obj = transcriber.get_transcript(transcript_obj.id)
            status = transcript_obj.status
            print(f"Transcript ID {transcript_obj.id} status: {status}")
            
        # 3. Handle Error Status specifically
        if status == aai.TranscriptStatus.error:
             # This is the crucial debugging step: printing the specific error message
             error_details = transcript_obj.error if hasattr(transcript_obj, 'error') else "Unknown AssemblyAI Error."
             print(f"AssemblyAI FAILED with details: {error_details}")
             return f"Transcription failed with error: {error_details}"
        
        # 4. Handle Completed Status
        return transcript_obj.text if transcript_obj.text else "Transcription returned empty text."
        
    except Exception as e:
        print(f"AssemblyAI API request failed: {e}")
        return f"Transcription service error: {e}"

# No local file cleanup is needed.
