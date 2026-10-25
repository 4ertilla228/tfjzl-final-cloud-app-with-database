from django.db import models

# Create your models here.
class Question(models.Model):
    # Поля для вопроса
    text = models.CharField(max_length=200)
    grade = models.IntegerField(default=1)
    # связь с уроком (Lesson)

class Choice(models.Model):
    # Поля для выбора
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    # связь с вопросом (Question)

class Submission(models.Model):
    # Поля для результата экзамена
    pass