from django.contrib import admin
from django.urls import path,include
from webapp.views.login import Login, logout
from webapp. views.signup import Signup
from webapp. views.homepage import index
from webapp. views.dashboard import Dashboard, MyVideosView, summary_view
from django.conf import settings
from django.conf.urls.static import static
from. views.uploads import upload_video
from .views.summary import process_video
from .views.storage import video_list, video_view
from .middlewares.auth import  auth_middleware
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from webapp.views.translate import translator,tt
from webapp.views.attendees import upload,display
from webapp.views.action_words import action_words
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='webapp/', permanent=True)),
    path('webapp/', index, name='index'), 
    path("signup/",Signup.as_view(), name='signup'),
    path("login/", Login.as_view(), name='login'),
    path("logout/", logout, name='logout'),
    path("dashboard/", Dashboard.as_view(), name='dashboard'),
    path("upload/", upload_video, name='upload_video'),
    path('summary/<int:video_id>/', process_video , name='summary'),
     path('summaryview/<int:summary_id>/', summary_view, name='summary_view'),
   # path('summaryview/', summary_list, {'summary_id': 0}, name='summary_view_default'),
    path("storage/",MyVideosView.as_view(), name='storage'),
    path('videoview/<int:video_id>/',video_view, name='video_view'),
    path('translatee/<int:summary_id>/', tt, name='translate_1'),
    path('translate/<int:summary_id>/', translator, name='translate'),
    path('upload_yo/', upload, name='upload'),
    path('display/<int:file_id>/', display, name='display'),
    path('actionpoints/<int:video_id>/',action_words, name='action_words'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)