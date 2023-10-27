from django.db import models
from django.utils import timezone
import uuid
import datetime


class setting(models.Model):
  site_title = models.CharField(max_length=200)
  site_sub_title = models.CharField(max_length=200)
  contact_email = models.CharField(max_length=200)
  contact_number = models.CharField(max_length=200)
  address = models.CharField(max_length=200)
  map_link = models.TextField()
  smtp_host = models.CharField(max_length=200)
  smtp_username = models.CharField(max_length=200)
  smtp_password = models.CharField(max_length=200)
  smtp_port = models.CharField(max_length=200)
  smtp_protocol = models.CharField(max_length=200)
  smtp_from = models.CharField(max_length=200)
  maintenance_mode = models.BooleanField(default=False)
  maintenance_message = models.TextField()
  default_package = models.IntegerField()

    
  class Meta:
      db_table = 'setting'
   



class GeneralSettings(models.Model):
    id                                  = models.AutoField(primary_key=True) 
    
    maintenance_enable                  = models.BooleanField(default=False,null=True)
    individual_user                     = models.BooleanField(default=False,null=True)
    business_user                       = models.BooleanField(default=False,null=True)
    business_admin                      = models.BooleanField(default=False,null=True)
    # maintenance_mode_web_panel_image    = models.CharField(max_length=500,null=True)
    maintenance_mode_web_panel_image    = models.ImageField(upload_to='setting_pic',blank=True,null=True)
    maintenance_page_title              = models.CharField(max_length=500,null=True)
    maintenance_page_contain            = models.CharField(max_length=800,null=True)

    production_server_API_end_point     = models.CharField(max_length=800,null=True)
    pre_production_server_API_end_point = models.CharField(max_length=800,null=True)
    test_server_API_end_point           = models.CharField(max_length=800,null=True)
    iphone_application_update           = models.BooleanField(default=False,null=True)
    iphone_update_mandatory             = models.BooleanField(null=True)
    iphone_current_version              = models.CharField(max_length=100,null=True)
    iphone_new_version                  = models.CharField(max_length=100,null=True)
    android_application_update          = models.BooleanField(default=False,null=True)
    android_update_mandatory            = models.BooleanField(default=False,null=True)
    android_current_version             = models.CharField(max_length=100,null=True)
    android_new_version                 = models.CharField(max_length=500,null=True)
    
    web_panel_header_logo               = models.ImageField(upload_to='setting_pic',blank=True,null=True)
    login_page_logo                     = models.ImageField(upload_to='setting_pic',blank=True,null=True)
    webpanel_title_text                 = models.CharField(max_length=500,null=True)
    webPanel_copyright_text             = models.CharField(max_length=500,null=True)
    
    contracts_price = models.DecimalField(max_digits=10, decimal_places=3,null=True)
    users_price = models.DecimalField(max_digits=10, decimal_places=3,null=True)
    myfatoorah_api_url = models.CharField(max_length=500,null=True)
    payment_test_mode = models.BooleanField(null=True)  
    myfatoorah_api_url_key = models.TextField(max_length=1000,null=True)
    smtp_host_name = models.CharField(max_length=250,null=True)
    smtp_port = models.CharField(max_length=500,null=True)
    smtp_username = models.CharField(max_length=500,null=True)
    smtp_password = models.CharField(max_length=500,null=True)
    SMTP_SECURITY = [
        ('tls', 'TLS'),
        ('ssl', 'SSL')
    ]    
    smtp_security = models.CharField(max_length=500,choices=SMTP_SECURITY,null=True)
    smtp_sender_email = models.CharField(max_length=500,null=True)
    fcm_server_key = models.CharField(max_length=500,null=True)
    web_panel_header_logo_arabic = models.ImageField(upload_to='setting_pic',blank=True,null=True)
    login_page_logo_arabic = models.ImageField(upload_to='setting_pic',blank=True,null=True)
    paci_recall_time  = models.IntegerField(null=True)
    paci_expire_time = models.IntegerField(null=True)

    class Meta: 
        db_table = 'general_settings'

# Create your models here.
class languages_label(models.Model):
  code = models.TextField(max_length=100)
  english = models.TextField(max_length=100)
  arabic = models.TextField(max_length=100,null=True)
  class Meta:
      db_table = 'languages_label'




class language(models.Model):
  name= models.CharField(max_length=20)
  class Meta:
    db_table = "language"





class nationality_type(models.Model):
    name = models.CharField(max_length=50)
    name_arabic = models.CharField(max_length=50,null=True)
    
    class Meta:
      db_table = 'nationality'



class packages (models.Model):
  name = models.CharField(max_length=200)
  individual_price = models.IntegerField()
  business_price = models.IntegerField()
  individual_discount = models.IntegerField()
  business_discount = models.ImageField()
  validity = models.IntegerField()
  max_contracts = models.IntegerField()
  max_contacts = models.IntegerField()
  descriptions = models.TextField()
  is_active = models.BooleanField()
  created_date = models.DateTimeField(default=timezone.now)
  
  class Meta:
    db_table = 'packages'


class Membership(models.Model):
    id                      = models.AutoField(primary_key=True)
    user_available          = (('Individual', 'Individual'),('Business', 'Business'),)
    user_type               = models.CharField(max_length=100, choices=user_available, default='Individual')
    membership_name         = models.CharField(max_length=100)
    membership_name_arabic  = models.CharField(max_length=100, null=True)
    membership_amount       = models.DecimalField(max_digits=10, decimal_places=3,null=True)
    discount_type           = models.CharField(max_length=100,null=True)
    discount_rate           = models.IntegerField(null=True)
    discount_price          = models.DecimalField(max_digits=10, decimal_places=3,null=True)
    payment_gateway_kne     = models.BooleanField(default=False,null=True)
    payment_gateway_cb_card = models.BooleanField(default=False,null=True)
    payment_gateway_gp      = models.BooleanField(default=False,null=True)
    payment_gateway_ap      = models.BooleanField(default=False,null=True)
    number_of_contract      = models.IntegerField(null=True)
    number_of_parties       = models.IntegerField(null=True)
    number_of_templates     = models.IntegerField(null=True)
    chat_between_parties    = models.BooleanField(default=False,null=True)
    address_book            = models.BooleanField(default=False,null=True)
    create_blank_contract   = models.BooleanField(default=False,null=True)
    upload_contract         = models.BooleanField(default=False,null=True)
    view_log                = models.BooleanField(default=False,null=True)
    free_contract_storage   = models.BooleanField(default=False,null=True)
    free_sign_up            = models.BooleanField(default=False,null=True)
    private_or_not          = models.BooleanField(default=False,null=True)
    contract_template       = models.BooleanField(default=False,null=True)
    free_template           = models.BooleanField(default=False,null=True)
    basic_template          = models.BooleanField(default=False,null=True)
    premium_template        = models.BooleanField(default=False,null=True)
    day_availability        = models.IntegerField(null=True)
    number_of_user          = models.IntegerField(null=True)  
    collaborative_editing   = models.BooleanField(default=False,null=True)
    revision_history        = models.BooleanField(default=False,null=True)
    updated_at              = models.DateTimeField(default=timezone.now)
    class Meta:
      db_table = 'membership'
      
      
      
      

from django.conf import settings

class UserMembership(models.Model):
    user = models.ForeignKey('user.Users', on_delete=models.CASCADE)
    membership = models.ForeignKey('Membership', on_delete=models.CASCADE,null=True)
    payment_id = models.CharField(max_length=255,null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    discount_type = models.CharField(max_length=100,null=True)
    discount_rate = models.DecimalField(max_digits=5,decimal_places=2,null=True)
    discount_amount = models.DecimalField(max_digits=5,decimal_places=2,null=True)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    coupen_code = models.IntegerField(null=True)
    ACTIVE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]
    active_status = models.CharField(max_length=255,choices=ACTIVE_STATUS_CHOICES,null=True)
    created_at = models.DateTimeField(null=True)
    
    class Meta:
      db_table = 'user_membership'



class contract_histroy (models.Model):
    user = models.ForeignKey('user.Users', on_delete=models.CASCADE,null=True)
    contracts = models.IntegerField(null=True)
    parties = models.IntegerField(null=True)
    users = models.IntegerField(null=True)
    action_type = models.CharField(max_length=100,null=True)
    action_info = models.CharField(max_length=500,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
      db_table = 'contract_history'





class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('user.Users', on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100)
    membership = models.ForeignKey('Membership', on_delete=models.CASCADE,null=True)
    purchase_id = models.IntegerField(null=True)
    contract_buy = models.IntegerField(null=True)
    user_buy = models.IntegerField(null=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=3,null=True)
    discount_type = models.CharField(max_length=100,null=True)
    discount_rate = models.DecimalField(max_digits=10, decimal_places=3,null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=3,null=True)
    net_amount = models.DecimalField(max_digits=10, decimal_places=3,null=True)
    payment_method = models.CharField(max_length=100,null=True)
    payment_status = models.CharField(max_length=100,null=True)
    tr_id = models.CharField(max_length=100,null=True)
    ref_code = models.CharField(max_length=100,null=True)
    auth_code = models.CharField(max_length=100,null=True)
    track_id = models.CharField(max_length=100,null=True)
    payment_id = models.CharField(max_length=100,null=True)
    payment_info = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon_code = models.CharField(max_length=50,null=True)
    tothiq_id = models.CharField(max_length=50, unique=True,null=True)
    invoice_status = models.CharField(max_length=500,null=True)
    invoice_id = models.CharField(max_length=500,null=True)
    invoice_reference = models.CharField(max_length=500,null=True)

    def save(self, *args, **kwargs):
        if not self.tothiq_id:
            # Generate current date in the format YearMonthDay
            ymd = datetime.datetime.now().strftime('%Y%m%d')

            # Generate random alphanumeric strings
            random_str_6chars = uuid.uuid4().hex[:6]
            random_str_3chars = uuid.uuid4().hex[:3]

            # Create the Tothiq ID
            self.tothiq_id = f"T-{ymd}-{random_str_6chars}-{random_str_6chars}-{random_str_3chars}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tothiq_id}"  
    class Meta:
      db_table = 'payment'

    
    
    
class Coupon(models.Model):
    
    id = models.AutoField(primary_key=True)  
    coupon_name = models.CharField(max_length=100,null=True)
    coupon_name_arabic = models.CharField(max_length=100,null=True)
    coupon_code = models.CharField(max_length=50, unique= True,null=True)
    # limited_number_input = models.IntegerField(default= True,null= True) #Additional:
    limited_coupon_per_Customer = models.IntegerField(default=1, null =True)
    ACTIVE_STATUS_TYPE_CHOICES = [
        ('Inactive','inactive'),
        ('Active','active')
    ]
    active_status = models.CharField(max_length=20,choices=ACTIVE_STATUS_TYPE_CHOICES,null = True)
    total_coupons = models.CharField(max_length=20,default='Unlimited', null=True)
    # used = models.PositiveIntegerField(null=True)
    # unused = models.PositiveIntegerField(null=True)
    
    start_datetime = models.DateTimeField(null=True)
    end_datetime = models.DateTimeField(null=True)
    
    action = models.CharField(max_length=100,null= True)
    created_at= models.DateTimeField(default=timezone.now,null=True)
    updated_at = models.DateTimeField(default=timezone.now,null=True)
    deleted_at = models.DateTimeField(default=timezone.now,null=True)
    banner_image = models.ImageField(upload_to='coupon_banners/',null=True)
    
    coupon_details = models.TextField(null=True)   
    coupon_details_arabic = models.TextField(null=True)   
    DISCOUNT_TYPE_CHOICES = [
        ('Fixed Price','fixed_price'),
        ('Percentage','percentage')
    ]
    
    discount_type = models.CharField(max_length=20,choices=DISCOUNT_TYPE_CHOICES,null = True)# Additional
    DISCOUNT_FOR_CHOICES = [
        ('membership', 'Membership'),
        ('contracts', 'Contracts'),
        ('users', 'Users'),
        ('all','All')
    ]    #Additional: 
    discount_for = models.CharField(max_length=100, choices=DISCOUNT_FOR_CHOICES, null= True)
    discount_for_user_type = models.CharField(max_length=50,null=True)
    # value = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    # alert = models.BooleanField(null= True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    selected_users = models.TextField(null = True)
    discount_rate = models.DecimalField(max_digits=5,decimal_places=2,null=True)

    class Meta:
      db_table = 'coupon'
      
      
      
      
class PaymentMethod(models.Model):
    id                                     = models.AutoField(primary_key=True) 
    payment_name                           = models.CharField(max_length=500,null=True)
    payment_status                         = models.BooleanField(null=True)   
    payment_transportal_id                 = models.CharField(max_length=500,null=True)
    payment_transportal_password           = models.CharField(max_length=500,null=True)
    payment_terminal_resource_key          = models.CharField(max_length=500,null=True)
    payment_test_mode                      = models.BooleanField(null=True)   
    class Meta: 
        db_table = 'paymentmethod'
        
        
        
        
        
class tothiq_super_user(models.Model):
      id = models.AutoField(primary_key=True)
      full_name = models.CharField(max_length=200,null=True)
      email = models.EmailField(
          verbose_name='Email',
          max_length=200,
          unique=True
      )
      phone_number = models.CharField(max_length=10,null=True)
      password = models.CharField(max_length=100,null=True)
      # current_password = models.CharField(max_length=100,null=True)
      # new_password = models.CharField(max_length=100,null=True)
      image = models.ImageField(upload_to='media/profile_pic/',null=True)
      create_template = models.BooleanField(default=False,null=True)
      edit_tempalte = models.BooleanField(default=False,null=True)
      assign_custom_package = models.BooleanField(default=False,null=True)
      activate_block_business_users = models.BooleanField(default=False,null=True)
      created_at = models.DateTimeField(default=timezone.now,null=True)
      updated_at = models.DateTimeField(null=True)
      last_login = models.DateTimeField(null=True)
      ACTIVE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked'),
        ('deleted', 'Deleted'),
      ]
      active_status = models.CharField(
        max_length=255,
        choices=ACTIVE_STATUS_CHOICES,
        default='active',null=True
      )
      class Meta:
        db_table = 'tothiq_super_user'
        
        
        
class Activity_logs(models.Model):
  #  user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, db_column='user_id')
   full_name = models.CharField(max_length=200,null=True)
   browser_name = models.CharField(max_length=250,null=True)
   Ip_address =models.CharField(max_length=200,null=True)
   latitude = models.CharField(max_length=200,null=True)
   longitude = models.CharField(max_length=200,null=True)
  #  ACTIVITY_TYPE_CHOICES=[
  #    ('login','Login'),
  #    ('update_profile','Update_profile'),
  #    ('user_create','User_Create'),
  #    ('user_block','User_Block'),
  #    ('')
  #  ]
   activity_Type = models.CharField(max_length=255,null=True)
   created_at = models.DateTimeField(default=timezone.now,null=True)
   class Meta:
        db_table = 'activity_logs'
        
        
        
class countrycurrency(models.Model):
    country_name = models.CharField(max_length=100)
    # currency_code = models.CharField(max_length=3)
    currency_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    class Meta:
      db_table = 'country_currency'



class NotificationTemplates(models.Model):
    ACTIVE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('in-active', 'In Active'),
        ('delete', 'Delete'),
    ]
    id = models.AutoField(primary_key=True)
    notification_code = models.CharField(max_length=100, db_index=True)
    notification_subject = models.CharField(max_length=100, db_index=True)
    notification_subject_arabic = models.CharField(max_length=100,db_index=True, null=True)
    notification_content = models.TextField()
    notification_content_arabic = models.TextField(null=True)
    active_status = models.CharField(max_length=20, choices=ACTIVE_STATUS_CHOICES, default='active')
    created_at= models.DateTimeField(default=timezone.now,null=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'notification_templates'