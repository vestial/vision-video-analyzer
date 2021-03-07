import os
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
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
        rating = "Great!"
        recommendation = "Your frame rate is good. You can increase it to 60 fps if you wish to capture fast moving footages or use slow motion effects."
    elif video.frame_rate <= 60:
        rating = "Great!"
        recommendation = "s Great frame rate! You can lower it to 24 fps if you want a more cinematic video look."
    elif video.frame_rate > 60:
        rating = "Bad"
        recommendation = "Your frame rate might be too high. Please lower it to at least 60 fps since such a high frame rate is unlikely needed for vision videos and has a diminishing return."
    else:
        rating = "Unknown"
        recommendation = "Please set your frame rate to 24, 25, 30, or 60 FPS for a standard frame rate."
    return (rating, recommendation)


def get_frame_rate_boxplot(video, current_frame_rate):

    visualization_output_path = f'{visualizations}/{video}/'
    fig, ax = plt.subplots(figsize=(5, 2), dpi=100)

    boxes = [{
        'label': "Frame rate",
        'whislo': 24,  # Bottom whisker position
        'q1': 24,  # First quartile (25th percentile)
        'med': current_frame_rate,  # Median         (50th percentile)
        'q3': 60,  # Third quartile (75th percentile)
        'whishi': 120,  # Top whisker position
    }]
    ax.bxp(boxes,
           showfliers=False,
           vert=False,
           positions=[0],
           patch_artist=True,
           medianprops=dict(color='red', linewidth=2),
           boxprops=dict(facecolor='none'))
    plt.yticks([0], ['Frame rate'])
    plt.xlabel('Frames per second (fps)')
    legend_elements = [
        Line2D([0], [0], color='red', lw=2, label='Current frame rate'),
        Patch(facecolor='white',
              edgecolor='grey',
              linewidth=1,
              label='Optimal threshold')
    ]
    ax.legend(handles=legend_elements)
    plt.tight_layout()
    if os.path.isdir(visualization_output_path) == False:
        os.mkdir(visualization_output_path)
    plt.savefig(f'{visualizations}/{video}/frame_rate')
    plt.close()
