from main.shots_analyzer import analyze_shots
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.contrib import messages

from main.models import Video
import os
import shutil
from main.analyzer import analyze_video, get_thumbnail


# Home view
def home(response):

    #Checks if media folder exists
    if os.path.isdir('./media') == False:
        os.mkdir('media')
    if os.path.isdir('./media/thumbnails') == False:
        os.mkdir('media/thumbnails')
    if os.path.isdir('./media/videos') == False:
        os.mkdir('media/videos')
    if os.path.isdir('./media/shots') == False:
        os.mkdir('media/shots')

    #Checks the validity of video upload
    if response.method == "POST":
        if (response.FILES.get('document') is None):
            print("No video uploaded")
            messages.error(response, "Please choose a video to upload!")
            return render(response, "main/home.html", {})
        uploaded_file = response.FILES['document']
        if uploaded_file.content_type[:5] == "video":
            print("upload successful")
            video = Video(name=uploaded_file.name,
                          video=uploaded_file,
                          uploader=response.user,
                          thumbnail=get_thumbnail(uploaded_file))
            video.save()
            analyze_video(video, uploaded_file)
            video.save()
            messages.success(
                response,
                mark_safe(
                    "The video was uploaded successfully. Check out the video <a href='/videos/"
                    + str(video.id) + "'>here</a>"))
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
        vid.video.delete()
        if (os.path.isfile('./media/videos/' + str(vid)) == False):
            if (os.path.isfile('./media/thumbnails/' + str(vid) +
                               ".png") == True):
                os.remove('./media/thumbnails/' + str(vid) + ".png")
            if (os.path.isdir('./media/shots/' + str(vid)) == True):
                shutil.rmtree('./media/shots/' + str(vid))
        vid.delete()
        return HttpResponseRedirect("/videos")
    return render(request, "main/delete.html", context)


def shots(response, id):
    vid = Video.objects.filter(id=id).first()
    context = {"video": vid}
    if response.method == "POST" and os.path.isdir('./media/shots/' +
                                                   str(vid)) == False:
        print("Analyzing shots")
        analyze_shots(vid.video)
    return render(response, "main/shots.html", context)
