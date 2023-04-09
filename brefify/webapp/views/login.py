from django.shortcuts import render
from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth.hashers import  check_password, make_password
from  webapp.models import UserProfile
from django.views import View
from django import template

from django.shortcuts import render, redirect
from django.views import View
from webapp.models import UserProfile

class Login(View):
    return_url = None
    
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = UserProfile.get_user_by_email(email)
        next_url = request.GET.get('next')
        error_message = None
        if user:
            flag = check_password(password, user.password)
            if flag:
                # Set the user_id value in the session object
                request.session['user_id'] = user.id
                
                if Login.return_url:
                    return redirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('dashboard')
            else:
                error_message = 'Invalid password!'
        else:
            error_message = 'Invalid email!'
        context = {'next': next_url}
        return render(request, 'login.html', {'error': error_message}, context)

def logout(request):
    request.session.clear()
    return redirect('index')
