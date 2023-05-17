from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class URLUser(AbstractUser):
    def __str__(self):
        return self.username

# class URLUser(models.Model):
#     firstname = models.CharField(max_length=100)
#     lastname  = models.CharField(max_length=100)
#     username  = models.CharField(max_length=50)
#     email     = models.EmailField()
#     # password = models.CharField(max_length=200)

    
class ShortenedURL(models.Model):
    original    = models.URLField()
    shortened   = models.URLField()
    dateCreated = models.DateField()
    hourCreated = models.TimeField()
    urlUser     = models.ForeignKey(URLUser, on_delete=models.CASCADE)

class Access(models.Model):
    navigator    = models.CharField(max_length=100)
    dateAccesed  = models.DateField()
    hourAccessed = models.TimeField()
    ip           = models.GenericIPAddressField()
    shortenedURL = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE)


