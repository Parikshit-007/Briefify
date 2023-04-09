from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#from bson.objectid import ObjectIdField

 # add this line


class UserProfile(models.Model):
   # user_id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)
    first_name = models.CharField(max_length=50,default='')
    username = models.CharField(max_length=50, default='')
    email = models.EmailField(default='')
    password = models.CharField(max_length=100,default='')
    video_file = models.FileField(upload_to="main/videos",default='default_value')
   # id = models.ObjectIdField(primary_key=True)

    def __str__(self):
        return self.username
    def register(self):
        self.save()

    # ...

    # ...2

  
    @staticmethod
    def get_user_by_email(email):
        try:
            return UserProfile.objects.get(email=email)
        except:
            return False
  
    def isExists(self):
        if UserProfile.objects.filter(email=self.email):
            return True
  
        return False   

    def __str__(self):
       return self.user.username    
class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    title = models.CharField(max_length=100)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to="main/videos")
# Create your models here.

class Summary(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, default=None)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    title=models.CharField(max_length=100, default='')
    summary_text = models.TextField()
    summary_words = models.IntegerField(default=0)
    transcript_words = models.IntegerField(default=0)
    duration = models.CharField(max_length=20, null=True, blank=True)
    generated_date = models.DateTimeField(auto_now_add=True)
    #id = models.OneToOneField(UserProfile, primary_key=True, on_delete=models.CASCADE, related_name='user_summary')
    def __str__(self):
       if self.user is not None:
          return f"{self.user.username}'s summary for {self.video.title}"
       else:
        return 'Missing user'
    def save(self, *args, **kwargs):
       self.title = self.video.title
       super().save(*args, **kwargs)    

class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files/')       