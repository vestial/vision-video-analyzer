import numpy as np


def get_resolution_recommendation(video):
    rating = ""
    recommendation = ""
    resolution = video.resolution.split('x')
    resolution = list(map(int, resolution))
    if resolution[1] >= 1080 and resolution[1] <= 2160:  #Between 1080p and 4k
        rating = "Great!"
        recommendation = "Great video resolution!"
    elif resolution[1] >= 720 and resolution[1] < 1080:  #Between 720p and 1080p
        rating = "Okay"
        recommendation = "Your resolution is okay. However, you can still improve it by increasing the resolution to 1080p."
    elif resolution[1] < 720:  #Below 720p
        rating = "Bad"
        recommendation = "Your resolution is too low. Please increase it to at least 720p."
    else:
        rating = "Okay"
        recommendation = "Your video resolution might be too high. Try lowering it to at least 4k to increase support for more devices and reduce bandwidth usage."
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


def bit_rate_helper(video, frame_rate, high_fps_minimum, high_fps_maximum,
                    low_fps_minimum, low_fps_maximum):
    rating = ""
    recommendation = ""
    recommended = ""
    bit_rate = float(video.bit_rate)
    if frame_rate == "high":
        recommended = f'{high_fps_minimum} Mbps up to {high_fps_maximum} Mbps'
        if bit_rate >= high_fps_minimum and bit_rate <= high_fps_maximum:
            rating = "Great!"
            recommendation = "Great bit rate!"
        elif bit_rate > high_fps_maximum:
            rating = "Okay"
            recommendation = "Your bit rate might be too high. Try increasing the resolution, increasing the fps or reducing the bit rate."
        else:
            rating = "Bad"
            recommendation = f'Your bit rate is too low. Please increase it to at least {high_fps_minimum} Mbps'
    else:
        recommended = f'{low_fps_minimum} Mbps up to {low_fps_maximum} Mbps'
        if bit_rate >= low_fps_minimum and bit_rate <= low_fps_maximum:
            rating = "Great!"
            recommendation = "Great bit rate!"
        elif bit_rate > low_fps_maximum:
            rating = "Okay"
            recommendation = "Your bit rate might be too high. Try increasing the resolution, increasing the fps or reducing the bit rate."
        else:
            rating = "Bad"
            recommendation = f'Your bit rate is too low. Please increase it to at least {low_fps_minimum} Mbps'
    return (rating, recommendation, recommended)


def get_bit_rate_recommendation(video):
    result = ()
    frame_rate = "high" if video.frame_rate > 30 else "standard"
    resolution = video.resolution.split('x')
    resolution = list(map(int, resolution))

    if resolution[1] == 2160:
        result = bit_rate_helper(video, frame_rate, 53, 85, 35, 56)
    elif resolution[1] == 1440:
        result = bit_rate_helper(video, frame_rate, 24, 30, 16, 20)
    elif resolution[1] == 1080:
        result = bit_rate_helper(video, frame_rate, 12, 15, 8, 10)
    elif resolution[1] == 720:
        result = bit_rate_helper(video, frame_rate, 7.5, 9.5, 5, 6.5)
    elif resolution[1] == 480:
        result = bit_rate_helper(video, frame_rate, 4, 5, 2.5, 3.5)
    elif resolution[1] < 480:
        result[0] = "Bad"
        result[
            1] = "Please increase your resolution to at least 480p in order to see meaningful bit rate recommendation."
        result[2] = "Unsupported recommendation"
    else:
        result[0] = "Unknown"
        result[
            1] = "Unsupported bit rate analysis. Your resolution is most likely too high or not a standard resolution."
        result[2] = "Unsupported recommendation"
    return result
