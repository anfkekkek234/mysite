from django.shortcuts import render , get_object_or_404 , redirect
from django.utils import timezone
from blog.models import Post , Comment
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from website.models import Contact
from blog.forms import CommentForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
def blog(request,**kwargs):
    current_time = timezone.now()
    posts = Post.objects.filter(status=1,published_date__lte=current_time)
    if kwargs.get('cat_name') != None:
        posts = posts.filter(category__name=kwargs['cat_name'])
    if kwargs.get('author_username') != None:
        posts = posts.filter(author__username=kwargs['author_username'])
    if kwargs.get('tag_name') != None:
        posts = posts.filter(tags__name=kwargs['tag_name'])
    posts = Paginator(posts,3)
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
    context = {'posts': posts}
    return render(request,'blog/blog-home.html',context)

def blog_single(request, pid):
    current_time = timezone.now()
    post = get_object_or_404(Post, pk=pid, status=1, published_date__lte=current_time)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # مقداردهی فیلد post_id
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Your comment submitted successfully')
        else:
            messages.add_message(request, messages.ERROR, 'Your comment didn\'t submit')
    else:
        form = CommentForm()
    if not post.login_required:
        comments = Comment.objects.filter(post=post.id, approved=True)
        post.counted_views += 1
        post.save()
        all_posts = Post.objects.filter(status=1, published_date__lte=current_time)
        current_index = list(all_posts).index(post)

        previous_post = None
        next_post = None
        if current_index > 0:
            previous_post = all_posts[current_index - 1]
        if current_index < len(all_posts) - 1:
            next_post = all_posts[current_index + 1]

        context = {
            'post': post,
            'previous_post': previous_post,
            'next_post': next_post,
            'comments': comments,
            'form': form,
        }
        return render(request, 'blog/blog-single.html', context)
    else:
        return HttpResponseRedirect(reverse('accounts:login'))




def search(request):
    current_time = timezone.now()
    posts = Post.objects.filter(status=1,published_date__lte=current_time)
    if request.method == 'GET':
        if s := request.GET.get('s'):
            posts = posts.filter(content__contains=s)
    context = {'posts': posts}
    return render(request,'blog/blog-home.html',context)