from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Blog, Category

# Create your views here.
def posts_by_category(request, category_id):
    # Fetch the posts that belongs to a particular category_id
    posts = Blog.objects.filter(status='Published', category=category_id)

    # To perform some action if the category_id is not found, we use try-except block
    # try:
    #     category = Category.objects.get(pk=category_id)
    # except:
    #     # redirect the user to home page instead of showing the error
    #     return redirect('home')
    
    category = get_object_or_404(Category, pk=category_id)

    context = {
        'posts': posts,
        'category': category,
    }

    return render(request, 'post_by_category.html', context)