from django.urls import path
from cabinet.views import *


urlpatterns = [
    path('', index, name='cabinet_index'),
    path('add-camera/', add_cameras, name='cabinet_cameras'),
    path('add-place/', add_places, name='cabinet_places'),
    path('watch/', watch_site, name='watch_site'),
    path('watch/video', stream_video, name="stream_video"),
    path('reports/', reports, name='cabinet_reports'),
    path('journal/', journal, name='cabinet_journal'),
    path('statistics/', statistics, name='cabinet_statistics'),
]