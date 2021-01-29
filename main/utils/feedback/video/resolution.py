import os
import matplotlib.pyplot as plt
from vision_video_analyzer.settings import MEDIA_ROOT

visualizations = f'{MEDIA_ROOT}/visualizations'


# Get the rating and recommendation based on the video resolution.
def get_resolution_recommendation(video):
    rating = ""
    recommendation = ""
    resolution = video.resolution.split('x')
    resolution = list(map(int, resolution))
    get_resolution_boxplot(video, resolution[1])
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


def get_resolution_boxplot(video, current_resolution):

    visualization_output_path = f'{visualizations}/{video}/'
    fig, ax = plt.subplots(figsize=(5, 2), dpi=100)

    boxes = [{
        'label': "Resolution",
        'whislo': 720,  # Bottom whisker position
        'q1': 1080,  # First quartile (25th percentile)
        'med': current_resolution,  # Median         (50th percentile)
        'q3': 2160,  # Third quartile (75th percentile)
        'whishi': 4320,  # Top whisker position
    }]
    ax.bxp(boxes, showfliers=False, vert=False, positions=[0])
    plt.yticks([0], ['Resolution height (pixels)'])
    if os.path.isdir(visualization_output_path) == False:
        os.mkdir(visualization_output_path)
    plt.tight_layout()
    plt.savefig(f'{visualizations}/{video}/resolution')
    plt.close()
