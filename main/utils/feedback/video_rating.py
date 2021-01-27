def get_resolution_rating(video):
    result = ""

    return result


def get_frame_rate_rating(video):
    result = ""
    if video.frame_rate < 24:
        result = "Bad"
    elif video.frame_rate >= 24 and video.frame_rate <= 30:
        result = "Good"
    elif video.frame_rate <= 60:
        result = "Great!"
    else:
        result = "Unknown"
    return result
