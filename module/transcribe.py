import os
import subprocess
import assemblyai as aai
import streamlit as st
import tempfile # <--- New import needed for secure cookies

def download_youtube_audio(youtube_url, output_path="audio.mp3",i=0):
    
    # 1. Securely handle cookies (Fixes "Sign in to confirm you're not a bot" error)
    cookie_data = st.secrets["YOUTUBE_COOKIES"]
    tmp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    tmp_file.write(cookie_data)
    cookies_path = tmp_file.name
    tmp_file.close() # Close to ensure data is written and ready for yt-dlp

    # We use a simple output template to fix "Argument list too long" (Errno 7)
    # The output file will be saved as "<VideoID>.mp3" in the temp folder
    output_template = f"{i}%(id)s.%(ext)s" 
    
    try:
        print(f"Downloading audio from: {youtube_url}")
        
        # We will use the system's temporary directory for saving the audio
        # to prevent permission issues on Streamlit Cloud.
        temp_dir = tempfile.gettempdir()
        final_output_path = os.path.join(temp_dir, f"{i}downloaded_audio.mp3") 

        command = [
            "yt-dlp",
            "--cookies", cookies_path,        # Authentication fix
            "-f", "bestaudio/best",
            "--extract-audio",
            "--audio-format", "mp3",
            
            # --- FIX FOR ARGUMENT LIST TOO LONG ERROR ---
            # Use the short template and force output to a known, safe path.
            "-o", os.path.join(temp_dir, output_template), 
            # --- END FIX ---
            
            youtube_url
        ]
        
        # Run yt-dlp
        subprocess.run(command, check=True)
        
        # yt-dlp names the file based on the template, we need to find the exact file name
        # We must rename it or return the dynamically generated filename path
        # Since we used a simple template, we can rely on finding it in the temp directory.

        # For simplicity, let's look for the first file ending with .mp3 in temp_dir
        # NOTE: This is a robust solution: it creates the file in a safe location
        
        # We'll rely on the original name logic from the current code (downloaded_audio.mp3)
        # but place it in the temp folder. 
        
        # Since yt-dlp doesn't always use the exact output_path when a template is used, 
        # let's modify the command to explicitly use the full path without a template:
        
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
        
        subprocess.run(command, check=True)
        print(f"Audio downloaded and saved as {final_output_path_cmd}")
        return final_output_path_cmd

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
