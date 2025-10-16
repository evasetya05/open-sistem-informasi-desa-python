from django.shortcuts import render, get_object_or_404, redirect
from .models import Penduduk, KartuKeluarga
from .forms import PendudukForm, KartuKeluargaForm
from django.contrib import messages


# --- Kartu Keluarga ---
def kk_list(request):
    kks = KartuKeluarga.objects.all()
    return render(request, 'kependudukan/kk_list.html', {'kks': kks})


def kk_detail(request, pk):
    kk = get_object_or_404(KartuKeluarga, pk=pk)
    anggota = kk.penduduk_set.all()
    anak_kk = kk.children.all()  # semua KK turunan

    return render(request, 'kependudukan/kk_detail.html', {
        'kk': kk,
        'anggota': anggota,
        'anak_kk': anak_kk,
    })



def kk_add(request):
    if request.method == 'POST':
        form = KartuKeluargaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kartu Keluarga baru berhasil ditambahkan.")
            return redirect('kk_list')
    else:
        form = KartuKeluargaForm()
    return render(request, 'kependudukan/kk_form.html', {'form': form})


def kk_edit(request, pk):
    kk = get_object_or_404(KartuKeluarga, pk=pk)
    if request.method == 'POST':
        form = KartuKeluargaForm(request.POST, instance=kk)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Kartu Keluarga berhasil diperbarui.")
            return redirect('kk_detail', pk=kk.pk)
    else:
        form = KartuKeluargaForm(instance=kk)
    return render(request, 'kependudukan/kk_form.html', {'form': form})


# --- Penduduk ---
def penduduk_list(request):
    penduduks = Penduduk.objects.select_related('kk').all()
    return render(request, 'kependudukan/penduduk_list.html', {'penduduks': penduduks})


def penduduk_add(request):
    if request.method == 'POST':
        form = PendudukForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Penduduk baru berhasil ditambahkan.")
            return redirect('penduduk_list')
    else:
        form = PendudukForm()
    return render(request, 'kependudukan/penduduk_form.html', {'form': form})


def penduduk_detail(request, pk):
    penduduk = get_object_or_404(Penduduk, pk=pk)
    return render(request, 'kependudukan/penduduk_detail.html', {'penduduk': penduduk})
