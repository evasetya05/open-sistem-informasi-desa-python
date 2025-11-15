from django.shortcuts import render, get_object_or_404, redirect
from apps.home.models import PostingInvestasi
from apps.home.forms import PostingInvestasiForm

def posting_investasi(request):
    data_posting = PostingInvestasi.objects.all().order_by('-tanggal_terbit')
    return render(request, 'home/investasi.html', {
        'posting_investasi': data_posting
    })


def detail_posting(request, slug):
    post = get_object_or_404(PostingInvestasi, slug=slug)
    return render(request, 'home/detail_investasi.html', {
        'post': post
    })



def create_posting_investasi(request):
    if request.method == "POST":
        form = PostingInvestasiForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("investasi")  # kembali ke daftar posting
    else:
        form = PostingInvestasiForm()

    return render(request, "home/create_investasi.html", {"form": form})


