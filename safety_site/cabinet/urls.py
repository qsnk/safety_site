from django.urls import path
from cabinet.views import *


urlpatterns = [
    path('', index, name='cabinet_index'),
    path('cameras/', cameras, name='cabinet_cameras'),
]