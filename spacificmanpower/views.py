from django.shortcuts import render
from .serializers import *
from .models import *
from django.contrib.auth.models import User, Group
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from django.http import Http404
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]


class usertype(APIView):
     # Return a list of all userreg objects serialized using userregSerializer

    queryset = user_type.objects.all()
    serializer_class = user_type_serializer

    def get(self, request, format=None):
        staffs = user_type.objects.all().order_by('-createdDate')
        serializer = user_type_serializer(staffs, many=True, context={'request': request})
        return Response(serializer.data)
    
class useraccount(APIView):
     # Return a list of all userreg objects serialized using userregSerializer

    queryset = user_type.objects.all()
    serializer_class = user_type_serializer

    def get(self, request, format=None):
        staffs = user_type.objects.all().order_by('-createdDate')
        serializer = user_type_serializer(staffs, many=True, context={'request': request})
        return Response(serializer.data)
    

