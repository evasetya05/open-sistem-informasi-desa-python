from django.shortcuts import render, get_object_or_404, redirect
from .models import Penduduk, KartuKeluarga
from .forms import PendudukForm, KartuKeluargaForm
from django.contrib import messages
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required

# --- Kartu Keluarga ---
@login_required
def kk_list(request):
    # Ambil semua penduduk yang kepala keluarga untuk prefetch
    kepala_qs = Penduduk.objects.filter(stat_hbkel_1__icontains="Kepala Keluarga")
    
    kks = KartuKeluarga.objects.prefetch_related(
        Prefetch('penduduk_set', queryset=kepala_qs, to_attr='kepala_list')
    ).all()

    return render(request, 'kependudukan/kk_list.html', {'kks': kks})

@login_required
def kk_detail(request, pk):
    kk = get_object_or_404(KartuKeluarga, pk=pk)
    anggota = kk.penduduk_set.all()
    anak_kk = kk.children.all()  # semua KK turunan

    return render(request, 'kependudukan/kk_detail.html', {
        'kk': kk,
        'anggota': anggota,
        'anak_kk': anak_kk,
    })


@login_required
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

@login_required
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
@login_required
def penduduk_list(request):
    penduduks = Penduduk.objects.select_related('no_kk').all()
    return render(request, 'kependudukan/penduduk_list.html', {'penduduks': penduduks})

@login_required
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

@login_required
def penduduk_detail(request, pk):
    penduduk = get_object_or_404(Penduduk, pk=pk)
    return render(request, 'kependudukan/penduduk_detail.html', {'penduduk': penduduk})
