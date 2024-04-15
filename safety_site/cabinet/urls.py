from django.urls import path
from cabinet.views import *


urlpatterns = [
    path('', index, name='cabinet_index'),
    path('add-cameras/', add_cameras, name='cabinet_cameras'),
    path('watch/', watch_site, name='watch_site'),
    path('reports/', reports, name='cabinet_reports'),
    path('journal/', journal, name='cabinet_journal'),
    path('statistics/', statistics, name='cabinet_statistics'),
]