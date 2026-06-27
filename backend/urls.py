from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def home(request):
    return render(request, "home.html")


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    path('api/dashboard/', include('dashboard.urls')),
    path('api/accounts/', include('accounts.urls')),
]