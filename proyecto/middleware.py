"""Platzigram middleware catalog"""

#django
from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    """Profile completion middleware.
    Ensure evely user that is interacting with the plataform
    have their profile picture and biography.
    """
    def __init__(self, get_response):
        """Initialization Middleware"""
        self.get_response = get_response

    def __call__(self, request):
        """Code to be executed for each request before the view is called"""
        if not request.user.is_anonymous:  #verifica si hay un usuario logueado
            if not request.user.is_staff:
                profile = request.user.profile #obtiene el perfil del usuario que se a logueado
                if not profile.picture or not profile.biography: #verifica si el usuario tiene datos en el campo foto y byography
                    if request.path not in [reverse('users:update'), reverse('users:logout')]: #la reverse es obtener la url apartir del nombre
                        return redirect('users:update')
    
        response = self.get_response(request)
        return response