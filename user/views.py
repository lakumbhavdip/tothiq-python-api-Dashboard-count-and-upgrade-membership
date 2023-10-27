from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Users,notification,business_info,user_firebase_token
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserprofileupdateSerializer, UserProfileSerializer,UserPasswordSerializer,UserProfileviewSerializer,UserNotificationlistSerializer,UserNotificationupdateSerializer,DeleteNotificationSerializer,ListnotificationSerializer,SwitchUsersSerializer,SwitchACLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage
from tothiq import settings
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.contrib.auth.hashers import make_password
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from urllib.parse import urljoin
from urllib.parse import quote
from contracts.models import contracts
from rest_framework.authtoken.models import Token
from contracts.models import Folder
from masterapp.models import Membership,UserMembership,contract_histroy,Payment
from datetime import datetime, timedelta
from utils import get_label_by_code_and_language
from django.utils.html import format_html
from django.contrib.auth.hashers import check_password  # Import the check_password function






# generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


# Individual User register view with civil_id and email
class UserRegisterViewAPIView(APIView):
    def post(self, request):
        civil_id = request.data.get('civil_id')
        email = request.data.get('email')
        password = request.data.get('password')
        user_type = request.data.get('user_type', 'Individual User')  # Set default value to "Individual User"
        membership_type = request.data.get('membership_type', 'Free') # Set default value to "Free"

        if not civil_id:
                    return Response({'status': 400, 'message': get_label_by_code_and_language('civil_id_field_is_required.', request.headers.get('language', 'en'))}, status=status.HTTP_200_OK)
        if not email:
                    return Response({'status': 400, 'message': get_label_by_code_and_language('email_field_is_required.', request.headers.get('language', 'en'))}, status=status.HTTP_200_OK)
                 
        if not password:
            return Response ({'status':400,'message':'password is required.'})

        # Check if a user with the given civil_id already exists
        existing_user_civil_id = Users.objects.filter(civil_id=civil_id).first()
        if existing_user_civil_id:
            if existing_user_civil_id.user_type == user_type:
                return Response({'status': 400, 'message': 'Users with this civil id already exist.'}, status=400)

        serializer = UserRegisterSerializer(data=request.data)
        
        # Additional serializer validation
        if user_type == 'Business User':
            return Response ({'status':400,'message':"Business users cannot register."})

        # Check if a user with the given civil_id already exists using the serializer's logic
        existing_user_civil_id = Users.objects.filter(civil_id=civil_id).first()
        if existing_user_civil_id:
            if existing_user_civil_id.user_type == user_type:
                return Response({'status':400,'message':"Users with this civil id already exist."})
            
        # Check if a user with the given email already exists using the serializer's logic
        existing_user_email = Users.objects.filter(email=email).first()
        if existing_user_email:
            if existing_user_email.user_type == user_type:
                return Response({'status':400,'message':"Users with this email id already exist."})
        
        if serializer.is_valid():       
            user = serializer.save(created_at=timezone.now(), verified_at=timezone.now(), status=True, language=1, user_type=user_type, membership_type=membership_type, active_status='inactive', id=None)

            token, _ = Token.objects.get_or_create(user=user)  # Generate or retrieve the token for the user
            response_data = {
                'status': status.HTTP_200_OK,
                'message': 'Registration successful',
                'user_id': user.id,
                'token': token.key,
                'user_type':user.user_type,
                'membership_type':user.membership_type,
                'civil_id':user.civil_id,
                'email':user.email
            }
            
            # Send email to the user's email address
            email_subject = 'Registration Successful'
            email_body = format_html(
                '<p>Hello {user_email},</p>'
                '<p>Congratulations! You have successfully registered on our Tothiq platform.</p>'
                '<p>Here are the details of your registration:</p>'
                '<ul>'
                '<li><strong>Civil ID:</strong> {user_civil_id}</li>'
                '<li><strong>User Type:</strong> {user_type}</li>'
                '<li><strong>Membership Type:</strong> {membership_type}</li>'
                '</ul>'
                '<p>Kindly fill-up the necessary fields to activate your account and unlock all the exciting features!</p>'
                '<p>If you have any questions or need assistance, please feel free to contact us. Thank you for choosing Tothiq!</p>'
                '<p>Best regards,<br>The Tothiq Team</p>',
                user_email=user.email,
                user_civil_id=user.civil_id,
                user_type=user.user_type,
                membership_type=user.membership_type,
            )
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
            
            
            # Check if a user with the given civil_id and user_type='Business User' exists and Update the status of all existing business users to True
            existing_business_users = Users.objects.filter(civil_id=civil_id, user_type='Business User')
            existing_business_users.update(status=True)
            
            # Create the "general" department for the business
            general_folder = Folder.objects.create(
            user=user,
            folder_name='General',
            folder_name_arabic = 'عام',
            active_status='active',
            created_at=datetime.now()
            )
            # Reset verified_at to blank
            user.verified_at = None
            user.save()
            
            # Fetch membership based on user_type and store its ID in UserMembership
            membership = Membership.objects.filter(user_type=user_type, membership_name=membership_type).first()
            if membership:
                if membership_type == 'free':
                    start_date = datetime.now()
                    end_date = None
                else:
                    day_availability = membership.day_availability or 0
                    start_date = datetime.now()
                    end_date = start_date + timedelta(days=day_availability)
                user_membership = UserMembership(
                    user=user,
                    membership=membership,
                    start_date=start_date,
                    end_date=end_date,
                    total_amount=None,  # Set the appropriate value
                    discount_type=None,  # Set the appropriate value
                    discount_rate=None,  # Set the appropriate value
                    discount_amount=None,  # Set the appropriate value
                    net_amount=None,  # Set the appropriate value
                    coupen_code=None,  # Set the appropriate value
                    active_status='active',
                    created_at=datetime.now()
                )
                user_membership.membership_id = membership.id  # Set the correct membership_id
                user_membership.save()

                # Count the number of contracts for the selected membership and store in contract_history
                contracts_count = membership.number_of_contract
                action_info = membership.membership_name

                contract_histroy.objects.create(
                    user=user,
                    contracts=contracts_count,
                    parties=None, 
                    users=None,  
                    action_type='add',
                    action_info=action_info,
                    created_at=datetime.now()
                )
            
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_200_OK)

from user_agents import parse

# Individual User login
from django.contrib.auth.hashers import check_password  
class userloginviewAPIView(APIView):
    def post(self, request, format=None):
        civil_id = request.data.get('civil_id')
        otp = request.data.get('otp')
        password = request.data.get('password')  # Retrieve password from request body if available
        user_type = request.data.get('user_type', 'Individual User')  # Set default value to "Individual User"

        if not civil_id:
            return Response({'status': 400, 'message': get_label_by_code_and_language('civil_id_field_is_required.', request.headers.get('language', 'en'))}, status=status.HTTP_200_OK)

        if not otp:
            return Response({'status': 400, 'message': 'OTP is required.'}, status=status.HTTP_200_OK)

        try:
            user = Users.objects.get(civil_id=civil_id, user_type=user_type)

            # Check if the user is blocked or deleted
            if user.active_status == 'blocked':
                return Response({'status': 400, 'message': 'Your account is blocked. Kindly contact Tothiq Administration.'}, status=status.HTTP_200_OK)

            if user.active_status == 'deleted':
                return Response({'status': 400, 'message': 'Your account is deleted. Kindly contact Tothiq Administration.'}, status=status.HTTP_200_OK)

            # Check if a password is provided and if it matches the stored password
            if password and not check_password(password, user.password):
                return Response({'status': 400, 'message': 'Incorrect password.'}, status=status.HTTP_200_OK)

            # Delete the existing token
            # Token.objects.filter(user=user).delete()

            # Generate a new token
            token, _ = Token.objects.get_or_create(user=user)

            # Update the last_login field
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

            # Save optional fields if provided
            udid = request.data.get('udid')
            device_type = request.data.get('device_type')
            firebase_token = request.data.get('firebase_token')
            if udid:
                user.udid = udid
            if device_type:
                user.device_type = device_type
            # Check if firebase_token exists and update or create user_firebase_token
            if firebase_token:
                # Retrieve all records for the user
                user_firebase_tokens = user_firebase_token.objects.filter(user=user)

                # Flag to check if the token is found in any record
                token_found = False

                # Iterate through existing records
                for user_firebase_token_obj in user_firebase_tokens:
                    # Check if the retrieved token matches the provided token
                    if user_firebase_token_obj.firebase_token == firebase_token:
                        token_found = True  # Token is found, no need to create a new record
                        break

                # If the token is not found in any record, create a new one
                if not token_found:
                    user_firebase_token.objects.create(user=user, firebase_token=firebase_token)

            user.save()

            # Send email to the user's email address
            email_subject = 'Login Successful'
            email_body = format_html(
                '<p>Hello {user_email},</p>'
                '<p>We are excited to inform you that you have successfully logged in to your Tothiq account.</p>'
                '<p>Here are the details of your login:</p>'
                '<ul>'
                '<li><strong>Civil ID:</strong> {user_civil_id}</li>'
                '<li><strong>User Type:</strong> {user_type}</li>'
                '<li><strong>Membership Type:</strong> {membership_type}</li>'
                '</ul>'
                '<p>If you did not perform this login or suspect any unauthorized activity, please contact our support team immediately.</p>'
                '<p>If you have any questions or need assistance, please feel free to contact us. Thank you for choosing Tothiq!</p>'
                '<p>Best regards,<br>The Tothiq Team</p>',
                user_email=user.email,
                user_civil_id=user.civil_id,
                user_type=user.user_type,
                membership_type=user.membership_type,
            )
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)

            return Response({'status': 200, 'message': 'Login successfully', 'user_id': user.id, 'user_type': user_type, 'token': token.key, 'membership_type': user.membership_type}, status=status.HTTP_200_OK)

        except Users.DoesNotExist:
            return Response({'status': 400, 'message': 'Civil id is not valid.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_200_OK)


# user get profile
class UserProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        language = request.data.get('language', 'English')  # Default to English if not specified
        serializer = self.serializer_class(request.user, context={'request': request, 'language': language})
        data = serializer.data

        # Replace null values with empty strings
        for key, value in data.items():
            if value is None:
                data[key] = ""

        response_data = {
            'status': status.HTTP_200_OK,
            'message': 'Get profile successfully.',
            'data': data,
        }
        return Response(response_data)
    
    
    






# user profile view 
class UserProfileViewAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileviewSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        # serializer = self.serializer_class(request.user, context={'request': request})
        serializer = self.serializer_class(request.user)
        data = {
            'status': status.HTTP_200_OK,
            'message': 'View profile successfully',
            'data': serializer.data
        }
        return Response(data)
    



# Individual User update profile data
# class UserProfileUpdateAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request):
#         user_id = request.data.get('user_id')
#         if not user_id:
#             return Response({'error': 'User ID is missing'}, status=status.HTTP_400_BAD_REQUEST)
#         user = Users.objects.filter(id=int(user_id)).first()
#         if not user:
#             return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
#         if user.id != request.user.id:
#             return Response({'error': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
#         serializer = UserprofileupdateSerializer(user, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             user.updated_at = timezone.now()
#             user.save(update_fields=['updated_at'])
#             return Response({'status':status.HTTP_200_OK,'message': 'Update profile successfully','data':serializer.data},status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404
class UserProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserprofileupdateSerializer(instance=user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user

        serializer = UserprofileupdateSerializer(instance=user, data=request.data, context={'request': request})
        if serializer.is_valid():
            updated_user = serializer.save()
            updated_user.verified_at = timezone.now()
            updated_user.active_status = "active"  # Set active_status to "active"
            updated_user.updated_at = timezone.now()
            updated_user.save(update_fields=['verified_at', 'updated_at', 'active_status'])

            # Check if the current user's civil_id exists in the Users table with user_type='Business User'
            existing_business_users = Users.objects.filter(civil_id=user.civil_id, user_type='Business User').exclude(id=user.id)

            # Update all other fields provided in the request body for each existing business user
            for existing_business_user in existing_business_users:
                for key, value in serializer.validated_data.items():
                    setattr(existing_business_user, key, value)
                existing_business_user.verified_at = timezone.now()
                existing_business_user.active_status = "active"  # Set active_status to "active"
                existing_business_user.updated_at = timezone.now()
                existing_business_user.save()

            # Get the updated instance with the updated image URL
            updated_serializer = UserprofileupdateSerializer(instance=updated_user, context={'request': request})
            response_data = updated_serializer.data

            # Check if 'image' key exists in response_data
            if 'image' in response_data:
                response_data['image'] = self._get_full_image_url(request, response_data['image'])
                
            # Send email to notify the user of the profile update
            email_subject = 'Profile Updated Successfully'
            email_body = format_html(
                '<p>Hello {user_full_name},</p>'
                '<p>Your Tothiq account profile has been successfully updated.</p>'
                '<p>If you have any questions or need further assistance, please feel free to contact us. Thank you for choosing Tothiq!</p>'
                '<p>Best regards,<br>The Tothiq Team</p>',
                user_full_name=f"{user.full_name}",
            )
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)

            return Response({'status': status.HTTP_200_OK, 'message': 'Update profile successfully', 'data': response_data}, status=status.HTTP_200_OK)

        error_messages = []
        for field, errors in serializer.errors.items():
            error_messages.append({'field': field, 'message': errors[0]})

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{error_messages[0]['field']} {error_messages[0]['message']}"}, status=status.HTTP_200_OK)

    def _get_full_image_url(self, request, image_path):
        base_url = request.build_absolute_uri('/')[:-1]
        return urljoin(base_url, urljoin('/media/', image_path.lstrip('/')))







# user create passowrd 
class UserCreatePasswordView(generics.CreateAPIView):
    serializer_class = UserPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Hash the password before storing it in the database
            hashed_password = make_password(serializer.validated_data['password'])

            # Update the currently logged in user's password field with the hashed password
            user = request.user
            user.password = hashed_password
            user.save()

            return Response({'status':status.HTTP_200_OK,"message": "Password created successfully"}, status=status.HTTP_200_OK)
        else:
            # Get the error message and return the custom response
            error_message = list(serializer.errors.values())[0][0]
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': error_message}, status=status.HTTP_200_OK)
    
    
    

    
# user image upload view
from rest_framework.parsers import MultiPartParser, FormParser
import os
from django.conf import settings

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if 'image' not in request.data:
            return Response({'status':200 ,'message': 'No image data'}, status=status.HTTP_200_OK)
        
        image = request.data['image']
        image_name = f"tothiq_pic/{image.name}"
        
        file_path = os.path.join(settings.MEDIA_ROOT, image_name)
        with open(file_path, 'wb') as file:
            file.write(image.read())
        
        request.user.image = image_name
        request.user.save()

        image_url = request.build_absolute_uri(settings.MEDIA_URL + image_name)
        response_data = {
            'status': status.HTTP_200_OK,
            'message': 'Image uploaded successfully',
            'data': {
                'image': image_url
            }
        }   
        response = Response(response_data, status=status.HTTP_200_OK)
        response['content-type'] = 'multipart/form-data'  # Set the content-type header
        
        return response
    
    

class SigntureImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if 'signature_image' not in request.data:
            return Response({'status': 400, 'message': 'No signature image data'}, status=status.HTTP_400_BAD_REQUEST)

        signature_image = request.data['signature_image']
        image_name = f"signature_image/{signature_image.name}"

        file_path = os.path.join(settings.MEDIA_ROOT, image_name)
        with open(file_path, 'wb') as file:
            file.write(signature_image.read())

        request.user.signature_image = image_name
        request.user.save()

        image_url = request.build_absolute_uri(settings.MEDIA_URL + image_name)
        response_data = {
            'status': status.HTTP_200_OK,
            'message': 'Signature image uploaded successfully',
            'data': {
                'signature_image': image_url
            }
        }
        response = Response(response_data, status=status.HTTP_200_OK)
        response['content-type'] = 'multipart/form-data'  # Set the content-type header

        return response










# User notification APIView     
class NotificationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Assuming you have authentication configured properly
        try:
            notification = Users.objects.get(id=user.id)  # Retrieve the user by their ID
            serializer = UserNotificationlistSerializer(notification)
            return Response({
                'status': 200,
                'message': 'Notifications list retrieved successfully.',
                'data': serializer.data
            })
        except Users.DoesNotExist:
            return Response({
                'success': 400,
                'message': 'No notifications found for the user.',
                'data': {}
            })
            
            
            
            
            
            
#update user notification

class UpdateNotificationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user  # Assuming you have authentication configured properly
        try:
            notification = Users.objects.get(email=user.email)  # Retrieve the user by their email
            serializer = UserNotificationupdateSerializer(notification, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 200,
                    'message': 'Notifications updated successfully.',
                    'data': serializer.data
                })
            else:
                return Response({
                    'status': 400,
                    'message': 'Invalid data.',
                    'data': serializer.errors
                })
        except Users.DoesNotExist:
            return Response({
                'status': 400,
                'message': 'No notifications found for the user.',
                'data': {}
            })
            
            
            
            
#list notification (mobile API)
from datetime import datetime

class listNotificationAPIView(generics.ListAPIView):
    serializer_class = ListnotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = notification.objects.filter(user=user, is_active=True)

        text = self.request.data.get('text')
        if text:
            queryset = queryset.filter(title__icontains=text)

        return queryset

    def post(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Get the language parameter from the request data (default to English)
        language = request.data.get('language', 'English')
        
        # Define the Pin label based on the language
        pin_label = 'Pin' if language == 'English' else 'دبوس'

        notifications_by_day = {}
        pinned_notifications = []

        for notification in queryset:
            notification_day = notification.created_at.date()
            if notification.pin:
                pinned_notifications.append(self.serialize_notification(notification, language))
            else:
                if notification_day not in notifications_by_day:
                    notifications_by_day[notification_day] = []
                notifications_by_day[notification_day].append(self.serialize_notification(notification, language))

        serialized_data = []
        if pinned_notifications:
            serialized_data.append({
                'notification_day': pin_label,  # Use the Pin label based on language
                'list': pinned_notifications
            })

        for notification_day, notification_list in notifications_by_day.items():
            serialized_data.append({
                'notification_day': notification_day.strftime("%Y-%m-%d"),
                'list': notification_list
            })

        response_data = {
            'status': '200',
            'message': 'Notifications retrieved successfully.',
            'data': serialized_data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def serialize_notification(self, notification, language):
        # Define the fields to use based on the language
        if language == 'Arabic':
            title_field = 'title_arabic'
            description_field = 'description_arabic'
        else:
            title_field = 'title'
            description_field = 'description'

        # Create a dictionary with the serialized notification
        serialized_notification = {
            'id': notification.id,
            'notification_type': notification.notification_type,
            'title': getattr(notification, title_field),
            'description': getattr(notification, description_field),
            'created_at': notification.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'read': notification.read,
            'pin': notification.pin,
            'contract': notification.contract,
        }

        return serialized_notification







#list notification (Web API)
class listNotificationAPIViewWEB(APIView):
    serializer_class = ListnotificationSerializer
    permission_classes = [IsAuthenticated]  # Add authentication permission

    def post(self, request):
        user = request.user  # Get the currently logged-in user
        text = request.data.get('text', None)  # Get the 'text' parameter from the request body
        language = request.data.get('language', 'English')  # Default to 'English' if not specified

        
        queryset = notification.objects.filter(user=user, is_active=True)  # Filter by user and is_active=True
        
        if text:
            queryset = queryset.filter(title__icontains=text)
        
        serialized_data = []
        
        for Notification in queryset:
            serialized_notification = self.serialize_notification(Notification, language)
            serialized_data.append(serialized_notification)
        
        response_data = {
            'status': '200',
            'message': 'Notifications retrieved successfully.',
            'data': serialized_data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def serialize_notification(self, notification, language):
        # Define the fields to use based on the language
        if language == 'Arabic':
            title_field = 'title_arabic'
            description_field = 'description_arabic'
        else:
            title_field = 'title'
            description_field = 'description'

        # Create a dictionary with the serialized notification
        serialized_notification = {
            'id': notification.id,
            'notification_type': notification.notification_type,
            'title': getattr(notification, title_field),
            'description': getattr(notification, description_field),
            'created_at': notification.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'read': notification.read,
            'pin': notification.pin,
            'contract': notification.contract,
        }

        return serialized_notification









# chnage the notification status 
class ChangeNotificationStatus(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        notification_id = request.data.get('notification_id')
        status = request.data.get('status')
        pin = request.data.get('pin')
        user_id = request.user.id  # Assuming you have implemented authentication

        if notification_id is None:
            return Response({"status": 400, "message": "Notification id is required."})
        if status is None:
            return Response({"status": 400, "message": "Status is required."})
        if status not in [True, False]:
            return Response({"status": 400, "message": "Invalid input for status."})

        try:
            # Retrieve the notification from the database
            notification_obj = notification.objects.get(id=notification_id, user_id=user_id)

            # Update the 'read' field based on the status parameter
            notification_obj.read = status

            # Update the 'pin' field based on the pin parameter
            if pin is not None:
                notification_obj.pin = pin

            notification_obj.save()

            return Response({"status": 200, "message": "Notification status updated successfully."})
        except notification.DoesNotExist:
            return Response({"status": 400, "message": "Notification does not exist."})



#delete notification API
class NotificationDeleteAPIView(generics.GenericAPIView):
    serializer_class = DeleteNotificationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        notification_id = request.data.get('notification_id')
        if notification_id is None:
            return Response({"status": 400, 'message': 'Please provide notification id'}, status=status.HTTP_200_OK)

        user = request.user
        try:
            instance = notification.objects.get(id=notification_id, user=user)
            if instance.is_active:
                instance.is_active = False
                instance.save()
                return Response({"status": 200, 'message': 'Notification deleted successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({"status": 400, 'message': 'Notification is already deleted.'}, status=status.HTTP_200_OK)
        except notification.DoesNotExist:
            return Response({"status": 400, 'message': 'Notification not found'}, status=status.HTTP_200_OK)
        
         
        
        
        
#logout user (Mobile App)
from rest_framework.authtoken.models import Token
class UserLogoutAPIView(APIView):
    def post(self, request, format=None):
        # Get the user's token from the request headers
        auth_token = request.headers.get('Authorization')
        if not auth_token:
            return Response({'status': 400, 'message': 'Please provide a token in the header'}, status=status.HTTP_200_OK)

        try:
            # Retrieve the user based on the token
            token = auth_token.split(' ')[1]
            user_token = Token.objects.get(key=token)
            user = user_token.user

            # Delete the user's token to log them out
            user_token.delete()

            # Return success response
            return Response({'status': 200, 'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except (IndexError, Token.DoesNotExist):
            return Response({'status': 400, 'message': 'Invalid token'}, status=status.HTTP_200_OK)
            
            
            
    
    
#Dashborad API view (WEB)
from django.db.models import Sum
from masterapp.models import languages_label
class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_label_key(self, title):
        try:
            # Query the languages_label table to fetch objects with the specified title
            label_entries = languages_label.objects.filter(english=title)
            
            # Check if there are any matching entries
            if label_entries.exists():
                # You can choose one of the matching entries here, e.g., the first one
                english_label_entry = label_entries.first()
                return english_label_entry.id
            else:
                # Handle the case where no matching entry is found
                return ""
        except languages_label.DoesNotExist:
            return ""


    def get_notifications(self, user):
        queryset = notification.objects.filter(user=user)
        serializer = ListnotificationSerializer(queryset, many=True)
        return serializer.data


    def get_contract_summary(self, user):
        if user.user_type == 'Business Admin':
            try:
                business_info_entry = business_info.objects.get(user_id=user.id)
                business_id = business_info_entry.id
                business_user_ids = Users.objects.filter(business_id=business_id).values_list('id', flat=True)
                business_user_contracts_data = contracts.objects.filter(user_id__in=business_user_ids)

                status_counts = {
                    'Used': 0,
                    'Draft': 0,
                    'Under Review': 0,
                    'Ready': 0,
                    'Signed': 0,
                    'Rejected': 0,
                    'Deleted': 0,
                    'Cancelled': 0
                }

                for contract in business_user_contracts_data:
                    status = contract.get_status_display()
                    if status in status_counts:
                        status_counts[status] += 1

                # Calculate the "Used" number as the total count of all other statuses
                used_number = sum(status_counts.values()) - status_counts['Used']
                status_counts['Used'] = used_number

                summary_data = []
                for title, count in status_counts.items():
                    label_key = self.get_label_key(title)  # Fetch label_key for the title
                    summary_data.append({'title': title, 'count': str(count), 'label_key': label_key})

                return summary_data
            except business_info.DoesNotExist:
                pass
        else:
            contracts_data = contracts.objects.filter(user=user)
            status_counts = {
                'Used': 0,
                'Draft': 0,
                'Under Review': 0,
                'Ready': 0,
                'Signed': 0,
                'Rejected': 0,
                'Deleted': 0,
                'Cancelled': 0
            }

            for contract in contracts_data:
                status = contract.get_status_display()
                if status in status_counts:
                    status_counts[status] += 1

            # Calculate the "Used" number as the total count of all other statuses
            used_number = sum(status_counts.values()) - status_counts['Used']
            status_counts['Used'] = used_number

            summary_data = []
            for title, count in status_counts.items():
                label_key = self.get_label_key(title)  # Fetch label_key for the title
                summary_data.append({'title': title, 'count': str(count), 'label_key': label_key})

            return summary_data
        



    def get_payment_summary(self, user):
        title = ""
        label_key = self.get_label_key(title)

        # Calculate the total net amount for payments with a payment_type of 'membership'
        membership_net_amount = Payment.objects.filter(payment_type='membership', user=user).aggregate(membership_net_amount=Sum('net_amount'))['membership_net_amount']
        membership_net_amount = membership_net_amount if membership_net_amount is not None else 0

        # Calculate the total net amount for payments with a payment_type of 'contracts'
        contracts_net_amount = Payment.objects.filter(payment_type='contracts', user=user).aggregate(contracts_net_amount=Sum('net_amount'))['contracts_net_amount']
        contracts_net_amount = contracts_net_amount if contracts_net_amount is not None else 0

        total_net_amount = contracts_net_amount + membership_net_amount

        if user.user_type == 'Business Admin':
            # Fetch the net amount for the current user
            user_net_amount = Payment.objects.filter(payment_type='user_net_amount', user=user).aggregate(user_net_amount=Sum('net_amount'))['user_net_amount']
            user_net_amount = user_net_amount if user_net_amount is not None else 0
            total_net_amount += user_net_amount

            # Create the PaymentSummary data with title, count, and label_key
            payment_summary_data = [
                {
                    "title": "Total",
                    "count": total_net_amount,
                    "label_key": self.get_label_key("Total")
                },
                {
                    "title": "Membership",
                    "count": membership_net_amount,
                    "label_key": self.get_label_key("Membership")
                },
                {
                    "title": "Contracts",
                    "count": contracts_net_amount,
                    "label_key": self.get_label_key("Contracts")
                },
                {
                    "title": "Users",  # Additional field for Business Admin
                    "count": user_net_amount,
                    "label_key": self.get_label_key("Users")
                }
            ]
        else:
            # Create the PaymentSummary data without the User Net Amount field
            payment_summary_data = [
                {
                    "title": "Total",
                    "count": total_net_amount,
                    "label_key": self.get_label_key("Total")
                },
                {
                    "title": "Membership",
                    "count": membership_net_amount,
                    "label_key": self.get_label_key("Membership")
                },
                {
                    "title": "Contracts",
                    "count": contracts_net_amount,
                    "label_key": self.get_label_key("Contracts")
                }
            ]

        return payment_summary_data


    def get_contracts_status(self, user):
        if user.user_type == 'Business User':
            try:
                current_user = Users.objects.get(id=user.id)
                business_id = current_user.business_id
                business_user_ids = Users.objects.filter(business_id=business_id).values_list('id', flat=True)
                try:
                    business = business_info.objects.get(id=business_id)
                    business_user_id = business.user_id

                    total_contracts = contract_histroy.objects.filter(user_id=business_user_id).aggregate(total_contracts=Sum('contracts'))['total_contracts']
                    total_contracts = total_contracts if total_contracts is not None else 0
                    user_contracts = contracts.objects.filter(user_id__in=business_user_ids).count()
                    available_contracts = total_contracts - user_contracts
                    used_contracts = user_contracts
                except business_info.DoesNotExist:
                    total_contracts = 0
                    user_contracts = 0
                    available_contracts = 0
                    used_contracts = 0
            except Users.DoesNotExist:
                total_contracts = 0
                user_contracts = 0
                available_contracts = 0
                used_contracts = 0
        elif user.user_type == 'Business Admin':
            try:
                business_info_entry = business_info.objects.get(user_id=user.id)
                business_id = business_info_entry.id
                business_user_ids = Users.objects.filter(business_id=business_id).values_list('id', flat=True)
                business = business_info.objects.get(id=business_id)
                business_user_id = business.user_id
                
                
                total_contracts = contract_histroy.objects.filter(user_id=business_user_id).aggregate(total_contracts=Sum('contracts'))['total_contracts']
                total_contracts = total_contracts if total_contracts is not None else 0
                user_contracts = contracts.objects.filter(user_id__in=business_user_ids).count()
                available_contracts = total_contracts - user_contracts
                used_contracts = user_contracts
            except business_info.DoesNotExist:
                total_contracts = 0
                user_contracts = 0
                available_contracts = 0
                used_contracts = 0
        else:
            total_contracts = contract_histroy.objects.filter(user=user).aggregate(total_contracts=Sum('contracts'))['total_contracts']
            total_contracts = total_contracts if total_contracts is not None else 0
            user_contracts = contracts.objects.filter(user=user).count()
            available_contracts = total_contracts - user_contracts
            used_contracts = user_contracts

        contracts_status_data = [
        {'title': 'Total', 'count': str(total_contracts), 'label_key': self.get_label_key('Total')},
        {'title': 'Used', 'count': str(used_contracts), 'label_key': self.get_label_key('Used')},
        {'title': 'Available', 'count': str(available_contracts), 'label_key': self.get_label_key('Available')}
        ]

        return contracts_status_data

        
        
    def get_usage_percentage(self, user):
        contracts_data_list = self.get_contracts_status(user)

        if contracts_data_list:  # Check if the list is not empty
            total_contracts = None
            used_contracts = None

            for contract_data in contracts_data_list:
                if contract_data['title'] == 'Total':
                    total_contracts = int(contract_data['count'])
                elif contract_data['title'] == 'Used':
                    used_contracts = int(contract_data['count'])

            if total_contracts is not None and used_contracts is not None:
                if total_contracts > 0:
                    usage_percentage = (used_contracts / total_contracts) * 100
                else:
                    usage_percentage = 0.0
            else:
                usage_percentage = 0.0
        else:
            usage_percentage = 0.0

        # Format the usage_percentage with two decimal places
        formatted_usage_percentage = round(usage_percentage, 2)
        return formatted_usage_percentage



    def get(self, request):
        user = request.user  # Get the currently authenticated user

        notifications = self.get_notifications(user)
        contract_summary = self.get_contract_summary(user)
        payment_summary = self.get_payment_summary(user)
        contracts_status = self.get_contracts_status(user)
        usage_percentage = self.get_usage_percentage(user)

        response_data = {
                'Notifications':notifications,
                'ContractsSummary': contract_summary,
                'ContractsStatus': contracts_status,
                'usagepercentage': usage_percentage,
                'PaymentSummary': payment_summary
            }

        return Response({'status': 200, 'message': 'Dashboard data fetched successfully.', 'data': response_data})



#Dashborad API view (APP)
class DashboardAPIViewAPP(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_label_key(self, title):
        try:
            # Query the languages_label table to fetch objects with the specified title
            label_entries = languages_label.objects.filter(english=title)
            
            # Check if there are any matching entries
            if label_entries.exists():
                # You can choose one of the matching entries here, e.g., the first one
                english_label_entry = label_entries.first()
                return english_label_entry.id
            else:
                # Handle the case where no matching entry is found
                return ""
        except languages_label.DoesNotExist:
            return ""


    def get_notifications(self, user):
        queryset = notification.objects.filter(user=user)
        serializer = ListnotificationSerializer(queryset, many=True)
        return serializer.data


    def get_contract_summary(self, user):
        if user.user_type == 'Business Admin':
            try:
                business_info_entry = business_info.objects.get(user_id=user.id)
                business_id = business_info_entry.id
                business_user_ids = Users.objects.filter(business_id=business_id).values_list('id', flat=True)
                business_user_contracts_data = contracts.objects.filter(user_id__in=business_user_ids)

                status_counts = {
                    # 'Used': 0,
                    'Draft': 0,
                    'Review': 0,
                    'Ready': 0,
                    # 'Signed': 0,
                    # 'Rejected': 0,
                    # 'Deleted': 0,
                    # 'Cancelled': 0
                }

                for contract in business_user_contracts_data:
                    status = contract.get_status_display()
                    if status in status_counts:
                        status_counts[status] += 1

                # # Calculate the "Used" number as the total count of all other statuses
                # used_number = sum(status_counts.values()) - status_counts['Used']
                # status_counts['Used'] = used_number

                summary_data = []
                for title, count in status_counts.items():
                    label_key = self.get_label_key(title)  # Fetch label_key for the title
                    summary_data.append({'title': title, 'count': str(count), 'label_key': label_key})

                return summary_data
            except business_info.DoesNotExist:
                pass
        else:
            contracts_data = contracts.objects.filter(user=user)
            status_counts = {
                # 'Used': 0,
                'Draft': 0,
                'Review': 0,
                'Ready': 0,
                # 'Signed': 0,
                # 'Rejected': 0,
                # 'Deleted': 0,
                # 'Cancelled': 0
            }

            for contract in contracts_data:
                status = contract.get_status_display()
                if status in status_counts:
                    status_counts[status] += 1

            # # Calculate the "Used" number as the total count of all other statuses
            # used_number = sum(status_counts.values()) - status_counts['Used']
            # status_counts['Used'] = used_number

            summary_data = []
            for title, count in status_counts.items():
                label_key = self.get_label_key(title)  # Fetch label_key for the title
                summary_data.append({'title': title, 'count': str(count), 'label_key': label_key})

            return summary_data
        



    def get_payment_summary(self, user):
        # Fetch label_key for the 'Payment Summary' title
        title = ""
        label_key = self.get_label_key(title)

        # Create the PaymentSummary data with title, count, and label_key
        payment_summary_data = [
            {
                "title": "Total",
                "count": "28",  # Replace with your count logic
                "label_key": 22
            },
            {
                "title": "Membership",
                "count": "18",  # Replace with your count logic
                "label_key": 460
            },
            {
                "title": "Contracts",
                "count": "10",  # Replace with your count logic
                "label_key": 79
            }
        ]
        return payment_summary_data


    def get_contracts_status(self, user):
        if user.user_type == 'Business User':
            try:
                current_user = Users.objects.get(id=user.id)
                business_id = current_user.business_id
                business_user_ids = Users.objects.filter(business_id=business_id).values_list('id', flat=True)
                try:
                    business = business_info.objects.get(id=business_id)
                    business_user_id = business.user_id

                    total_contracts = contract_histroy.objects.filter(user_id=business_user_id).aggregate(total_contracts=Sum('contracts'))['total_contracts']
                    total_contracts = total_contracts if total_contracts is not None else 0
                    user_contracts = contracts.objects.filter(user_id__in=business_user_ids).count()
                    available_contracts = total_contracts - user_contracts
                    used_contracts = user_contracts
                except business_info.DoesNotExist:
                    total_contracts = 0
                    user_contracts = 0
                    available_contracts = 0
                    used_contracts = 0
            except Users.DoesNotExist:
                total_contracts = 0
                user_contracts = 0
                available_contracts = 0
                used_contracts = 0
        elif user.user_type == 'Business Admin':
            try:
                business_info_entry = business_info.objects.get(user_id=user.id)
                business_id = business_info_entry.id
                business_user_ids = Users.objects.filter(business_id=business_id).values_list('id', flat=True)
                business = business_info.objects.get(id=business_id)
                business_user_id = business.user_id
                
                
                total_contracts = contract_histroy.objects.filter(user_id=business_user_id).aggregate(total_contracts=Sum('contracts'))['total_contracts']
                total_contracts = total_contracts if total_contracts is not None else 0
                user_contracts = contracts.objects.filter(user_id__in=business_user_ids).count()
                available_contracts = total_contracts - user_contracts
                used_contracts = user_contracts
            except business_info.DoesNotExist:
                total_contracts = 0
                user_contracts = 0
                available_contracts = 0
                used_contracts = 0
        else:
            total_contracts = contract_histroy.objects.filter(user=user).aggregate(total_contracts=Sum('contracts'))['total_contracts']
            total_contracts = total_contracts if total_contracts is not None else 0
            user_contracts = contracts.objects.filter(user=user).count()
            available_contracts = total_contracts - user_contracts
            used_contracts = user_contracts

        contracts_status_data = [
        {'title': 'Total', 'count': str(total_contracts), 'label_key': self.get_label_key('Total')},
        {'title': 'Used', 'count': str(used_contracts), 'label_key': self.get_label_key('Used')},
        {'title': 'Available', 'count': str(available_contracts), 'label_key': self.get_label_key('Available')}
        ]

        return contracts_status_data

        
        
    def get_usage_percentage(self, user):
        contracts_data_list = self.get_contracts_status(user)

        if contracts_data_list:  # Check if the list is not empty
            total_contracts = None
            used_contracts = None

            for contract_data in contracts_data_list:
                if contract_data['title'] == 'Total':
                    total_contracts = int(contract_data['count'])
                elif contract_data['title'] == 'Used':
                    used_contracts = int(contract_data['count'])

            if total_contracts is not None and used_contracts is not None:
                if total_contracts > 0:
                    usage_percentage = (used_contracts / total_contracts) * 100
                else:
                    usage_percentage = 0.0
            else:
                usage_percentage = 0.0
        else:
            usage_percentage = 0.0

        # Format the usage_percentage with two decimal places
        formatted_usage_percentage = round(usage_percentage, 2)
        return formatted_usage_percentage



    def get(self, request):
        user = request.user  # Get the currently authenticated user

        notifications = self.get_notifications(user)
        contract_summary = self.get_contract_summary(user)
        payment_summary = self.get_payment_summary(user)
        contracts_status = self.get_contracts_status(user)
        usage_percentage = self.get_usage_percentage(user)

        response_data = {
                'Notifications':notifications,
                'ContractsSummary': contract_summary,
                'ContractsStatus': contracts_status,
                'usagepercentage': usage_percentage,
                'PaymentSummary': payment_summary
            }

        return Response({'status': 200, 'message': 'Dashboard data fetched successfully.', 'data': response_data})





#switch user details view 
class SwitchUsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  # Get the currently authenticated user

        # Get all business user accounts with the given civil_id, excluding the current user
        business_users = Users.objects.filter(civil_id=user.civil_id, user_type='Business User').exclude(id=user.id)

        # Get all individual user accounts with the given civil_id, excluding the current user
        individual_users = Users.objects.filter(civil_id=user.civil_id, user_type='Individual User').exclude(id=user.id)

        # Prepare a list to store the user data
        user_data_list = []

        # Iterate over each business user account
        for account in business_users:
            switch_user_image = Users.objects.get(id=account.id)
            business_info1 = business_info.objects.filter(user_id=switch_user_image.id).first()  # Filter by user_id

            # Check if there is a corresponding BusinessInfo entry for this user
            image = business_info1.profile_picture if business_info1 else ""

            user_data = {
                "user_id": account.id,
                "civil_id": account.civil_id,
                "user_type": account.user_type,
                "company_name": account.company_name,
                "image": image
            }

            # Add the user data to the list
            user_data_list.append(user_data)

        # Iterate over each individual user account
        for account in individual_users:
            user_data = {
                "user_id": account.id,
                "civil_id": account.civil_id,
                "user_type": account.user_type,
                "full_name": account.full_name,
                "image": account.image
            }

            # Add the user data to the list
            user_data_list.append(user_data)

        # Return the user data as a response
        return Response({
            "status": 200,
            "message": "Switch account details fetched successfully.",
            "data": user_data_list
        }, status=status.HTTP_200_OK)

    
    

# switch  login view 
from rest_framework.authtoken.models import Token

class SwitchAccountUserLoginViewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'status': 400, 'message': 'User id is required.'},status=status.HTTP_200_OK)

        serializer = SwitchACLoginSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.data.get('user_id')
            try:
                user = Users.objects.get(id=user_id)
                
                # Check if a token already exists for the user
                token, created = Token.objects.get_or_create(user=user)

                if not created:
                    # Update the existing token
                    # token.delete() 
                    token, _ = Token.objects.get_or_create(user=user)

                # Send email to the user's email address
                email_subject = 'Switch Account Successful'

                if user.user_type == 'Individual User':
                    email_body = (
                        f"<html><body>"
                        f"<p>Hello {user.email},</p>"
                        f"<p>Your Tothiq account (ID: {user.id}) associated with {user.civil_id} has been successfully switched to.</p>"
                        f"<p>If you did not perform this switch, please contact our support team immediately.</p>"
                        f"<p>If you have any questions or need assistance, please feel free to contact us.</p>"
                        f"<p>Thank you for choosing Tothiq!</p>"
                        f"<p>Best regards,<br>The Tothiq Team</p>"
                        f"</body></html>"
                    )
                elif user.user_type == 'Business User':
                    email_body = (
                        f"<html><body>"
                        f"<p>Hello {user.email},</p>"
                        f"<p>Your Tothiq account (ID: {user.id}) associated with {user.company_name} has been successfully switched to.</p>"
                        f"<p>If you did not perform this switch, please contact our support team immediately.</p>"
                        f"<p>If you have any questions or need assistance, please feel free to contact us.</p>"
                        f"<p>Thank you for choosing Tothiq!</p>"
                        f"<p>Best regards,<br>The Tothiq Team</p>"
                        f"</body></html>"
                    )
                else:
                    # Handle other user types here if needed
                    email_body = (
                        f"<html><body>"
                        f"<p>Hello {user.email},</p>"
                        f"<p>Your Tothiq account (ID: {user.id}) has been successfully switched to.</p>"
                        f"<p>If you did not perform this switch, please contact our support team immediately.</p>"
                        f"<p>If you have any questions or need assistance, please feel free to contact us.</p>"
                        f"<p>Thank you for choosing Tothiq!</p>"
                        f"<p>Best regards,<br>The Tothiq Team</p>"
                        f"</body></html>"
                    )
                email = EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)

                return Response({'status': status.HTTP_200_OK, 'message': 'Login successfully', 'token': token.key, 'id': user.id, 'user_type': user.user_type}, status=status.HTTP_200_OK)
            except Users.DoesNotExist:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'User ID is not valid'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)