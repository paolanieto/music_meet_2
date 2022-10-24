from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# this is where we are going to create our database tables

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Event(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # many to many relationship
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
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

class Musician(models.Model):
    # username, primary key, charfield,  max length of 60
    user = models.ForeignKey(User, on_delete=models.CASCADE) #fk???

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