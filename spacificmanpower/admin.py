from django.contrib import admin

from spacificmanpower.models import *
# Register your models here.

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_type_name','createdDate', 'modifiedDate')
    list_display_links = ('id', 'user_type_name')

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('id','user_type_id','email_address','password','date_of_birth','gender','isactive','contact_number',
                'email_notification_active','subscribed_email_id','subscribed','user_image','registration_date','createdDate','modifiedDate')
    list_display_links = ('id', 'user_type_id')

class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user_account_id','last_login_date','last_job_apply_date','createdDate','modifiedDate')
    list_display_links = ('user_account_id','last_login_date')

class BusinessStreamAdmin(admin.ModelAdmin):
    list_display = ('id','business_stream_name','user_account_id','createdDate','modifiedDate')
    list_display_links = ('id','business_stream_name')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id','company_name','profile_description','companyimage','business_stream_id','user_account_id','establishment_date',
                    'company_website_url','company_location','company_size','createdDate','modifiedDate')
    list_display_links = ('id','company_name')

class EducationDetailAdmin(admin.ModelAdmin):
    list_display = ('id','user_account_id','certificate_degree_name','major','institute_university_name','starting_date',
                    'completion_date','percentage','cgpa','createdDate','modifiedDate')
    list_display_links = ('id','user_account_id')

class ExperinceDetailAdmin(admin.ModelAdmin):
    list_display = ('id','user_account_id','is_current_job','start_date','end_date','job_title',
                    'company_name','job_location_city','job_location_state','job_location_country','description','createdDate','modifiedDate')
    list_display_links = ('id','user_account_id')

class SeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('user_account_id','first_name','last_name','current_salary','is_annually_monthly','uploaded_cv',
                    'currency','createdDate','modifiedDate')
    list_display_links = ('user_account_id','first_name')

class SeekerSkillSetAdmin(admin.ModelAdmin):
    list_display = ('id','user_account_id','skill_set_id','skill_level','createdDate','modifiedDate')
    list_display_links = ('id','user_account_id')

class SkillSetAdmin(admin.ModelAdmin):
    list_display = ('id','skill_set_name','user_account_id','createdDate','modifiedDate')
    list_display_links = ('id','skill_set_name')

class JobPostAdmin(admin.ModelAdmin):
    list_display = ('id','posted_by_id','job_type_id','company_id','user_account_id','experince_type_id','is_company_name_hidden','job_title','created_date',
                    'job_description','job_location_id','salary','is_active','createdDate','modifiedDate')
    list_display_links = ('id','posted_by_id')

class JobPostActivityAdmin(admin.ModelAdmin):
    list_display = ('id','user_account_id','job_post_id','apply_date','status','userstatus','applicant_name','applicant_email'
                ,'phone_num','city','country','enquiry','uploaded_cv','notice_period','expected_pay','experience','createdDate','modifiedDate')
    list_display_links = ('id','user_account_id')

class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('id','job_type','createdDate','modifiedDate')
    list_display_links = ('id','job_type')

class JobLocationAdmin(admin.ModelAdmin):
    list_display = ('id','street_address','city','state','country','zip','createdDate','modifiedDate')
    list_display_links = ('id','street_address')

class JobPostSkillSet(admin.ModelAdmin):
    list_display = ('id','skill_set_id','job_post_id','skill_level','createdDate','modifiedDate')
    list_display_links = ('id','skill_set_id')

class TrendingNewsAdmin(admin.ModelAdmin):
    list_display = ('id','user_account_id','news_title','news_description','news_image','createdDate','modifiedDate')
    list_display_links = ('id','user_account_id')

class ContactUs(admin.ModelAdmin):
    list_display = ('id','user_account_id','name','email','message','createdDate','modifiedDate')
    list_display_links = ('id','user_account_id')

class ExperinceTypeAdmin(admin.ModelAdmin):
    list_display = ('id','experince_type','createdDate','modifiedDate')
    list_display_links = ('id','experince_type')

class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id','user_account_id','email','createdDate','modifiedDate')
    list_display_links = ('id','user_account_id')

class ApplyAdmin(admin.ModelAdmin):
    list_display = ('user_account_id','job_post_id','apply_date','createdDate','modifiedDate')
    list_display_links = ('user_account_id','job_post_id')

class recserviceAdmin(admin.ModelAdmin):
    list_display = ('id','user_account_id','name','email','message','createdDate','modifiedDate')
    list_display_links = ('id','user_account_id')

class galleryAdmin(admin.ModelAdmin):
    list_display = ('id','user_account_id','image','title','createdDate','modifiedDate')
    list_display_links = ('id','user_account_id')

admin.site.register(user_type,UserTypeAdmin)
admin.site.register(user_account, UserAccountAdmin)
admin.site.register(user_log, UserLogAdmin)
admin.site.register(business_stream, BusinessStreamAdmin)
admin.site.register(company, CompanyAdmin)
# admin.site.register(company_image, CompanyImageAdmin)
admin.site.register(education_detail, EducationDetailAdmin)
admin.site.register(experience_detail, ExperinceDetailAdmin)
admin.site.register(seeker_profile, SeekerProfileAdmin)
admin.site.register(seeker_skill_set, SeekerSkillSetAdmin)
admin.site.register(skill_set, SkillSetAdmin)
admin.site.register(job_post, JobPostAdmin)
admin.site.register(job_post_activity, JobPostActivityAdmin)
admin.site.register(job_type, JobTypeAdmin)
admin.site.register(job_location, JobLocationAdmin)
admin.site.register(job_post_skill_set, JobPostSkillSet)
admin.site.register(trending_news, TrendingNewsAdmin)
admin.site.register(contact_us, ContactUs)
admin.site.register(experince_type, ExperinceTypeAdmin)
admin.site.register(subscribe, SubscribeAdmin)
admin.site.register(recservice, recserviceAdmin)
admin.site.register(gallery, galleryAdmin)