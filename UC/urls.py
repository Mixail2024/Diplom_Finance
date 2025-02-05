
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('users/', include('users.urls')),
    path("finance/", include('finance.urls')),
    path("login/", auth_views.LoginView.as_view(), name="login"),
]
