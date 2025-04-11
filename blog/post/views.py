from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post/post_list.html', {'posts': posts})

@login_required
def post_create(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    print(categories)
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        category_id = request.POST.get('category')
        tag_ids = request.POST.getlist('tags')
        image = request.FILES.get('image')
        print(image, 'img')

        category = Category.objects.get(id=category_id)
        post = Post.objects.create(
            title=title, content=content, image=image, category=category)

        for tag_id in tag_ids:
            tag = Tag.objects.get(id=tag_id)
            post.tags.add(tag)
        return redirect('post_list')

    return render(request, 'post/post_create.html', {'categories': categories, 'tags': tags})

@login_required
def post_delete(request, id):
    get_object_or_404(Post, id=id).delete()
    return redirect('post_list')

@login_required
def update_post(request, id):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.category = Category.objects.get(id=request.POST['category'])
        if 'image' in request.FILES:
            post.image = request.FILES['image']

        post.tags.clear()
        tag_ids = request.POST.getlist('tags')
        for tag_id in tag_ids:
            tag = Tag.objects.get(id=tag_id)
            post.tags.add(tag)
        post.save()
        return redirect('post_list')
    return render(request, 'post/update_post.html', {'categories': categories, 'tags': tags, "post": post})


def register_view(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'user already taken or exists ')
            return redirect('register')
        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.save()
        messages.success(request, 'account createed successfully  ')
        return redirect('login')
    return render(request, 'user/register_view.html', )


def login_view(request):
    if request.method == "POST":
    
        username = request.POST['username']
        password = request.POST['password']
        # **credentials
        user = authenticate(request, username=username, password=password)
        if user :
            login(request,user)
            messages.success(request, 'login successfully  ')
            return redirect('post_list')
        else:
            messages.error(request, ' invalid credentials ')
            return redirect('login/')
            
    
    return render(request, 'user/login.html', )
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, ' logout successfully ')
    return redirect('login_view')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment, Post

@login_required 
def comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)  
    comments = Comment.objects.filter(post=post).order_by('-id')  
    count = Comment.objects.filter(post=post).count()
    if request.method == "POST":
        text = request.POST.get('text')

       
        Comment.objects.create(user=request.user, text=text, post=post)
        return redirect("comment", post_id=post.id)

    return render(request, 'post/comment.html', {'post': post, 'comments': comments,'count':count})

def only(request, id):
    onl = get_object_or_404(Post, id=id)  
    return render(request, 'post/only.html', {'only': onl,})


