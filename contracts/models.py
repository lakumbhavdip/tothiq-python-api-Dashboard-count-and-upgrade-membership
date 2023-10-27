from django.db import models
from user.models import Users
from django.utils import timezone
from business_admin.models import business_info
from masterapp.models import countrycurrency


#contracts folder model
class Folder(models.Model):
    id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', db_column='parent_id')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, db_column='user_id')
    folder_name = models.CharField(max_length=255)
    folder_name_arabic = models.CharField(max_length=255,null=True)
    ACTIVE_STATUS_CHOICES = [
          ('active', 'Active'),
          ('inactive', 'Inactive'),
          ('blocked', 'Blocked'),
          ('deleted', 'Deleted'),
      ]
    active_status = models.CharField(max_length=100,choices=ACTIVE_STATUS_CHOICES,null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.folder_name






#contracts categories
class categories(models.Model):
    category_name = models.CharField(max_length=100)
    category_name_arabic = models.CharField(max_length=100,null=True)
#     CATEGORY_AVAILABILITY = (
#     ('Free membership', 'Free membership'),
#     ('Basic membership', 'Basic membership'),
#     ('Premium membership', 'Premium membership'),
#   )
    CATEGORY_AVAILABILITY = (
        ('Individual Membership','individual membership'),
        ('Business Membership','business membership'),
    )
    category_availability = models.CharField(max_length=50, choices=CATEGORY_AVAILABILITY, default='')
    individual_Premium_Membership = models.BooleanField(default=False)
    individual_basic_Membership = models.BooleanField(default=False)
    individual_free_Membership = models.BooleanField(default=False)
    business_Premium_Membership = models.BooleanField(default=False)
    business_basic_Membership = models.BooleanField(default=False)
    business_free_Membership = models.BooleanField(default=False)
    category_availability = models.CharField(max_length=50, choices=CATEGORY_AVAILABILITY, default='')
    
    # is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)



# contracts templates
class template (models.Model):
    template_title = models.CharField(max_length=250)
    template_title_arabic = models.CharField(max_length=250, null=True)
    category = models.ForeignKey(categories, on_delete=models.CASCADE, null=True)
    individual_free_template = models.BooleanField(default=False)
    individual_basic_template = models.BooleanField(default=False)
    individual_premium_template = models.BooleanField(default=False)
    business_free_template = models.BooleanField(default=False)
    business_basic_template = models.BooleanField(default=False)
    business_premium_template = models.BooleanField(default=False)
    image = models.ImageField(upload_to='tothiq_pic',blank=True)
    description = models.TextField()
    description_arabic = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    
#create contracts
class contracts(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, db_column='user_id')
    business = models.ForeignKey(business_info, on_delete=models.CASCADE,null=True)
    folder = models.ForeignKey(Folder,on_delete=models.CASCADE,null=True)
    template = models.ForeignKey(template,on_delete=models.CASCADE,null=True)
    contract_title = models.CharField(max_length=200,null=True)
    category = models.ForeignKey(categories, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=500,null=True)
    contract_duration = models.BooleanField(default=False, null=True)
    contract_start_date = models.DateField(null=True)
    contract_end_date = models.DateField(null=True)
    currency = models.ForeignKey(countrycurrency,on_delete=models.CASCADE,null=True)
    contract_fees = models.BooleanField(default=False, null=True)
    contract_amount = models.DecimalField(max_digits=500,decimal_places=3,null=True)
    contract_amount_words = models.CharField(max_length=500,null=True)
    arbitration = models.BooleanField(null=True)
    jurisdiction = models.BooleanField(null=True)
    STATUS_CHOICES = (
            ('draft', 'Draft'),
            ('under_review', 'Under Review'),
            ('ready', 'Ready'),
            ('signed', 'Signed'),
            ('rejected', 'Rejected'),
            ('deleted', 'Deleted'),
            ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
    delete_reason = models.CharField(max_length=100,null=True)
    cancellation_reason = models.CharField(max_length=100,null=True)
    pin = models.BooleanField(default=False,null=True)
    appendix = models.ImageField(upload_to='tothiq_pic',blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
      db_table = 'contracts'




#contracts party type
class contract_party(models.Model):
    contract = models.ForeignKey(contracts, on_delete=models.CASCADE, null=True, blank=True, related_name='contract_parties')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id',null=True,blank=True)
    first_party_civil_id = models.CharField(max_length=12, blank=True, null=True)
    first_party_name = models.CharField(max_length=200, blank=True, null=True)
    first_party_email = models.CharField(max_length=100, blank=True, null=True)
    second_party_name = models.CharField(max_length=200, blank=True, null=True)
    second_party_email = models.CharField(max_length=100, blank=True, null=True)
    second_party_civil_id = models.CharField(max_length=12, blank=True, null=True)
    status = models.BooleanField(default=True)
    view_contract = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
      db_table = 'contracts_party'
      
      
    
#business contracts party type
class business_contract_party(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id', null=True, blank=True)
    contract = models.ForeignKey(contracts, on_delete=models.CASCADE, null=True, blank=True, related_name='contract')
    # authorized_person_sign = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='authorized_person_sign', null=True, blank=True)
    authorized_person_ids = models.TextField(null=True)  # Store IDs as comma-separated text
    PARTY_TYPE = (
        ('company', 'Company'),
        ('individual', 'Individual')
    )
    first_party_type = models.CharField(choices=PARTY_TYPE, max_length=500,null=True)
    first_party_name = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='first_party_name', null=True, blank=True)
    first_party_email = models.CharField(max_length=500,null=True)
    second_party_type = models.CharField(choices=PARTY_TYPE, max_length=500,null=True)
    second_party_name = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='second_party_name', null=True, blank=True)
    second_party_email = models.CharField(max_length=500,null=True)
    
    class Meta:
      db_table = 'business_contracts_party'
      