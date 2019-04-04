"""Post forms"""

#django
from django import forms

#models
from posts.models import Posts

class PostForm(forms.ModelForm):
    """Post model form"""

    class Meta:
        """Form settings"""
        model  = Posts
        fields = ('user', 'profile', 'title', 'photo')