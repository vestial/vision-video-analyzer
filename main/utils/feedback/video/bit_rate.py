# Helper function to get the bit depth recommendation based on frame rate and resolution
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


# Get the rating and recommendation based on the video bit rate. The values are based on Youtube's recommended upload settings.
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
