from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Aset
from .forms import AsetForm

def aset_list(request):
    q = request.GET.get("q", "").strip()
    aset_qs = Aset.objects.all().order_by('-tahun_data')
    if q:
        aset_qs = aset_qs.filter(
            Q(nama__icontains=q)
            | Q(jenis__icontains=q)
            | Q(sub_kategori__icontains=q)
            | Q(no_ktp__icontains=q)
            | Q(no_sppt__icontains=q)
            | Q(nib__icontains=q)
            | Q(tahun_data__icontains=q)
        )
    return render(request, "aset/aset_list.html", {"asets": aset_qs, "q": q})

def aset_create(request):
    if request.method == "POST":
        form = AsetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("aset:aset_list")
    else:
        form = AsetForm()
    return render(request, "aset/aset_form.html", {"form": form})

def aset_edit(request, pk):
    aset = get_object_or_404(Aset, pk=pk)
    if request.method == "POST":
        form = AsetForm(request.POST, instance=aset)
        if form.is_valid():
            form.save()
            return redirect("aset:aset_list")
    else:
        form = AsetForm(instance=aset)
    return render(request, "aset/aset_form.html", {"form": form})
