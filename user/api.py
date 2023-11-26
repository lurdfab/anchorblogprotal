from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework  import status, permissions
from rest_framework.request import Request
from django.contrib.auth import authenticate
from rest_framework import viewsets, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from rest_framework.decorators import action
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.permissions import AllowAny
from likes.mixins import *

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
   

    def post(self, request:Request):  
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response = {
                "message":"user created successfully",
                "data":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST )

   
class LoginViewSet(viewsets.ModelViewSet):
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    authentication_class = [TokenAuthentication]

    
    def post(self, request:Request): 
        username= request.data.get('username')
        password = request.data.get('password')

        user=authenticate(username=username, password=password)

        if user is not None:

            token = Token.objects.create(user=user)
            response = {
                "message": "Login was successful",
                "tokens": token
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "invalid username and password"})

    def get(self, request:Request): 
        content = {
            "user":str(request.user),
            "auth":str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK )
    
class LogoutViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]  #Use the appropriate authentication method
  

    def post(self, request):
        # When a user logs out, you can simply delete their token (or perform other necessary actions).
        request.auth.delete()  # Delete the token
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(LikedResourceMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_class = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_permissions(self):

        if self.action == "password_recovery":
            self.permission_class = (AllowAny,)

        if self.action == "change_password_from_recovery":
            self.permission_class = (AllowAny,)

        return super().get_permissions()

    
    def get_serializer(self, *args, **kwargs):
        
        if self.action == "password_recovery":
            self.serializer_class = EmailSerializer

        if self.action == "change_password_from_recovery":
            self.serializer_class = RecoverySerializer
        
        return super().get_serializer(*args, **kwargs)


    @action(detail=False, methods=['POST'])
    def password_recovery(self, request, pk=None):
        email = request.data.get('email', None)

        if not email:
            raise exceptions.ValidationError(_("Invalid email"))

        user = get_object_or_404(User, email=email)
        user.token = str(uuid.uuid4())
        user.save(update_fields=["token"])

     
        email_content = render_to_string('password_reset_email.html', {"token":user.token})
        send_mail(
            subject= "Password Reset",
            message= "Password reset",  
            from_email='your_email@example.com',
            recipient_list= [email,],
            html_message=email_content,  
        )
        

        return Response({"detail": _("Mail sent successfully!")}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def change_password_from_recovery(self, request, pk=None):
        """
        Change password with token (from password recovery step).
        """
        serializer = RecoverySerializer(data=request.data, many=False)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(token=serializer.data["token"])
        except User.DoesNotExist:
            raise exceptions.ValidationError(_("Token is invalid"))

        user.set_password(serializer.data["password"])
        user.token = None
        user.save(update_fields=["password", "token"])

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_class = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



            

        

    
    