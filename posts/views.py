#las vistas son la logica de como se traen los datos

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
#models
from posts.models import Posts

#forms
from posts.forms import PostForm

#utilities
from datetime import datetime

# Create your views here.
"""
posts=[
    {
        'title': 'Mont Blac',
        'user':{
            'name': 'Fernanda Palacios',
            'picture': 'https://picsum.photos/60/60/?image=1027',
        },
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'photo': 'https://picsum.photos/200/200/?image=1036', 
    },
    {
        'title': 'Via Láctea',
        'user':{
            'name': 'Victor Torres',
            'picture': 'https://picsum.photos/60/60/?image=1005',
        },
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'photo': 'https://picsum.photos/200/200/?image=903',
    },
    {
        'title': 'Nuevo Auditorio',
        'user':{
            'name': 'Abraham Palacios',
            'picture': 'https://picsum.photos/60/60/?image=883',
        },
        
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'photo': 'https://picsum.photos/200/200/?image=1076',
    }

]"""

@login_required
def list_posts(request):

    posts = Posts.objects.all().order_by('-created')
    return render(request, 'posts/feed.html', {'posts': posts})
    #content = []
    #for post in posts:
    #    content.append("""
    #        <p><Strong>{name}</Strong></p>
    #        <p><small>{user} - <i>{timestamp} </i></samll></p>
    #        <figure><img src="{picture}" /></figure>
    #    """.format(**post))
    #return HttpResponse('<br>'.join(content))

class PostsFeedView(LoginRequiredMixin, ListView):
    """Return all piblished posts"""

    template_name='posts/feed.html'
    model = Posts
    ordering= ('-created',)
    paginate_by = 24
    context_object_name = 'posts'

class PostDetailView(LoginRequiredMixin, DetailView):
    """Post Detail view"""
    template_name='posts/detail.html'
    queryset= Posts.objects.all()
    context_object_name='post'

class CreatePostView(LoginRequiredMixin, CreateView):
    """Create new posts view"""

    template_name='posts/new.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self, **kwargs):
        """Add user and profile to context"""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile 
        return context
        

@login_required
def create_post(request):
    """Create new post new"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:feed')
    else:
        form = PostForm()

    return render(
        request =  request,
        template_name = 'posts/new.html',
        context= {
            'form':form,
            'user': request.user,
            'profile': request.user.profile
        }
    )


        
