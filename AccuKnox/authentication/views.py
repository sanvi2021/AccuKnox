from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class Signup(APIView):
    permission_classes = [AllowAny]
    def post(self,request,format=None):
        print(request.data['email'],'------------tracking mail id-------')
        if 'email' not in request.data:
            return Response({"success":False,"message":"Missing email in REQUEST"})
        email = request.data['email']
        check_usr = User.objects.filter(email=email)
        print(type(check_usr))
        if len(check_usr)> 0:
            return Response({"success": False, "message":"User already Exists!"})  
        else:
            user = User.objects.create(email=email,username=email)
            return Response({"success": True, "message":"user created"})
#without any authentication permission
class Login(APIView):    
    permission_classes = [AllowAny]
    def post(self,request,format=None):
        print(request.data['email'],'---------checking username data')
        username = request.data['email']
        password = request.data['password']
        try:
            usr = User.objects.filter(email=username).values()
            if len(usr)>0:
                print(usr,'----------email')
                return Response({"success": True, "message": "user logged in"})
            else:
                return Response({"success": False, "message": "user doesn't exist"})
        except Exception as e:
            print(e)
        return Response({"success": False, "message": "invalid request"})

