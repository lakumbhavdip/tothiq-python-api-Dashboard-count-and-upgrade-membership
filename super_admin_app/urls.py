from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required

app_name = 'superadminapp'

urlpatterns = [
    
    path('', views.login, name='login'),
    path('temp_update/<int:templateid>/', views.template_update, name='Template_Update'),
    path('template_create_second/<int:templateid>/', views.template_create_second, name='Template_Create_Second'),
    path('home/', views.home, name='home'),
    path('template/', views.template_view, name='Template'),
    path('category/', views.category_view, name='Category'),
    path('template_create/', views.template_create, name='Template_Create'),
    path('template_create_membership/', views.template_create_membership, name='Template_Create_Membership'),
    path('template_create_category/', views.template_create_category, name='Template_Create_Category'), #category create 
    path('update/',views.update_category, name='update_category'), #Update category
    path('user', views.user, name='User'), #User 
    path('invite_user', views.invite_user, name='invite_user'), #User add
    path('validate_Email/', views.validate_Email, name='validate_Email'),
    path('invite_business',views.invite_business,name='invite_business'),    
    path('user_individual_user_details/<int:uid>/', views.user_individual_user_details, name='User_Individual_User_Details'),
    path('user_individual_add_contracts', views.user_individual_add_contracts, name='User_Individual_Add_Contracts'),
    path('user_individual_custom_package', views.user_individual_custom_package, name='User_Individual_Custom_Package'),
    path('user_individual_upgrade_membership/', views.user_individual_upgrade_membership, name='User_Individual_Upgrade_Membership'),
    path('user_business_user_details/<int:id>/', views.user_business_user_details, name='User_Business_User_Details'),    
    path('user_business_admin_details/<int:id>/', views.user_business_admin_details, name='User_Business_admin_Details'),
    
    path('business_admin_custom_package', views.business_admin_custom_package, name='Business_Admin_Custom_Package'),
    path('business_admin_user_custom_package', views.business_admin_user_custom_package, name='Business_Admin_User_Custom_Package'),

    path('membarship/', views.membership, name='Membership'),
    path('update_memb/',views.update_membarship, name='update_membarship'), #Update membarship
    path('notification_bell/', views.notification_bell, name='Notification_Bell'),
    path('label_management', views.label, name='Label_Management'),    
    # path('label/update/<int:label_id>/', views.update_label, name='update_label'),
    path('update_label/',views.update_label, name='Update_Label'), #Update Label

    path('coupon_management/', views.coupon_management, name='Coupon_Management'),
    path('coupon_management_details/', views.coupon_management_details, name='Coupon_Management_Details'),
    path('coupon/update/',views.update_coupon, name= "update_cupen"),    
    path('setting/', views.setting, name='Setting'),
    path('user_report/', views.user_report, name='User_Report'),
    path('finance_reports/', views.finance_reports, name='finance_reports'),    
    path('maintenance_mode_setting/', views.maintenance_mode_setting, name='Maintenance_Mode_Setting'),
    path('application_setting/', views.application_setting, name='Application_Setting'),
    path('company_setting_setting/', views.company_setting_setting, name='Company_Setting'),
    path('my_fatoorah_payment_gateway_setting/', views.my_fatoorah_payment_gateway_setting, name='My_Fatoorah_Payment_Gateway_Setting'),
    path('smtp_fcm_setting/', views.smtp_fcm_setting, name='Smtp_Fcm_Setting'),
    path('paci_authantication/', views.paci_authantication, name='Paci Authantication'),
    path('contract_user_price_setting/', views.contract_user_price_setting, name='Contract_User_price_Setting'),
    path('payment_gateway_setting/', views.payment_gateway_setting, name='Payment_Gateway_Setting'),
    path('email_template/', views.email_template_setting, name='Email_Template'),
    # path('create_email_template/', views.create_email_template_setting, name='Create_Email_Template'),
    path('update_email_template/<int:emailtempid>/', views.update_email_template_setting, name='Update_Email_Template'),
    path('tothiq_user/', views.tothiq_admin_user, name='Tothiq_User'),
    path('creat_tothiq_user/',views.creat_tothiq_user, name='creat_tothiq_user'),
    path('validate_Email_super_user/',views.validate_Email_super_user, name='validate Email super user'),
    path('validate_Email_super_user_update/',views.validate_Email_super_user_update, name='validate Email super user Update'),
    path('verify_email/<str:slug>',views.verify_email,name='verify'),
    path('tothiq_user_update/',views.update_tothiq_user,name='tothiq_user_update'),
    path('profile/update/',views.profile_update, name= "profile_update"),
    path('passwor/update',views.update_password, name= "update_password"),
    path('validate_password/', views.validate_password, name='validate_password'),
    path('general_notifications/', views.general_notifications, name='General Notifications'),    
    path('create_notifications/', views.create_general_notifications, name='create_notifications'),    
    path('update_notifications/', views.update_general_notifications, name='update_notifications'),    
    path('user_activity_logs/',views.activity_logs,name='user_activity_logs'),
    path('block_user/',views.block_unblock_user, name='block_user'),
    path('block_business/',views.block_unblock_business, name='block_business'),
    path('active_inactive_business/',views.active_inactive_business, name='active_inactive_business'),
    path('get_notification_template/', views.get_notification_template, name='get_notification_template'),
    path('update_notification_template/<int:id>/', views.update_notification_template, name='update_notification_template'),
    path('logout/', views.logout, name='Logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


