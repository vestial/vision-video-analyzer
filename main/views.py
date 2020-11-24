from django.conf import settings
from django.http import request, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.utils.safestring import mark_safe
from django.contrib import messages

from main.models import Video
import os
from main.analyzer import get_frame_rate, get_resolution, get_thumbnail, get_bit_rate 

# Home view
def home(response):

	#Checks if media folder exists
	if os.path.isdir('./media') == False :
		os.mkdir('media')
	if os.path.isdir('./media/thumbnails') == False :
		os.mkdir('media/thumbnails')
	if os.path.isdir('./media/videos') == False :
		os.mkdir('media/videos')

	#Checks the validity of video upload
	if response.method == "POST":
		uploaded_file = response.FILES['document']
		if uploaded_file.content_type[:5] == "video":
			print("upload successful")
			video = Video(name=uploaded_file.name, video=uploaded_file, uploader=response.user)
			video.save()
			video.thumbnail = get_thumbnail(uploaded_file)
			video.resolution = get_resolution(uploaded_file)
			video.frame_rate = get_frame_rate(uploaded_file)
			video.bit_rate = get_bit_rate(uploaded_file)
			video.save()
			messages.success(response, mark_safe("The video was uploaded successfully. Check out the video <a href='/videos/" + str(video.id) +"'>here</a>"))
		else:
			print("Upload unsuccessful")
			messages.error(response, "The uploaded file is not a video!")
	return render(response, "main/home.html", {})

# Videos view
def videos(response):
	path = os.path.join(settings.MEDIA_ROOT, "videos")
	video_list = list()
	allVideos = Video.objects.filter(uploader=response.user)
	for video in allVideos:
		video_list.append(video)
	context = {"videos": video_list}
	return render(response, "main/videos.html", context)

# Video view
def video(response, id):
	vid = Video.objects.filter(id=id).first()
	context = {"video": vid}
	return render(response, "main/video.html", context)

def delete(request, id):
	vid = get_object_or_404(Video, id=id)
	context = {"video": vid}
	if request.method == "POST":
		vid.delete()
		return HttpResponseRedirect("/videos")
	return render(request, "main/delete.html", context)