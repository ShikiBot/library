from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books', views.index, name='books'),
    path('autors', views.index, name='autors'),
]
