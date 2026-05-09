from app.services.query_service import generate_query
from app.services.filter_service import filter_videos
from app.services.ranking_service import rank_videos
from app.utils.video_utils import normalize_video

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"

def search_videos(query):
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 5,
        "key": API_KEY
    }

    res = requests.get(SEARCH_URL, params=params)
    data = res.json()

    print("\n=== YOUTUBE RESPONSE ===")
    print(data)

    return [item["id"]["videoId"] for item in data["items"]]

def get_video_details(video_ids):
    params = {
        "part": "snippet,contentDetails,statistics",
        "id": ",".join(video_ids),
        "key": API_KEY
    }

    res = requests.get(VIDEO_URL, params=params)
    return res.json()["items"]

def get_best_videos(step, device_os):
    query = generate_query(step, device_os)

    print("\n========================")
    print("STEP:", step["instruction"])
    print("QUERY:", query)

    video_ids = search_videos(query)

    if not video_ids:
        print("No video IDs found")
        return []

    raw_videos = get_video_details(video_ids)

    normalized = [normalize_video(v) for v in raw_videos]

    print("NORMALIZED:", [v["title"] for v in normalized])

    filtered = filter_videos(normalized, step)

    print("FILTERED:", [v["title"] for v in filtered])

    if not filtered:
        print("Fallback triggered")
        filtered = normalized

    ranked = rank_videos(filtered, step)

    print("FINAL:", [v["title"] for v in ranked])

    return ranked