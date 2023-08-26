import datetime
from .serializers import *
from .models import *
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from rest_framework import status,viewsets
from django.http import Http404
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from ast import literal_eval
import json
import ast
import tempfile
from django.db.models import Q
from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import get_object_or_404
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from django.http import JsonResponse
from datetime import datetime
from django.forms.models import model_to_dict
from django.http import QueryDict
from django.utils import timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
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

    queryset = user_type.objects.all()
    serializer_class = user_type_serializer

    def get(self, request, format=None):
        data = user_type.objects.all().order_by('-createdDate')
        serializer = user_type_serializer(data, many=True, context={'request': request})
        return Response(serializer.data)
    
class usersaveaccount(APIView):

    queryset = user_account.objects.all()
    serializer_class = user_account_serializer

    def get(self, request, format=None):
        user_data = user_account.objects.all().order_by('-createdDate')
        serializer = user_account_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):

        email_address = request.data.get('email_address')
        if user_account.objects.filter(email_address=email_address).exists():
            return Response({"message": "Email address already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user_type_id = request.data.get('user_type_id')

        user_image = request.FILES.get('user_image')
        if user_image:
            valid_extensions = ['.jpg', '.jpeg', '.png']
            ext = os.path.splitext(user_image.name)[1]
            if not ext.lower() in valid_extensions:
                return Response({"message": "Invalid file type. Only image files with extensions {} are allowed".format(', '.join(valid_extensions))}, status=status.HTTP_403_FORBIDDEN)
            
        if user_type_id:
            userObject = user_type.objects.get(pk=user_type_id)
            request.data['isactive'] = True
        serializer = user_account_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user_type_id=userObject)
            user_id = user_account.objects.last()
            userlogObject = user_account.objects.get(pk=user_id.id)
            log_Data={
                'last_login_date':datetime.now()
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
        try:
            dataGot = user_account.objects.get(pk=pk)
        except user_account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        dataGot.first_name = request.data.get('first_name')
        dataGot.last_name = request.data.get('last_name')  
        dataGot.email_address = request.data.get('email_address')   
        dataGot.password = request.data.get('password')
        dataGot.date_of_birth=request.data.get('date_of_birth')
        dataGot.gender = request.data.get('gender')
        dataGot.contact_number = request.data.get('contact_number')
        dataGot.user_image=request.data.get('user_image')

        dataGot.save()
        serializer=user_account_serializer(dataGot)
        return Response(serializer.data,status=status.HTTP_200_OK)
                
class userlog(APIView):

    queryset = user_log.objects.all()
    serializer_class = user_log_serializer

    def get(self, request, format=None):
        user_data = user_log.objects.all().order_by('-createdDate')
        serializer = user_log_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
class userlogin(APIView):
    def post(self, request):
        email = request.data.get('email_address')
        password = request.data.get('password')

        try:
            user = user_account.objects.get(email_address=email)
            user_logData = user_log.objects.last()
        except user_account.DoesNotExist:
            
            return Response({"message": "User account doesn't exists"}, status=status.HTTP_404_NOT_FOUND)

        if user.password == password:
            
            user_logData.last_login_date = datetime.now()
            user_logData.save()
            unique_id = get_random_string(length=32)
            return Response({"userid": user.id,"user_type_id": user.user_type_id.id,"username":user.first_name,"token": unique_id},status=status.HTTP_200_OK)
        else:
            
            return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
       
class forgotpassword(APIView):
    def post(self, request, *args, **kwargs):
        my_model_instance = user_account.objects.get(id=request.data['id'])
        my_model_instance.password = request.data['password']
        my_model_instance.save(update_fields=['password'])
        return Response({'success': True})
    
class businessstream(APIView):

    queryset = business_stream.objects.all()
    serializer_class = business_stream_serializer

    def get(self, request, format=None):
        user_data = business_stream.objects.all().order_by('-createdDate')
        serializer = business_stream_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        business_stream_name=request.data.get('business_stream_name','').lower()

        if business_stream.objects.filter(business_stream_name__iexact=business_stream_name).exists():
            return JsonResponse({'error': 'Record already exists in business_stream table.'}, status=status.HTTP_400_BAD_REQUEST)
        
        business_stream_name=request.data.get('business_stream_name')
        user_account_id = request.data.get('user_account_id')
        user_account_id = user_account.objects.get(id=user_account_id)

        skillset = business_stream(business_stream_name=business_stream_name, user_account_id=user_account_id)
        skillset.save() 

        serializer=business_stream_serializer(skillset)
        return Response(serializer.data,status=status.HTTP_200_OK)
        # else:
        #     serializer = business_stream_serializer(data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class companyadddetails(APIView):

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
        user_account_id = request.data.get('user_account_id')
        establishment_date = request.data.get('establishment_date')
        company_website_url = request.data.get('company_website_url')
        companyimage = request.data.get('companyimage')
        company_location = request.data.get('company_location')
        company_size = request.data.get('company_size')
        business_stream_id = business_stream.objects.get(id=business_stream_id)
        user_account_id = user_account.objects.get(id=user_account_id)

        company_data = company(company_name=company_name, profile_description=profile_description, business_stream_id=business_stream_id, 
                              user_account_id=user_account_id,establishment_date=establishment_date,company_size=company_size,
                              company_website_url=company_website_url,company_location=company_location,companyimage=companyimage)
        company_data.save() 

        # company_id = company_data.id
        # company_id_instance = company.objects.get(id=company_id)
        # company_image_data = request.data.get('companyimage')

        # company_image_instance = company_image(company_id=company_id_instance, companyimage=company_image_data)
        # company_image_instance.save()

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

    # def put(self, request, pk, format=None):
    #     dataGot = self.get_object(pk)
    #     serializer = company_serializer(dataGot, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        try:
            companydetails = company.objects.get(pk=pk)
        except company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        companydetails.business_stream_id = business_stream.objects.get(id=request.data.get('business_stream_id'))
        companydetails.user_account_id = user_account.objects.get(id=request.data.get('user_account_id'))
        companydetails.company_name = request.data.get('company_name')
        companydetails.profile_description = request.data.get('profile_description')
        companydetails.establishment_date = request.data.get('establishment_date')
        # companydetails.companyimage = request.data.get('companyimage')
        companydetails.company_location = request.data.get('company_location')
        companydetails.company_size = request.data.get('company_size')
        companydetails.company_website_url = request.data.get('company_website_url')

        if 'companyimage' in request.data:
            companydetails.companyimage = request.data.get('companyimage')

        companydetails.save()

        return Response(status=status.HTTP_200_OK)
    

    def delete(self, request, pk, format=None):
        try:
            company_obj = company.objects.get(pk=pk)
        except company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Delete company image, if applicable
        # company_image_obj = company_image.objects.filter(company_id=company_obj.id).first()
        # if company_image_obj:
        #     company_image_obj.delete()

        # Delete company object
        company_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class postjoblocation(APIView):
    def get_object(self, pk):
        try:
            return job_location.objects.get(pk=pk)
        except job_location.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = job_location_serializer(data)
        return Response(serializer.data)

class postjobcompany(APIView):
    def get_object(self, pk):
        try:
            return company.objects.get(pk=pk)
        except company.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = company_serializer(data)
        return Response(serializer.data)
    
class postjobjobype(APIView):
    def get_object(self, pk):
        try:
            return job_type.objects.get(pk=pk)
        except job_type.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = job_type_serializer(data)
        return Response(serializer.data)
    
# class companysaveimage(APIView):
#     # Return a list of all userreg objects serialized using userregSerializer

#     queryset = company_image.objects.all()
#     serializer_class = company_image_serializer

#     def get(self, request, format=None):
#         user_data = company_image.objects.all().order_by('-createdDate')
#         serializer = company_image_serializer(user_data, many=True, context={'request': request})
#         return Response(serializer.data)
    
class postjob(APIView):

    queryset = job_post.objects.all()
    serializer_class = job_post_serializer

    def get(self, request, format=None):
        user_data = job_post.objects.all().order_by('-createdDate')
        serializer = job_post_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):

        street_address = request.data.get('street_address','')
        city = request.data.get('city','')
        state = request.data.get('state','')
        country = request.data.get('country','')
        zip = request.data.get('zip','')
        jobtypeid=request.data.get('job_type_id','')
        companyid=request.data.get('company_id','')
        useraccountid=request.data.get('user_account_id')
        job_title=request.data.get('job_title','')
        salary=request.data.get('salary',0)

        joblocation = job_location(street_address=street_address, city=city, state=state, country=country,zip=zip)
        joblocation.save()

        job_type_id = job_type.objects.get(id=jobtypeid)

        if companyid:
            try:
                company_id = company.objects.get(id=companyid)
            except company.DoesNotExist:
                return Response({"message": "Invalid company ID"}, status=400)
        else:
            company_id = None
            
        user_account_id=user_account.objects.get(id=useraccountid)
        is_company_name_hidden = request.data.get('is_company_name_hidden',False)
        job_description = request.data.get('job_description')
        job_qualification = request.data.get('job_qualification',[])
        job_location_id = joblocation.id
        created_date=request.data.get('created_date')
        is_active = request.data.get('is_active',True)
        experincetypeid = request.data.get('experince_type_id','')
        experince_type_id = experince_type.objects.get(id=experincetypeid)
        job_location_instance = job_location.objects.get(id=job_location_id)

        # try:
        #     job_qualification_list = json.dumps(job_qualification)
        # except json.JSONDecodeError:
        #     job_qualification_list = []

        job_qualifications_with_ids = [{'id': idx, 'value': qual['value']} for idx, qual in enumerate(job_qualification, start=1)]


        jobpost=job_post(job_type_id=job_type_id,company_id=company_id,is_company_name_hidden=is_company_name_hidden,job_title=job_title,
                         job_description=job_description,job_qualification=job_qualifications_with_ids,job_location_id=job_location_instance,created_date=created_date,is_active=is_active,
                         experince_type_id=experince_type_id,salary=salary,user_account_id=user_account_id)
        
        jobpost.save()

        skillsetids = request.data.get('skill_set_id','').split(',') 
        
        for skillsetid in skillsetids:
            try:
                skill_set_id = skill_set.objects.get(id=int(skillsetid))
                skill_level = request.data.get('skill_level',0)
                job_post_id=jobpost.id
                job_post_instance = job_post.objects.get(id=job_post_id)
                seekerskillset = job_post_skill_set( skill_set_id=skill_set_id, skill_level=skill_level,job_post_id=job_post_instance)
                seekerskillset.save() 
            except skill_set.DoesNotExist:
                pass
        
        return Response(status=status.HTTP_201_CREATED)

class editjob(APIView):
    def get_object(self, pk):
        try:
            return job_post.objects.get(pk=pk)
        except job_post.DoesNotExist:
            raise Http404
    def get_objects(self,pk):
        try:
            return job_post_skill_set.objects.get(pk=pk)
        except job_post_skill_set.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = job_post_serializer(data)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        jobpost = self.get_object(pk)
        # useraccountid=request.data.get('user_account_id')
        # user_account_id=user_account.objects.get(id=useraccountid)

        joblocation = jobpost.job_location_id
        joblocation.street_address = request.data.get('street_address', joblocation.street_address)
        joblocation.city = request.data.get('city', joblocation.city)
        joblocation.state = request.data.get('state', joblocation.state)
        joblocation.country = request.data.get('country', joblocation.country)
        joblocation.zip = request.data.get('zip', joblocation.zip)
        joblocation.save()

        jobpost.job_type_id = job_type.objects.get(id=request.data.get('job_type_id', jobpost.job_type_id.id))
        # jobpost.company_id = company.objects.get(id=request.data.get('company_id', jobpost.company_id.id))
        
        company_id = request.data.get('company_id', None)

        if company_id is not None:
            try:
                company_instance = company.objects.get(id=company_id)
            except company.DoesNotExist:
                return Response({"message": "Invalid company ID"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            company_instance = None

        
        is_company_name_hidden = request.data.get('is_company_name_hidden', None)
        if is_company_name_hidden is not None:
            if is_company_name_hidden.lower() == 'true':
                jobpost.is_company_name_hidden = True
            elif is_company_name_hidden.lower() == 'false':
                jobpost.is_company_name_hidden = False
            else:
                # Handle invalid input
                pass

        jobpost.job_description = request.data.get('job_description', jobpost.job_description)
        
        # incoming_data = {}

        # for key in request.data.keys():
        #     if key.startswith('job_qualification[') and key.endswith('][id]'):
        #         start_index = key.find('[') + 1
        #         end_index = key.find(']')
        #         index_value = int(key[start_index:end_index])

        #         id = request.data.getlist('job_qualification[{}][id]'.format(index_value))[0]
        #         value = request.data.getlist('job_qualification[{}][value]'.format(index_value))[0]
        #         incoming_data[int(id)] = value

        # existing_qualifications = jobpost.job_qualification
        # existing_ids = [qualification['id'] for qualification in existing_qualifications]

        # for qualification in existing_qualifications:
        #     id = qualification['id']
        #     if id not in incoming_data:
        #         existing_qualifications.remove(qualification)

        # for qualification in existing_qualifications:
        #     id = qualification['id']
        #     existing_value = qualification['value']
        #     incoming_value = incoming_data.get(id)

        #     if incoming_value and incoming_value != existing_value:
        #         qualification['value'] = incoming_value

        # for key in request.data.keys():
        #     if key.startswith('job_qualification[') and key.endswith('][id]'):
        #         start_index = key.find('[') + 1
        #         end_index = key.find(']')
        #         id = int(key[start_index:end_index])

        #         if id not in existing_ids:
        #             value = request.data.getlist('job_qualification[{}][value]'.format(id))[0]
        #             existing_qualifications.append({'id': id, 'value': value})

        # jobpost.job_qualification = existing_qualifications

        incoming_data = {}

        for key in request.data.keys():
            if key.startswith('job_qualification[') and key.endswith('][id]'):
                start_index = key.find('[') + 1
                end_index = key.find(']')
                index_value = int(key[start_index:end_index])

                id = request.data.getlist('job_qualification[{}][id]'.format(index_value))[0]
                value = request.data.getlist('job_qualification[{}][value]'.format(index_value))[0]
                incoming_data[int(id)] = value

        existing_qualifications = jobpost.job_qualification

        if not existing_qualifications:
            existing_qualifications = []

        existing_ids = [qualification['id'] for qualification in existing_qualifications]

        # Remove qualifications that are not in the incoming request
        for qualification in existing_qualifications:
            id = qualification['id']
            if id not in incoming_data:
                existing_qualifications.remove(qualification)

        # Update or add qualifications based on incoming data
        for qualification in existing_qualifications:
            id = qualification['id']
            existing_value = qualification['value']
            incoming_value = incoming_data.get(id)

            if incoming_value and incoming_value != existing_value:
                qualification['value'] = incoming_value

        for key in request.data.keys():
            if key.startswith('job_qualification[') and key.endswith('][id]'):
                start_index = key.find('[') + 1
                end_index = key.find(']')
                id = int(key[start_index:end_index])

                if id not in existing_ids:
                    value = request.data.getlist('job_qualification[{}][value]'.format(id))[0]
                    existing_qualifications.append({'id': id, 'value': value})

        jobpost.job_qualification = existing_qualifications



        jobpost.job_title = request.data.get('job_title', jobpost.job_title)
        jobpost.job_location_id = joblocation
        jobpost.created_date = request.data.get('created_date', jobpost.created_date)
        jobpost.is_active = request.data.get('is_active', jobpost.is_active)
        is_active_str = request.data.get('is_active')
        experince_type_id = request.data.get('experince_type_id', jobpost.experince_type_id.id)
        experince_type_instance = experince_type.objects.get(id=experince_type_id)
        jobpost.experince_type_id = experince_type_instance

        user_account_id = request.data.get('user_account_id', jobpost.user_account_id.id)
        user_account_id_instance = user_account.objects.get(id=user_account_id)
        jobpost.user_account_id = user_account_id_instance
        # jobpost.experince_type_id = request.data.get('experince_type_id',jobpost.experince_type_id)

        jobpost.salary = request.data.get('salary',jobpost.salary)
        jobpost.is_active = ast.literal_eval(is_active_str.title())

        jobpost.company_id = company_instance
        
        jobpost.save()

        skillsetids = request.data.get('skill_set_id').split(',')
        
        # # Delete existing records
        # job_post_skill_set.objects.filter(user_account_id=user_account_id).delete()
        
        seekerskillset = None

        for skillsetid in skillsetids:
            if skillsetid:
                try:
                    skill_set_id = skill_set.objects.get(id=int(skillsetid))
                    skill_level = request.data.get('skill_level')
                    job_post_id=jobpost.id
                    job_post_instance = job_post.objects.get(id=job_post_id)
                    seekerskillset = job_post_skill_set(skill_set_id=skill_set_id, skill_level=skill_level,job_post_id=job_post_instance)
                    seekerskillset.save() 
                except skill_set.DoesNotExist:
                    
                    pass

        serializer = job_post_serializer(jobpost)
        return Response(serializer.data)
    
    def delete(self, request, pk, format=None):
        calendars = self.get_object(pk)
        # test=self.get_objects(pk)
        # test.delete()
        calendars.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
        
class joblocation(APIView):

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

class editjoblocation(APIView):
    def get_object(self, pk):
        try:
            return job_location.objects.get(pk=pk)
        except job_location.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        calendars = self.get_object(pk)
        serializer = job_location_serializer(calendars)
        try:
            data = list()
            data.append(serializer.data)
        except Http404:
            return Response(data)
        return Response(data)

    def patch(self, request, pk):
        calendars = self.get_object(pk)
        serializer = job_location_serializer(calendars, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        calendars = self.get_object(pk)
        serializer = job_location_serializer(calendars, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        calendars = self.get_object(pk)
        calendars.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
class educationdetail(APIView):

    queryset = education_detail.objects.all()
    serializer_class = education_detail_serializer

    def get(self, request, format=None):
        user_data = education_detail.objects.all().order_by('-createdDate')
        serializer = education_detail_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = education_detail_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class seekerskillset(APIView):

    queryset = seeker_skill_set.objects.all()
    serializer_class = seeker_skill_set_serializer

    def get(self, request, format=None):
        user_data = seeker_skill_set.objects.all().order_by('-createdDate')
        serializer = seeker_skill_set_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
        
class experincedetail(APIView):

    queryset = experience_detail.objects.all()
    serializer_class = experience_detail_serializer

    def get(self, request, format=None):
        user_data = experience_detail.objects.all().order_by('-createdDate')
        serializer = experience_detail_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = experience_detail_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class skills(APIView):

    queryset = skill_set.objects.all()
    serializer_class = skill_set_serializer

    def get(self, request, format=None):
        user_data = skill_set.objects.all().order_by('-createdDate')
        serializer = skill_set_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        skill_set_name=request.data.get('skill_set_name','').lower()
        if skill_set.objects.filter(skill_set_name__iexact=skill_set_name).exists():
            return JsonResponse({'error': 'Record already exists in skill_set table.'}, status=status.HTTP_400_BAD_REQUEST)
        
        skill_set_name = request.data.get('skill_set_name')
        user_account_id = request.data.get('user_account_id')
        user_account_id = user_account.objects.get(id=user_account_id)

        skillset = skill_set(skill_set_name=skill_set_name, user_account_id=user_account_id)
        skillset.save() 

        serializer=skill_set_serializer(skillset)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class skillset(APIView):

    queryset = job_post_skill_set.objects.all()
    serializer_class = job_post_skill_set_serializer

    def get(self, request, format=None):
        user_data = job_post_skill_set.objects.all().order_by('-createdDate')
        serializer = job_post_skill_set_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
class jobtype(APIView):

    queryset = job_type.objects.all()
    serializer_class = job_type_serializer

    def get(self, request, format=None):
        user_data = job_type.objects.all().order_by('-createdDate')
        serializer = job_type_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
class seekerprofile(APIView):

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
        uploaded_cv = request.data.get('uploaded_cv')

        seekerprofile=seeker_profile(user_account_id=user_account_id,first_name=first_name,last_name=last_name,
                            current_salary=current_salary,is_annually_monthly=is_annually_monthly,currency=currency,uploaded_cv=uploaded_cv)
        seekerprofile.save()

        certificate_degree_name = request.data.get('certificate_degree_name')
        major = request.data.get('major')
        institute_university_name = request.data.get('institute_university_name')
        
        starting_date = request.data.get('starting_date')
        completion_date = request.data.get('completion_date')
        
        starting_date = datetime.strptime(starting_date, '%Y-%m-%d').date()
        starting_date = timezone.make_aware(datetime.combine(starting_date, datetime.min.time()))

        completion_date = datetime.strptime(completion_date, '%Y-%m-%d').date()
        completion_date = timezone.make_aware(datetime.combine(completion_date, datetime.min.time()))

        percentage = request.data.get('percentage')
        cgpa = request.data.get('cgpa')

        educationdetail=education_detail(user_account_id=user_account_id,certificate_degree_name=certificate_degree_name,major=major,
                         institute_university_name=institute_university_name,starting_date=starting_date,completion_date=completion_date,percentage=percentage,cgpa=cgpa)
        educationdetail.save()

        is_current_job = request.data.get('is_current_job', None)
        if is_current_job is not None:
            if is_current_job.lower() == 'true':
                is_current_job = True
            elif is_current_job.lower() == 'false':
                is_current_job = False
            else:
                # Handle invalid input
                pass
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if start_date == "":
            start_date = None
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
        if end_date == "":
            end_date = None
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.min.time()))

        job_title = request.data.get('job_title')
        company_name = request.data.get('company_name')
        job_location_city = request.data.get('job_location_city')
        job_location_state = request.data.get('job_location_state')
        job_location_country = request.data.get('job_location_country')
        description = request.data.get('description')

        experincedetail=experience_detail(user_account_id=user_account_id,is_current_job=is_current_job,start_date=start_date,
                         end_date=end_date,job_title=job_title,company_name=company_name,job_location_city=job_location_city,job_location_state=job_location_state,job_location_country=job_location_country,description=description)
        experincedetail.save()

        skillsetids = request.data.get('skill_set_id').split(',')

        for skillsetid in skillsetids:
            try:
                skill_set_id = skill_set.objects.get(id=int(skillsetid))
                skill_level = request.data.get('skill_level')
                seekerskillset = seeker_skill_set(user_account_id=user_account_id, skill_set_id=skill_set_id, skill_level=skill_level)
                seekerskillset.save() 
            except skill_set.DoesNotExist:
                
                pass


        data = {

        }
        
        return JsonResponse({'success': True, 'data': data},status=status.HTTP_201_CREATED)
    
class applyjob(APIView):
    queryset = job_post_activity.objects.all()
    serializer_class = job_post_activity_serializertest

    def get(self, request, format=None):
        user_data = job_post_activity.objects.all().order_by('-createdDate')
        serializer = job_post_activity_serializertest(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):

        # useraccountid = request.data.get('user_account_id')  
        # user_account_id = user_account.objects.get(id=useraccountid)

        status_test = request.data.get('status')
        # userstatus = request.data.get('userstatus')
        applicant_name = request.data.get('applicant_name')
        applicant_email = request.data.get('applicant_email')
        phone_num = request.data.get('phone_num')
        uploaded_cv = request.data.get('uploaded_cv')
        notice_period = request.data.get('notice_period')
        expected_pay = request.data.get('expected_pay')

        city = request.data.get('city')
        country = request.data.get('country')
        enquiry = request.data.get('enquiry')

        experience = request.data.get('experience')
        experience=experince_type.objects.get(id=experience)

        jobpostid = request.data.get('job_post_id')
        job_post_id = job_post.objects.get(id=jobpostid)

        jobpostactivity = job_post_activity(job_post_id=job_post_id, apply_date=datetime.now(),
                                                status=status_test,experience=experience,applicant_name=applicant_name,
                                                applicant_email=applicant_email,phone_num=phone_num,uploaded_cv=uploaded_cv,
                                                notice_period=notice_period,expected_pay=expected_pay,city=city,country=country,
                                                enquiry=enquiry)
        jobpostactivity.save()

        serializer=job_post_activity_serializertest(jobpostactivity)

        jobtitle = job_post_id.job_title
        applicant_name = request.data.get('applicant_name')
        applicant_email = request.data.get('applicant_email')
        phone_num = request.data.get('phone_num')
        city = request.data.get('city')
        country = request.data.get('country')
        enquiry = request.data.get('enquiry')
        uploaded_cv = request.data.get('uploaded_cv')
            
        SMTPserver = 'shared42.accountservergroup.com'
        sender = 'support@pacificmanpower.com.pg'
        destination = ['recruitment@pacificmanpower.com.pg', 'operations@pacificmanpower.com.pg']

        USERNAME = "ashwini@arohagroup.com"
        PASSWORD = "I2GJS.]rYk^s321"

        text_subtype = 'html'
        content = f"""\
            <html>
              <head>
                
              </head>
              <body>
                <table> 
                <tr>
                    <td>Job Name: </td>
                    <td>{jobtitle}</td>
                </tr>
                <tr>
                    <td>First Name: </td>
                    <td>{request.data['applicant_name']}</td>
                </tr>
                <br>
                <tr>
                    <td>Email address: </td>
                    <td>{request.data['applicant_email']}</td>
                </tr>
                <br>
                <tr>
                    <td>Phone: </td>
                    <td>{request.data['phone_num']}</td>
                </tr>
                <br>
                <tr>
                    <td>City: </td>
                    <td>{request.data['city']}</td>
                </tr>
                <br>
                <tr>
                    <td>Country: </td>
                    <td>{request.data['country']}</td>
                </tr>
                <br>
                <tr>
                    <td>Enquiry: </td>
                    <td>{request.data['enquiry']}</td>
                </tr>
                <br>
                </table><br>
              </body>
            </html>
            """

        subject = "Job Application"

        # msg = MIMEText(content, text_subtype)
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = destination

        msg.attach(MIMEText(content, text_subtype))

        # Attach the uploaded CV file
        cv_filename = os.path.basename(uploaded_cv.name)  # Extract the filename from the uploaded_cv object

        # Save the uploaded CV to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in uploaded_cv.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        # Attach the temporary CV file to the email
        with open(temp_file_path, "rb") as f:
            cv_part = MIMEApplication(f.read(), Name=cv_filename)
        cv_part['Content-Disposition'] = f'attachment; filename="{cv_filename}"'
        msg.attach(cv_part)


        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()

        os.remove(temp_file_path)

        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class trendingnews(APIView):

    queryset = trending_news.objects.all()
    serializer_class = trending_news_serializer

    def get(self, request, format=None):
        user_data = trending_news.objects.all().order_by('-createdDate')
        serializer = trending_news_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):

        useraccountid=request.data.get('user_account_id') 
        user_account_id=user_account.objects.get(id=useraccountid)

        news_title = request.data.get('news_title')
        news_description = request.data.get('news_description')
        news_image = request.data.get('news_image')

        trendingnews=trending_news(user_account_id=user_account_id,news_title=news_title,news_description=news_description,
                         news_image=news_image)
        trendingnews.save()

        return Response(status=status.HTTP_201_CREATED)

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
        try:
            trendingnews = trending_news.objects.get(pk=pk)
        except trending_news.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        trendingnews.user_account_id = user_account.objects.get(id=request.data.get('user_account_id'))
        trendingnews.news_title = request.data.get('news_title')
        trendingnews.news_description = request.data.get('news_description')
        # trendingnews.news_image = request.data.get('news_image')

        if 'news_image' in request.data:
            trendingnews.news_image = request.data.get('news_image')

        trendingnews.save()

        return Response(status=status.HTTP_200_OK)
    

    def patch(self, request, pk):
        calendars = self.get_object(pk)
        serializer = trending_news_serializer(calendars, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def delete(self, request, pk, format=None):
        data = self.get_object(pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class educationdetailIND(APIView):
    def get_object(self, pk):
        try:
            return education_detail.objects.get(user_account_id=pk)
        except education_detail.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = education_detail_serializer(data)
        return Response(serializer.data)
    
class skillsetIND(APIView):
    def get_object(self, pk):
        try:
            return job_post_skill_set.objects.get(pk=pk)
        except job_post_skill_set.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = job_post_skill_set_serializer(data)
        return Response(serializer.data)
    
class skillssetIND(APIView):
    def get_object(self, pk):
        try:
            return skill_set.objects.get(pk=pk)
        except skill_set.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = skill_set_serializer(data)
        return Response(serializer.data)
    
class experincedetailIND(APIView):
    def get_object(self, pk):
        try:
            return experience_detail.objects.get(user_account_id=pk)
        except experience_detail.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = experience_detail_serializer(data)
        return Response(serializer.data)
    
class seekerskillsetIND(APIView):
    def get_object(self, pk):
        try:
            return seeker_skill_set.objects.filter(user_account_id=pk)
        except seeker_skill_set.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = seeker_skill_set_serializertest(data, many=True)
        return Response(serializer.data)
    
class applyjobIND(APIView):

    def get_object(self, pk):
        try:
            return job_post_activity.objects.filter(pk=pk)
        except job_post_activity.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = job_post_activity_serializertest(queryset, many=True)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None): 

        status_test = request.data.get('status')
        job_post_id = request.data.get('job_post_id')

        jobpostactivity = job_post_activity.objects.get(pk=pk)

        jobpostactivity.status = status_test
        jobpostactivity.job_post_id__id = job_post_id

        jobpostactivity.save()

        return Response({"message": "updated"}, status=status.HTTP_201_CREATED) 

class editseekrprofile(APIView):
    def get_object(self, pk):
        try:
            return seeker_profile.objects.get(pk=pk)
        except seeker_profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = seeker_profile_serializer(data)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        useraccountid = request.data.get('user_account_id')
        user_account_id = user_account.objects.get(id=useraccountid)

        user_account_id.user_image = request.data.get('user_image')
        user_account_id.save()

        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        current_salary = request.data.get('current_salary')
        is_annually_monthly = request.data.get('is_annually_monthly')
        currency = request.data.get('currency')
        
        uploaded_cv = request.data.get('uploaded_cv', None)

        seekerprofile = seeker_profile.objects.get(pk=pk)

        seekerprofile.user_account_id = user_account_id
        seekerprofile.first_name = first_name
        seekerprofile.last_name = last_name
        seekerprofile.current_salary = current_salary
        seekerprofile.is_annually_monthly = is_annually_monthly
        seekerprofile.currency = currency
        if uploaded_cv is not None:
            seekerprofile.uploaded_cv = uploaded_cv

        seekerprofile.save()
        
        # if uploaded_cv:
        #     valid_extensions = ['.pdf']
        #     ext = os.path.splitext(uploaded_cv.name)[1]
        #     if not ext.lower() in valid_extensions:
        #         return Response({"message": "Invalid file type. Only image files with extensions {} are allowed".format(', '.join(valid_extensions))}, status=status.HTTP_403_FORBIDDEN)
            
        # else:

        #     seekerprofile.save()

        certificate_degree_name = request.data.get('certificate_degree_name')
        major = request.data.get('major')
        institute_university_name = request.data.get('institute_university_name')
        starting_date = request.data.get('starting_date')
        completion_date = request.data.get('completion_date')

        if starting_date == "":
            starting_date = None
        else:
            starting_date = datetime.strptime(starting_date, '%Y-%m-%d').date()
            starting_date = timezone.make_aware(datetime.combine(starting_date, datetime.min.time()))

        if completion_date == "":
            completion_date = None
        else:
            completion_date = datetime.strptime(completion_date, '%Y-%m-%d').date()
            completion_date = timezone.make_aware(datetime.combine(completion_date, datetime.min.time()))
            
        percentage = request.data.get('percentage')
        cgpa = request.data.get('cgpa')

        educationdetail = education_detail.objects.get(user_account_id=user_account_id)
        
        educationdetail.certificate_degree_name = certificate_degree_name
        educationdetail.major = major
        educationdetail.institute_university_name = institute_university_name
        educationdetail.starting_date = starting_date
        educationdetail.completion_date = completion_date
        educationdetail.percentage = percentage
        educationdetail.cgpa = cgpa

        educationdetail.save()

        is_current_job = request.data.get('is_current_job', None)
        if is_current_job is not None:
            if is_current_job.lower() == 'true':
                is_current_job = True
            elif is_current_job.lower() == 'false':
                is_current_job = False
            else:
                
                pass
        
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if start_date == "" or start_date == 'undefined':
            start_date = None
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))

        if end_date == "" or end_date == 'undefined':
            end_date = None
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.min.time()))
        
        job_title = request.data.get('job_title')
        company_name = request.data.get('company_name')
        job_location_city = request.data.get('job_location_city')
        job_location_state = request.data.get('job_location_state')
        job_location_country = request.data.get('job_location_country')
        description = request.data.get('description')

        experincedetail = experience_detail.objects.get(user_account_id=user_account_id)

        experincedetail.is_current_job = is_current_job
        experincedetail.start_date = start_date
        experincedetail.end_date = end_date
        experincedetail.job_title = job_title
        experincedetail.company_name = company_name
        experincedetail.job_location_city = job_location_city
        experincedetail.job_location_state = job_location_state
        experincedetail.job_location_country = job_location_country
        experincedetail.description = description

        experincedetail.save()

        skillsetids = request.data.get('skill_set_id').split(',')
  
        seeker_skill_set.objects.filter(user_account_id=user_account_id).delete()

        seekerskillset = None

        for skillsetid in skillsetids:
            if skillsetid:
                try:
                    skill_set_id = skill_set.objects.get(id=int(skillsetid))
                    skill_level = request.data.get('skill_level')
                    seekerskillset = seeker_skill_set(user_account_id=user_account_id, skill_set_id=skill_set_id, skill_level=skill_level)
                    seekerskillset.save() 
                except skill_set.DoesNotExist:
                    
                    pass

        # seekerprofiledata = serializers.serialize('json', [seekerprofile, ])
        # educationdetaildata = serializers.serialize('json', [educationdetail, ])
        # experincedetaildata = serializers.serialize('json', [experincedetail, ])
        # seekerskillsetdata = serializers.serialize('json', [seekerskillset, ])

        data = {
            # 'seeker_profile': seekerprofiledata,
            # 'education_detail': educationdetaildata,
            # 'experience_detail': experincedetaildata,
            # 'seekerskillsetdata': seekerskillsetdata
        }
        return JsonResponse({'success': True, 'data': data},status=status.HTTP_201_CREATED)

class contactus(APIView):

    queryset = contact_us.objects.all()
    serializer_class = contact_us_serializer

    def get(self, request, format=None):
        user_data = contact_us.objects.all().order_by('-createdDate')
        serializer = contact_us_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):


        email = request.data.get('email')
        name = request.data.get('name')
        message = request.data.get('message')

        getInTouch=contact_us(email=email,name=name,message=message)
        getInTouch.save()
            
        SMTPserver = 'shared42.accountservergroup.com'
        sender = 'support@pacificmanpower.com.pg'
        destination = ['recruitment@pacificmanpower.com.pg', 'operations@pacificmanpower.com.pg']

        USERNAME = "ashwini@arohagroup.com"
        PASSWORD = "I2GJS.]rYk^s321"

        text_subtype = 'html'
        content = f"""\
            <html>
              <head>
                
              </head>
              <body>
                <p>

                <p2>Hi,</p2>
                <br>
                <br>
                <p2>Below the information about the user who is interested</p2>
                <br><br>
                <table> 
                <tr>
                    <td>Name : </td>
                    <td>{request.data['name']}</td>
                </tr>
                <br>
                <tr>
                    <td>Email address : </td>
                    <td>{request.data['email']}</td>
                </tr>
                <br>
                 <tr>
                    <td>Message : </td>
                    <td>{request.data['message']}</td>
                </tr>
                </table><br>
              </body>
            </html>
            """

        subject = "Contact Us"

        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(destination)

        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()

        return Response({'email sent': True}, status=status.HTTP_201_CREATED)
    
class recEmail(APIView):

    queryset = recservice.objects.all()
    serializer_class = recservice_serializer

    def get(self, request, format=None):
        user_data = recservice.objects.all().order_by('-createdDate')
        serializer = recservice_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        # useraccountid=request.data.get('user_account_id')
        # user_account_id=user_account.objects.get(id=useraccountid)

        email = request.data.get('email')
        name = request.data.get('name')
        message = request.data.get('message')

        getInTouch=recservice(email=email,name=name,message=message)
        getInTouch.save()

        SMTPserver = 'shared42.accountservergroup.com'
        sender = 'support@pacificmanpower.com.pg'
        destination = ['recruitment@pacificmanpower.com.pg', 'operations@pacificmanpower.com.pg']

        USERNAME = "ashwini@arohagroup.com"
        PASSWORD = "I2GJS.]rYk^s321"

        text_subtype = 'html'
        content = f"""\
            <html>
              <head>
                
              </head>
              <body>
                <p>

                <p2>Hi,</p2>
                <br>
                <br>
                <p2>Below the information about the user who is interested</p2>
                <br><br>
                <table> 
                <tr>
                    <td>Name : </td>
                    <td>{request.data['name']}</td>
                </tr>
                <br>
                <tr>
                    <td>Email address : </td>
                    <td>{request.data['email']}</td>
                </tr>
                <br>
                 <tr>
                    <td>Message : </td>
                    <td>{request.data['message']}</td>
                </tr>
                </table><br>
              </body>
            </html>
            """
        
        subject = "Recruitment service"
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = destination

        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()

        return Response({'email sent': True}, status=status.HTTP_201_CREATED)
    
class joblistbycompany(APIView):
    def get(self, request,searchItem, format=None, *args, **kwargs):
        
        if not searchItem or searchItem.lower() == 'null':
            # return an empty array if searchItem is null or empty
            return Response([], status=status.HTTP_204_NO_CONTENT)
        
        search_terms = [term.strip() for term in searchItem.split('/') if term.strip() and term.strip().lower() != 'null']
        query = Q()

        filtered_data = []

        if(len(search_terms)>0):

            if(len(search_terms)==1):

                or_query = Q(job_title__icontains=search_terms[0]) | Q(job_location_id__country__iexact=search_terms[0]) | Q(job_type_id__job_type__iexact=search_terms[0]) | Q(company_id__company_name__iexact=search_terms[0])
                filtered_data = job_post.objects.filter(or_query)

            else:

                for term in search_terms:
                    query &= Q(job_title__icontains=term.strip()) | Q(job_location_id__country__iexact=term.strip()) | Q(job_type_id__job_type__iexact=term.strip()) | Q(company_id__company_name__iexact=term.strip())

                filtered_data = job_post.objects.filter(query)
        
            serializer = job_post_serializer(filtered_data, many=True)
            return Response(serializer.data)
    
class filteredjobbyparttime(APIView):
    def get(self, request, format=None, *args, **kwargs):

        filtered_data = job_post.objects.filter(job_type_id__job_type__iexact='part time')

        serializer = job_post_serializer(filtered_data, many=True)
        return Response(serializer.data)
    
class applyjobTrue(APIView):
    def get(self, request, userstatus, format=None):
        calendars = job_post_activity.objects.filter(userstatus=userstatus)
        serializer = job_post_activity_serializertest(calendars, many=True)
        return Response(serializer.data)
 
class applyjobUserIdTrue(APIView):
    def get(self, request, user_account_id,userstatus, format=None):
        calendars = job_post_activity.objects.filter(user_account_id=user_account_id,userstatus=userstatus)
        serializer = job_post_activity_serializertest(calendars, many=True)
        return Response(serializer.data)
    
    def get(self, request, format=None, *args, **kwargs):

        filtered_data = job_post_activity.objects.filter( 
            user_account_id=self.kwargs['user_account_id'],
            userstatus=self.kwargs['userstatus'])

        serializer = job_post_activity_serializertest(filtered_data, many=True)
        return Response(serializer.data)
    
class filteredjobbyfulltime(APIView):
    def get(self, request, format=None, *args, **kwargs):

        filtered_data = job_post.objects.filter(job_type_id__job_type__iexact='full time')

        serializer = job_post_serializer(filtered_data, many=True)
        return Response(serializer.data)
    
class filteredjobbyfreelancer(APIView):
    def get(self, request, format=None, *args, **kwargs):

        filtered_data = job_post.objects.filter(job_type_id__job_type__iexact='freelancer')

        serializer = job_post_serializer(filtered_data, many=True)
        return Response(serializer.data)
    

class subscribeemail(APIView):

    queryset = subscribe.objects.all()
    serializer_class = subscribe_serializer

    def get(self, request, format=None):
        user_data = subscribe.objects.all().order_by('-createdDate')
        serializer = subscribe_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        
        # useraccountid = request.data.get('user_account_id')
        # user_account_obj = user_account.objects.get(id=useraccountid)
        email = request.data.get('email')

        subscribetable = subscribe( email=email)
        subscribetable.save()

        # user_account_obj.subscribed_email_id = email
        # user_account_obj.subscribed = 1
        # user_account_obj.save()

        serializer = subscribe_serializer(subscribetable)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class notappliedjob(APIView):
    def post(self, request, format=None, *args, **kwargs):

        user_account_id=request.data.get('user_account_id')

        if job_post_activity.objects.filter(user_account_id=user_account_id).exists():
            job_post_ids = job_post_activity.objects.filter(user_account_id=user_account_id).values_list('job_post_id', flat=True)

            postedjob = job_post.objects.exclude(id__in=job_post_ids)
            postedjob_data = job_post_serializer(postedjob, many=True).data
            
            return Response(postedjob_data)
        else:

            all_job_posts = job_post.objects.all()
            all_job_posts_data = job_post_serializer(all_job_posts, many=True).data
            return Response(all_job_posts_data)
        
class activefilter(APIView):
    def get(self, request, user_account_id,is_active, format=None):
        # calendars = job_post.objects.filter(is_active=is_active)
        # serializer = job_post_serializer(calendars, many=True)
        # return Response(serializer.data)

        # user_account_id=request.data.get('user_account_id')

        if job_post_activity.objects.filter(user_account_id=user_account_id).exists():
            # job_post_ids = job_post_activity.objects.values_list('job_post_id', flat=True)
            job_post_ids = job_post_activity.objects.filter(user_account_id=user_account_id).values_list('job_post_id', flat=True)

            postedjob = job_post.objects.exclude(id__in=job_post_ids).filter(is_active=True)
            postedjob_data = job_post_serializer(postedjob, many=True).data

            return Response(postedjob_data)
        else:
            postedjob = job_post.objects.filter(is_active=True)
            postedjob_data = job_post_serializer(postedjob, many=True).data

            return Response(postedjob_data)
    
class expType(APIView):

    queryset = experince_type.objects.all()
    serializer_class = experince_type_serializer

    def get(self, request, format=None):
        user_data = experince_type.objects.all().order_by('-createdDate')
        serializer = experince_type_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = experince_type_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class fetchJobSkills(APIView):
    def get(self, request, job_post_id, format=None):
        job_skills = job_post_skill_set.objects.filter(job_post_id=job_post_id)
        serializer = job_post_skill_set_serializer(job_skills, many=True)
        return Response(serializer.data)
    

class addgallery(APIView):

    queryset = gallery.objects.all()
    serializer_class = gallery_serializer

    def get(self, request, format=None):
        user_data = gallery.objects.all().order_by('-createdDate')
        serializer = gallery_serializer(user_data, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):

        useraccountid=request.data.get('user_account_id') 
        user_account_id=user_account.objects.get(id=useraccountid)
        image = request.data.get('image')
        title = request.data.get('title')

        gallerydata=gallery(user_account_id=user_account_id,image=image,title=title)
        gallerydata.save()

        return Response(status=status.HTTP_201_CREATED)
    
class editgallery(APIView):
    def get_object(self, pk):
        try:
            return gallery.objects.get(pk=pk)
        except gallery.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = gallery_serializer(data)
        return Response(serializer.data)
        
    # def put(self, request, pk, format=None): 
    #     user_account_id = request.data.get('user_account_id')
    #     image = request.data.get('image')

    #     gallerydata = gallery.objects.get(pk=pk)
    #     gallerydata.user_account_id__id = user_account_id
    #     gallerydata.image = image

    #     gallerydata.save()

    #     return Response({"message": "updated"}, status=status.HTTP_201_CREATED) 
        
    def delete(self, request, pk, format=None):
        data = self.get_object(pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class statusThroughfilter(APIView):
    def get(self, request, status,format=None, *args, **kwargs):
        filtered_data=None
        if status.lower()=='accepted':
            filtered_data = job_post_activity.objects.filter(status__iexact='Accepted')
        elif status.lower()=='rejected':
            filtered_data = job_post_activity.objects.filter(status__iexact='Rejected')
        elif status.lower()=='pending':
            filtered_data = job_post_activity.objects.filter(status__iexact='Pending')

        serializer = job_post_activity_serializertest(filtered_data, many=True)
        return Response(serializer.data)

class companynamefilter(APIView):
    def get(self, request, company_name, format=None, *args, **kwargs):
        filtered_data = company.objects.filter(company_name__icontains=company_name)
        serializer = company_serializer(filtered_data, many=True)
        return Response(serializer.data)