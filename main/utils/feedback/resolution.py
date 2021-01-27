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