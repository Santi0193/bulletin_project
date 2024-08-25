from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from ckeditor.fields import RichTextField

# Create your models here.


class Post(models.Model):
    CATEGORY = (
        ("tank", "Танки"),
        ("heal", "Хилы"),
        ("dd", "ДД"),
        ("buyers", "Торговцы"),
        ("gildmaster", "Гилдмастеры"),
        ("quest", "Квестгивверы"),
        ("smith", "Кузнецы"),
        ("tanner", "Кожевники"),
        ("potion", "Зельевары"),
        ("spellmaster", "Мастера заклинаний"),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    heading = models.CharField(max_length=255)
    text = RichTextField()
    category = models.CharField(max_length=11, choices=CATEGORY, default="tank")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("post", args=[str(self.pk)])

    def __str__(self):
        return f"{self.heading}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("post", args=[str(self.post.id)])

    def __str__(self):
        return f"{self.user} {self.text[:10]}..."
