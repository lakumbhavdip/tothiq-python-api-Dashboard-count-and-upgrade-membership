from django_cron import CronJobBase, Schedule
from pyfcm import FCMNotification
from masterapp.models import GeneralSettings
from super_admin_app.models import GeneralNotification
import re
from django.db.models import Q
from django.core.mail import send_mail
from tothiq.settings import EMAIL_HOST_USER
from user.models import Users, user_firebase_token
import datetime



class Reminder(CronJobBase):
    RUN_EVERY_MINS = 15  # Set the frequency to 1 hour

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'super_admin_app.send_reminder'  # Replace with the actual management command path

    def do(self):
        current_datetime = datetime.now()   
        total_notification = GeneralNotification.objects.filter(push_status = "pending" , schedule_datetime__lt = current_datetime).reverse()[:10]
        setting_obj = GeneralSettings.objects.filter(id = "1").last()


        for notification in total_notification:
            if notification.user_type == "0":   # user_type : all 
                notification.push_status = "in-progress"
                if Q(notification.notifications_type =='email') | Q(notification.notifications_type == 'both'):
                    user_ids = notification.user_ids
                    integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))] # extract int from the list of user_ids
                    for user_id in integers_id:
                        user = Users.objects.filter(id = user_id).last()
                        send_mail(
                            notification.title,
                            notification.message,
                            EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=False,
                        )
                elif Q(notification.notifications_type =='push-notification') | Q(notification.notifications_type == 'both'):
                        push_service = FCMNotification(api_key=setting_obj.fcm_server_key)
                        user_ids = notification.user_ids
                        integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))] # extract int from the list of user_ids
                        for user_id in integers_id: # Send to multiple devices by passing a list of ids.
                            user = user_firebase_token.objects.filter(user_id = user_id)
                            for i in user:
                                registration_id = i.firebase_token
                                message_title = notification.title
                                message_body = notification.message
                                result = push_service.notify_single_device(registration_id=registration_id, 
                                                                                message_title=message_title,
                                                                                message_body=message_body)
                notification.push_status = "sent"
                notification.save()

            elif notification.user_type == "1":  # user_type : Individual User 
                notification.push_status = "in-progress"
                if Q(notification.notifications_type == 'email') | Q(notification.notifications_type == 'both'):
                    user_ids = notification.user_ids
                    integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))] # extract int from the list of user_ids
                    for user_id in integers_id:
                        user = Users.objects.filter(id = user_id).last()
                        send_mail(
                            notification.title,
                            notification.message,
                            EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=False,
                        )

                if Q(notification.notifications_type =='push-notification') | Q(notification.notifications_type == 'both'):
                    push_service = FCMNotification(api_key=setting_obj.fcm_server_key)
                    user_ids = notification.user_ids
                    integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))] # extract int from the list of user_ids
                    print("aaaa", integers_id)
                    for user_id in integers_id:
                            user = user_firebase_token.objects.filter(user_id = user_id)
                            for i in user:
                                registration_id = i.firebase_token
                                message_title = notification.title
                                message_body = notification.message
                                result = push_service.notify_single_device(registration_id=registration_id, 
                                                                                message_title=message_title,
                                                                                message_body=message_body)
                    
                notification.push_status = "sent"
                notification.save()
    

            elif notification.user_type == "2":  # user_type : Business User
                notification.push_status = "in-progress"
                if Q(notification.notifications_type =='email') | Q(notification.notifications_type == 'both'):
                    user_ids = notification.user_ids
                    integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))]
                    for user_id in integers_id:
                        user = Users.objects.filter(id = user_id).last()
                        send_mail(
                            notification.title,
                            notification.message,
                            EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=False,
                        )
                elif Q(notification.notifications_type =='push-notification') | Q(notification.notifications_type == 'both'):
                        push_service = FCMNotification(api_key=setting_obj.fcm_server_key)
                        user_ids = notification.user_ids
                        integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))]
                        for user_id in integers_id:
                            user = user_firebase_token.objects.filter(user_id = user_id)
                            for i in user:
                                registration_id = i.firebase_token
                                message_title = notification.title
                                message_body = notification.message
                                result = push_service.notify_single_device(registration_id=registration_id, 
                                                                                message_title=message_title,
                                                                                message_body=message_body)
                notification.push_status = "sent"
                notification.save()

            elif notification.user_type == "3":  # user_type : Business Admin
                notification.push_status = "in-progress"
                if Q(notification.notifications_type =='email') | Q(notification.notifications_type == 'both'):
                    user_ids = notification.user_ids
                    integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))]
                    for user_id in integers_id:
                        user = Users.objects.filter(id = user_id).last()
                        send_mail(
                            notification.title,
                            notification.message,
                            EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=False,
                        )
                elif Q(notification.notifications_type =='push-notification') | Q(notification.notifications_type == 'both'):
                        push_service = FCMNotification(api_key=setting_obj.fcm_server_key)
                        user_ids = notification.user_ids
                        integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))]
                        for user_id in integers_id:
                            user = user_firebase_token.objects.filter(user_id = user_id)
                            for i in user:
                                registration_id = i.firebase_token
                                message_title = notification.title
                                message_body = notification.message
                                result = push_service.notify_single_device(registration_id=registration_id, 
                                                                                message_title=message_title,
                                                                                message_body=message_body)
                notification.push_status = "sent"
                notification.save()
        pass
