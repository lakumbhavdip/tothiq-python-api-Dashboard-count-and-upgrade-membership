from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Folder, categories, template, contracts, contract_party, Users, business_contract_party
from rest_framework.permissions import IsAuthenticated
from contracts.serializers import FolderListSerializer, FoldernamelistSerializer, TemplatelistSerializerEnglish,TemplatelistSerializerArabic, AddTemplateSerializer, ContractSerializer, ContractPartySerializer, ContractStatusUpdateSerializer, PartyUserdetailsSerializer, AddappendixSerializer,TemplateImageUploadSerializer, contractsdetailSerializer, ContractPartyDetailsSerializer,ContractPartylistSerializerAPP,UpdateContractPartySerializer, ContractPartylistSerializerWEB,BusinessContractPartySerializer,CategorylistSerializerEnglish,CategorylistSerializerArabic
from rest_framework import generics
from datetime import datetime, date
from django.db.models import Q
from datetime import datetime, timedelta
from django.conf import settings
from masterapp.models import contract_histroy,Membership
from business_admin.models import business_info
from django.db.models.functions import Lower
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Folder

# add folder API in Contracts
class AddFolder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        parent_id = request.data.get('parent_id')
        folder_name = request.data.get('folder_name')
        folder_name_arabic = request.data.get('folder_name_arabic')

        # If folder_name is not provided in the request body
        if not folder_name:
            return Response({'status':400,'message': 'folder name is requried'}, status=status.HTTP_200_OK)
        
        if not folder_name_arabic:
            return Response({'status':400,'message': 'folder name arabic is requried'}, status=status.HTTP_200_OK)

        if folder_name == 'General':
            return Response({'status':400,'message': 'Cannot create a user in the "General" folder'}, status=status.HTTP_200_OK)

        existing_folder = Folder.objects.filter(
            user_id=user_id, folder_name=folder_name).exists() | Folder.objects.filter(
            user_id=user_id, folder_name_arabic=folder_name_arabic).exists()
        if existing_folder:
            return Response({'status':400,'message': 'Folder with this name already exists'}, status=status.HTTP_200_OK)

         # If parent_id is provided, check if it exists in the database and belongs to the current user
        if parent_id:
            try:
                parent_folder = Folder.objects.get(id=parent_id, user_id=user_id)
            except Folder.DoesNotExist:
                return Response({'status': 400, 'message': 'Parent folder does not exist.'}, status=status.HTTP_200_OK)

            # If parent folder exists, create a new folder with it as the parent
            new_folder = Folder(parent_id=parent_folder,
                                user_id=user_id, folder_name=folder_name,folder_name_arabic=folder_name_arabic,active_status='active')
            new_folder.save()
            return Response({'status': status.HTTP_200_OK, 'success': 'Folder added successfully'}, status=status.HTTP_200_OK)

        # If parent_id is not provided, create a new top-level folder
        new_folder = Folder(
            user_id=user_id, folder_name=folder_name,folder_name_arabic=folder_name_arabic, created_at=datetime.now(),active_status='active')
        new_folder.save()
        return Response({'status': status.HTTP_200_OK, 'success': 'Folder added successfully'}, status=status.HTTP_200_OK)


# List folder API in Contracts

class FolderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_folder_tree(self, folders, folder_id, language):
        folder = folders.get(id=folder_id)
        serialized_folder = FolderListSerializer(folder, context={'language': language}).data

        if language == 'Arabic':
            serialized_folder['folder_name'] = folder.folder_name_arabic

        children = folders.filter(parent_id=folder_id)
        serialized_children = FolderListSerializer(children, many=True, context={'language': language}).data

        # Recursively process children
        for child in serialized_children:
            child['children'] = self.get_folder_tree(folders, child['id'], language)

        if not serialized_children:  # If there are no children, set 'children' to an empty list
            serialized_folder['children'] = []

        return serialized_folder

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        language = request.data.get('language', 'English')
        folders = Folder.objects.filter(user_id=user_id, active_status='active')

        general_folder = folders.filter(folder_name__iexact='General').first()

        sorted_folders = folders.exclude(id=general_folder.id if general_folder else None).order_by('folder_name')

        folder_tree = []
        if general_folder:
            folder_tree.append(self.get_folder_tree(folders, general_folder.id, language))

        for folder in sorted_folders:
            folder_tree.append(self.get_folder_tree(folders, folder.id, language))

        folder_tree = [folder for folder in folder_tree if folder['parent_id'] is None]

        return Response({"status": 200, "message": "Folder list fetched successfully.", 'data': folder_tree}, status=status.HTTP_200_OK)

# folder name listing Contracts
class FolderNameListAPIView(generics.ListAPIView):
    serializer_class = FoldernamelistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Folder.objects.filter(user=user, active_status='active', parent_id=None).exclude(folder_name='General')
        queryset = queryset.annotate(lower_name=Lower('folder_name')).order_by('lower_name')
        return queryset

    def post(self, request):
        language = request.data.get('language', 'English')  # Default to 'English' if not provided

        queryset = self.get_queryset()

        folder_names = []
        for folder in queryset:
            if language == 'Arabic':
                folder_name = folder.folder_name_arabic if folder.folder_name_arabic else folder.folder_name
            else:
                folder_name = folder.folder_name
            folder_names.append({"id": folder.id, "folder_name": folder_name})

        data = {
            'status': status.HTTP_200_OK,
            'message': 'Folders name list fetched successfully.',
            'data': folder_names
        }
        return Response(data)
    
# folder all name listing Contracts
class FolderNameListallAPIView(generics.ListAPIView):
    serializer_class = FoldernamelistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Folder.objects.filter(user=user, active_status='active').exclude(folder_name='General')
        queryset = queryset.annotate(lower_name=Lower('folder_name')).order_by('lower_name')
        return queryset

    def post(self, request):
        language = request.data.get('language', 'English')  # Default to 'English' if not provided

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'language': language})

        data = {
            'status': status.HTTP_200_OK,
            'message': 'Folders name list fetched successfully.',
            'data': serializer.data
        }
        return Response(data)

#delete folder View
class DeleteFolderAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        folder_id = request.data.get('folder_id')

        if not folder_id:
            return Response({"status": 400, "message": "Folder id is required."}, status=status.HTTP_200_OK)

        try:
            folder = Folder.objects.get(id=folder_id, user_id=user.id)
        except Folder.DoesNotExist:
            return Response({"status": 400, "message": "Folder not found."}, status=status.HTTP_200_OK)

        # Check if the folder is the "General" folder
        if folder.folder_name.lower() == "general":
            return Response({"status": 400, "message": "The General folder cannot be deleted."}, status=status.HTTP_200_OK)

        # Get the general folder of the current login user
        general_folder, _ = Folder.objects.get_or_create(folder_name__iexact="General", user_id=user.id)

        # Update the folder_id of contracts assigned to the folder being deleted
        assigned_contracts = contracts.objects.filter(folder=folder)
        assigned_contracts.update(folder=general_folder)

        folder.active_status = 'inactive'
        folder.save()

        return Response({"status": 200, "message": "Folder is deleted successfully. All the associated folder are moved to General."}, status=status.HTTP_200_OK)

#edit folder
class EditFolderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        folder_id = request.data.get('folder_id', None)
        folder_name = request.data.get('folder_name', None)
        folder_name_arabic = request.data.get('folder_name_arabic', None)
        parent_id = request.data.get('parent_id', None)  # New parent_id to be updated

        if not folder_id:
            return Response({"status": 400, "message": "Folder id is required"}, status=status.HTTP_200_OK)

        if not folder_name:
            return Response({"status": 400, "message": "Folder name is required."}, status=status.HTTP_200_OK)
        
        if not folder_name_arabic:
            return Response({"status": 400, "message": "Folder name arabic is required."}, status=status.HTTP_200_OK)
        

        try:
            folder = Folder.objects.get(id=folder_id, user_id=user.id)            
        except Folder.DoesNotExist:
            return Response({"status": 404, "message": "Folder not found."}, status=status.HTTP_200_OK)

        if folder.folder_name.lower() == "general":
            return Response({"status": 400, "message": "Cannot change the name of the General folder."}, status=status.HTTP_200_OK)

        # Check if the specified parent_id exists for the user's folders
        if parent_id:
            try:
                parent_folder = Folder.objects.get(id=parent_id, user_id=user.id)
            except Folder.DoesNotExist:
                return Response({"status": 404, "message": "Parent folder not found."}, status=status.HTTP_200_OK)

            # Check if the parent_id belongs to a folder that is not the same as the current folder
            if parent_id != folder.parent_id:
                folder.parent_id = parent_folder  # Assign the instance, not just the ID    

        folder.folder_name = folder_name
        folder.folder_name_arabic = folder_name_arabic
        folder.save()

        return Response({"status": 200, "message": "Folder updated successfully."}, status=status.HTTP_200_OK)
    
    
# GET particular folder name and that parent_ids 
class FolderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        folder_id = request.data.get('folder_id')
        if not folder_id:
            return Response({'status': 400, 'message': 'Folder id is required'}, status=status.HTTP_200_OK)

        try:
            folder = Folder.objects.get(id=folder_id)

            # Check if the folder is assigned to the current user
            if folder.user != request.user:
                return Response({'status': 403, 'message': 'Folder not found'}, status=status.HTTP_200_OK)

            parent_id = self.get_parent_id(folder)
            folder_data = {
                'folder_name': folder.folder_name,
                'parent_id': parent_id,
                'folder_name_arabic': folder.folder_name_arabic
            }
            return Response({'status': 200, 'message': 'Folder details fetched successfully.', 'data': folder_data}, status=status.HTTP_200_OK)
        except Folder.DoesNotExist:
            return Response({'status': 404, 'message': 'Folder not found'}, status=status.HTTP_200_OK)

    def get_parent_id(self, folder):
        parent_id = folder.parent_id_id if folder.parent_id else None
        return parent_id


# add notification API
# class AddNotificationAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         title = request.data.get('title')
#         description = request.data.get('description')
#         notification_type = request.data.get('notification_type', '')
#         is_active = request.data.get('is_active', True)

#         if not title or not description or not notification_type:
#             return Response({"status":400,'message': 'Title, description, and notification_type are required fields'}, status=status.HTTP_400_BAD_REQUEST)

#         # Check if notification_type is valid
#         if notification_type not in dict(notification.NOTIFICATION_TYPES).keys():
#             return Response({"status":400,'message': 'Invalid notification type'}, status=status.HTTP_400_BAD_REQUEST)

#         existing_notification = notification.objects.filter(title=title, description=description).first()
#         if existing_notification:
#             return Response({"status":400,'message': 'Notification with the same title and description already exists'}, status=status.HTTP_400_BAD_REQUEST)

#         new_notification = notification.objects.create(title=title, description=description, is_active=is_active, notification_type=notification_type, user=user)
#         new_notification.save()

#         serializer = AddnotificationSerializer(new_notification)
#         return Response({"status": 200, "message": "Notification add successfully","data": serializer.data},status=status.HTTP_200_OK)




# liat category APIView
class CategoryListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        queryset = categories.objects.all()

        text_param = request.data.get('text', None)
        language_param = request.data.get('language', 'English')  # Default to 'English' if not provided

        # Validate language parameter
        if language_param not in ['English', 'Arabic']:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid language.',
            }, status=status.HTTP_400_BAD_REQUEST)

        if text_param:
            if language_param == 'English':
                queryset = queryset.filter(
                    Q(category_name__icontains=text_param) |
                    Q(category_name_arabic__icontains=text_param)
                )
            elif language_param == 'Arabic':
                queryset = queryset.filter(
                    Q(category_name_arabic__icontains=text_param) |
                    Q(category_name__icontains=text_param)
                )

        if language_param == 'English':
            serializer = CategorylistSerializerEnglish(queryset, many=True)
        elif language_param == 'Arabic':
            serializer = CategorylistSerializerArabic(queryset, many=True)
        
        data = serializer.data
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Categories list fetched successfully.',
            'data': data,
        }, status=status.HTTP_200_OK)






# list of template APIView
class TemplateListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        category_id = request.data.get('category_id', None)
        text_param = request.data.get('text', None)
        language_param = request.data.get('language', 'English')  # Default to 'English' if not provided

        if not category_id:
            return Response({'status': 400, 'message': 'Category ID is required.'}, status=400)

        try:
            # Check if the category ID exists
            category = categories.objects.get(id=category_id)
        except categories.DoesNotExist:
            return Response({'status': 400, 'message': 'Category ID does not exist.'}, status=400)

        # Validate language parameter
        if language_param not in ['English', 'Arabic']:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid language.',
            }, status=status.HTTP_400_BAD_REQUEST)

        # Filter templates by category ID and text parameter (if provided)
        queryset = template.objects.filter(category=category)
        if text_param:
            if language_param == 'Arabic':
                # When language is Arabic, we want to search for the text in both English and Arabic fields
                queryset = queryset.filter(Q(template_title__icontains=text_param) | Q(template_title_arabic__icontains=text_param))
            if language_param == 'English':
                queryset = queryset.filter(Q(template_title__icontains=text_param) | Q(template_title_arabic__icontains=text_param))
                

        if language_param == 'English':
            serializer = TemplatelistSerializerEnglish(
                queryset, many=True, context={'request': request})
        elif language_param == 'Arabic':
            serializer = TemplatelistSerializerArabic(
                queryset, many=True, context={'request': request})
        
        data = serializer.data

        if queryset.exists():
            return Response({'status': 200, 'message': 'Template list fetched successfully.', 'data': data})
        else:
            return Response({'status': 400, 'message': 'No templates found for the given category id.'}, status=400)




# template image APIView


class TemplateImageUploadAPIView(APIView):
    def post(self, request):
        serializer = TemplateImageUploadSerializer(data=request.data)

        if serializer.is_valid():
            image = serializer.validated_data['image']
            if image:
                # Save the image to the appropriate location
                file_path = default_storage.save(
                    f'tothiq_pic/templates/{image.name}', image)

                # Construct the absolute URL for the image
                image_url = request.build_absolute_uri(
                    settings.MEDIA_URL + file_path)

                response_data = {
                    'status': '200',
                    'message': 'Image uploaded successfully.',
                    'image_url': image_url
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'status': '400',
                    'message': 'No image file provided'
                }
                return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)



# add template APIView
class AddTemplateAPIView(APIView):
    def post(self, request):
        serializer = AddTemplateSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'message': 'Template added successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)



# add contracts APIView (Step-2)
from django.db.models import Sum
class AddContractAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            contract_start_date = serializer.validated_data.get('contract_start_date')
            contract_end_date = serializer.validated_data.get('contract_end_date')
            contract_title = serializer.validated_data.get('contract_title')
            contract_duration = request.data.get('contract_duration', False)
            contract_fees = request.data.get('contract_fees', False)
            arbitration = request.data.get('arbitration', None)
            jurisdiction = request.data.get('jurisdiction', None)
            

            # Conditional Validation
            if contract_duration and (not contract_start_date or not contract_end_date):
                return Response({'status': 400, 'message': 'contract_start_date and contract_end_date are required when contract_duration is true.'}, status=status.HTTP_200_OK)

            if contract_fees:
                required_fields = ['currency', 'contract_amount', 'contract_amount_words']
                for field in required_fields:
                    if not request.data.get(field):
                        return Response({'status': 400, 'message': f'{field} is required when contract_fees is true.'}, status=status.HTTP_200_OK)

            if arbitration is None and jurisdiction is None:
                            return Response({'status': 400, 'message': 'At least one of arbitration or jurisdiction must be required.'}, status=status.HTTP_200_OK)
                        
            # Calculate available_contract
            user_id = request.user.id
            total_contracts = contract_histroy.objects.filter(user_id=user_id).aggregate(total_contracts=Sum('contracts'))['total_contracts']
            total_contracts = total_contracts if total_contracts is not None else 0
            user_contracts = contracts.objects.filter(user_id=user_id).count()
            available_contracts = total_contracts - user_contracts
            
            # Check if folder is provided in the request data
            folder = serializer.validated_data.get('folder')
            if folder:
                folder_id = folder.id  # Retrieve the folder ID from the instance
                try:
                    folder = Folder.objects.get(id=folder_id, user_id=request.user.id)
                except Folder.DoesNotExist:
                    return Response({'status': 400, 'message': 'Folder does not exist.'}, status=status.HTTP_200_OK)

            if contract_start_date and contract_end_date and contract_start_date >= contract_end_date:
                return Response({'status': 400, 'message': 'Contract end date must be later than start date.'}, status=status.HTTP_200_OK)

            if contract_start_date and contract_start_date < date.today():
                return Response({'status': 400, 'message': 'Contract start date cannot be in the past.'}, status=status.HTTP_200_OK)
            
            existing_contract = contracts.objects.filter(user=request.user, contract_title=contract_title).first()
            if existing_contract:
                return Response({'status': 400, 'message': 'You have already created a contract with this name, please try another name.'}, status=status.HTTP_200_OK)

            if request.user.user_type == 'Business User':
                business_id = request.user.business_id
                if not business_id:
                    return Response({'status': 400, 'message': 'Business information not found for this user.'}, status=status.HTTP_200_OK)

                # Fetch the user_id associated with the business_id
                try:
                    business = business_info.objects.get(id=business_id)
                except business_info.DoesNotExist:
                    return Response({'status': 400, 'message': 'Business information not found.'}, status=status.HTTP_200_OK)
                
                business_user_id = business.user_id

                total_contracts_business = contract_histroy.objects.filter(user_id=business_user_id).aggregate(total_contracts=Sum('contracts'))['total_contracts']
                total_contracts_business = total_contracts_business if total_contracts_business is not None else 0
                used_contracts_business = contracts.objects.filter(user_id=business_user_id).count()
                available_contracts_business = total_contracts_business - used_contracts_business
                
                if available_contracts_business <= 0:
                    return Response({'status': 400, 'message': 'You have reached the maximum number of contracts allowed for your business membership type'}, status=status.HTTP_200_OK)

                available_contracts_response = available_contracts_business

                # Add business_id to the serializer data for contracts
                serializer.validated_data['business_id'] = business_id
            else:
                if available_contracts <= 0:
                    return Response({'status': 400, 'message': 'You have reached the maximum number of contracts allowed for your membership type'}, status=status.HTTP_200_OK)
                
                available_contracts_response = available_contracts

            contract = serializer.save(user=request.user)
            response_data = {
                'status': 200,
                'message': 'Contract added successfully.',
                'contract_id': contract.id,
                'available_contracts': available_contracts_response - 1  # Decrement available_contracts by 1 since a new contract is created
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_200_OK)




# Update contracts UpdateAPIView (Step-2)
class UpdateContractAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # Get contract_id from the request data
        contract_id = request.data.get('contract_id')

        # Check if contract_id is provided 
        if not contract_id:
            return Response({'status': 400, 'message': 'Contract id is required.'}, status=status.HTTP_200_OK)

        # Check if the contract exists and is associated with the current user
        try:
            contract = contracts.objects.get(id=contract_id, user=request.user)
        except contracts.DoesNotExist:
            return Response({'status': 403, 'message': 'You do not have permission to update this contract.'}, status=status.HTTP_200_OK)

        # Serialize the updated data
        serializer = ContractSerializer(contract, data=request.data, partial=True)

        if serializer.is_valid():
            # Check if contract_duration is provided and perform date validation
            if 'contract_duration' in serializer.validated_data:
                contract_duration = serializer.validated_data['contract_duration']

                if not contract_duration:
                    # Remove contract_start_date and contract_end_date if contract_duration is False
                    serializer.validated_data['contract_start_date'] = None
                    serializer.validated_data['contract_end_date'] = None
                else:
                    # If contract_duration is True, perform date validation
                    contract_start_date = serializer.validated_data.get('contract_start_date')
                    contract_end_date = serializer.validated_data.get('contract_end_date')
                    
                    # Check if required fields are missing when contract_fees is true
                    required_fields = ['contract_start_date', 'contract_end_date']
                    for field in required_fields:
                        if not serializer.validated_data.get(field):
                            return Response({'status': 400, 'message': f'{field} is required when contract_fees is true.'}, status=status.HTTP_200_OK)

                    if contract_start_date and contract_start_date < date.today():
                        return Response({'status': 400, 'message': 'Contract start date cannot be in the past.'}, status=status.HTTP_200_OK)
                    
                    if contract_start_date and contract_end_date and contract_start_date >= contract_end_date:
                        return Response({'status': 400, 'message': 'Contract end date must be later than start date.'}, status=status.HTTP_200_OK)

            # Check if contract_fees is provided and perform validation
            if 'contract_fees' in serializer.validated_data:
                contract_fees = serializer.validated_data['contract_fees']

                if not contract_fees:
                    # Remove currency, contract_amount, and contract_amount_words if contract_fees is False
                    serializer.validated_data.pop('currency', None)
                    serializer.validated_data.pop('contract_amount', None)
                    serializer.validated_data.pop('contract_amount_words', None)
                else:
                    # Check if required fields are missing when contract_fees is true
                    required_fields = ['currency', 'contract_amount', 'contract_amount_words']
                    for field in required_fields:
                        if not serializer.validated_data.get(field):
                            return Response({'status': 400, 'message': f'{field} is required when contract_fees is true.'}, status=status.HTTP_200_OK)

            # Save the updated contract
            serializer.save()

            return Response({'status': 200, 'message': f'Contract {contract_id} updated successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





# add party APIView (Step-3)
from rest_framework.exceptions import ValidationError
class AddPartyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get contract_id from the request data
        contract_id = request.data.get('contract_id')
        if not contract_id:
            return Response(
                {'status': 400, 'message': 'Contract id not provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Retrieve the contract based on contract_id
        contract = contracts.objects.filter(id=contract_id).first()
        if not contract:
            return Response(
                {'status': 404, 'message': 'Contract not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check the number of parties allowed based on membership type
        membership_type = request.user.membership_type
        user_type = request.user.user_type
        membership = Membership.objects.filter(user_type=user_type, membership_name=membership_type).first()
        if membership and membership.number_of_parties is not None:
            total_parties = contract_party.objects.filter(contract_id=contract_id).count() + len(request.data.get('first_party', [])) + len(request.data.get('second_party', []))
            if total_parties > membership.number_of_parties:
                return Response(
                    {"status": 400, "message": "You have reached the maximum number of parties allowed for your membership type."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create parties based on the input data
        first_party_data = request.data.get('first_party', [])
        second_party_data = request.data.get('second_party', [])

        # Iterate through the lists and insert corresponding pairs
        for i in range(max(len(first_party_data), len(second_party_data))):
            first_party_item = first_party_data[i] if i < len(first_party_data) else {}
            second_party_item = second_party_data[i] if i < len(second_party_data) else {}

            first_party_email = first_party_item.get('first_party_email')
            first_party_civil_id = first_party_item.get('first_party_civil_id')

            second_party_email = second_party_item.get('second_party_email')
            second_party_civil_id = second_party_item.get('second_party_civil_id')

            if first_party_email and first_party_civil_id:
                first_party_user = Users.objects.filter(email=first_party_email, civil_id=first_party_civil_id).first()
                if not first_party_user:
                    return Response(
                        {"status": 400, "message": f"User with the provided first party email and civil ID does not exist for entry {i + 1}."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            if second_party_email and second_party_civil_id:
                second_party_user = Users.objects.filter(email=second_party_email, civil_id=second_party_civil_id).first()
                if not second_party_user:
                    return Response(
                        {"status": 400, "message": f"User with the provided second party email and civil ID does not exist for entry {i + 1}."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            contract_party.objects.create(
                contract=contract,
                user=request.user,
                first_party_name=first_party_item.get('first_party_name'),
                first_party_email=first_party_email,
                first_party_civil_id=first_party_civil_id,
                second_party_name=second_party_item.get('second_party_name'),
                second_party_email=second_party_email,
                second_party_civil_id=second_party_civil_id,
            )

        return Response(
            {'status': 200, 'message': 'Parties added successfully.'},
            status=status.HTTP_200_OK
        )

# get contract party detail
class ContractPartyDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        contract_id = request.data.get('contract_id')

        if not contract_id:
            return Response({"status": 400, "message": "Contract id is requried."}, status=status.HTTP_200_OK)

        user = request.user  # Get the currently logged-in user

        parties = contract_party.objects.filter(
            contract_id=contract_id, user=user)

        if not parties.exists():
            return Response({"status": 400, "message": "Party details not found."}, status=status.HTTP_200_OK)

        serializer = ContractPartyDetailsSerializer(parties, many=True)

        return Response({"status": 200, "message": "Party details fetched successfully.", "data": serializer.data}, status=status.HTTP_200_OK)




# update party details (Step-3)
class UpdatePartyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        contract_id = request.data.get('contract_id')
        party_id = request.data.get('party_id')

        if not contract_id or not party_id:
            return Response(
                {'status': 400, 'message': 'Contract id and Party if must be provided.'},
                status=status.HTTP_200_OK
            )
        # Check if the contract belongs to the current user
        contract = contracts.objects.filter(id=contract_id, user=request.user).first()
        if not contract:
            return Response(
                {'status': 400, 'message': 'You do not have permission to update this contract party.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if the contract belongs to the party
        party = contract_party.objects.filter(id=party_id, contract=contract).first()
        if not party:
            return Response(
                {'status': 400, 'message': 'Party not found for the given contract.'},
                status=status.HTTP_200_OK
            )

        serializer = UpdateContractPartySerializer(party, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_id = request.user.id

        second_party_civil_id = serializer.validated_data.get(
            'second_party_civil_id')
        second_party_email = serializer.validated_data.get(
            'second_party_email')
        first_party_email = serializer.validated_data.get('first_party_email')
        first_party_civil_id = serializer.validated_data.get(
            'first_party_civil_id')  # Get the first_party_civil_id

        # Check if the user with the provided email exists
        if first_party_email:
            try:
                user = Users.objects.get(email=first_party_email)
            except Users.DoesNotExist:
                return Response({"status": 400, "message": "User with the provided first party email does not exist."}, status=status.HTTP_200_OK)

        # Check if the user with the provided civil ID exists
        if second_party_civil_id:
            user_exists = Users.objects.filter(
                civil_id=second_party_civil_id).exists()
            if not user_exists:
                return Response({"status": 400, "message": "User with the provided second party civil ID does not exist."}, status=status.HTTP_200_OK)

            # Check if the email is associated with the civil ID
            user = Users.objects.get(civil_id=second_party_civil_id)
            if second_party_email and user.email != second_party_email:
                return Response({"status": 400, "message": "The provided second party email does not match the civil ID."}, status=status.HTTP_200_OK)

        # Check if the user with the provided civil ID exists for the first party
        if first_party_civil_id:
            user_exists = Users.objects.filter(
                civil_id=first_party_civil_id).exists()
            if not user_exists:
                return Response({"status": 400, "message": "User with the provided first party civil ID does not exist."}, status=status.HTTP_200_OK)

            # Check if the email is associated with the civil ID
            user = Users.objects.get(civil_id=first_party_civil_id)
            if first_party_email and user.email != first_party_email:
                return Response({"status": 400, "message": "The provided first party email does not match the civil ID."}, status=status.HTTP_200_OK)
            
            serializer.save()

        return Response({"status": 200, "message": "Party details updated successfully."}, status=status.HTTP_200_OK)


# contract status update APIView
class ContractStatusUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ContractStatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        contract_id = request.data.get('contract_id')
        contract_status = request.data.get('status')
        pin_contract = request.data.get('pin')  # Default value is False if 'pin' is not provided

        if not contract_id:
            return Response({"status": 400, "message": "Contract id is required."}, status=status.HTTP_200_OK)

        if not contract_status:
            return Response({"status": 400, "message": "Status is required."}, status=status.HTTP_200_OK)

        try:
            instance = contracts.objects.get(pk=contract_id)
        except contracts.DoesNotExist:
            return Response({"status": 404, "message": "Contract not found."}, status=status.HTTP_200_OK)

        # Check if the contract belongs to the current user
        if instance.user != request.user:
            return Response({"status": 403, "message": "You do not have permission to update this contract."}, status=status.HTTP_200_OK)
        
        # Additional logic for delete_reason and cancellation_reason
        if contract_status == 'deleted':
            delete_reason = request.data.get('delete_reason')
            if not delete_reason:
                return Response({"status": 400, "message": "Delete reason is required for deleted status."}, status=status.HTTP_200_OK)
            instance.delete_reason = delete_reason

        if contract_status == 'cancelled':
            cancellation_reason = request.data.get('cancellation_reason')
            if not cancellation_reason:
                return Response({"status": 400, "message": "Cancellation reason is required for cancelled status."}, status=status.HTTP_200_OK)
            instance.cancellation_reason = cancellation_reason
       
        instance.status = contract_status
        instance.pin = pin_contract  # Set the 'pinned' field based on the 'pin' parameter
        instance.save()

        return Response({"status": 200, "message": "Contract status updated successfully."}, status=status.HTTP_200_OK)





# contract status list APIView
class ContractStatusListAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Add authentication permission

    def post(self, request):
        user = request.user  # Retrieve the current authenticated user

        folder_id_param = request.data.get('folder_id')

        # Fetch contracts data for the current user
        contracts_data = contracts.objects.filter(user=user)

        if folder_id_param:
            try:
                folder = Folder.objects.get(id=folder_id_param, user=user)
                contracts_data = contracts_data.filter(folder_id=folder.id)
            except Folder.DoesNotExist:
                return Response({"status": 404, "message": "Folder not found"}, status=status.HTTP_200_OK)

        # Count the number of contracts with each status
        status_counts = {'draft': 0, 'used': 0, 'under_review': 0, 'ready': 0, 'signed': 0, 'rejected': 0, 'deleted': 0, 'cancelled': 0}

        for contract in contracts_data:
            status_counts[contract.status] += 1

        # Calculate the "used" number as the total count of all other statuses
        used_number = sum(status_counts.values()) - status_counts['used']
        status_counts['used'] = used_number

        response_data = {
            'used': status_counts['used'],
            'draft': status_counts['draft'],
            'under_review': status_counts['under_review'],
            'ready': status_counts['ready'],
            'signed': status_counts['signed'],
            'rejected': status_counts['rejected'],
            'deleted': status_counts['deleted'],
            'cancelled': status_counts['cancelled']
        }

        return Response({"status": 200, "message": "Contract status list fetched successfully.", "data": response_data})





#contract List APIView (Mobile APP)
from django.urls import reverse

class ContractslistAPIViewAPP(APIView):
    permission_classes = [IsAuthenticated]

    # change the Status filed format like (under_review -> Under-Review)
    def format_status(self, status):
        words = status.split('_')
        formatted_status = '-'.join([word.capitalize() for word in words])
        return formatted_status

    def post(self, request):
        user = request.user

        status_param = request.data.get('status')
        contracts_data = contracts.objects.filter(user=user)

        if status_param:
            contracts_data = contracts.objects.filter(user=user, status=status_param)

        # Apply additional filters based on options
        option_param = request.data.get('option')
        if option_param == 'Last Month':
            last_month = datetime.now() - timedelta(days=30)
            contracts_data = contracts_data.filter(created_at__gte=last_month)
        elif option_param == 'Last Quarter':
            last_quarter = datetime.now() - timedelta(days=90)
            contracts_data = contracts_data.filter(created_at__gte=last_quarter)
        elif option_param == 'Last Year':
            last_year = datetime.now() - timedelta(days=365)
            contracts_data = contracts_data.filter(created_at__gte=last_year)

        # Text filter based on contract title (if parameter is provided)
        text_param = request.data.get('text')
        if text_param:
            contracts_data = contracts_data.filter(contract_title__icontains=text_param)

            if not contracts_data.exists():
                return Response({"status": 400, "message": "No contracts found matching the provided text."}, status=status.HTTP_200_OK)

        folder_id_param = request.data.get('folder_id')
        if folder_id_param:
            try:
                folder = Folder.objects.get(id=folder_id_param, user=user)
                contracts_data = contracts_data.filter(folder_id=folder.id)
            except Folder.DoesNotExist:
                return Response({"status": 400, "message": "Folder not found"}, status=status.HTTP_200_OK)

        # Order by 'created_at' in descending order
        contracts_data = contracts_data.order_by('-created_at')

        contracts_serializer = ContractPartylistSerializerAPP(contracts_data, many=True, context={'request': request})

        # Apply the format_status function to each contract's status field
        for contract in contracts_serializer.data:
            contract['status'] = self.format_status(contract['status'])

        response_data = {
            'status': status.HTTP_200_OK,
            'message': 'Contracts list fetched successfully.',
            'data': []
        }

        for contract in contracts_serializer.data:
            response_data['data'].append(contract)

        return Response(response_data)

 





# #contract List APIView (Web)
class ContractslistAPIViewWEB(APIView):
    permission_classes = [IsAuthenticated]

    def format_status(self, status):
        words = status.split('_')
        formatted_status = '-'.join([word.capitalize() for word in words])
        return formatted_status
    
    def post(self, request):
        user = request.user

        status_param = request.data.get('status')
        contracts_data = contracts.objects.filter(user=user)

        if status_param:
            if status_param.lower() == 'used':
                # Show all contracts of the user without applying the status filter
                pass
            else:
                contracts_data = contracts.objects.filter(user=user, status=status_param)

        # Apply additional filters based on options
        option_param = request.data.get('option')
        if option_param == 'Last Month':
            last_month = datetime.now() - timedelta(days=30)
            contracts_data = contracts_data.filter(created_at__gte=last_month)
        elif option_param == 'Last Quarter':
            last_quarter = datetime.now() - timedelta(days=90)
            contracts_data = contracts_data.filter(created_at__gte=last_quarter)
        elif option_param == 'Last Year':
            last_year = datetime.now() - timedelta(days=365)
            contracts_data = contracts_data.filter(created_at__gte=last_year)

        text_param = request.data.get('text')
        if text_param:
            contracts_data = contracts_data.filter(contract_title__icontains=text_param)

            if not contracts_data.exists():
                return Response({"status": 400, "message": "No contracts found matching the provided text"}, status=status.HTTP_200_OK)

        folder_id_param = request.data.get('folder_id')
        if folder_id_param:
            try:
                folder = Folder.objects.get(id=folder_id_param, user=user)
                contracts_data = contracts_data.filter(folder_id=folder.id)
            except Folder.DoesNotExist:
                return Response({"status": 400, "message": "Folder not found"}, status=status.HTTP_200_OK)

        contracts_data = contracts_data.order_by('-created_at')

        response_data = {
            'status': status.HTTP_200_OK,
            'message': 'Contracts list fetched successfully',
            'data': []
        }

        contract_dict = {}

        for contract in contracts_data:
            if contract.id not in contract_dict:
                contract_dict[contract.id] = {
                    'id': contract.id,
                    'contract_title': contract.contract_title,
                    'created_at': contract.created_at,
                    'status': self.format_status(contract.status),
                    'contract_party': {'first_party_user': [], 'second_party_user': []},
                    # 'user': self.serialize_user(user)  # Serialize user data here
                }

            if user.user_type == 'Business User':
                business_party_data = business_contract_party.objects.filter(user=user, contract=contract)
                business_party_serializer = BusinessContractPartySerializer(
                    business_party_data, many=True, context={'request': request})
                
                for business_party in business_party_serializer.data:
                    if business_party['first_party_user']:
                        contract_dict[contract.id]['contract_party']['first_party_user'].append(business_party['first_party_user'])
                    if business_party['second_party_user']:
                        contract_dict[contract.id]['contract_party']['second_party_user'].append(business_party['second_party_user'])
            else:
                contract_party_data = contract_party.objects.filter(contract=contract)
                contract_party_serializer = ContractPartylistSerializerWEB(
                    contract_party_data, many=True, context={'request': request})
                
                for party in contract_party_serializer.data:
                    if party['first_party_user']:
                        contract_dict[contract.id]['contract_party']['first_party_user'].append(party['first_party_user'])
                    if party['second_party_user']:
                        contract_dict[contract.id]['contract_party']['second_party_user'].append(party['second_party_user'])

        response_data['data'] = list(contract_dict.values())

        return Response(response_data)


'''in above code add some logic check also current user email_id and and after that email check in contract_party and business_contract_party table if that email avaaliable so that time also show a that contract '''


# Party user details View
class PartyUserdetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"status": 200, 'message': 'User id is required.'}, status=status.HTTP_200_OK)
        try:
            user = Users.objects.filter(id=user_id).first()
            if not user:
                return Response({"status": 200, 'message': 'User not found'}, status=status.HTTP_200_OK)

            serializer = PartyUserdetailsSerializer(user, context={'request': request})
            return Response({'status': status.HTTP_200_OK, 'message': 'Get profile successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"status": 200, 'message': 'Invalid user id.'}, status=status.HTTP_200_OK)


# add appendix in contract APIView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
class AppendixUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        contract_id = request.data.get('contract_id')
        if not contract_id:
            return Response({'status': '400', 'message': 'Contract id is requried.'}, status=status.HTTP_200_OK)

        try:
            contract = contracts.objects.get(id=contract_id)
        except contracts.DoesNotExist:
            return Response({'status': '400', 'message': 'Contract not found'}, status=status.HTTP_200_OK)

        appendix_file = request.data.get('appendix')
        if not appendix_file:
            return Response({'status': '400', 'message': 'No appendix file provided.'}, status=status.HTTP_200_OK)

        contract.appendix = appendix_file
        contract.save()

        current_site = get_current_site(request)
        appendix_url = request.build_absolute_uri(contract.appendix.url)

        serializer = AddappendixSerializer(contract)
        response_data = {
            'status': '200',
            'message': 'Appendix added successfully.',
            'data': {
                'contract_id': contract_id,
                'appendix': appendix_url
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)






# clone contract APIView
class ContractCloneAPIView(APIView):
    def post(self, request):
        contract_id = request.data.get('contract_id')

        if not contract_id:
            return Response(
                {'error': 'Contract id not provided.'},
                status=status.HTTP_200_OK
            )

        try:
            # Retrieve the contract to be cloned
            contract = contracts.objects.get(id=contract_id)
            
            # Check the number of available contracts for the user's membership type
            user_id = request.user.id
            total_contracts = contract_histroy.objects.filter(user_id=user_id).aggregate(total_contracts=Sum('contracts'))['total_contracts']
            total_contracts = total_contracts if total_contracts is not None else 0
            user_contracts = contracts.objects.filter(user_id=user_id).count()
            available_contracts = total_contracts - user_contracts
            if available_contracts <= 0:
                return Response({'status': 400, 'message': 'You have reached the maximum number of contracts allowed for your membership type.'}, status=status.HTTP_200_OK)

            # Create a new contract object with the same attributes
            cloned_contract = contracts.objects.create(
                user=contract.user,  # Set the current user as the user field
                folder=contract.folder,
                template=contract.template,
                contract_title=contract.contract_title,
                category=contract.category,
                description=contract.description,
                contract_duration = contract.contract_duration,
                contract_start_date=contract.contract_start_date,
                contract_end_date=contract.contract_end_date,
                currency = contract.currency,
                contract_fees = contract.contract_fees,
                contract_amount = contract.contract_amount,
                contract_amount_words = contract.contract_amount_words,
                # contract_valuation=contract.contract_valuation,
                status='draft',  # Assuming cloned contracts are always in draft status
                appendix=contract.appendix
            )

            return Response({
                'message': 'Contract cloned successfully.',
                'status': status.HTTP_200_OK,
                'data': {
                    'id': cloned_contract.id
                }
            }, status=status.HTTP_200_OK)
        except contracts.DoesNotExist:
            return Response(
                {'error': 'Contract not found.'},
                status=status.HTTP_200_OK
            )





# contract details APIview
class ContractDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        contract_id = request.data.get('contract_id')

        if not contract_id:
            return Response(
                {'status':400,'message': 'Contract id is requried.'},
                status=status.HTTP_200_OK
            )

        try:
            # Retrieve the contract based on the provided contract_id and the current user
            contract = contracts.objects.get(id=contract_id, user=request.user)

            # Serialize the contract for response
            serializer = contractsdetailSerializer(contract)

            return Response({
                'message': 'Contract details fetch successfully.',
                'status': status.HTTP_200_OK,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except contracts.DoesNotExist:
            return Response(
                {'status': 400, 'message': 'Contract not found.'},
                status=status.HTTP_200_OK
            )
            
            
# accoriding to party_type fetched a user and company data 
class Party_company_users_listAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        party_type = request.data.get('party_type')
        
        if party_type is None:
            return Response({'status': 400, 'message': 'Party type is required.'})
        
        if party_type == 'Company':
            data = self.get_company_data(self.request.user.id)  # Pass the user ID here
        elif party_type == 'Individual':
            data = self.get_individual_data(self.request.user.id)  # Pass the user ID here
        else:
            data = {'status': 400, 'message': 'Invalid party_type.'}
        
        return Response(data)
    
    def get_company_data(self, user_id):
        company_users = Users.objects.filter(user_type='Business Admin').exclude(id=user_id)
        company_data = [{'id': user.id, 'name': user.company_name} for user in company_users]
        sorted_company_data = sorted(company_data, key=lambda x: (x['name'] or '').lower())
        return {'status': 200, 'message': 'Party company users list fetched successfully.', 'data': sorted_company_data}
    
    def get_individual_data(self, user_id):
        individual_users = Users.objects.filter(user_type='Individual User', active_status='active').exclude(id=user_id)
        individual_data = [{'id': user.id, 'name': user.full_name} for user in individual_users]
        sorted_individual_data = sorted(individual_data, key=lambda x: (x['name'] or '').lower())
        return {'status': 200, 'message': 'Party company users list fetched successfully.', 'data': sorted_individual_data}

    
   
    
    
    
# accoriding to current user login GET a all Business_user list    
class Authorized_users_listView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Check if the user has a valid business_id
        if not user.business_id:
            return Response({'status':400,'message': 'User does not have a valid business_id.'})

        # Get all users with the same business_id excluding the current user
        business_users = Users.objects.filter(business_id=user.business_id).exclude(id=user.id)

        # Extract name and id from each user
        business_users_data = [{'id': u.id, 'name': u.full_name} for u in business_users]

        return Response({'status':200,'message':'Authorized users list fetched successfully.','data': business_users_data})
    

# add business party 
class BusinessContractPartyCreateView(APIView):
 
    def post(self, request, *args, **kwargs):
        contract_id = request.data.get('contract_id')

        contract = contracts.objects.filter(id=contract_id).first()
        if not contract:
            return Response(
                {'status': 404, 'message': 'Contract not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if contract.user != request.user:
            return Response(
                {'status': 403, 'message': 'You do not have permission to update this contract.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        first_party_data = request.data.get('first_party', [])
        additional_first_party_data = request.data.get('additional_first_party', [{}])[0]
        second_party_data = request.data.get('second_party', [{}])[0]

        authorized_person_to_sign_list = [entry.get('authorized_person_to_sign') for entry in first_party_data]
        authorized_person_ids_str = ','.join(authorized_person_to_sign_list)

        first_party_type = additional_first_party_data.get('first_party_type')
        first_party_name_id = additional_first_party_data.get('first_party_name')
        first_party_email = additional_first_party_data.get('first_party_email')

        second_party_type = second_party_data.get('second_party_type')
        second_party_name_id = second_party_data.get('second_party_name')
        second_party_email = second_party_data.get('second_party_email')

        # Get User instances
        first_party_name_instance = Users.objects.get(id=first_party_name_id)
        second_party_name_instance = Users.objects.get(id=second_party_name_id)

        # Prepare data to save
        data_to_save = {
            'user': request.user,
            'contract': contract,
            'authorized_person_ids': authorized_person_ids_str,
            'first_party_type': first_party_type,
            'first_party_name': first_party_name_instance,
            'first_party_email': first_party_email,
            'second_party_type': second_party_type,
            'second_party_name': second_party_name_instance,
            'second_party_email': second_party_email,
        }

        # Create a new business_contract_party record
        business_party = business_contract_party.objects.create(**data_to_save)

        return Response({'status': 200, 'message': 'Business contract party created successfully.'})