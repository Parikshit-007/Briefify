from django.shortcuts import render
from django.shortcuts import render , redirect , HttpResponseRedirect

def index(request):
    return render(request, 'home.html')
