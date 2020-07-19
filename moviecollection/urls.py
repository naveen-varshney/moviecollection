"""moviecollection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from colsapp.views import home_page, request_count, reset_request_count, UserCreate

urlpatterns = [
    path("", home_page),
    path("admin/", admin.site.urls),
    path("api/v1/", include("colsapp.urls")),
    # for request count
    path("request-count/", request_count),
    path("request-count/reset/", reset_request_count),
    # for user registration and login
    path("login/", obtain_auth_token),
    path("register/", UserCreate.as_view()),
]
