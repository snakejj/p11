from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import logout as log_out
from django.contrib.auth import login as log_in
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')

            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False
            user.save()

            messages.warning(
                request,
                "Merci de cliquer sur le lien envoyé dans votre boite mail !",
                fail_silently=True
            )
            return redirect('users:login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {
        'form': form,
        'title': "Inscription",
        'header_title': "Inscription", })


def profile(request):
    return render(request, 'users/profil.html', {'title': "Page de profil"})


def logout(request):
    log_out(request)
    messages.info(request, "On espere vous revoir bientot !", fail_silently=True)
    return redirect("core:home")


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        try:
            user_inst = User.objects.get(username=request.POST.get("username"))
            user_active = user_inst.is_active
            if user_active is False:
                messages.warning(
                    request,
                    "Merci de cliquer sur le lien envoyé dans votre boite mail !",
                    fail_silently=True
                )
                return redirect('users:login')
            else:
                if form.is_valid():
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password')
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        log_in(request, user)
                        messages.info(request, f"Bienvenue {username} !", fail_silently=True)
                        return redirect('/')

                else:
                    messages.error(request, "Nom d'utilisateur ou mot de passe incorrect", fail_silently=True)
        except:
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    log_in(request, user)
                    messages.info(request, f"Bienvenue {username} !", fail_silently=True)
                    return redirect('/')

            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect", fail_silently=True)
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {"form": form, 'title': "Login"})
