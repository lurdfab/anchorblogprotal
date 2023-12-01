from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    category = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='videos/')
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name='video')
    upload_date = models.DateTimeField(auto_now_add=True)

class Music(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    category = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='music/')
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name='music')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title