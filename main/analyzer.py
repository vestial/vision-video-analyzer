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

#Get fps from ffprobe in frame/sec format. Rounded to make it look better
def get_frame_rate(video):
    video_input_path = f'{videos}/{video}'
    frame_rate = subprocess.run(['ffprobe', '-v', '0', '-of', 'csv=p=0', '-select_streams', 'v:0',
                                 '-show_entries', 'stream=r_frame_rate', video_input_path], capture_output=True, text=True, input="Y")
    fps_string = frame_rate.stdout
    a = int(fps_string.split('/')[0])
    b = int(fps_string.split('/')[1])
    rounded_fps = int(np.round(np.divide(a,b)))
    return rounded_fps
