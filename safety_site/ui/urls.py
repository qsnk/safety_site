from django.urls import path
from ui.views import *


urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login')
]