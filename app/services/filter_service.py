def filter_videos(videos, step):
    instruction = step["instruction"].lower()
    instruction_words = set(instruction.split())

    filtered = []

    for v in videos:
        title = v["title"].lower()
        title_words = set(title.split())

        # Calculate keyword match score (0 to 1)
        matching_words = instruction_words.intersection(title_words)
        keyword_score = len(matching_words) / len(instruction_words) if instruction_words else 0

        # Must contain at least some keywords (>20% match)
        if keyword_score < 0.2:
            continue

        v["keyword_score"] = keyword_score
        filtered.append(v)

    return filtered