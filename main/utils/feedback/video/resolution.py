import os
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from vision_video_analyzer.settings import MEDIA_ROOT

visualizations = f'{MEDIA_ROOT}/visualizations'


# Get the rating and recommendation based on the video resolution.
def get_resolution_recommendation(video):
    rating = ""
    recommendation = ""
    resolution = video.resolution.split('x')
    resolution = list(map(int, resolution))
    get_resolution_boxplot(video, resolution[1])
    if resolution[1] >= 1080:  #Above 1080p
        rating = "Great!"
        recommendation = "Great video resolution!"
    elif resolution[1] >= 720 and resolution[1] < 1080:  #Between 720p and 1080p
        rating = "Okay"
        recommendation = "Your resolution is okay. However, you can still improve it by increasing the resolution to 1080p."
    else:
        rating = "Bad"  #Below 720p
        recommendation = "Your resolution is too low. Please increase it to at least 720p."
    return (rating, recommendation)


def get_resolution_boxplot(video, current_resolution):

    visualization_output_path = f'{visualizations}/{video}/'
    fig, ax = plt.subplots(figsize=(5, 2), dpi=100)

    boxes = [{
        'label': "Resolution",
        'whislo': 720,  # Bottom whisker position
        'q1': 1080,  # First quartile (25th percentile)
        'med': current_resolution,  # Median         (50th percentile)
        'q3': 4320,  # Third quartile (75th percentile)
        'whishi': 4320,  # Top whisker position
    }]
    ax.bxp(boxes,
           showfliers=False,
           vert=False,
           positions=[0],
           patch_artist=True,
           medianprops=dict(color='red', linewidth=2),
           boxprops=dict(facecolor='none'))
    plt.yticks([0], ['Video resolution'])
    plt.xlabel('Resolution height (pixels)')
    legend_elements = [
        Line2D([0], [0], color='red', lw=2, label='Current resolution'),
        Patch(facecolor='white',
              edgecolor='grey',
              linewidth=1,
              label='Optimal threshold')
    ]
    ax.legend(handles=legend_elements)

    plt.tight_layout()
    if os.path.isdir(visualization_output_path) == False:
        os.mkdir(visualization_output_path)
    plt.savefig(f'{visualizations}/{video}/resolution')
    plt.close()
