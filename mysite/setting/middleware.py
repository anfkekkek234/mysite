from django.shortcuts import redirect
from django.urls import reverse

class ComingSoonMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = [
            reverse('admin:index'),
            '/admin/',
            reverse('coming_soon'),
            '/coming_soon/'
        ]

        if not any(request.path.startswith(path) for path in excluded_paths):
            return redirect('coming_soon')

        response = self.get_response(request)
        return response
