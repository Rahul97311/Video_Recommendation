import isodate

def normalize_video(video):
    duration = isodate.parse_duration(
        video["contentDetails"]["duration"]
    ).total_seconds()

    return {
        "video_id": video["id"],
        "title": video["snippet"]["title"],
        "description": video["snippet"]["description"],
        "duration": duration,
        "views": int(video["statistics"].get("viewCount", 0)),
        "url": f"https://www.youtube.com/watch?v={video['id']}"
    }