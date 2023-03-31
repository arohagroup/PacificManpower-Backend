from django.contrib import admin

from spacificmanpower.models import *
# Register your models here.

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_type_name','createdDate', 'modifiedDate')
    list_display_links = ('id', 'user_type_name') # adds links to id and name fields

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('id','user_type_id','email','password','date_of_birth','gender','isactive','contact_number','sms_notification_active',
                'email_notification_active','user_image','registration_date','createdDate','modifiedDate')
    list_display_links = ('id', 'user_type_id') # adds links to id and name fields

# class MyProfileAdmin(admin.ModelAdmin):
#     list_display = ('id','user','profile_image','first_name','last_name','email_address','about_me','languages','location','attached_cv','createdDate','modifiedDate')
#     list_display_links = ('id', 'profile_image') # adds links to id and name fields

# class PostJobAdmin(admin.ModelAdmin):
#     list_display = ('id','job_title','job_description','email_address','phone_number','categories','job_type','designation','salary','job_skills',
#                     'job_title','application_deadline_date','country','city','zip_code','createdDate','modifiedDate')
#     list_display_links = ('id', 'job_title') # adds links to id and name fields

admin.site.register(user_type,UserTypeAdmin)
admin.site.register(user_account, UserAccountAdmin)

