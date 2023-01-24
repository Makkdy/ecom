from django.shortcuts import render
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from django.http import JsonResponse
from .serializers import CustomUserSerializer
from .models import CustomUser
import random 
import re

# Create your views here.

def generate_session_tokken(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97,123)]+[str(i) for i in range(10)]) for _ in range(length))

@csrf_exempt
def signin(request):
    #checkin if request is post, else return error
    if request.method != 'POST':
        return JsonResponse({'error':'send post request with valid parameter'})

    # fetch and user and password from the rquest to perform authentication
    # below methode describe that this function accept HTML form data
    username = request.POST['username']
    password = request.POST['password']

    #perform validation on username and password

    #regular expression gapped by regexr.com website
    pattern = "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"

    if not re.match(pattern, username):
        return JsonResponse({'error':'Not a valid email'})

    if len(password) < 3:
        return JsonResponse({'error':'password length is too less'})
    
    #Authenticate the user 

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)
        if user.check_password(password):
            usr_dict = UserModel.objects.filter(email=username).values().first()
            #removing password we don't want it to show anywhere(special frontend)
            usr_dict.pop('password')
            # setting new session at every login 
            if user.session_token != '0':
                user.session_token = '0'
                user.save()
                return JsonResponse({'error':'previous session exist'})
            token  = generate_session_tokken()
            user.session_token = token
            user.save()
            # before going on to login first need to be authenticated
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return JsonResponse({'token': user.session_token, 'user': usr_dict})
        #through password invalid errror
        else:
            return JsonResponse({'error':'Credential'})
    # throughing username not exist error
    except UserModel.DoesNotExist:
        return JsonResponse({'error':'Credential'})


def signout(request, id):
    
    #grabbing UserModel
    UserModel = get_user_model()

    try:
        #update user session to none
        user = UserModel.objects.get(pk=id)
        user.session_token = '0'
        user.save()
        #logout doesn't matter its position only need 1 argument request
        logout(request)
        #  return the sucess message
        return JsonResponse({'success':'Logout success'})
    except UserModel.DoesNotExist:
        return JsonResponse({"error":'Not valid Credentials'})

class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}

    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


