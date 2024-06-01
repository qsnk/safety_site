from django.contrib import admin
from cabinet.models import NeuralNetwork, Camera, Place, Violation, Report

# Register your models here.

@admin.register(NeuralNetwork)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "file"]


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "user_id"]


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "camera_id", "user_id"]


@admin.register(Violation)
class ViolationAdmin(admin.ModelAdmin):
    list_display = ["date_time", "violation_class", "description", "photo", "user_id"]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["date_time", "violation_id", "file"]