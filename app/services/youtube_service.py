from app.services.query_service import generate_query
from app.services.filter_service import filter_videos
from app.services.ranking_service import rank_videos
from app.services.transcript_service import enrich_videos_with_transcripts
from app.services.scoring_service import score_videos_with_ai
from app.utils.video_utils import normalize_video

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"


def search_videos(query: str) -> list[str]:
    """Search YouTube and return a list of video IDs."""
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 5,
        "key": API_KEY,
    }

    res = requests.get(SEARCH_URL, params=params)
    data = res.json()

    print("\n=== YOUTUBE RESPONSE ===")
    print(data)

    return [item["id"]["videoId"] for item in data.get("items", [])]


def get_video_details(video_ids: list[str]) -> list[dict]:
    """Fetch full metadata for a list of video IDs."""
    params = {
        "part": "snippet,contentDetails,statistics",
        "id": ",".join(video_ids),
        "key": API_KEY,
    }

    res = requests.get(VIDEO_URL, params=params)
    return res.json().get("items", [])


def get_best_videos(step: dict, device_os: str) -> list[dict]:
    """
    Full pipeline:
      1. Generate a search query from the step instruction.
      2. Search YouTube and fetch video metadata.
      3. Normalise raw API responses.
      4. Filter by keyword relevance (basic sanity check).
      5. Enrich each video with its YouTube transcript.
      6. Score videos with Claude using transcript context.
      7. Re-rank combining keyword + AI scores.
      8. Return the ranked list.
    """
    query = generate_query(step, device_os)

    print("\n========================")
    print("STEP     :", step["instruction"])
    print("QUERY    :", query)

    # ── 1. Fetch video IDs ──────────────────────────────────────────────────
    video_ids = search_videos(query)
    if not video_ids:
        print("No video IDs found")
        return []

    # ── 2. Fetch metadata ───────────────────────────────────────────────────
    raw_videos = get_video_details(video_ids)

    # ── 3. Normalise ────────────────────────────────────────────────────────
    normalized = [normalize_video(v) for v in raw_videos]
    print("NORMALIZED:", [v["title"] for v in normalized])

    # ── 4. Keyword filter ───────────────────────────────────────────────────
    filtered = filter_videos(normalized, step)
    print("FILTERED  :", [v["title"] for v in filtered])

    if not filtered:
        print("Fallback: using all normalised videos")
        filtered = normalized

    # ── 5. Enrich with transcripts ──────────────────────────────────────────
    print("\n--- Fetching transcripts ---")
    enriched = enrich_videos_with_transcripts(filtered)

    # ── 6. Embeddings-based ranking ────────────────────────────────────────
    print("\n--- Embedding-Based Ranking ---")
    scored = score_videos_with_ai(step, enriched)  # Now just a passthrough
    ranked = rank_videos(scored, step)

    print("\nFINAL RANKING (by relevance score):")
    for i, v in enumerate(ranked, 1):
        print(
            f"  {i}. [{v['score']:.2f}] {v['title']} "
            f"(semantic={round(v.get('semantic_score', 0), 2)}, keyword={round(v.get('keyword_score', 0), 2)}) "
            f"| Views: {v.get('views', 0):,}"
        )

    return ranked