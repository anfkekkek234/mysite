from django.shortcuts import render , get_object_or_404
from django.utils import timezone
from blog.models import Post


# Create your views here.
def blog(request):
    current_time = timezone.now()
    posts = Post.objects.filter(status=1,published_date__lte=current_time)
    context = {'posts': posts}
    return render(request,'blog/blog-home.html',context)

def blog_single(request,pid):
    current_time = timezone.now()
    post = get_object_or_404(Post,pk=pid,status=1,published_date__lte=current_time)
    post.counted_views += 1
    post.save()
    all_posts = Post.objects.filter(status=1)
    current_index = list(all_posts).index(post)

    previous_post = None
    next_post = None

    # بررسی می‌کنیم آیا پست‌های قبلی و بعدی وجود دارند یا نه
    if current_index > 0:
        previous_post = all_posts[current_index - 1]
    if current_index < len(all_posts) - 1:
        next_post = all_posts[current_index + 1]

    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,}
    return render(request, 'blog/blog-single.html',context)

