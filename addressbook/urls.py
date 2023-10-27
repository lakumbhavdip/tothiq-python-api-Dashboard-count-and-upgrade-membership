from django.urls import path
from addressbook.views import AddressBookAPIView,AddressBookListAPIView,AddressBookdetailAPIView,contactsuggestAPIView,DeleteInviteAPIView

urlpatterns = [
    path('address-book', AddressBookAPIView.as_view(), name='address-book'),
    path('address-book-list', AddressBookListAPIView.as_view(), name='address-book'),
    path('address-book-suggestions', contactsuggestAPIView.as_view(), name='address-book'),
    # path('address-book-list-filter', AddressBookListFilterAPIView.as_view(), name='address-book'),
    path('address-book-details', AddressBookdetailAPIView.as_view(), name='address-book'),
    path('delete_invite', DeleteInviteAPIView.as_view(), name='address-book')
    
]