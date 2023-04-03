
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('search/',Searchuser.as_view(),name="search"),
    path('send_request/',Send_fr_request.as_view(),name='send request'),
    path('frstatus/',Fr_req_approve.as_view(),name="Friend status"),
    path('frlist/',Fr_list.as_view(),name="friend list"),
    path('friendship/', include('friendship.urls')),
    
    
]
