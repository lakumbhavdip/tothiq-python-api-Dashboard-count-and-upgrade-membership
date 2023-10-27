from django.utils import timezone
from django.db import models

class GeneralNotification(models.Model):
    PUSH_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in-progress', 'In Progress'),
        ('sent', 'Sent'),
        ('cancelled', 'Cancelled'),
    ]
    NOTIFICATION_TYPE_CHOICES = [
        ('both', 'Both'),
        ('email', 'Email'),
        ('push-notification', 'Push Notification'),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    title_arabic = models.CharField(max_length=100, null=True)
    message = models.TextField()
    message_arabic = models.TextField(null=True)
    image = models.ImageField(upload_to='notification_images/', null=True, blank=True)
    user_type = models.CharField(max_length=50)
    user_ids = models.CharField(max_length=255)  # You may consider using ArrayField if using PostgreSQL
    schedule_datetime = models.DateTimeField()
    push_status = models.CharField(max_length=20, choices=PUSH_STATUS_CHOICES, default='pending')
    notifications_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='both')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)


    class Meta:
        db_table = 'general_notification'
        
        
class Email_Template(models.Model):
    ACTIVE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('in-active', 'In Active'),
        ('delete', 'Delete'),
    ]
    id = models.AutoField(primary_key=True)
    email_code = models.CharField(max_length=100)
    email_subject = models.CharField(max_length=100)
    email_subject_arabic = models.CharField(max_length=100, null=True)
    email_content = models.TextField()
    email_content_arabic = models.TextField(null=True)
    active_status = models.CharField(max_length=20, choices=ACTIVE_STATUS_CHOICES, default='active')
    created_at= models.DateTimeField(default=timezone.now,null=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


    class Meta:
        db_table = 'email_template'
        
        
        
