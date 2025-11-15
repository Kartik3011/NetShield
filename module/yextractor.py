# FULL WORKING moduleytextrator

import csv
from googleapiclient.discovery import build
from datetime import datetime
import streamlit as st 


api_key = st.secrets["YOUTUBE_API_KEY"] 
youtube = build('youtube', 'v3', developerKey=api_key)

def videoData(video_id):

    try:
        request = youtube.videos().list(
            part="statistics",
            id=video_id
        )
        response = request.execute()

        # Video statistics
        video_stats = response['items'][0]['statistics']
        views = int(video_stats.get('viewCount', 0))
        likes = int(video_stats.get('likeCount', 0))
        dislikes = int(video_stats.get('dislikeCount', 0))
        comment_count = int(video_stats.get('commentCount', 0))

        return views, likes, dislikes, comment_count

    except Exception as e:
        print(f"Error fetching statistics for video {video_id}: {e}")
        return None, None, None, None

def channelData(channel_id):

    try:
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()

        # Channel metadata
        channel_info = response['items'][0]
        channel_title = channel_info['snippet']['title']
        channel_id = channel_info['id']
        channel_description = channel_info['snippet']['description']
        subscriber_count = channel_info['statistics'].get('subscriberCount', 'N/A')
        total_views = channel_info['statistics'].get('viewCount', 'N/A')
        video_count = channel_info['statistics'].get('videoCount', 'N/A')

        return channel_title, channel_id, subscriber_count, total_views, video_count, channel_description

    except Exception as e:
        print(f"Error fetching metadata for channel {channel_id}: {e}")
        return None, None, None, None, None, None

def video_info(hashtag, latitude, longitude, radius='50km', max_results=10, start_date=None, end_date=None, csv_filename="video_data.csv"):

    try:
        next_page_token = None
        video_count = 0  # Track the total number of videos processed

        # Save to CSV file
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Video Title', 'Description', 'Video URL', 'Published At',
                'Channel Title', 'Channel ID', 'Channel Description', 'Subscriber Count',
                'Total Views', 'Video Count', 'Views', 'Likes', 'Dislikes', 'Comments',
                'Channel URL'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            while video_count < max_results:
                request = youtube.search().list(
                    part="snippet",
                    q=hashtag,
                    type="video",
                    location=f"{latitude},{longitude}",
                    locationRadius=radius,
                    maxResults=min(50, max_results - video_count),  # Request only remaining videos
                    pageToken=next_page_token,
                    publishedAfter=start_date.strftime('%Y-%m-%dT%H:%M:%SZ') if start_date else None,
                    publishedBefore=end_date.strftime('%Y-%m-%dT%H:%M:%SZ') if end_date else None,
                )
                response = request.execute()

                for item in response.get('items', []):
                    if video_count >= max_results:
                        break  # Stop once max_results is reached

                    video_title = item['snippet']['title']
                    video_description = item['snippet']['description']
                    video_id = item['id']['videoId']
                    published_at = item['snippet']['publishedAt']
                    channel_title = item['snippet']['channelTitle']
                    channel_id = item['snippet']['channelId']

                    # Convert the publishedAt to datetime
                    published_datetime = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')

                    # Filter by the date range if specified
                    if start_date and end_date:
                        if not (start_date <= published_datetime <= end_date):
                            continue

                    # Get video statistics (views, likes, dislikes, comments)
                    views, likes, dislikes, comment_count = videoData(video_id)

                    # Channel metadata
                    channel_data = channelData(channel_id)
                    if channel_data[0] is None:
                        continue
                    channel_title, channel_id, subscriber_count, total_views, video_count_data, channel_description = channel_data

                    # Print video details
                    print(f"Video {video_count + 1}:")
                    print(f"Title: {video_title}")
                    print(f"Description: {video_description}")
                    print(f"Video URL: https://www.youtube.com/watch?v={video_id}")
                    print(f"Published At: {published_at}")
                    print(f"Channel: {channel_title}")
                    print(f"Channel URL: https://www.youtube.com/channel/{channel_id}")
                    print(f"Channel Description: {channel_description}")
                    print(f"Social Blade: https://socialblade.com/youtube/channel/{channel_id}")
                    print(f"Subscriber Count: {subscriber_count}")
                    print(f"Total Views: {total_views}")
                    print(f"Video Count: {video_count_data}")
                    print(f"Views: {views}")
                    print(f"Likes: {likes}")
                    print(f"Comments: {comment_count}\n")

                    # Write the video and channel details to the CSV file
                    writer.writerow({
                        'Video Title': video_title,
                        'Description': video_description,
                        'Video URL': f'https://www.youtube.com/watch?v={video_id}',
                        'Published At': published_at,
                        'Channel Title': channel_title,
                        'Channel ID': channel_id,
                        'Channel Description': channel_description,
                        'Subscriber Count': str(subscriber_count),
                        'Total Views': str(total_views),
                        'Video Count': str(video_count_data),
                        'Views': str(views),
                        'Likes': str(likes),
                        'Dislikes': str(dislikes),
                        'Comments': str(comment_count),
                        'Channel URL': f'https://www.youtube.com/channel/{channel_id}'
                    })

                    video_count += 1  # Increment video count

                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break  

    except Exception as e:
        print(f"Error: {e}")



def total_videos_on_topic(hashtag, start_date=None, end_date=None, max_results=50):
# ... (function body is unchanged)
    
    try:
        total_videos = 0
        next_page_token = None

        while True:
            request = youtube.search().list(
                part="snippet",
                q=hashtag,
                type="video",
                maxResults=max_results,
                pageToken=next_page_token,
                publishedAfter=start_date.strftime('%Y-%m-%dT%H:%M:%SZ') if start_date else None,
                publishedBefore=end_date.strftime('%Y-%m-%dT%H:%M:%SZ') if end_date else None,
            )
            response = request.execute()

            total_videos += len(response.get('items', []))
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        print(f"Total videos for the topic '{hashtag}' in the given period: {total_videos}")
        return total_videos
    except Exception as e:
        print(f"Error : {e}")
        return 0



if __name__ == "__main__":
# ... (if __name__ is unchanged)
    hashtag = input("Enter the hashtag to search for: ")
    latitude = float(input("Enter the latitude: "))
    longitude = float(input("Enter the longitude: "))
    radius = input("Enter the radius (e.g., '50km', '1000m'): ") or '50km'
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    max_results = int(input("Enter the number of videos to fetch: "))

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    video_info(hashtag, latitude, longitude, radius, max_results, start_date, end_date)
    total_videos = total_videos_on_topic(hashtag, start_date, end_date)
