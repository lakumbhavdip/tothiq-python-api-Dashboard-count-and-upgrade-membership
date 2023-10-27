from atexit import register
from dataclasses import field
from rest_framework import serializers
from .models import Users, Addressbook
from django.core.mail import send_mail
from rest_framework import status


# add contact in addressbook serializer
class AddressBookSerializer(serializers.Serializer):
    civil_id = serializers.CharField(max_length=12, required=True)
    full_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)




class contactsuggestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['full_name', 'email', 'civil_id', 'active_status','user_type']




# list contact in addressbook serializer
from django.conf import settings

class AddressBooklistSerializer(serializers.Serializer):
    addressbook_id = serializers.IntegerField()
    full_name = serializers.CharField(allow_null=True)  # Set allow_null=True to handle missing 'full_name'
    email = serializers.EmailField()
    phone_number = serializers.CharField(allow_null=True)
    active_status = serializers.CharField()
    nationality = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    invite_date = serializers.DateTimeField()


    class Meta:
        fields = ("addressbook_id", "full_name", "email", "phone_number", "active_status", "nationality", "image")

    def get_nationality(self, obj):
        nationality = obj.get('nationality')
        if nationality is not None:
            return nationality.name
        return None


    def get_image(self, obj):
        image_url = obj.get('image')
        if image_url:
            request = self.context.get('request')
            if request is not None:
                base_url = request.build_absolute_uri('/')
                media_url = base_url + 'media/'
                return media_url + image_url
        return ""











# details contact in addressbook serializer
class AddressBookdetailSerializer(serializers.ModelSerializer): 
    nationality = serializers.StringRelatedField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ("full_name", "email", "phone_number", "nationality", "gender","image","created_at")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.nationality is not None:
            rep['nationality'] = instance.nationality.name
        else:
            rep['nationality'] = None  # or any other default value you prefer

        return rep
    
    def get_image(self, instance):
        image_filename = instance.image  # Assuming the 'image' field stores the filename
        if image_filename:
            request = self.context.get('request')
            if request is not None:
                base_url = request.build_absolute_uri('/')
                media_url = base_url + 'media/'
                image_url = f'{media_url}{image_filename}'
                return image_url
        return ""
   