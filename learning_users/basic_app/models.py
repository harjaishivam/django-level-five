from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #additional parameters
    portfolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    # profile_pics should be a subdirectory in the media folder.
    # for images, pillow is installed by default in Django.

    def __str__(self):
        return self.user.username
