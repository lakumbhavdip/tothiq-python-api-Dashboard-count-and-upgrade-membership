from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from business_admin.models import business_info,business_department
from masterapp.models import nationality_type,language,packages
from super_admin_app.models import GeneralNotification

class Users(AbstractBaseUser, PermissionsMixin):
    civil_id = models.CharField(max_length=12, validators=[MinLengthValidator(12)],null=True)
    company_name = models.CharField(max_length=200,null=True)
    email = models.EmailField(
        verbose_name='Email',
        max_length=200,
        unique=True
    )
    full_name = models.CharField(max_length=200,null=True)
    full_name_arabic = models.CharField(max_length=200,null=True)
    phone_number = models.CharField(max_length=12,null=True)
    address_type = models.CharField(max_length=100,default="",null=True)
    address_type_arabic = models.CharField(max_length=100,default="",null=True)
    nationality = models.ForeignKey(nationality_type, on_delete=models.CASCADE,null=True,default=2)
    language = models.ForeignKey(language, on_delete=models.CASCADE,null=True,default=1)
    email_verified_at = models.DateTimeField(default=timezone.now,null=True)
    date_of_birth = models.DateField(null=True)
    GENDER_TYPES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other','Other')
    )
    gender = models.CharField(max_length=6,choices=GENDER_TYPES,null=True)
    # GENDER_TYPES_ARABIC = (
    #     ('Male', 'Male'),
    #     ('Female', 'Female'),
    #     ('Other','Other')
    # )
    gender_arabic = models.CharField(max_length=20,null=True)    
    password = models.TextField(null=True)
    
    area = models.CharField(max_length=200,default="",blank=True,null=True)
    area_arabic = models.CharField(max_length=200,default="",blank=True,null=True)
    block = models.CharField(max_length=200,default="",blank=True,null=True)
    block_arabic = models.CharField(max_length=200,default="",blank=True,null=True)
    street_name_number = models.CharField(max_length=200,default="",blank=True,null=True)
    street_name_number_arabic = models.CharField(max_length=200,default="",blank=True,null=True)
    house_number = models.CharField(max_length=200,default="",blank=True,null=True)
    house_number_arabic = models.CharField(max_length=200,default="",blank=True,null=True)
    floor = models.CharField(max_length=200,default="",blank=True,null=True)
    floor_arabic = models.CharField(max_length=200,default="",blank=True,null=True)
    apartment_number = models.CharField(max_length=200,default="",blank=True,null=True)
    apartment_number_arabic = models.CharField(max_length=200,default="",blank=True,null=True)
     
     
    USER_TYPE_CHOICES = [
        ('individual_user', 'Individual User'),
        ('business_user', 'Business User'),
        ('business_admin', 'Business Admin')
    ]
    user_type = models.CharField(max_length=255, choices=USER_TYPE_CHOICES,null=True)
    ACCOUNT_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('business', 'Business')
    ]
    account_type = models.CharField(max_length=255, choices=ACCOUNT_TYPE_CHOICES,null=True)
    MEMBERSHIP_TYPE_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium')
    ]
    membership_type = models.CharField(max_length=50,choices=MEMBERSHIP_TYPE_CHOICES,null=True,default='Free')
    membership_expiry_date = models.DateTimeField(null=True)
    business = models.ForeignKey(business_info, on_delete=models.CASCADE,null=True)
    department = models.ForeignKey(business_department,on_delete=models.CASCADE,null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    signature_image = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True,null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True,null=True)
    
    created_at = models.DateTimeField(null=True,default=timezone.now)
    updated_at = models.DateTimeField(null=True,default=timezone.now)
    deleted_at = models.DateTimeField(null=True,default=timezone.now)
    last_login = models.DateTimeField(null=True)
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='users')
    
    new_comment_enabled = models.BooleanField(default=False,null=True)
    status_change_enabled = models.BooleanField(default=False,null=True)
    membership_expiration_enabled = models.BooleanField(default=False,null=True)
    user_addon_enabled = models.BooleanField(default=False,null=True)
    contract_deletion_enabled = models.BooleanField(default=False,null=True)
    contract_review_enabled = models.BooleanField(default=False,null=True)
    contract_signature_enabled = models.BooleanField(default=False,null=True)
    contract_canceled_enabled = models.BooleanField(default=False,null=True)
    new_draft_contract_enabled = models.BooleanField(default=False,null=True)
    chat_sound_enabled = models.BooleanField(default=False,null=True)
    chat_highlight_enabled = models.BooleanField(default=False,null=True)
    reminder_push_enabled = models.BooleanField(default=False,null=True)
    reminder_email_enabled = models.BooleanField(default=False,null=True)
    
    ACTIVE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked'),
        ('deleted', 'Deleted'),
    ]
    active_status = models.CharField(
        max_length=255,
        choices=ACTIVE_STATUS_CHOICES,
        default='inactive',null=True
    )
    udid = models.CharField(max_length=500,null=True,blank=True)
    device_type = models.CharField(max_length=500,null=True,blank=True)
    firebase_token = models.CharField(max_length=500,null=True,blank=True)
    view_read = models.BooleanField(default=False,null=True)
    review_comment = models.BooleanField(default=False,null=True)
    invite_users = models.BooleanField(default=False,null=True)
    sign_contract = models.BooleanField(default=False,null=True)
    upload_document = models.BooleanField(default=False,null=True)
    contract_report = models.BooleanField(default=False,null=True)
    financial_report = models.BooleanField(default=False,null=True)
    super_user_full_access = models.BooleanField(default=False,null=True)
    hawati_verification = models.BooleanField(default=False)
    membership_expiry_date = models.DateTimeField(null=True)

    # Add a field to store the sequential ID
    tothiq_id = models.PositiveIntegerField(unique=True,null=True)
    def save(self, *args, **kwargs):
        if not self.tothiq_id:
            # Get the maximum tothiq_id value and increment it by 1
            max_id = Users.objects.aggregate(models.Max('tothiq_id'))['tothiq_id__max']
            if max_id is not None:
                self.tothiq_id = max_id + 1
            else:
                # Start with 101
                self.tothiq_id = 101

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.tothiq_id)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['civil_id']

    # objects = UsersManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'

    
    
    

from contracts.models import contracts

# #Notification setting for user 
class notification(models.Model):
    NOTIFICATION_TYPES = (
        ('new_comment', 'Get notification for new comments.'),
        ('status_change', 'Get notification for status changes.'),
        ('membership_expiration', 'Get notification for membership expriration.'),
        ('user_addition', 'Get notification for users add on.'),
        ('contract_deletion', 'Get Notification on deleting contract.'),
        ('contract_review', 'Get notification on reviewed contract.'),
        ('contract_signature', 'Get notification on signature.'),
        ('contract_cancellation', 'Get notification on cancted contract.'),
        ('new_draft_contract', 'Get notification on new or draft contract.')
    )

    notification_type = models.CharField(max_length=100, choices=NOTIFICATION_TYPES, default='',null=True)
    title = models.CharField(max_length=100)
    title_arabic = models.CharField(max_length=100,null=True)
    description = models.TextField()
    description_arabic = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, db_column='user_id')
    general_notification_id = models.ForeignKey(GeneralNotification, on_delete=models.CASCADE, null=True, blank=True, db_column='general_notification_id')
    contract = models.ForeignKey(contracts, on_delete=models.CASCADE, null=True, blank=True, related_name='contract_id')
    read = models.BooleanField(default=False)
    pin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'notification'
        
        
class user_firebase_token(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, db_column='user_id')
    firebase_token = models.CharField(max_length=500,null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now,null=True)
    updated_at = models.DateTimeField(default=timezone.now,null=True)
    class Meta:
        db_table = 'user_firebase_token'