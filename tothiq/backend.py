from django.contrib.auth.backends import ModelBackend
from business_admin.models import business_info

class BusinessInfoBackend(ModelBackend):
    def authenticate(self, request, token=None):
        try:
            user = business_info.objects.get(token=token)
            return user
        except business_info.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = business_info.objects.get(pk=user_id)
            return user
        except business_info.DoesNotExist:
            return None
