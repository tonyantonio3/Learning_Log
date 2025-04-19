from tkinter.constants import CASCADE
from django.contrib.auth.models import User
from django.db import models


class Topic(models.Model):
    """Um assunto sobre o qual o usuário está estudando."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Deixa a primeira letra maiúscula e o restante minúsculo
        self.text = str(self.text).title()
        super().save(*args, **kwargs)

    def __str__(self):
        """Devolve uma representação em string do modelo"""
        return self.text

class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Devolve uma representação em string do modelo"""
        return self.text[:50] + '...'


