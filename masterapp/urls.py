from django.urls import path
from .views import LanguageListView,NationalityListAPIView,FileUploadView,initializeAPIView,MembershipAPIView,PaymentInitAPIView,PaymentResponseAPIView,CouponApplyView,labellistAPIView,AddLabelAPIView,UpdateLabelAPIView,AddCountryCurrency,ListCountryCurrency,UpdateCountryCurrency


urlpatterns = [
    path('language', LanguageListView.as_view()),
    path('nationality', NationalityListAPIView.as_view()),
    path('file_upload', FileUploadView.as_view()),
    path('initialize', initializeAPIView.as_view()),
    path('membership', MembershipAPIView.as_view()),
    path('payment-init',PaymentInitAPIView.as_view()),
    path('payment-response',PaymentResponseAPIView.as_view()),
    path('coupon-apply',CouponApplyView.as_view()),
    path('label_list',labellistAPIView.as_view()),
    path('add_label',AddLabelAPIView.as_view()),
    path('update_label',UpdateLabelAPIView.as_view()),
    path('add_country_currency',AddCountryCurrency.as_view()),
    path('list_country_currency',ListCountryCurrency.as_view()),
    path('update_country_currency',UpdateCountryCurrency.as_view()),
    
    
]
