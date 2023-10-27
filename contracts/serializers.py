from rest_framework import serializers
from .models import Folder,categories,template,contracts,contract_party,Users,business_contract_party
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site





#List folder serializer in contracts
# class FolderListSerializer(serializers.ModelSerializer):
#     children = serializers.SerializerMethodField()

#     class Meta:
#         model = Folder
#         fields = ('id', 'parent_id', 'folder_name', 'children')

#     def get_children(self, obj):
#         children = obj.children.all()
#         return self.__class__(children, many=True).data

class ChildFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('id', 'parent_id', 'folder_name', 'children')

class FolderListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ('id', 'parent_id', 'folder_name', 'children')

    def get_children(self, obj):
        children = obj.children.all()
        language = self.context.get('language', 'English')
        if language == 'Arabic':
            for child in children:
                child.folder_name = child.folder_name_arabic
        return ChildFolderSerializer(children, many=True, context=self.context).data




    

# folder name listing Contracts
class FoldernamelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('id', 'folder_name')

    def to_representation(self, instance):
        language = self.context.get('language', 'English')
        
        if language == 'Arabic':
            folder_name = instance.folder_name_arabic or instance.folder_name
        else:
            folder_name = instance.folder_name

        return {
            'id': instance.id,
            'folder_name': folder_name
        }
        
        

# add notification serializer
# class AddnotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = notification
#         fields = ['id', 'notification_type', 'title', 'description', 'created_at', 'read']

#     def create(self, validated_data):
#         notification_type = validated_data.pop('notification_type')
#         instance = notification.objects.create(notification_type=notification_type, **validated_data)
#         return instance

        
        
        
        
#list category serializer
class CategorylistSerializerEnglish(serializers.ModelSerializer):
    class Meta:
        model = categories
        fields = ('id', 'category_name','individual_Premium_Membership','individual_basic_Membership','individual_free_Membership','business_Premium_Membership','business_basic_Membership','business_free_Membership')

class CategorylistSerializerArabic(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category_name_arabic')  # Map 'category_name_arabic' to 'category_name'

    class Meta:
        model = categories
        fields = ('id', 'category_name','individual_Premium_Membership','individual_basic_Membership','individual_free_Membership','business_Premium_Membership','business_basic_Membership','business_free_Membership')
        
        
        
        
        
#template list serializer 
from django.conf import settings

class TemplatelistSerializerEnglish(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = template
        fields = ('id', 'template_title', 'description', 'image')

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class TemplatelistSerializerArabic(serializers.ModelSerializer):
    template_title = serializers.CharField(source='template_title_arabic')
    image = serializers.SerializerMethodField()

    class Meta:
        model = template
        fields = ('id', 'template_title', 'description', 'image')

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None




#template image serializer 
class TemplateImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField(max_length=None)




#add template serializer
class AddTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = template
        fields = ['template_title', 'category', 'template_availability', 'description', 'image']
        extra_kwargs = {
            'template_title': {'required': True},
            'category': {'required': True},
            'template_availability': {'required': True},
            'description': {'required': True},
            'image': {'required': True},
        }


        
            
        

#add contracts (Step-2)serializer
from datetime import datetime
from datetime import datetime, date

class ContractSerializer(serializers.ModelSerializer):
    contract_start_date = serializers.DateField(input_formats=['%d/%m/%Y'])
    contract_end_date = serializers.DateField(input_formats=['%d/%m/%Y'])
    category = serializers.PrimaryKeyRelatedField(queryset=categories.objects.all())
    folder = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all())
    # template = serializers.PrimaryKeyRelatedField(queryset=template.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(ContractSerializer, self).__init__(*args, **kwargs)
        self.fields['contract_start_date'].required = False
        self.fields['contract_end_date'].required = False
    
    def validate_contract_start_date(self, value):
            if isinstance(value, date):
                value = value.strftime('%d/%m/%Y')
            try:
                return datetime.strptime(value, '%d/%m/%Y').date()
            except ValueError:
                raise serializers.ValidationError('Invalid contract start date format. Use the format "dd/mm/yyyy".')

    def validate_contract_end_date(self, value):
        if isinstance(value, date):
            value = value.strftime('%d/%m/%Y')
        try:
            return datetime.strptime(value, '%d/%m/%Y').date()
        except ValueError:
            raise serializers.ValidationError('Invalid contract end date format. Use the format "dd/mm/yyyy".')

    class Meta:
        model = contracts
        fields = ('id', 'user', 'contract_title', 'template','category','description', 'contract_start_date', 'contract_end_date', 'created_at', 'deleted_at', 'folder', 'business','contract_duration', 'contract_start_date', 'contract_end_date','currency', 'contract_fees', 'contract_amount', 'contract_amount_words','arbitration','jurisdiction')
        extra_kwargs = {
            'contract_title': {'required': True},
            'category': {'required': True},
            'folder': {'required': True},
            # 'template': {'required': True}
        }


#update contracts (Step-2)serializer
class UpdateContractSerializer(serializers.ModelSerializer):
    contract_start_date = serializers.DateField(input_formats=['%d/%m/%Y'], required=False)
    contract_end_date = serializers.DateField(input_formats=['%d/%m/%Y'], required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=categories.objects.all())
    folder = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all())

    def validate_contract_start_date(self, value):
        if isinstance(value, date):
            value = value.strftime('%d/%m/%Y')
        try:
            return datetime.strptime(value, '%d/%m/%Y').date()
        except ValueError:
            raise serializers.ValidationError('Invalid contract start date format. Use the format "dd/mm/yyyy".')

    def validate_contract_end_date(self, value):
        if isinstance(value, date):
            value = value.strftime('%d/%m/%Y')
        try:
            return datetime.strptime(value, '%d/%m/%Y').date()
        except ValueError:
            raise serializers.ValidationError('Invalid contract end date format. Use the format "dd/mm/yyyy".')

    class Meta:
        model = contracts
        fields = ('id', 'user', 'contract_title', 'category', 'description', 'contract_start_date', 'contract_end_date', 'created_at', 'deleted_at','folder')
        extra_kwargs = {
            'contract_title': {'required': True},
            'category': {'required': True},
            'folder': {'required': True},
            'description': {'required': False}
        }


        

#add party (Step-3) serializer 
# class ContractFirstPartySerializer(serializers.ModelSerializer):
#     contract_id = serializers.IntegerField(write_only=True)  # Add this field for contract_id
#     class Meta:
#         model = contract_party
#         fields = ('name', 'email', 'party_type', 'civil_id', 'contract_id')
class ContractPartySerializer(serializers.ModelSerializer):
    contract_id = serializers.IntegerField(required=False)
    first_party_name = serializers.CharField(required=False)
    first_party_email = serializers.EmailField(required=False)
    first_party_civil_id = serializers.CharField(required=False)
    second_party_name = serializers.CharField(required=False)
    second_party_email = serializers.EmailField(required=False)
    second_party_civil_id = serializers.CharField(required=False)

    class Meta:
        model = contract_party
        fields = ['contract_id','first_party_name', 'first_party_email','first_party_civil_id', 'second_party_name', 'second_party_email', 'second_party_civil_id']



# get contract party detail 
class ContractPartyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = contract_party
        fields = (
            'id',
            'contract',
            'user',
            'first_party_civil_id',
            'first_party_name',
            'first_party_email',
            'second_party_name',
            'second_party_email',
            'second_party_civil_id',
            'status',
            'created_at',
            'updated_at',
        )




#update party details 
class UpdateContractPartySerializer(serializers.ModelSerializer):
    contract_id = serializers.IntegerField(required=False)
    first_party_name = serializers.CharField(required=False)
    first_party_email = serializers.EmailField(required=False)
    first_party_civil_id = serializers.CharField(required=False)
    second_party_name = serializers.CharField(required=False)
    second_party_email = serializers.EmailField(required=False)
    second_party_civil_id = serializers.CharField(required=False)

    class Meta:
        model = contract_party
        fields = ['contract_id', 'first_party_name', 'first_party_email', 'first_party_civil_id', 'second_party_name', 'second_party_email', 'second_party_civil_id']
        
        
        
        

#contract status serializer 
class ContractStatusUpdateSerializer(serializers.Serializer):
    contract_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=contracts.STATUS_CHOICES)
    delete_reason = serializers.CharField(required=False)  # Add delete_reason field
    cancellation_reason = serializers.CharField(required=False)  # Add cancellation_reason field
    def to_internal_value(self, data):
            try:
                return super().to_internal_value(data)
            except serializers.ValidationError as error:
                error_detail = []
                for field, errors in error.detail.items():
                    field_errors = [f"{field} {error}" for error in errors]
                    error_detail.extend(field_errors)
                raise serializers.ValidationError({"status": "400", "message": " ".join(error_detail)})
        
        
        
# List contract serializer (Mobile APP)
from django.conf import settings
from rest_framework.reverse import reverse
class ContractPartylistSerializerAPP(serializers.ModelSerializer):
    contract_party = serializers.SerializerMethodField()

    def get_full_image_url(self, image_path):
        if image_path:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(settings.MEDIA_URL + image_path)
        return None

    def get_user_data(self, user, view_contract):
        image_url = self.get_full_image_url(user.image) if user.image else None
        user_data = {
            "id": user.id,
            "image": image_url,
            "email": user.email,
            "full_name": user.full_name,
            "phone_number": user.phone_number,
            "user_type": user.user_type,
            "view_contract": view_contract,
            "hawati_verification": user.hawati_verification
        }

        if user.user_type == "Business User" or user.user_type == "Business Admin":
            user_data["company_name"] = user.company_name
        else:
            user_data["company_name"] = ""

        return user_data

    def get_contract_party(self, obj):
        contract = obj
        contract_parties = contract_party.objects.filter(contract=contract)

        contract_party_data = []
        for party in contract_parties:
            first_party_user = Users.objects.filter(email=party.first_party_email).first()
            second_party_user = Users.objects.filter(email=party.second_party_email).first()

            if first_party_user:
                contract_party_data.append(self.get_user_data(first_party_user, party.view_contract))
            if second_party_user:
                contract_party_data.append(self.get_user_data(second_party_user, party.view_contract))

        return contract_party_data

    class Meta:
        model = contracts
        fields = ['id', 'contract_title', 'created_at', 'status', 'contract_party']









        
        
# List contract serializer (WEB)
class ContractPartylistSerializerWEB(serializers.ModelSerializer):
    first_party_user = serializers.SerializerMethodField()
    second_party_user = serializers.SerializerMethodField()

    def get_full_image_url(self, image_path):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(settings.MEDIA_URL + image_path)
        return None

    def get_user_data(self, user):
        image_url = None
        if user.image:
            if isinstance(user.image, str):
                # Handle the case when the image is a string
                request = self.context.get('request')
                if request is not None:
                    image_url = request.build_absolute_uri(
                        f"{settings.MEDIA_URL}{user.image}"
                    )
            else:
                request = self.context.get('request')
                image_url = self.get_full_image_url(user.image.path)

        return {
            "id": user.id,
            "image": image_url
        }

    def get_first_party_user(self, obj):
        first_party_email = obj.first_party_email
        user = Users.objects.filter(email=first_party_email).first()
        return self.get_user_data(user) if user else None

    def get_second_party_user(self, obj):
        second_party_email = obj.second_party_email
        user = Users.objects.filter(email=second_party_email).first()
        return self.get_user_data(user) if user else None

    class Meta:
        model = contract_party
        fields = ['first_party_user', 'second_party_user']
        
        
class BusinessContractPartySerializer(serializers.ModelSerializer):
    first_party_user = serializers.SerializerMethodField()
    second_party_user = serializers.SerializerMethodField()

    def get_full_image_url(self, image_path):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(settings.MEDIA_URL + image_path)
        return None

    def get_user_data(self, user):
        if user:
            return {
                "id": user.id,
                "image": self.get_full_image_url(user.image) if user.image else None,  # Get full image URL
                # Add other user attributes you want to include
            }
        return None

    def get_first_party_user(self, obj):
        user = obj.first_party_name  # Access the foreign key relation
        return self.get_user_data(user)

    def get_second_party_user(self, obj):
        user = obj.second_party_name  # Access the foreign key relation
        return self.get_user_data(user)

    class Meta:
        model = business_contract_party
        fields = ['first_party_user', 'second_party_user']

        

# Assuming Users is your custom User model
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'full_name', 'image']  # Add other fields as needed







#Party user details serializer
class PartyUserdetailsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_full_image_url(self, image_path):
        request = self.context.get('request')  # Get the request object from the context
        if request is not None:
            return request.build_absolute_uri(settings.MEDIA_URL + image_path)
        return ""
    
    def get_image(self, obj):
        if obj.image:
            return self.get_full_image_url(obj.image)
        else:
            return ""

    class Meta:
        model = Users
        fields = ('email', 'full_name', 'phone_number', 'status', 'hawati_verification', 'image')
        

        

# add appendix Serialzer 
class AddappendixSerializer(serializers.ModelSerializer):
    contract_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = contracts
        fields = ['contract_id','appendix']
        
        
        
        
        
        
# clone contract serializer   
class CloneContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = contracts
        fields = '__all__'



#contract details serializer
class contractsdetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = contracts
        fields =  ('id', 'contract_title','folder', 'category','status','description','contract_duration', 'contract_start_date', 'contract_end_date', 'currency','contract_fees','contract_amount','contract_amount_words','arbitration','jurisdiction','created_at')