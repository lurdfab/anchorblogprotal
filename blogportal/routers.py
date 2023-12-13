from rest_framework import routers
from user.api import *
from posts.api import *



router = routers.DefaultRouter(trailing_slash=True)


#user
router.register(r"register", RegisterViewSet, basename="register")
router.register(r"login", LoginViewSet, basename="login")
router.register(r"userprofile", UserProfileViewSet, basename="userprofile")
router.register(r"user", UserViewSet, basename="user")
#posts
router.register(r"posts", PostViewset, basename="posts")
router.register(r"posts/(?P<post_id>\d+)/postcomments", PostCommentViewSet, basename="postcomments")





