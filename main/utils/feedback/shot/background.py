import os
import numpy as np
import argparse
import cv2
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

    color_range = [
        ([150, 0, 0], [255, 50, 50]),  #Red
        ([200, 200, 0], [255, 255, 50]),  #Yellow
        ([0, 200, 0], [50, 255, 50]),  #Bright green
    ]
    strong_color = False
    if background[0] >= color_range[0][0][0] and background[0] <= color_range[
            0][1][0]:
        if background[1] >= color_range[0][0][1] and background[
                1] <= color_range[0][1][1]:
            if background[2] >= color_range[0][0][2] and background[
                    2] <= color_range[0][1][2]:
                rating = "Too red!"
                feedback = "Please avoid using red as a background color to not distract the audience and to not modify apparent color of the subject."
                strong_color = True
    if background[0] >= color_range[1][0][0] and background[0] <= color_range[
            1][1][0]:
        if background[1] >= color_range[1][0][1] and background[
                1] <= color_range[1][1][1]:
            if background[2] >= color_range[1][0][2] and background[
                    2] <= color_range[1][1][2]:
                rating = "Too yellow!"
                feedback = "Please avoid using yellow as a background color to not distract the audience and to not modify apparent color of the subject."
                strong_color = True
    if background[0] >= color_range[2][0][0] and background[0] <= color_range[
            2][1][0]:
        if background[1] >= color_range[2][0][1] and background[
                1] <= color_range[2][1][1]:
            if background[2] >= color_range[2][0][2] and background[
                    2] <= color_range[2][1][2]:
                rating = "Too bright green!"
                feedback = "Please avoid using bright green as a background color to not distract the audience and to not modify apparent color of the subject."
                strong_color = True
    if strong_color is False:
        rating = "Normal background color."
        feedback = "Your background color is normal and is neither strong red, yellow, nor bright green."
    return [recommended, rating, feedback]


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
