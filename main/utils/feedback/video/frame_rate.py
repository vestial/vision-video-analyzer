import os
import matplotlib.pyplot as plt
from vision_video_analyzer.settings import MEDIA_ROOT

visualizations = f'{MEDIA_ROOT}/visualizations'


# Get the rating and recommendation based on the video frame rate.
def get_frame_rate_recommendation(video):
    rating = ""
    recommendation = ""
    get_frame_rate_boxplot(video, video.frame_rate)
    if video.frame_rate < 24:
        rating = "Bad"
        recommendation = "Your frame rate is low. Please increase it to at least 24 fps by changing the settings in your camera."
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


def get_frame_rate_boxplot(video, current_frame_rate):

    visualization_output_path = f'{visualizations}/{video}/'
    fig, ax = plt.subplots(figsize=(5, 2), dpi=100)

    boxes = [{
        'label': "Frame rate",
        'whislo': 24,  # Bottom whisker position
        'q1': 30,  # First quartile (25th percentile)
        'med': current_frame_rate,  # Median         (50th percentile)
        'q3': 60,  # Third quartile (75th percentile)
        'whishi': 120,  # Top whisker position
    }]
    ax.bxp(boxes, showfliers=False, vert=False, positions=[0])
    plt.yticks([0], ['Frame rate'])
    plt.xlabel('Frames per second (fps)')
    if os.path.isdir(visualization_output_path) == False:
        os.mkdir(visualization_output_path)
    plt.tight_layout()
    plt.savefig(f'{visualizations}/{video}/frame_rate')
    plt.close()
