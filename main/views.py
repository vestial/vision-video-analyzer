from django.conf import settings
from django.http import request
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from main.models import Video
import os

# Home view
def home(response):

	#Checks if media folder exists
	if os.path.isdir('./media') == False :
		os.mkdir('media')

	#Checks the validity of video upload
	if response.method == "POST":
		uploaded_file = response.FILES['document']
		if uploaded_file.content_type[:5] == "video":
			print("upload successful")
			messages.success(response, "The video was uploaded successfully.")
			video = Video(name=uploaded_file.name, video=uploaded_file, uploader=response.user)
			video.save()
		else:
			print("Upload unsuccessful")
			messages.error(response, "The uploaded file is not a video!")
	return render(response, "main/home.html", {})

# Videos view
def videos(response):
	path = os.path.join(settings.MEDIA_ROOT, "videos")
	video_list = os.listdir(path)
	context = {"videos": video_list}
	return render(response, "main/videos.html", context)

