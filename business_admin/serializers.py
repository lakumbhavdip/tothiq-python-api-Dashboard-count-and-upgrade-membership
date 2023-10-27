from rest_framework import serializers
from business_admin.models import business_info,business_department
from user.models import notification,Users
from masterapp.models import GeneralSettings,contract_histroy
from contracts.models import contracts
from django.db.models import Sum



#Get business info serializer class
class GetBusinessInfoSerializer(serializers.ModelSerializer):
    authorized_signatory_image = serializers.SerializerMethodField()
    licence_image = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    authorized_signatory_expiry_date = serializers.DateField(format='%d/%m/%Y')
    licence_expiry_date = serializers.DateField(format='%d/%m/%Y')
    user_type = serializers.SerializerMethodField()
    membership_type = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        return obj.user_id

    def get_licence_image(self, obj):
        request = self.context.get('request')
        if obj.licence_image:
            if isinstance(obj.licence_image, str):
                # Return the complete image URL with dynamic domain and port
                return request.build_absolute_uri(f'/media/{obj.licence_image}')
            else:
                # Generate the URL for the file
                return request.build_absolute_uri('/media/' + obj.licence_image.name)
        return None

    def get_authorized_signatory_image(self, obj):
        request = self.context.get('request')
        if obj.authorized_signatory_image:
            if isinstance(obj.authorized_signatory_image, str):
                # Return the complete image URL with dynamic domain and port
                return request.build_absolute_uri(f'/media/{obj.authorized_signatory_image}')
            else:
                # Generate the URL for the file
                return request.build_absolute_uri('/media/' + obj.authorized_signatory_image.name)
        return None

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if obj.profile_picture:
            if isinstance(obj.profile_picture, str):
                # Return the complete image URL with dynamic domain and port
                return request.build_absolute_uri(f'/media/{obj.profile_picture}')
            else:
                # Generate the URL for the file
                return request.build_absolute_uri('/media/' + obj.profile_picture.name)
        return None

    def get_user_count_data(self,request,business_id):
        current_user_id = self.context['request'].user.id
        authorized_users_count = Users.objects.filter(business=business_id, user_type='authorized').count()
        restricted_users_count = Users.objects.filter(business=business_id, user_type='restricted').count()
        total_users_business = contract_histroy.objects.filter(user_id=current_user_id).aggregate(total_users=Sum('users'))['total_users']
        used_users_count = Users.objects.filter(business=business_id).count()
        avaliable_user_business = total_users_business - used_users_count if total_users_business is not None else 0
        
        user_count_data = {
            "total_users": total_users_business,
            "authorized_person": authorized_users_count,
            "restricted_users": restricted_users_count,
            "used_user": used_users_count,
            "avaliable_user": avaliable_user_business
        }
        return user_count_data

    def to_representation(self, instance):
        data = super().to_representation(instance)

        try:
            # Check if a business_info entry exists for the user
            business_info_entry = business_info.objects.get(user_id=self.context['request'].user.id)
            business_id = business_info_entry.id
            business_user_ids = Users.objects.filter(business_id=business_id).values_list('id', flat=True)
            business_user_id = business_info_entry.user_id
        except business_info.DoesNotExist:
            # If no business_info entry exists, use the current user as-is
            business_user_ids = [self.context['request'].user.id]
            business_user_id = self.context['request'].user.id

        # Calculate total contracts for the business
        total_contracts = contract_histroy.objects.filter(user_id=business_user_id).aggregate(total_contracts=Sum('contracts'))['total_contracts']
        total_contracts = total_contracts if total_contracts is not None else 0

        # Calculate used contracts for the business
        user_contracts = contracts.objects.filter(user_id__in=business_user_ids).count()

        # Update data dictionary with contract-related fields
        data.update({
            "total_contracts": total_contracts,
            "used_contracts": user_contracts,
            # "available_contracts": total_contracts - user_contracts,
        })

        # Fetch the user_price from GeneralSettings
        try:
            general_settings = GeneralSettings.objects.first()
            user_price = general_settings.users_price
        except GeneralSettings.DoesNotExist:
            user_price = None

        # Fetch the contract_price from GeneralSettings
        try:
            general_settings = GeneralSettings.objects.first()
            contract_price = general_settings.contracts_price
        except GeneralSettings.DoesNotExist:
            contract_price = None

        data['user_price'] = user_price
        data['contract_price'] = contract_price
        
        user_count_data = self.get_user_count_data(instance.user.id, instance.id)
        data.update(user_count_data)  # Update the data dictionary with user_count_data
        
        # Remove the "user_count" key
        data.pop('user_count', None)
        
        return data
    
    def get_user_type(self, obj):
        # Retrieve the user_type from the Users table based on the business_info entry
        try:
            user = Users.objects.get(id=obj.user_id)
            return user.user_type
        except Users.DoesNotExist:
            return None  # Handle the case where the user doesn't exist

    def get_membership_type(self, obj):
        # Retrieve the membership_type from the Users table based on the business_info entry
        try:
            user = Users.objects.get(id=obj.user_id)
            return user.membership_type
        except Users.DoesNotExist:
            return None

    class Meta:
        model = business_info
        fields = ['id', 'business_name', 'business_name_arabic', 'business_email_address', 'business_contact_number', 'extension_number', 'area', 'area_arabic', 'block', 'block_arabic', 'street_name_number', 'street_name_arabic', 'building_name_number', 'building_name_arabic', 'office_number', 'office_number_arabic', 'licence_expiry_date', 'authorized_signatory_expiry_date', 'licence_image', 'authorized_signatory_image', 'profile_picture','user_type','membership_type']



    
    
    
class BusinessInfoUpdateSerializer(serializers.ModelSerializer):
    authorized_signatory_image = serializers.SerializerMethodField()
    licence_image = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        return obj.user_id

    def get_licence_image(self, obj):
        request = self.context.get('request')
        if obj.licence_image:
            if isinstance(obj.licence_image, str):
                # Return the complete image URL with dynamic domain and port
                return request.build_absolute_uri(f'/media/{obj.licence_image}')
            else:
                # Generate the URL for the file
                return request.build_absolute_uri('/media/' + obj.licence_image.name)
        return None

    def get_authorized_signatory_image(self, obj):
        request = self.context.get('request')
        if obj.authorized_signatory_image:
            if isinstance(obj.authorized_signatory_image, str):
                # Return the complete image URL with dynamic domain and port
                return request.build_absolute_uri(f'/media/{obj.authorized_signatory_image}')
            else:
                # Generate the URL for the file
                return request.build_absolute_uri('/media/' + obj.authorized_signatory_image.name)
        return None
    
    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if obj.profile_picture:
            if isinstance(obj.profile_picture, str):
                # Return the complete image URL with dynamic domain and port
                return request.build_absolute_uri(f'/media/{obj.profile_picture}')
            else:
                # Generate the URL for the file
                return request.build_absolute_uri('/media/' + obj.profile_picture.name)
        return None
    class Meta:
        model = business_info
        fields = ['id',  'business_name','business_name_arabic', 'business_email_address', 'business_contact_number', 'extension_number','area','area_arabic','block','block_arabic','street_name_number','street_name_arabic','building_name_number','building_name_arabic','office_number','office_number_arabic', 'licence_expiry_date', 'authorized_signatory_expiry_date','licence_image','authorized_signatory_image','profile_picture']
        
        
        
        
class ListDepartmentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, department):
        children = department.children.filter(active_status='active')  # Filter out inactive children
        serializer = ListDepartmentSerializer(children, many=True)
        return serializer.data

    class Meta:
        model = business_department
        fields = ['id', 'parent_department_id', 'department_name', 'children']

        
        
        
        
class DepartmentnamelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = business_department
        fields = ('id', 'department_name')
        
        
class AdminListnotificationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = notification
        fields = ['id', 'notification_type', 'title', 'description', 'created_at', 'read','pin' ]
        
        
        
class AdminDeleteNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = notification
        fields = '__all__'	