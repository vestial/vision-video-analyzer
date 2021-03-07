import os
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
from vision_video_analyzer.settings import MEDIA_ROOT

visualizations = f'{MEDIA_ROOT}/visualizations'


# Get the rating and recommendation based on the bit depth
def get_bit_depth_recommendation(video):
    rating = ""
    recommendation = ""
    bit_depth = int(video.bit_depth)
    get_bit_depth_boxplot(video, bit_depth)
    if bit_depth >= 10 and bit_depth <= 12:
        rating = "Great!"
        recommendation = "Great video bit depth!"
    elif bit_depth >= 8 and bit_depth < 10:
        rating = "Okay"
        recommendation = "Your bit depth is good enough. However, consider increasing bit/color depth to 10 or 12 bits to increase the range of possible displayed colors and enable usage of HDR video technology."
    elif bit_depth > 12:
        rating = "Unknown"
        recommendation = "Your bit depth is very high. You may want to lower it to 10 or 12 bits to save data and bandwidth. It is unknown if increasing bit depth above 12 bits increases the perceptible quality of vision videos."
    else:
        rating = "Bad"
        recommendation = "Your bit depth is too low. Try to increase it to at least 8 bits, in order to display a wider range of possible colors"
    return (rating, recommendation)


def get_bit_depth_boxplot(video, current_bit_depth):

    visualization_output_path = f'{visualizations}/{video}/'
    fig, ax = plt.subplots(figsize=(5, 2), dpi=100)

    boxes = [{
        'label': "Bit depth",
        'whislo': 8,  # Bottom whisker position
        'q1': 10,  # First quartile (25th percentile)
        'med': current_bit_depth,  # Median         (50th percentile)
        'q3': 12,  # Third quartile (75th percentile)
        'whishi': 24,  # Top whisker position
    }]
    ax.bxp(boxes,
           showfliers=False,
           vert=False,
           positions=[0],
           patch_artist=True,
           medianprops=dict(color='red', linewidth=2),
           boxprops=dict(facecolor='none'))
    plt.yticks([0], ['Bit depth'])
    plt.xlabel('Bits')
    legend_elements = [
        Line2D([0], [0], color='red', lw=2, label='Current bit depth'),
        Patch(facecolor='white',
              edgecolor='grey',
              linewidth=1,
              label='Optimal threshold')
    ]
    ax.legend(handles=legend_elements)

    plt.tight_layout()
    if os.path.isdir(visualization_output_path) == False:
        os.mkdir(visualization_output_path)
    plt.savefig(f'{visualizations}/{video}/bit_depth')
    plt.close()
