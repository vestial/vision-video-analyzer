# vision-video-analyzer

## Installation

1. Download the repo.
2. Make sure you have ffmpeg and mediainfo, and redis as apt packages installed.
3. Run `pipenv install` to install all the required modules.
4. Run `pipenv shell`.
5. Run `python manage.py runserver` to start the web app.
6. Run `celery -A vision_video_analyzer worker -l info` on another terminal.
6. Navigate to https://localhost:8000 to see the web app.