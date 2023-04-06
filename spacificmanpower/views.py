import datetime
from django.shortcuts import render
from .serializers import *
from .models import *
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
        company_name = request.data.get('company_name')
        profile_description = request.data.get('profile_description')
        business_stream_id = request.data.get('business_stream_id')

        establishment_date = request.data.get('establishment_date')
        company_website_url = request.data.get('company_website_url')

        business_stream_id = business_stream.objects.get(id=business_stream_id)

        company_data = company(company_name=company_name, profile_description=profile_description, business_stream_id=business_stream_id, 
                              establishment_date=establishment_date,company_website_url=company_website_url)
        company_data.save() 

        company_id = company_data.id
        company_id_instance = company.objects.get(id=company_id)
        company_image_data = request.data.get('company_image')

        company_image_instance = company_image(company_id=company_id_instance, company_image=company_image_data)
        company_image_instance.save()

        return Response(status=status.HTTP_201_CREATED)

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
        # Extract data from request.data
        street_address = request.data.get('street_address')
        city = request.data.get('city')
        state = request.data.get('state')
        country = request.data.get('country')
        zip = request.data.get('zip')
        jobtypeid=request.data.get('job_type_id')
        companyid=request.data.get('company_id')
        useraccountid=request.data.get('user_account_id')
        

        joblocation = job_location(street_address=street_address, city=city, state=state, country=country,zip=zip)
        joblocation.save()

        job_type_id = job_type.objects.get(id=jobtypeid)
        company_id = company.objects.get(id=companyid)
        user_account_id=user_account.objects.get(id=useraccountid)
        is_company_name_hidden = request.data.get('is_company_name_hidden')
        job_description = request.data.get('job_description')
        job_location_id = joblocation.id
        created_date=request.data.get('created_date')
        is_active = request.data.get('is_active')

        job_location_instance = job_location.objects.get(id=job_location_id)

        jobpost=job_post(job_type_id=job_type_id,company_id=company_id,is_company_name_hidden=is_company_name_hidden,
                         job_description=job_description,job_location_id=job_location_instance,created_date=created_date,is_active=is_active)
        jobpost.save()

        skill_level=request.data.get('skill_level')
        skill_set_id=request.data.get('skill_set_id')
        job_post_id=jobpost.id
        job_post_instance = job_post.objects.get(id=job_post_id)
        
        jobpostskillset=job_post_skill_set(skill_set_id=skill_set_id,skill_level=skill_level,job_post_id=job_post_instance)
        jobpostskillset.save()

        jobpostactivity=job_post_activity(user_account_id=user_account_id,job_post_id=job_post_instance)
        jobpostactivity.save()

        user_log_instance = user_log.objects.get(user_account_id=user_account_id)
        user_log_instance.last_job_apply_date = datetime.datetime.now()
        user_log_instance.save()
        
        return Response(status=status.HTTP_201_CREATED)

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
    
class seekerskillset(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = seeker_skill_set.objects.all()
    serializer_class = seeker_skill_set_serializer

    def get(self, request, format=None):
        user_data = seeker_skill_set.objects.all().order_by('-createdDate')
        serializer = seeker_skill_set_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
class jobpostactivity(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = job_post_activity.objects.all()
    serializer_class = job_post_activity_serializer

    def get(self, request, format=None):
        user_data = job_post_activity.objects.all().order_by('-createdDate')
        serializer = job_post_activity_serializer(user_data, many=True, context={'request': request})
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
        useraccountid=request.data.get('user_account_id')

        user_account_id=user_account.objects.get(id=useraccountid)

        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        current_salary = request.data.get('current_salary')
        is_annually_monthly = request.data.get('is_annually_monthly')
        currency = request.data.get('currency')

        seekerprofile=seeker_profile(user_account_id=user_account_id,first_name=first_name,last_name=last_name,
                         current_salary=current_salary,is_annually_monthly=is_annually_monthly,currency=currency)
        seekerprofile.save()

        useraccountid=request.data.get('user_account_id')
        
        user_account_id=user_account.objects.get(id=useraccountid)
        certificate_degree_name = request.data.get('certificate_degree_name')
        major = request.data.get('major')
        institute_university_name = request.data.get('institute_university_name')
        starting_date = request.data.get('starting_date')
        completion_date = request.data.get('completion_date')
        percentage = request.data.get('percentage')
        cgpa = request.data.get('cgpa')

        educationdetail=education_detail(user_account_id=user_account_id,certificate_degree_name=certificate_degree_name,major=major,
                         institute_university_name=institute_university_name,starting_date=starting_date,completion_date=completion_date,percentage=percentage,cgpa=cgpa)
        educationdetail.save()

        useraccountid=request.data.get('user_account_id')
        
        user_account_id=user_account.objects.get(id=useraccountid)
        is_current_job = request.data.get('is_current_job')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        job_title = request.data.get('job_title')
        company_name = request.data.get('company_name')
        job_location_city = request.data.get('job_location_city')
        job_location_state = request.data.get('job_location_state')
        job_location_country = request.data.get('job_location_country')
        description = request.data.get('description')

        experincedetail=experience_detail(user_account_id=user_account_id,is_current_job=is_current_job,start_date=start_date,
                         end_date=end_date,job_title=job_title,company_name=company_name,job_location_city=job_location_city,job_location_state=job_location_state,job_location_country=job_location_country,description=description)
        experincedetail.save()

        useraccountid=request.data.get('user_account_id')
        skillsetid=request.data.get('skill_set_name')
        
        user_account_id=user_account.objects.get(id=useraccountid)
        # try:
        #     skill_set_id = skill_set.objects.get(id=skillsetid)
        # except skill_set.DoesNotExist:
        #     skill_set_id = None

        skill_set_id = skill_set.objects.get(id=skillsetid)
        skill_level = request.data.get('skill_level')

        seekerskillset=seeker_skill_set(user_account_id=user_account_id,skill_set_id=skill_set_id,skill_level=skill_level)
        seekerskillset.save()

        return Response(status=status.HTTP_201_CREATED)
    
class trendingnews(APIView):
    # Return a list of all userreg objects serialized using userregSerializer

    queryset = trending_news.objects.all()
    serializer_class = trending_news_serializer

    def get(self, request, format=None):
        user_data = trending_news.objects.all().order_by('-createdDate')
        serializer = trending_news_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):

        user_account_id=request.data.get('user_account_id')
        news_title = request.data.get('news_title')
        news_description = request.data.get('news_description')
        news_image = request.data.get('news_image')

        trending_news=trending_news(user_account_id=user_account_id,news_title=news_title,news_description=news_description,
                         news_image=news_image)
        trending_news.save()

class updatenews(APIView):
    def get_object(self, pk):
        try:
            return trending_news.objects.get(pk=pk)
        except trending_news.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = trending_news_serializer(data)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        userObject = trending_news.objects.get(pk=request.data['id'])
        addmoreUser = self.get_object(pk)
        serializer = trending_news_serializer(addmoreUser, data=request.data)
        if serializer.is_valid():
            serializer.save(staff=userObject)
            return Response(serializer.data)
        
    def delete(self, request, pk, format=None):
        data = self.get_object(pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)