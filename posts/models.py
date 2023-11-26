from django.db import models

class Post(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_images = models.ImageField(upload_to='post_images/', blank=True, null=True)
    category = models.CharField(max_length=500, default=None, null=True, blank=True)

    def __str__(self):
        return self.user.username

