from django.db import models
from user.models import Users
from django.utils import timezone


# Create your models here.

class Addressbook(models.Model):
    id = models.AutoField(primary_key=True)  # Add this field
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    civil_id = models.CharField(max_length=12,null=True)
    email = models.CharField(max_length=100,null=True)
    ACTIVE_STATUS_CHOICES = [
          ('active', 'Active'),
          ('inactive', 'Inactive'),
          ('blocked', 'Blocked'),
          ('deleted', 'Deleted'),
      ]
    active_status = models.CharField(max_length=100,choices=ACTIVE_STATUS_CHOICES,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(default=timezone.now)
    
    
    def __str__(self):
        return f"{self.user} - {self.civil_id}"
    
    class Meta:
        db_table = 'addressbook'
