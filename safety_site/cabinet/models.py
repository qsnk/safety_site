from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class NeuralNetwork(models.Model):
    name = models.CharField(name="name", max_length=100, null=False, help_text="Введите название нейронной сети", verbose_name="Название нейронной сети")
    description = models.CharField(name="description", max_length=200, null=True, help_text="Введите описание нейронной сети", verbose_name="Описание нейронной сети")
    date_time = models.DateTimeField(name="date_time", auto_now_add=True, verbose_name="Дата и время добавления", null=False, help_text="Введите дату и время добавления")
    file = models.FileField(name="file", verbose_name="Файл", upload_to="neural_networks/")

    def __str__(self):
        return self.name


class Camera(models.Model):
    name = models.CharField(name="name",max_length=100, null=False, help_text="Введите название камеры", verbose_name="Название камеры")
    date_time = models.DateTimeField(name="date_time", auto_now_add=True, verbose_name="Дата и время добавления", null=False, help_text="Введите дату и время добавления")
    url = models.CharField(name="url", max_length=300, null=False, help_text="Введите ссылку для подключения к камере", verbose_name="Ссылка для подключения к камере")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", verbose_name="Идентификатор пользователя")

    def __str__(self):
        return f'Камера: {self.name}'


class Place(models.Model):
    name = models.CharField(name="name", max_length=100, null=False, help_text="Введите название площадки", verbose_name="Название площадки")
    description = models.CharField(name="description", max_length=200, null=True, default="Описания нет", help_text="Введите описание площадки", verbose_name="Описание площадки")
    date_time = models.DateTimeField(name="date_time", auto_now_add=True, verbose_name="Дата и время добавления", null=False, help_text="Введите дату и время добавления")
    camera_id = models.ForeignKey(Camera, on_delete=models.CASCADE, db_column="camera_id", verbose_name="Идентификатор камеры", default=None)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", verbose_name="Идентификатор пользователя", default=None)

    def __str__(self):
        return self.name


class Violation(models.Model):
    date_time = models.DateTimeField(name="date_time", auto_now_add=True, verbose_name="Дата и время нарушения", null=False, help_text="Введите дату и время нарушения")
    violation_class = models.CharField(name="violation_class", max_length=100, null=False, help_text="Введите название нарушения", verbose_name="Название нарушения")
    violation_class_ru = models.CharField(name="violation_class_ru", max_length=100, null=False, default="Отсутствует", help_text="Введите название нарушения на руссокм", verbose_name="Название нарушения (рус)")
    description = models.CharField(max_length=200, null=True, help_text="Введите описание нарушения", verbose_name="Описание нарушения")
    photo = models.ImageField(name="photo", verbose_name="Изображение", null=False, upload_to='violations/images/')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", verbose_name="Идентификатор пользователя")
    video = models.FileField(name="video", verbose_name="Видео", null=True, default=None, upload_to='violations/videos/')

    def __str__(self):
        return f'{self.violation_class_ru} [{self.date_time.strftime("%d-%m-%Y %H:%M")}]'


class Report(models.Model):
    name = models.CharField(name="name", max_length=200, null=False, help_text="Введите название отчета", verbose_name="Название отчета")
    date_time = models.DateTimeField(name="date_time", auto_now_add=True, verbose_name="Дата и время формирования отчета")
    violation_id = models.ForeignKey(Violation, on_delete=models.CASCADE, default=None, db_column="violation_id", verbose_name="Идентификатор нарушения")
    file = models.FileField(name="file", null=True, blank=True, verbose_name="Файл", upload_to="reports/")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", default=1, verbose_name="Идентификатор пользователя")

    def __str__(self):
        return f"Отчет за {self.date_time.strftime('%d.%m.%y %H:%M')}"