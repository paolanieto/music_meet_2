from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User
import uuid

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# Create your models here.
# this is where we are going to create our database tables

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Event(models.Model):
    event_id = models.UUIDField(default=uuid.uuid4(), editable=False, primary_key=True)

    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # many to many relationship
    participants = models.ManyToManyField(User, related_name = 'participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    instruments = models.CharField(max_length=20, blank = True, null = True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4(), editable=False, primary_key=True)

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

class Musician(models.Model):
    musician_id = models.UUIDField(default=uuid.uuid4(), editable=False, primary_key=True)

    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    # instruments, charfield, max length of 200
    instruments = models.CharField(max_length = 200)

    # genres, charfield, max length of 200
    genres = models.CharField(max_length = 200)

    # experience, floatfield, no max length?
    experience = models.FloatField()

    #location, charField, max length of 50
    location = models.CharField(max_length = 50)

    #demo, url field, max lenght of 200, will be a url to the demo?
    demo = models.URLField(max_length = 200)

    def __str__(self):
         return self.user.first_name + self.user.last_name


class Group(models.Model):
    group_id = models.UUIDField(default=uuid.uuid4(), editable=False, primary_key=True)

    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)

    #group name, charfield, max length of 60
    group_name = models.CharField(max_length = 60)

    #genre, charfield, max length of 30
    genre = models.CharField(max_length = 30)

    #location, charfield, max length of 30
    location = models.CharField(max_length = 30)

    #in case the group gets deleted the contract should still be in the database
    events = models.ForeignKey(Event, on_delete = models.PROTECT, null = True, blank = True)

    def __str__(self):
        return self.group_name
    

class Contract(models.Model):
    contract_id = models.UUIDField(default=uuid.uuid4(), editable=False, primary_key=True)

    musician = models.ForeignKey(Musician, on_delete=models.PROTECT)
    event = models.ForeignKey('Event', on_delete = models.PROTECT, null = True, blank = True)

    description = models.TextField(max_length = 500)

    start_time = models.CharField(max_length = 10, default='TBD')
    end_time = models.CharField(max_length = 10, default='TBD')
    location = models.CharField(max_length =100, default='TBD')
    pay = models.DecimalField(max_digits=7, decimal_places=2, default='15.00')

    def __str__(self):
         return self.musician.user.first_name + "'s Contract"
