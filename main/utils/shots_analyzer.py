from main.utils.background import BackgroundColorDetector
from time import sleep
from vision_video_analyzer.settings import MEDIA_ROOT
import subprocess
import numpy as np
import cv2
import os

videos = f'{MEDIA_ROOT}/videos'
thumbnails = f'{MEDIA_ROOT}/thumbnails'
shots = f'{MEDIA_ROOT}/shots'


# Wrapper for the shot analysis getters
def analyze_shots(uploaded_file):
    get_shots(uploaded_file)
    get_shots_length(uploaded_file)
    get_contrast(uploaded_file)
    get_background(uploaded_file)


# Use pyscenedetect to split video into shots
def get_shots(video):
    video_input_path = f'{videos}/{video}'
    shots_screenshots_output_path = f'{shots}/{video}/screenshots/'
    shots_output_path = f'{shots}/{video}/shots/'

    process = subprocess.Popen([
        'scenedetect', '--input', video_input_path, 'detect-content',
        'list-scenes', '-o', shots_screenshots_output_path, 'save-images',
        '-o', shots_screenshots_output_path, 'split-video', '-o',
        shots_output_path
    ],
                               stdout=subprocess.PIPE)
    while stream_process(process):
        sleep(0.1)


# Prints subprocess output to console
def stream_process(process):
    go = process.poll() is None
    for line in process.stdout:
        print(line)
    return go


# Use ffprobe to get shots length that were produced by pyscenedtect
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
def get_contrast(video):
    shots_output_path = f'{shots}/{video}/screenshots/'

    contrasts = []
    for filename in sorted(os.listdir(shots_output_path)):
        img = cv2.imread(os.path.join(shots_output_path, filename))
        if img is not None:
            # Use RMS contrast for contrast measurement
            img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            contrast = img_grey.std() / 100
            contrasts.append(str(contrast))

    temp = []
    results = []
    for i in range(len(contrasts)):
        if i == 0 or i % 3 != 0:
            temp.append(contrasts[i])
            if i == len(contrasts) - 1:
                mean_contrast = np.mean(np.array(temp).astype(np.float))
                results.append(mean_contrast)
                print("Average contrast: shot " + str((int(i / 3) + 1)) +
                      " is " + mean_contrast.astype(str) + " (RMS)")
        else:
            mean_contrast = np.mean(np.array(temp).astype(np.float))
            results.append(mean_contrast)
            print("Average contrast: shot " + str(int(i / 3)) + " is " +
                  mean_contrast.astype(str) + " (RMS)")
            temp = []
            temp.append(contrasts[i])
    return results


# Get average background color for each shot
def get_background(video):
    shots_output_path = f'{shots}/{video}/screenshots/'
    for filename in sorted(os.listdir(shots_output_path)):
        if filename.endswith(".jpg"):
            background = BackgroundColorDetector(
                os.path.join(shots_output_path, filename), filename)
            background.detect()
