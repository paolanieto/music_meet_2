from django.forms import ModelForm
from .models import Event, Group, Musician
from django.contrib.auth.models import User


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        # FixingEventForm 10_22_222
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


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

