from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse

# from .forms import ContactForm
# from .forms import LoginForm, RegisterForm


def home_page(request):
  context = {
    "title": "Hello from the homepageeeee",
     "premium_content": "Yeeaaaahhhh premium content!",
  }
  if request.user.is_authenticated:
    print("user is authenticated")

  return render(request, "home_page.html", context)