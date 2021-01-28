def get_video_length_recommendation(video):
    rating = ""
    recommendation = ""
    video_length = float(video.video_length)
    if video_length > 300:  #Between 1080p and 4k
        rating = "Bad"
        recommendation = "Keep the final video short to ensure that you only show the important details to the audience."
    else:
        rating = "Great!"
        recommendation = "The length of your video is already short enough to only show the important details to the audience."
    return (rating, recommendation)