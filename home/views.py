from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.http import urlencode
from django.urls import reverse
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from .forms import UserProfileForm
from django.contrib.auth.models import User
from battles.models import Battle
from django.db.models import Q


# Create your views here.

def index(request):
    leader_list = UserProfile.objects.order_by('-rating')
    ctx = {
        'leader_list': leader_list,
    }
    return render(request, 'home/index.html', ctx)


def login_view(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        ctx = {
            'form': form,
        }
        try:
            if request.GET['invalid'] is not None:
                ctx['invalid'] = True
        except:
            pass

        return render(request, 'home/login.html', ctx)
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)

            return redirect('home:index')
        else:
            return redirect(reverse('home:login') + "?" + urlencode({'invalid': True}))


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home:index')


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home:index')
    else:
        form = UserCreationForm()
        profile_form = UserProfileForm()
    ctx = {
        'form': form,
        'profile_form': profile_form,
    }
    return render(request, 'registration/registration.html', ctx)


def profile_view(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    match_history = Battle.objects.filter(Q(player1=user.userprofile) | Q(player2=user.userprofile))
    ctx = {
        'match_history': match_history,
        'user': user
    }
    return render(request, 'home/profile.html', ctx)

