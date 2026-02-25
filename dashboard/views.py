from django.shortcuts import get_object_or_404, redirect, render
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required
from .forms import AddUserForm, BlogPostForm, CategoryForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
        'category_count': category_count,
        'blogs_count': blogs_count,
    }
    return render(request, 'dashboard/dashboard.html', context)

#################3 Categories crud operations ###################33

def categories(request):
    return render(request, 'dashboard/categories.html')

@permission_required('blogs.add_category', raise_exception=True)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()

    context = {
            'form': form,
        }
    return render(request, 'dashboard/add_category.html', context)

@permission_required('blogs.change_category', raise_exception=True)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
        else:
            messages.error(request, "Category already exists!!...")
    form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'dashboard/edit_category.html', context)

@permission_required('blogs.delete_category', raise_exception=True)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories') 


##################### Blogs Crud operations ##################
def posts(request):
    posts = Blog.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'dashboard/posts.html', context)

def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) # temporarily saving the form
            post.author = request.user
            post.save()

            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()

            return redirect('posts')
        else:
            print('form is invalid')
            print(form.errors)
    form = BlogPostForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_post.html', context)

def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    
    # Allow if admin OR author
    if not (request.user.has_perm('blogs.change_blog') or post.author == request.user):
        return HttpResponseForbidden("You are not allowed to edit this post")

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug =slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')
    form = BlogPostForm(instance=post)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'dashboard/edit_post.html', context)

def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if not (request.user.has_perm('blogs.delete_blog') or post.author == request.user):
        return HttpResponseForbidden("You are not allowed to delete this post")
    post.delete()
    return redirect('posts') 

#################### User CRUD operations ######################

def users(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'dashboard/users.html', context)

def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            print(form.errors)

    form = AddUserForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_user.html', context)

def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            print(form.errors)
    form = EditUserForm(instance=user)
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'dashboard/edit_user.html', context)

def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('users') 

def dashboard_logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('home')  # or wherever you want

    return render(request, 'dashboard/logout.html')

# Self blog posts crud 

def my_posts(request):
    posts = Blog.objects.filter(author=request.user)
    context = {
        'posts': posts,
    }
    return render(request, 'dashboard/my_posts.html', context)

