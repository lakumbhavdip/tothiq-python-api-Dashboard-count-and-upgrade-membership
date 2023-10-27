# custom_error_middleware.py

from django.shortcuts import render
from django.http import HttpResponseNotFound

class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return self.custom_404_handler(request)
        return response

    def custom_404_handler(self, request):
        return render(request, '404.html', status=404)
