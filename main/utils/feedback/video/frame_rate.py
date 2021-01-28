import matplotlib.pyplot as plt


# Get the rating and recommendation based on the video frame rate.
def get_frame_rate_recommendation(video):
    rating = ""
    recommendation = ""
    get_frame_rate_boxplot(video.frame_rate)
    if video.frame_rate < 24:
        rating = "Bad"
        recommendation = "Your frame rate is too low. Please increase it to at least 24 fps by changing the settings in your camera."
    elif video.frame_rate >= 24 and video.frame_rate < 30:
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


def get_frame_rate_boxplot(current_frame_rate):
    fig, ax = plt.subplots()
    boxes = [{
        'label': "Frame rate",
        'whislo': 24,  # Bottom whisker position
        'q1': 30,  # First quartile (25th percentile)
        'med': current_frame_rate,  # Median         (50th percentile)
        'q3': 60,  # Third quartile (75th percentile)
        'whishi': 120,  # Top whisker position
    }]
    ax.bxp(boxes, showfliers=False)
    ax.set_ylabel("Frames per second (fps)")
    plt.savefig("frame_rate_visual_png")
    plt.close()
