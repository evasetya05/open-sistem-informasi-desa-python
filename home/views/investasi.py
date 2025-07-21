from django.shortcuts import render, get_object_or_404
from home.models import PostingInvestasi

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

