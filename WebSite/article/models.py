from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime

# Create your models here.

# Get the current time
now = datetime.now()

# Format the time using strftime
formatted_date = now.strftime('%Y-%m-%d')

User = get_user_model()


class Article(models.Model):
    title = models.CharField(name='title',max_length=50, verbose_name='Title', null=True)
    description = models.TextField(name='description',max_length=255, verbose_name='Description', null=True)
    pup_date = models.DateField(default=formatted_date, name='pup_date', verbose_name='Pup Date',auto_now=False)
    author = models.ForeignKey(User, name='author',verbose_name='Author', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

