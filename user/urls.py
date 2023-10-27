from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    UserRegisterViewAPIView, UserProfileUpdateAPIView,
    userloginviewAPIView,UserProfileAPIView,UserCreatePasswordView,ImageUploadView,UserProfileViewAPIView,UpdateNotificationAPIView,NotificationAPIView,listNotificationAPIView,NotificationDeleteAPIView,ChangeNotificationStatus,UserLogoutAPIView,listNotificationAPIViewWEB,DashboardAPIView,SwitchUsersAPIView,SwitchAccountUserLoginViewAPIView,SigntureImageUploadView,DashboardAPIViewAPP
)

urlpatterns = [
    # path('type', UserViewSet.as_view(), name='users-type'),
    path('register', UserRegisterViewAPIView.as_view()),
    path('login', userloginviewAPIView.as_view()),
    path('profile-update', UserProfileUpdateAPIView.as_view()),
    path('profile', UserProfileAPIView.as_view()),
    path('profile_view', UserProfileViewAPIView.as_view()),
    path('password', UserCreatePasswordView.as_view()),
    path('image', ImageUploadView.as_view()),
    path('signature_image', SigntureImageUploadView.as_view()),
    path('notification', NotificationAPIView.as_view()),
    path('notification_update', UpdateNotificationAPIView.as_view()),
    path('notification_list',listNotificationAPIView.as_view()),
    path('notification_list_web',listNotificationAPIViewWEB.as_view()),
    path('notification_status',ChangeNotificationStatus.as_view()),
    path('notification_delete',NotificationDeleteAPIView.as_view()),
    path('logout',UserLogoutAPIView.as_view()),
    path('dashboard',DashboardAPIView.as_view()),
    path('dashboard_listing',DashboardAPIViewAPP.as_view()),
    path('switch_user_details',SwitchUsersAPIView.as_view()),
    path('switch_account_login',SwitchAccountUserLoginViewAPIView.as_view()),
    
]