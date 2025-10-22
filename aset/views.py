from django.shortcuts import render, get_object_or_404, redirect
from .models import Aset
from .forms import AsetForm

def aset_list(request):
    aset_list = Aset.objects.all().order_by('-tahun_data')
    return render(request, "aset/aset_list.html", {"asets": aset_list})

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
