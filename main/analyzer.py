from main.models import Video
from vision_video_analyzer.settings import MEDIA_ROOT
import subprocess

videos = f'{MEDIA_ROOT}/videos'
thumbnails = f'{MEDIA_ROOT}/thumbnails'
def get_thumbnail(video):
    print(MEDIA_ROOT)
    video_input_path = f'{videos}/{video}'
    img_output_path = f'{thumbnails}/{video}.png'
    subprocess.run(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000', '-vframes', '1', img_output_path], capture_output=True, text=True, input="Y")
