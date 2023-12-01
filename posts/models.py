from django.db import models
from django.utils.translation import gettext_lazy as _
class Post(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name='posts')
    parent = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.CASCADE, related_name="thread"
    )
    reply = models.BooleanField(verbose_name=_("Is a reply?"), default=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_images = models.ImageField(upload_to='post_images/', blank=True, null=True)
    category = models.CharField(max_length=500, default=None, null=True, blank=True)

    def __str__(self):
        return self.content
    

    def get_parent(self):
        if self.parent:
            return self.parent

        else:
            return self

    def reply_this(self, user, text):
        """Handler function to create a News instance as a reply to any
        published news.

        :requires:

        :param user: The logged in user who is doing the reply.
        :param content: String with the reply.
        """
        parent = self.get_parent()
        return Post.objects.create(
            user=user, content=text, reply=True, parent=parent
        )

    def get_thread(self):
        
        return Post.objects.filter(parent=self)
        # parent = self.get_parent()
        # return parent.thread.all()


    def count_thread(self):
        return self.get_thread().count()


