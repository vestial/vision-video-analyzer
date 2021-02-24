from main.utils.analyzer import get_frame_rate
from vision_video_analyzer.settings import MEDIA_ROOT
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery import shared_task

import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

import csv

logger = get_task_logger(__name__)
shots = f'{MEDIA_ROOT}/shots'
visualizations = f'{MEDIA_ROOT}/visualizations'
mpl.use('agg')


# Use histogram analysis to analyze the exposure of each shot.
@shared_task
def get_exposure_histogram(video):
    shots_output_path = f'{shots}/{video}/screenshots/'
    visualization_output_path = f'{visualizations}/{video}/exposures/'
    logger.info("Calculating histogram")
    exposures = []
    i = 1
    for filename in sorted(os.listdir(shots_output_path)):
        img = cv2.imread(os.path.join(shots_output_path, filename))
        if img is not None:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            gray = hsv[:, :, 2]
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            dark_pixels = np.sum(hist[:50])
            bright_pixels = np.sum(hist[200:255])

            total_pixels = np.sum(hist)
            logger.info(f'Total pixels: {total_pixels}')

            if dark_pixels / total_pixels > 0.5:
                logger.info(f'{filename} is underexposed!')
                exposures.append("underexposed")
            elif bright_pixels / total_pixels > 0.5:
                logger.info(f'{filename} is overexposed!')
                exposures.append("overexposed")
            else:
                exposures.append("normal")
            figure = plt.figure(figsize=(5, 2))
            plt.title("Grayscale Histogram")
            plt.xlabel("Bins")
            plt.ylabel("# of Pixels")
            plt.plot(hist)
            plt.xlim([0, 256])
            plt.tight_layout()
            if os.path.isdir(visualization_output_path) == False:
                os.mkdir(visualization_output_path)
            if filename.endswith("-02.jpg"):
                plt.savefig(f'{visualizations}/{video}/exposures/{i}')
                i = i + 1
            figure.clear()
            plt.close(figure)
            logger.info(filename + " Histogram calculated")
    return determine_exposures(exposures)


# Determine the exposure of each shot by checking the exposure of the 3 screenshots output of every shot
def determine_exposures(exposures):
    result = []
    temp = set()
    print(exposures)
    for i in range(len(exposures)):
        if (i % 3 == 0 and i != 0) or i == len(exposures) - 1:
            if "underexposed" in temp and "overexposed" in temp:
                result.append(parse_exposure("both"))
            elif "underexposed" in temp:
                result.append(parse_exposure("underexposed"))
            elif "overexposed" in temp:
                result.append(parse_exposure("overexposed"))
            else:
                result.append(parse_exposure("normal"))
            temp = set()
        temp.add(exposures[i])
    print(f'Processed exposures: {result}')
    return result


# Convert raw exposure into proper text for users to understand
def parse_exposure(exposure):
    if (exposure == "both"):
        return "Some part of the shot is underexposed and another part is overexposed!"
    elif (exposure == "underexposed"):
        return "Shot is underexposed!"
    elif (exposure == "overexposed"):
        return "Shot is overexposed!"
    elif (exposure == "normal"):
        return "Exposure is normal."
    else:
        return "Error in calculating exposure"


# Parse content_val from scenedetect stats to assist in determining optimal threshold value
def parse_stats(stats):
    content_vals = []
    if (stats is None):
        logger.info("No stats file found")
        return
    with open(stats) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count < 2:
                line_count += 1
            else:
                content_vals.append(row[2])
                line_count += 1
        print(f'Processed {line_count} lines.')
        return content_vals


# Generates csv which contains content_val deltas for finding optimal threshold
def generate_threshold_csv(video):
    stats_path = f'{shots}/{video}/{video}.csv'
    threshold_path = f'{shots}/{video}/{video}-threshold.csv'
    with open(threshold_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Frame Number', 'content_val', 'del_content_val',
            'del_content_val_abs'
        ])
        content_vals = parse_stats(stats_path)
        i = 0
        for content_val in content_vals:
            del_content_val = 0
            if i != 0:
                del_content_val = float(content_vals[i]) - float(
                    content_vals[i - 1])
            del_content_val_abs = abs(del_content_val)
            writer.writerow(
                [i + 1, content_val, del_content_val, del_content_val_abs])
            i += 1


# Get the optimal threshold from the generated csv file
def get_threshold(video):
    csv_path = f'{shots}/{video}/{video}-threshold.csv'
    thresholds_path = f'{shots}/{video}/thresholds/'
    if os.path.isdir(thresholds_path) == False:
        os.mkdir(thresholds_path)
    change_vals = []
    raw_change_vals = []
    borders = []
    threshold = 30  #Default ContentDetector threshold value
    window_size = int(
        get_frame_rate(video))  #Window size to check validity of border
    #Get only the absolute content_val changes from the generated csv
    generate_threshold_csv(video)
    with open(csv_path, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count < 2:
                line_count += 1
                continue
            elif float(row[3]) > threshold:
                borders.append((int(row[0]), float(row[3]), float(row[1])))
            change_vals.append((int(row[0]), float(row[3])))
            raw_change_vals.append(float(row[3]))
            line_count += 1
    #Generate absolute content_val difference for the whole video
    plt.figure()
    plt.xlabel("Frame number")
    plt.ylabel("Absolute content_val difference")
    plt.plot(raw_change_vals)
    plt.savefig(f'{csv_path}.png')
    i = 0
    pruned_borders = borders  # Copy border to avoid modifying borders in for loop
    for border in borders:
        #Define bounding region for each window
        region_start = 0 if int(border[0]) - window_size < 1 else int(
            border[0]) - window_size
        region_end = len(change_vals) if int(border[0]) + window_size > len(
            change_vals) - 1 else int(border[0]) + window_size

        region = change_vals[region_start:region_end]
        region_vals = []
        for val in region:
            region_vals.append(val[1])
        #Generate boxplot for each window
        figure = plt.figure()
        plt.xlabel("del_content_val_abs")
        plt.ylabel("Absolute content_val difference")
        plt.boxplot(region_vals)
        boxplot_stats = mpl.cbook.boxplot_stats(region_vals)
        upper_whisker = next(item for item in boxplot_stats).get('whishi')
        #Checks if border is real (not within normal distribution of the box plot)
        if border[1] <= upper_whisker:
            pruned_borders.remove(border)
        plt.savefig(f'{thresholds_path}{i}.png')
        figure.clear()
        plt.close(figure)
        i += 1
    border_thresholds = []
    for border in pruned_borders:
        if border[2] >= threshold:
            border_thresholds.append(border[2])
    logger.info(border_thresholds)
    threshold = min(border_thresholds)
    logger.info(border_thresholds)
    logger.info("Threshold set: " + str(threshold))
    return threshold
