import ast
from collections import defaultdict
from datetime import datetime, timezone
import datetime
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import re
import smtplib
from concurrent.futures import ThreadPoolExecutor
import socket
import string
import uuid
from click import get_current_context
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
import psycopg2
import os
from django.db.models import Q
import requests
from business_admin.models import business_info
from contracts.models import contracts, template, categories,Users
from masterapp.models import languages_label,contract_histroy,UserMembership, nationality_type,Membership,Coupon,GeneralSettings,PaymentMethod,tothiq_super_user,Activity_logs,Payment,NotificationTemplates
from super_admin_app.models import GeneralNotification,Email_Template
from tothiq.settings import EMAIL_HOST_USER
from user.models import Users, notification,user_firebase_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.utils import timezone
# from .tasks import task_fun
from user_agents import parse
import geocoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pyfcm import FCMNotification
import random
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.core.mail import send_mail
from decimal import Decimal  
from rest_framework.views import APIView
from django.utils.html import format_html
from rest_framework.authtoken.models import Token
from django.core.files import File
from utils import send_email_test
from django.http import HttpResponseNotFound
from django.db.models import Sum, F, Value, IntegerField




def login(request):
    ilogo = GeneralSettings.objects.filter(id=1)
    for i in ilogo:
        login_page_logo = i.login_page_logo
        media_path = login_page_logo.path if login_page_logo else None
        login_page_logo_file_exists = os.path.exists(media_path)

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["pw"]
        
        user = tothiq_super_user.objects.filter(email=email).first()
        if user is None or not check_password(password, user.password):
            messages.error(request, "Email or Password is incorrect")
            return render(request, "index.html",{"ilogo":ilogo,"login_page_logo_file_exists":login_page_logo_file_exists})
        else:
            login =tothiq_super_user.objects.filter(pk=user.id).update(last_login=datetime.now())
           
            request.session['userid'] = user.id
            try:
                log_activity(request,user.id,"Login")
            except Exception as e:
                return render(request , "connection_error.html")
            try:
                subject = "Your User Account Login Information"
                body = 'Congratulations, you have successfully logged into your account. If you have any questions or need assistance, please do not hesitate to contact us.'
                recipient_email = email

                send_email_test(subject, body, recipient_email)
            except Exception as e:
                # Return an error response
                return HttpResponse(f'<h3>Error sending email: {e}</h3>')
            return redirect("superadminapp:home")   
                 
    return render(request, "index.html",{"ilogo":ilogo,"login_page_logo_file_exists":login_page_logo_file_exists})

def home(request):
    user_id = request.session.get('userid')
    if user_id:
        user = tothiq_super_user.objects.get(id=user_id)
        super_users = tothiq_super_user.objects.all()
      
        username = user.full_name
        userimage = user.image
        
        ind_free = Users.objects.filter(Q(user_type="Individual User") & Q(Q(membership_type='Free') | Q(membership_type="free")))
        buss_free = Users.objects.filter(Q(Q(user_type="Business User") | Q(user_type="business_user")) & Q(Q(membership_type='Free') | Q(membership_type="free")))
        
        ind_basic = Users.objects.filter(Q(user_type="Individual User") & Q(Q(membership_type='Basic') | Q(membership_type="basic")))
        buss_basic = Users.objects.filter(Q(Q(user_type="Business User") | Q(user_type="business_user")) & Q(Q(membership_type='Basic') | Q(membership_type="basic")))
        
        ind_pre = Users.objects.filter(Q(user_type="Individual User") & Q(Q(membership_type='Premium') | Q(membership_type="premium")))
        buss_pre = Users.objects.filter(Q(Q(user_type="Business User") | Q(user_type="business_user")) & Q(Q(membership_type='Premium') | Q(membership_type="premium")))
        
        ind_gold = Users.objects.filter(Q(user_type="Individual User") & Q(Q(membership_type='Gold') | Q(membership_type="gold")))
        buss_gold = Users.objects.filter(Q(Q(user_type="Business User") | Q(user_type="business_user")) & Q(Q(membership_type='Gold') | Q(membership_type="gold")))
        
        ind_pla = Users.objects.filter(Q(user_type="Individual User") & Q(Q(membership_type='Platinium') | Q(membership_type="platinium")))
        buss_pla = Users.objects.filter(Q(Q(user_type="Business User") | Q(user_type="business_user")) & Q(Q(membership_type='Platinium') | Q(membership_type="platinium")))
    
        totaluser = ind_free.count() + ind_basic.count() + ind_pre.count() + ind_gold.count() + ind_pla.count()
        totaluser1 = buss_free.count() + buss_basic.count() + buss_pre.count() + buss_gold.count() + buss_pla.count()
        
        with_coupon = Payment.objects.filter(Q(Q(discount_type="percentage") | Q(discount_type="fixed_price")) & Q(payment_status="success"))
        result = with_coupon.aggregate(total_net_amount=Sum('net_amount'))
        with_coupon_total_net_amount = float(result['total_net_amount']) if result['total_net_amount'] is not None else 0.0
        
        without_coupon = Payment.objects.filter(discount_type=None,payment_status="success") 
        result1 = without_coupon.aggregate(total_net_amount=Sum('net_amount'))
        without_coupon_total_net_amount = float(result1['total_net_amount']) if result1['total_net_amount'] is not None else 0.0

            
        discount_from_coupon = Payment.objects.filter(payment_status="success")
        discount_from_coupon_result = discount_from_coupon.aggregate(total_discount_amount=Sum('discount_amount'))
        discount_from_coupon_results = discount_from_coupon_result['total_discount_amount']

        try:
            if totaluser != 0:
                percentage_reviews = [f"{(ind_total / totaluser) * 100:.0f}%" for ind_total in [ind_free.count(), ind_basic.count(), ind_pre.count(), ind_gold.count(), ind_pla.count()]]
            else:
                percentage_reviews = []
            
            if totaluser1 != 0:
                percentage_reviews1 = [f"{(buss_total / totaluser1) * 100:.0f}%" for buss_total in [buss_free.count(), buss_basic.count(), buss_pre.count(), buss_gold.count(), buss_pla.count()]]
            else:
                percentage_reviews1 = []
            
        except ZeroDivisionError:
            # Handle the ZeroDivisionError by setting default values or displaying an error message.
            percentage_reviews = []
            percentage_reviews1 = []

        context = {
        
            "super_users": super_users,
            "with_coupon_total_net_amount": with_coupon_total_net_amount,
            "without_coupon_total_net_amount": without_coupon_total_net_amount,
            "discount_from_coupon_results": discount_from_coupon_results,
            "username": username,
            "userimage": userimage,
            "user_instance1": ind_free,
            "user_instance2": ind_basic,
            "user_instance3": ind_pre,
            "user_instance7": ind_gold,
            "user_instance8": ind_pla,
            "user_instance4": buss_free,
            "user_instance5": buss_basic,
            "user_instance6": buss_pre,
            "user_instance9": buss_gold,
            "user_instance10": buss_pla,
            "percentage_reviews": percentage_reviews,
            "percentage_reviews1": percentage_reviews1
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('superadminapp:login')

def template_update(request, templateid):
    user_id = request.session.get('userid')
    if user_id:
        # try:
        #     user = Users.objects.get(id=user_id)
        #     userimage = user.image
        # except ObjectDoesNotExist:
        #     # Handle the case when the user does not exist.
        #     user = None
        #     userimage = None
        
        # user = Users.objects.get(id=user_id)
        # userimage = user.image
        temp = template.objects.filter(id=templateid).select_related('category')
        for mediaImage in temp:
            img = mediaImage.image
            media_path = img.path if img else None
            file_exists = os.path.exists(media_path)

        for i in temp:
            exits_temp_category = i.category.category_name
            exits_temp_image = i.image
            exits_temp_desc = i.description
            exits_temp_create_at = i.created_at
            template_category_name = i.category.category_name 

        templateid = templateid
        cat_table = categories.objects.all().order_by('category_name')
        
        if request.method == "POST":
            template_title = request.POST['templatetitle']
            template_title_arabic = request.POST['templatetitlearabic']
            if template.objects.filter(template_title=template_title).exclude(Q(pk=templateid)).exists():
                messages.info(request, 'Template Name is already used')
                # return redirect('http://127.0.0.1:8000/temp_update/' + str(templateid))
                return redirect('superadminapp:Template_Update', templateid=templateid)
            
            temp_cat_name = request.POST['categoryname']
            category_instance = categories.objects.get(category_name=temp_cat_name)  # Get the categories instance
            ind_free = bool(request.POST.get('ind_free', False))
            ind_basic = bool(request.POST.get('ind_basic', False))
            ind_pre = bool(request.POST.get('ind_pre', False))
            bus_free = bool(request.POST.get('bus_free', False))
            bus_basic = bool(request.POST.get('bus_basic', False))
            bus_pre = bool(request.POST.get('bus_pre', False))
            description = request.POST.get('temp_des')
            description_arabic = request.POST.get('temp_des_arabic')
           
            # description = request.POST['temp_des']
            created_at = exits_temp_create_at
            updated_at = timezone.now()
            image = request.FILES.get('imageInput')
            if image == None:
                image = exits_temp_image
            try:
                template_obj = template.objects.get(pk=templateid)
                template_obj.template_title = template_title
                template_obj.template_title_arabic = template_title_arabic
                template_obj.category = category_instance  # Assign the categories instance to the template.category field
                template_obj.individual_free_template = ind_free
                template_obj.individual_basic_template = ind_basic
                template_obj.individual_premium_template = ind_pre
                template_obj.business_free_template = bus_free
                template_obj.business_basic_template = bus_basic
                template_obj.business_premium_template = bus_pre
                template_obj.image = image
                template_obj.created_at = created_at
                template_obj.updated_at = updated_at
                template_obj.description = description
                template_obj.description_arabic = description_arabic
                template_obj.save()
            except Exception as e:
                return HttpResponse(f'<h3>Error update template: {e} </h3>')       
            try:
                log_activity(request,user_id,"update template")
            except Exception as e:
                return render(request , "connection_error.html")
            messages.info(request, 'Template have been updated.')
            return redirect('superadminapp:Template')
        
        context = {
            "temp":temp,
            "file_exists":file_exists,
            # "userimage":userimage,
            "cat_table": cat_table,
            "templateid": templateid,
            "template_category_name": template_category_name,
            "exits_temp_category": exits_temp_category
        }
        return render(request, 'template_update.html', context)
    
    else:
        return redirect('superadminapp:login')

def profile_update(request):
    user_id = request.session.get('userid')
    if user_id:
        oldemail = tothiq_super_user.objects.filter(id=user_id)
        for i in oldemail:
            oldmail = i.email
        if request.method == "POST":
            name = request.POST["user_name"]
            email = request.POST["user_email"]
            number = request.POST["user_phone_number"]
            img = request.FILES.get('user_profile_pic')
            if img is None:
                img = tothiq_super_user.objects.get(pk=user_id).image
            try:   
                u = tothiq_super_user.objects.get(pk=user_id)
                u.full_name=name
                u.email=email
                u.phone_number=number
                u.image=img
                u.updated_at=datetime.now()
                u.save()
            except Exception as e:
                return HttpResponse(f'<h3>Error update profile: {e} </h3>')
            try:
                log_activity(request,user_id,"update profile")
            except Exception as e:
                return render(request , "connection_error.html")
            try:
                
                subject = "Profile Update Successful."
                body = 'Congratulations! Your profile has been updated successfully. If you have any further changes or need assistance, feel free to reach out to us anytime.'
                recipient_email = oldmail
                send_email_test(subject, body, recipient_email)
              
            except Exception as e:
                # Return an error response
                return HttpResponse(f'<h3>Error sending email: {e}</h3>')
            return redirect('superadminapp:home')
    else:
        return redirect('superadminapp:login')

def update_password(request):
    user_id = request.session.get('userid')
    if user_id:
        oldemail = tothiq_super_user.objects.filter(id=user_id)
        for i in oldemail:
            oldmail = i.email
        if request.method == "POST":
            user = tothiq_super_user.objects.get(pk=user_id)
            old_password = user.password
            curent_password = request.POST.get("curent_password")
            new_password = request.POST.get("new_password")
            if check_password(curent_password,old_password):
                new = make_password(new_password)
                u = tothiq_super_user.objects.get(pk=user_id)
                u.password = new
                u.save()
                
                try:
                    
                    subject = "Password Changed Successfully."
                    body = 'Congratulations, your profile password has been successfully changed. If you have any further questions or require assistance, please feel free to reach out to us.'
                    recipient_email = oldmail

                    send_email_test(subject, body, recipient_email)
                   
                except Exception as e:
                    # Return an error response
                    return HttpResponse(f'<h3>Error sending email: {e}</h3>')
                try:
                    log_activity(request,user_id,"changed password")
                except Exception as e:
                    return render(request , "connection_error.html")            
            else :
                print("current pass word is not correct.")
            return redirect('superadminapp:home')
    else:
        return redirect('superadminapp:login')

def validate_password(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == 'POST':
            data = request.body.decode('utf-8')
            entered_password = json.loads(data).get('password')
            old = tothiq_super_user.objects.get(pk=user_id)
            hashed_password = old.password
            # Perform password validation using Django's check_password function
            is_valid = check_password(entered_password, hashed_password)
            return JsonResponse({'is_valid': is_valid})
    else:
        return redirect('superadminapp:login')
        
def template_view(request):
    user_id = request.session.get('userid')
    if user_id:
        # try:
        #     user = Users.objects.get(id=user_id)
        #     userimage = user.image
        # except ObjectDoesNotExist:
        #     # Handle the case when the user does not exist.
        #     user = None
        #     userimage = None
       
        # user = Users.objects.get(id=user_id)
        # userimage = user.image
        cat_name = request.GET.get('cat_name')
        if cat_name == None:
            table = template.objects.all().order_by('-id')
        else:
            table = template.objects.filter(category=cat_name).order_by('-id')
        if request.method == "POST":
            search = request.POST["search"]
            if search != "":
                table = template.objects.all()
                cat_table = categories.objects.filter(category_name=search)
                return render(request, "template.html", {'table': table, 'cat_table': cat_table})
        cat_table = categories.objects.order_by('category_name')
        return render(request, "template.html", {'table': table,
            'cat_table': cat_table
        #  , "userimage":userimage
            })
    else:
        return redirect('superadminapp:login')

def template_create(request):
    user_id = request.session.get('userid')
    if user_id:
        # user = Users.objects.get(id=user_id)
        # userimage = user.image
        cat_table = categories.objects.all().order_by('category_name')
        if request.method == "POST":
            template_title = request.POST.get('templatetitle')
            template_title_arabic = request.POST.get('templatetitlearabic')
            if template.objects.filter(template_title=template_title).exists():
                messages.info(request, 'Template Name is alredy used')
                return redirect('superadminapp:Template_Create')
            cat_name = request.POST.get('categoryname')
            cat_name = categories.objects.filter(category_name=cat_name)
            for cat in cat_name:
                category_id = cat.id
            ind_free = bool(request.POST.get('ind_free', False))
            ind_basic = bool(request.POST.get('ind_basic', False))
            ind_pre = bool(request.POST.get('ind_pre', False))
            bus_free = bool(request.POST.get('bus_free', False))
            bus_basic = bool(request.POST.get('bus_basic', False))
            bus_pre = bool(request.POST.get('bus_pre', False))
            description = request.POST.get('temp_des')
            description_arabic = request.POST.get('temp_des_arabic')
            created_at = timezone.now()  
            updated_at = timezone.now()
            image = request.FILES.get('imageInput')
            temp_id = request.POST.get('temp_id')
            print(ind_free)
            try:
                new_template = template.objects.create(
                    template_title=template_title,
                    template_title_arabic=template_title_arabic,
                    category_id=category_id,
                    individual_free_template = ind_free,
                    individual_basic_template = ind_basic,
                    individual_premium_template = ind_pre,
                    business_free_template = bus_free,
                    business_basic_template = bus_basic,
                    business_premium_template = bus_pre,
                    description=description,
                    description_arabic=description_arabic,
                    created_at=created_at,
                    updated_at=updated_at,
                    image=image
                )
                new_template.save()
            except Exception as e:
                return HttpResponse(f'<h3>Error create template: {e} </h3>')
            templateid = new_template.id
            try:
                log_activity(request,user_id,"create template")
            except Exception as e:
                return render(request , "connection_error.html")
            
            messages.info(request, 'Template successfully created!')
            return redirect('superadminapp:Template_Create_Second', templateid=templateid)

            # return redirect('superadminapp:Template')
        return render(request, "template_create.html", {  'cat_table': cat_table,
                                                        # "userimage":userimage
                                                        })
    else:
        return redirect('superadminapp:login')

def template_create_membership(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        try:
            category = categories.objects.get(category_name=category_name)
        except categories.DoesNotExist:
            return JsonResponse({'error': 'Category not found'})

        data = {
            'cat_ind_free': category.individual_free_Membership,
            'cat_ind_basic': category.individual_basic_Membership,
            'cat_ind_prem': category.individual_Premium_Membership,
            'cat_bus_free': category.business_free_Membership,
            'cat_bus_basic': category.business_basic_Membership,
            'cat_bus_prem': category.business_Premium_Membership,
        }
        return JsonResponse(data)

def template_create_second(request,templateid):
    temp = template.objects.filter(id=templateid)
    return render(request,"template_create_next.html",{"temp":temp})

def category_view(request):
    user_id = request.session.get('userid')
    if user_id:
        global category_id
        category_id = request.GET.get('category_id')
        category_name = request.GET.get('category_name')
        categorydata = categories.objects.filter(id=category_id)
        if category_id is not None:
           
            categorydata = categories.objects.filter(id=category_id)
            for i in categorydata:
                global c
                c = i.id
                a = i.category_name
                b = i.is_active
            global c_id
            c_id = c
            return render(request, "category.html", {"categotydata": categorydata})
        else:
            data = categories.objects.all().order_by('-id')
            # paginator = Paginator(data, 15)
            # page_number = request.GET.get('page')
            # page_obj = paginator.get_page(page_number)
        return render(request, "category.html", {"page_obj": data})
    else:
        return redirect('superadminapp:login')

def template_create_category(request):
    user_id = request.session.get('userid')
    if user_id:
        # print(category_id)
        if request.method == "POST":
            category_name = request.POST['category_name']
            category_name_arabic = request.POST['category_name_arabic']
            if categories.objects.filter(category_name=category_name).exists():
                messages.info(request, 'category Name is alredy used')
                # return redirect('http://127.0.0.1:8000/template_create_category/')
                return redirect('superadminapp:Template_Create_Category')
            # print(template_title)
            i_Premium_Membership = request.POST.get('i_Premium_Membership', 'False')
            i_Basic_Membership = request.POST.get('i_Basic_Membership', 'False')
            i_Free_Membership = request.POST.get('i_Free_Membership', 'False')
            
            b_Premium_Membership = request.POST.get('b_Premium_Membership', 'False')
            b_Basic_Membership = request.POST.get('b_Basic_Membership', 'False')
            b_Free_Membership = request.POST.get('b_Free_Membership', 'False')
            
            created_at = datetime.now()
            IS_ACTIVE = "True"
            
            # a = []
            
            # if i_Premium_Membership or i_Basic_Membership or i_Free_Membership:
            #     a.append('Individual Membership')
            # if b_Premium_Membership or b_Basic_Membership or b_Free_Membership:
            #     a.append('Business Membership')
            # i_Premium_Membership
            
            # if i_Premium_Membership:
            #     i_Premium_Membership = True
            # else:
            #     i_Premium_Membership = False
            # # i_Basic_Membership
            # if i_Basic_Membership:
            #     i_Basic_Membership = True
            # else:
            #     i_Basic_Membership = False           
            # # i_Free_Membership
            # if i_Free_Membership:
            #     i_Free_Membership = True
            # else:
            #     i_Free_Membership = False 
                
            # # b_Premium_Membership
            # if b_Premium_Membership:
            #     b_Premium_Membership = True
            # else:
            #     b_Premium_Membership = False 
            # # b_Basic_Membership
            # if b_Basic_Membership:
            #     b_Basic_Membership = True
            # else:
            #     b_Basic_Membership = False 
            # # b_Free_Membership
            # if b_Free_Membership:
            #     b_Free_Membership = True
            # else:
            #     b_Free_Membership = False 
                
            
            # print(i_Premium_Membership,"ind p",i_Basic_Membership,"ind b",i_Free_Membership,"ind f",".....................",b_Premium_Membership,"ind p",b_Basic_Membership,"ind b",b_Free_Membership,"ind f")
            # create category
            try:
                abc = categories.objects.create(
                    category_name=category_name,
                    category_name_arabic = category_name_arabic,
                    # category_availability=a,
                    # is_premium=is_premium,
                    individual_Premium_Membership = i_Premium_Membership,
                    individual_basic_Membership = i_Basic_Membership,
                    individual_free_Membership = i_Free_Membership ,
                    business_Premium_Membership = b_Premium_Membership,
                    business_basic_Membership = b_Basic_Membership,
                    business_free_Membership = b_Free_Membership,
                    is_active=IS_ACTIVE,
                    created_at=created_at
                )
                abc.save()
            except Exception as e:
                return HttpResponse(f'<h3>Error create category: {e} </h3>')
            try:
                log_activity(request,user_id,"create category")
            except Exception as e:
                return render(request , "connection_error.html")
            
            data = categories.objects.all()
            messages.info(request, 'Category Created')
            return redirect('superadminapp:Category')
        return render(request, "template_create_category.html")
    else:
        return redirect('superadminapp:login')

def update_category(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":
            # print(request.method)
            c_id = request.POST.get('c_id')
            categori_name = request.POST['category_name']
            categori_name_arabic = request.POST['category_name_arabic']
            i_Premium_Membership = request.POST.get('i_Premium_Membership', 'False')
            i_Basic_Membership = request.POST.get('i_Basic_Membership', 'False')
            i_Free_Membership = request.POST.get('i_Free_Membership', 'False')
            b_Premium_Membership = request.POST.get('b_Premium_Membership', 'False')
            b_Basic_Membership = request.POST.get('b_Basic_Membership', 'False')
            b_Free_Membership = request.POST.get('b_Free_Membership', 'False')
            ACTIVE = request.POST.get('is_active')
            # print("...............")
            # print(ACTIVE)
            if ACTIVE is None:
                ACTIVE = False
            if ACTIVE == 'true':
                ACTIVE = True
            # a = []    
            # if i_Premium_Membership or i_Basic_Membership or i_Free_Membership:
            #     a.append('Individual Membership')
            # if b_Premium_Membership or b_Basic_Membership or b_Free_Membership:
            #     a.append('Business Membership')
            # i_Premium_Membership
            # if i_Premium_Membership:
            #     i_Premium_Membership = True
            # else:
            #     i_Premium_Membership = False
            # # i_Basic_Membership
            # if i_Basic_Membership:
            #     i_Basic_Membership = True
            # else:
            #     i_Basic_Membership = False           
            # # i_Free_Membership
            # if i_Free_Membership:
            #     i_Free_Membership = True
            # else:
            #     i_Free_Membership = False 
                
            # # b_Premium_Membership
            # if b_Premium_Membership:
            #     b_Premium_Membership = True
            # else:
            #     b_Premium_Membership = False 
            # # b_Basic_Membership
            # if b_Basic_Membership:
            #     b_Basic_Membership = True
            # else:
            #     b_Basic_Membership = False 
            # # b_Free_Membership
            # if b_Free_Membership:
            #     b_Free_Membership = True
            # else:
            #     b_Free_Membership = False 

            # print(i_Premium_Membership,i_Basic_Membership,i_Free_Membership,".....................",b_Premium_Membership,b_Basic_Membership,b_Free_Membership)   
            try: 
                category = categories.objects.get(id=c_id)
                category.category_name = categori_name
                category.category_name_arabic = categori_name_arabic
                category.is_active = ACTIVE
                # category.is_premium = x
                category.individual_Premium_Membership = i_Premium_Membership
                category.individual_basic_Membership = i_Basic_Membership
                category.individual_free_Membership = i_Free_Membership
                category.business_Premium_Membership = b_Premium_Membership
                category.business_basic_Membership = b_Basic_Membership
                category.business_free_Membership = b_Free_Membership
                category.save()
            except Exception as e:
                return HttpResponse(f'<h3>Error update category: {e} </h3>')
            # print(i_Premium_Membership,"---------------------------")
            try:
                template.objects.filter(category=c_id).update(
                    individual_premium_template=i_Premium_Membership,
                    individual_basic_template=i_Basic_Membership,
                    individual_free_template=i_Free_Membership,
                    business_premium_template=b_Premium_Membership,
                    business_basic_template=b_Basic_Membership,
                    business_free_template=b_Free_Membership
                )
            except Exception as e:
                return HttpResponse(f'<h3>Error update category membership: {e} </h3>')
            
            try:
                log_activity(request,user_id,"update category")
            except Exception as e:
                return render(request , "connection_error.html")

            messages.info(request, 'Category Updated')
            return redirect("/category/")
        data = categories.objects.all().order_by('id')
        return render(request,"category.html",{'data':data})
    else:
        return redirect('superadminapp:login')

def user(request):
    user_id = request.session.get('userid')
    if user_id:
        # try:
        #     user = Users.objects.get(id=user_id)
        #     userimage = user.image
        # except ObjectDoesNotExist:
        #     # Handle the case when the user does not exist.
        #     user = None
        #     userimage = None
       
        # users_data = Users.objects.filter(user_type="Individual User").order_by('-id')
        # business_users_data = Users.objects.filter(user_type="business_user").order_by('-id')    
        # business_admin_data = Users.objects.filter(user_type="Business Admin").order_by('-id')
        users_data = Users.objects.filter(Q(user_type="Individual User") & Q(active_status='active') | Q(active_status='blocked')).order_by('-pk')
        business_users_data = Users.objects.filter(Q(Q(user_type="Business User") |Q (user_type="business_user" ))  & Q(active_status='active')).order_by('-id') 
        business_admin_data = Users.objects.filter(Q(user_type="Business Admin") & Q(active_status='active')).order_by('-id')
        
        invited_users_data = Users.objects.filter(Q(user_type="Individual User") & Q(active_status='Inactive')).order_by('-pk')
        invited_business_admin_data = Users.objects.filter(Q(user_type="Business Admin") & Q(active_status='Inactive')).order_by('-id')
        # paginator = Paginator(users_data, 15)
        # page_number = request.GET.get('page')
        # users = paginator.get_page(page_number)
        
        # paginatorb = Paginator(business_users_data, 15)
        # page_numberb = request.GET.get('pageB')
        # business_users = paginatorb.get_page(page_numberb)
        
        # paginatorA = Paginator(business_admin_data, 15)
        # page_numberA = request.GET.get('pageA')
        # business_admin = paginatorA.get_page(page_numberA)
        
        count_I = Users.objects.filter(user_type="Individual User").count()
        count_B = Users.objects.filter(user_type="Business User").count()
        count_A = Users.objects.filter(user_type="Business Admin").count()

        user_dict = {
            'count_I' : count_I,
            'count_B' : count_B,
            'count_A' : count_A,
            'count_Total' : count_I + count_B + count_A,
            'users':users_data,
            'business_users':business_users_data,
            'business_admin':business_admin_data,
            'invited_users_data':invited_users_data,
            'invited_business_admin':invited_business_admin_data,
           
            # "userimage":userimage
        }

        return render(request, 'user.html', user_dict)  
    else:
        return redirect('superadminapp:login')
   
def invite_user(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":
            Civil_id = request.POST['Civil_id']
            email = request.POST['EmailAddress']
            created_at = datetime.now()
            user_type = "Individual User"
            active_status = "Inactive"
            status = False
            
            try:
                creat = Users.objects.create(
                    civil_id = Civil_id,
                    email  =  email,
                    created_at = created_at,
                    user_type = "Individual User",
                    active_status ="Inactive",
                    status = False,
                    hawati_verification=False
                )
                creat.save()
            except Exception as e:
                return HttpResponse(f'<h3>Error invite user: {e} </h3>')
            
            try:
                log_activity(request,user_id,"invite user")
            except Exception as e:
                return render(request , "connection_error.html")
            
            try:
                
                # verification_token = str(uuid.uuid4())
                loginlink = 'https://versionreview.com/tothiqweb/en/'
                subject = "Activate Your Tothiq Account and Join the Tothiq Community!"
                body = format_html(
                    '<p> Hello,</p>'
                    '<p> You have been invited to join Tothiq.</p>'
                    '<p> Here are the details of your invitation:</p>'
                    '<ul>'
                    f'<li><b>Email</b>: {email}</li>' 
                    f'<li><b>Civil ID</b>: {Civil_id}</li>'
                    f'<li><b>User Type</b>: {user_type}</li>'
                    '</ul>'
                    '<p> If you have any questions or need further assistance, please feel free to contact us. Thank you for choosing Tothiq!</p>'
                    '<p> To activate your account and unlock all the exciting features, please click on the following link:</p>'
                    f'<p><a href="{loginlink}">Activate Your Tothiq Account</a></p>'
                    '<p> Kindly fill up the necessary fields to complete your registration.</p>'
                    '<p> Best regards,\nThe Tothiq Team</p>'
                )
                recipient_email = email

                send_email_test(subject, body, recipient_email)
                # send_mail(
                #         subject,
                #         message,
                #         EMAIL_HOST_USER,
                #         [recipient],
                #         fail_silently=False,
                #     )
                messages.info(request, 'Individual User have been Invited.')
                return redirect('superadminapp:User')
            except Exception as e:
                # Return an error response
                return HttpResponse(f'<h3>Error sending email: {e}</h3>')
    else:
        return redirect('superadminapp:login')
    
def invite_business(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":
            
            CompanyName = request.POST['CompanyName']
            email= request.POST['EmailAddress']
            created_at = datetime.now()
            user_type = "Business Admin"
            active_status = "Inactive"
            status = False
            try:
                creat = Users.objects.create(
                    company_name = CompanyName,
                    email  =  email,
                    created_at = created_at,
                    user_type = user_type,
                    active_status = active_status,
                    status = status
                )
                creat.save()
            except Exception as e:
                return HttpResponse(f'<h3>Error invite business: {e} </h3>')
        
            user_instance = Users.objects.get(created_at=created_at)
            u_id = user_instance
            i = u_id.id
            add = business_info.objects.create(
                business_name = CompanyName,
                business_email_address = email,
                created_at = created_at,
                active_status = "Inactive",
                user=u_id
            )
            add.save()
            try:
                log_activity(request,user_id,"invite business")
            except Exception as e:
                return render(request , "connection_error.html")
            
            try:
                loginlink = 'https://versionreview.com/tothiqweb/en/'
                subject = "Activate Your Tothiq Account and Join the Tothiq Community!"
                body = format_html(
                    '<p>Hello,</p>'
                    '<p>You have been invited to join Tothiq.</p>'
                    '<p>Here are the details of your invitation:</p>'
                    f'<p>Email: {email}</p>'
                    f'<p>Company Name: {CompanyName}</p>'
                    f'<p>User Type: {user_type}</p>'
                    '<p>If you have any questions or need further assistance, please feel free to contact us. Thank you for choosing Tothiq!</p>'
                    '<p>To activate your account and unlock all the exciting features, please click on the following link:</p>'
                    f'<a href="{loginlink}">Activate Your Tothiq Account</a>'
                    '<p>Kindly fill up the necessary fields to complete your registration.</p>'
                    '<p>Best regards,<br>The Tothiq Team</p>'
                )
                recipient_email = email
                send_email_test(subject, body, recipient_email)
                # send_mail(
                #         subject,
                #         message,
                #         EMAIL_HOST_USER,
                #         [recipient],
                #         fail_silently=False,
                #     )
                messages.info(request, 'Business Admin have been Invited.')
                return redirect('superadminapp:User')
            except Exception as e:
                # Return an error response
                return HttpResponse(f'<h3>Error sending email: {e}</h3>')
            
           
    else:
        return redirect('superadminapp:login')

def validate_Email(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == 'POST':
            data = request.body.decode('utf-8')
            entered_email = json.loads(data).get('password')
            email1 = Users.objects.filter(email=entered_email)
            if email1:
                is_valid = False
            else:
                is_valid = True
            # Perform password validation using Django's check_password function
            return JsonResponse({'is_valid': is_valid})
    else:
        return redirect('superadminapp:login')

def add_user(request):
    user_id = request.session.get('userid')
    if user_id:
        
        if request.method == "POST":  
            var1 = request.POST.get("CompanyName")
            var2 = request.POST.get("EmailAddress")

            business_admin = Users(
                company_name = var1,
                email = var2,
                user_type = "Business Admin",
                active_status = "inactive",
                created_at = datetime.now(),
            )
            # info = Users(
            #     company_name = var1,
            #     email = var2,
            #     active_status = "inactive",
            #     created_at = datetime.now(),
            # )
            business_admin.save()
            # info.save()          
        return redirect('superadminapp:User')
    else:
        return redirect('superadminapp:login')

def user_individual_add_contracts(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":
            uid = request.POST.get("uid") 
            contracts = request.POST.get("contractsinput") 
            contracts = int(contracts)
            if contracts > 0:
                msg = "Add"
            else:
                msg = "Deduct"
            user_instance = Users.objects.get(pk=uid)
            
            if msg ==  "Add":
                action_info_msg = "admin added"
            else:
                action_info_msg = "admin deduct"
           
            contract_histroy.objects.create(
                user=user_instance,
                contracts=contracts,
                action_type=msg,
                action_info=action_info_msg,
                created_at=datetime.now()
            )
            try:
                log_activity(request,user_id,"user add contracts")
            except Exception as e:
                return render(request , "connection_error.html")
            oldemail = Users.objects.filter(id=uid)
            
            for i in oldemail:
                oldmail = i.email
                
            try:
                
                subject = " Successful Contract Addition."
                body = 'Congratulations! Your contract has been successfully added to your account. If you have any questions or need further assistance, please do not hesitate to reach out.'
                recipient_email = oldmail

                send_email_test(subject, body, recipient_email)

                # send_mail(
                #         subject,
                #         message,
                #         EMAIL_HOST_USER,
                #         [recipient],
                #         fail_silently=False,
                #     )
            except Exception as e:
                return HttpResponse(f'<h3>Error sending email: {e}</h3>')
                
               
        if msg == "Add":
            messages.info(request, 'Contracts added')
        else:
            messages.info(request, 'Contracts deducted')
        return redirect('superadminapp:User_Individual_User_Details' ,  uid=uid)
    else:
        return redirect('superadminapp:login')

def user_individual_custom_package(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method== "POST":
            uid = request.POST.get("uid") 
            user_instance = Users.objects.get(pk=uid)
            custompackageinput = request.POST["custompackageinput"]
            percontractPrice = request.POST["percontract"]
            totalprice = float(custompackageinput)*float(percontractPrice)
            try:
                # user = User.objects.get(username=user_instance.username)
                token = Token.objects.get(user=uid)
                token_value = token.key
            except (Token.DoesNotExist):
                # Handle the case where the user or token does not exist
                token_value = "token not found..."
            api_url = "http://127.0.0.1:8000//masterapp/payment-init"
            headers = {
                "Authorization": f"Token {token_value}" if token_value else ""
            }
            payload = {
                "payment_type": "contracts",
                "payment_method": "myfatoorah",
                "purchase_id": custompackageinput
                }
            try:
                response = requests.post(api_url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    api_data = response.json()
                    payment_url = api_data.get("data", {}).get("payment_url")

                    # Send payment URL in email
                    subject = "Payment Initiated for Custom Package"
                    body = format_html(
                            '<p>We are thrilled to inform you that you have initiated payment for a custom package.</p>'
                            '<p><strong>Package Details:</strong></p>'
                            '<ul>'
                            f'<li>Package Name: Custom Package</li>'
                            f'<li>Contract quantity: {custompackageinput}</li>'
                            f'<li>Contract Price: KD {percontractPrice}</li>'
                            f'<li>Total Price: KD {totalprice}</li>'
                            '</ul>'
                            '<p>To complete the payment and activate your custom package, please click the following link:</p>'
                            f'<a href="{payment_url}">Payment Link</a>'
                            '<p>If you have any questions or need further assistance, please do not hesitate to reach out to our support team.</p>'
                            '<p>Thank you for choosing our services! We look forward to serving you.</p>'
                        )

                    recipient_email = user_instance.email

                    send_email_test(subject, body, recipient_email)
                    # send_mail(
                    #     subject,
                    #     message,
                    #     EMAIL_HOST_USER,
                    #     [recipient],
                    #     fail_silently=False,
                    # )
                    try:
                        log_activity(request, user_id, "send payment link email to user for custom package")
                    except Exception as e:
                        return render(request , "connection_error.html")
                    
                    messages.info(request, 'Send payment link email to user for custom package')
                    return redirect('superadminapp:User_Individual_User_Details', uid=uid)
                else:
                    # Handle API error here
                    return HttpResponse(f'<h3>Error calling payment API: {response.status_code} </h3>')
            except Exception as e:
                return HttpResponse(f'<h3>Error calling payment API: {e}</h3>')
    else:
        return redirect('superadminapp:login')

def user_individual_upgrade_membership(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":
            uid = request.POST.get("uid") 
            user_instance = Users.objects.get(pk=uid)
            
            memnameinput = request.POST.get("memnameinput") 
            mem_instance = Membership.objects.get(pk=memnameinput)
            start_date_str = request.POST.get("start_datetime") 
            end_date_str = request.POST.get("end_datetime") 
            
            one_year_date=""
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            if end_date_str =="":
                one_year_duration = timedelta(days=365)
                one_year_date = start_date + one_year_duration
            else:
                one_year_date = datetime.strptime(end_date_str, '%Y-%m-%d')
             
            created_at = datetime.now()
            total_amount = None
            discount_rate = None
            discount_amount = None
            net_amount = None
            rp = request.POST.get('aum', 'NO') 
            if rp == "YES":
                rp = "True"
                # Fetch the user and token
                try:
                  
                    # user = User.objects.get(username=user_instance.username)
                    token = Token.objects.get(user=uid)
                    token_value = token.key
                except (Token.DoesNotExist):
                    # Handle the case where the user or token does not exist
                    token_value = "token not found..."
                api_url = "http://127.0.0.1:8000//masterapp/payment-init"
                headers = {
                    "Authorization": f"Token {token_value}" if token_value else ""
                }
                payload = {
                    "payment_type": "membership",
                    "payment_method": "myfatoorah",
                    "purchase_id": memnameinput
                    }
                try:
                    response = requests.post(api_url, json=payload, headers=headers)
          
                    if response.status_code == 200:
                        api_data = response.json()
                        
                        payment_url = api_data.get("data", {}).get("payment_url")
                        # Send payment URL in email
                        subject = "Upgrade Your Membership - Payment Link"
                        body = f"Payment has been initiated for your contract. Please proceed to make the payment by clicking the following link: {payment_url}"
                        
                        body = format_html(
                            
                            '<p> Upgrade your membership to access exclusive benefits and premium content. To complete the process, please click the link below to make your payment. </p>'
                            f'<a href="{payment_url}">Payment Link</a>'
                            '<p>If you have any questions or need further assistance, please do not hesitate to reach out to our support team.</p>'
                            '<p>Thank you for choosing our services! We look forward to serving you.</p>'
                        )
                         
                        recipient_email = user_instance.email

                        send_email_test(subject, body, recipient_email)
                        # send_mail(
                        #     subject,
                        #     message,
                        #     EMAIL_HOST_USER,
                        #     [recipient],
                        #     fail_silently=False,
                        # )
                        try:
                            log_activity(request, user_id, "send payment link email to user for upgrade membership ")
                        except Exception as e:
                            return render(request , "connection_error.html")                    
                        messages.info(request, 'Send payment link email to user for upgrade membership')
                        return redirect('superadminapp:User_Individual_User_Details', uid=uid)
                    else:
                        # Handle API error here
                        return HttpResponse(f'<h3>Error calling payment API: {response.status_code} </h3>')
                except Exception as e:
                    return HttpResponse(f'<h3>Error calling payment API: {e}</h3>')
            else:
                rp = "False"
                # If rp is not True, continue with the rest of your code
                total_amount = 0
                discount_rate = 0
                discount_amount = 0
                net_amount = 0
        
                UserMembership.objects.create(
                    user=user_instance,
                    membership=mem_instance,
                    start_date=start_date,
                    end_date=one_year_date,
                    total_amount=total_amount,
                    discount_rate=discount_rate,
                    discount_amount=discount_amount,
                    net_amount=net_amount,
                    active_status="inactive",
                    created_at=datetime.now()
                )
                try:
                    log_activity(request, user_id, "user upgrade membership")
                except Exception as e:
                    return render(request , "connection_error.html")                    

                oldemail = Users.objects.filter(id=uid)
                for i in oldemail:
                    oldmail = i.email
                try:
                    subject = " Successful Membership Upgrade."
                    message = 'Congratulations! Your membership is successfult upgraded to your account. If you have any questions or need further assistance, please do not hesitate to reach out.'
                    recipient = oldmail

                    send_mail(
                        subject,
                        message,
                        EMAIL_HOST_USER,
                        [recipient],
                        fail_silently=False,
                    )
                except Exception as e:
                    return HttpResponse(f'<h3>Error sending email: {e}</h3>')
                        
                messages.info(request, 'Upgraded Membership')
                return redirect('superadminapp:User_Individual_User_Details', uid=uid)
            
        return redirect('superadminapp:User_Individual_User_Details', uid=uid)
    else:
        return redirect('superadminapp:login')

def user_individual_user_details(request,uid):
    user_id = request.session.get('userid')
    if user_id:
        # try:
        #     user = Users.objects.get(id=user_id)
        #     userimage = user.image
        # except ObjectDoesNotExist:
        #     # Handle the case when the user does not exist.
        #     user = None
        #     userimage = None
        # user = Users.objects.get(id=user_id)
        # userimage = user.image
        stng = GeneralSettings.objects.all()
        memname = Membership.objects.filter(user_type='Individual User', membership_amount__gt=0).order_by("id")
    
        # memname = Membership.objects.filter(user_type='Individual User', membership_amount != 0).order_by("id")
        uid=uid
        for i in stng:
            hlg = i.web_panel_header_logo
            wptx = i.webpanel_title_text
            crtx = i.webPanel_copyright_text
            c_p = i.contracts_price
            u_p = i.users_price
        user_detail = Users.objects.filter(pk=uid)
        # for mediaimg in user_detail:
        #     img = mediaimg.image
        #     if isinstance(img, File):
        #         media_path = img.path
        #         file_exists = os.path.exists(media_path)
        #     else:
        #         media_path = None
        #         file_exists = False
                
        nationality = nationality_type.objects.all()
        payment_history =Payment.objects.filter(user=uid, payment_status = 'paid')

        draft = contracts.objects.filter(user_id=uid,status='draft').count()
        review = contracts.objects.filter(user_id=uid,status='review').count()
        ready = contracts.objects.filter(user_id=uid,status='ready').count()
        signed = contracts.objects.filter(user_id=uid,status='signed').count()
        cancel = contracts.objects.filter(Q(user_id=uid,status='deleted')|Q(user_id=uid,status='rejected')|Q(user_id=uid,status='cancelled')).count()
        return render(request, "user_individual_user_details.html",{"hlg":hlg,
                                                                    # "userimage":userimage,
                                                                    "wptx":wptx,"crtx":crtx,"c_p":c_p,"u_p":u_p,"memname":memname,"uid":uid,"userdetail":user_detail,"nationality":nationality,"draft":draft,"review":review,"ready":ready,"signed":signed,"cancel":cancel,"payment_history":payment_history})
    else:
        return redirect('superadminapp:login')

def user_business_user_details(request,id):
    user_id = request.session.get('userid')
    if user_id:
        # try:
        #     user = Users.objects.get(id=user_id)
        #     userimage = user.image
        # except ObjectDoesNotExist:
        #     # Handle the case when the user does not exist.
        #     user = None
        #     userimage = None
        # user = Users.objects.get(id=user_id)
        # userimage = user.image
       
        user_detail = Users.objects.filter(pk=id)
        # for mediaimg in user_detail:
        #     img = mediaimg.image
        #     if isinstance(img, File):
        #         media_path = img.path
        #         file_exists = os.path.exists(media_path)
        #     else:
        #         media_path = None
        #         file_exists = False
        nationality = nationality_type.objects.all()
        extention = business_info.objects.filter(user_id=id)
        # print(extention)
        draft = contracts.objects.filter(user_id=id,status='draft').count()
        review = contracts.objects.filter(user_id=id,status='review').count()
        ready = contracts.objects.filter(user_id=id,status='ready').count()
        signed = contracts.objects.filter(user_id=id,status='signed').count()
        cancel = contracts.objects.filter(Q(user_id=id,status='deleted')|Q(user_id=id,status='rejected')|Q(user_id=id,status='cancelled')).count()
        return render(request, "user_business_user_details.html",{ "userdetail":user_detail,
                                                                #   "userimage":userimage,
                                                                  "nationality":nationality,"extention":extention,"draft":draft,"review":review,"ready":ready,"signed":signed,"cancel":cancel})
    else:
        return redirect('superadminapp:login')

def business_admin_custom_package(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method== "POST":
            uid = request.POST.get("uid") 
            user_instance = Users.objects.get(pk=uid)
            custompackageinput = request.POST["custompackageinput"]
            percontractPrice = request.POST["percontract"]
            totalprice = float(custompackageinput)*float(percontractPrice)
            try:
                # user = User.objects.get(username=user_instance.username)
                token = Token.objects.get(user=uid)
                token_value = token.key
            except (Token.DoesNotExist):
                # Handle the case where the user or token does not exist
                token_value = "token not found..."
            api_url = "http://127.0.0.1:8000//masterapp/payment-init"
            headers = {
                "Authorization": f"Token {token_value}" if token_value else ""
            }
            payload = {
                "payment_type": "contracts",
                "payment_method": "myfatoorah",
                "purchase_id": custompackageinput
                }
            try:
                response = requests.post(api_url, json=payload, headers=headers)

                if response.status_code == 200:
                    api_data = response.json()
                    
                    payment_url = api_data.get("data", {}).get("payment_url")
                    
                    # Send payment URL in email
                    subject = "Payment Initiated for Custom Package"
                    body = format_html(
                        '<p>We are thrilled to inform you that you have initiated payment for a custom package.</p>'
                        '<p><strong>Package Details:</strong></p>'
                        '<ul>'
                        f'<li>Package Name: Custom Package</li>'
                        f'<li>Contract quantity: {custompackageinput}</li>'
                        f'<li>Contract Price: KD {percontractPrice}</li>'
                        f'<li>Total Price: KD {totalprice}</li>'
                        '</ul>'
                        '<p>To complete the payment and activate your custom package, please click the following link:</p>'
                        f'<a href="{payment_url}">Payment Link</a>'
                        '<p>If you have any questions or need further assistance, please do not hesitate to reach out to our support team.</p>'
                        '<p>Thank you for choosing our services! We look forward to serving you.</p>'
                    )

                    recipient_email = user_instance.email
                    send_email_test(subject, body, recipient_email)
                    # send_mail(
                    #     subject,
                    #     message,
                    #     EMAIL_HOST_USER,
                    #     [recipient],
                    #     fail_silently=False,
                    # )
                    try:
                        log_activity(request, user_id, "send payment link email to business admin for custom package")
                    except Exception as e:
                        return render(request , "connection_error.html")                     
                    messages.info(request, 'Send payment link email to  business admin for custom package')
                    return redirect('superadminapp:User_Business_admin_Details', id=uid)
                else:
                    # Handle API error here
                    return HttpResponse(f'<h3>Error calling payment API: {response.status_code} </h3>')
            except Exception as e:
                return HttpResponse(f'<h3>Error calling payment API: {e}</h3>')
    else:
        return redirect('superadminapp:login')
    
def business_admin_user_custom_package(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method== "POST":
            uid = request.POST.get("uid") 
            user_instance = Users.objects.get(pk=uid)
            custompackageinput = request.POST["usercustompackageinput"]
            percontractPrice = request.POST["peruser"]
            totalprice = float(custompackageinput)*float(percontractPrice)
            try:
                # user = User.objects.get(username=user_instance.username)
                token = Token.objects.get(user=uid)
                token_value = token.key
            except (Token.DoesNotExist):
                # Handle the case where the user or token does not exist
                token_value = "token not found..."
            api_url = "http://127.0.0.1:8000//masterapp/payment-init"
            headers = {
                "Authorization": f"Token {token_value}" if token_value else ""
            }
            payload = {
                "payment_type": "contracts",
                "payment_method": "myfatoorah",
                "purchase_id": custompackageinput
                }
            try:
                response = requests.post(api_url, json=payload, headers=headers)

                if response.status_code == 200:
                    api_data = response.json()
                    
                    payment_url = api_data.get("data", {}).get("payment_url")
                    
                    # Send payment URL in email
                    subject = "Payment Initiated for Custom Package"
                    body = format_html(
                        '<p>We are thrilled to inform you that you have initiated payment for a custom package.</p>'
                        '<p><strong>Package Details:</strong></p>'
                        '<ul>'
                        f'<li>Package Name: Custom Package</li>'
                        f'<li>User quantity: {custompackageinput}</li>'
                        f'<li>User Price: KD {percontractPrice}</li>'
                        f'<li>Total Price: KD {totalprice}</li>'
                        '</ul>'
                        '<p>To complete the payment and activate your custom package, please click the following link:</p>'
                        f'<a href="{payment_url}">Payment Link</a>'
                        '<p>If you have any questions or need further assistance, please do not hesitate to reach out to our support team.</p>'
                        '<p>Thank you for choosing our services! We look forward to serving you.</p>'
                    )

                    recipient_email = user_instance.email
                    send_email_test(subject, body, recipient_email)
                    # send_mail(
                    #     subject,
                    #     message,
                    #     EMAIL_HOST_USER,
                    #     [recipient],
                    #     fail_silently=False,
                    # )
                    try:
                        log_activity(request, user_id, "send payment link email to business admin for user custom package")
                    except Exception as e:
                        return render(request , "connection_error.html")                     
                    messages.info(request, 'Send payment link email to  business admin for user custom package')
                    return redirect('superadminapp:User_Business_admin_Details', id=uid)
                else:
                    # Handle API error here
                    return HttpResponse(f'<h3>Error calling payment API: {response.status_code} </h3>')
            except Exception as e:
                return HttpResponse(f'<h3>Error calling payment API: {e}</h3>')
    else:
        return redirect('superadminapp:login')
    
def user_business_admin_details(request,id):
    user_id = request.session.get('userid')
    if user_id:
        # print(id)
        user_detail = Users.objects.filter(pk=id)
        nationality = nationality_type.objects.all()
        extention = business_info.objects.filter(user_id=id)
        draft = contracts.objects.filter(user_id=id,status='draft').count()
        review = contracts.objects.filter(user_id=id,status='review').count()
        ready = contracts.objects.filter(user_id=id,status='ready').count()
        signed = contracts.objects.filter(user_id=id,status='signed').count()
        cancel = contracts.objects.filter(Q(user_id=id,status='deleted')|Q(user_id=id,status='rejected')|Q(user_id=id,status='cancelled')).count()
        payment_history =Payment.objects.filter(user=id)
        stng = GeneralSettings.objects.all()
        for i in stng:
            c_p = i.contracts_price
            u_p = i.users_price
        return render(request, "user_business_admin_details.html",{"user_detail":user_detail,"nationality":nationality,"extention":extention,"draft":draft,"review":review,"ready":ready,"signed":signed,"cancel":cancel,"c_p":c_p,"u_p":u_p,"uid":id})
    else:
        return redirect('superadminapp:login')
    
def membership(request):
    user_id = request.session.get('userid')
    if user_id:
        # try:
        #     user = Users.objects.get(id=user_id)
        #     userimage = user.image
        # except ObjectDoesNotExist:
        #     # Handle the case when the user does not exist.
        #     user = None
        #     userimage = None
           
        # indi_f_table = Membership.objects.filter(user_type="Individual User",membership_name="Free")
        indi_f_table = Membership.objects.filter(id=1)
        for i in indi_f_table:
            enable1 = ''
            if i.discount_type == "percentage":
                enable1 = "Discount Percentage"
            else:
                enable1 = "Fixed Discount Price" 
        # indi_b_table = Membership.objects.filter(user_type="Individual User",membership_name="Basic")
        indi_b_table = Membership.objects.filter(id=2)
        for i in indi_b_table:
            enable2 = ''
            if i.discount_type == "percentage":
                enable2 = "Discount Percentage"
            else:
                enable2 = "Fixed Discount Price" 
           
        # indi_p_table = Membership.objects.filter(user_type="Individual User",membership_name="Premium")
        indi_p_table = Membership.objects.filter(id=3)
        for i in indi_p_table:
            enable3 = ''
            if i.discount_type == "percentage":
                enable3 = "Discount Percentage"
            else:
                enable3 = "Fixed Discount Price" 
           
        # indi_d_table = Membership.objects.filter(user_type="Individual User",membership_name="Gold")
        indi_d_table = Membership.objects.filter(id=7)
        for i in indi_d_table:
            enable7 = ''
            if i.discount_type == "percentage":
                enable7 = "Discount Percentage"
            else:
                enable7 = "Fixed Discount Price" 
            # print("-------------------------------------------------------")
            # print(i.id)
            # print(enable7)
            # print("-------------------------------------------------------")
        # indi_pla_table = Membership.objects.filter(user_type="Individual User",membership_name="Platinum")
        indi_pla_table = Membership.objects.filter(id=8)
        for i in indi_pla_table:
            
            enable8 = ''
            if i.discount_type == "percentage":
                enable8 = "Discount Percentage"
            else:
                enable8 = "Fixed Discount Price" 
        # buss_f_table = Membership.objects.filter(user_type="Business Admin",membership_name="Free")
        buss_f_table = Membership.objects.filter(id=4)
        for i in buss_f_table:
            enable4 = ''
            if i.discount_type == "percentage":
                enable4 = "Discount Percentage"
            else:
                enable4 = "Fixed Discount Price" 
        # buss_b_table = Membership.objects.filter(user_type="Business Admin",membership_name="Basic")
        buss_b_table = Membership.objects.filter(id=5)
        for i in buss_b_table:
            enable5 = ''
            if i.discount_type == "percentage":
                enable5 = "Discount Percentage"
            else:
                enable5 = "Fixed Discount Price" 
        # buss_p_table = Membership.objects.filter(user_type="Business Admin",membership_name="Premium")
        buss_p_table = Membership.objects.filter(id=6)
        for i in buss_p_table:
            enable6 = ''
            if i.discount_type == "percentage":
                enable6 = "Discount Percentage"
            else:
                enable6 = "Fixed Discount Price" 
        # buss_d_table = Membership.objects.filter(user_type="Business Admin",membership_name="Gold")
        buss_d_table = Membership.objects.filter(id=9)
        for i in buss_d_table:
            enable9 = ''
            if i.discount_type == "percentage":
                enable9 = "Discount Percentage"
            else:
                enable9 = "Fixed Discount Price" 
        # buss_pla_table = Membership.objects.filter(user_type="Business Admin",membership_name="Platinum")
        buss_pla_table = Membership.objects.filter(id=10)
        for i in buss_pla_table:
            enable10 = ''
            if i.discount_type == "percentage":
                enable10 = "Discount Percentage"
            else:
                enable10 = "Fixed Discount Price" 
        context = {"indi_f_table":indi_f_table,"indi_b_table":indi_b_table,"indi_p_table":indi_p_table,"indi_d_table":indi_d_table,"indi_pla_table":indi_pla_table,"buss_f_table":buss_f_table,"buss_b_table":buss_b_table,"buss_p_table":buss_p_table,"buss_d_table":buss_d_table,"buss_pla_table":buss_pla_table,"enable1":enable1,"enable2":enable2,"enable3":enable3,"enable4":enable4,"enable5":enable5,"enable6":enable6,"enable7":enable7,"enable8":enable8,"enable9":enable9,"enable10":enable10
                #    , "userimage":userimage
                   }
        return render(request, "membership.html", context)
    else:
        return redirect('superadminapp:login')

def update_membarship(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":
            up1 = request.POST['up1id']
            mem_name = request.POST.get('if_mem_name')
            mem_name_arabic = request.POST.get('if_mem_name_arabic')
            day_ava = request.POST['if_day_ava']
            if day_ava == "":
                day_ava = 0
            if 'if_mem_amount' in request.POST:
                mem_amount = request.POST['if_mem_amount']
                if mem_amount == "":
                    mem_amount = 0
                if mem_name == "Free":
                    mem_amount = 0                    
            else:
                mem_amount = None 
                
            try:
                if request.method == "POST":
                    dt  = request.POST.get('discount-type')
                    if dt == "Discount Percentage":
                        dt = "percentage"
                    else:
                        dt = "fixedprice"     
                disc_per = request.POST.get('disc_rate')
                if disc_per == "":
                    disc_per = 0
                dp = request.POST.get('if_mem_am_dis')
                if dp == "":
                    dp = 0
                knet = bool(request.POST.get('knet_name', False))
                cdc = bool(request.POST.get('cdcname', False))
                gp = bool(request.POST.get('gpname', False))
                ap = bool(request.POST.get('apname', False))

                num_contract = request.POST['if_num_con']
                if num_contract == "":
                    num_contract = 0
                num_part = request.POST['if_num_part']
                if num_part == "":
                    num_part = 0
                num_templates = request.POST['if_num_templates']
                if num_templates == "":
                    num_templates = 0
                num_users = request.POST.get('if_num_users', '')  # Provide a default value, e.g., '' or 0
                if num_users == "":
                    num_users = 0
                cbp = bool(request.POST.get('if_cbp', False))
                fbp_c_temp = bool(request.POST.get('if_ct', False))
                f_c_temp = bool(request.POST.get('if_f_ct', False))
                b_c_temp = bool(request.POST.get('if_b_ct', False))
                p_c_temp = bool(request.POST.get('if_p_ct', False))
                # u_c_temp = bool(request.POST.get('if_u_ct', False))
                add_book = bool(request.POST.get('if_ab', False))
                create_blank_c = bool(request.POST.get('if_cbc', False))
                upload_contract = bool(request.POST.get('if_uc', False))
                view_log = bool(request.POST.get('if_vl', False))
                vcs = bool(request.POST.get('if_vcs', False))
                if_fsu = bool(request.POST.get('if_fsu', False))
                
                if_ce = bool(request.POST.get('if_f_ce', False))
                if_rh = bool(request.POST.get('if_f_rh', False))
                dtu = bool(request.POST.get('is_active', False))
                
                if not (f_c_temp or b_c_temp or p_c_temp):
                    fbp_c_temp = False
            
                Membership.objects.filter(id=up1).update(
                    membership_name_arabic=mem_name_arabic,
                    membership_amount=mem_amount,
                    discount_type=dt,
                    discount_rate=disc_per,
                    discount_price=dp,
                    payment_gateway_kne=knet,
                    payment_gateway_cb_card=cdc,
                    payment_gateway_gp=gp,
                    payment_gateway_ap=ap,
                    number_of_contract=num_contract,
                    number_of_parties=num_part,
                    number_of_templates=num_templates,
                    number_of_user=num_users,
                    chat_between_parties=cbp,
                    
                    collaborative_editing=if_ce,
                    revision_history=if_rh,
                    
                    contract_template=fbp_c_temp,
                    free_template=f_c_temp,
                    basic_template=b_c_temp,
                    premium_template=p_c_temp,
                    
                    # unlimited_templates=u_c_temp,
                    address_book=add_book,
                    create_blank_contract=create_blank_c,
                    upload_contract=upload_contract,
                    view_log=view_log,
                    free_contract_storage=vcs,
                    free_sign_up=if_fsu,
                    private_or_not=dtu,
                    day_availability=day_ava,
                    
                    updated_at=datetime.now()
                )
                log_activity(request,user_id,"update membership")
                try:
                    log_activity(request, user_id, "send payment link email to business admin for user custom package")
                except Exception as e:
                    return render(request , "connection_error.html")
                
                messages.info(request,"Membership details have been updated.")
                
            except Exception as e:
                return HttpResponse(f'<h3>Error Membership Update</h3>')
        return redirect('superadminapp:Membership')
    else:
        return redirect('superadminapp:login')

def notification_bell(request):
    user_id = request.session.get('userid')
    if user_id:
        # user = Users.objects.get(id=user_id)
        # userimage = user.image
        return render(request, "notification_bell.html")
    else:
        return redirect('superadminapp:login')

def label(request):
    user_id = request.session.get('userid')
    if user_id:
        data = languages_label.objects.all().order_by('-id')
        
        # paginator = Paginator(data, 15)
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)

        
        return render(request, 'label_management.html', {'page_obj': data})
    else:
        return redirect('superadminapp:login')

def update_label(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":
            label_id = request.POST.get('label_id')
            english_name = request.POST.get('updated_English')
            arabic_name = request.POST.get('updated_Arabic')
            print(label_id,english_name,arabic_name,"-------------------------")
            try:
                label = languages_label.objects.get(id=label_id)
                label.english = english_name
                label.arabic = arabic_name
                label.save()
                messages.info(request,"Label have been updated.")
                return redirect("superadminapp:Label_Management")
            except Exception as e:
                return HttpResponse(f'<h3>Error Label Update: {e}</h3>')
    else:
        return redirect('superadminapp:login')

def coupon_management(request):
    user_id = request.session.get('userid')
    if user_id:
        # try:
        #     user = Users.objects.get(id=user_id)
        #     userimage = user.image
        # except ObjectDoesNotExist:
        #     # Handle the case when the user does not exist.
        #     user = None
        #     userimage = None
        # user = Users.objects.get(id=user_id)
        # userimage = user.image
        user = Users.objects.all().order_by('pk')
        data = Coupon.objects.all().order_by('-id')
        # paginator = Paginator(data, 10)
        # page_num = request.GET.get('page')
        # page_obj = paginator.get_page(page_num)
       
        return render(request,'coupon_management.html',{
            'page_obj':data,
            'user':user,
            #  "userimage":userimage
        })
    else:
        return redirect('superadminapp:login')

def coupon_management_details(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":  
            var1 = request.POST.get('coupon_name')
            var1_arabic = request.POST.get('coupon_name_arabic')
            var2 = request.POST.get('coupon_code')
            var3 = request.POST.get('start_datetime')
            var4 = request.POST.get('end_datetime')
            var5 = request.POST.get('limited_number_input')
            var6 = request.POST.get('discount_type')
            var7 = request.POST.get('discount_for')
            # var8 = request.POST.get('value')
            var9 = request.POST.get('limited_coupon_code')
            var10 = request.FILES.get('couponimageInput')
            var11 = request.POST.get('coupon_details')
            var11_arabic = request.POST.get('coupon_details_arabic')
            # var12 = request.POST.getlist('selected_user')
            var12 = request.POST.getlist('selected_user')
            selected_user_integers = list(set([int(user_id) for user_id in var12]))
            var13 = request.POST.getlist('discount_for_user_type')
            var14 = request.POST.get('couponrate')

            current_datetime = datetime.now()
            current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            if var3 <= current_datetime_str <= var4:
                active_status = "active"
            else :
                active_status = "inactive"
           
            print(var7)
            print(selected_user_integers)
            try:
                info = Coupon(
                coupon_name=var1,
                coupon_name_arabic=var1_arabic,
                coupon_code= var2,
                start_datetime =var3,
                end_datetime = var4,
                total_coupons = var5,
                discount_type = var6,
                discount_for = var13,
                # value = var8,
                limited_coupon_per_Customer = var9,
                banner_image = var10,
                coupon_details = var11,
                coupon_details_arabic = var11_arabic,
                selected_users = selected_user_integers,
                discount_for_user_type = var7,
                discount_rate = var14,
                active_status = active_status
                )
                # print("info",info)
                context = {'info':info}
                info.save()
            except Exception as e:
                return HttpResponse(f'<h3>Error create coupon: {e} </h3>')
            
            if not selected_user_integers or selected_user_integers == [] or selected_user_integers == [0]:
                users = Users.objects.all()
                for user in users:
                    alluser = user.id
                    selected_user_integers.append(alluser)
            if var12 == '1':
                if 0 in selected_user_integers:
                    users = Users.objects.all()
                    for user in users:
                        alluser = user.id
                        while 0 in selected_user_integers:
                            selected_user_integers.remove(0)
                        selected_user_integers.append(alluser)   
            elif var12 == '2' :
                if 0 in selected_user_integers:
                    users = Users.objects.filter(user_type = "Individual User")
                    for user in users:
                        alluser = user.id
                        while 0 in selected_user_integers:
                            selected_user_integers.remove(0)
                        selected_user_integers.append(alluser)  
            elif var12 == '3':
                if 0 in selected_user_integers:
                    users = Users.objects.filter(user_type = "Business User")
                    for user in users:
                        alluser = user.id
                        while 0 in selected_user_integers:
                            selected_user_integers.remove(0)
                        selected_user_integers.append(alluser)                
            while 0 in selected_user_integers:
                            selected_user_integers.remove(0)
            userseleceted= list(set(selected_user_integers))
            for id in userseleceted:   
                # print(id)
                user_data = Users.objects.get(id = id)
                template_code = "Coupon Created"
                email_code = {
                    'name' : user_data.full_name,
                    'email' : user_data.email
                }
                sendmailwithtemplate(template_code, email_code) # send mail to user for creating new coupon
                token = user_firebase_token.objects.filter(user = id)
                for user in token:
                    template_code = "Coupon"
                    notification_code = {
                        'name' : user_data.full_name,
                        'id' : user.firebase_token
                    }
                    sendnotificationwithtemplate(template_code, notification_code) # send notification with template to user for creating new coupon
            try:
                log_activity(request,user_id,"create coupon")
            except Exception as e:
                return render(request , "connection_error.html")        
        return redirect('/coupon_management/')     
    else:
        return redirect('superadminapp:login')     
    # return render(request,'coupon_management_details.html',context)

def update_coupon(request):
    user_id = request.session.get('userid')
    if user_id:
        
        if request.method == 'POST':
            coupon_Id = request.POST.get('id')
            var1 = request.POST.get('coupon_name')
            var1_arabic = request.POST.get('coupon_name_arabic')
            var2 = request.POST.get('coupon_code')
            var3 = request.POST.get('start_datetime')
            var4 = request.POST.get('end_datetime')
            var5 = request.POST.get('limited_number_input')
            var6 = request.POST.get('discount_type')
            var7 = request.POST.get('discount_for')
            # var8 = request.POST.get('value')
            var9 = request.POST.get('limited_coupon_code')
            var10 = request.FILES.get('mmwpiimageInput')
            if var10==None:
                coupontable = Coupon.objects.get(id=coupon_Id)
                var10 = coupontable.banner_image
            var11 = request.POST.get('coupon_details')
            var11_arabic = request.POST.get('coupon_details_arabic')
            # var12 = request.POST.getlist('selected_user')
            var12 = request.POST.getlist('selected_user')
            selected_user_integers = list(set([int(user_id) for user_id in var12]))
    
            current_datetime = datetime.now()
            current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            if var3 <= current_datetime_str <= var4:
                active_status = "active"
            else :
                active_status = "inactive"
    
            var13 = request.POST.getlist('discount_for_user_type')
            var14 = request.POST.get('couponrate')
            # print(var3,"..........................................")
            # print(selected_user_integers,"..........................................")
            # print(current_datetime_str,"..........................................")
            try:
                coupon = Coupon.objects.get(id=coupon_Id)
                coupon.coupon_name = var1
                coupon.coupon_name_arabic = var1_arabic
                coupon.coupon_code= var2
                coupon.start_datetime = var3
                coupon.end_datetime = var4
                coupon.total_coupons = var5
                # coupon.discount_type = var6
                coupon.discount_for = var13
                # coupon.value = var8
                coupon.limited_coupon_per_Customer = var9
                coupon.banner_image = var10
                coupon.coupon_details = var11
                coupon.coupon_details_arabic = var11_arabic
                coupon.selected_users = selected_user_integers
                coupon.discount_for_user_type = var7
                coupon.active_status = active_status
                coupon.discount_rate = var14
                coupon.save()
                try:
                    log_activity(request,user_id,"update coupon")
                except Exception as e:
                    return render(request , "connection_error.html")        
                messages.info(request, f'{var1} have been Updated')
                return redirect('superadminapp:Coupon_Management')
                # return redirect('/coupon_management/')
            except coupon.DoesNotExist:
                return render(request, 'result.html', {'message': 'Coupon not found'})
        else:
            return render(request, 'result.html', {'message': 'Invalid request method'})
    else:
        return redirect('superadminapp:login')     

def setting(request):
    user_id = request.session.get('userid')
    if user_id:
        # try:
        #     user = Users.objects.get(id=user_id)
        #     userimage = user.image
        # except ObjectDoesNotExist:
        #     # Handle the case when the user does not exist.
        #     user = None
        #     userimage = None
        # user = Users.objects.get(id=user_id)
        # userimage = user.image
        
        stg_tab = GeneralSettings.objects.all()
        for i in stg_tab:
            maintenance_mode_web_panel_image = i.maintenance_mode_web_panel_image
            media_path = maintenance_mode_web_panel_image.path if maintenance_mode_web_panel_image else None
            maintenance_mode_web_panel_image_file_exists = os.path.exists(media_path) if media_path else False
            
            web_panel_header_logo = i.web_panel_header_logo
            media_path = web_panel_header_logo.path if web_panel_header_logo else None
            web_panel_header_logo_file_exists = os.path.exists(media_path) if media_path else False

            login_page_logo = i.login_page_logo
            media_path = login_page_logo.path if login_page_logo else None
            login_page_logo_file_exists = os.path.exists(media_path) if media_path else False
            
            web_panel_header_logo_arabic = i.login_page_logo_arabic
            media_path = web_panel_header_logo_arabic.path if web_panel_header_logo_arabic else None
            web_panel_header_logo_arabic_file_exists = os.path.exists(media_path) if media_path else False

            login_page_logo_arabic = i.login_page_logo_arabic
            media_path = login_page_logo_arabic.path if login_page_logo_arabic else None
            login_page_logo_arabic_file_exists = os.path.exists(media_path) if media_path else False


            enable = ''
            if i.maintenance_enable == True:
                enable = "Active"
            else:
                enable = "Inactive" 
                    
            i_app_update = ''
            if i.iphone_application_update == True:
                i_app_update = "Active"
            else:
                i_app_update = "Inactive"  
            # print(i_app_update)
            i_app_update = ''
            if i.iphone_application_update == True:
                i_app_update = "Active"
            else:
                i_app_update = "Inactive"  
            # print(i_app_update)
            
            a_app_update = ''
            if i.iphone_application_update == True:
                a_app_update = "Active"
            else:
                a_app_update = "Inactive"     
        
        knettable = PaymentMethod.objects.filter(id=1)
        cdctable = PaymentMethod.objects.filter(id=2)
        gptable = PaymentMethod.objects.filter(id=3)
        aptable = PaymentMethod.objects.filter(id=4)
            
        context = {"stg_tab":stg_tab,"enable":enable,"i_app_update":i_app_update,"a_app_update":a_app_update,
                   "maintenance_mode_web_panel_image_file_exists":maintenance_mode_web_panel_image_file_exists,
                   "web_panel_header_logo_file_exists":web_panel_header_logo_file_exists,
                   "login_page_logo_file_exists":login_page_logo_file_exists,
                   "login_page_logo_arabic_file_exists":login_page_logo_arabic_file_exists,
                   "web_panel_header_logo_arabic_file_exists":web_panel_header_logo_arabic_file_exists,
                #    "userimage":userimage,
                   "knettable":knettable,"cdctable":cdctable,"gptable":gptable,"aptable":aptable}
        return render(request, "settings.html",context)
    else:
        return redirect('superadminapp:login')
    
def maintenance_mode_setting(request):
    user_id = request.session.get('userid')
    if user_id:
        
        maintenance_mode = GeneralSettings.objects.all()
        for img in maintenance_mode:
            images =img.maintenance_mode_web_panel_image
        
        if request.method == "POST":
            me  = request.POST['enable']
            if me == "Active":
                me = True
            else:
                me = "False"     
            iu = bool(request.POST.get('induser', False))
            bu = bool(request.POST.get('busiuser', False))
            ba = bool(request.POST.get('busadmin', False))
            # image  = request.POST['imageInput']
            image = request.FILES.get('mmwpiimageInput')
            if image == None:
                image = images
           
            mt  = request.POST['miantitle']
            mc  = request.POST['mainconte']
            
            
            # GeneralSettings.objects.filter(id=1).update(
            #     maintenance_enable=me,
            #     individual_user=iu,
            #     business_user=bu,
            #     business_admin=ba,
            #     maintenance_mode_web_panel_image=image_path,
            #     maintenance_page_title=mt,
            #     maintenance_page_contain=mc,
            # )
            try:        
                generalsettings = GeneralSettings.objects.get(id=1)
                generalsettings.maintenance_enable = me
                generalsettings.individual_user = iu  
                generalsettings.business_user = bu
                generalsettings.business_admin = ba
                generalsettings.maintenance_mode_web_panel_image = image
                generalsettings.maintenance_page_title = mt
                generalsettings.maintenance_page_contain = mc
                generalsettings.save()
                messages.info(request,"Maintenance Mode updated")
            except Exception as e:
                return HttpResponse(f'<h3>Error Maintenance Mode: {e} </h3>')
        return redirect('superadminapp:Setting')
    else:
        return redirect('superadminapp:login')

def application_setting(request):
    user_id = request.session.get('userid')
    if user_id:
        app_stg = GeneralSettings.objects.all()
        if request.method == "POST":
            psaep  = request.POST['psaep']
            ppseaep  = request.POST['ppseaep']
            tsaep  = request.POST['tsaep']
            app_update  = request.POST['app_update']
            if app_update == "Active":
                app_update = True
            else:
                app_update = "False"
            # print(app_update)
            ium  = request.POST['ium']
            if ium == "YES":
                ium = "True"
            else:
                ium = "False"
            # print("__________________________________________________")
            # print(ium)
            # print("__________________________________________________")
            icv  = request.POST['icv']
            inv  = request.POST['inv']
            
            amas  = request.POST['amas']
            if amas == "Active":
                amas = True
            else:
                amas = "False"
           
            aum  = request.POST['aum']
            if aum == "YES":
                aum = "True"
            else:
                aum = "False"
            # print("__________________________________________________")
            # print(aum)
            # print("__________________________________________________")
            acv  = request.POST['acv']
            anv  = request.POST['anv']
     
            # GeneralSettings.objects.filter(id=1).update(
            #     production_server_API_end_point=psaep,
            #     pre_production_server_API_end_point=ppseaep,
            #     test_server_API_end_point=tsaep,
            #     iphone_application_update=app_update,
            #     iphone_update_mandatory=ium,
            #     iphone_current_version=icv,
            #     iphone_new_version=inv,
            #     android_application_update=amas,
            #     android_update_mandatory=aum,
            #     android_current_version=acv,
            #     android_new_version=anv,
            # )
            try:    
                generalsettings = GeneralSettings.objects.get(id=1)
                generalsettings.production_server_API_end_point = psaep
                generalsettings.pre_production_server_API_end_point = ppseaep  
                generalsettings.test_server_API_end_point = tsaep
                generalsettings.iphone_application_update = app_update
                generalsettings.iphone_update_mandatory = ium
                generalsettings.iphone_current_version = icv
                generalsettings.iphone_new_version = inv
                generalsettings.android_application_update = amas
                generalsettings.android_update_mandatory = aum
                generalsettings.android_current_version = acv
                generalsettings.android_new_version = anv
                generalsettings.save()
                messages.info(request,"Application Setting updated")
            except Exception as e:
                return HttpResponse(f'<h3>Error Application Setting: {e} </h3>')
    
        return redirect('superadminapp:Setting')
    else:
        return redirect('superadminapp:login')
    
def company_setting_setting(request):
    user_id = request.session.get('userid')
    if user_id:
        maintenance_mode = GeneralSettings.objects.all()
        for img in maintenance_mode:
            wphlogo =img.web_panel_header_logo
            wphlogo1 =img.web_panel_header_logo_arabic
            lplogo =img.login_page_logo
            lplogo1 =img.login_page_logo_arabic
        if request.method == "POST":
            wphlimage = request.FILES.get('new_imageInput1')
            if wphlimage == None:
                wphlimage = wphlogo
            wphlimage1 = request.FILES.get('new_imageInput13')
            if wphlimage1 == None:
                wphlimage1 = wphlogo1
            # if wphlimage:
            #     image_path1 = "tothiq_pic/" + str(wphlimage)
            # else:
            #     image_path1 = wphlogo
            lplogoimage = request.FILES.get('new_imageInput2')
            if lplogoimage == None:
                lplogoimage = lplogo
            lplogoimage1 = request.FILES.get('new_imageInput23')
            if lplogoimage1 == None:
                lplogoimage1 = lplogo1
            # if lplogoimage:
            #     image_path2 = "tothiq_pic/" + str(lplogoimage)
            # else:
            #     image_path2 = lplogo
            wpt  = request.POST['wpt']
            wpcr  = request.POST['wpcr']
            # GeneralSettings.objects.filter(id=1).update(
            #     web_panel_header_logo=image_path1,
            #     login_page_logo=image_path2,
            #     webpanel_title_text=wpt,
            #     webPanel_copyright_text=wpcr,
            # )
            try:
                generalsettings = GeneralSettings.objects.get(id=1)
                generalsettings.web_panel_header_logo = wphlimage
                generalsettings.web_panel_header_logo_arabic = wphlimage1
                generalsettings.login_page_logo = lplogoimage  
                generalsettings.login_page_logo_arabic = lplogoimage1  
                generalsettings.webpanel_title_text = wpt
                generalsettings.webPanel_copyright_text = wpcr
                generalsettings.save()
                messages.info(request,"Company Setting updated")
            except Exception as e:
                return HttpResponse(f'<h3>Error Company Setting: {e} </h3>')
        return redirect('superadminapp:Setting')
    else:
        return redirect('superadminapp:login')
    
def my_fatoorah_payment_gateway_setting(request):
    user_id = request.session.get('userid')
    if user_id:
      
        if request.method == "POST":
            ptmmf = request.POST.get('payment_test_mode_myfatoorah', 'False')  
            mfau  = request.POST['mfau']
            mfak  = request.POST['mfak']
            try:
                generalsettings = GeneralSettings.objects.get(id=1)
                generalsettings.payment_test_mode = ptmmf
                generalsettings.myfatoorah_api_url = mfau
                generalsettings.myfatoorah_api_url_key = mfak
                generalsettings.save()
                messages.info(request,"Payment Gateway Setting updated")
            except Exception as e:
                return HttpResponse(f'<h3>Error Payment Gateway Setting: {e} </h3>')
        return redirect('superadminapp:Setting')
    else:
        return redirect('superadminapp:login')
    
def smtp_fcm_setting(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":
            smtp_hostname  = request.POST['smtp-hostname']
            smtp_port  = request.POST['smtp-port']
            smtp_username  = request.POST['smtp-username']
            smtp_password  = request.POST['smtp-password']
            sender_email  = request.POST['sender-email']
            fcm_server_key  = request.POST['fcm-server-key']
            security_type = request.POST.get('security_type')
            # print(security_type,"=======")
            try:
                generalsettings = GeneralSettings.objects.get(id=1)
                generalsettings.smtp_host_name = smtp_hostname
                generalsettings.smtp_port = smtp_port
                generalsettings.smtp_username = smtp_username
                generalsettings.smtp_password = smtp_password
                generalsettings.smtp_sender_email = sender_email
                generalsettings.smtp_security = security_type
                generalsettings.fcm_server_key = fcm_server_key
                generalsettings.save()
            except Exception as e:
                return HttpResponse(f'<h3>Error SMTP Or FCM Setting: {e} </h3>')
            messages.info(request,"SMTP Or FCM Setting updated")
        return redirect('superadminapp:Setting')
    else:
        return redirect('superadminapp:login')  

def paci_authantication(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":
            paci_recalltime = request.POST["pacirecall_time"]
            paci_expiretime = request.POST["paci_expiretime"]
            print(paci_expiretime)
            print(paci_recalltime)
            try:
                generalsettings = GeneralSettings.objects.get(id=1)
                generalsettings.paci_recall_time   = paci_recalltime
                generalsettings.paci_expire_time = paci_expiretime
                generalsettings.save()
                messages.info(request,"Paci Authantiocations updated")
            except Exception as e:
                return HttpResponse (f'<h3>Error Paci Authantiocations: {e} </h3>')
        return redirect('superadminapp:Setting')
    else:
        return redirect('superadminapp:login')  
    
def contract_user_price_setting(request):
    user_id = request.session.get('userid')
    if user_id:
      
        if request.method == "POST":
            user_price  = request.POST['user-price']
            contract_price  = request.POST['contract-price']
            
            generalsettings = GeneralSettings.objects.get(id=1)
            generalsettings.users_price = user_price
            generalsettings.contracts_price = contract_price
            generalsettings.save()
            messages.info(request,"Payment Gateway Setting updated")
        return redirect('superadminapp:Setting')
    else:
        return redirect('superadminapp:login')

def payment_gateway_setting(request):
    user_id = request.session.get('userid')
    if user_id:
      
                
        if request.method == "POST":
            ps = request.POST.get('knetstatus')
            if ps == 'true':
                ps = True
            else:
                ps = False

            kti = request.POST['knet_transportalid']
            ktp  = request.POST['knet_transportalpass']
            ktk  = request.POST['knet_trk']
            ktm = request.POST.get('knet_test_mode')
            if ktm == 'true':
                ktm = True
            else:
                ktm = False
                
                
            cdcs = request.POST.get('cdcstatus')
            if cdcs == 'true':
                cdcs = True
            else:
                cdcs = False
            cdcti = request.POST['cdcp_transportalid']
            cdctp  = request.POST['cdcp_transportalpass']
            cdctk  = request.POST['cdcp_trk']
            cdctm = request.POST.get('cdcp_test_mode')
            if cdctm == 'true':
                cdctm = True
            else:
                cdctm = False
                
            gpps = request.POST.get('gppstatus')
            if gpps == 'true':
                gpps = True
            else:
                gpps = False
            gppti = request.POST['gpp_transportalid']
            gpptp  = request.POST['gpp_transportalpass']
            gpptk  = request.POST['gpp_trk']
            gpptm = request.POST.get('gpp_test_mode')
            if gpptm == 'true':
                gpptm = True
            else:
                gpptm = False
                
            apps = request.POST.get('appstatus')
            if apps == 'true':
                apps = True
            else:
                apps = False
            appti = request.POST['app_transportalid']
            apptp  = request.POST['app_transportalpass']
            apptk  = request.POST['app_trk']
            apptm = request.POST.get('app_test_mode')
            if apptm == 'true':
                apptm = True
            else:
                apptm = False

           
            PaymentMethod.objects.filter(id=1).update(
                payment_status=ps,
                payment_transportal_id=kti,
                payment_transportal_password=ktp,
                payment_terminal_resource_key=ktk,
                payment_test_mode=ktm,
            )
            
            PaymentMethod.objects.filter(id=2).update(
                payment_status=cdcs,
                payment_transportal_id=cdcti,
                payment_transportal_password=cdctp,
                payment_terminal_resource_key=cdctk,
                payment_test_mode=cdctm,
            )
            
            PaymentMethod.objects.filter(id=3).update(
                payment_status=gpps,
                payment_transportal_id=gppti,
                payment_transportal_password=gpptp,
                payment_terminal_resource_key=gpptk,
                payment_test_mode=gpptm,
            )
            
            PaymentMethod.objects.filter(id=4).update(
                payment_status=apps,
                payment_transportal_id=appti,
                payment_transportal_password=apptp,
                payment_terminal_resource_key=apptk,
                payment_test_mode=apptm,
            )
            messages.info(request,"Payment Gateway updated")
        return redirect('superadminapp:Setting')
    else:
        return redirect('superadminapp:login')

def user_report(request):
    user_id = request.session.get('userid')
    if user_id:
       
        created_contract =[]
        remainig_contract =[]
        user = Users.objects.all().order_by('pk')
        indivisual = Users.objects.filter(Q(user_type="Individual User") or Q(user_type="individual_user") ).count()
        bus = Users.objects.filter(Q(user_type="Business User") or Q(user_type="business_user") ).count()
        admin = Users.objects.filter(Q(user_type="Business Admin") or Q(user_type="business_admin") ).count()
        userly_count= defaultdict(lambda: {'total_contract': 0, 'user': 0,'total_additional_contracts':0,'total_utilization_contracts':0})
        for i in user:
            user_id=i.id
            userly_count[user_id]['user'] = i.id
            usercontract_count = contracts.objects.filter(user_id=i.id).count()
            created_contract.append(usercontract_count)
            total = contract_histroy.objects.values('user_id').annotate(count=Sum('contracts')).order_by('user_id').filter(user_id=i.id)
            for t in total:
                user_id=t['user_id']
                userly_count[user_id]['total_contract'] = t['count']
                # print(userly_count)
        for i, (month, data) in enumerate(userly_count.items()):
            # print(month,":",data['total_contract'],created_contract[i],data['total_contract'] - created_contract[i])
            remainig_contract.append(data['total_contract'] - created_contract[i])
        
        while len(remainig_contract) < len(user):
            remainig_contract.append(0)
        
        while len(created_contract) < len(user):
            created_contract.append(0)

        user_with_contracts = zip(user, created_contract,remainig_contract)
              
      
        
        free = Users.objects.filter(Q(membership_type="Free") or Q(membership_type="free") ).count()
        # print(free)
        
        Basic = Users.objects.filter(Q(membership_type="Basic") or Q(membership_type="basic") ).count()
        Premium = Users.objects.filter(Q(membership_type="Premium") or Q(membership_type="premium") ).count()
        Gold = Users.objects.filter(Q(membership_type="Gold") or Q(membership_type="gold") ).count()
        Platinum = Users.objects.filter(Q(membership_type="Platinum") or Q(membership_type="platinum") ).count()
        # print(Basic,Premium,Gold,Platinum)
        return render(request, "report.html",{
                                            # "userimage":userimage,
                                            "user_with_contracts": user_with_contracts,
                                             "usercontract":created_contract,
                                             
                                              "individual":indivisual,"bus":bus,"admin":admin,"free":free,"Basic":Basic,"Premium":Premium,"Gold":Gold,"Platinum":Platinum})
    else:
        return redirect('superadminapp:login')
    
def finance_reports(request):
    user_id = request.session.get('userid')
    if user_id:
        # try:
        #     user = Users.objects.get(id=user_id)
        #     userimage = user.image
        # except ObjectDoesNotExist:
        #     # Handle the case when the user does not exist.
        #     user = None
        #     userimage = None
        # user = Users.objects.get(id=user_id)
        # userimage = user.image
        f_reports = Payment.objects.all().order_by('-pk')
        c_reports = Payment.objects.filter(payment_type="contracts")
        u_reports = Payment.objects.filter(payment_type="users")
        b_m_reports = Payment.objects.filter(Q(payment_type="membership") & (Q(membership="2") | Q(membership="5")))
        p_m_reports = Payment.objects.filter(Q(payment_type="membership") & (Q(membership="3") | Q(membership="6")))
        total_dis = Decimal(0)
        total_net = Decimal(0)
        basic_net = Decimal(0)
        basic_dis = Decimal(0)
        premium_net = Decimal(0)
        premium_dis = Decimal(0)
        contracts_net = Decimal(0)
        contracts_dis = Decimal(0)
        users_net = Decimal(0)
        users_dis = Decimal(0)
        for i in f_reports:
            if i.discount_amount is not None:
                total_dis += i.discount_amount
            if i.net_amount is not None:
                total_net += i.net_amount

        for j in b_m_reports:
            if j.discount_amount is not None:
                basic_dis += j.discount_amount
            if j.net_amount is not None:
                basic_net += j.net_amount

        for k in p_m_reports:
            if k.discount_amount is not None:
                premium_dis += k.discount_amount
            if k.net_amount is not None:
                premium_net += k.net_amount

        for l in c_reports:
            if l.discount_amount is not None:
                contracts_dis += l.discount_amount
            if l.net_amount is not None:
                contracts_net += l.net_amount

        for m in u_reports:
            if m.discount_amount is not None:
                users_dis += m.discount_amount
            if m.net_amount is not None:
                users_net += m.net_amount

        # print(users_net)
        # print(users_dis)
        return render(request, "finance_reports.html",{'f_reports':f_reports,'contracts_net':contracts_net,'contracts_dis':contracts_dis,'total_dis':total_dis,'total_net':total_net,'users_net':users_net,'users_dis':users_dis,'basic_net':basic_net,'basic_dis':basic_dis,'premium_net':premium_net,'premium_dis':premium_dis})
    else:
        return redirect('superadminapp:login')    

def general_notifications(request):
    user_id = request.session.get('userid')
    if user_id:
        user = Users.objects.all().order_by('pk')
        subuser = tothiq_super_user.objects.all().order_by('pk')
       
        notificatios = GeneralNotification.objects.all().order_by('-pk')
  
        userid = request.GET.get('user_id')
        global abd
        abd = userid
        if userid is not None:
            # print(userid)
            not_data = GeneralNotification.objects.get(id=userid)
            # if not_data.push_status == "pending" :
            if not_data.push_status == "pending" or not_data.push_status == "in-progress":
                not_data.push_status = "cancel"
                not_data.updated_at = timezone.now() 
                # print("updated... ")
                not_data.save()
        return render(request, "general_notifications.html",{'user':user,'subuser':subuser,'notificatios':notificatios})
    else:
        return redirect('superadminapp:login')
    
def create_general_notifications(request):
    user_id = request.session.get('userid')
    if user_id:
        try:
            if request.method=="POST":
                title = request.POST['notifications_title'] 
                title_arabic = request.POST['notifications_title_arabic'] 
                message = request.POST['notifications_message'] 
                message_arabic = request.POST['notifications_message_arabic'] 
                image = request.FILES.get('notificationimage')
                usertype = request.POST['notification_for_user'] 
                selecteduser = request.POST.getlist('selected_user')
                selected_user_integers = list(set([int(user_id) for user_id in selecteduser]))
                datetime = request.POST['datetime'] 
                Notification_Type = request.POST['Notification_Type']
                
                notifications = GeneralNotification(
                title=title,
                title_arabic=title_arabic,
                message= message,
                message_arabic=message_arabic,
                image =image,
                user_type = usertype,
                user_ids = selected_user_integers,
                schedule_datetime = datetime,
                push_status = "pending",
                notifications_type = Notification_Type,
                created_at =  timezone.now()  
                )
                
                notifications.save()
                created_notification_id = notifications.id
                
                # print(created_notification_id,"--------------------------------")
                
                # if Notification_Type == 'Both':
                #     print(Notification_Type)
                #     push_notification(request,title,message)
                #     send_email(title,message,selected_user_integers,usertype)
                # elif Notification_Type == 'Email':
                #     print(Notification_Type)
                #     send_email(title,message,selected_user_integers,usertype)
                # elif Notification_Type == 'Both':
                #     print(Notification_Type)
                #     push_notification(request,title,message)
                
                # print(selected_user_integers,"--------------------------------")
                
                
                if not selected_user_integers:
                    users = Users.objects.all()
                    for user in users:
                        alluser = user.id
                        selected_user_integers.append(alluser)
                # print(selected_user_integers,"--------------------------------")
                if usertype == '1':
                    if 0 in selected_user_integers:
                        users = Users.objects.all()
                        for user in users:
                            alluser = user.id
                            while 0 in selected_user_integers:
                                selected_user_integers.remove(0)
                            selected_user_integers.append(alluser)
                        # print(selected_user_integers)
                    
                elif usertype == '2' :
                    if 0 in selected_user_integers:
                        users = Users.objects.filter(user_type = "Individual User")
                        for user in users:
                            alluser = user.id
                            while 0 in selected_user_integers:
                                selected_user_integers.remove(0)
                            selected_user_integers.append(alluser)
                        # print(selected_user_integers)
            
                elif usertype == '3':
                    if 0 in selected_user_integers:
                        users = Users.objects.filter(user_type = "Business User")
                        for user in users:
                            alluser = user.id
                            while 0 in selected_user_integers:
                                selected_user_integers.remove(0)
                            selected_user_integers.append(alluser)
                        # print(selected_user_integers)
                
                elif usertype == '4':
                    if 0 in selected_user_integers:
                        users = Users.objects.filter(user_type = "Business Admin")
                        for user in users:
                            alluser = user.id
                            while 0 in selected_user_integers:
                                selected_user_integers.remove(0)
                            selected_user_integers.append(alluser)
                        # print(selected_user_integers)
            
                while 0 in selected_user_integers:
                                selected_user_integers.remove(0)
                userseleceted= list(set(selected_user_integers))

                for id in userseleceted:   
                    # print(id)
                    general_notification_instance = GeneralNotification.objects.get(id=created_notification_id)
                
                    user = notification.objects.create(
                        notification_type=None,
                        title=title,
                        title_arabic=title_arabic,
                        description =message,
                        description_arabic =message_arabic,
                        is_active=True,
                        read = False,
                        user_id = id,
                        general_notification_id = general_notification_instance,
                        pin = False,
                        contract = None,
                        created_at= timezone.now()  
                    )
                messages.info(request, 'Notifications have been Created')
                try:
                    log_activity(request,user_id,"create notifications")
                except Exception as e:
                    return render(request , "connection_error.html")
                return redirect('superadminapp:General Notifications')
        except Exception as e:
            return HttpResponse(f'<h3>Error create notification: {e} </h3>')
    else:
        return redirect('superadminapp:login')
    
# def push_notification(request,title,msg):
#     push_service = FCMNotification(api_key="AAAA5LS_Q2E:APA91bEl-inXQwB-OrfEIT0k34patsZwicmujZay4a0lZoopkGEuxDfQp6KCHmP07tOIKzVdJGHPLaAt469F8N9tU4vcV_f8wEizbuUMSmgJ6xXav0RBKa_Hqd_4d1fMCsrtVYly6g6S")

# # Fetch all Users with non-empty firebase_token
#     users_with_tokens = Users.objects.exclude(firebase_token='')
# # Extract firebase_token values and create the registration_ids list
#     registration_ids = [user.firebase_token for user in users_with_tokens]
   
#     message_title = title
    
#     message_body = msg
   

#     result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)


#     # print (result)

 
def push_notification(request, title, msg, selected_user_integers, usertype, scheduled_time, id):
    fcm_server_key=GeneralSettings.objects.get(id=1).fcm_server_key
    push_service = FCMNotification(api_key=fcm_server_key)

    registration_ids = []

    try:
        
        # Update notification status to "in progress" at the beginning
        notification = GeneralNotification.objects.get(id=id)
        notification.push_status = "in progress"
        notification.save()
        
        users = GeneralNotification.objects.get(id=id)
        user_ids = ast.literal_eval(users.user_ids)

        for user_id in user_ids:
            if user_id == 0:
                print("Sending to all users")
                if usertype == '1':
                    users_to_notify = Users.objects.all()
                elif usertype == '2':
                    users_to_notify = Users.objects.filter(user_type='Individual User').order_by('pk')
                elif usertype == '3':
                    users_to_notify = Users.objects.filter(user_type='Business User').order_by('pk')
                elif usertype == '4':
                    users_to_notify = Users.objects.filter(user_type='Business User').order_by('pk')

                for user in users_to_notify:
                    user_tokens = user_firebase_token.objects.filter(user_id=user.id)
                    registration_ids.extend([token.firebase_token for token in user_tokens])
            else:
                user_tokens = user_firebase_token.objects.filter(user_id=user_id)
                registration_ids.extend([token.firebase_token for token in user_tokens])

        print(registration_ids)
        message_title = title
        message_body = msg

        extra_kwargs = {
            "data": {
                "type": "general"
            }
        }

        result = push_service.notify_multiple_devices(
            registration_ids=registration_ids,
            message_body=message_body,
            message_title=message_title,
            extra_kwargs=extra_kwargs
        )

        print(result)
        # Update notification status to "send" after sending notifications
        notification.push_status = "send"
        notification.save()

    except Exception as e:
        # Handle other exceptions that might occur
        # You can log the error, return a specific HTTP response, or take other actions as needed
        print(f"An error occurred: {e}")


    # print (result)

    
# def send_email(subject, body,selected_user_integers,usertype):
#     # users_with_email = Users.objects.exclude(firebase_token='')
#     # to_emails =[user.firebase_token for user in users_with_email]
#     to_emails = []
#     for i in selected_user_integers:
#         if usertype == '5':
#                 if i == 0:
#                     user = tothiq_super_user.objects.all()
#                     for u in user:
#                         if u.email:
#                             to_emails.append(u.email)
#                 else:
#                     user = tothiq_super_user.objects.get(id=i)
#                     to_emails.append(user.email)
#         else:
#             if i == 0:
#                 if usertype == '1':
#                     user = Users.objects.all()
#                 elif usertype == '2':
#                     user = Users.objects.filter(user_type='Individual User').order_by('pk')
#                 elif usertype == '3':
#                     user = Users.objects.filter(user_type='Business User').order_by('pk')
#                 elif usertype == '4':
#                     user = Users.objects.filter(user_type='Business User').order_by('pk')
                    
#                 for k in user:
#                     if k.email:
#                         to_emails.append(k.email)
#             else:
#                 user = Users.objects.get(id=i)
#                 to_emails.append(user.email)
                    
                
#     msg = MIMEMultipart()
#     msg['From'] = 'bhagydetroja.e19@gpahmedabad.ac.in'
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))
#     def send_email_to_recipient(to_email):
        
#         try:
#             server = smtplib.SMTP('smtp.gmail.com', 587)
#             server.starttls()
#             server.login('bhagydetroja.e19@gpahmedabad.ac.in', 'Detroja@227')
#             server.sendmail('bhagydetroja.e19@gpahmedabad.ac.in', to_email, msg.as_string())
#             server.quit()
#             # print(f"Email sent successfully to {to_email}!")
#         except Exception as e: 
#             print(f"Error sending email to {to_email}: {str(e)}")
#     with ThreadPoolExecutor() as executor:
#         executor.map(send_email_to_recipient, to_emails)


  
def send_email(subject, body, selected_user_integers, usertype, scheduled_time, id):
    try:
        # Update notification status to "in progress"
        notification = GeneralNotification.objects.get(id=id)
        notification.push_status = "in progress"
        notification.save()

        # Check if it's time to send the email
        current_time = datetime.now()
        if current_time >= scheduled_time:
            # Prepare the email
            to_emails = []  # List of recipient email addresses

            # Populate to_emails based on your logic
            # ...
            for i in ast.literal_eval(selected_user_integers):
                if usertype == '5':
                        if i == 0:
                            user = tothiq_super_user.objects.all()
                            for u in user:
                                if u.email:
                                    to_emails.append(u.email)
                        else:
                            user = tothiq_super_user.objects.get(id=i)
                            to_emails.append(user.email)
                else:
                    if i == 0:
                        if usertype == '1':
                            user = Users.objects.all()
                        elif usertype == '2':
                            user = Users.objects.filter(user_type='Individual User').order_by('pk')
                        elif usertype == '3':
                            user = Users.objects.filter(user_type='Business User').order_by('pk')
                        elif usertype == '4':
                            user = Users.objects.filter(user_type='Business User').order_by('pk')
                            
                        for k in user:
                            if k.email:
                                to_emails.append(k.email)
                    else:
                        user = Users.objects.get(id=i)
                        to_emails.append(user.email)
            print(to_emails,"................................................................")
            for to_email in to_emails:
                msg = MIMEMultipart()
                msg['From'] = 'bhagydetroja.e19@gpahmedabad.ac.in'
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login('bhagydetroja.e19@gpahmedabad.ac.in', 'Detroja@227')
                    server.sendmail('bhagydetroja.e19@gpahmedabad.ac.in', to_email, msg.as_string())
                    print(f"Email sent successfully to {to_email}!")

            # Update notification status to "send"
            notification.push_status = "send"
            notification.save()
    except Exception as e:
        # Handle exceptions and log the error
        print(f"Error: {str(e)}")

        
# def update_general_notifications(request):
#     user_id = request.session.get('userid')
#     if user_id:
        
#         if request.method == 'POST':
#             id = request.POST.get('nid')
#             title = request.POST.get('notifications_title')
#             title_arabic = request.POST['notifications_title_arabic'] 
#             message = request.POST.get('notifications_message')
#             message_arabic = request.POST['notifications_message_arabic'] 
#             notimage = request.FILES.get('notimageInput')
#             if notimage==None:
#                 nottab = GeneralNotification.objects.get(id=id)
#                 notimage = nottab.image
#             usertype = request.POST.get('notification_for_user')
#             userids = request.POST.getlist('selected_user')
#             selected_user_integers = list(set([int(user_id) for user_id in userids]))
#             notifications_type = request.POST.get('notification_type')
#             datetime = request.POST.get('datetime')
#             try:
#                 genral_not= GeneralNotification.objects.get(id=id)
#                 genral_not.title = title
#                 genral_not.title_arabic = title_arabic
#                 genral_not.message_arabic = message_arabic
#                 genral_not.message = message
#                 genral_not.image = notimage
#                 genral_not.user_type = usertype
#                 genral_not.user_ids = selected_user_integers
#                 genral_not.notifications_type = notifications_type
#                 genral_not.schedule_datetime = datetime
#                 genral_not.updated_at = timezone.now()  
#                 genral_not.save()
#                 try:
#                     log_activity(request,user_id,"update notification")
#                 except Exception as e:
#                     return render(request , "connection_error.html")
                        
#             except genral_not.DoesNotExist:
#                 return render(request, 'result.html', {'message': 'Coupon not found'})
       
          
#             messages.info(request, 'Notifications have been Updated')
#             return redirect('superadminapp:General Notifications')

#     else:
#         return redirect('superadminapp:login')

   
def update_general_notifications(request):
    user_id = request.session.get('userid')
    if user_id:
        
        if request.method == 'POST':
            id = request.POST.get('nid')
            title = request.POST.get('notifications_title')
            title_arabic = request.POST['notifications_title_arabic'] 
            message = request.POST.get('notifications_message')
            message_arabic = request.POST['notifications_message_arabic'] 
            notimage = request.FILES.get('notimageInput')
            if notimage==None:
                nottab = GeneralNotification.objects.get(id=id)
                notimage = nottab.image
            usertype = request.POST.get('notification_for_user')
            userids = request.POST.getlist('selected_user')
            selected_user_integers = list(set([int(user_id) for user_id in userids]))
            notifications_type = request.POST.get('notification_type')
            datetime = request.POST.get('datetime')
            try:
                genral_not= GeneralNotification.objects.get(id=id)
                genral_not.title = title
                genral_not.title_arabic = title_arabic
                genral_not.message_arabic = message_arabic
                genral_not.message = message
                genral_not.image = notimage
                genral_not.user_type = usertype
                genral_not.user_ids = selected_user_integers
                genral_not.push_type = notifications_type.lower()
                genral_not.schedule_datetime = datetime
                genral_not.updated_at = timezone.now()  
                genral_not.save()
                try:
                    log_activity(request,user_id,"update notification")
                except Exception as e:
                    return render(request , "connection_error.html")
                        
            except genral_not.DoesNotExist:
                return render(request, 'result.html', {'message': 'Coupon not found'})
       
          
            messages.info(request, 'Notifications have been Updated')
            return redirect('superadminapp:General Notifications')

    else:
        return redirect('superadminapp:login')


def tothiq_admin_user(request):
    user_id = request.session.get('userid')
    if user_id:
        user = tothiq_super_user.objects.get(id=user_id)
        # userimage = user.image
        stng = GeneralSettings.objects.all()
        for i in stng:
            hlg = i.web_panel_header_logo
            wptx = i.webpanel_title_text
            crtx = i.webPanel_copyright_text
        userid = request.GET.get('user_id')
        global abd
        abd = userid
        if userid is not None:
            # print(userid)
            user_data = tothiq_super_user.objects.get(id=userid)
            if user_data.active_status == "inactive":
                user_data.active_status = "active"
                # print("active")
                user_data.save()
            elif user_data.active_status == "active":
                user_data.active_status = "inactive"
                # print("inactive")
                user_data.save()
        data = tothiq_super_user.objects.filter().order_by('-id')
        items_per_page = 15
        paginator = Paginator(data, items_per_page)
        page_number = request.GET.get('page')
        paginated_data = paginator.get_page(page_number)
        context = {'data': data,"hlg":hlg,"wptx":wptx,
                #    "userimage":userimage,
                   "crtx":crtx}
        return render(request, "tothiq_user.html", context)
    else:
        return redirect('superadminapp:login')

def creat_tothiq_user(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":
            name = request.POST['name']
            Number = request.POST['Number']
            email = request.POST['email']
            current_time =timezone.now()
            print(current_time)
            
            # create_template = request.POST.get('create_template')  # A
            # if create_template == "true":
            #     A = True
            # else:
            #     A = False
            # edit_tempalte = request.POST.get('edit_tempalte')  # B
            # if edit_tempalte == "true":
            #     B = True
            # else:
            #     B = False
            # assign_custom_package = request.POST.get('assign_custom_package')  # C
            # if assign_custom_package == "true":
            #     C = True
            # else:
            #     C = False
            # activate_block_business_users = request.POST.get(
            #     'activate_block_business_users')  # D
            # if activate_block_business_users == "true":
            #     D = True
            # else:
            #     D = False
            # print(A, B, C, D)
            if 'Create' in request.POST:
                creat = tothiq_super_user.objects.create(
                    full_name=name,
                    phone_number=Number,
                    email=email,
                    # create_template=A,
                    # edit_tempalte=B,
                    # assign_custom_package=C,
                    # activate_block_business_users=D,
                    active_status="inactive",
                    created_at= current_time
                    # is_superuser=True
                )
                messages.info(request,"Super Admin Users have been Created")
        
            elif 'Create & Send' in request.POST:
                try:
                    password = ''.join(random.choice('0123456789') for _ in range(6))
                    subject = "Invitstion of tothiq super admin "
                    body = f"Welcome! You are added as a Tothiq-User\n\nPassword is: {password}"
                    recipient_email = email
                    
                    send_email_test(subject, body, recipient_email)


                    # send_mail(
                    #         subject,
                    #         message,
                    #         EMAIL_HOST_USER,
                    #         [recipient],
                    #         fail_silently=False,
                    #     )
                    new = make_password(password)
                    # print(new)
                    creatsuperuser = tothiq_super_user.objects.create(
                                full_name=name,
                                phone_number=Number,
                                email=email,
                                password=new,
                                # create_template=A,
                                # edit_tempalte=B,
                                # assign_custom_package=C,
                                # activate_block_business_users=D,
                                active_status="active",
                                created_at= current_time
                                # is_superuser=True
                            )
                    # Return a success response
                    messages.info(request, "Super Admin User has been Created and Email Sent")
                    return redirect('superadminapp:Tothiq_User')
                except Exception as e:
                    # Return an error response
                    return HttpResponse(f'<h3>Error sending email: {e}</h3>')
            return redirect('superadminapp:Tothiq_User')
    else:
        return redirect('superadminapp:login')
    
def validate_Email_super_user(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == 'POST':
            data = request.body.decode('utf-8')
            entered_email = json.loads(data).get('emailin')
            email1 = tothiq_super_user.objects.filter(email=entered_email)
            if email1:
                is_valid = False
            else:
                is_valid = True
            # Perform password validation using Django's check_password function
            return JsonResponse({'is_valid': is_valid})
    else:
        return redirect('superadminapp:login')
    
def verify_email(request, slug):
    user_id = request.session.get('userid')
    if user_id:
        my_object = Users.objects.get(full_name=slug)
        my_object.active_status = "active"
        my_object.save()
        messages.info(request, 'Ativeted successfully.')

        return redirect('/home/')
    else:
        return redirect('superadminapp:login')

def update_tothiq_user(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":
            update_user_id = request.POST['id']
            name = request.POST['name']
            Number = request.POST['Number']
            email = request.POST['email']
            current_time =timezone.now()
            # create_template = request.POST.get('create_template')  # A
            # if create_template == "true":
            #     A = True
            # else:
            #     A = False
            # edit_tempalte = request.POST.get('edit_tempalte')  # B
            # if edit_tempalte == "true":
            #     B = True
            # else:
            #     B = False
            # assign_custom_package = request.POST.get('assign_custom_package')  # C
            # if assign_custom_package == "true":
            #     C = True
            # else:
            #     C = False
            # activate_block_business_users = request.POST.get(
            #     'activate_block_business_users')  # D
            # if activate_block_business_users == "true":
            #     D = True
            # else:
            #     D = False
            try:
                my_object = tothiq_super_user.objects.get(id=update_user_id)
                my_object.full_name = name
                my_object.phone_number = Number
                my_object.email = email
                my_object.updated_at = current_time
                # my_object.create_template = A
                # my_object.edit_tempalte = B
                # my_object.assign_custom_package = C
                # my_object.activate_block_business_users = D
                my_object.save()
                messages.info(request, "Super Admin User has been updated")
                return redirect('superadminapp:Tothiq_User')
            except tothiq_super_user.DoesNotExist:
                # Handle the case where the user with the given ID does not exist
                messages.error(request, "User does not exist")
                return redirect('superadminapp:Tothiq_User')
            except IntegrityError as e:
                if 'supertothiquser_email_key' in str(e):
                    messages.error(request, "Email address is already in use")
                else:
                    messages.error(request, "An error occurred while updating the user")
                return redirect('superadminapp:Tothiq_User')
    else:
        return redirect('superadminapp:login')

def validate_Email_super_user_update(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == 'POST':
            data = request.body.decode('utf-8')
            entered_email = json.loads(data).get('emailinupdate')
            
            email1 = tothiq_super_user.objects.filter(email=entered_email)
            
            if email1:
                is_valid = False
            else:
                is_valid = True
            return JsonResponse({'is_valid': is_valid})
    else:
        return redirect('superadminapp:login')
      
def email_template_setting(request):
    user_id = request.session.get('userid')
    if user_id:
        data = Email_Template.objects.filter().order_by('-id')
        # query = request.GET.get('q')  # Get the search query parameter
        # print(query,"--------------------")
        # if query:
        #     data = data.filter(email_subject__icontains=query)  # Adjust to the field you want to search in
        
        # paginator = Paginator(data, 5)  
        # page = request.GET.get('page')
        # try:
        #     data = paginator.page(page)
        # except PageNotAnInteger:
        #     data = paginator.page(1)
        # except EmptyPage:
        #     data = paginator.page(paginator.num_pages)

        emailid = request.GET.get('user_id')
        delemaiiid = request.GET.get('email_id')
        global abd
        abd = emailid
        if emailid is not None:
            not_data = Email_Template.objects.get(id=emailid)
            if not_data.active_status == "active" :
                not_data.active_status = "inactive"
                not_data.updated_at = timezone.now() 
                not_data.save()
                # print("updated... ")
            elif not_data.active_status == "inactive":
                not_data.active_status = "active"
                not_data.updated_at = timezone.now() 
                not_data.save()
                # print("updated... ")
        
        return render(request, "emailtemplate.html",{"data":data})
    else:
        return redirect('superadminapp:login')    
    
# def create_email_template_setting(request):
#     user_id = request.session.get('userid')
#     if user_id:
#         if request.method == "POST":
#             ecode = request.POST['email_code']
#             esubject = request.POST['email_subject']
#             earabicsubject = request.POST['email_subject_arabic']
#             econtent = request.POST['email_content']
            
#             emailtemplate = Email_Template(
#             email_code=ecode,
#             email_subject= esubject,
#             email_subject_arabic= earabicsubject,
#             email_content =econtent,
#             active_status = "active",
#             created_at =  timezone.now()  
#             )
#             emailtemplate.save()
#             messages.info(request, 'Email Template Created')
#             return  redirect('superadminapp:Email_Template')

#     else:
#         return redirect('superadminapp:login')  
    
def update_email_template_setting(request,emailtempid):
    user_id = request.session.get('userid')
    if user_id:
        emailtemptab = Email_Template.objects.filter(id=emailtempid)
        try:
            if request.method == "POST":
                
                seid = request.POST.get('eid')
                ecode = request.POST.get('email_code')
                esubject = request.POST.get('email_subject')
                arabicesubject = request.POST.get('email_subject_arabic')
                econtent = request.POST.get('email_content')
                econtent_arabic = request.POST.get('email_content_arabic')
                
                emailtemptab = Email_Template.objects.get(pk=seid)
                emailtemptab.email_code = ecode
                emailtemptab.email_subject = esubject
                emailtemptab.email_subject_arabic = arabicesubject
                emailtemptab.email_content = econtent
                emailtemptab.email_content_arabic = econtent_arabic
                emailtemptab.updated_at =  timezone.now() 
                emailtemptab.save()
                try:
                    log_activity(request,user_id,"update email template")
                except Exception as e:
                    return render(request , "connection_error.html")
                            
                messages.success(request, f"Email template status updated successfully!")
                return redirect('superadminapp:Email_Template')
        except Exception as e:
            return HttpResponse(f'<h3>Error update email template: {e} </h3>')
        context = {
            "data":emailtemptab
            }
            
        return render(request, 'update_email_template.html',context)
    else:
        return redirect('superadminapp:login')
    
def activity_logs(request):
    user_id = request.session.get('userid')
    if user_id:
        data = Activity_logs.objects.all().order_by('-pk')[:5000]
        # paginator = Paginator(data, 15)
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
       
        return render(request, "user_activity_logs.html",{'page_obj':data})
        
    else:
        return redirect('superadminapp:login')
    
def log_activity(request,u_id,type):
    user_name = tothiq_super_user.objects.get(pk=u_id).full_name
    hostname=socket.gethostname()
    ip = socket.gethostbyname(hostname)    #ip
    user_agent =  parse(request.META['HTTP_USER_AGENT'])
    browser_name =  user_agent.browser.family    #bron
    activity_type = type
    creat_at = datetime.now()
    # print(creat_at)
    url = f"https://ipinfo.io/{ip}/json"
    response = requests.get(url)
    data1 = response.json()
    location = data1.get('loc', None)
    location = geocoder.ip('me')
    current_location = location.latlng
    latitude, longitude = current_location      #lat,log
    # print(f"Latitude: {latitude}, Longitude: {longitude}")
    # print("ip Address:",ip)
    log = Activity_logs.objects.create(
                    full_name = user_name,
                    browser_name = browser_name,
                    Ip_address = ip,
                    latitude = latitude,
                    longitude = longitude,
                    activity_Type = activity_type,
                    created_at = creat_at,)
  
def block_unblock_user(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":
            data = request.body.decode('utf-8')
            id = json.loads(data).get('password')
            user = Users.objects.get(pk=id)
            a = user.active_status
            if a == "active":
                users = Users.objects.filter(pk=id).update(active_status="blocked")
                # print(a)
                try:
                    oldemail = Users.objects.filter(id=id)
                    for i in oldemail:
                        oldmail = i.email
                    subject = " Account Block by TOTHIQ."
                    body = 'Your account has been Block by TOTHIQ. If you have any questions or need further assistance, please do not hesitate to reach out.'
                    
                    recipient_email = oldmail
                    send_email_test(subject, body, recipient_email)



                    # send_mail(
                    #         subject,
                    #         message,
                    #         EMAIL_HOST_USER,
                    #         [recipient],
                    #         fail_silently=False,
                    #     )
                    # print("mail is send active")
                except Exception as e:
                    # Return an error response
                    # print("mail is not send active")
                    return HttpResponse(f'<h3>Error sending email: {e}</h3>')
            elif  a == "blocked":
                users = Users.objects.filter(pk=id).update(active_status="active")
                try:
                    oldemail = Users.objects.filter(id=id)
                    for i in oldemail:
                        oldmail = i.email
                    subject = " Account Unblock by TOTHIQ."
                    body = 'Your account has been Unblock by TOTHIQ. If you have any questions or need further assistance, please do not hesitate to reach out.'
                    
                    recipient_email = oldmail

                    send_email_test(subject, body, recipient_email)

                    # send_mail(
                    #         subject,
                    #         message,
                    #         EMAIL_HOST_USER,
                    #         [recipient],
                    #         fail_silently=False,
                    #     )
                except Exception as e:
                    # Return an error response
                    # print("mail is not send active")
                    return HttpResponse(f'<h3>Error sending email: {e}</h3>')
            active = "active"
            return JsonResponse({'active_status':active })
        else:
            return redirect('superadminapp:login')
    
def block_unblock_business(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":
       
            data = request.body.decode('utf-8')
            id = json.loads(data).get('password')
    
            user = Users.objects.get(pk=id)
            a = user.active_status
            # print(a)
            if a == "active" or a == "inactive":
                users = Users.objects.filter(pk=id).update(active_status="blocked")
                # print(a)
                try:
                    oldemail = Users.objects.filter(id=id)
                    for i in oldemail:
                        oldmail = i.email
                    subject = " Account Block by TOTHIQ."
                    body = 'Your account has been Block by TOTHIQ. If you have any questions or need further assistance, please do not hesitate to reach out.'
                    
                    recipient_email = oldmail
                    
                    send_email_test(subject, body, recipient_email)


                    # send_mail(
                    #         subject,
                    #         message,
                    #         EMAIL_HOST_USER,
                    #         [recipient],
                    #         fail_silently=False,
                    #     )
                    # print("mail is send active")
                except Exception as e:
                    # Return an error response
                    # print("mail is not send active")
                    return HttpResponse(f'<h3>Error sending email: {e}</h3>')
            elif  a == "blocked":
                users = Users.objects.filter(pk=id).update(active_status="active")
                # print(a)
                try:
                    oldemail = Users.objects.filter(id=id)
                    for i in oldemail:
                        oldmail = i.email
                    subject = " Account Unblock by TOTHIQ."
                    message = 'Your account has been Unblock by TOTHIQ. If you have any questions or need further assistance, please do not hesitate to reach out.'
                    
                    recipient = oldmail

                    send_mail(
                            subject,
                            message,
                            EMAIL_HOST_USER,
                            [recipient],
                            fail_silently=False,
                        )
                    # print("mail is send active")
                except Exception as e:
                    # Return an error response
                    print("mail is not send active")
                    return HttpResponse(f'<h3>Error sending email: {e}</h3>')
            active = "active"
            return JsonResponse({'active_status':active })
        else:
            return redirect('superadminapp:login')
        
def active_inactive_business(request):
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "POST":
            data = request.body.decode('utf-8')
            id = json.loads(data).get('password')
            # print(id)
            user = Users.objects.get(pk=id)
            a = user.active_status
            # print(a)
            if a == "active":
                users = Users.objects.filter(pk=id).update(active_status="inactive")
                # print(a)
                try:
                    oldemail = Users.objects.filter(id=id)
                    for i in oldemail:
                        oldmail = i.email
                    subject = " Account inactive by TOTHIQ."
                    body = 'Your account has been inactive by TOTHIQ. Please contact TOTHIQ Support at tothiq  for assistance.'
                    
                    recipient_email = oldmail
                    
                    send_email_test(subject, body, recipient_email)


                    # send_mail(
                    #         subject,
                    #         message,
                    #         EMAIL_HOST_USER,
                    #         [recipient],
                    #         fail_silently=False,
                    #     )
                except Exception as e:
                    # Return an error response
                    return HttpResponse(f'<h3>Error sending email: {e}</h3>')
            elif  a == "inactive":
                users = Users.objects.filter(pk=id).update(active_status="active")
                # print(a)
                try:
                    oldemail = Users.objects.filter(id=id)
                    for i in oldemail:
                        oldmail = i.email
                    subject = " Account active by TOTHIQ."
                    body = 'Your account has been active by TOTHIQ. Please contact TOTHIQ Support at tothiq for assistance.'
                    
                    recipient_email = oldmail

                    send_email_test(subject, body, recipient_email)

                    # send_mail(
                    #         subject,
                    #         message,
                    #         EMAIL_HOST_USER,
                    #         [recipient],
                    #         fail_silently=False,
                    #     )
                except Exception as e:
                    # Return an error response
                    return HttpResponse(f'<h3>Error sending email: {e}</h3>')
            active = "active"
            return JsonResponse({'active_status':active })
        else:
            return redirect('superadminapp:login')

def logout(request):
    user_id = request.session.get('userid')
    try:
        log_activity(request,user_id,"logout")
    except Exception as e:
        return render(request , "connection_error.html")
    del request.session['userid']
    # print(request.session.get('userid'))
    return redirect('superadminapp:login')

class BulkEmailSendView(APIView):
    api_view = ['GET', ]

    def get(self, request):
        #step 1 : get pending notification last 10 records max.
        total_notification = GeneralNotification.objects.filter(push_status = "pending").reverse()[:10]
        setting_obj = GeneralSettings.objects.filter(id = "1").last()

        for notification in total_notification:
            if notification.user_type == "0":   # user_type : all 
                notification.push_status = "in-progress"
                if Q(notification.notifications_type =='email') | Q(notification.notifications_type == 'both'):
                    user_ids = notification.user_ids
                    integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))] # extract int from the list of user_ids
                    for user_id in integers_id:
                        user = Users.objects.filter(id = user_id).last()
                        send_mail(
                            notification.title,
                            notification.message,
                            EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=False,
                        )
                elif Q(notification.notifications_type =='push-notification') | Q(notification.notifications_type == 'both'):
                        push_service = FCMNotification(api_key=setting_obj.fcm_server_key)
                        user_ids = notification.user_ids
                        integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))] # extract int from the list of user_ids
                        for user_id in integers_id: # Send to multiple devices by passing a list of ids.
                            user = user_firebase_token.objects.filter(user_id = user_id)
                            for i in user:
                                registration_id = i.firebase_token
                                message_title = notification.title
                                message_body = notification.message
                                result = push_service.notify_single_device(registration_id=registration_id, 
                                                                                message_title=message_title,
                                                                                message_body=message_body)
                notification.push_status = "sent"
                notification.save()

            elif notification.user_type == "1":  # user_type : Individual User 
                notification.push_status = "in-progress"
                if Q(notification.notifications_type == 'email') | Q(notification.notifications_type == 'both'):
                    user_ids = notification.user_ids
                    integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))] # extract int from the list of user_ids
                    for user_id in integers_id:
                        user = Users.objects.filter(id = user_id).last()
                        send_mail(
                            notification.title,
                            notification.message,
                            EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=False,
                        )

                if Q(notification.notifications_type =='push-notification') | Q(notification.notifications_type == 'both'):
                    push_service = FCMNotification(api_key=setting_obj.fcm_server_key)
                    user_ids = notification.user_ids
                    integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))] # extract int from the list of user_ids
                    # print("aaaa", integers_id)
                    for user_id in integers_id:
                            user = user_firebase_token.objects.filter(user_id = user_id)
                            for i in user:
                                registration_id = i.firebase_token
                                message_title = notification.title
                                message_body = notification.message
                                result = push_service.notify_single_device(registration_id=registration_id, 
                                                                                message_title=message_title,
                                                                                message_body=message_body)
                    
                notification.push_status = "sent"
                notification.save()
    

            elif notification.user_type == "2":  # user_type : Business User
                notification.push_status = "in-progress"
                if Q(notification.notifications_type =='email') | Q(notification.notifications_type == 'both'):
                    user_ids = notification.user_ids
                    integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))]
                    for user_id in integers_id:
                        user = Users.objects.filter(id = user_id).last()
                        send_mail(
                            notification.title,
                            notification.message,
                            EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=False,
                        )
                elif Q(notification.notifications_type =='push-notification') | Q(notification.notifications_type == 'both'):
                        push_service = FCMNotification(api_key=setting_obj.fcm_server_key)
                        user_ids = notification.user_ids
                        integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))]
                        for user_id in integers_id:
                            user = user_firebase_token.objects.filter(user_id = user_id)
                            for i in user:
                                registration_id = i.firebase_token
                                message_title = notification.title
                                message_body = notification.message
                                result = push_service.notify_single_device(registration_id=registration_id, 
                                                                                message_title=message_title,
                                                                                message_body=message_body)
                notification.push_status = "sent"
                notification.save()

            elif notification.user_type == "3":  # user_type : Business Admin
                notification.push_status = "in-progress"
                if Q(notification.notifications_type =='email') | Q(notification.notifications_type == 'both'):
                    user_ids = notification.user_ids
                    integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))]
                    for user_id in integers_id:
                        user = Users.objects.filter(id = user_id).last()
                        send_mail(
                            notification.title,
                            notification.message,
                            EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=False,
                        )
                elif Q(notification.notifications_type =='push-notification') | Q(notification.notifications_type == 'both'):
                        push_service = FCMNotification(api_key=setting_obj.fcm_server_key)
                        user_ids = notification.user_ids
                        integers_id = [int(item) for item in user_ids if re.match(r'^-?\d+$', str(item))]
                        for user_id in integers_id:
                            user = user_firebase_token.objects.filter(user_id = user_id)
                            for i in user:
                                registration_id = i.firebase_token
                                message_title = notification.title
                                message_body = notification.message
                                result = push_service.notify_single_device(registration_id=registration_id, 
                                                                                message_title=message_title,
                                                                                message_body=message_body)
                notification.push_status = "sent"
                notification.save()
        return redirect('/home/')
       
def sendmailwithtemplate(template_code, email_code): # send mail with template
    email_template_data = Email_Template.objects.filter(email_code = template_code , active_status = 'active').last() # fetching particular email code
    if email_template_data:
        email_subject  = email_template_data.email_subject
        email_message =  email_template_data.email_content
        new_email_message = email_message.replace("[User's Name]", str(email_code.get('name')))
        email_to = str(email_code.get('email'))
        send_mail(
            email_subject,
            new_email_message,
            EMAIL_HOST_USER,
            [email_to],
            fail_silently=False,
        )
    return True

def sendnotificationwithtemplate(template_code, notification_code): # send notification with template
    try:
        
        notification_template_data = NotificationTemplates.objects.filter(notification_code = template_code, active_status = 'active').last()
        if not notification_template_data:
            return False
        
        setting_obj = GeneralSettings.objects.filter(id = "1").last()
        if not setting_obj or not setting_obj.fcm_server_key:
            return False
        
   
        
        subject = notification_template_data.notification_subject
        content = notification_template_data.notification_content
        new_content = content.replace("[User's Name]", str(notification_code.get('name')))
        registration_id=notification_code.get('id')
        
        push_service = FCMNotification(api_key=setting_obj.fcm_server_key)
        result = push_service.notify_single_device(registration_id=registration_id,
                                                        message_title=subject,
                                                        message_body=new_content)
        return True
    except Exception as e:
            # Handle other exceptions here, such as network issues or unexpected errors
           return HttpResponse(f'<h3>Key Not Found: {e}</h3>')

def sendnotification(notification_code): # send notificatio without template
    setting_obj = GeneralSettings.objects.filter(id = "1").last()
    push_service = FCMNotification(api_key=setting_obj.fcm_server_key)
    registration_ids=notification_code.get('ids')
    result = push_service.notify_multiple_devices(registration_ids=registration_ids,
                                                    message_title=str(notification_code.get('title')),
                                                    message_body=str(notification_code.get('message')))
    return True

def get_notification_template(request): # get method of notification template
    user_id = request.session.get('userid')
    if user_id:
        if request.method == "GET":
            data = NotificationTemplates.objects.all()
            return render(request, 'notification_template.html', {'data': data})
    return redirect('superadminapp:login') 

# def create_notification_template(request): # post method of notification template
#     user_id = request.session.get('userid')
#     if user_id:
#         if request.method == "POST":
#             model = NotificationTemplates()
#             model.notification_code = request.POST['notification_code']
#             model.notification_subject = request.POST['notification_subject']
#             model.notification_subject_arabic = request.POST['notification_subject_arabic']
#             model.notification_content = request.POST['notification_content']
#             model.notification_content_arabic = request.POST['notification_content_arabic']
#             model.active_status = request.POST['active_status']
#             model.updated_at =  timezone.now()
#             model.save()
#             messages.info(request, 'Notification Template Created')
#             return  redirect('superadminapp:notification_template')
#         return render(request, "notification_template.html")
#     else:
#         return redirect('superadminapp:login')

def update_notification_template(request, id): # update method of notification template
    user_id = request.session.get('userid')
    if user_id:
        data = NotificationTemplates.objects.filter(id = id).last()
        if request.method == "POST":
            data.notification_code = request.POST['notification_code']
            data.notification_subject = request.POST['notification_subject']
            data.notification_subject_arabic = request.POST['notification_subject_arabic']
            data.notification_content = request.POST['notification_content']
            data.notification_content_arabic = request.POST['notification_content_arabic']
            data.updated_at =  timezone.now() 
            data.save()
            try:
                log_activity(request, id,"update email template")    
            except Exception as e:
                return render(request , "connection_error.html")
            messages.success(request, f"Notification template status updated successfully!")
            return redirect('superadminapp:get_notification_template')
        context = {
            "data":data
            }
        return render(request, 'update_notification_template.html',context)
    else:
        return redirect('superadminapp:login')