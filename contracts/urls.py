from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import AddFolder,FolderListAPIView,FolderNameListAPIView,CategoryListAPIView,TemplateListAPIView,AddTemplateAPIView,AddContractAPIView,AddPartyAPIView,ContractslistAPIViewAPP,ContractStatusUpdateAPIView,ContractStatusListAPIView,PartyUserdetailsAPIView,AppendixUploadView,TemplateImageUploadAPIView,ContractCloneAPIView,ContractDetailsAPIView,UpdateContractAPIView,ContractPartyDetailsAPIView,UpdatePartyAPIView,ContractslistAPIViewWEB,DeleteFolderAPI,EditFolderAPIView,FolderDetailAPIView,FolderNameListallAPIView,Party_company_users_listAPIView,Authorized_users_listView,BusinessContractPartyCreateView


urlpatterns = [
    path('folders_add', AddFolder.as_view(),),
    path('folders_list', FolderListAPIView.as_view()),
    path('folders_name', FolderNameListAPIView.as_view()),
    path('folders_name_all', FolderNameListallAPIView.as_view()),
    path('delete_folder', DeleteFolderAPI.as_view()),
    path('edit_folder', EditFolderAPIView.as_view()),
    path('folder_details', FolderDetailAPIView.as_view()),
    # path('notification_add',AddNotificationAPIView.as_view()),
    # path('notification_list',ListNotificationAPIView.as_view()),
    # path('notification_delete',NotificationDeleteAPIView.as_view()),
    path('category_list',CategoryListAPIView.as_view()),
    path('template_list',TemplateListAPIView.as_view()),
    path('template_image',TemplateImageUploadAPIView.as_view()),
    path('template_add',AddTemplateAPIView.as_view()),
    path('contract_add',AddContractAPIView.as_view()),
    path('contract_update',UpdateContractAPIView.as_view()),
    path('party_add',AddPartyAPIView.as_view()),
    path('party_details',ContractPartyDetailsAPIView.as_view()),
    path('party_update',UpdatePartyAPIView.as_view()),
    path('status_update',ContractStatusUpdateAPIView.as_view()),
    path('contract_status_list',ContractStatusListAPIView.as_view()),
    path('contract_listing',ContractslistAPIViewAPP.as_view()),
    path('contract_list',ContractslistAPIViewWEB.as_view()),
    path('party_user_detail',PartyUserdetailsAPIView.as_view()),
    path('appendix_add',AppendixUploadView.as_view()),
    path('clone_contract',ContractCloneAPIView.as_view()),
    path('contract_details',ContractDetailsAPIView.as_view()),
    path('party_company_users_list', Party_company_users_listAPIView.as_view()),
    path('authorized_users_list', Authorized_users_listView.as_view()),
    path('add_business_party', BusinessContractPartyCreateView.as_view()),
        
        
        
        
    # path('contract_list_test', ContractslistAPIViewWEBTest.as_view()),
        
]