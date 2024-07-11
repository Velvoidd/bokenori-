from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Prefix(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    prefix = models.ForeignKey(Prefix, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username     
    # Получение существующего пользователя
try:
    existing_user = User.objects.get(username='existing_user')
except User.DoesNotExist:
    print("Пользователь с указанным именем не существует.")
else:
    # Создание нового объекта CustomUser с использованием данных существующего пользователя
    custom_user = CustomUser.objects.create(
        user=existing_user,
        nickname=existing_user.username,  # Используйте имя пользователя в качестве nickname или любое другое значение
        # Другие поля модели CustomUser
    )

    # Сохранение объекта CustomUser
    custom_user.save()

    class Meta:
        model = CustomUser
        fields = ['discord_link']



class DiscordInvitation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    invite_link = models.CharField(max_length=100, unique=True)

    @classmethod
    def generate_invite_link(cls):
        return str(uuid.uuid4())
    


class MinecraftUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    prefix = models.ForeignKey(Prefix, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.user.username
    
    

class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    date_published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)



    def __str__(self):
        return self.title
    

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'



class Application(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('rejected', 'Отклонено'),
        ('approved', 'Одобрено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    age = models.IntegerField()
    source = models.CharField(max_length=100)
    previous_projects = models.TextField()
    activities = models.TextField()
    read_rules = models.TextField()
    communication_style = models.CharField(max_length=100)
    participate_in_storyline = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    prefix = models.ForeignKey(Prefix, on_delete=models.SET_NULL, null=True, blank=True)
    discord_link = models.URLField(blank=True)

    def __str__(self):
        return f'Application {self.id} by {self.user.username}'




class ServerEvent(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Ближайший'),
        ('current', 'Текущий'),
        ('past', 'Прошедший'),
    )
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    date = models.DateTimeField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title