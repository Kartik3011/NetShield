import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

# We no longer need assemblyai, openai, yt_dlp, or os/tempfile imports for this method.

# --- Utility to safely extract Video ID from URL ---
def get_video_id(url):
    """Extracts the 11-character YouTube video ID from a URL."""
    # Regex that captures the video ID from standard watch and short youtu.be URLs
    regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

# --- New Transcription Function using Subtitles ---
@st.cache_data(show_spinner=False, ttl=3600)
# CRITICAL: Use cache_version=5 to definitively bust the old failed cache
def transcript(url, video_index, cache_version=5): 
    """
    Fetches the video's transcript/captions directly from YouTube's API.
    Bypasses the 403 Forbidden error caused by audio streaming.
    """
    print(f"Starting Subtitle Extraction for URL: {url} (v{cache_version})")
    
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
        # This error occurs if the video has no manual or auto-generated subtitles
        print(f"No subtitles found for video ID: {video_id}")
        return "Transcription failed: No English, Hindi, or Urdu subtitles/captions found for this video."

    except Exception as e:
        print(f"Subtitle API failed: {e}")
        return f"Transcription service error: {e}"
