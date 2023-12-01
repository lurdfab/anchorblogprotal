from rest_framework import routers
from user.api import *
from posts.api import *
from comment_reply.api import *
from blog.api import *


router = routers.DefaultRouter(trailing_slash=True)


#user
router.register(r"register", RegisterViewSet, basename="register")
router.register(r"login", LoginViewSet, basename="login")
router.register(r"userprofile", UserProfileViewSet, basename="userprofile")
router.register(r"user", UserViewSet, basename="user")
#posts
router.register(r"posts", PostViewset, basename="posts")
router.register(r"posts/(?P<id>\d+)/replies", PostReplyViewset, basename="posts")
#comments_reply
router.register(r"comments", CommentViewset, basename="comments")
router.register(r'replies', ReplyViewSet, basename="replies")
router.register(r"musiccomments", MusicCommentViewset, basename="musiccomments")
router.register(r"musicreplies", MusicReplyViewSet, basename="musicreplies")
#videos and music
router.register(r"video", VideoViewset, basename="video")
router.register(r"music", MusicViewset, basename="music")



