from django.db import models

# Create your models here.

#User Management
class user_type(models.Model):
    user_type_name=models.CharField(max_length=200)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class user_account(models.Model):
    user_type_id = models.ForeignKey('user_type',related_name='usertype', on_delete=models.CASCADE,default=None)
    first_name=models.CharField(max_length=122)  
    last_name=models.CharField(max_length=122,null=True,blank=True)  
    email_address=models.CharField(max_length=122,unique=True)    
    password=models.CharField(max_length=200)
    date_of_birth=models.DateField(blank=True,null=True)  #Optional Field
    gender=models.CharField(max_length=10, blank=True,null=True)
    isactive=models.BooleanField(blank=True)
    contact_number = models.CharField(max_length=22, blank=True,null=True)
    subscribed_email_id=models.CharField(max_length=122,blank=True,null=True)
    subscribed=models.IntegerField(blank=True,default=0)
    # sms_notification_active=models.BooleanField()
    email_notification_active=models.BooleanField()
    user_image=models.ImageField(upload_to='user/',max_length=200,blank=True,null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class user_log(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_id', on_delete=models.CASCADE,default=None,primary_key=True)
    last_login_date = models.DateTimeField(auto_now=True)
    last_job_apply_date = models.DateTimeField(auto_now=True,blank=True,null=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

#Company Porfile
class business_stream(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_id_business_stream', on_delete=models.CASCADE,default=None)
    business_stream_name=models.CharField(max_length=200)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class company(models.Model):
    company_name=models.CharField(max_length=200)    
    profile_description=models.CharField(max_length=2000, null=True,blank=True)
    business_stream_id = models.ForeignKey('business_stream',related_name='business_stream_id', on_delete=models.CASCADE,default=None,null=True)
    user_account_id = models.ForeignKey('user_account',related_name='user_account_id_company', on_delete=models.CASCADE,default=None,null=True)
    establishment_date=models.DateField(null=True,blank=True)
    companyimage=models.ImageField(upload_to='companylogo/',max_length=200, null=True,blank=True)
    company_website_url=models.CharField(max_length=500, null=True,blank=True)
    company_size=models.CharField(max_length=500, null=True,blank=True)
    company_location=models.CharField(max_length=200, null=True,blank=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)


#Seeker Profile Builder
class education_detail(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_id_education_detail', on_delete=models.CASCADE,default=None)
    certificate_degree_name=models.CharField(max_length=500, null=True,blank=True)
    major=models.CharField(max_length=500, null=True,blank=True)
    institute_university_name=models.CharField(max_length=200, null=True,blank=True)
    starting_date=models.DateTimeField(null=True,blank=True)
    completion_date=models.DateTimeField(null=True,blank=True)
    percentage = models.IntegerField(null=True,blank=True)
    cgpa = models.IntegerField(null=True,blank=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    # primary_key = ('user_account_id','certificate_degree_name', 'major')

class experience_detail(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_ids', on_delete=models.CASCADE,default=None)
    is_current_job=models.BooleanField()
    start_date=models.DateTimeField(blank=True,null=True)
    end_date=models.DateTimeField(blank=True,null=True)
    job_title=models.CharField(max_length=500,blank=True,null=True)
    company_name=models.CharField(max_length=200,blank=True,null=True)
    job_location_city=models.CharField(max_length=500,blank=True,null=True)
    job_location_state=models.CharField(max_length=500,blank=True,null=True)
    job_location_country=models.CharField(max_length=500,blank=True,null=True)
    description=models.CharField(max_length=4000,blank=True,null=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    # primary_key = ('user_account_id','start_date', 'end_date')

class seeker_profile(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_idss', on_delete=models.CASCADE,default=None,primary_key=True)
    first_name=models.CharField(max_length=500)
    last_name=models.CharField(max_length=500, null=True,blank=True)
    current_salary = models.IntegerField(null=True,blank=True)
    is_annually_monthly=models.CharField(max_length=200,blank=True)
    currency=models.CharField(max_length=500,blank=True)
    uploaded_cv=models.FileField(null=True,blank=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)


class seeker_skill_set(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_idsss', on_delete=models.CASCADE,default=None)
    skill_set_id=models.ForeignKey('skill_set',related_name='skill_set_id_seeker', on_delete=models.CASCADE,default=None)# i need to add here forenkhkey from below table
    skill_level=models.IntegerField(null=True,blank=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    # primary_key = ('user_account_id', 'skill_set_id')

class skill_set(models.Model):
    skill_set_name=models.CharField(max_length=200)
    user_account_id = models.ForeignKey('user_account',related_name='user_account_id_skill_set', on_delete=models.CASCADE,default=None)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

#Job Post Management

class job_post(models.Model):
    posted_by_id = models.ForeignKey('job_post_activity',related_name='posted_by_id', on_delete=models.CASCADE,default=None,null=True,blank=True)
    job_type_id = models.ForeignKey('job_type',related_name='job_type_id', on_delete=models.CASCADE,default=None,null=True,blank=True)
    company_id = models.ForeignKey('company',related_name='company_id', on_delete=models.CASCADE,default=None,null=True,blank=True)
    experince_type_id = models.ForeignKey('experince_type',related_name='experince_type_id', on_delete=models.CASCADE,default=None,null=True,blank=True)
    user_account_id = models.ForeignKey('user_account',related_name='user_account_id_job_post', on_delete=models.CASCADE,default=None,null=True,blank=True)
    is_company_name_hidden=models.BooleanField()
    job_title=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True, blank=True)
    job_description=models.CharField(max_length=2000,null=True,blank=True)
    job_qualification=models.JSONField(max_length=3000,null=True,blank=True)
    salary=models.IntegerField(blank=True,null=True)
    job_location_id = models.ForeignKey('job_location',related_name='job_location_id', on_delete=models.CASCADE,default=None)
    is_active=models.BooleanField()
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    # primary_key = ('posted_by_id', 'job_type_id','company_id','job_location_id')

class job_post_activity(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_idssss', on_delete=models.CASCADE,default=None,null=True,blank=True)
    job_post_id = models.ForeignKey('job_post',related_name='job_post_id', on_delete=models.CASCADE,default=None,null=True)
    apply_date=models.DateTimeField(auto_now_add=True, blank=True)
    status=models.CharField(max_length=200)
    userstatus=models.BooleanField(blank=True,null=True)
    applicant_name=models.CharField(max_length=200, null=True,blank=True)
    applicant_email=models.CharField(max_length=200, null=True,blank=True)
    phone_num=models.CharField(max_length=22, null=True,blank=True)
    city=models.CharField(max_length=500, null=True,blank=True)
    country=models.CharField(max_length=500, null=True,blank=True)
    enquiry=models.CharField(max_length=500, null=True,blank=True)
    uploaded_cv=models.FileField(null=True,blank=True)
    notice_period=models.CharField(max_length=30,null=True,blank=True)
    expected_pay=models.IntegerField(null=True,blank=True)
    experience= models.ForeignKey('experince_type',related_name='experince_type_job_post_activity', on_delete=models.CASCADE,default=None,null=True,blank=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    # primary_key = ('user_account_id', 'job_post_id')


class job_type(models.Model):
    job_type=models.CharField(max_length=200)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class experince_type(models.Model):
    experince_type=models.CharField(max_length=200)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class job_location(models.Model):
    street_address=models.CharField(max_length=200, null=True,blank=True)
    city=models.CharField(max_length=500, null=True,blank=True)
    state=models.CharField(max_length=500, null=True,blank=True)
    country=models.CharField(max_length=500, null=True,blank=True)
    zip=models.CharField(max_length=500, null=True,blank=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class job_post_skill_set(models.Model):
    skill_set_id = models.ForeignKey('skill_set',related_name='skill_set_id', on_delete=models.CASCADE,default=None,null=True,blank=True,max_length=200)
    job_post_id = models.ForeignKey('job_post',related_name='job_post_id_job_post_skill_set', on_delete=models.CASCADE,default=None)
    skill_level=models.IntegerField(null=True,blank=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    # primary_key = ('skill_set_id', 'job_post_id')

class trending_news(models.Model):
    news_title=models.CharField(max_length=200)
    news_description=models.CharField(max_length=500,null=True,blank=True)
    news_image=models.ImageField(upload_to='news/',max_length=200, blank=True,null=True)
    user_account_id=models.ForeignKey('user_account',related_name='user_account_id_trending_news', on_delete=models.CASCADE,default=None)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class contact_us(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_id_contact_us', on_delete=models.CASCADE,default=None,null=True,blank=True)
    name=models.CharField(max_length=200, null=True,blank=True)
    email=models.CharField(max_length=122, null=True,blank=True)
    message=models.CharField(max_length=400, null=True,blank=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class recservice(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_id_recservice', on_delete=models.CASCADE,default=None,null=True,blank=True)
    name=models.CharField(max_length=200, null=True,blank=True)
    email=models.CharField(max_length=122, null=True,blank=True)
    message=models.CharField(max_length=400, null=True,blank=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class subscribe(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_id_subscribe', on_delete=models.CASCADE,default=None,null=True,blank=True)
    email=models.CharField(max_length=122)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)

class gallery(models.Model):
    user_account_id = models.ForeignKey('user_account',related_name='user_account_id_gallery', on_delete=models.CASCADE,default=None)
    title=models.CharField(max_length=200, null=True,blank=True)
    image=models.ImageField(upload_to='gallery/',max_length=200, blank=True,null=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True)