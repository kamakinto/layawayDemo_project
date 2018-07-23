from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import LoginForm
from django.utils.http import is_safe_url



def  login_page(request):
        form = LoginForm(request.POST or None)
        context = {
        "form": form
        }
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        if form.is_valid(): #if the form is clean, begin the log-in authentication process
                print(form.cleaned_data)
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(request, username=username, password=password)

                if user is not None: #if we have found a user, log them in, and handle the redirect
                        login(request, user)
                        context['form'] = LoginForm() #adds an empty login form after user is logged in.
                        if is_safe_url(redirect_path, request.get_host()):
                                return redirect(redirect_path)
                        else:
                                return redirect('/dashboard/')
                else:
                        print("Error") #return an invalid login error message
        return render(request, "login.html", context)


