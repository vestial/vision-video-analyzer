from django.conf import settings
from django.http import request
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import os

# Create your views here.
def home(response):

	#Checks if media folder exists
	if os.path.isdir('./media') == False :
		os.mkdir('media')

	if response.method == "POST":
		uploaded_file = response.FILES['document']
		if uploaded_file.content_type[:5] == "video":
			print("upload successful")
			messages.success(response, "The video was uploaded successfully.")
			fs = FileSystemStorage()
			fs.save(uploaded_file.name, uploaded_file)
		else:
			print("Upload unsuccessful")
			messages.error(response, "The uploaded file is not a video!")
	return render(response, "main/home.html", {})

def videos(response):
	path = settings.MEDIA_ROOT
	video_list = os.listdir(path)
	context = {"videos": video_list}
	return render(response, "main/videos.html", context)

