from django.db import models

# Create your models here.
class Online(models.Model):
    name = models.CharField(max_length=100, db_index=True)  # channel_name of each user in chat

    def __str__(self):
        return self.name