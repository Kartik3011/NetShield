import os
import subprocess
import assemblyai as aai
import streamlit as st
import tempfile 
import yt_dlp 

# Set the AssemblyAI API key from Streamlit secrets
try:
    aai.settings.api_key = st.secrets["ASSEMBLYAI_API_KEY"]
except KeyError:
    st.error("ASSEMBLYAI_API_KEY not found in st.secrets.")
    aai.settings.api_key = "DUMMY_KEY" 

# Using the library directly avoids the 'Argument list too long' shell error.
def download_youtube_audio(youtube_url, i=0):
    
    # 1. Securely handle cookies for yt-dlp to read
    cookie_data = st.secrets["YOUTUBE_COOKIES"]
    tmp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    tmp_file.write(cookie_data)
    cookies_path = tmp_file.name
    tmp_file.close() 

    temp_dir = tempfile.gettempdir()
    # Define the fixed, simple output file path
    final_output_path = os.path.join(temp_dir, f"video_{i}_audio.mp3")

    # --- CRITICAL FIX: Use YoutubeDL class directly ---
    ydl_opts = {
        # Audio extraction options
        'format': 'bestaudio/best', 
        'extract_audio': True, 
        'audioformat': "mp3", 
        'outtmpl': final_output_path, # Define the output path template
        'noplaylist': True,
        'quiet': True, # Suppress console output for cleaner logs
        # Authentication/Cookie fix
        'cookiefile': cookies_path, 
        # Prevent Argument list too long error
        'writethumbnail': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        print(f"Downloading audio from: {youtube_url} to {final_output_path}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download the video (it will only extract and save the audio)
            ydl.download([youtube_url])
        
        print(f"Audio downloaded and saved as {final_output_path}")
        return final_output_path

    except yt_dlp.utils.DownloadError as e:
        print(f"yt-dlp Download Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during audio download setup: {e}")
        return None
    finally:
        # 3. Clean up: Delete the temporary cookies file
        if os.path.exists(cookies_path):
            os.remove(cookies_path)


# --- The transcript function (remains the same as previous fix) ---
@st.cache_data(show_spinner=False)
def transcript(url, video_index):
    """
    Downloads audio and transcribes it using AssemblyAI.
    """
    print(f"Starting transcription for video index: {video_index}")
    
    # 1. Download the audio file
    audio_path = download_youtube_audio(url, i=video_index)
    
    if not audio_path or not os.path.exists(audio_path):
        return "Audio download failed."
        
    try:
        # 2. Upload the audio file to AssemblyAI
        transcriber = aai.Transcriber()
        config = aai.TranscriptionConfig(language_code="en")
        
        # 3. Perform the transcription
        transcript_obj = transcriber.transcribe(audio_path, config=config)
        
        if transcript_obj.status == aai.TranscriptStatus.error:
             return f"Transcription failed with error: {transcript_obj.error}"
        
        return transcript_obj.text if transcript_obj.text else "Transcription returned empty text."
        
    except Exception as e:
        print(f"AssemblyAI transcription failed: {e}")
        return f"Transcription service error: {e}"
        
    finally:
        # 5. Clean up the downloaded audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)
