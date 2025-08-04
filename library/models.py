from django.db import models

class Book(models.Model):
    class Cover(models.TextChoices):
        HARD = "HARD", "Hardcover"
        SOFT = "SOFT", "Softcover"

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(
        max_length=4,
        choices=Cover.choices
    )
    inventory = models.IntegerField()

    def __str__(self):
        return self.title


