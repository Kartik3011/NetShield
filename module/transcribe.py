import os
import subprocess
import assemblyai as aai
import streamlit as st
import tempfile 
import time

# ... (API Key setup remains the same) ...
# Set the AssemblyAI API key from Streamlit secrets
try:
    aai.settings.api_key = st.secrets["ASSEMBLYAI_API_KEY"]
except KeyError:
    st.error("ASSEMBLYAI_API_KEY not found in st.secrets.")
    aai.settings.api_key = "DUMMY_KEY" 


def download_youtube_audio(youtube_url, i=0):
    
    # 1. Securely handle cookies
    cookie_data = st.secrets["YOUTUBE_COOKIES"]
    tmp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    tmp_file.write(cookie_data)
    cookies_path = tmp_file.name
    tmp_file.close() 

    temp_dir = tempfile.gettempdir()
    # Use a simpler, non-dynamic output path for the final file
    final_output_path = os.path.join(temp_dir, f"video_{i}_audio.mp3")

    try:
        print(f"Downloading audio from: {youtube_url}")
        
        # --- CRITICAL FIX: MINIMIZE ARGUMENTS AND USE KNOWN OUTPUT PATH ---
        command = [
            "yt-dlp",
            "--cookies", cookies_path,        # Authentication fix
            "-f", "bestaudio/best",           # Select best audio stream
            "--extract-audio",                # Extract audio
            "--audio-format", "mp3",          # Convert to MP3
            "-o", final_output_path,          # Force output to the fixed path
            youtube_url
        ]
        
        # Use shell=False (default) and ensure stdout/stderr are hidden for cleaner output
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"Audio downloaded and saved as {final_output_path}")
        return final_output_path

    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during audio download setup: {e}")
        return None
    finally:
        # 3. Clean up: Delete the temporary cookies file
        if os.path.exists(cookies_path):
            os.remove(cookies_path)


# --- (The transcript function added in the previous response goes here) ---
@st.cache_data(show_spinner=False)
def transcript(url, video_index):
    # ... (content of this function remains the same, using the fixed download_youtube_audio)
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
