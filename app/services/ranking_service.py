def rank_videos(videos, step):
    instruction_words = step["instruction"].lower().split()

    for v in videos:
        title = v["title"].lower()

        score = 0

        for word in instruction_words:
            if word in title:
                score += 1

        # Boost important words
        if "install" in title:
            score += 3
        if "app" in title:
            score += 2
        if "alfred" in title:
            score += 5

        v["score"] = score

    return sorted(videos, key=lambda x: x["score"], reverse=True)