from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('deduct', views.deduct, name='deduct'),
    path('play', views.play, name='play'),
    path('update', views.update, name='update'),
]