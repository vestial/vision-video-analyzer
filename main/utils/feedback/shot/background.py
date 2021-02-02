import os
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
from vision_video_analyzer.settings import MEDIA_ROOT

visualizations = f'{MEDIA_ROOT}/visualizations'


def get_background_recommendation_wrapper(video, backgrounds):

    results = []
    i = 1
    for background in backgrounds:
        results.append(get_background_recommendation(background))
        get_background_visualization(video, i, background)
        i = i + 1

    return results


def get_background_recommendation(background):

    recommended = "Colors that are not black or strong (red, yellow, or bright green)."
    rating = ""
    feedback = ""

    return [recommended, rating, feedback]


def color_picker(rgb):
    result = ""
    if rgb[0] <= 255 and rgb[0] >= 200 and rgb[1] <= 50 and rgb[
            2] <= 50:  #Bright red
        result = "red"

    return result


def get_background_visualization(video, i, current_background):

    visualization_output_path = f'{visualizations}/{video}/backgrounds/'
    fig, ax = plt.subplots(figsize=(5, 2), dpi=100)
    ax.axis('off')
    fig.set
    plt.xlabel('Average background color')
    plt.tight_layout()
    if os.path.isdir(visualization_output_path) == False:
        os.mkdir(visualization_output_path)
    plt.savefig(f'{visualizations}/{video}/backgrounds/{i}',
                facecolor=convert_rgb_to_hex(current_background))
    plt.close()


def convert_rgb_to_hex(rgb):
    r = int(rgb[0])
    g = int(rgb[1])
    b = int(rgb[2])
    return "#{:02x}{:02x}{:02x}".format(r, g, b)
