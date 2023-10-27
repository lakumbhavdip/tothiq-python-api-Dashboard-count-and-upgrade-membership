from rest_framework import serializers
from .models import nationality_type,language,languages_label,Membership,Payment,contract_histroy

# list label language serializer
# class languagelistserializer(serializers.ModelSerializer):
#     label = serializers.SerializerMethodField()

#     class Meta:
#         model = languages_label
#         fields = ('id', 'label')

#     def get_label(self, obj):
#         user_language = self.context['request'].user.language.strip().lower()
#         if user_language == 'arabic':
#             return obj.arabic
#         else:
#             return obj.english

    
    
    
    
# list label language serializer
class languagelistserializer(serializers.ModelSerializer):
  class Meta:
    model = language
    fields = ('id','name')    
    
    
    
    
    
    
  
# list nationality serialzer
class nationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = nationality_type
        fields = ('id', 'name','name_arabic')
        


class languages_labelSerializer(serializers.ModelSerializer):
    class Meta:
        model = languages_label
        fields = ('id','label', 'english', 'arabic')
class nationality_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = nationality_type
        fields = ('id','name','name_arabic')
class language_typeSerializer(serializers.ModelSerializer):
    class Meta:
      model = language
      fields = ('id','name')
     
     
     
# payment initialize serializer
class PaymentInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('payment_type', 'payment_method', 'purchase_id')
        extra_kwargs = {
            field: {'required': True}
            for field in ('payment_type', 'payment_method', 'purchase_id')
        }



class ContractHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = contract_histroy
        fields = ('user_id', 'contracts', 'parties', 'action_type', 'action_info', 'created_at')
