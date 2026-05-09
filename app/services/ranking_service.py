from app.services.embedding_service import semantic_score


def rank_videos(videos, step):

    instruction = step["instruction"]

    ranked = []

    print("\n--- EMBEDDINGS SCORING ---")

    for video in videos:

        # Combine all useful text
        video_text = f"""
        {video.get('title', '')}
        {video.get('description', '')}
        {video.get('transcript', '')}
        """

        # Embedding similarity (0 to 1)
        semantic_score_val = semantic_score(
            instruction,
            video_text
        )
        video["semantic_score"] = semantic_score_val

        # Get keyword score (already computed in filter_service, default to 0.5)
        keyword_score_val = video.get("keyword_score", 0.5)

        # Combine scores: 70% semantic, 30% keyword relevance
        combined_score = (semantic_score_val * 0.7) + (keyword_score_val * 0.3)
        video["score"] = combined_score

        print(f"[{round(combined_score, 3)}] {video['title']} (semantic={round(semantic_score_val, 3)}, keyword={round(keyword_score_val, 3)})")

        ranked.append(video)

    # Sort highest first
    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked