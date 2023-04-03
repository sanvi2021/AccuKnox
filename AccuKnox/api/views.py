from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import views
from django.http import HttpResponse
from django.db import connections
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.shortcuts import get_object_or_404
from .models import *
import json
from friendship.models import Friend,FriendshipRequest
from rest_framework.throttling import UserRateThrottle
import time
# Create your views here.

class Searchuser(views.APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        content ={
            'user':str(request.user),    
        }
        return Response({"sucess": True,"message":content})
        
    def post(self,request,format=None):
        data_dict ={}
        data_dict['name']=[]
        if "searching_key" not in request.data:
            return HttpResponse(json.dumps({"success":False,"message":"Missing searching_key in REQUEST"}))
        search_key = request.data["searching_key"]
        search_key = str(search_key)
        cursor = connections['default'].cursor()
        if '@' in search_key: 
            #query to find the user name only if correct email is passed in search field
            query = "select username from auth_user where email like '@search'"
            query = query.replace("@search",search_key)
            cursor.execute(query)
            result =cursor.fetchall()            
        else: 
            #query to find the user name is name of user is searched
            query = "select username from auth_user where username like '@search%'"
            query = query.replace("@search",search_key)
            cursor.execute(query)
            result =cursor.fetchall()
        [data_dict['name'].append(i[0])for i in result]         
        return Response({"success": True,"result": data_dict})
    
class Send_fr_request(views.APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes =[IsAuthenticated]
    throttle_classes = [UserRateThrottle] # if user tries to send more than 3 req in a min, will get message as -> "detail": "Request was throttled. Expected available in 5 seconds."
    def post(self,request,format=None):
        from_user = request.user
        get_user_id = User.objects.filter(email=request.data['user_id']).values('id')
        if len(get_user_id)>0:
            id = get_user_id[0].get('id')
            to_user = User.objects.get(pk=id)
        else:
            return Response({"success":False,"message":"could not get the id for blank list"})
        try:
            result = Friend.objects.add_friend(from_user,to_user,message='Hi! I would like to add you')
            return Response({"success":True, "message":"Friend Request send"})
        except Exception as e:
            return Response({"success":True, "message":str(e)})
    
class Fr_req_approve(views.APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes =[IsAuthenticated]
    def post(self,request,format=None):
        to_usr = User.objects.filter(email=request.data['user_id']).values('id')
        if len(to_usr)>0:
            to_user = to_usr[0].get('id')
            status = request.data['status'] # Assuming that user can either accept or reject the request. '0' for approval and '1'for rejection
            friend_request = FriendshipRequest.objects.get(from_user=request.user, to_user=to_user)
            if status == '0':
                friend_request.accept()
                return Response({"success": True,"message": "Request is accepted"})
            else:
                friend_request.reject()
                return Response({"success": True,"message":"Request is Rejected"})
        else:
            return Response({"success":False,"message": "could get the id for blank list"})

class Fr_list(views.APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes =[IsAuthenticated]
    def post(self,request,format=None):
        #assuming that user will either request to see all pending req or accepted req
        status = request.data['status']
        print(status,'------------------')# '0' if user wants to view all friends list & '1' to view all pending req.
        if status =='0':
            friend_list = Friend.objects.friends(request.user)
            fr_list={}
            fr_list["friend_list"] = []
            for f in friend_list:
                fr_list["friend_list"].append(str(f))
            return Response({"success": True, "message": fr_list})
        else:
            pending_list = Friend.objects.unread_requests(user=request.user)
            pn_list={}
            pn_list["pending_list"] = []
            for p in pending_list:
                pn_list["pending_list"].append(str(p))
            return Response({"success": True, "message": pn_list})
    