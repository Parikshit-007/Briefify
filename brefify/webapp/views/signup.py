from django.forms import ValidationError
from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password, make_password
from webapp.models import UserProfile
from django.views import View
from django import template
from django.core.validators import validate_email
import re


class Signup (View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        username = postData.get('username')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'username': username,
            'email': email,
        }
        error_message = None

        # email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error_message = "Invalid email address"

        user = UserProfile(first_name=first_name,
                             username=username,
                             email=email,
                             password=password)
        error_message = self.validateUser(user)

        if not error_message:
            print(first_name, username, email, password)
            user.password = make_password(user.password)
            user.register()
            return redirect('index')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'login.html', data)

    def validateUser(self, user):
         error_message = None
         if not user.first_name:
            error_message = "Please Enter your First Name!!"
         elif len(user.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
         elif not user.username:
             error_message = 'Please Enter your User Name'
         elif len(user.username) < 3:
             error_message = 'Last Name must be 3 char long or more'
         elif len(user.password) < 5:
              error_message = 'Password must be 5 char long'
         else:
             try:
                 validate_email(user.email)
             except ValidationError:
                 error_message = 'Please enter a valid email address'
             else:
               if user.isExists():
                 error_message = 'Email Address Already Registered..'

         return error_message    