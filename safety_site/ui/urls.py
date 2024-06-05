from django.urls import path
from ui.views import *


urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('login/', sign_in, name='login')
]