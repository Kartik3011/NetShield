import os
import subprocess
import assemblyai as aai
import streamlit as st
import tempfile 
import time # Added import for delay and polling (best practice)

# Set the AssemblyAI API key from Streamlit secrets
try:
    aai.settings.api_key = st.secrets["ASSEMBLYAI_API_KEY"]
except KeyError:
    st.error("ASSEMBLYAI_API_KEY not found in st.secrets.")
    # Set a dummy key to avoid import error, but transcription will fail
    aai.settings.api_key = "DUMMY_KEY" 
    
def download_youtube_audio(youtube_url, output_path="audio.mp3", i=0):
    # ... (Keep the existing implementation of this function) ...
    cookie_data = st.secrets["YOUTUBE_COOKIES"]
    tmp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    tmp_file.write(cookie_data)
    cookies_path = tmp_file.name
    tmp_file.close() 

    try:
        print(f"Downloading audio from: {youtube_url}")
        temp_dir = tempfile.gettempdir()
        final_output_path_cmd = os.path.join(temp_dir, f"{i}downloaded_audio.mp3")

        command = [
            "yt-dlp",
            "--cookies", cookies_path,        
            "-f", "bestaudio/best",
            "--extract-audio",
            "--audio-format", "mp3",
            "-o", final_output_path_cmd,
            youtube_url
        ]
        
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Audio downloaded and saved as {final_output_path_cmd}")
        return final_output_path_cmd

    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during audio download setup: {e}")
        return None
    finally:
        if os.path.exists(cookies_path):
            os.remove(cookies_path)


# --- FIX: ADD THE MISSING 'transcript' FUNCTION ---
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
        # Using aai.Transcriber() for a clear pipeline
        transcriber = aai.Transcriber()
        
        # 3. Create a Transcription config (optional, but good practice)
        config = aai.TranscriptionConfig(language_code="en")
        
        # 4. Perform the transcription
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
