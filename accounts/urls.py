from django.urls import path
from .views import RegisterView, LoginView, ProfileView, UserList, GoogleLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users/', UserList.as_view(), name='users'),
    path('google/', GoogleLoginView.as_view(), name='google-login'),
]
