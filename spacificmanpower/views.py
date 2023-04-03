from django.shortcuts import render
from .serializers import *
from .models import *
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from django.http import Http404
from django.contrib.auth.hashers import check_password
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class usertype(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = user_type.objects.all()
    serializer_class = user_type_serializer

    def get(self, request, format=None):
        data = user_type.objects.all().order_by('-createdDate')
        serializer = user_type_serializer(data, many=True, context={'request': request})
        return Response(serializer.data)
    
class usersaveaccount(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = user_account.objects.all()
    serializer_class = user_account_serializer

    def get(self, request, format=None):
        user_data = user_account.objects.all().order_by('-createdDate')
        serializer = user_account_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        userObject = user_type.objects.get(pk=request.data['user_type_id'])
        serializer = user_account_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type_id=userObject)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class edituseraccount(APIView):
    def get_object(self, pk):
        try:
            return user_account.objects.get(pk=pk)
        except user_account.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = user_account_serializer(data)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        userObject = user_account.objects.get(pk=request.data['id'])
        addmoreUser = self.get_object(pk)
        serializer = user_account_serializer(addmoreUser, data=request.data)
        if serializer.is_valid():
            serializer.save(staff=userObject)
            return Response(serializer.data)
        
class userlogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = user_account.objects.get(email=email)
        except user_account.DoesNotExist:
            # User does not exist
            return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check the password
        if user.password == password:
            # Passwords match, user is authenticated
            return Response({"message": "User authenticated"}, status=status.HTTP_200_OK)
        else:
            # Passwords do not match
            return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    
        # try:
        #     user = user_account.objects.get(email=email)
        #     if check_password(password, user.password):
        #         return Response({'success': True, 'data': 'Logged in successfully'})
        #     else:
        #         return Response({'success': False, 'data': 'Incorrect password'})
        # except user_account.DoesNotExist:
        #     return Response({'success': False, 'data': 'User not found'})

        

class forgotpassword(APIView):
    def post(self, request, *args, **kwargs):
        my_model_instance = user_account.objects.get(id=request.data['id'])
        my_model_instance.password = request.data['password']
        my_model_instance.save(update_fields=['password'])
        return Response({'success': True})
