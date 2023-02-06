from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
#from django.contrib.auth.models import User
import uuid

ACCOUNT_TYPES = (
    ('M', 'Musician'),
    ('G', 'Group'),
)
class User(AbstractUser):
    
    username = models.CharField(max_length=100, null=False)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    account_type = models.CharField(default='M', max_length = 10, choices = ACCOUNT_TYPES)
    #musician_Account = models.BooleanField(default=False, null=True)
    #group_Account = models.BooleanField(default=False, null=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=100)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Event(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    flier = models.ImageField(null=True, blank=True, default="flyer.png")
    instruments_needed = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # many to many relationship
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    occurring = models.DateField(null=True)
    #time = models.TimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # this is a one to many relationship
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
    


    def __str__(self):
        return self.body[0:50]

    
experience_choices = (
    ('One Year','0-1'),
    ('Two To Three Years','2-3'),
    ('Four To Seven Years','4-7'),
    ('Eight Or More Years','8+'),
)

class Musician(models.Model):
    # username, primary key, charfield,  max length of 60
    #uname = models.CharField(max_length = 60, primary_key = True) #fk???
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # instruments, charfield, max length of 200
    instruments = models.CharField(max_length = 200)

    # genres, charfield, max length of 200
    genres = models.CharField(max_length = 200)

    # experience, floatfield, no max length?
    experience = models.CharField(default='One Year',max_length = 19, choices = experience_choices)

    #location, charField, max length of 50
    location = models.CharField(max_length = 50)

    #demo, url field, max lenght of 200, will be a url to the demo?
    demo = models.URLField(max_length = 200, null = True, blank = True)


class Group(models.Model):
    #username, charfield, max length of 60, primary key
    #uname = models.CharField(max_length = 60, primary_key = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    #group name, charfield, max length of 60
    group_name = models.CharField(max_length = 60)

    #genre, charfield, max length of 30
    genre = models.CharField(max_length = 30)

    #location, charfield, max length of 30
    location = models.CharField(max_length = 30)
    

class Contract(models.Model):
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete = models.CASCADE, null = True, blank = True)

    #unique id for each contract
    contract_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    description = models.TextField(max_length = 500)

    start_time = models.CharField(max_length = 10, default='TBD')
    end_time = models.CharField(max_length = 10, default='TBD')
    location = models.CharField(max_length =100, default='TBD')
    pay = models.DecimalField(max_digits=7, decimal_places=2, default='15.00')

    def __str__(self):
         return self.musician.user.first_name + "'s Contract"
