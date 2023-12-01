from django.db import models

class Comment(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name='comments')
    video = models.ForeignKey("blog.Video", on_delete=models.CASCADE, null=True, blank=True,  related_name='comments')
    music = models.ForeignKey("blog.Music", on_delete=models.CASCADE, null=True, blank=True,  related_name='comments')
    comment = models.CharField(max_length=1000)
    commented_at = models.DateTimeField(auto_now_add=True) 
    comment_image = models.ImageField(upload_to='comment_images/', blank=True, null=True)

    def __str__(self):
        return self.comment
    

class Reply(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    reply = models.CharField(max_length=1000)
    reply_image = models.ImageField(upload_to='reply_images/', blank=True, null=True)

    def __str__(self):
        return self.reply