from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Article(models.Model):
    title = models.CharField(verbose_name='Title',max_length=255, blank=True, null=True)
    description = models.TextField(verbose_name='description',max_length=255,blank=True, null=True)
    updated_at = models.DateTimeField(verbose_name='Updated_at',auto_now=True, blank=True, null=True)
    author = models.ForeignKey(
        User,
        verbose_name='Author',
        on_delete=models.CASCADE, 
        related_name='articles',
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(viewname='article', kwargs={'pk': self.pk})