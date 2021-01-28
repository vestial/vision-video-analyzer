def get_bit_depth_recommendation(video):
    rating = ""
    recommendation = ""
    bit_depth = int(video.bit_depth)
    if bit_depth >= 10 and bit <= 12:  #Between 1080p and 4k
        rating = "Great!"
        recommendation = "Great video bit depth!"
    elif bit_depth >= 8 and bit_depth < 10:  #Between 720p and 1080p
        rating = "Good"
        recommendation = "Your bit depth is good enough. However, consider increasing bit/color depth to 10 or 12 bits to increase the range of possible displayed colors."
    elif bit_depth > 12:
        rating = "Good"
        recommendation = "Your bit depth is very high. You may want to lower it to 10 or 12 bits to save data and bandwidth."
    else:
        rating = "Bad"
        recommendation = "Your bit depth is too low. Try to increase it to at least 8 bits, in order to display a wider range of possible colors"
    return (rating, recommendation)