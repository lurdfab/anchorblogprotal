from rest_framework import routers
from user.api import *
from posts.api import *
from comment_reply.api import *


router = routers.DefaultRouter(trailing_slash=True)


#user
router.register(r"register", RegisterViewSet, basename="register")
router.register(r"login", LoginViewSet, basename="login")
router.register(r"userprofile", UserProfileViewSet, basename="userprofile")
router.register(r"user", UserViewSet, basename="user")

#posts
router.register(r"posts", PostViewset, basename="posts")
#comments_reply
router.register(r"comments", CommentViewset, basename="comments")
router.register(r'replies', ReplyViewSet)


