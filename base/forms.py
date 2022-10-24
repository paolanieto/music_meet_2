from django.forms import ModelForm
from .models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        # FixingEventForm 10_22_222
        exclude = ['host', 'participants']
