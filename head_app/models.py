from django.db import models

# Create your models here.


class TeacherModel(models.Model):
    username = models.CharField(verbose_name='username', max_length=100, null=True)
    chat_id = models.CharField(verbose_name='chat_id', max_length=100, null=True)
    name = models.CharField(verbose_name='ФИО', max_length=100)
    subject = models.CharField(verbose_name='Предмет', max_length=100)


    def __str__(self):
        return f'{self.name} -- {self.subject}'


class StudentModel(models.Model):
    username = models.CharField(verbose_name='username', max_length=100, null=True)
    chat_id = models.CharField(verbose_name='chat_id', max_length=100, null=True)
    name = models.CharField(verbose_name='ФИО', max_length=100)
    form = models.CharField(verbose_name='Класс', max_length=100)

    def __str__(self):
        return f'{self.name} -- {self.form}'
    





