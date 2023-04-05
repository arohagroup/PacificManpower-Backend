import datetime
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

        user_type_id = request.data.get('user_type_id')
        if user_type_id:
            userObject = user_type.objects.get(pk=user_type_id)
            request.data['isactive'] = True
        serializer = user_account_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user_type_id=userObject)
            user_id = user_account.objects.last()
            userlogObject = user_account.objects.get(pk=user_id.id)
            log_Data={
                'last_login_date':datetime.datetime.now()
            }
            logserializer = user_log_serializer(data=log_Data)
            if logserializer.is_valid():
                logserializer.save(user_account_id=userlogObject)
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
        
class userlog(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = user_log.objects.all()
    serializer_class = user_log_serializer

    def get(self, request, format=None):
        user_data = user_log.objects.all().order_by('-createdDate')
        serializer = user_log_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
class userlogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = user_account.objects.get(email=email)
            user_logData = user_log.objects.last()
        except user_account.DoesNotExist:
            # User does not exist
            return Response({"message": "User account doesn't exists"}, status=status.HTTP_404_NOT_FOUND)

        # Check the password
        if user.password == password:
            # Passwords match, user is authenticated
            user_logData.last_login_date = datetime.datetime.now()
            user_logData.save()

            return Response({"message": "User authenticated"}, status=status.HTTP_200_OK)
        else:
            # Passwords do not match
            return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
class forgotpassword(APIView):
    def post(self, request, *args, **kwargs):
        my_model_instance = user_account.objects.get(id=request.data['id'])
        my_model_instance.password = request.data['password']
        my_model_instance.save(update_fields=['password'])
        return Response({'success': True})
    
class businessstream(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = business_stream.objects.all()
    serializer_class = business_stream_serializer

    def get(self, request, format=None):
        user_data = business_stream.objects.all().order_by('-createdDate')
        serializer = business_stream_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = business_stream_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class companyadddetails(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = company.objects.all()
    serializer_class = company_serializer

    def get(self, request, format=None):
        user_data = company.objects.all().order_by('-createdDate')
        serializer = company_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):

        if 'business_stream_id' in request.data:
          
            business_streamObject = business_stream.objects.get(pk=request.data['business_stream_id'])
        else:
            
            business_streamObject = None

        serializer = company_serializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save(business_stream_id=business_streamObject)
            user_id = company.objects.last()
            userlogObject = company.objects.get(pk=user_id.id)
            
            log_Data={
                # 'company_id':user_id,
                'company_image':request.data['company_image']
            }

            
            logserializer = company_image_serializer(data=log_Data)

            if logserializer.is_valid():
                print("EXCUTED")
                logserializer.save(company_id=userlogObject)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class companyprofile(APIView):
    def get_object(self, pk):
        try:
            return company.objects.get(pk=pk)
        except company.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = company_serializer(data)
        return Response(serializer.data)
    
class companysaveimage(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = company_image.objects.all()
    serializer_class = company_image_serializer

    def get(self, request, format=None):
        user_data = company_image.objects.all().order_by('-createdDate')
        serializer = company_image_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
class postjob(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = job_post.objects.all()
    serializer_class = job_post_serializer

    def get(self, request, format=None):
        user_data = job_post.objects.all().order_by('-createdDate')
        serializer = job_post_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = job_post_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class editjob(APIView):
    def get_object(self, pk):
        try:
            return job_post.objects.get(pk=pk)
        except job_post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = job_post_serializer(data)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        userObject = job_post.objects.get(pk=request.data['id'])
        addmoreUser = self.get_object(pk)
        serializer = job_post_serializer(addmoreUser, data=request.data)
        if serializer.is_valid():
            serializer.save(staff=userObject)
            return Response(serializer.data)
        
    
class joblocation(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = job_location.objects.all()
    serializer_class = job_location_serializer

    def get(self, request, format=None):
        user_data = job_location.objects.all().order_by('-createdDate')
        serializer = job_location_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = job_location_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class educationdetail(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = education_detail.objects.all()
    serializer_class = education_detail_serializer

    def get(self, request, format=None):
        user_data = education_detail.objects.all().order_by('-createdDate')
        serializer = education_detail_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
class experincedetail(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = experience_detail.objects.all()
    serializer_class = experience_detail_serializer

    def get(self, request, format=None):
        user_data = experience_detail.objects.all().order_by('-createdDate')
        serializer = experience_detail_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
class skills(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = skill_set.objects.all()
    serializer_class = skill_set_serializer

    def get(self, request, format=None):
        user_data = skill_set.objects.all().order_by('-createdDate')
        serializer = skill_set_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
class skillset(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = job_post_skill_set.objects.all()
    serializer_class = job_post_skill_set_serializer

    def get(self, request, format=None):
        user_data = job_post_skill_set.objects.all().order_by('-createdDate')
        serializer = job_post_skill_set_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
class jobtype(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = job_type.objects.all()
    serializer_class = job_type_serializer

    def get(self, request, format=None):
        user_data = job_type.objects.all().order_by('-createdDate')
        serializer = job_type_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
class seekerprofile(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = seeker_profile.objects.all()
    serializer_class = seeker_profile_serializer

    def get(self, request, format=None):
        user_data = seeker_profile.objects.all().order_by('-createdDate')
        serializer = seeker_profile_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)

    
    def post(self, request, format=None):
        if 'user_account_id' in request.data:
            business_streamObject = seeker_profile.objects.get(pk=request.data['user_account_id'])
        else:
            
            business_streamObject = None

        serializer = seeker_profile_serializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save(user_account_id=business_streamObject)
            # user_id = company.objects.last()
            # userlogObject = company.objects.get(pk=user_id.id)
            
            # log_Data={
            #     # 'company_id':user_id,
            #     'company_image':request.data['company_image']
            # }

            
            # logserializer = company_image_serializer(data=log_Data)

            # if logserializer.is_valid():
            #     print("EXCUTED")
            #     logserializer.save(company_id=userlogObject)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






