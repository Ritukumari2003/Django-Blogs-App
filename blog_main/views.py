from django.shortcuts import render
from about.models import About
from blogs.models import Category, Blog

def home(request):
    featured_posts = Blog.objects.filter(is_featured=True, status = 'Published').order_by('updated_at')
    posts = Blog.objects.filter(is_featured=False, status = 'Published').order_by('updated_at')

    # Fetch the about section data 
    try:
        about = About.objects.get()
    except:
        about=None
        
    context = {
        'featured_posts': featured_posts,
        'posts':posts,
        'about': about,
    }

    return render(request, 'home.html', context)