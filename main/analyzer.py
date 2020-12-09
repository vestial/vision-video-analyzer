from main.background import BackgroundColorDetector
from main.models import Video
from pymediainfo import MediaInfo
from time import sleep
from vision_video_analyzer.settings import MEDIA_ROOT
import subprocess
import numpy as np
import cv2
import sys
import os

videos = f'{MEDIA_ROOT}/videos'
thumbnails = f'{MEDIA_ROOT}/thumbnails'
shots = f'{MEDIA_ROOT}/shots'

# Wrapper for the analysis getters


def analyze_video(video, uploaded_file):
    video.thumbnail = get_thumbnail(uploaded_file)
    video.resolution = get_resolution(uploaded_file)
    #video.shutter_speed = get_shutter_speed(uploaded_file)
    video.frame_rate = get_frame_rate(uploaded_file)
    video.bit_rate = get_bit_rate(uploaded_file)
    video.bit_depth = get_bit_depth(uploaded_file)
    video.sample_rate = get_sample_rate(uploaded_file)
    video.video_length = get_video_length(uploaded_file)

    get_shots(uploaded_file)
    get_shots_length(uploaded_file)
    get_contrast(uploaded_file)
    get_background(uploaded_file)
    
# Use ffmpeg to get the thumbnail


def get_thumbnail(video):
    video_input_path = f'{videos}/{video}'
    img_output_path = f'{thumbnails}/{video}.png'
    subprocess.run(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000',
                    '-vframes', '1', img_output_path], capture_output=True, text=True, input="Y")


# Use ffprobe to get the video resolution
def get_resolution(video):
    video_input_path = f'{videos}/{video}'
    resolution = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                 'stream=width,height', '-of', 'csv=s=x:p=0 ', video_input_path], capture_output=True, text=True, input="Y")
    return resolution.stdout

# def get_shutter_speed(video):
    # return "Unknown"
# Get fps from ffprobe in frame/sec format. Rounded to make it look better


def get_frame_rate(video):
    video_input_path = f'{videos}/{video}'
    frame_rate = subprocess.run(['ffprobe', '-v', '0', '-of', 'csv=p=0', '-select_streams', 'v:0',
                                 '-show_entries', 'stream=r_frame_rate', video_input_path], capture_output=True, text=True, input="Y")
    fps_string = frame_rate.stdout
    a = int(fps_string.split('/')[0])
    b = int(fps_string.split('/')[1])
    rounded_fps = int(np.round(np.divide(a, b)))
    return rounded_fps

# Get bit rate from ffprobe and format it to kbps


def get_bit_rate(video):
    video_input_path = f'{videos}/{video}'
    bit_rate = subprocess.run(['exiftool', '-s', '-s', '-s', '-avgBitrate',
                               video_input_path], capture_output=True, text=True, input="Y")

    return bit_rate.stdout

# Get bit depth using MediaInfo


def get_bit_depth(video):
    video_input_path = f'{videos}/{video}'
    media_info = MediaInfo.parse(video_input_path)
    bit_depth = media_info.video_tracks[0].bit_depth
    return str(bit_depth) + " bits"

# Get sample rate using ffprobe and convert to kHz


def get_sample_rate(video):
    video_input_path = f'{videos}/{video}'
    sample_rate = subprocess.run(['ffprobe', '-v', '1', '-of', 'csv=p=0', '-select_streams', 'a:0',
                                  '-show_entries', 'stream=sample_rate', video_input_path], capture_output=True, text=True, input="Y")
    rounded_sample_rate = str(
        np.round(np.divide(int(sample_rate.stdout), 1000))) + " kHz"
    return rounded_sample_rate

# Get video length using ffprobe. Might need to have a better time format later


def get_video_length(video):
    video_input_path = f'{videos}/{video}'
    video_length = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                                   'default=noprint_wrappers=1:nokey=1', video_input_path], capture_output=True, text=True, input="Y")
    rounded_video_length = str(
        int(np.round(float(video_length.stdout)))) + " seconds"
    return rounded_video_length

# Use pyscenedetect to split video into shots


def get_shots(video):
    video_input_path = f'{videos}/{video}'
    shots_screenshots_output_path = f'{shots}/{video}/screenshots/'
    shots_output_path = f'{shots}/{video}/shots/'

    process = subprocess.Popen(['scenedetect', '--input', video_input_path, 'detect-content', 'list-scenes', '-o',
                                shots_screenshots_output_path, 'save-images', '-o', shots_screenshots_output_path, 'split-video', '-o', shots_output_path], stdout=subprocess.PIPE)
    while stream_process(process):
        sleep(0.1)


def stream_process(process):
    go = process.poll() is None
    for line in process.stdout:
        print(line)
    return go


def get_shots_length(video):
    shots_output_path = f'{shots}/{video}/shots/'
    lengths = []
    for filename in sorted(os.listdir(shots_output_path)):
        length = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                                   'default=noprint_wrappers=1:nokey=1', os.path.join(shots_output_path, filename)], capture_output=True, text=True, input="Y")
        
        lengths.append( "Shot: "+ filename + " lasts "+ str(float(length.stdout)) + " seconds")
    for length in lengths:
        print(length)
    
    
# Get contrast of each shot images by using OpenCV

def get_contrast(video):
    shots_output_path = f'{shots}/{video}/screenshots/'

    result = []
    for filename in sorted(os.listdir(shots_output_path)):
        img = cv2.imread(os.path.join(shots_output_path, filename))
        if img is not None:
            # Use RMS contrast for contrast measurement
            img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            contrast = img_grey.std() / 100
            result.append(str(contrast))

    print(result)


def get_background(video):
    shots_output_path = f'{shots}/{video}/screenshots/'
    for filename in sorted(os.listdir(shots_output_path)):
        if filename.endswith(".jpg"):
            background = BackgroundColorDetector(os.path.join(shots_output_path, filename), filename)
            background.detect()