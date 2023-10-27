from rest_framework import serializers
from .models import Users,language,nationality_type
from django.utils import timezone
from .models import notification
from django.conf import settings
from django.urls import reverse
from urllib.parse import quote
from masterapp.models import Membership,UserMembership,contract_histroy,GeneralSettings
from datetime import timedelta
from contracts.models import contracts
from business_admin.models import business_info
from django.contrib.auth.hashers import make_password  # Import the password hashing function




# Individual User Register view with civil_id and email
# class UserregisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = ('civil_id', 'email')

#     def create(self, validated_data):
#         User = Users.objects.create(
#             civil_id=validated_data['civil_id'],
#             email=validated_data['email'],
#         )
#         User.save()
#         return User
    
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('civil_id', 'email', 'password')  # Include 'password' in the fields

    def create(self, validated_data):
        civil_id = validated_data['civil_id']
        email = validated_data['email']
        user_type = validated_data['user_type']
        password = validated_data['password']  # Get the password from the validated data

        # Hash the password before saving it
        hashed_password = make_password(password)

        user = Users.objects.create(
            civil_id=civil_id,
            email=email,
            user_type=user_type,
            membership_type=validated_data['membership_type'],
            password=hashed_password,  # Save the hashed password
        )
        return user










# user login with civil id
class UserLoginSerializer(serializers.ModelSerializer):
    civil_id = serializers.CharField(max_length=12)
    otp = serializers.CharField(max_length=12)
    firebase_token = serializers.CharField(required=False)
    device_type = serializers.CharField(required=False)
    udid = serializers.CharField(required=False)
    user_type = serializers.CharField(required=False)

    class Meta:
        model = Users
        fields = ('civil_id', 'otp', 'firebase_token', 'device_type', 'udid', 'user_type')

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as error:
            error_detail = []
            for field, errors in error.detail.items():
                field_errors = [f"{field} {error}" for error in errors]
                error_detail.extend(field_errors)
            raise serializers.ValidationError({"status": "400", "message": " ".join(error_detail)})





# user profile serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.request import Request
import urllib.parse
from datetime import datetime, timedelta
from django.db.models import Sum

class UserProfileSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(format='%d/%m/%Y')
    image = serializers.SerializerMethodField()
    signature_image = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = (
            'id', 'tothiq_id','civil_id', 'company_name', 'email', 'full_name','full_name_arabic', 'phone_number',
            'address_type', 'address_type_arabic','nationality', 'language', 'email_verified_at',
            'date_of_birth', 'gender','gender_arabic', 'is_active', 'created_at', 'last_login',
            'area','area_arabic','block', 'block_arabic','street_name_number', 'street_name_number_arabic','house_number','house_number_arabic','floor','floor_arabic','apartment_number', 'apartment_number_arabic','verified_at', 'status', 'active_status','image', 'account_type',
            'user_type', 'membership_type','signature_image'
        )

    def get_image(self, obj):
        if obj.image:
            return self.get_full_image_url(obj.image)
        else:
            return ""
    
    def get_signature_image(self, obj):
        if obj.signature_image:
            return self.get_full_image_url(obj.signature_image)
        else:
            return ""
        
    def get_company_image(self, obj):
        if obj.user_type == 'Business User':
            business_id = obj.business_id
            try:
                business_in = business_info.objects.get(id=business_id)
                if business_in.profile_picture:
                    return self.get_full_image_url(business_in.profile_picture)
            except business_info.DoesNotExist:
                pass
        return "" 

    def get_full_image_url(self, image_path):
        request = self.context.get('request')  # Get the request object from the context
        if request is not None:
            return request.build_absolute_uri(settings.MEDIA_URL + image_path)
        return ""

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_id = instance.id
        request = self.context.get('request')
        language = request.data.get('language')  # Default to 'English' if not provided

        # Define the fields to exclude based on the 'language' parameter
        fields_to_exclude = []
        if language == 'English':
            fields_to_exclude.extend([
                'full_name_arabic',
                'address_type_arabic',
                'gender_arabic',
                'area_arabic',
                'block_arabic',
                'street_name_number_arabic',
                'house_number_arabic',
                'floor_arabic',
                'apartment_number_arabic',
            ])
        elif language == 'Arabic':
            fields_to_exclude.extend([
                'full_name',
                'address_type',
                'gender',
                'area',
                'block',
                'street_name_number',
                'house_number',
                'floor',
                'apartment_number',
            ])

        # Exclude the specified fields from the response data
        for field in fields_to_exclude:
            data.pop(field, None)

        active_membership = UserMembership.objects.filter(user_id=user_id, active_status='active').exclude(membership_id__in=[1, 4]).first()
        if active_membership:
            data['membership_expiry_date'] = active_membership.end_date
        else:
            data['membership_expiry_date'] = None

        data['image'] = self.get_image(instance)

        # Calculate available_contract
        total_contracts = contract_histroy.objects.filter(user_id=user_id).aggregate(total_contracts=Sum('contracts'))['total_contracts']
        total_contracts = total_contracts if total_contracts is not None else 0
        user_contracts = contracts.objects.filter(user_id=user_id).count()
        available_contracts = total_contracts - user_contracts
        data['available_contracts'] = available_contracts
        
        # Count used_contracts for the current user_id
        used_contracts = contracts.objects.filter(user_id=user_id).count()
        data['used_contracts'] = used_contracts

        # Fetch the contract_price from GeneralSettings
        try:
            general_settings = GeneralSettings.objects.first()
            contract_price = general_settings.contracts_price
        except GeneralSettings.DoesNotExist:
            contract_price = None

        data['contract_price'] = contract_price
        
        # Add company_image to the response
        data['company_image'] = self.get_company_image(instance)

        return data







# user profile view serializers
class UserProfileviewSerializer(serializers.ModelSerializer):
    nationality = serializers.StringRelatedField()
    language = serializers.StringRelatedField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ('civil_id','company_name','email','full_name','full_name_arabic','phone_number','address_type','address_type_arabic','nationality','language','email_verified_at','date_of_birth','gender','gender_arabic','is_active','status','created_at','last_login','area','area_arabic','block','block_arabic','street_name_number','street_name_number_arabic','house_number', 'house_number_arabic','floor','floor_arabic','apartment_number','apartment_number_arabic','verified_at','image')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['nationality'] = instance.nationality.name
        rep['language'] = instance.language.name
        return rep
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request is not None:
                return self._get_full_image_url(request, obj.image)
        return None

    def _get_full_image_url(self, request: Request, image_path: str) -> str:
        # Manually construct the full URL using the request's scheme, hostname, and port
        base_url = f'{request.scheme}://{request.get_host()}'
        media_url = urllib.parse.urljoin(base_url, settings.MEDIA_URL)
        full_url = urllib.parse.urljoin(media_url, image_path)
        return full_url







# user update profile serializer
from rest_framework import serializers
from rest_framework.request import Request
from django.conf import settings
import urllib.parse
from urllib.parse import urljoin

class UserprofileupdateSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(input_formats=['%d/%m/%Y'], format='%d/%m/%Y')
    image = serializers.CharField(required=False, allow_blank=True)  # Set 'required' to False and allow blank value

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request is not None:
                return self._get_full_image_url(request, obj.image)
        return None

    def _get_full_image_url(self, request, image_path):
        if image_path:
            # Get the base URL from the request
            base_url = f'{request.scheme}://{request.get_host()}'
            # Construct the full image URL using the base URL, "/media/", and image path
            full_url = urljoin(base_url, urljoin('/media/', image_path.lstrip('/')))
            return full_url
        else:
            return None

    class Meta:
        model = Users
        fields = ('full_name','full_name_arabic','phone_number', 'language', 'gender','gender_arabic', 'date_of_birth', 'address_type','address_type_arabic','nationality','area','area_arabic','block','block_arabic','street_name_number','street_name_number_arabic', 'house_number', 'house_number_arabic','floor','floor_arabic', 'apartment_number','apartment_number_arabic','image')
        extra_kwargs = {
            'full_name': {'required': True},
            'phone_number': {'required': True},
            # 'language': {'required': True},
            'address_type': {'required': True},
            'gender': {'required': True},
            'area': {'required': True},
            'block': {'required': True},
            'street_name_number': {'required': True},
            'house_number': {'required': True},
            'floor': {'required': True},
            'apartment_number': {'required': True}
        }

    def validate(self, attrs):
        if attrs.get('address_type') == 'apartment':
            attrs['area'] = self.initial_data.get('area')
            attrs['block'] = self.initial_data.get('block')
            attrs['street_name_number'] = self.initial_data.get('street_name_number')
            attrs['house_number'] = self.initial_data.get('house_number')
            attrs['floor'] = self.initial_data.get('floor')
            attrs['apartment_number'] = self.initial_data.get('apartment_number')
        elif attrs.get('address_type') == 'house':
            attrs['area'] = self.initial_data.get('area')
            attrs['block'] = self.initial_data.get('block')
            attrs['street_name_number'] = self.initial_data.get('street_name_number')
            attrs['house_number'] = self.initial_data.get('house_number')
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        errors = []

        # Check if image is null in the database
        if 'image' in representation and instance.image is None:
            del representation['image']  # Remove image field from the representation

        # Check for other required fields
        for field_name, field in self.fields.items():
            if field.required and field_name not in representation:
                field_name_formatted = field_name.capitalize().replace('_', ' ')
                errors.append({
                    'field': field_name,
                    'message': f"{field_name_formatted} field is required."
                })

        if errors:
            return {'status': 400, 'message': errors}

        return representation

    def update(self, instance, validated_data):
        image = validated_data.get('image')
        if image is not None:
            instance.image = image
        return super().update(instance, validated_data)




 
    
    
    
    
    
    
    
#user create password serializer
class UserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, write_only=True)
    retype_password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['retype_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs






#image upload serialzier 
# class UserImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = ('image',)







# user notification list serializer
class UserNotificationlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'new_comment_enabled',
            'status_change_enabled',
            'membership_expiration_enabled',
            'user_addon_enabled',
            'contract_deletion_enabled',
            'contract_review_enabled',
            'contract_signature_enabled',
            'contract_canceled_enabled',
            'new_draft_contract_enabled',
            'chat_sound_enabled',
            'chat_highlight_enabled',
            'reminder_push_enabled',
            'reminder_email_enabled',
        ]





#update user notification serializer
class UserNotificationupdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'new_comment_enabled',
            'status_change_enabled',
            'membership_expiration_enabled',
            'user_addon_enabled',
            'contract_deletion_enabled',
            'contract_review_enabled',
            'contract_signature_enabled',
            'contract_canceled_enabled',
            'new_draft_contract_enabled',
            'chat_sound_enabled',
            'chat_highlight_enabled',
            'reminder_push_enabled',
            'reminder_email_enabled',
        ]
        

# list notification serializers
class ListnotificationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Check and replace None values with an empty string
        for field in data:
            if data[field] is None:
                data[field] = ""

        return data

    class Meta:
        model = notification
        fields = ['id', 'notification_type', 'title', 'description', 'created_at', 'read', 'pin', 'contract']


#delete notification serializer
class DeleteNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = notification
        fields = '__all__'	
        
        
        
#switch user serializer class
class SwitchUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        
        
        
# switch account login 
class SwitchACLoginSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()