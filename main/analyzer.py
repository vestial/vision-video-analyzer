from main.models import Video
from vision_video_analyzer.settings import MEDIA_ROOT
import subprocess

videos = f'{MEDIA_ROOT}/videos'
thumbnails = f'{MEDIA_ROOT}/thumbnails'

#Use ffmpeg to get the thumbnail
def get_thumbnail(video):
    video_input_path = f'{videos}/{video}'
    img_output_path = f'{thumbnails}/{video}.png'
    subprocess.run(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000',
                    '-vframes', '1', img_output_path], capture_output=True, text=True, input="Y")

#Use ffprobe to get the video resolution
def get_resolution(video):
    video_input_path = f'{videos}/{video}'
    resolution = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                 'stream=width,height', '-of', 'csv=s=x:p=0 ', video_input_path], capture_output=True, text=True, input="Y")
    return resolution.stdout
