from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Blog, Category, Comment
from django.db.models import Q
from django.shortcuts import redirect

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

def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.blog = single_blog
        comment.comment = request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)   # To come back to same page we were in, Httpresponseredirect is user

    # Comments 
    comments = Comment.objects.filter(blog=single_blog)
    comment_count = comments.count()

    context = {
        'single_blog': single_blog,
        'comments': comments,
        'comment_count': comment_count,
    }
    return render(request, 'blogs.html', context)

def delete_comment(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=comment_id)

        if request.user == comment.user:
            slug = comment.blog.slug
            comment.delete()
            return redirect('blogs', slug=slug)

    return redirect('/')

def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='Published')
    context = {
        'blogs': blogs,
        'keyword': keyword,
    }
    return render(request, 'search.html', context)
