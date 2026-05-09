from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound


def get_transcript(video_id: str, max_chars: int = 1500) -> str | None:
    """
    Fetch the transcript for a YouTube video.

    Args:
        video_id: The YouTube video ID (e.g. 'dQw4w9WgXcQ').
        max_chars: Truncate the joined transcript to this many characters
                   so it stays within a reasonable context window.

    Returns:
        A plain-text transcript string, or None if unavailable.
    """
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.fetch(video_id, languages=["en"])
        text = " ".join(entry.text for entry in transcript_list)
        return text[:max_chars]
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception as e:
        print(f"[transcript_service] Unexpected error for video {video_id}: {e}")
        return None


def enrich_videos_with_transcripts(videos: list[dict]) -> list[dict]:
    """
    Attach a 'transcript' field to each video dict in-place.

    Args:
        videos: List of normalised video dicts (must contain 'video_id').

    Returns:
        The same list with a 'transcript' key added to each item
        (value is a string or None).
    """
    for video in videos:
        video_id = video.get("video_id")
        if video_id:
            transcript = get_transcript(video_id)
            video["transcript"] = transcript
            if transcript:
                print(f"[transcript_service] Got transcript for {video_id} ({len(transcript)} chars)")
            else:
                print(f"[transcript_service] No transcript for {video_id}")
        else:
            video["transcript"] = None

    return videos