from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, read_only='True')
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )
    email = serializers.CharField(
        style={'input_type': 'email'}, write_only=True
    )
    groups = serializers.CharField(
        style={'input_type': 'text'}, write_only=True
    )

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'password', 'groups']
        
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            password = make_password(validated_data['password'])
        )
        return user

class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ['url', 'id', 'name']

#User Management
class user_type_serializer(serializers.ModelSerializer):
    class Meta:
        model=user_type
        fields=['id','user_type_name','createdDate','modifiedDate']

class user_account_serializer(serializers.ModelSerializer):
    
    user_type_id=serializers.ReadOnlyField(source='user_type_id.id')
    class Meta:
        model=user_account
        fields=['id','user_type_id','email_address','password','first_name','last_name','date_of_birth','gender','isactive','contact_number',
                'email_notification_active','user_image','registration_date','createdDate','modifiedDate']
        
class user_log_serializer(serializers.ModelSerializer):

    user_account_id=serializers.ReadOnlyField(source='user_account_id.id')
    class Meta:
        model=user_log
        fields=['user_account_id','last_login_date','last_job_apply_date','createdDate','modifiedDate']
        
#Company Porfile
class business_stream_serializer(serializers.ModelSerializer):
    class Meta:
        model=business_stream
        fields=['id','business_stream_name']

class company_serializer(serializers.ModelSerializer):
    
    business_stream_id=serializers.ReadOnlyField(source='business_stream_id.id')
    class Meta:
        model=company
        fields=['id','company_name','profile_description','business_stream_id','establishment_date','company_website_url','createdDate','modifiedDate']

class company_image_serializer(serializers.ModelSerializer):

    company_id=serializers.ReadOnlyField(source='company_id.id')
    class Meta:
        model=company_image
        fields=['id','company_id','companyimage','createdDate','modifiedDate']

#Seeker Profile Builder
class education_detail_serializer(serializers.ModelSerializer):
   
    user_account_id=serializers.ReadOnlyField(source='user_account_id.id')
    class Meta:
        model=education_detail
        fields=['id','user_account_id','certificate_degree_name','major','institute_university_name','starting_date','completion_date','percentage','cgpa',
                'createdDate','modifiedDate']
        
class experience_detail_serializer(serializers.ModelSerializer):
   
    user_account_id=serializers.ReadOnlyField(source='user_account_id.id')
    class Meta:
        model=experience_detail
        fields=['id','user_account_id','is_current_job','start_date','end_date','job_title','company_name','job_location_city','job_location_state',
                'job_location_country','description','createdDate','modifiedDate']
        
class seeker_profile_serializer(serializers.ModelSerializer):
    
    user_account_id=serializers.ReadOnlyField(source='user_account_id.id')
    class Meta:
        model=seeker_profile
        fields=['user_account_id','first_name','last_name','current_salary','is_annually_monthly','currency','uploaded_cv'
                ,'createdDate','modifiedDate']
        
class seeker_skill_set_serializer(serializers.ModelSerializer):
    
    user_account_id=serializers.ReadOnlyField(source='user_account_id.id')
    skill_set_id=serializers.ReadOnlyField(source='skill_set_id.id')
    class Meta:
        model=seeker_skill_set
        fields=['id','user_account_id','skill_set_id','skill_level','createdDate','modifiedDate']

class skill_set_serializer(serializers.ModelSerializer):
    class Meta:
        model=skill_set
        fields=['id','skill_set_name','createdDate','modifiedDate']

#Job Post Management
class job_post_activity_serializer(serializers.ModelSerializer):
    
    user_account_id=serializers.ReadOnlyField(source='user_account_id.id')
    job_post_id=serializers.ReadOnlyField(source='job_post.id')
    class Meta:
        model=job_post_activity
        fields=['id','job_post_id','user_account_id','apply_date','createdDate','modifiedDate']

class job_post_skill_set_serializer(serializers.ModelSerializer):
    
    skill_set_id=serializers.ReadOnlyField(source='skill_set_id.id')
    job_post_id=serializers.ReadOnlyField(source='job_post_id.id')
    class Meta:
        model=job_post_skill_set
        fields=['id','skill_set_id','job_post_id','skill_level','createdDate','modifiedDate']

class job_type_serializer(serializers.ModelSerializer):
    class Meta:
        model=job_type
        fields=['id','job_type','createdDate','modifiedDate']



class job_location_serializer(serializers.ModelSerializer):
    class Meta:
        model=job_location
        fields=['id','street_address','city','state','country','zip','createdDate','modifiedDate']

class job_post_serializer(serializers.ModelSerializer):
    # posted_by_id=serializers.ReadOnlyField(source='posted_by_id.id')
    # job_type_id=serializers.ReadOnlyField(source='job_type_id.id')
    # company_id=company(source='company_id.id')
    posted_by_id=job_post_activity_serializer()
    job_type_id=job_type_serializer()
    company_id=company_serializer()
    job_location_id=job_location_serializer()
    class Meta:
        model=job_post
        fields=['id','posted_by_id','job_type_id','company_id','is_company_name_hidden','job_title','created_date',
                'job_description','is_active','job_location_id','createdDate','modifiedDate']

class trending_news_serializer(serializers.ModelSerializer):
   
    user_account_id=serializers.ReadOnlyField(source='user_account_id.id')
    class Meta:
        model=trending_news
        fields=['id','news_title','news_description','news_image','user_account_id',
                'createdDate','modifiedDate']

