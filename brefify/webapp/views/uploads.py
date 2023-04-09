import os
import shutil
from django.shortcuts import redirect, render
from webapp.forms import VideoForm
from webapp.models import Video
from django.conf import settings


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            # Rename the uploaded file to match the title
            filename = f"{video.title}.mp4"
            new_path = os.path.join(settings.MEDIA_ROOT, filename)
            try:
                shutil.move(video.video_file.path, new_path)
            except FileNotFoundError:
                pass
            video.video_file.name = filename
            video.save()
            return redirect('dashboard')
    else:
        form = VideoForm()
    return render(request, 'upload.html', {'form': form})
