from django.db import models
from django.contrib.auth.models  import User

# Create your models here.
class Favourite(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    track_id = models.CharField(max_length=500,null=True, blank=True)
    track_name = models.CharField(max_length=500, null= True, blank= True)
   
    def __str__(self):
        return f"{self.track_id} X {self.track_name}"

    # class META:
    #     ordering = ["song"]


# class Album(models.Model):
#     name = models.CharField(max_length=400,null=True, blank=True)