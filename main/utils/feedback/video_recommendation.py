import numpy as np


def get_resolution_recommendation(video):
    rating = ""
    recommendation = ""
    resolution = video.resolution.split('x')
    resolution = list(map(int, resolution))
    if resolution[1] >= 1080 and resolution[1] <= 2160:  #Between 1080p and 4k
        rating = "Great!"
        resolution = "Great video resolution!"
    elif resolution[1] >= 720 and resolution[1] < 1080:  #Between 720p and 1080p
        rating = "Okay"
        recommendation = "Your resolution is okay. However, you can still improve it by increasing the resolution to 1080p."
    elif resolution[1] < 720:  #Below 720p
        rating = "Bad"
        recommendation = "Your resolution is too low. Please increase it to at least 720p."
    else:
        result = "Okay"
        resolution = "Your video resolution might be too high. Try lowering it to at least 4k to increase support for more devices and reduce bandwidth usage."
    return (rating, recommendation)


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
