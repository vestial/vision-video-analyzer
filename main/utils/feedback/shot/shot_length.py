import os
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
from vision_video_analyzer.settings import MEDIA_ROOT

visualizations = f'{MEDIA_ROOT}/visualizations'


def get_shot_length_recommendation_wrapper(video, shot_lengths):

    results = []
    i = 1
    for shot_length in shot_lengths:
        results.append(get_shot_length_recommendation(shot_length))
        get_shot_length_boxplot(video, i, shot_length)
        i = i + 1

    return results


def get_shot_length_recommendation(shot_length):

    recommended = "Between 15 and 30 seconds."
    rating = ""
    feedback = ""

    if (shot_length >= 15 and shot_length <= 30):
        rating = "Great!"
        feedback = "The length of your shot is great, since it is between 15 and 30 seconds."
    elif (shot_length < 15):
        rating = "Bad"
        feedback = "Try increasing the length of your shot to at least 15 seconds to enable audience to understand the information presented."
    else:
        rating = "Bad"
        feedback = "Try reducing the length of your shot to at least 30 seconds. Avoid too long shots that the audience cannot understand."

    return [recommended, rating, feedback]


def get_shot_length_boxplot(video, i, current_shot_length):

    visualization_output_path = f'{visualizations}/{video}/lengths/'
    fig, ax = plt.subplots(figsize=(5, 2), dpi=100)

    boxes = [{
        'label': "Shot duration",
        'whislo': 5,  # Bottom whisker position
        'q1': 15,  # First quartile (25th percentile)
        'med': current_shot_length,  # Median         (50th percentile)
        'q3': 30,  # Third quartile (75th percentile)
        'whishi': 45,  # Top whisker position
    }]
    ax.bxp(boxes,
           showfliers=False,
           vert=False,
           positions=[0],
           patch_artist=True,
           medianprops=dict(color='red', linewidth=2),
           boxprops=dict(facecolor='none'))
    plt.yticks([0], ['Shot length'])
    plt.xlabel('Duration (seconds)')
    legend_elements = [
        Line2D([0], [0], color='red', lw=2, label='Current shot duration'),
        Patch(facecolor='white',
              edgecolor='grey',
              linewidth=1,
              label='Optimal threshold')
    ]
    ax.legend(handles=legend_elements)
    plt.tight_layout()
    if os.path.isdir(visualization_output_path) == False:
        os.mkdir(visualization_output_path)
    plt.savefig(f'{visualizations}/{video}/lengths/{i}')
    plt.close()
