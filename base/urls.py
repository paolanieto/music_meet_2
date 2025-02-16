from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('event/<str:pk>/', views.event, name="event"),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),

    path('create-event/', views.createEvent, name="create-event"),
    path('update-event/<str:pk>', views.updateEvent, name="update-event"),
    path('delete-event/<str:pk>', views.deleteEvent, name="delete-event"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),
]