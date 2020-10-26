from django.http import request
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

# Create your views here.
def home(response):
	if response.method == "POST":
		uploaded_file = response.FILES['document']
		if uploaded_file.content_type[:5] == "video":
			print("upload successful")
			messages.success(response, "The video was uploaded successfully.")
			fs = FileSystemStorage()
			fs.save(uploaded_file.name, uploaded_file)
		else:
			messages.error(response, "The uploaded file is not a video!")
	return render(response, "main/home.html", {})

def videos(response):
	return render(response, "main/videos.html", {})

