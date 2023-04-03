from django.contrib import admin

from spacificmanpower.models import *
# Register your models here.

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_type_name','createdDate', 'modifiedDate')
    list_display_links = ('id', 'user_type_name') # adds links to id and name fields

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('id','user_type_id','email','password','date_of_birth','gender','isactive','contact_number',
                'email_notification_active','user_image','registration_date','createdDate','modifiedDate')
    list_display_links = ('id', 'user_type_id') # adds links to id and name fields

class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user_account_id','last_login_date','last_job_apply_date','createdDate','modifiedDate')
    list_display_links = ('user_account_id','last_login_date') # adds links to id and name fields


admin.site.register(user_type,UserTypeAdmin)
admin.site.register(user_account, UserAccountAdmin)
admin.site.register(user_log, UserLogAdmin)

