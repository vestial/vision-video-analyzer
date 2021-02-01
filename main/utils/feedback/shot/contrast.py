import os
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
from vision_video_analyzer.settings import MEDIA_ROOT

visualizations = f'{MEDIA_ROOT}/visualizations'


def get_contrast_recommendation_wrapper(video, contrasts):

    results = []
    i = 1
    for contrast in contrasts:
        results.append(get_contrast_recommendation(contrast))
        get_contrast_boxplot(video, i, contrast)
        i = i + 1

    return results


def get_contrast_recommendation(contrast):

    recommended = "Between 0.3 and 0.8."
    rating = ""
    feedback = ""
    #Temporary set values
    if (contrast >= 0.3 and contrast <= 0.8):
        rating = "Great!"
        feedback = "The contrast of your shot is great!"
    elif (contrast < 0.3):
        rating = "Bad"
        feedback = "Try to increase your RMS contrast to at least 0.3. You can do this by either changing your settings or by choosing video backgrounds with colors which contrast with the subject. "
    else:
        rating = "Bad"
        feedback = "Try to decrease your RMS contrast to at least 0.8. You can do this by either changing your settings or by choosing video backgrounds with colors which contrast with the subject. "

    return [recommended, rating, feedback]


def get_contrast_boxplot(video, i, current_contrast):

    visualization_output_path = f'{visualizations}/{video}/contrasts/'
    fig, ax = plt.subplots(figsize=(5, 2), dpi=100)

    boxes = [{
        'label': "Contrast",
        'whislo': 0.1,  # Bottom whisker position
        'q1': 0.3,  # First quartile (25th percentile)
        'med': current_contrast,  # Median         (50th percentile)
        'q3': 0.8,  # Third quartile (75th percentile)
        'whishi': 1,  # Top whisker position
    }]
    ax.bxp(boxes,
           showfliers=False,
           vert=False,
           positions=[0],
           patch_artist=True,
           medianprops=dict(color='red', linewidth=2),
           boxprops=dict(facecolor='none'))
    plt.yticks([0], ['Average contrast'])
    plt.xlabel('RMS contrast value')
    legend_elements = [
        Line2D([0], [0], color='red', lw=2, label='Current shot contrast'),
        Patch(facecolor='white',
              edgecolor='grey',
              linewidth=1,
              label='Optimal threshold')
    ]
    ax.legend(handles=legend_elements)
    plt.tight_layout()
    if os.path.isdir(visualization_output_path) == False:
        os.mkdir(visualization_output_path)
    plt.savefig(f'{visualizations}/{video}/contrasts/{i}')
    plt.close()
