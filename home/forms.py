from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = {'main_char'}


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {
            'username',
            # 'userprofile.main_char'
        }