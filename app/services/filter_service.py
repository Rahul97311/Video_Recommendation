def filter_videos(videos, step):
    instruction = step["instruction"].lower()

    filtered = []

    for v in videos:
        title = v["title"].lower()

        # Must contain at least one key word from instruction
        if not any(word in title for word in instruction.split()):
            continue

        filtered.append(v)

    return filtered