from django.shortcuts import render , get_object_or_404
from datetime import datetime
from blog.models import Post


# Create your views here.
def blog(request):
    current_time = datetime.now()
    posts = Post.objects.filter(status=1,published_date__lte=current_time)
    context = {'posts': posts}
    return render(request,'blog/blog-home.html',context)

def blog_single(request,pid):
    post = get_object_or_404(Post,pk=pid,status=1)
    post.counted_views += 1
    post.save()
    context = {'post':post}
    return render(request, 'blog/blog-single.html',context)
