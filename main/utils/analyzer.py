from main.utils.feedback.video_length import get_video_length_recommendation
from main.utils.feedback.sample_rate import get_sample_rate_recommendation
from main.utils.feedback.bit_depth import get_bit_depth_recommendation
from main.utils.feedback.bit_rate import get_bit_rate_recommendation
from main.utils.feedback.frame_rate import get_frame_rate_recommendation
from main.utils.feedback.resolution import get_resolution_recommendation
from pymediainfo import MediaInfo
from vision_video_analyzer.settings import MEDIA_ROOT
from main.utils.background import BackgroundColorDetector
import subprocess
import numpy as np

videos = f'{MEDIA_ROOT}/videos'
thumbnails = f'{MEDIA_ROOT}/thumbnails'
shots = f'{MEDIA_ROOT}/shots'


# Wrapper for the analysis getters
def analyze_video(video, uploaded_file):
    video.thumbnail = get_thumbnail(uploaded_file)

    video.resolution = get_resolution(uploaded_file)
    video.resolution_rating = get_resolution_recommendation(video)[0]
    video.resolution_recommendation = get_resolution_recommendation(video)[1]
    video.resolution_recommended = "1920x1080 (1080p) up to 3840x2160 (4K)"

    video.frame_rate = get_frame_rate(uploaded_file)
    video.frame_rate_rating = get_frame_rate_recommendation(video)[0]
    video.frame_rate_recommendation = get_frame_rate_recommendation(video)[1]
    video.frame_rate_recommended = "24 - 60 fps"

    video.bit_rate = get_bit_rate(uploaded_file)
    video.bit_rate_rating = get_bit_rate_recommendation(video)[0]
    video.bit_rate_recommendation = get_bit_rate_recommendation(video)[1]
    video.bit_rate_recommended = get_bit_rate_recommendation(video)[2]

    video.bit_depth = get_bit_depth(uploaded_file)
    video.bit_depth_rating = get_bit_depth_recommendation(video)[0]
    video.bit_depth_recommendation = get_bit_depth_recommendation(video)[1]
    video.bit_depth_recommended = "8 - 12 bits"

    video.sample_rate = get_sample_rate(uploaded_file)
    video.sample_rate_rating = get_sample_rate_recommendation(video)[0]
    video.sample_rate_recommendation = get_sample_rate_recommendation(video)[1]
    video.sample_rate_recommended = "44.1 kHz - 48.0 kHz"

    video.video_length = get_video_length(uploaded_file)
    video.video_length_rating = get_video_length_recommendation(video)[0]
    video.video_length_recommendation = get_video_length_recommendation(
        video)[1]
    video.video_length_recommended = "Up to 5 minutes"


# Use ffmpeg to get the thumbnail
def get_thumbnail(video):
    video_input_path = f'{videos}/{video}'
    img_output_path = f'{thumbnails}/{video}.png'
    subprocess.run([
        'ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000', '-vframes',
        '1', img_output_path
    ],
                   capture_output=True,
                   text=True,
                   input="Y")


#Checks if the thumbnail is pure black or white
def thumbnail_checker(video):
    video_input_path = f'{videos}/{video}'
    img_output_path = f'{thumbnails}/{video}.png'
    thumbnail = BackgroundColorDetector(img_output_path, video.name + ".png")
    if thumbnail.detect() == "0, 0, 0" or thumbnail.detect(
    ) == "255, 255, 255":
        subprocess.run([
            'ffmpeg', '-i', video_input_path, '-ss', '00:00:03.5', '-vframes',
            '1', img_output_path
        ],
                       capture_output=True,
                       text=True,
                       input="Y")


# Use ffprobe to get the video resolution
def get_resolution(video):
    video_input_path = f'{videos}/{video}'
    resolution = subprocess.run([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
        'stream=width,height', '-of', 'csv=s=x:p=0 ', video_input_path
    ],
                                capture_output=True,
                                text=True,
                                input="Y")
    return resolution.stdout


# Get video fps from ffprobe in frame/sec format. Rounded to make it look better
def get_frame_rate(video):
    video_input_path = f'{videos}/{video}'
    frame_rate = subprocess.run([
        'ffprobe', '-v', '0', '-of', 'csv=p=0', '-select_streams', 'v:0',
        '-show_entries', 'stream=r_frame_rate', video_input_path
    ],
                                capture_output=True,
                                text=True,
                                input="Y")
    fps_string = frame_rate.stdout
    if fps_string is None:
        return "Unknown"
    a = int(fps_string.split('/')[0])
    b = int(fps_string.split('/')[1])
    rounded_fps = int(np.round(np.divide(a, b)))
    return rounded_fps


# Get video bit rate using MediaInfo and format it to mbps
def get_bit_rate(video):
    video_input_path = f'{videos}/{video}'
    media_info = MediaInfo.parse(video_input_path)
    bit_rate = media_info.video_tracks[0].bit_rate
    return str(np.round(np.divide(int(bit_rate), 1000000), 1))


# Get video bit depth using MediaInfo
def get_bit_depth(video):
    video_input_path = f'{videos}/{video}'
    media_info = MediaInfo.parse(video_input_path)
    bit_depth = media_info.video_tracks[0].bit_depth
    return bit_depth


# Get sample rate using ffprobe and convert to kHz
def get_sample_rate(video):
    video_input_path = f'{videos}/{video}'
    sample_rate = subprocess.run([
        'ffprobe', '-v', '1', '-of', 'csv=p=0', '-select_streams', 'a:0',
        '-show_entries', 'stream=sample_rate', video_input_path
    ],
                                 capture_output=True,
                                 text=True,
                                 input="Y")

    if not sample_rate.stdout:
        return "Unknown"
    rounded_sample_rate = np.round(np.divide(int(sample_rate.stdout), 1000))
    return rounded_sample_rate


# Get video length using ffprobe. Might need to have a better time format later
def get_video_length(video):
    video_input_path = f'{videos}/{video}'
    video_length = subprocess.run([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
        'default=noprint_wrappers=1:nokey=1', video_input_path
    ],
                                  capture_output=True,
                                  text=True,
                                  input="Y")
    rounded_video_length = int(np.round(float(video_length.stdout)))
    return rounded_video_length
