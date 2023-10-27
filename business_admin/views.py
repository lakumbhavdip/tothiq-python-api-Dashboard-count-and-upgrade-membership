from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from .serializers import GetBusinessInfoSerializer,BusinessInfoUpdateSerializer,ListDepartmentSerializer,AdminListnotificationSerializer,AdminDeleteNotificationSerializer,DepartmentnamelistSerializer
from rest_framework.permissions import IsAdminUser
from .models import business_info,business_department
from user.models import Users,notification
from datetime import datetime
from django.db.models import Q
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.db import IntegrityError
from masterapp.models import UserMembership,contract_histroy,Membership
from datetime import datetime, timedelta
# business admin APIView 
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from contracts.models import Folder



class BusinessAdminRegistrationAPIView(APIView):
    def post(self, request):
        # Retrieve parameters from request body
        company_name = request.data.get('company_name')
        email_address = request.data.get('email_address')
        password = request.data.get('password')  # Retrieve password from request body
        membership_type = request.data.get('membership_type', 'Free')  # Set default value to "Free"

        # Check if company_name and email_address are provided
        if not company_name:
            return Response({'status': 400, 'message': 'Company name is required.'}, status=status.HTTP_200_OK)
        if not email_address:
            return Response({'status': 400, 'message': 'Email ID is required field.'}, status=status.HTTP_200_OK)
        if not password:
            return Response({'status': 400, 'message': 'Password is required.'}, status=status.HTTP_200_OK)
        
        try:
            # Check if a record with the same company name or email address already exists
            # existing_record = business_info.objects.filter(Q(business_name=company_name) | Q(business_email_address=email_address)).first()
            # if existing_record:
            #     return Response({'status': 400, 'message': 'A record with the same company name or email address already exists.'}, status=status.HTTP_200_OK)
            
            # Check if a record with the same email address already exists
            existing_record = business_info.objects.filter(business_email_address=email_address).first()
            if existing_record:
                return Response({'status': 400, 'message': 'A record with the same email address already exists.'}, status=status.HTTP_200_OK)

            # Create a new user entry in the Users table
            user = Users.objects.create(
                company_name=company_name,
                email=email_address,
                user_type ='Business Admin',
                active_status='active',
                created_at=datetime.now(),
                membership_type = membership_type,
                # business_id = business.id
            )
            
            # Generate a token using Token model and associate it with the user
            token, created = Token.objects.get_or_create(user=user)

            # Hash the password
            password_hash = make_password(password)

            # Create a new instance of the business_info model and store the hashed password
            business = business_info(
                user=user,
                business_name=company_name,
                business_email_address=email_address,
                password=password_hash,  # Store the hashed password in the "password" field
                active_status='inactive',
                created_at=datetime.now()
            )
            business.save()

            # Fetch membership based on user_type and store its ID in UserMembership
            membership = Membership.objects.filter(user_type="Business Admin", membership_name=membership_type).first()
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
                user_count = membership.number_of_user

                contract_histroy.objects.create(
                    user=user,
                    contracts=contracts_count,
                    parties=None,
                    users=user_count,
                    action_type='add',
                    action_info=action_info,
                    created_at=datetime.now()
                )

            
            # Create the "general" department for the business
            general_department = business_department.objects.create(
                business=business,
                department_name='General',
                active_status='active',
                created_at=datetime.now()
            )

            # Send email with verification link
            verification_link = f'https://yourdomain.com/activate?token={token.key}'  # Replace with your domain
            email_subject = 'Business Registration Verification' 
            email_message = f'Dear {company_name},\n\nThank you for registering your business. Please click the following link to activate your account:\n\n{verification_link}'
            send_mail(email_subject, email_message, 'your-email@example.com', [email_address], fail_silently=False)

            # Return success response with the created business_info ID, token, and membership type
            response_data = {
                'status': 200,
                'message': 'Registration successful. Verification email sent.',
                'id': business.id,
                'user_id': user.id,
                'email': user.email,
                'token': token.key,
                'membership_type': membership_type,
                'user_type': 'Business Admin'
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except IntegrityError:
            return Response({'status': 400, 'message': 'Email ID is already registered.'}, status=status.HTTP_200_OK)



#create password APIView
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated

class CreatePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Retrieve parameters from request body
        create_password = request.data.get('create_password')
        retype_password = request.data.get('retype_password')

        # Check if create_password and retype_password are provided
        if not create_password:
            return Response({'status': 400, 'message': 'Create password is required.'}, status=status.HTTP_200_OK)

        if not retype_password:
            return Response({'status': 400, 'message': 'Retype password is required.'}, status=status.HTTP_200_OK)

        # Compare create_password and retype_password
        if create_password != retype_password:
            return Response({'status': 400, 'message': 'Passwords do not match.'}, status=status.HTTP_200_OK)

        # Get the authenticated user from the request
        user = request.user

        # Find the business_info record associated with the user
        try:
            business = business_info.objects.get(user=user)
        except business_info.DoesNotExist:
            return Response({'status': 404, 'message': 'Business record not found.'}, status=status.HTTP_200_OK)

        # Hash the password and set it for the business_info record
        hashed_password = make_password(create_password)
        business.password = hashed_password
        business.save()

        # Return success response
        response_data = {
            'status': 200,
            'message': 'Password created successfully.'
        }
        return Response(response_data, status=status.HTTP_200_OK)





#login APIView 
class LoginAPIView(APIView):
    def post(self, request):
        email_address = request.data.get('email_address')
        password = request.data.get('password')

        if not email_address:
            return Response({'status':400,'message': 'Email ID is required.'},status=status.HTTP_200_OK)
        
        if not password:
            return Response({'status': 400,'message': 'password is required.'})

        try:
            business = business_info.objects.get(business_email_address=email_address)
        except business_info.DoesNotExist:
            return Response({'status':400,'message': 'User not found.'},status=status.HTTP_200_OK)

        if not check_password(password, business.password):
            return Response({'status': 400,'message': 'Incorrect password.'},status=status.HTTP_200_OK)
        
        # Delete the existing token
        Token.objects.filter(user=business.user).delete()

        # Generate a new token
        token = Token.objects.create(user=business.user)

        return Response({
            'status': '200',
            'message': 'Login successfully.',
            'token': token.key,
            'id': business.id,
            'user_id': business.user.id,
            "membership_type":business.user.membership_type,
            'user_type': 'Business Admin'
        },status=status.HTTP_200_OK)







# Get business profile view
from rest_framework.permissions import IsAuthenticated
class GetBusinessInfoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            # Find the business_info record associated with the authenticated user
            business = business_info.objects.get(user=request.user)
            serializer = GetBusinessInfoSerializer(business, context={'request': request})
            return Response({'status': 200, 'message': 'Business profile fetch successfully.', 'data': serializer.data}, status=status.HTTP_200_OK)
        except business_info.DoesNotExist:
            return Response({'status': 400, 'message': 'Business profile not found.'}, status=status.HTTP_200_OK)






#update business profile view 

class UpdateBusinessAdminProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        # Retrieve the user from the request
        user = request.user

        try:
            # Find the business_info record for the user
            business = business_info.objects.get(user=user)

            # Retrieve the fields to be updated from the request body
            business_name_arabic = request.data.get('business_name_arabic', business.business_name_arabic)
            business_contact_number = request.data.get('business_contact_number', business.business_contact_number)
            extension_number = request.data.get('extension_number', business.extension_number)
            area = request.data.get('area', business.area)
            area_arabic = request.data.get('area_arabic', business.area_arabic)
            block = request.data.get('block', business.block)
            block_arabic = request.data.get('block_arabic', business.block_arabic)
            street_name_number = request.data.get('street_name_number', business.street_name_number)
            street_name_arabic = request.data.get('street_name_arabic', business.street_name_arabic)
            building_name_number = request.data.get('building_name_number', business.building_name_number)
            building_name_arabic = request.data.get('building_name_arabic', business.building_name_arabic)
            office_number = request.data.get('office_number', business.office_number)
            office_number_arabic = request.data.get('office_number_arabic', business.office_number_arabic)
            licence_expiry_date = request.data.get('licence_expiry_date', business.licence_expiry_date)
            authorized_signatory_expiry_date = request.data.get('authorized_signatory_expiry_date', business.authorized_signatory_expiry_date)
            licence_image = request.data.get('licence_image', business.licence_image)
            authorized_signatory_image = request.data.get('authorized_signatory_image', business.authorized_signatory_image)
            profile_picture = request.data.get('profile_picture')


            # Check if the required fields are provided
            if not business_contact_number or not extension_number or not licence_expiry_date:
                return Response({'status': 400, 'message': 'Required fields are missing.'}, status=status.HTTP_200_OK)
        
            if not area and not area_arabic:
                return Response({'status': 400, 'message': 'Required fields are missing'}, status=status.HTTP_200_OK)
        
            if not block and not block_arabic:
                return Response({'status': 400, 'message': 'Required fields are missing'}, status=status.HTTP_200_OK)

            if not street_name_number and not street_name_arabic:
                return Response({'status': 400, 'message': 'Required fields are missing'}, status=status.HTTP_200_OK)

            if not building_name_number and not building_name_arabic:
                return Response({'status': 400, 'message': 'Required fields are missing'}, status=status.HTTP_200_OK)

            if not office_number and not office_number_arabic:
                return Response({'status': 400, 'message': 'Required fields are missing'}, status=status.HTTP_200_OK)

            # Convert the licence_expiry_date to datetime object
            licence_expiry_date = datetime.strptime(licence_expiry_date, '%d/%m/%Y').date()

            # Convert the authorized_signatory_expiry_date to datetime object
            authorized_signatory_expiry_date = datetime.strptime(authorized_signatory_expiry_date, '%d/%m/%Y').date()
            
            
        # try:
        #     # Convert the licence_expiry_date to datetime object
        #     licence_expiry_date = datetime.strptime(licence_expiry_date, '%d/%m/%Y').date()

        #     # Convert the authorized_signatory_expiry_date to datetime object
        #     authorized_signatory_expiry_date = datetime.strptime(authorized_signatory_expiry_date, '%d/%m/%Y').date()

        #     # Your existing code...

        # except ValueError:
        #     return Response({'status': 400, 'message': 'Invalid date format. Date must be in the format dd/mm/yyyy'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the business_info record with the new data
            business.business_name_arabic = business_name_arabic
            business.business_contact_number = business_contact_number
            business.extension_number = extension_number
            business.area = area
            business.block = block
            business.street_name_number = street_name_number
            business.building_name_number = building_name_number
            business.office_number = office_number
            business.licence_expiry_date = licence_expiry_date
            business.authorized_signatory_expiry_date = authorized_signatory_expiry_date
            business.updated_at = datetime.now()
            business.active_status = 'active'

            # Update the licence_image field if provided
            if licence_image:
                business.licence_image = licence_image

            # Update the authorized_signatory_image field if provided
            if authorized_signatory_image:
                business.authorized_signatory_image = authorized_signatory_image
                
            # Update the profile_picture field if provided
            if profile_picture:
                business.profile_picture = profile_picture

            business.save()

            serializer = BusinessInfoUpdateSerializer(business, context={'request': request})
            return Response({'status': 200, 'message': 'Business profile updated successfully.', 'data': serializer.data}, status=status.HTTP_200_OK)

        except business_info.DoesNotExist:
            return Response({'status': 400, 'message': 'User not found'}, status=status.HTTP_200_OK)





#add department view
class BusinessAddDepartmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        print(user)

        department_name = request.data.get('department_name', None)
        parent_department_id = request.data.get('parent_department_id', None)

        if not department_name:
            return Response({"status": 400, "message": "Department name is required."},status=status.HTTP_200_OK)

        try:
            business = user.business_info_set.get()
        except business_info.DoesNotExist:
            return Response({'status': 400, 'message': 'Business info not found.'}, status=status.HTTP_200_OK)

        # Check if a department with the same name already exists for the user's business_info
        if business.departments.filter(department_name=department_name).exists():
            return Response({"status": 400, "message": "A department with this name already exists."}, status=status.HTTP_200_OK)
        
        if department_name == 'General':
            return Response({"status": 400, "message": "Cannot create a user in the 'General' department."}, status=status.HTTP_200_OK)

        if parent_department_id:
            try:
                parent_department = business_department.objects.get(id=parent_department_id, business=business)
            except business_department.DoesNotExist:
                return Response({'status': 400, 'message': 'Parent department not found.'}, status=status.HTTP_200_OK)

            # Create the department with the specified parent_department_id
            department = business_department(
                business=business,
                department_name=department_name,
                parent_department_id=parent_department
            )
        else:
            # Create the department without a parent_department_id
            department = business_department(
                business=business,
                department_name=department_name
            )

        department.active_status = 'active'  # Set active_status to 'active'
        department.save()

        return Response({"status": 200, "message": "Department created successfully."}, status=status.HTTP_200_OK)





    


#Department list view
class ListDepartmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        try:
            business = user.business_info_set.get()
        except business_info.DoesNotExist:
            return Response({'status': 400, 'message': 'Business info not found.'}, status=status.HTTP_200_OK)

        # Retrieve only top-level (non-child) active departments
        departments = business.departments.filter(active_status='active', parent_department_id=None)
        general_department = departments.filter(department_name__iexact='General').first()

        # Sort departments by creation date in descending order
        # departments = departments.order_by('-created_at')

        # Sort folders by folder_name in ascending order (excluding "General" folder)
        departments = departments.exclude(id=general_department.id).order_by('department_name')
        
        # Move the "General" department to the beginning of the list
        if general_department:
            departments = [general_department] + list(departments.exclude(id=general_department.id))

        # Filter out inactive departments
        departments = [dept for dept in departments if dept.active_status == 'active']

        serializer = ListDepartmentSerializer(departments, many=True)

        return Response({'status': 200, 'message': 'Department list fetched successfully.', 'data': serializer.data}, status=status.HTTP_200_OK)







#Department name list view
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from django.db.models.functions import Lower

class DepartmentListAPIView(generics.ListAPIView):
    serializer_class = DepartmentnamelistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the logged-in user
        user = self.request.user

        # Find the business_info object associated with the user
        business_info_obj = get_object_or_404(business_info, user=user)

        # Filter departments based on the business_info id and exclude 'General'
        queryset = business_department.objects.filter(business=business_info_obj, active_status='active',parent_department_id=None).exclude(department_name='General')

        # Sort departments by creation date in descending order (latest first)
        # queryset = queryset.order_by('-created_at')
        
        # Sort folders by folder name in ascending order (A to Z)
        queryset = queryset.annotate(lower_name=Lower('department_name')).order_by('lower_name')

        return queryset

    def list(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            data = {
                'status': status.HTTP_200_OK,
                'message': 'Department name list fetched successfully.',
                'data': serializer.data
            }
            return Response(data)
        except AuthenticationFailed as e:
            data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            }
            return Response(data)




#Department all name list API
class DepartmentListnameAPIView(generics.ListAPIView):
    serializer_class = DepartmentnamelistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the logged-in user
        user = self.request.user

        # Find the business_info object associated with the user
        business_info_obj = get_object_or_404(business_info, user=user)

        # Filter departments based on the business_info id and exclude 'General'
        queryset = business_department.objects.filter(business=business_info_obj, active_status='active').exclude(department_name='General')

        # Sort departments by creation date in descending order (latest first)
        # queryset = queryset.order_by('-created_at')
        
        # Sort folders by folder name in ascending order (A to Z)
        queryset = queryset.annotate(lower_name=Lower('department_name')).order_by('lower_name')

        return queryset

    def list(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            data = {
                'status': status.HTTP_200_OK,
                'message': 'Department name list fetched successfully.',
                'data': serializer.data
            }
            return Response(data)
        except AuthenticationFailed as e:
            data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            }
            return Response(data)





#delete department View 
class DeleteDepartmentAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        department_id = request.data.get('department_id')

        if not department_id:
            return Response({"status": 400, "message": "Department id is required."}, status=status.HTTP_200_OK)

        try:
            department = business_department.objects.get(id=department_id, business__user_id=user.id)
        except business_department.DoesNotExist:
            return Response({"status": 400, "message": "Department not found."}, status=status.HTTP_200_OK)

        # Check if the department is the "General" department
        if department.department_name.lower() == "general":
            return Response({"status": 400, "message": "The General department cannot be deleted."}, status=status.HTTP_200_OK)

        # Get the general department of the current login user
        general_department = business_department.objects.get(department_name__iexact="General", business__user_id=user.id)

        # Update the department_id of users assigned to the department being deleted
        assigned_users = Users.objects.filter(department=department)
        assigned_users.update(department=general_department)

        department.active_status = 'inactive'
        department.save()

        return Response({"status": 200, "message": "Department is deleted successfully. All the associated departments are moved to General."}, status=status.HTTP_200_OK)






#edit department view 
class EditDepartmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user

        department_id = request.data.get('department_id', None)
        department_name = request.data.get('department_name', None)
        parent_department_id = request.data.get('parent_department_id', None)  # New parent_department_id to be updated

        if not department_id:
            return Response({"status": 400, "message": "Department id is required"}, status=status.HTTP_200_OK)

        if not department_name:
            return Response({"status": 400, "message": "Department name is required."}, status=status.HTTP_200_OK)

        try:
            department = business_department.objects.get(id=department_id, business__user_id=user.id)
        except business_department.DoesNotExist:
            return Response({"status": 404, "message": "Department not found"}, status=status.HTTP_200_OK)

        if department.department_name.lower() == "general":
            return Response({"status": 400, "message": "Cannot change the name of the General Department."}, status=status.HTTP_200_OK)

        # Check if the specified parent_department_id exists for the user's departments
        if parent_department_id is not None and parent_department_id != '':
            try:
                parent_department = business_department.objects.get(id=parent_department_id, business__user_id=user.id)
            except business_department.DoesNotExist:
                return Response({"status": 404, "message": "Parent department not found."}, status=status.HTTP_200_OK)

            # Check if the parent_department_id belongs to a department that is not the same as the current department
            if parent_department_id != department.parent_department_id:
                department.parent_department_id = parent_department  # Assign the instance, not just the ID
        # Only update the parent_department_id if a valid non-blank value is provided
        # If parent_department_id is blank or None, keep the existing parent_department_id
        # To change the parent_department_id to None, provide an explicit None value for parent_department_id
        department.department_name = department_name
        department.save()

        return Response({"status": 200, "message": "Department updated successfully."}, status=status.HTTP_200_OK)





# GET a particular department name and that parent_department_ids     
class DepartmentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        department_id = request.data.get('department_id')
        if not department_id:
            return Response({'status': 400, 'message': 'Department id is required'}, status=400)

        try:
            department = business_department.objects.get(id=department_id)

            # Check if the department is assigned to the current user
            if department.business.user != request.user:
                return Response({'status': 403, 'message': 'Department not found'}, status=403)

            parent_department_id = self.get_parent_department_id(department)
            department_data = {
                'department_name': department.department_name,
                'parent_department_id': parent_department_id,
            }
            return Response({'status': 200, 'message': 'Department details fetched successfully.', 'data': department_data})
        except business_department.DoesNotExist:
            return Response({'status': 404, 'message': 'Department not found.'}, status=404)

    def get_parent_department_id(self, department):
        parent_department_id = department.parent_department_id_id if department.parent_department_id else None
        return parent_department_id



# add user view
from django.db.models import Sum

class AddUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        business_info_entry = business_info.objects.get(user_id=user.id)
        business_id = business_info_entry.id
        civil_id = request.data.get('civil_id')
        email = request.data.get('email')
        department_id = request.data.get('department_id')
        membership_type = request.data.get('membership_type', 'Free') # Set default value to "Free"
        view_read = self.to_bool(request.data.get('view_read'))
        review_comment = self.to_bool(request.data.get('review_comment'))
        invite_users = self.to_bool(request.data.get('invite_users'))
        sign_contract = self.to_bool(request.data.get('sign_contract'))
        upload_document = self.to_bool(request.data.get('upload_document'))
        contract_report = self.to_bool(request.data.get('contract_report'))
        financial_report = self.to_bool(request.data.get('financial_report'))
        super_user_full_access = self.to_bool(request.data.get('super_user_full_access'))

        # Check if civil_id, email, and department_id are provided
        if not civil_id:
            return Response({"status": 400, "message": "Civil ID is required"}, status=status.HTTP_200_OK)
        if not email:
            return Response({"status": 400, "message": "Email ID is required"}, status=status.HTTP_200_OK)
        if not department_id:
            return Response({"status": 400, "message": "Department id is required"}, status=status.HTTP_200_OK)

        total_users_business = contract_histroy.objects.filter(user_id=user.id).aggregate(total_users=Sum('users'))['total_users']
        used_users_count = Users.objects.filter(business=business_id).count()
        avaliable_user_business = total_users_business - used_users_count
        
        if avaliable_user_business <= 0:
            return Response({'status': 400, 'message': 'You have reached the maximum number of users allowed for your business membership type'}, status=status.HTTP_200_OK)

        try:
            business = business_info.objects.get(user_id=user.id)
            department = business_department.objects.get(id=department_id, business=business)
        except business_department.DoesNotExist:
            return Response({"status": 400, "message": "Department not found"}, status=status.HTTP_200_OK)
        
        # Check if the user is already added to the business as a Business User or an Invite
        existing_business_user = Users.objects.filter(business=business, civil_id=civil_id, user_type='Business User').first()

        if existing_business_user:
            return Response({"status": 400, "message": "User is already added to the business."}, status=status.HTTP_200_OK)

        # Check if a user with the same civil_id and user_type 'Individual User' exists
        existing_user = Users.objects.filter(civil_id=civil_id, user_type='Individual User').first()
        if existing_user:
            try:
                with transaction.atomic():
                    # Create a new user with the provided information
                    user, created = Users.objects.update_or_create(
                        business=business,
                        civil_id=civil_id,
                        defaults={
                            'email': email,
                            'department': department,
                            'status':True,
                            'active_status': 'active',
                            'company_name': business.business_name,
                            'user_type': 'Business User',
                            'view_read': super_user_full_access or view_read if view_read is not None else False,
                            'review_comment': super_user_full_access or review_comment if review_comment is not None else False,
                            'invite_users': super_user_full_access or invite_users if invite_users is not None else False,
                            'sign_contract': super_user_full_access or sign_contract if sign_contract is not None else False,
                            'upload_document': super_user_full_access or upload_document if upload_document is not None else False,
                            'contract_report': super_user_full_access or contract_report if contract_report is not None else False,
                            'financial_report': super_user_full_access or financial_report if financial_report is not None else False,
                            'super_user_full_access': super_user_full_access if super_user_full_access is not None else False
                        }
                    )
                    # Fetch fields from the existing Individual User and update the new Business User
                    user.full_name = existing_user.full_name
                    user.phone_number = existing_user.phone_number
                    user.date_of_birth = existing_user.date_of_birth
                    user.gender = existing_user.gender
                    user.address_type = existing_user.address_type
                    user.nationality = existing_user.nationality
                    user.language = existing_user.language
                    user.image = existing_user.image
                    user.save()

                    # Send the request email to the user
                    email_subject = f'Invitation to join {business.business_name}'
                    email_content = f'Dear {email},\n\nYou are welcome to join {business.business_name} company. Please visit the link below and accept the invitation.\n\nThank you.'
                    send_mail(
                        email_subject,
                        email_content,
                        'sender@example.com',
                        [user.email],
                        fail_silently=False,
                    )

                    # Create the "general" department for the business
                    general_folder = Folder.objects.create(
                    user=user,
                    folder_name='General',
                    folder_name_arabic = 'عام',
                    active_status='active',
                    created_at=datetime.now()
                    )
                    
                return Response({"status": 200, "message": "User added successfully.", "user_id": user.id}, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({"status": 400, "message": "Email is already registered"}, status=status.HTTP_200_OK)
        else:
            existing_business_invite = Users.objects.filter(business=business, civil_id=civil_id, user_type='Business User', status=False).first()
            if existing_business_invite:
                return Response({"status": 400, "message": "User is already added to the business as an invite."}, status=status.HTTP_200_OK)
            # If no user with the provided civil_id and user_type 'Individual User' exists
            # Create a new user as a Business User with default values
            try:
                with transaction.atomic():
                    user, created = Users.objects.update_or_create(
                        business=business,
                        civil_id=civil_id,
                        defaults={
                            'email': email,
                            'department': department,
                            'status':False,
                            'active_status': 'inactive',  # Set status to inactive
                            'company_name': business.business_name,
                            'user_type': 'Business User',
                            'view_read': super_user_full_access or view_read if view_read is not None else False,
                            'review_comment': super_user_full_access or review_comment if review_comment is not None else False,
                            'invite_users': super_user_full_access or invite_users if invite_users is not None else False,
                            'sign_contract': super_user_full_access or sign_contract if sign_contract is not None else False,
                            'upload_document': super_user_full_access or upload_document if upload_document is not None else False,
                            'contract_report': super_user_full_access or contract_report if contract_report is not None else False,
                            'financial_report': super_user_full_access or financial_report if financial_report is not None else False,
                            'super_user_full_access': super_user_full_access if super_user_full_access is not None else False
                        }
                    )

                    # Send the invitation email to the user
                    email_subject = f'Invitation to join {business.business_name}'
                    email_content = f'Dear {email},\n\nYou have been invited to join {business.business_name} company as a business user, but you are not registered as an individual user in Tothiq. So Please register as an individual user in Tothiq and then accept this {business.business_name} invitation.\n\nThank you.'
                    send_mail(
                        email_subject,
                        email_content,
                        'sender@example.com',
                        [user.email],
                        fail_silently=False,
                    )

                return Response({"status": 200, "message": "User invited successfully. invitation has been sent to the given email."}, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({"status": 400, "message": "Email is already registered"}, status=status.HTTP_200_OK)

    def to_bool(self, value):
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        return value.lower() in ['true', 't', 'yes', 'y', '1']







# business user list accoriding to business aadmin
from django.conf import settings

class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_image_url(self, request, user):
        if user.image:
            # Assuming 'image' field contains the file path like "tothiq_pic/150-2.jpg"
            return request.build_absolute_uri(settings.MEDIA_URL + user.image)
        return None

    def post(self, request):
        department_id = request.data.get('department_id')
        text = request.data.get('text')
        start_with = request.data.get('start_with')
        user_type = request.data.get('user_type') or 'users'  # Set the default value to 'users' if not provided

        # Fetch the authenticated user's business
        user = request.user
        try:
            business = business_info.objects.get(user_id=user.id)
        except business_info.DoesNotExist:
            return Response({'status': 400, 'message': 'Business profile not found.'}, status=status.HTTP_200_OK)

        # Validate the start_with parameter
        if start_with is not None:
            if not start_with.isalpha() or len(start_with) != 1:
                return Response({"status": 400, "message": "Invalid input"}, status=status.HTTP_200_OK)

        # Fetch the list of users for the business and filter by department_id if provided
        users = Users.objects.filter(business=business)
        if department_id:
            users = users.filter(department_id=department_id)

        # Filter users by full_name if text is provided
        if text:
            users = users.filter(full_name__icontains=text)
            
        # Add logic to show the latest created record first
        users = users.order_by('-created_at')  # The minus sign indicates descending order

        # Filter users by full_name starting with specified alphabet if start_with is provided
        if start_with:
            users = users.filter(full_name__istartswith=start_with)

        # Filter users by user_type (active or invited)
        if user_type == 'users':
            users = users.filter(active_status='active', status=True)
        elif user_type == 'invites':
            users = users.filter(active_status='inactive', status=False)
            # Show only specific fields for invites
            user_list = []
            for user in users:
                department_name = user.department.department_name if user.department else ""
                image_url = self.get_image_url(request, user)

                # Consider invited_date as created_date for invites
                invited_date = user.created_at
                # invited_date_str = invited_date.strftime('%Y-%m-%d %H:%M:%S')

                user_data = {
                    'user_id': user.id,
                    'civil_id':user.civil_id,
                    'email': user.email,
                    'department_name': department_name,
                    'invited_date': invited_date,
                }
                user_list.append(user_data)

            response_data = {
                'status': 200,
                'message': 'Invited users list retrieved successfully.',
                'data': user_list
            }

            return Response(response_data, status=status.HTTP_200_OK)

        # For user_type='users', show all fields as before
        user_list = []
        for user in users:
            department_name = user.department.department_name if user.department else ""
            image_url = self.get_image_url(request, user)

            user_data = {
                'user_id': user.id,
                'full_name': user.full_name,
                'department_name': department_name,
                'email': user.email,
                'phone_number': user.phone_number,
                'last_login': user.last_login,
                'image': image_url,  # Include the full image URL in the response
            }
            user_list.append(user_data)

        response_data = {
            'status': 200,
            'message': 'User list retrieved successfully.',
            'data': user_list
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    
    
    
    
#list notifications view 
class listNotificationAPIViewWEB(APIView):
    serializer_class = AdminListnotificationSerializer
    permission_classes = [IsAuthenticated]  # Add authentication permission

    def post(self, request):
        user = request.user  # Get the currently logged-in user
        text = request.data.get('text', None)  # Get the 'text' parameter from the request body
        
        queryset = notification.objects.filter(user=user, is_active=True)  # Filter by user and is_active=True
        
        if text:
            queryset = queryset.filter(title__icontains=text)  # Filter notifications by title containing the provided text
        
        serializer = self.serializer_class(queryset, many=True)
        response_data = {
            'status': '200',
            'message': 'Notifications retrieved successfully.',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    
    
    

#delete notification
class NotificationDeleteAPIView(generics.GenericAPIView):
    serializer_class = AdminDeleteNotificationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        notification_id = request.data.get('notification_id')
        if notification_id is None:
            return Response({"status": 400, 'message': 'Notification id is required.'}, status=status.HTTP_200_OK)

        user = request.user
        try:
            instance = notification.objects.get(id=notification_id, user=user)
            if instance.is_active:
                instance.is_active = False
                instance.save()
                return Response({"status": 200, 'message': 'Notification deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({"status": 400, 'message': 'Notification is already deleted'}, status=status.HTTP_200_OK)
        except notification.DoesNotExist:
            return Response({"status": 400, 'message': 'Notification not found'}, status=status.HTTP_200_OK)