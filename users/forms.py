"""Users forms"""

from django import forms

#models
from django.contrib.auth.models import User
from users.models import Profile

class SignupForm(forms.Form):
    """Sign uo Form"""
    username = forms.CharField(min_length=4, max_length=50)
    password = forms.CharField(max_length=70, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(max_length=70, widget=forms.PasswordInput())
    first_name = forms.CharField(min_length=2, max_length=50)
    last_name = forms.CharField(min_length=2, max_length=50)
    email = forms.CharField(min_length=6, max_length=70, widget=forms.EmailInput())

    def clean_username(self): #validar solo el campo username
        """Username must be unique"""
        username = self.cleaned_data['username'] #obtener el valor que django ya limpio
        query = User.objects.filter(username=username).exists()
        if query:
            raise forms.ValidationError('Username is already in use.')
        return username #siempre que se valide una dato se debe retornar

    def clean(self): 
        """Verify password confirmation match"""
        data = super().clean() #se obtiene los datos con suoer antes de ser csobreescrito
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match')
        
        return data
    
    def save(self): #por ultimo cuando ya se ecnutran los datos correctamente se guardan
        """Create user and profile"""
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()


class ProfileForm(forms.Form): #este modelo de profile no se utiliza pcuando se utiliza la UpdateView(class-based views)
    """Profile Form"""
    website = forms.URLField(max_length=200, required=True)
    biography = forms.CharField(max_length=500, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    picture = forms.ImageField()
