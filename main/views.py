from django.http import request
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# Create your views here.
def home(response):
	if response.method == "POST":
		uploaded_file = response.FILES['document']
		fs = FileSystemStorage()
		fs.save(uploaded_file.name, uploaded_file)
	return render(response, "main/home.html", {})

def videos(response):
	return render(response, "main/videos.html", {})

