from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class NeuralNetwork(models.Model):
    name = models.CharField(name="name", max_length=100, null=False, help_text="Введите название нейронной сети", verbose_name="Название нейронной сети")
    description = models.CharField(name="description", max_length=200, null=True, help_text="Введите описание нейронной сети", verbose_name="Описание нейронной сети")
    file = models.FileField(name="file", verbose_name="Файл", upload_to="neural_networks/")

    def __str__(self):
        return f'{self.name}'


class Camera(models.Model):
    name = models.CharField(name="name",max_length=100, null=False, help_text="Введите название камеры", verbose_name="Название камеры")
    url = models.CharField(name="url", max_length=300, null=False, help_text="Введите ссылку для подключения к камере", verbose_name="Ссылка для подключения к камере")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", verbose_name="Идентификатор пользователя")

    def __str__(self):
        return f'Камера участка: {self.name}'


class Place(models.Model):
    name = models.CharField(name="name", max_length=100, null=False, help_text="Введите название площадки", verbose_name="Название площадки")
    description = models.CharField(name="description", max_length=200, null=True, help_text="Введите описание площадки", verbose_name="Описание площадки")
    camera_id = models.ForeignKey(Camera, on_delete=models.CASCADE, db_column="camera_id", verbose_name="Идентификатор камеры", default=None)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", verbose_name="Идентификатор пользователя", default=None)

    def __str__(self):
        return f'Площадка: {self.name}'


class Violation(models.Model):
    date_time = models.DateTimeField(name="date_time", auto_now_add=True, verbose_name="Дата и время нарушения")
    violation_class = models.CharField(name="violation_class", max_length=100, null=False, help_text="Введите название нарушения", verbose_name="Название нарушения")
    description = models.CharField(max_length=200, null=True, help_text="Введите описание нарушения", verbose_name="Описание нарушения")
    photo = models.ImageField(name="photo", verbose_name="Изображение", null=False, upload_to='static/images/')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", verbose_name="Идентификатор пользователя")

    def __str__(self):
        return f'Нарушение: {self.violation_class}'


class Record(models.Model):
    date_time = models.DateTimeField(name="date_time", auto_now_add=True, verbose_name="Дата и время записи")
    violation = models.ForeignKey(Violation, on_delete=models.CASCADE, db_column="violation_id", verbose_name="Идентификатор нарушения")

    def __str__(self):
        return f'Запись журнала за {self.date_time}'


class Report(models.Model):
    date_time = models.DateTimeField(name="date_time", auto_now_add=True, verbose_name="Дата и время формирования отчета")
    record_id = models.ForeignKey(Record, on_delete=models.CASCADE, db_column="record_id", verbose_name="Идентификатор записи")
    file = models.FileField(name="file", upload_to="reports/")

    def __str__(self):
        return f'Отчет за {self.date_time}'


class Statistic(models.Model):
    period = models.DurationField(name="period")
    violations = models.CharField(name="violations", max_length=500, null=False, verbose_name="Нарушения")
    counter = models.IntegerField(name="number_of_violations", null=False, help_text="Введите количество нарушений", verbose_name="Количество нарушений")

    def __str__(self):
        return f'Статистика за {self.period}'