from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class URLUser(AbstractUser):
    def __str__(self):
        return self.username
    
class ShortenedURL(models.Model):
    original    = models.URLField(unique=True)
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

    @classmethod
    def create(cls, navigator, ip, shortenedURL):

        from datetime import datetime

        currentDateAndTime = datetime.now()
        currentDate = currentDateAndTime.strftime("%Y-%m-%d")
        currentTime = currentDateAndTime.strftime("%H:%M:%S")

        anAccess = cls(navigator=navigator, ip=ip, shortenedURL=shortenedURL)
        anAccess.dateAccesed = currentDate
        anAccess.hourAccessed = currentTime
        return anAccess

