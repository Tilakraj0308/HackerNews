from django.shortcuts import render,redirect
from .models import Post, Comment, User
from itertools import chain
from django.contrib.auth import logout,login, authenticate
from django.contrib import messages
from datetime import datetime
from .forms import postForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.


def calculate_score(votes, submission_time, comments):
    submission_time = submission_time.replace(tzinfo=None)
    time_delta = datetime.now() - submission_time
    hours_since_submission = time_delta.total_seconds() / 3600
    gravity = 1.3
    score = (votes - 1) / pow((hours_since_submission + 2), gravity)
    return score + comments * 0.5

def rank_posts(posts):
    ranked_posts = []
    for post in posts:
        score = calculate_score(post.upvote, post.created, post.comment_set.count())
        ranked_posts.append((post, score))
    ranked_posts.sort(key=lambda x: x[1], reverse=True)
    return ranked_posts

def pagination(p, post_per_page, obj):
    size = len(obj)
    total_pages = size//post_per_page+1
    start_index = (p - 1) * post_per_page
    end_index = start_index + post_per_page
    ol_start = (p-1)*post_per_page+1
    curr_obj = obj[start_index:end_index]
    return {"curr_obj" : curr_obj, "p": p, "total_pages" : total_pages, "post_per_page":post_per_page, "ol_start":ol_start}


def home(request):
    p = request.GET.get('p')
    if p == None:
        p = 1
    p = int(p)
    posts = Post.objects.all()
    posts = rank_posts(posts)
    context = pagination(p=p, post_per_page=10, obj=posts)
    return render(request, 'base/home.html', context)

def new(request):
    p = request.GET.get('p')
    if p == None:
        p = 1
    p = int(p)
    posts = Post.objects.order_by('-created')
    # context = {'posts' : posts}
    context = pagination(p=p, post_per_page=10, obj=posts)
    return render(request, 'base/new.html', context)

def thread(request):
    p = request.GET.get('p')
    if p == None:
        p = 1
    p = int(p)
    user = request.user
    posts = user.post_set.all()
    comments = user.comment_set.all()

    combined_objects = sorted(chain(posts, comments),
                              key = lambda obj : obj.created, reverse=True)
    
    # context = {'threads' : combined_objects}
    context = pagination(p=p, post_per_page=10, obj=combined_objects)

    return render(request, 'base/thread.html', context)

def comment(request):
    p = request.GET.get('p')
    if p == None:
        p = 1
    p = int(p)
    comments = Comment.objects.all()
    context = pagination(p=p, post_per_page=10, obj=comments)
    return render(request, 'base/comment.html', context)

# @login_required(login_url='login_form')
def submit(request):
    if not request.user.is_authenticated:
        arg1 = 'You have to be logged in to submit'
        return redirect(reverse('login_form')+f'?arg1={arg1}')
    form = postForm()
    if request.method == 'POST':
        form = postForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user= request.user
            instance.save()
            return redirect('new')
        url = form.data['url']
        post = Post.objects.filter(url=url)
        post_url = reverse('items') + f'?id={post[0].id}&reply_to=post'
        return redirect(post_url)
            # Redirect or perform other actions
    context = {'form':form}
    return render(request, 'base/submit.html', context)

def logPage(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    arg1 = request.GET.get('arg1')
    arg2 = request.GET.get('arg2')
    pk = request.GET.get('pk')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "No such username")
            return redirect('login_form')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user=user)
            _to = arg1.split()[-1]
            if _to == 'submit':
                return redirect('submit')
            elif _to == 'vote':
                if arg2 == 'p':
                    return redirect('upvote', 'p', pk)
                else:
                    return redirect('upvote', 'c', pk)
            return redirect('new')
        else:
            messages.error(request, "Username and password doesn't match")
    context = {}
    if arg1 is not None:
        context['arg1'] = arg1
    return render(request, 'base/form.html', context)

def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        if user is not None:
            return redirect('login_form')
        else:
            messages.error(request, "Error creating account!!")
            return redirect('register_form')
    return render(request, 'base/form.html')

def upvote(request, mod, pk):
    if not request.user.is_authenticated:
        arg1 = 'You have to be logged in to vote'
        return redirect(reverse('login_form')+f'?arg1={arg1}&arg2={mod}&pk={pk}')
        # return redirect('login_form' , arg1="You have to be logged in to vote")
    if mod == 'p':
        post = Post.objects.get(id=pk)
        post.upvote+=1
        post.up_users.add(request.user)
        post.save()
        return redirect('home')
    else:
        # print('hello')
        comment = Comment.objects.get(id=pk)
        comment.upvote+=1
        comment.up_users.add(request.user)
        comment.save()
        return redirect('home')
    
def dvote(request, mod, pk):
    if mod == 'p':
        post = Post.objects.get(id=pk)
        post.upvote-=1
        post.up_users.remove(request.user)
        post.save()
        return redirect('home')
    else:
        comment = Comment.objects.get(id=pk)
        comment.upvote-=1
        comment.up_users.remove(request.user)
        comment.save()
        return redirect('home')
    

def items(request):
    pk = request.GET.get('id')
    reply_to = request.GET.get('reply_to')
    if reply_to == 'post':
        post = Post.objects.get(id=pk)
        if request.method == 'POST':
            comment_body = request.POST.get('comment')
            comment = Comment.objects.create(
                user = request.user,
                parent = None,
                body = comment_body,
                post = post
            )
            comment.save()
        comments = Comment.objects.filter(post=post, parent=None)
        context = {"comments" : comments, "post" : post}
    else :
        comment = Comment.objects.get(id=pk)
        post = comment.post
        if request.method == 'POST':
            comment_body = request.POST.get('comment')
            comment = Comment.objects.create(
                user = request.user,
                parent = comment,
                body = comment_body,
                post = comment.post
            )
            comment.save()
        comments = Comment.objects.filter(post=post, parent=comment)
        context={"comments" : comments, "parent_comment" : comment}
    return render(request, 'base/items.html', context)

def profile(request):
    username = request.GET.get('id')
    user = User.objects.get(username=username)
    context = {'user':user}
    return render(request, 'base/profile.html', context)

def getprofileItems(request):
    username = request.GET.get('id')
    user = User.objects.get(username=username)
    obj = request.GET.get('obj')
    if obj == 'post':
        p = request.GET.get('p')
        if p == None:
            p = 1
        p = int(p)
        posts = Post.objects.get(user=user)
        posts = rank_posts(posts)
        context = pagination(p=p, post_per_page=10, obj=posts)
        return render(request, 'base/new.html', context)
    else:
        comments = Comment.objects.filter(user=user)
        context = {"obj":obj, "comments":comments}
    return render(request, 'base/userItems.html', context)
