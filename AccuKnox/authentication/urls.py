
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',Signup.as_view(),name="signup"),
    path('login/',Login.as_view(),name="login"),
    
]
