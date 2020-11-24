from main.models import Video
from vision_video_analyzer.settings import MEDIA_ROOT
import subprocess
import numpy as np

videos = f'{MEDIA_ROOT}/videos'
thumbnails = f'{MEDIA_ROOT}/thumbnails'

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
    bit_rate = subprocess.run(['ffprobe', '-v', '0', '-select_streams', 'a:0', '-show_entries', 'stream=bit_rate',
                               '-of', 'compact=p=0:nk=1', video_input_path], capture_output=True, text=True, input="Y")
    rounded_bit_rate = str(
        np.round(np.divide(int(bit_rate.stdout), 1000))) + " kbps"
    return rounded_bit_rate

#Get video length using ffprobe. Might need to have a better time format later
def get_video_length(video):
    video_input_path = f'{videos}/{video}'
    video_length = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                                   'default=noprint_wrappers=1:nokey=1', video_input_path], capture_output=True, text=True, input="Y")
    rounded_video_length = str(int(np.round(float(video_length.stdout)))) + " seconds"
    return rounded_video_length
