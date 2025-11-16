import os
import subprocess
import assemblyai as aai
import streamlit as st


def download_youtube_audio(youtube_url, output_path="audio.mp3",i=0):

    try:
        print(f"Downloading audio from: {youtube_url}")
        output_path=f"{i}{output_path}"
        
        command = [
            "yt-dlp",
            "-f", "bestaudio/best",
            "--extract-audio",
            "--audio-format", "mp3",
            "--output", output_path,
            youtube_url
        ]
        subprocess.run(command, check=True)
        print(f"Audio downloaded and saved as {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        return None

def transcribe_audio(file_path):
    try:
        aai.settings.api_key = st.secrets["ASSEMBLYAI_API_KEY"]  

        # enable Automatic Language Detection
        config = aai.TranscriptionConfig(language_detection=True)
        transcriber = aai.Transcriber(config=config)

        print("Uploading audio to AssemblyAI for transcription...")
        transcript = transcriber.transcribe(file_path)

        if transcript.status == aai.TranscriptStatus.error:
            print(f"Transcription error: {transcript.error}")
        else:
            print("Transcription completed successfully.")
            return transcript.text
    except Exception as e:
        print(f"Error in transcription: {e}")
        return None

# main func that handles transcription processs

def transcript(url,i):

    youtube_url = url
    audio_path = "downloaded_audio.mp3"

    # Download yt audio
    audio_file = download_youtube_audio(youtube_url, audio_path,i)

    if audio_file:
        transcript = transcribe_audio(audio_file)
        if transcript:
            print("Transcript:")
            print(transcript)
            tt=transcript
            return tt

'''
if __name__ == "__main__":
# ... (if __name__ is unchanged)
    youtube_url = input("Enter the YouTube video URL: ")
    audio_path = "downloaded_audio.mp3"

    # Download YouTube audio
    audio_file = download_youtube_audio(youtube_url, audio_path)

    if audio_file:
        # Transcribe the downloaded audio
        transcript = transcribe_audio(audio_file)
        if transcript:
            print("Transcript:")
            print(transcript)
'''