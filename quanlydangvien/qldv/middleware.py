from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Middleware that redirects all unauthenticated users to the login page.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            # List of URL names that are exempt from the login requirement
            exempt_url_names = ['login', 'signup', 'logout']
            
            # Check if the current URL name is in the exempt list
            from django.urls import resolve
            try:
                resolver_match = resolve(request.path_info)
                if resolver_match.url_name in exempt_url_names:
                    return self.get_response(request)
                
                # Also exempt admin pages
                if request.path_info.startswith('/admin/'):
                    return self.get_response(request)
            except:
                pass

            # Redirect to login page
            return redirect(f"{reverse('login')}?next={request.path}")

        response = self.get_response(request)
        return response
