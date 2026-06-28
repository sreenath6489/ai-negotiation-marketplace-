from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate

from .models import CustomUser
from .serializers import RegisterSerializer,ProfileSerializer


class RegisterView(generics.CreateAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=RegisterSerializer


class LoginView(generics.GenericAPIView):

    def post(self,request):

        username=request.data.get("username")
        password=request.data.get("password")

        user=authenticate(username=username,password=password)

        if user:

            refresh=RefreshToken.for_user(user)

            return Response({

                "refresh":str(refresh),
                "access":str(refresh.access_token),
                "username":user.username

            })

        return Response({"error":"Invalid Credentials"},status=401)


class ProfileView(generics.RetrieveUpdateAPIView):

    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserList(generics.ListAPIView):

    queryset=CustomUser.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]


import urllib.request
import json
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.conf import settings

def verify_google_token(token, client_id):
    # Try using google-auth library if available
    try:
        from google.oauth2 import id_token
        from google.auth.transport import requests as google_requests
        return id_token.verify_oauth2_token(token, google_requests.Request(), client_id)
    except ImportError:
        # Fallback to direct HTTP request to Google API
        try:
            url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
                # Check for error in response
                if 'error_description' in data:
                    raise ValueError(data['error_description'])
                
                # Verify audience (client ID)
                aud = data.get('aud')
                if aud != client_id:
                    raise ValueError("Audience mismatch")
                    
                return data
        except Exception as e:
            raise ValueError(f"Token verification failed: {str(e)}")


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get settings Client ID or fallback to standard placeholder
        client_id = getattr(settings, 'GOOGLE_CLIENT_ID', '793655183858-5c845tf7qgjadbt7q577g1bms95gtd62.apps.googleusercontent.com')

        try:
            idinfo = verify_google_token(token, client_id)

            email = idinfo.get('email')
            name = idinfo.get('name', '')
            picture = idinfo.get('picture', '')

            if not email:
                return Response({'error': 'Email not provided by Google'}, status=status.HTTP_400_BAD_REQUEST)

            # Get or create CustomUser
            username_prefix = email.split('@')[0]
            
            user, created = CustomUser.objects.get_or_create(email=email, defaults={
                'username': username_prefix,
                'first_name': idinfo.get('given_name', ''),
                'last_name': idinfo.get('family_name', ''),
            })

            if created and picture:
                user.bio = f"Google User: {name}"
                user.save()

            # Generate SimpleJWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email,
                'is_new': created
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'error': 'Invalid token: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Authentication failed: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)