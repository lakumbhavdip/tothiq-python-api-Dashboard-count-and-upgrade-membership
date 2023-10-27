from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token


# Create your models here.
class business_info(models.Model):
  id = models.AutoField(primary_key=True)  # Add this field
  user = models.ForeignKey('user.Users', on_delete=models.CASCADE,null=True)
  business_name = models.CharField(max_length=500,blank=True,null=True)
  business_name_arabic = models.CharField(max_length=500,blank=True,null=True)
  business_email_address = models.CharField(max_length=500,blank=True)
  business_contact_number = models.CharField(blank=True,null=True,max_length=15)
  extension_number = models.IntegerField(blank=True,null=True)
  area  = models.CharField(max_length=500,null=True)
  block = models.CharField(max_length=500,null=True)
  street_name_number = models.CharField(max_length=500,null=True)
  building_name_number = models.CharField(max_length=500,null=True)
  office_number = models.CharField(max_length=500,null=True)
  area_arabic = models.CharField(max_length=500,null=True)
  block_arabic = models.CharField(max_length=500,null=True)
  street_name_arabic = models.CharField(max_length=500,null=True)
  building_name_arabic = models.CharField(max_length=500,null=True)
  office_number_arabic = models.CharField(max_length=500,null=True)
  licence_expiry_date = models.DateField(blank=True,null=True)
  authorized_signatory_expiry_date = models.DateField(blank=True,null=True)
  licence_image = models.CharField(max_length=500,blank=True,null=True)
  authorized_signatory_image = models.CharField(max_length=500,blank=True,null=True)
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
  password = models.CharField(max_length=500,null=True)
  token = models.CharField(max_length=500,null=True)
  profile_picture = models.CharField(max_length=500,null=True)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)
  deleted_at = models.DateTimeField(default=timezone.now)
  class Meta:
      db_table = 'business_info'
  
  
  
  
class business_admin_token(models.Model):
  business = models.ForeignKey(business_info, on_delete=models.CASCADE,null=True)
  token = models.CharField(max_length=500,null=True)
  class Meta:
      db_table = 'business_admin_token'
  
  
class business_department(models.Model):
  id = models.AutoField(primary_key=True)  # Add this field
  parent_department_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', db_column='parent_id')
  business = models.ForeignKey(business_info, on_delete=models.CASCADE, null=True, related_name='departments')
  department_name = models.CharField(max_length=500)
  created_at = models.DateTimeField(default=timezone.now)
  deleted_at = models.DateTimeField(default=timezone.now)
  ACTIVE_STATUS_CHOICES = [
          ('active', 'Active'),
          ('inactive', 'Inactive'),
          ('blocked', 'Blocked'),
          ('deleted', 'Deleted'),
      ]
  active_status = models.CharField(max_length=100,choices=ACTIVE_STATUS_CHOICES,null=True)
  class Meta:
    db_table = 'business_department'