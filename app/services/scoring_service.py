# Embeddings-based scoring service (replaces Claude)
# Uses semantic similarity for all scoring

def score_videos_with_ai(step: dict, videos: list[dict]) -> list[dict]:
    """
    Placeholder function for compatibility.
    All scoring is now done via embeddings in ranking_service.py.
    This function simply returns videos unchanged.

    Args:
        step   : The current step dict (keys: title, instruction, step_id).
        videos : Normalised + transcript-enriched video dicts.

    Returns:
        The same list (no changes needed as embeddings are used instead).
    """
    print("[scoring_service] Using embeddings-based scoring (Claude removed)")
    return videos