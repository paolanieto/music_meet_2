from django.contrib import admin

# Register your models here.


from .models import Event, Topic, Message, Contract, Group, Musician

admin.site.register(Event)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Contract)
admin.site.register(Group)
admin.site.register(Musician)