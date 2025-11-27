import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

# You should have already installed 'youtube-transcript-api' in requirements.txt

# --- Utility to safely extract Video ID from URL ---
def get_video_id(url):
    """Extracts the 11-character YouTube video ID from a URL."""
    regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

# --- New Transcription Function using Subtitles ---
@st.cache_data(show_spinner=False, ttl=3600) 
def transcript(url, video_index): 
    """
    Fetches the video's transcript/captions directly from YouTube's API.
    """
    print(f"Starting Subtitle Extraction for URL: {url}")
    
    video_id = get_video_id(url)
    if not video_id:
        return f"Error: Invalid YouTube URL format detected for index {video_index}."

    try:
        # Fetch the transcript list for the video ID
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi', 'ur'])
        
        # Combine the list of dictionaries into a single text string
        full_transcript = ' '.join([item['text'] for item in transcript_list])
        
        return full_transcript if full_transcript else "Transcript returned empty content (No subtitles available)."

    except NoTranscriptFound:
        print(f"No subtitles found for video ID: {video_id}")
        return "Transcription failed: No English, Hindi, or Urdu subtitles/captions found for this video."

    except Exception as e:
        print(f"Subtitle API failed: {e}")
        return f"Transcription service error: {e}"
