from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),

    path('user_type/',views.usertype.as_view()),

    path('user_save_account/',views.usersaveaccount.as_view()),
    path('user_save_account/<int:pk>/',views.edituseraccount.as_view()),

    path('user_log/',views.userlog.as_view()),

    path('user_login/',views.userlogin.as_view()),
    path('forgot_password/<int:pk>/',views.forgotpassword.as_view()),

    path('business_stream/',views.businessstream.as_view()),

    path('company_save_details/',views.companyadddetails.as_view()),
    path('company_save_image/',views.companysaveimage.as_view()),
    path('company_save_details/<int:pk>/',views.companyprofile.as_view()),

    path('seeker_profile/',views.seekerprofile.as_view()),
    path('seeker_profile/<int:pk>/',views.editseekrprofile.as_view()),
    path('education_detail/',views.educationdetail.as_view()),
    path('experince_detail/',views.experincedetail.as_view()),

    path('seeker_skill_set/',views.seekerskillset.as_view()),

    path('post_job/',views.postjob.as_view()),
    path('post_job/<int:pk>/',views.editjob.as_view()),

    path('jobpostactivity/',views.jobpostactivity.as_view()),
    
    path('job_type/',views.jobtype.as_view()),
    path('jobskillset/',views.skillset.as_view()),

    path('skillset/',views.skills.as_view()),  

    path('job_location/',views.joblocation.as_view()),

    path('trendingnews/',views.trendingnews.as_view()),
    path('trendingnews/<int:pk>/',views.updatenews.as_view()),
]