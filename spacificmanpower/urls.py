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
]