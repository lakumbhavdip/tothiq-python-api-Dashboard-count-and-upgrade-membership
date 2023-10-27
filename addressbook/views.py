from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AddressBooklistSerializer, AddressBookdetailSerializer, contactsuggestSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Users, Addressbook
from rest_framework.generics import CreateAPIView
from django.core.mail import send_mail
from contracts.models import business_contract_party
from contracts.serializers import BusinessContractPartySerializer
from django.core.mail import EmailMessage
from tothiq import settings



# add contact class
class AddressBookAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        civil_id = request.data.get('civil_id')
        email = request.data.get('email')
        
        if not civil_id:
            return Response({"status": "400", "message": "Civil id is required."}, status=status.HTTP_200_OK)
        
        if not email:
            return Response({"status": "400", "message": "Email is required."}, status=status.HTTP_200_OK)

        user = self.request.user

        if user.civil_id == civil_id:
            return Response({"status": "400", "message": "Cannot add own Civil id to address book."}, status=status.HTTP_200_OK)

        try:
            user_obj = Users.objects.get(civil_id=civil_id, user_type='Individual User')
            active_status = 'active'  # Email exists in Users table with user_type='Individual User', so set active_status to 'active'
        except Users.DoesNotExist:
            user_obj = None
            active_status = 'inactive'  # Email does not exist in Users table or does not have user_type='Individual User', so set active_status to 'inactive'
            
        addressbook_obj, created = Addressbook.objects.get_or_create(user=user, civil_id=civil_id, defaults={'active_status': active_status, 'email': email})
        
        if not created:
            return Response({"status": "400", "message": "You have already added this user in your address book."}, status=status.HTTP_200_OK)

        if user_obj:
            recipient_email = user_obj.email
            send_mail(
                'Civil ID Added',
                f'Your Civil ID {civil_id} has been added to your address book.',
                'sender@example.com',
                [recipient_email],
                fail_silently=False,
            )

        return Response({'status': status.HTTP_200_OK, "message": "This Civil id added in Addressbook"}, status=status.HTTP_200_OK)









# contact suggest when create contact
class contactsuggestAPIView(APIView):
    def post(self, request, *args, **kwargs):
        civil_id = request.data.get('civil_id')

        if not civil_id:
            return Response({"status": 400, "message": "Civil ID is required field."}, status=status.HTTP_200_OK)

        if civil_id.isdigit() and 12 <= len(civil_id) <= 12:
            filtered_users = Users.objects.filter(
                civil_id__startswith=civil_id, user_type="Individual User").first()
            if filtered_users:
                serializer = contactsuggestSerializer(filtered_users)
                return Response({"status": 200, "message": "User filtered successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": 404, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"status": 400, "message": "Civil id is not valid."}, status=status.HTTP_200_OK)





# fetch contact list filter class
class AddressBookListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        start_with = request.data.get('start_with', None)
        text = request.data.get('text', None)
        contact_type = request.data.get('contact_type', 'users')

        if start_with is not None:
            if not start_with.isalpha() or len(start_with) != 1:
                return Response({"status": 400, "message": "Invalid input"}, status=status.HTTP_200_OK)

        address_books = Addressbook.objects.filter(user_id=user_id)
        filtered_books = []

        for book in address_books:
            user = Users.objects.filter(civil_id=book.civil_id).first()
            if user:
                full_name = user.full_name
                email = user.email
                phone_number = user.phone_number
                active_status = book.active_status
                nationality = user.nationality
                image = user.image
                invite_date = book.created_at  # Add invite_date parameter

                if contact_type == 'users' and active_status == 'active':
                    if start_with is None or (full_name and full_name.upper().startswith(start_with.upper())):
                        if text is None or (full_name and text.lower() in full_name.lower()):
                            filtered_books.append({
                                "addressbook_id": book.id,
                                "full_name": full_name,
                                "email": email,
                                "phone_number": phone_number,
                                "active_status": active_status,
                                "nationality": nationality,
                                "user": user,
                                "image": image,
                                "invite_date": invite_date
                            })

            user = Addressbook.objects.filter(civil_id=book.civil_id).first()
            if user:
                email = book.email
                active_status = book.active_status
                invite_date = book.created_at  # Add invite_date parameter
                
            if contact_type == 'invites' and active_status == 'inactive':
                if start_with is None or (email and email.upper().startswith(start_with.upper())):
                    if text is None or (email and text.lower() in email.lower()):
                        filtered_books.append({
                            "addressbook_id": book.id,
                            "email": email,
                            "active_status": active_status,
                            "invite_date": invite_date
                        })
            
        sorted_books = sorted(filtered_books, key=lambda x: x.get('full_name', '') or x.get('email', ''))
        
        serializer = AddressBooklistSerializer(sorted_books, many=True, context={'request': request})
        return Response({"status": 200, "message": "Contact list fetched successfully", 'data': serializer.data},
                        status=status.HTTP_200_OK)

        
        

#delete invite API view
from django.shortcuts import get_object_or_404

class DeleteInviteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        addressbook_id = request.data.get('addressbook_id')

        # Check if addressbook_id is present in request parameters
        if not addressbook_id:
            return Response({'status': 400, 'message': 'Addressbook id is required'}, status=status.HTTP_200_OK)

        # Get the address book instance if it exists
        addressbook = get_object_or_404(Addressbook, id=addressbook_id)

        # Check if the address book is assigned to the current user
        if addressbook.user != request.user:
            return Response({'status': 400, 'message': 'User not found'}, status=status.HTTP_200_OK)

        # Get the civil_id assigned to the addressbook_id
        civil_id = addressbook.civil_id

        # Delete the addressbook entry
        addressbook.delete()
        
        # Remove the user from the Users table based on the associated civil_id
        Users.objects.filter(civil_id=civil_id).delete()

        return Response({'status': 200, 'message': 'Invite deleted successfully'}, status=status.HTTP_200_OK)





# fetch contact details class
from contracts.serializers import ContractPartylistSerializerWEB
from contracts.models import contract_party,contracts
from django.db.models import Q

class AddressBookdetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def format_status(self, status):
        words = status.split('_')
        formatted_status = '-'.join([word.capitalize() for word in words])
        return formatted_status

    def fetch_contracts(self, user, contact_email):
        contract_dict = {}

        # Fetch contract IDs from business_contract_party or contract_party table based on user type
        contract_ids = []

        # Filter contract IDs based on the user's email
        if user.user_type == 'Business User':
            contract_ids = business_contract_party.objects.filter(
                Q(first_party_email=contact_email) | Q(second_party_email=contact_email)
            ).values_list('contract', flat=True)
        else:
            contract_ids = contract_party.objects.filter(
                Q(first_party_email=contact_email) | Q(second_party_email=contact_email)
            ).values_list('contract', flat=True)

        # Fetch the contract objects using the contract IDs and the user's ID
        contracts_data = contracts.objects.filter(id__in=contract_ids, user=user)

        # Loop through all the contract records and store them in the contract_dict
        for contract in contracts_data:
            if contract.id not in contract_dict:
                contract_dict[contract.id] = {
                    'id': contract.id,
                    'contract_title': contract.contract_title,
                    'created_at': contract.created_at,
                    'status': self.format_status(contract.status),
                    'contract_party': {'first_party_user': [], 'second_party_user': []},
                }

            if user.user_type == 'Business User':
                business_party_data = business_contract_party.objects.filter(contract=contract)
                business_party_serializer = BusinessContractPartySerializer(
                    business_party_data, many=True, context={'request': self.request})
                
                for business_party in business_party_serializer.data:
                    if business_party['first_party_user']:
                        contract_dict[contract.id]['contract_party']['first_party_user'].append(business_party['first_party_user'])
                    if business_party['second_party_user']:
                        contract_dict[contract.id]['contract_party']['second_party_user'].append(business_party['second_party_user'])
            else:
                contract_party_data = contract_party.objects.filter(contract=contract)
                contract_party_serializer = ContractPartylistSerializerWEB(
                    contract_party_data, many=True, context={'request': self.request})
                
                for party in contract_party_serializer.data:
                    if party['first_party_user']:
                        contract_dict[contract.id]['contract_party']['first_party_user'].append(party['first_party_user'])
                    if party['second_party_user']:
                        contract_dict[contract.id]['contract_party']['second_party_user'].append(party['second_party_user'])

        # Convert the accumulated contracts into a list
        return list(contract_dict.values())

    def post(self, request, *args, **kwargs):
        user = request.user
        contact_id = request.data.get('contact_id')
        if not contact_id:
            return Response({'status': 400, 'message': 'Contact id is required'}, status=status.HTTP_200_OK)

        try:
            address_book = Addressbook.objects.get(id=contact_id)
        except Addressbook.DoesNotExist:
            return Response({'status': 400, 'message': 'Contact not found'}, status=status.HTTP_200_OK)

        if address_book.user.id != request.user.id:
            return Response({'status': 400, 'message': 'This Contact id is not available for this user.'}, status=status.HTTP_200_OK)

        # User not found, fetch address book data
        civil_ids = [address_book.civil_id]
        users = Users.objects.filter(civil_id__in=civil_ids, user_type='Individual User')
        if users.exists():
            serializer = AddressBookdetailSerializer(users[0], context={'request': request})

            # Fetch contracts associated with the contact_email
            contact_email = address_book.email
            contracts_data = self.fetch_contracts(user, contact_email)

            address_book_data = {
                "email": address_book.email,
                "active_status": address_book.active_status,
                "created_at": address_book.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "contracts": contracts_data  # Add contracts to the response data
            }

            response_data = {
                'status': status.HTTP_200_OK,
                "message": "Contact details fetched successfully.",
                "data": {
                    "full_name": serializer.data.get('full_name'),
                    "email": serializer.data.get('email'),
                    "phone_number": serializer.data.get('phone_number'),
                    "nationality": serializer.data.get('nationality'),
                    "gender": serializer.data.get('gender'),
                    "image": serializer.data.get('image'),
                    "created_at": serializer.data.get('created_at'),
                    "contracts": address_book_data["contracts"]
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # User not found, return Addressbook data
            address_book_data = {
                "email": address_book.email,
                "active_status": address_book.active_status,
                "created_at": address_book.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            response_data = {
                'status': 200,
                'message': 'Contact details fetched successfully.',
                'data': address_book_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
