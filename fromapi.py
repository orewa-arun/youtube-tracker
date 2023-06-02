import re
from googleapiclient.discovery import build
from dotenv import dotenv_values

cloud_key = dotenv_values(".env")['GOOGLE_CLOUD_API_KEY']

youtube = build('youtube', 'v3', developerKey=cloud_key)


def get_video_views(video_id):
    # Send a request to the API to retrieve video details
    response = youtube.videos().list(
        part='statistics',
        id=video_id
    ).execute()

    # Extract the view count from the response
    items = response.get('items', [])
    if items:
        stats = items[0]['statistics']
        view_count = stats["viewCount"]
        like_count = stats["likeCount"]
        comment_count = stats["commentCount"]

        return (view_count, like_count, comment_count)


def get_video_id(url):
    # Regular expression pattern to match YouTube video ID
    pattern = r'(?:v=|youtu\.be\/|v\/|\/v\/|youtu\.be\/|embed\/|watch\?v=|embed\/|watch\?feature=player_embedded&v=|watch\?v=)([\w-]+)'

    # Find the video ID using the pattern
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        print("Invalid YouTube URL.")


# Replace with the actual YouTube video URL
video_url = "https://www.youtube.com/watch?v=0aavCtXiiX4"
video_id = get_video_id(video_url)
views = get_video_views(video_id)
if views:
    print("Number of views:", views)
