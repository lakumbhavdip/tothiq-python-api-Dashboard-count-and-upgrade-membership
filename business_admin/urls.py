from django.urls import path
from .views import BusinessAdminRegistrationAPIView,CreatePasswordAPIView,GetBusinessInfoDetailView,BusinessAddDepartmentAPIView,ListDepartmentAPIView,LoginAPIView,UpdateBusinessAdminProfileView,AddUserAPI,UserListAPIView,DeleteDepartmentAPI,EditDepartmentAPIView,listNotificationAPIViewWEB,NotificationDeleteAPIView,DepartmentListAPIView,DepartmentDetailAPIView,DepartmentListnameAPIView

urlpatterns = [

    path('register', BusinessAdminRegistrationAPIView.as_view(), name='business_admin_register'),
    path('login', LoginAPIView.as_view(), name='business_admin_login'),
    path('create_password', CreatePasswordAPIView.as_view(), name='business_admin_password'),
    path('business_profile', GetBusinessInfoDetailView.as_view(), name='business_info_details'),
    path('update_business_profile', UpdateBusinessAdminProfileView.as_view(), name='business_info_update'),
    path('add_department', BusinessAddDepartmentAPIView.as_view(), name='business_add_folder'),
    path('department_list', ListDepartmentAPIView.as_view(), name='business_department_list'),
    path('department_name_list', DepartmentListAPIView.as_view(), name='business_department_name_list'),
    path('department_name_list_all', DepartmentListnameAPIView.as_view(), name='business_department_name_list'),
    path('delete_department', DeleteDepartmentAPI.as_view(), name='business_department_delete'),
    path('edit_department', EditDepartmentAPIView.as_view(), name='business_department_delete'),
    path('department_details', DepartmentDetailAPIView.as_view(), name='business_department_delete'),
    path('business_add_user', AddUserAPI.as_view(), name='business_add_user'),
    path('business_user_list', UserListAPIView.as_view(), name='business_user_list'),
    path('notification_list', listNotificationAPIViewWEB.as_view(), name='list_notofication'),
    path('delete_notification', NotificationDeleteAPIView.as_view(), name='delete_notification'),
    # other URL patterns
]
