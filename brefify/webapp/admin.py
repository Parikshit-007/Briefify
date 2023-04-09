from django.contrib import admin
from . models import  UserProfile,Video, Summary

admin.site.register(UserProfile)
admin.site.register(Video)
admin.site.register(Summary)
# Register your models here.
