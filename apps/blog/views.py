from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BlogForm
from .models import Blog

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.penulis = request.user
            blog.save()
            
            messages.success(request, "Blog berhasil di-post!")  # ✅ Show success message
            
            form = BlogForm()  # ✅ Reset form after successful submission

    else:
        form = BlogForm()

    return render(request, 'blog/create_blog.html', {'form': form})


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')  # Newest first
    return render(request, 'blog/blog_list.html', {'blogs': blogs})

