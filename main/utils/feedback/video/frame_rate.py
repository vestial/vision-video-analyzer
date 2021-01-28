# Get the rating and recommendation based on the video frame rate.
def get_frame_rate_recommendation(video):
    rating = ""
    recommendation = ""
    if video.frame_rate < 24:
        rating = "Bad"
        recommendation = "Your frame rate is too low. Please increase it to at least 24 fps by changing the settings in your camera."
    elif video.frame_rate >= 24 and video.frame_rate <= 30:
        rating = "Good"
        recommendation = "Your frame rate is good. You can increase it to 60 fps if you wish to capture fast moving footages or use slow motion effects."
    elif video.frame_rate <= 60:
        rating = "Great!"
        recommendation = "Great frame rate!"
    elif video.frame_rate > 60:
        rating = "Unknown"
        recommendation = "Your frame rate might be too high. Please lower it to 30 or 24 fps if you do not use any slow motion effects."
    else:
        recommendation = "Please set your frame rate to 24, 25, 30, or 60 FPS for a standard frame rate."
    return (rating, recommendation)
