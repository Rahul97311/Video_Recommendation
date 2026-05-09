def generate_query(step, device_os):
    instruction = step["instruction"].lower()
    title = step.get("title", "")

    if "install" in instruction:
        return f"{instruction} {device_os} tutorial"
    
    if "mount" in instruction or "place" in instruction:
        return f"{title} phone mounting setup DIY"
    
    if "connect" in instruction:
        return f"{instruction} {device_os} guide"
    
    return f"{title} DIY tutorial"