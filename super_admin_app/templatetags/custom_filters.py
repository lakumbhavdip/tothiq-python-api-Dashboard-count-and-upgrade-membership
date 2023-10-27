import ast
from django import template
from django.contrib.auth.hashers import check_password
import os

from super_admin_app.models import GeneralNotification

register = template.Library()

@register.filter(name='literal_eval')
def literal_eval(value):
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        # If the conversion fails, return an empty list (or handle the error as desired)
        return []
    
    
@register.filter(name='is_valid_password')
def is_valid_password(value, hashed_password):
    return check_password(value, hashed_password)

@register.filter
def has_missing_image(image):
    media_path = image.path if image else ''
    return media_path and os.path.exists(media_path)