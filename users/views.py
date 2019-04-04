"""Users views."""

# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

#exception
#from django.db.utils import IntegrityError

#models
from django.contrib.auth.models import User
from posts.models import Posts
from users.models import Profile

#forms
from users.forms import ProfileForm, SignupForm


def login_view(request):
    """Login view."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('posts:feed')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid username or password'})

    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    """Logout user"""

    logout(request)
    return redirect('users:login')

@login_required
def update_profile(request):
    """Update profile"""
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            #print(form.cleaned_data)
            data = form.cleaned_data

            profile.website = data['website']
            profile.phone_number = data['phone_number']
            profile.biography = data['biography']
            profile.picture = data['picture']
            profile.save()

            url = reverse('users:detail', kwargs={'username': request.user.username})
            return redirect(url)

    else:
        form = ProfileForm()

    return render(
        request= request, 
        template_name='users/update_profile.html', 
        context={
            'profile': profile,
            'user': request.user,
            'form':form
        }
    )

def signup(request):
    """sing up user"""
    if request.method == 'POST': #se verifica que el metodo sea post
        form = SignupForm(request.POST) #se le pasa el request al form y se almacena en una variable
        if form.is_valid(): #verifica que las validaciones sea correctas
            form.save() #guarda el form
            return redirect('users:login') #y returna a login
    else: #si no es un metodo post sino un get
        form = SignupForm()

    return render(  #retorna al template de singup envieanlode los parametros correspondientes
        request=request,
        template_name='users/signup.html',
        context={'form': form}
    )


class SignupView(FormView):
    """User´s sign up view"""
    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form): #siempre que sea un form como view se debe escribir esta funcion 
        """Save form data,"""
        form.save()
        return super.form_valid(form)



class UserDetailView(LoginRequiredMixin, DetailView):
    """user detail view"""
    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's posts to context"""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Posts.objects.filter(user=user).order_by('-created')
        return context
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view"""
    template_name='users/update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']

    def get_object(self):
        """Return user´s profile """
        return self.request.user.profile

    def get_success_url(self):
        """Return to user´s profile"""
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username': username})