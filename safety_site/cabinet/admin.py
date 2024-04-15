from django.contrib import admin
from cabinet.models import NeuralNetwork, Camera, Place, Violation, Record, Report, Statistic

# Register your models here.

admin.register(NeuralNetwork, Camera, Place, Violation, Record, Report, Statistic)