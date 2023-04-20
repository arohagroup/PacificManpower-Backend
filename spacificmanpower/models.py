from django.db import models

# Create your models here.

#User Management
class user_type(models.Model):
    user_type_name=models.CharField(max_length=20)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class user_account(models.Model):
    user_type_id = models.ForeignKey('user_type',related_name='usertype', on_delete=models.CASCADE,default=None)
    first_name=models.CharField(max_length=122)  
    last_name=models.CharField(max_length=122)  
    email_address=models.CharField(max_length=122,unique=True)    
    password=models.CharField(max_length=100)
    date_of_birth=models.DateField()
    gender=models.CharField(max_length=10)
    isactive=models.BooleanField(blank=True)
    contact_number = models.IntegerField()
    # sms_notification_active=models.BooleanField()
    email_notification_active=models.BooleanField()
    user_image=models.ImageField(max_length=200,null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class user_log(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_id', on_delete=models.CASCADE,default=None,primary_key=True)
    last_login_date = models.DateTimeField(auto_now=True)
    last_job_apply_date = models.DateTimeField(blank=True,null=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    modifiedDate = models.DateTimeField(auto_now=True)

#Company Porfile
class business_stream(models.Model):
    business_stream_name=models.CharField(max_length=100)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class company(models.Model):
    company_name=models.CharField(max_length=100)    
    profile_description=models.CharField(max_length=1000)
    business_stream_id = models.ForeignKey('business_stream',related_name='business_stream_id', on_delete=models.CASCADE,default=None,null=True)
    establishment_date=models.DateField()
    company_website_url=models.CharField(max_length=500)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class company_image(models.Model):
    company_id = models.ForeignKey('company',related_name='company_id_company_image', on_delete=models.CASCADE,default=None,null=True)
    companyimage=models.ImageField(max_length=200, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

#Seeker Profile Builder
class education_detail(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_id_education_detail', on_delete=models.CASCADE,default=None)
    certificate_degree_name=models.CharField(max_length=50)
    major=models.CharField(max_length=50)
    institute_university_name=models.CharField(max_length=100)
    starting_date=models.DateTimeField()
    completion_date=models.DateTimeField(blank=True)
    percentage = models.IntegerField(blank=True)
    cgpa = models.IntegerField(blank=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    # primary_key = ('user_account_id','certificate_degree_name', 'major')

class experience_detail(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_ids', on_delete=models.CASCADE,default=None)
    is_current_job=models.BooleanField()
    start_date=models.DateTimeField(blank=True,null=True)
    end_date=models.DateTimeField(blank=True,null=True)
    job_title=models.CharField(max_length=50,blank=True,null=True)
    company_name=models.CharField(max_length=100,blank=True,null=True)
    job_location_city=models.CharField(max_length=50,blank=True,null=True)
    job_location_state=models.CharField(max_length=50,blank=True,null=True)
    job_location_country=models.CharField(max_length=50,blank=True,null=True)
    description=models.CharField(max_length=4000,blank=True,null=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    # primary_key = ('user_account_id','start_date', 'end_date')

class seeker_profile(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_idss', on_delete=models.CASCADE,default=None,primary_key=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    current_salary = models.IntegerField(blank=True,null=True)
    is_annually_monthly=models.CharField(max_length=100,blank=True)
    currency=models.CharField(max_length=50,blank=True)
    uploaded_cv=models.FileField(null=True,blank=True)
    createdDate = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modifiedDate = models.DateTimeField(auto_now=True)


class seeker_skill_set(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_idsss', on_delete=models.CASCADE,default=None)
    skill_set_id=models.ForeignKey('skill_set',related_name='skill_set_id_seeker', on_delete=models.CASCADE,default=None)# i need to add here forenkhkey from below table
    skill_level=models.IntegerField()
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    # primary_key = ('user_account_id', 'skill_set_id')

class skill_set(models.Model):
    skill_set_name=models.CharField(max_length=50)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

#Job Post Management

class job_post(models.Model):
    posted_by_id = models.ForeignKey('job_post_activity',related_name='posted_by_id', on_delete=models.CASCADE,default=None,null=True,blank=True)
    job_type_id = models.ForeignKey('job_type',related_name='job_type_id', on_delete=models.CASCADE,default=None)
    company_id = models.ForeignKey('company',related_name='company_id', on_delete=models.CASCADE,default=None)
    experince_type_id = models.ForeignKey('experince_type',related_name='experince_type_id', on_delete=models.CASCADE,default=None,null=True,blank=True)
    is_company_name_hidden=models.BooleanField()
    job_title=models.CharField(max_length=20)
    created_date=models.DateTimeField(auto_now_add=True, blank=True)
    job_description=models.CharField(max_length=500)
    salary=models.IntegerField(max_length=30)
    job_location_id = models.ForeignKey('job_location',related_name='job_location_id', on_delete=models.CASCADE,default=None)
    is_active=models.BooleanField()
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    # primary_key = ('posted_by_id', 'job_type_id','company_id','job_location_id')

class job_post_activity(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_idssss', on_delete=models.CASCADE,default=None)
    job_post_id = models.ForeignKey('job_post',related_name='job_post_id', on_delete=models.CASCADE,default=None)
    apply_date=models.DateTimeField(auto_now_add=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    # primary_key = ('user_account_id', 'job_post_id')


class job_type(models.Model):
    job_type=models.CharField(max_length=20)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class experince_type(models.Model):
    experince_type=models.CharField(max_length=20)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class job_location(models.Model):
    street_address=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    zip=models.CharField(max_length=50)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class job_post_skill_set(models.Model):
    skill_set_id = models.ForeignKey('skill_set',related_name='skill_set_id', on_delete=models.CASCADE,default=None,null=True,blank=True)
    job_post_id = models.ForeignKey('job_post',related_name='job_post_id_job_post_skill_set', on_delete=models.CASCADE,default=None)
    skill_level=models.IntegerField()
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    # primary_key = ('skill_set_id', 'job_post_id')

class trending_news(models.Model):
    news_title=models.CharField(max_length=100)
    news_description=models.CharField(max_length=50)
    news_image=models.ImageField(max_length=200, blank=True,null=True)
    user_account_id=models.ForeignKey('user_account',related_name='user_account_id_trending_news', on_delete=models.CASCADE,default=None)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class contact_us(models.Model):
    name=models.CharField(max_length=25)
    email=models.CharField(max_length=15)
    message=models.CharField(max_length=400)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class subscribe(models.Model):
    email=models.CharField(max_length=25)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)
