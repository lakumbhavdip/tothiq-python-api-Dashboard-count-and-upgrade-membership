from rest_framework import generics
from .models import nationality_type,language,languages_label,Membership,Payment,UserMembership,contract_histroy,GeneralSettings
from .serializers import languagelistserializer,nationalitySerializer,nationality_typeSerializer,language_typeSerializer,PaymentInitSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import os
from django.conf import settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from django.db.models import F
from django.shortcuts import get_object_or_404
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Coupon, Membership
from django.utils import timezone
from django.utils.text import format_lazy
import random
import time
from user.models import Users  # Import the Users model
from .models import countrycurrency
from datetime import datetime, timedelta



#for knet encryption-decryption and http form data response
from cryptography.fernet import Fernet
from urllib.parse import parse_qs
from datetime import date, timedelta
import urllib.request
from cryptography.fernet import Fernet
from urllib.parse import parse_qs
from collections import namedtuple
from cryptography.fernet import Fernet
from django.shortcuts import get_object_or_404
import base64



#for myfatoorah payment gateway integration
# Import required libraries (make sure it is installed!)
import requests
import json
import sys





# class languageListView(generics.ListAPIView):
#     serializer_class = languagelistserializer

#     def get_queryset(self):
#         current_user = self.request.user
#         user_language = current_user.language.strip().lower()
#         if user_language == 'arabic':
#             queryset = languages_label.objects.only('id', 'label', 'arabic')
#         else:
#             queryset = languages_label.objects.only('id', 'label', 'english')
#         return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         data = serializer.data
#         message = "Language list fetched successfully."
#         status_code = 200
#         response_data = {
#             'status': '200',
#             'message': message,
#             'data': data
#         }
#         return Response(response_data, status=status_code)



#language list 
class LanguageListView(generics.ListAPIView):
    queryset = language.objects.all()
    serializer_class = languagelistserializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        user_id = request.user.id  # Get the user ID from the request object
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        message = "Language list fetched successfully."
        status_code = 200
        response_data = {
            'status': '200',
            'message': message,
            'data': data,
            # 'user_id': user_id  # Include the user ID in the response
        }
        return Response(response_data, status=status_code)



#Nationality list 
class NationalityListAPIView(generics.ListAPIView):
    queryset = nationality_type.objects.all()
    serializer_class = nationalitySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        queryset = self.get_queryset()

        # Check if the 'language' parameter is provided in the request body
        language = request.data.get('language', 'English')

        # Serialize the queryset
        serializer = self.get_serializer(queryset, many=True)

        # Modify the response data based on the 'language' parameter
        if language == 'Arabic':
            data = [{'id': item['id'], 'name': item['name_arabic']} for item in serializer.data if 'name_arabic' in item]
        else:
            data = [{'id': item['id'], 'name': item['name']} for item in serializer.data]

        message = "Nationalities list fetched successfully."
        status_code = 200

        response_data = {
            'status': '200',
            'message': message,
            'data': data
        }
        return Response(response_data, status=status_code)
    
    
    
    
# file upload APIview 

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')  # Using get() to handle the case when the file is not provided

        if file_obj is None:
            return Response({'status': 400, 'message': 'No file provided.'}, status=status.HTTP_200_OK)

        # Generate a unique filename using timestamp and random number
        timestamp = time.strftime('%Y%m%d%H%M%S')
        random_number = random.randint(1000, 900000)
        unique_filename = f"{timestamp}-{random_number}-{file_obj.name}"

        file_path = os.path.join('tothiq_pic', unique_filename)
        full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

        # Save the file to the desired path
        with open(full_file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        image_path = file_path.replace("\\", "/")  # Replace backslashes with forward slashes

        image_url = request.build_absolute_uri(settings.MEDIA_URL + image_path)

        response_data = {
            'status': 200,
            'message': 'File uploaded successfully',
            'image_path': image_path,
            'image_url': image_url
        }

        return Response(response_data)
        


    
    
    
#initialize APIView
class initializeAPIView(APIView):
    def get(self, request):
        auth_token = request.headers.get('Authorization')
        language_param = request.headers.get('language')

        # Check if token exists in the database
        token_valid = False
        user_active_status = None  # Initialize user_active_status

        if Token.objects.filter(key=auth_token).exists():
            token_valid = True

            # Fetch the user associated with the token
            user = Token.objects.get(key=auth_token).user

            # Get the user's active_status or set it to an empty string if it's None
            user_active_status = user.active_status if hasattr(user, 'active_status') else ''

        nationalities = nationality_type.objects.all()
        nationality_serializer = nationality_typeSerializer(nationalities, many=True)
        nationality_data = nationality_serializer.data

        languages = language.objects.all()
        languages_serializer = language_typeSerializer(languages, many=True)
        languages_data = languages_serializer.data

        labels = languages_label.objects.values('id', 'code', 'arabic', 'english')
        
        # Map ACTIVE_STATUS_CHOICES to integer values
        status_mapping = {
            'active': 0,
            'inactive': 1,
            'blocked': 2,
            'deleted': 3,
        }

        # Get the integer code based on user_active_status
        user_status = status_mapping.get(user_active_status, -1)

        # Define user status messages based on active_status
        user_status_messages = {
            "blocked": "Your account is blocked. Kindly contact Tothiq Administration .",
            "deleted": "Your account is deleted. Kindly contact Tothiq Administration .",
        }

        # Get the user status message based on active_status
        user_status_message = user_status_messages.get(user_active_status, '')

        response_data = {
            "status": "200",
            "message": "Authorized user" if token_valid else "Unauthorized user",
            "token_valid": token_valid,
            "data": {
                "user_status": user_status,  # Include user_active_status in response
                "user_status_message": user_status_message,  # Include user_status_message
                "nationalities": nationality_data,
                "languages": languages_data,
                "label": labels,
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)



class AddLabelAPIView(APIView):
    def post(self, request):
        id = request.data.get('id')
        code = request.data.get('code')
        english = request.data.get('english')
        arabic = request.data.get('arabic')

        if not code:
            return Response({'status':400,"message": "code field required."}, status=status.HTTP_200_OK)

        if not english:
            return Response({'status':400, 'message':'english field requried.'},status=status.HTTP_200_OK)
        
        # if not arabic:
        #     return Response({'status':400, 'message':'arabic field requried.'},status=status.HTTP_200_OK)

        if languages_label.objects.filter(code=code).exists():
            return Response({"message": "This label already exists"}, status=status.HTTP_200_OK)

        new_label = languages_label(id=id, code=code, english=english, arabic=arabic)
        new_label.save()

        return Response({"message": "Label added successfully."}, status=status.HTTP_200_OK)
    
    
    
class UpdateLabelAPIView(APIView):
    def post(self, request):
        id = request.data.get('id')
        code = request.data.get('code')
        english = request.data.get('english')
        arabic = request.data.get('arabic')

        if not id:
            return Response({'status': 400, "message": "Label id required."}, status=status.HTTP_200_OK)

        try:
            label = languages_label.objects.get(pk=id)
        except languages_label.DoesNotExist:
            return Response({'status': 400, "message": "Label not found."}, status=status.HTTP_200_OK)

        if code and languages_label.objects.filter(code=code).exclude(pk=id).exists():
            return Response({"message": "This code already exists."}, status=status.HTTP_200_OK)

        if code:
            label.code = code
        if english:
            label.english = english
        if arabic:
            label.arabic = arabic
        label.save()

        return Response({'status': 200, "message": "Label updated successfully."}, status=status.HTTP_200_OK)





class labellistAPIView(APIView):
    def post(self, request):
        # auth_token = request.headers.get('Authorization')
        language_param = request.POST.get('language')


        if not language_param:
            return Response({'status':400,'message':'language is requried.'})
        # Check if token exists in the database
        # token_valid = False
        # if Token.objects.filter(key=auth_token).exists():
        #     token_valid = True

        # nationalities = nationality_type.objects.all()
        # nationality_serializer = nationality_typeSerializer(nationalities, many=True)
        # nationality_data = nationality_serializer.data

        # languages = language.objects.all()
        # languages_serializer = language_typeSerializer(languages, many=True)
        # languages_data = languages_serializer.data

        # Filter labels based on language_param
        if language_param == 'Arabic':
            labels = languages_label.objects.values('id', 'code', 'arabic').annotate(label=F('arabic')).values('id', 'code', 'label')
        elif language_param == 'English':
            labels = languages_label.objects.values('id', 'code', 'english').annotate(label=F('english')).values('id', 'code', 'label')
        elif language_param is None:
            labels = languages_label.objects.values('id', 'code', 'english').annotate(label=F('english')).values('id', 'code', 'label')
        else:
            return Response({'status':400,'message':'invalid language'})

        response_data = {
            "status": "200",
            "message": "Label list fetch successfully.",
            # "message": "Authorized user" if token_valid else "Unauthorized user",
            # "token_valid": token_valid,
            # "data": {
                # "nationalities": nationality_data,
                # "languages": languages_data,
                "data": labels
            # }
        }
        return Response(response_data, status=status.HTTP_200_OK)



 
#membership listing
class MembershipAPIView(APIView):
    def post(self, request):
        user_type = request.data.get("user_type", "individual user").lower()
        membership_id = request.data.get("id")
        user_id = request.data.get("user_id")  # New parameter

        if user_type not in ["business admin", "individual user"]:
            return Response(
                {"status": 400, "message": "Invalid user type."},
                status=status.HTTP_200_OK,
            )

        if membership_id:
            try:
                membership = Membership.objects.get(id=membership_id)
                membership_data = {
                    "id": membership.id,
                    "user_type": membership.user_type,
                    "membership_name": membership.membership_name,
                    "membership_amount": membership.membership_amount,
                    "discount_type": membership.discount_type,
                    "discount_rate": membership.discount_rate,
                    "discount_price": membership.discount_price,
                    "payment_gateway_kne": membership.payment_gateway_kne,
                    "payment_gateway_cb_card": membership.payment_gateway_cb_card,
                    "payment_gateway_gp": membership.payment_gateway_gp,
                    "payment_gateway_ap": membership.payment_gateway_ap,
                    "number_of_contract": membership.number_of_contract,
                    "number_of_parties": membership.number_of_parties,
                    "chat_between_parties": membership.chat_between_parties,
                    "address_book": membership.address_book,
                    "create_blank_contract": membership.create_blank_contract,
                    "upload_contract": membership.upload_contract,
                    "view_log": membership.view_log,
                    "free_contract_storage": membership.free_contract_storage,
                    "free_sign_up": membership.free_sign_up,
                    "private_or_not": membership.private_or_not,
                    "free_template": membership.free_template,
                    "free_premium_template": membership.free_premium_template,
                    "unlimited_templates": membership.unlimited_templates,
                }

                # Remove fields with False values from the membership_data dictionary
                membership_data = {
                    k: v for k, v in membership_data.items() if v is not False
                }

                message = "Membership details retrieved successfully."
                return Response(
                    {"status": 200, "message": message, "data": membership_data},
                    status=status.HTTP_200_OK,
                )
            except Membership.DoesNotExist:
                return Response(
                    {"status": 400, "message": "Membership not found."},
                    status=status.HTTP_200_OK,
                )

        # Fetch all memberships if no 'id' parameter is provided
        memberships = Membership.objects.exclude(
            membership_name__in=["Gold", "Platinum"]
        )

        if user_type:
            memberships = memberships.filter(user_type__icontains=user_type)

        memberships = memberships.order_by("id")

        data = {}  # Change from list to dictionary
        for membership in memberships:
            membership_data = {
                "id": membership.id,
                "user_type": membership.user_type,
                "membership_name": membership.membership_name,
                "membership_amount": membership.membership_amount,
                "discount_type": membership.discount_type,
                "discount_rate": membership.discount_rate,
                "discount_price": membership.discount_price,
                "payment_gateway_kne": membership.payment_gateway_kne,
                "payment_gateway_cb_card": membership.payment_gateway_cb_card,
                "payment_gateway_gp": membership.payment_gateway_gp,
                "payment_gateway_ap": membership.payment_gateway_ap,
                "number_of_contract": membership.number_of_contract,
                "number_of_parties": membership.number_of_parties,
                "chat_between_parties": membership.chat_between_parties,
                "address_book": membership.address_book,
                "create_blank_contract": membership.create_blank_contract,
                "upload_contract": membership.upload_contract,
                "view_log": membership.view_log,
                "free_contract_storage": membership.free_contract_storage,
                "free_sign_up": membership.free_sign_up,
                "private_or_not": membership.private_or_not,
                "free_template": membership.free_template,
                "free_premium_template": membership.free_premium_template,
                "unlimited_templates": membership.unlimited_templates,
            }

            # Remove fields with False values from the membership_data dictionary
            membership_data = {
                k: v for k, v in membership_data.items() if v is not False
            }

            data[membership.membership_name] = membership_data
            
        if user_id:
            try:
                user = Users.objects.get(id=user_id)
                user_membership_type = user.membership_type  # Replace with your actual field name

                # Filter memberships based on the user's membership type
                filtered_data = {user_membership_type: data.get(user_membership_type, {})}

                message = "Membership details retrieved successfully."
                return Response(
                    {"status": 200, "message": message, "data": filtered_data},
                    status=status.HTTP_200_OK,
                )
            except Users.DoesNotExist:
                return Response(
                    {"status": 400, "message": "User not found."},
                    status=status.HTTP_200_OK,
                )

        message = "Membership details retrieved successfully."
        return Response(
            {"status": 200, "message": message, "data": data},
            status=status.HTTP_200_OK,
        )
        

 


# add currency API
class AddCountryCurrency(APIView):
    def post(self, request):
        # Check if 'currency_name' and 'country_name' are present in the request data
        country_name = request.data.get('country_name')
        currency_name = request.data.get('currency_name')

        if not country_name :
            return Response({'status':200,'message': 'Country name is required.'}, status=status.HTTP_200_OK)

        if not currency_name :
            return Response({'status':200,'message': 'Currency name is required.'}, status=status.HTTP_200_OK)
        
        # Check if a country_currency with the same country_name already exists
        existing_country_currency = countrycurrency.objects.filter(country_name=country_name).first()
        if existing_country_currency:
            return Response({'status': 400, 'message': f'{country_name} Country already exists with {existing_country_currency.currency_name} currency.'}, status=status.HTTP_200_OK)
        
        try:
            # Create a new country_currency object
            country_currency1 = countrycurrency.objects.create(
                currency_name=currency_name,
                country_name=country_name,
                created_at=timezone.now()  # Save the current timezone
            )

            return Response({'status':200,'message': 'Country Currency added successfully.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
# currency List API
class ListCountryCurrency(APIView):
    def get(self, request):
        try:
            # Fetch all country_currency objects
            country_currencies = countrycurrency.objects.all().order_by('id')
            # Create a list of dictionaries for the response data
            data = [{'id': cc.id,'country_name': cc.country_name, 'currency_name': cc.currency_name} for cc in country_currencies]

            return Response({'status': 200, 'message': 'Currency list fetch successfully.', 'data': data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 500, 'message': 'An error occurred while fetching currency list.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# update currency API
class UpdateCountryCurrency(APIView):
    def post(self, request):
        # Get the 'id', 'country_name', and 'currency_name' from the request data
        id = request.data.get('id')
        country_name = request.data.get('country_name')
        currency_name = request.data.get('currency_name')

        # Check if 'id' is provided
        if id is None:
            return Response({'status': 400, 'message': 'Currency ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Try to get the country_currency object with the provided 'id'
            country_currency = countrycurrency.objects.get(pk=id)

            # Check if 'country_name' already exists with a different 'id'
            if country_name:
                existing_country_currency = countrycurrency.objects.filter(country_name=country_name).exclude(pk=id).first()
                if existing_country_currency:
                    return Response({'status': 400, 'message': f'{country_name} Country already exists with {existing_country_currency.currency_name} currency.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the country_currency object if values are provided
            if country_name is not None:
                country_currency.country_name = country_name
            if currency_name is not None:
                country_currency.currency_name = currency_name
            country_currency.updated_at = timezone.now()
            country_currency.save()

            return Response({'status': 200, 'message': 'Country Currency updated successfully.'}, status=status.HTTP_200_OK)

        except countrycurrency.DoesNotExist:
            return Response({'status': 404, 'message': f'Country Currency with ID {id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': 500, 'message': 'An error occurred while updating Country Currency.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    


#----------- MYFATOORAH PAYMENT GATEWAY FUNCTIONS

# Test Environment
base_url = "https://apitest.myfatoorah.com"
api_key = "rLtt6JWvbUHDDhsZnfpAhpYk4dxYDQkbcPTyGaKp2TYqQgG7FGZ5Th_WD53Oq8Ebz6A53njUoo1w3pjU1D4vs_ZMqFiz_j0urb_BH9Oq9VZoKFoJEDAbRZepGcQanImyYrry7Kt6MnMdgfG5jn4HngWoRdKduNNyP4kzcp3mRv7x00ahkm9LAK7ZRieg7k1PDAnBIOG3EyVSJ5kK4WLMvYr7sCwHbHcu4A5WwelxYK0GMJy37bNAarSJDFQsJ2ZvJjvMDmfWwDVFEVe_5tOomfVNt6bOg9mexbGjMrnHBnKnZR1vQbBtQieDlQepzTZMuQrSuKn-t5XZM7V6fCW7oP-uXGX-sMOajeX65JOf6XVpk29DP6ro8WTAflCDANC193yof8-f5_EYY-3hXhJj7RBXmizDpneEQDSaSz5sFk0sV5qPcARJ9zGG73vuGFyenjPPmtDtXtpx35A-BVcOSBYVIWe9kndG3nclfefjKEuZ3m4jL9Gg1h2JBvmXSMYiZtp9MR5I6pvbvylU_PP5xJFSjVTIz7IQSjcVGO41npnwIxRXNRxFOdIUHn0tjQ-7LwvEcTXyPsHXcMD8WtgBh-wxR8aKX7WPSsT1O8d8reb2aR7K3rkV3K82K_0OgawImEpwSvp9MNKynEAJQS6ZHe_J_l77652xwPNxMRTMASk1ZsJL"
# Test token value to be placed here: https:#myfatoorah.readme.io/docs/test-token


# Live Environment
# base_url = "https:#api.myfatoorah.com"
# api_key = "mytokenvalue" #Live token value to be placed here: https:#myfatoorah.readme.io/docs/live-token


def check_data(key, response_data):
    if key in response_data.keys() and response_data[key] is not None:
        return True
    else:
        return False


# Error Handle Function
def handle_response(response):
    if response.text == "":  # In case of empty response
        raise Exception("API key is not correct")

    response_data = response.json()
    response_keys = response_data.keys()

    if "IsSuccess" in response_keys and response_data["IsSuccess"] is True:
        return  # Successful
    elif check_data("ValidationErrors", response_data):
        error = []
        for i in range(len(response.json()["ValidationErrors"])):
            v_error = [response_data["ValidationErrors"][i].get(key) for key in ["Name", "Error"]]
            error.append(v_error)
    elif check_data("ErrorMessage", response_data):
        error = response_data["ErrorMessage"]
    elif check_data("Message", response_data):
        error = response_data["Message"]
    elif check_data("Data", response_data):
        error = response_data["Data"]["ErrorMessage"]
    elif check_data("ErrorMessage", response_data["Data"]):
        error = response_data["Data"]["ErrorMessage"]
    else:
        error = "An Error has occurred. API response: " + response.text
    raise Exception(error)


# Call API Function
def call_api(api_url, api_key, request_data, request_type="POST"):
    request_data = json.dumps(request_data)
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}
    response = requests.request(request_type, api_url, data=request_data, headers=headers)
    handle_response(response)
    return response


# Initiate Payment endpoint Function
def initiate_payment(initiatepay_request):
    api_url = base_url + "/v2/InitiatePayment"
    initiatedpay_response = call_api(api_url, api_key, initiatepay_request).json()
    payment_methods = initiatedpay_response["Data"]["PaymentMethods"]
    # Initiate Payment output if successful
    #print("Payment Methods: ", payment_methods)
    return payment_methods

# Send Payment endpoint Function
def send_payment(sendpay_data):
    api_url = base_url + "/v2/SendPayment"
    sendpay_response = call_api(api_url, api_key, sendpay_data).json()  # RReceiving the response of MyFatoorah

    invoice_id = sendpay_response["Data"]["InvoiceId"]
    invoice_url = sendpay_response["Data"]["InvoiceURL"]
    # Send Payment output if successful
    print("InvoiceId: ", invoice_id,
          "\nInvoiceURL: ", invoice_url)
    return invoice_id, invoice_url


# Execute Payment endpoint Function
def execute_payment(executepay_request):
    api_url = base_url + "/v2/ExecutePayment"
    executepay_response = call_api(api_url, api_key, executepay_request).json()
    invoice_id = executepay_response["Data"]["InvoiceId"]
    invoice_url = executepay_response["Data"]["PaymentURL"]
    # Execute Payment output if successful
    print("InvoiceId: ", invoice_id,
          "\nInvoiceURL: ", invoice_url)
    return invoice_id, invoice_url


# Get Payment Status endpoint Function
def get_payment_status(getpay_request):
    api_url = base_url + "/v2/getPaymentStatus"
    getpay_response = call_api(api_url, api_key, getpay_request).json()
    return getpay_response["Data"]



# payment intiated Bharat parmar
class PaymentInitAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        required_fields = ['payment_type', 'payment_method', 'purchase_id']
        missing_fields = [field for field in required_fields if field not in request.data]

        if missing_fields:
            response_data = {
                'status': 400,
                'message': f'Missing required fields: {", ".join(missing_fields)}',
                'data': {}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        payment_type = request.data.get('payment_type')
        payment_method = request.data.get('payment_method')
        purchase_id = request.data.get('purchase_id')
        
        if payment_type not in ['membership', 'contracts', 'users']:
            return Response({'status': 400, 'message': 'Invalid payment type.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if payment_method not in ['knet', 'myfatoorah']:
            return Response({'status': 400, 'message': 'Invalid payment method.'}, status=status.HTTP_400_BAD_REQUEST)
        
        contract = (contract_histroy)
        users = ()
        membership = get_object_or_404(Membership, id=purchase_id)

        membership_amount = membership.membership_amount
        discount_type = membership.discount_type
        discount_rate = membership.discount_rate


        if discount_type == "percentage":
            if discount_rate is not None:
                discount_amount = (membership_amount * discount_rate) / 100
            else:
                # Handle the case where discount_rate is None
                discount_amount = 0
        else:
            if discount_rate is not None:
                discount_amount = discount_rate
            else:
                # Handle the case where discount_rate is None
                discount_amount = 0

        membership_net_amount = round(membership_amount - discount_amount, 3)

        serializer = PaymentInitSerializer(data=request.data)
        
        payment_response_url = "https://versionreview.com/tothiq/payment-success.php"
        payment_fail_url = "https://versionreview.com/tothiq/payment-fail.php"
        
        if serializer.is_valid():
            
            payment_amount = membership_net_amount
            payment_discount_type = "percentage"
            payment_discount_amount = 0
            payment_discount_rate = 0


            if payment_discount_type=="percentage" :
                payment_discount_amount = (payment_amount*payment_discount_rate)/10
            else :
                payment_discount_amount = payment_discount_rate
            
            net_amount = round(payment_amount - payment_discount_amount,3)
            print(net_amount)
            if net_amount < 1:
                response_data = {
                    'status': 400,
                    'message': 'Invalid Amount.',
                    'data': {}    
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            #payment_insert_data = serializer.save(user=request.user)  
            
            data = {
                'user':request.user,
                'payment_type': payment_type,
                'payment_amount': payment_amount,
                'discount_type': payment_discount_type,
                'discount_rate': payment_discount_rate,
                'discount_amount': payment_discount_amount,
                'net_amount': net_amount,
                'payment_method': payment_method,
                'payment_status': 'pending',
                'purchase_id': membership.id
            }
            payment = Payment(**data)
            payment.save()
            payment_track_id = payment.id

            if payment_method == "knet":
                
                #knet live environment
                # knet_transport_id = '223401'
                # knet_transport_password = '6SdkmprU'
                # knet_terminal_key = 'FXW1F6T1E60B736X'

                #knet test environment
                knet_transport_id = '201701'
                knet_transport_password = '201701pg'
                knet_terminal_key = 'N67B2W142Q8UZY2V'
                
                knet_test_mode = True

                if knet_test_mode:
                    knet_payment_url = 'https://kpaytest.com.kw/kpg/PaymentHTTP.htm?param=paymentInit&trandata='
                else:
                    knet_payment_url = 'https://kpay.com.kw/kpg/PaymentHTTP.htm?param=paymentInit&trandata='
                    
                knet_url_string = 'id=' + knet_transport_id + '&password=' + knet_transport_password + '&amt=' + str(net_amount) + '&trackid=' + str(payment_track_id) + '&currencycode=414&langid=USA&action=1&udf1=' + payment_type + '&udf2=' + str(purchase_id)+'&responseURL=' + payment_response_url + '&errorURL=' + payment_fail_url
                
                #knet_url_string ='id=223401&password=6SdkmprU&action=1&langid=USA¤cycode=414&amt=1.5&responseURL=https://www.ibuysafety.com/knet/response&errorURL=https://www.ibuysafety.com/knet/response&trackid=413240845&udf1=862'
                
                

                #knet_terminal_key_encoded = base64.urlsafe_b64encode(knet_terminal_key).decode()
                #cipher_suite = Fernet(knet_terminal_key_encoded)
                #knet_url_string_encrypted = cipher_suite.encrypt(knet_url_string.encode()).decode()

                #print('knet vb url : ','https://versionreview.com/tothiq/knet-enc.php?enc='+ base64.b64encode(knet_url_string.encode()).decode())
                knetenc_url = 'https://versionreview.com/tothiq/knet-enc.php?enc='+ base64.b64encode(knet_url_string.encode()).decode()  # Replace with your desired URL
                
                try:
                    print('knet enc url ',knetenc_url)
                    response = urllib.request.urlopen(knetenc_url)
                    knet_url_string_encrypted = response.read().decode('utf-8')
                    print(knet_url_string_encrypted)
                except urllib.error.URLError as e:
                    print("Error: ", e)

                knet_payment_url+= knet_url_string_encrypted + '&tranportalId=' + knet_transport_id+'&responseURL=' + payment_response_url + '&errorURL=' + payment_fail_url
                
                response_data = {
                    'status': 200,
                    'message': 'Payment initiated. Kindly process the payment',
                    'data': {
                        'payment_url': knet_payment_url,
                        'payment_id': payment.id
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)

            #myfatoorah payment gateway payment init function
            elif payment_method == "myfatoorah" :
                if payment_type == "membership":
                    purchase_id = request.data.get('purchase_id')
                    try:
                        membership = Membership.objects.get(id=purchase_id)
                        net_amount = membership.discount_price
                        net_amount = float(net_amount)
                    except (ValueError, Membership.DoesNotExist):
                        return Response({"status": 400, "message": "Invalid purchase id for membership type.", "data": {}})
                    
                if payment_type == "contracts":
                    purchase_id = request.data.get('purchase_id')
                    try:
                        # Check if purchase_id is a valid numeric value
                        purchase_id = int(purchase_id)  # Assuming purchase_id is an integer, you can use `float` if it can be a decimal
                        general_settings = GeneralSettings.objects.first()  # Assuming there's only one row in the GeneralSettings table
                        contracts_price = general_settings.contracts_price
                        contracts_price = float(contracts_price)
                        net_amount = contracts_price * purchase_id
                        net_amount = float(net_amount)
                    except (ValueError, GeneralSettings.DoesNotExist):
                        return Response({"status": 400, "message": "Invalid contracts price in general settings", "data": {}})
                        
                if payment_type == "users":
                    purchase_id = request.data.get('purchase_id')
                    try:
                        # Check if purchase_id is a valid numeric value
                        purchase_id = int(purchase_id)  # Assuming purchase_id is an integer, you can use `float` if it can be a decimal
                        general_settings = GeneralSettings.objects.first()  # Assuming there's only one row in the GeneralSettings table
                        users_price = general_settings.users_price
                        users_price = float(users_price)
                        net_amount = users_price * purchase_id
                        net_amount = float(net_amount)
                    except (ValueError, GeneralSettings.DoesNotExist):
                        return Response({"status": 400, "message": "Invalid users price in general settings", "data": {}})

                
                        # Calculate the net amount after discount
                # net_amount = total_amount - discount_amount
                    
                # Initaite Payment request data
                initiatepay_request = {
                    "InvoiceAmount": net_amount,
                    "CurrencyIso": "KWD"
                }

                try:
                    # Getting the value of payment Method Id
                    payment_method = initiate_payment(initiatepay_request)

                    # Creating a simplified list for payment methods
                    payment_method_list = []
                    for item in range(len(payment_method)):
                        if payment_method[item]["IsDirectPayment"] == False:
                            y = [payment_method[item].get(key) for key in ["PaymentMethodEn", "PaymentMethodId"]]
                            payment_method_list.append(y)


                    # Get the payment method key.
                    while True:
                        #payment gateway
                            # [['QPay', 7], ['MADA', 6], ['KNET', 1], ['Apple Pay', 11], ['VISA/MASTER', 2], ['STC Pay', 14], ['UAE Debit Cards', 8], ['AMEX', 3], ['Apple Pay (Mada)', 25], ['GooglePay', 32], ['Benefit', 5]]
                            # 1 : knet
                            # 2 : visa/master
                            # 11 : Apple pay
                            # 32 : Google Pay
                        
                        #payment_method_id = 2 #input("Kindly enter the number equivalent to the required payment method: ")
                        if request.data.get('pmid') != None  :    
                            payment_method_id = int(request.data.get('pmid'))
                        else :
                            payment_method_id = 1
                        
                        try:
                            if int(payment_method_id) in [el[1] for el in payment_method_list]:
                                break
                            else:
                                print("Kindly enter a correct payment method id")
                        except:
                            print("The input must be a number")

                    # Based on the initiate payment response, we select the value of reference number to choose payment method
                    
                    if payment_type=="membership" :
                        invoice_items = [{
                            'ItemName': payment_type,  # ISBAN, or SKU
                            'Quantity': 1,  # Item's quantity
                            'UnitPrice': net_amount,  # Price per item
                        }]
                    if payment_type =='contracts':
                        invoice_items = [{
                            'ItemName': payment_type,  # ISBAN, or SKU
                            'Quantity': purchase_id,  # Item's quantity
                            'UnitPrice': contracts_price,  # Price per item
                        }]
                    if payment_type =='users':
                        invoice_items = [{
                            'ItemName': payment_type,  # ISBAN, or SKU
                            'Quantity': purchase_id,  # Item's quantity
                            'UnitPrice': users_price,  # Price per item
                        }]
                        
                    # Execute Payment Request
                    executepay_request = {
                        #"paymentMethodId" : payment_method_id,
                        "NotificationOption": "LNK",  # Mandatory Field ("LNK", "SMS", "EML", or "ALL")
                        "InvoiceValue"    : net_amount,
                        "CallBackUrl"     : payment_response_url,
                        "ErrorUrl"        : payment_fail_url,
                        
                        # Fill optional data
                        # "CustomerName": full_name if user_type in ["individual User", "Business User"] and full_name else "tothiq user",
                        "DisplayCurrencyIso" : "KWD",
                        #"MobileCountryCode"  : "+965",
                        #"CustomerMobile"     : user.phone_number,
                        #"CustomerEmail"      : user.email,
                        "Language"           : "en", #or "ar"
                        "CustomerReference"  : purchase_id,
                        #"CustomerCivilId"    : user.civil_id,
                        "UserDefinedField"   : payment_type,
                        #"ExpiryDate"         : "", #The Invoice expires after 3 days by default. Use "Y-m-d\TH:i:s" format in the "Asia/Kuwait" time zone.
                        #"SourceInfo"         : "Pure PHP", #For example: (Laravel/Yii API Ver2.0 integration)
                        #"CustomerAddress"    : "customerAddress",
                        "InvoiceItems"       : invoice_items,
                    }
                    
                    # If the user type is "individual User" or "Business User" and user has a full name, use the full name
                    if user.user_type in ["individual User", "Business User"] and user.full_name:
                        executepay_request["CustomerName"] = user.full_name
                    # If the user type is "Business Admin," use the company_name
                    elif user.user_type == "Business Admin":
                        executepay_request["CustomerName"] = user.company_name if hasattr(user, 'company_name') and user.company_name else "tothiq user"
                    # Otherwise, use "tothiq user"
                    else:
                        executepay_request["CustomerName"] = "tothiq user"
                        

                    #to create direct payment link
                    #[invoice_id,invoice_url] = execute_payment(executepay_request)
                    
                    [invoice_id,invoice_url] = send_payment(executepay_request)

                    # print(invoice_url)
                    # print(invoice_id)
                    
                    response_data = {
                        'status': 200,
                        'message': 'Payment initiated. Kindly process the payment.',
                        'data': {
                                'payment_url': invoice_url,
                                'payment_id': payment.id,
                            }
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                
                except:
                    ex_type, ex_value, ex_traceback = sys.exc_info()
                    print("Exception type : %s " % ex_type.__name__)
                    print("Exception message : %s" % ex_value)
            else:
                response_data = {
                    'status': 200,
                    'message': 'Invalid Payment Method',
                    'data': {}
                }
                return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





#payment response process
class PaymentResponseAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request,*args, **kwargs):
        user = request.user  # Retrieve the authenticated user
        # user_id = user.id 
        payment_status = request.data.get('payment_status')
        payment_id = request.data.get('payment_id')
        # print("Current user_id:",user_id)


        # if not payment_status :
        #     return Response({'status':400,'message':'payment_status is requried'})
        
        if not payment_id :
            return Response({'status':400,'message':'Payment id is requried.'})

        getpay_request = {
            "Key": payment_id,
            "KeyType": "paymentId"
        }

        try: 
            payment_data = get_payment_status(getpay_request)
            # print(payment_data)
        except Exception as ex:
            ex_type = type(ex).__name__
            ex_value = str(ex)
            ("Exception type : %s " % ex_type)
            ("Exception message : %s" % ex_value)

            response_data = {
                'status': 200,
                'message': 'Payment failed.',
                'data': {
                    'error': ex_type,
                    'errorText': ex_value
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)


        if payment_data:

            payment_status = payment_data['InvoiceStatus']       
            if payment_status == 'Paid':
                payment_status = 'success'
            else:
                payment_status = 'failed'
            purchase_id = payment_data['CustomerReference']
            print(purchase_id)
            payment_amount = payment_data['InvoiceValue']
            print(payment_amount)
            payment_type = payment_data['UserDefinedField']
            print(payment_type)

            try:
                payment = Payment.objects.get(id=purchase_id)
                payment.payment_status = payment_status
                # print(payment.payment_status)
                
                if payment_data['InvoiceTransactions']:
                    transaction = payment_data['InvoiceTransactions'][0]  # Access the first transaction
                    print(transaction,'transaction')
                    payment.tr_id= transaction['TransactionId']
                    print(payment.tr_id,'payment.tr_id')
                    payment.ref_code = transaction['ReferenceId']
                    print(payment.ref_code,'payment.ref_code')
                    payment.auth_code = transaction['AuthorizationId']
                    print(payment.auth_code,'payment.auth_code')
                    
                    # Loop through all transactions and concatenate track_ids
                    track_ids = [transaction['TrackId'] for transaction in payment_data['InvoiceTransactions']]
                    payment.track_id = ', '.join(track_ids)
                    print(payment.track_id,'payment.track_id')
                    
                    # Note: The previous line assigns a comma-separated list of track_ids to payment.track_id
                    
                    payment.payment_id = transaction['PaymentId']
                    payment.save()
                else:
                    # Handle the case where there are no InvoiceTransactions
                    pass

            except Payment.DoesNotExist:
                pass

            if payment_status == "success":
                if payment_type == "membership":
                    membership_id = purchase_id
                    try:
                        membership = Membership.objects.get(id=membership_id)
                        membership_data = {
                            'id': membership.id,
                            'name': membership.membership_name,
                            # Include other fields/columns as needed
                        }
                    except Membership.DoesNotExist:
                        pass

                    membership_start_date = date.today()
                    membership_end_date = membership_start_date + timedelta(days=membership.day_availability)

                    UserMembership1 = UserMembership.objects.create(
                        user=user,
                        membership=membership,
                        start_date=membership_start_date,
                        end_date=membership_end_date,
                        active_status='inactive'
                    )

                    contracts_count = membership.number_of_contract  # Assign the value for contracts_count
                    parties_count = membership.number_of_parties  # Assign the value for parties_count

                    contract_history = contract_histroy.objects.create(
                        user=user,
                        contracts=contracts_count,
                        parties=parties_count,
                        users=0,
                        action_type='add',
                        action_info=f"{membership.membership_name} membership purchase.",
                        created_at=datetime.now()
                    )

                    # Serialize the UserMembership1 object to a dictionary
                    user_membership_data = {
                        # 'id': UserMembership1.id,
                        'user_id': UserMembership1.user.id,
                        'membership_id': UserMembership1.membership.id,
                        'membership_name': membership.membership_name,
                        'membership_start_date': UserMembership1.start_date.strftime('%Y-%m-%d'),
                        'membership_end_date': UserMembership1.end_date.strftime('%Y-%m-%d'),
                        'active_status': UserMembership1.active_status,
                        # Include other fields from UserMembership1 as needed
                    }

                    # Create the response data dictionary
                    response_data = {
                        'status': 200,
                        'message': f"{membership.membership_name} membership has been upgraded successfully.",
                        'data': 
                            # 'membership_data': membership_data,
                            user_membership_data,
                    }
                    
                    return Response(response_data, status=status.HTTP_200_OK)

                elif payment_type == "contracts":
                    contract_history = contract_histroy.objects.create(
                                        user=user,
                                        contracts=int(purchase_id),
                                        parties=0, 
                                        users=0,  
                                        action_type='add',
                                        action_info="Additional contracts purchased.",
                                        created_at=datetime.now()
                                    )

                    response_data = {
                        'status': 200,
                        'message': f"Additional {purchase_id} contracts purchased successfully.",
                        'data': {
                            'user_id': contract_history.user.id,
                            'contracts': contract_history.contracts,
                            'parties': contract_history.parties,
                            'action_type': contract_history.action_type,
                            'action_info': contract_history.action_info,
                        }
                    }
                    return Response(response_data, status=status.HTTP_200_OK)

                elif payment_type == "users":
                    contract_history = contract_histroy.objects.create(
                                        user=user,
                                        users=purchase_id,
                                        parties=0, 
                                        contracts=0,  
                                        action_type='add',
                                        action_info="Additional users purchased.",
                                        created_at=datetime.now()
                                    )
                    


                    response_data = {
                        'status': 200,
                        'message': f"Additional {purchase_id} business users purchased successfully.",
                        'data': {
                            'user_id': contract_history.user.id,
                            'users': int(contract_history.users),
                            'parties': contract_history.parties,
                            'action_type': contract_history.action_type,
                            'action_info': contract_history.action_info,
                        }
                    }
                    return Response(response_data, status=status.HTTP_200_OK)

            else:
                response_data = {
                    'status': 400,
                    'message': 'Invalid payment response.',
                    'data': {}
                }
                return Response(response_data, status=status.HTTP_200_OK)


                
                
                
                
                
#coupon management
class CouponApplyView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        payment_charges = 0
        # Get request parameters
        purchase_type = request.data.get('purchase_type')
        purchase_id = request.data.get('purchase_id')
        coupon_code = request.data.get('coupon_code')

        if not purchase_type:
            return Response({'status': 400, 'message': 'Purchase type is required.'}, status=status.HTTP_200_OK)

        if not purchase_id:
            return Response({'status': 400, 'message': 'Purchase id required.'}, status=status.HTTP_200_OK)

        if not coupon_code:
            return Response({'status': 400, 'message': 'Coupon code required.'}, status=status.HTTP_200_OK)

        if purchase_type not in ['membership', 'contracts', 'users']:
            return Response({'status': 400, 'message': 'Invalid purchase type.'}, status=status.HTTP_200_OK)

        # Check if the coupon exists and is active
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code, active_status='active')
        except Coupon.DoesNotExist:
            return Response({'status': 400, 'message': 'Invalid coupon code.'}, status=status.HTTP_200_OK)

        # Check the coupon start date and end date
        current_datetime = timezone.now()
        if coupon.start_datetime and coupon.start_datetime > current_datetime:
            return Response({'status': 400, 'message': 'Coupon is not yet valid.'}, status=status.HTTP_200_OK)
        if coupon.end_datetime and coupon.end_datetime < current_datetime:
            return Response({'status': 400, 'message': 'Coupon has expired.'}, status=status.HTTP_200_OK)

        # Check if the coupon is valid for the purchase_type
        if coupon.discount_for != purchase_type and  'all' not in coupon.discount_for :
            message = format_lazy("Coupon is not valid for {} purchase.", purchase_type)
            return Response({'status': 400, 'message': message}, status=status.HTTP_200_OK)

        # Check if the coupon is valid for the user (if coupon is for selected users)
        user_id = request.user.id  # Get the user ID from the request, adjust this based on your authentication setup
        if "0" not in coupon.selected_users  and str(user_id) not in coupon.selected_users.split(','):
            return Response({'status': 400, 'message': 'Coupon is not valid for this user.'}, status=status.HTTP_200_OK)

        # Check the total number of coupon usages and user-wise usage
        if coupon.limited_coupon_per_Customer is not None:
            # Count coupon usage for this user
            user_coupon_usage = Payment.objects.filter(user_id=user_id, coupon_code=coupon_code).exclude(payment_status='pending').count()

            if user_coupon_usage >= coupon.limited_coupon_per_Customer:
                return Response({'status': 400, 'message': 'Coupon usage limit reached for this user.'}, status=status.HTTP_200_OK)
            

        # Fetch the actual total amount for the purchase
        total_amount = 0    
        if purchase_type == 'membership':
            # Assuming Membership model has a 'membership_amount' field
            try:
                membership = Membership.objects.get(id=purchase_id)
                total_amount = membership.membership_amount
            except Membership.DoesNotExist:
                return Response({'status': 400, 'message': 'Invalid membership id.'}, status=status.HTTP_200_OK)
            
        elif purchase_type == 'contracts':
            # Assuming Settings model has a 'contracts_price' field
            try:
                settings = GeneralSettings.objects.get(id=1)  # Assuming there's only one row in the settings table
                one_user_price = settings.contracts_price
                total_amount = one_user_price * Decimal(purchase_id)
            except GeneralSettings.DoesNotExist:
                return Response({'status': 400, 'message': 'Contracts price not found.'}, status=status.HTTP_200_OK)

        elif purchase_type == 'users':
            # Assuming Settings model has a 'users_price' field
            try:
                settings = GeneralSettings.objects.get(id=1)  # Assuming there's only one row in the settings table
                one_user_price = settings.users_price
                total_amount = one_user_price * Decimal(purchase_id)
            except GeneralSettings.DoesNotExist:
                return Response({'status': 400, 'message': 'Users price not found.'}, status=status.HTTP_200_OK)

        # Calculate the coupon discount based on discount type
        if coupon.discount_type == 'percentage':
            discount_amount = (total_amount * coupon.discount_rate) / Decimal('100')
        elif coupon.discount_type == 'fixed_price':
            discount_amount = coupon.value
        else:
            return Response({'status': 400, 'message': 'Invalid discount type.'}, status=status.HTTP_200_OK)

        # Calculate the net amount after discount
        net_amount = total_amount - discount_amount + payment_charges
        data = {
            'total_amount': total_amount,
            'discount_amount': discount_amount,
            'net_amount': net_amount
        }
        # Return success response with details
        return Response({
            'status': 200,
            'message': 'Coupon applied successfully.',
            'data': data
        }, status=status.HTTP_200_OK)
