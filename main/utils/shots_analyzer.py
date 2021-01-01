from main.utils.background import BackgroundColorDetector
from time import sleep
from vision_video_analyzer.settings import MEDIA_ROOT
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery import shared_task
from PIL import Image

import subprocess
import numpy as np
import cv2
import os
import pytesseract

videos = f'{MEDIA_ROOT}/videos'
thumbnails = f'{MEDIA_ROOT}/thumbnails'
shots = f'{MEDIA_ROOT}/shots'

logger = get_task_logger(__name__)


# Wrapper for the shot analysis getters
def analyze_shots(uploaded_file):
    get_shots.delay(uploaded_file)
    get_shots_length(uploaded_file)
    get_contrast(uploaded_file)
    get_background(uploaded_file)


# Use pyscenedetect to split video into shots
@shared_task
def get_shots(video):
    video_input_path = f'{videos}/{video}'
    shots_screenshots_output_path = f'{shots}/{video}/screenshots/'
    shots_output_path = f'{shots}/{video}/shots/'
    logger.info("Finding threshold")
    threshold_process = subprocess.Popen([
        'scenedetect',
        '--input',
        video_input_path,
        '--stats',
        video_input_path + '.csv',
        'detect-content',
        'list-scenes',
        '-o',
        shots_screenshots_output_path,
    ],
                                         stdout=subprocess.PIPE).wait()
    threshold = 37  # stub
    logger.info("Shots processing")
    process = subprocess.Popen([
        'scenedetect', '--input', video_input_path, 'detect-content', '-t',
        str(threshold), 'list-scenes', '-o', shots_screenshots_output_path,
        'save-images', '-o', shots_screenshots_output_path, 'split-video',
        '-o', shots_output_path
    ],
                               stdout=subprocess.PIPE)
    while stream_process(process):
        sleep(0.1)
    logger.info("Shots received")


# Prints subprocess output to console
def stream_process(process):
    go = process.poll() is None
    for line in process.stdout:
        print(line)
    return go


# Use ffprobe to get shots length that were produced by pyscenedtect
@shared_task
def get_shots_length(video):
    shots_output_path = f'{shots}/{video}/shots/'
    lengths = []
    for filename in sorted(os.listdir(shots_output_path)):
        length = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            os.path.join(shots_output_path, filename)
        ],
                                capture_output=True,
                                text=True,
                                input="Y")

        lengths.append(float(length.stdout))
        print("Shot: " + filename + " lasts " + str(float(length.stdout)) +
              " seconds")

    return lengths


# Get contrast of each shot images by using OpenCV
@shared_task
def get_contrast(video):
    shots_output_path = f'{shots}/{video}/screenshots/'

    contrasts = []
    for filename in sorted(os.listdir(shots_output_path)):
        img = cv2.imread(os.path.join(shots_output_path, filename))
        if img is not None:
            # Use RMS contrast for contrast measurement
            img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.normalize(img_grey,
                          img_grey,
                          alpha=0,
                          beta=1,
                          norm_type=cv2.NORM_MINMAX)
            contrast = img_grey.std(ddof=1)
            contrasts.append(str(contrast))

    temp = []
    results = []
    for i in range(len(contrasts)):
        if i == 0 or i % 3 != 0:
            temp.append(contrasts[i])
            if i == len(contrasts) - 1:
                mean_contrast = np.around(np.mean(
                    np.array(temp).astype(np.float)),
                                          decimals=3)
                results.append(mean_contrast)
                print("Average contrast: shot " + str((int(i / 3) + 1)) +
                      " is " + mean_contrast.astype(str) + " (RMS)")
        else:
            mean_contrast = np.around(np.mean(np.array(temp).astype(np.float)),
                                      decimals=3)
            results.append(mean_contrast)
            print("Average contrast: shot " + str(int(i / 3)) + " is " +
                  mean_contrast.astype(str) + " (RMS)")
            temp = []
            temp.append(contrasts[i])
    return results


# Get average background color for each shot
@shared_task
def get_background(video):
    shots_output_path = f'{shots}/{video}/screenshots/'
    backgrounds = []
    results = []
    temp_r, temp_g, temp_b = [], [], []
    for filename in sorted(os.listdir(shots_output_path)):
        if filename.endswith(".jpg"):
            background = BackgroundColorDetector(
                os.path.join(shots_output_path, filename), filename)
            backgrounds.append(background.detect())
    for i in range(len(backgrounds)):
        backgrounds[i] = tuple(map(float, backgrounds[i].split(', ')))
        if i == 0 or i % 3 != 0:
            temp_r.append(backgrounds[i][0])
            temp_g.append(backgrounds[i][1])
            temp_b.append(backgrounds[i][2])
            if i == len(backgrounds) - 1:
                results.append(mean_rgb_calculator(temp_r, temp_g, temp_r))
        else:
            results.append(mean_rgb_calculator(temp_r, temp_g, temp_r))
            temp_r, temp_g, temp_b = [], [], []
            temp_r.append(backgrounds[i][0])
            temp_g.append(backgrounds[i][1])
            temp_b.append(backgrounds[i][2])

    return results


#Helper function to calculate mean RGB
def mean_rgb_calculator(r, g, b):
    mean_r = np.around(np.mean(np.array(r).astype(np.float)), decimals=1)
    mean_g = np.around(np.mean(np.array(g).astype(np.float)), decimals=1)
    mean_b = np.around(np.mean(np.array(b).astype(np.float)), decimals=1)
    return tuple([mean_r, mean_g, mean_b])


#Get the second shot screenshot for each shot
@shared_task
def get_shot_screenshot(video):
    shots_output_path = f'{shots}/{video}/screenshots/'
    results = []
    for filename in sorted(os.listdir(shots_output_path)):
        if filename.endswith("-02.jpg"):
            results.append(filename)
    return results


'''
# List all shots with text
@shared_task
def get_shot_text(video):
    shots_output_path = f'{shots}/{video}/screenshots/'
    results = []
    for filename in sorted(os.listdir(shots_output_path)):
        if filename.endswith(".jpg"):
            img = Image.open(os.path.join(shots_output_path, filename))
            if img.getcolors() is not None:
                #border = pytesseract.image_to_boxes(img).split(" ")
                #(left, upper, right, lower) = (int(border[1]),int(border[2]) - 8,int(border[3]),int(border[4]) + 8)
                #im_crop = img.crop((left, upper, right, lower))
                #colors = sorted(im_crop.getcolors())
                #hex = ('#%02x%02x%02x' % colors[-2][1])
                text = pytesseract.image_to_string(img)
                #print("Color is: " + hex + ". Text is: " + text)
                print(text)
    return results
'''
