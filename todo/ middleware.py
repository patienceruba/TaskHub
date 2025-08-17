from django.shortcuts import redirect
from django.urls import reverse

class SuperuserOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_urls = [
            reverse('register'), 
            reverse('system_settings'),
        ]
        if request.path in admin_urls:
            if not request.user.is_authenticated or not request.user.is_superuser:
                return redirect('no_permission')
        return self.get_response(request)
