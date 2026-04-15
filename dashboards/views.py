from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import AddUserForm, BlogPostForm, CategoryForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Helper — only allow staff users
def staff_required(view_func):
    decorated = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='login'
    )(view_func)
    return login_required(decorated, login_url='login')


@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access the dashboard.')
        return redirect('home')
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
        'category_count': category_count,
        'blogs_count': blogs_count,
    }
    return render(request, 'dashboard/dashboard.html', context)


@staff_required
def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'dashboard/categories.html', context)


@staff_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('categories')
    form = CategoryForm()
    context = {'form': form}
    return render(request, 'dashboard/add_category.html', context)


@staff_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('categories')
    form = CategoryForm(instance=category)
    context = {'form': form, 'category': category}
    return render(request, 'dashboard/edit_category.html', context)


@staff_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully.')
    return redirect('categories')


@staff_required
def posts(request):
    posts = Blog.objects.all()
    context = {'posts': posts}
    return render(request, 'dashboard/posts.html', context)


@staff_required
def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            messages.success(request, 'Post published successfully.')
            return redirect('posts')
        else:
            print('form is invalid')
            print(form.errors)
    form = BlogPostForm()
    context = {'form': form}
    return render(request, 'dashboard/add_post.html', context)


@staff_required
def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('posts')
    form = BlogPostForm(instance=post)
    context = {'form': form, 'post': post}
    return render(request, 'dashboard/edit_post.html', context)


@staff_required
def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    messages.success(request, 'Post deleted successfully.')
    return redirect('posts')


@staff_required
def users(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'dashboard/users.html', context)


@staff_required
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully.')
            return redirect('users')
        else:
            print(form.errors)
    form = AddUserForm()
    context = {'form': form}
    return render(request, 'dashboard/add_user.html', context)


@staff_required
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('users')
    form = EditUserForm(instance=user)
    context = {'form': form}
    return render(request, 'dashboard/edit_user.html', context)


@staff_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('users')
