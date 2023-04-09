from django.shortcuts import redirect, render
from webapp.models import Video, UserProfile

def video_list(request):
    # Check if the user is authenticated
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    else:
        # Fetch all videos from the database
        videos = Video.objects.all()
        # Filter videos by the current user's UserProfile instance
        user_profile = UserProfile.objects.get(id=user_id)
        if user_profile.user:
           user_videos = videos.filter(user=user_profile)
           return render(request, 'storage.html', {'videos': user_videos})
        else:
            return redirect('login')
        # Render the template with the filtered videos
      #  return render(request, 'storage.html', {'videos': user_videos})

def  video_view(request,video_id):
     videos=Video.objects.all()
     print(videos)
     video = Video.objects.get(id=video_id)
     return render(request, 'video.html', {'video':video})
