import streamlit as st
import os
import tempfile
from openai import OpenAI # New dependency for Whisper
import yt_dlp # Re-introducing for local download

# Ensure your OPENAI_API_KEY is available in Streamlit secrets
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except KeyError:
    st.error("OPENAI_API_KEY not found in st.secrets.")
    client = None

# --- NEW FUNCTION: Simplified Audio Download ---
def download_youtube_audio_local(youtube_url, i=0):
    """
    Downloads audio from a YouTube URL to a local temporary file using yt-dlp.
    Bypasses cookie logic to test a clean local download path.
    """
    if not client: return None
    
    temp_dir = tempfile.gettempdir()
    final_output_path = os.path.join(temp_dir, f"video_{i}_audio.mp3")

    try:
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio', 
            'extract_audio': True, 
            'audioformat': "mp3", 
            'outtmpl': final_output_path, 
            'noplaylist': True,
            'quiet': True,
            # CRITICAL: Removing 'cookiefile' option from the old code
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        
        if os.path.exists(final_output_path):
            print(f"Audio downloaded locally to {final_output_path}")
            return final_output_path
        else:
            return None

    except Exception as e:
        print(f"yt-dlp Local Download Error: {e}")
        return None
# -----------------------------------------------


@st.cache_data(show_spinner=False, ttl=3600)
# CRITICAL: Use cache_version=3 to definitively bust the old cache
def transcript(url, video_index, cache_version=3): 
    """
    Downloads audio locally and transcribes it using OpenAI Whisper API.
    """
    if not client: return "OpenAI client not initialized (API key missing)."
    
    print(f"Starting local download & Whisper transcription for URL: {url} (v{cache_version})")
    audio_path = None
    
    try:
        # 1. Local Download Attempt
        audio_path = download_youtube_audio_local(url, i=video_index)
        
        if not audio_path or not os.path.exists(audio_path):
            return "Local audio download failed (yt-dlp or FFmpeg failure)."
            
        # 2. Whisper API Transcription (requires file object)
        with open(audio_path, "rb") as audio_file:
            transcript_obj = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text"
            )
        
        return transcript_obj
        
    except Exception as e:
        print(f"Whisper API transcription failed: {e}")
        return f"Whisper API service error: {e}"
        
    finally:
        # 3. Clean up the local file
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"Cleaned up local file: {audio_path}")
