import os
import matplotlib.pyplot as plt
from vision_video_analyzer.settings import MEDIA_ROOT

visualizations = f'{MEDIA_ROOT}/visualizations'


# Get the rating and recommendation based on the audio sample rate.
def get_sample_rate_recommendation(video):
    rating = ""
    recommendation = ""
    sample_rate = float(video.sample_rate)
    get_sample_rate_boxplot(video, sample_rate)
    if sample_rate >= 44.1 and sample_rate <= 48:
        rating = "Great!"
        recommendation = "Great audio sample rate!"
    elif sample_rate > 48:
        rating = "Good"
        recommendation = "Good sample rate. However, audio sample rate above 48.0 kHz has diminishing returns. Try lowering it to 48.0 kHz to minimize data usage"
    else:
        rating = "Bad"
        recommendation = "Your sample rate is too low. Try increasing it to at least 44.1 kHz to prevent sound distortion."
    return (rating, recommendation)


def get_sample_rate_boxplot(video, current_sample_rate):

    visualization_output_path = f'{visualizations}/{video}/'
    fig, ax = plt.subplots(figsize=(5, 2), dpi=100)

    boxes = [{
        'label': "Sample rate",
        'whislo': 44.1,  # Bottom whisker position
        'q1': 44.1,  # First quartile (25th percentile)
        'med': current_sample_rate,  # Median         (50th percentile)
        'q3': 48,  # Third quartile (75th percentile)
        'whishi': 96,  # Top whisker position
    }]
    ax.bxp(boxes, showfliers=False, vert=False, positions=[0])
    plt.yticks([0], ['Sample rate'])
    plt.xlabel('kHz')
    if os.path.isdir(visualization_output_path) == False:
        os.mkdir(visualization_output_path)
    plt.tight_layout()
    plt.savefig(f'{visualizations}/{video}/sample_rate')
    plt.close()
