from django.urls import path
from cabinet.views import *


urlpatterns = [
    path('', index, name='cabinet_index'),
    path('cameras/', cameras, name='cabinet_cameras'),
    path('reports/', reports, name='cabinet_reports'),
    path('journal/', journal, name='cabinet_journal'),
    path('statistics/', statistics, name='cabinet_statistics'),
]