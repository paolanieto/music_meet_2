from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Event, Group, Musician, User
#from django.contrib.auth.models import User


class MyUserCreationForm(UserCreationForm):
    musician_Account = UserCreationForm.BooleanField(widget=UserCreationForm.Select(choices=(True, False)))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'musician_Account', 'group_Account', 'username', 'email', 'password1', 'password2']

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        # FixingEventForm 10_22_222
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','first_name', 'last_name','username', 'email', 'bio']


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ['user']

class MusicianForm(ModelForm):
    class Meta:
        model = Musician
        fields = '__all__'
        exclude = ['user']

