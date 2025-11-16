import os
import assemblyai as aai
import streamlit as st
import tempfile 
import yt_dlp # CRITICAL: Direct import to bypass subprocess/shell errors
import time # Time import is needed for the sleep function

# Set the AssemblyAI API key from Streamlit secrets
try:
    aai.settings.api_key = st.secrets["ASSEMBLYAI_API_KEY"]
except KeyError:
    st.error("ASSEMBLYAI_API_KEY not found in st.secrets.")
    aai.settings.api_key = "DUMMY_KEY" 

# --- NEW FUNCTION TO CLEAN COOKIE DATA ---
def clean_cookies(raw_cookies: str) -> str:
    """Aggressively cleans the cookie string to ensure Netscape format integrity."""
    
    lines = raw_cookies.splitlines()
    cleaned_lines = []
    
    # Preserve the required Netscape headers and valid cookie lines
    for line in lines:
        stripped_line = line.strip()
        # Keep non-empty lines that are either comments (#) or start with a domain (.youtube.com)
        if stripped_line and (stripped_line.startswith('#') or stripped_line.startswith('.')):
             cleaned_lines.append(line) # Keep the original line spacing/tabs
             
    # Join them back together with a standard newline
    return '\n'.join(cleaned_lines)
# ----------------------------------------


def download_youtube_audio(youtube_url, i=0):
    
    temp_dir = tempfile.gettempdir()
    cookies_path = os.path.join(temp_dir, f"cookies_{i}.txt")
    final_output_path = os.path.join(temp_dir, f"video_{i}_audio.mp3")

    try:
        # 1. Retrieve raw cookie data
        raw_cookie_data = st.secrets["YOUTUBE_COOKIES"]
        
        # 2. Clean the cookie data
        cleaned_cookie_data = clean_cookies(raw_cookie_data)
        
        # 3. Write cleaned cookie data to ensure Netscape format integrity
        with open(cookies_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_cookie_data)
            
        # 4. Configuration for yt-dlp library
        ydl_opts = {
            'format': 'bestaudio/best', 
            'extract_audio': True, 
            'audioformat': "mp3", 
            'outtmpl': final_output_path, 
            'noplaylist': True,
            'quiet': True,
            'cookiefile': cookies_path, 
            'writethumbnail': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        print(f"Downloading audio from: {youtube_url} to {final_output_path}")
        
        # 5. Execute download using the yt-dlp library
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        
        
        # 6. CRITICAL FINAL CHECK: Verify file existence
        if os.path.exists(final_output_path):
            print(f"Audio downloaded and saved as {final_output_path}")
            return final_output_path
        else:
            print(f"Download completed, but final file not found at {final_output_path}.")
            return None

    except yt_dlp.utils.DownloadError as e:
        print(f"yt-dlp Download Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during audio download setup: {e}")
        return None
    finally:
        # 7. Clean up: Delete the temporary cookies file
        if os.path.exists(cookies_path):
            os.remove(cookies_path)


# This function was missing in the original module, causing the initial AttributeError
@st.cache_data(show_spinner=False)
def transcript(url, video_index):
    """
    Downloads audio and transcribes it using AssemblyAI.
    """
    print(f"Starting transcription for video index: {video_index}")
    
    # 1. Download the audio file using the fixed function
    audio_path = download_youtube_audio(url, i=video_index)
    
    if not audio_path or not os.path.exists(audio_path):
        return "Audio download failed."
        
    try:
        # 2. Perform the transcription
        transcriber = aai.Transcriber()
        config = aai.TranscriptionConfig(language_code="en")
        
        transcript_obj = transcriber.transcribe(audio_path, config=config)
        
        if transcript_obj.status == aai.TranscriptStatus.error:
             return f"Transcription failed with error: {transcript_obj.error}"
        
        return transcript_obj.text if transcript_obj.text else "Transcription returned empty text."
        
    except Exception as e:
        print(f"AssemblyAI transcription failed: {e}")
        return f"Transcription service error: {e}"
        
    finally:
        # 3. Clean up the downloaded audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)
