from vision_video_analyzer.settings import MEDIA_ROOT
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery import shared_task

import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

logger = get_task_logger(__name__)
shots = f'{MEDIA_ROOT}/shots'


@shared_task
def get_exposure_histogram(video):
    shots_output_path = f'{shots}/{video}/screenshots/'
    histogram_output_path = f'{shots}/{video}/histograms/'
    if os.path.isdir(histogram_output_path) == False:
        os.mkdir(histogram_output_path)
    logger.info("Calculating histogram")
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
            if bright_pixels / total_pixels > 0.5:
                logger.info(f'{filename} is overexposed!')
            plt.figure()
            plt.title("Grayscale Histogram")
            plt.xlabel("Bins")
            plt.ylabel("# of Pixels")
            plt.plot(hist)
            plt.xlim([0, 256])
            plt.savefig(histogram_output_path + filename)
            logger.info(filename + " Histogram calculated")
