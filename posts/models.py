from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from user.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


CHOICES = (
	("text", "text"),
	("video", "video"),
	("audio", "audio"),
	("images", "images")
)

class Post(models.Model):
	user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name='posts')
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	post_media = models.FileField(upload_to='post_media/', blank=True, null=True)
	category = models.CharField(max_length=500, default=None, null=True, blank=True)
	post_type = models.CharField(choices=CHOICES, max_length=50, default="text")


	class Meta:
		verbose_name = "Post"
		verbose_name_plural = "Posts"
		ordering = ["-created_at"]

	def __str__(self):
		return f"Post: {self.category} published by {self.user.username}"

	def is_edited(self):
		return (self.updated_at - self.created_at).total_seconds() > 1
	edited = property(is_edited)


class AbstractComment(models.Model):
	user = models.ForeignKey(
		User, null=True,
		verbose_name='user',
		on_delete=models.CASCADE,
		related_name="%(class)s_comments",
	)
	_comment = models.TextField(max_length=3000)
	is_removed = models.BooleanField(
		default=False,
		help_text='Check this box if the comment is inappropriate. '
			'A "This comment has been removed" message will '
			'be displayed instead.'
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	is_nesting_permitted = models.BooleanField(
		default=False
	)

	class Meta:
		abstract = True
		ordering = ['created_at',]

	def _get_comment(self):
		comment = self._comment
		if self.is_removed:
			comment = "This comment has been removed"
		return comment
	comment = property(_get_comment)

	def is_edited(self):
		return (self.updated_at - self.created_at).total_seconds() > 1
	edited = property(is_edited)

class PostComment(AbstractComment):
	post = models.ForeignKey(
		Post,
		verbose_name='post',
		on_delete=models.CASCADE,
		related_name="comments"
	)

	parent = models.ForeignKey(
		"self", null=True,
		related_name="comments",
		on_delete=models.CASCADE
	)

	class Meta:
		ordering = ['created_at',]
		verbose_name = "Post Comment"
		verbose_name_plural = "Post Comments"

	def __str__(self):
		return f"Comment: {self.post.category} by {self.user.username}"

	






	

  





  
