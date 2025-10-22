from django.shortcuts import render, get_object_or_404, redirect
from .models import Penduduk, KartuKeluarga
from .forms import PendudukForm, KartuKeluargaForm
from django.contrib import messages
from django.db.models import Prefetch, Q
from django.contrib.auth.decorators import login_required
from import_export.formats.base_formats import XLSX
from import_export.admin import ExportMixin
import tablib
from django.http import HttpResponse
from tablib import Dataset
from django.core.paginator import Paginator


@login_required
def kk_list(request):
    search = request.GET.get('q', '')
    kks = KartuKeluarga.objects.prefetch_related(
        'penduduk_set',
        Prefetch(
            'penduduk_set',
            queryset=Penduduk.objects.filter(stat_hbkel_1__icontains="Kepala Keluarga"),
            to_attr='kepala_list'
        )
    )


    if search:
        kks = kks.filter(
            Q(no_kk__icontains=search) |
            Q(penduduk_set__nama_lgkp__icontains=search)
        ).distinct()

    # Pagination seperti penduduk_list
    paginator = Paginator(kks, 100)  # 100 per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'kependudukan/kk_list.html', {
        'kks': page_obj,   # untuk list data KK
        'search': search,
        'penduduks': page_obj  # untuk template pagination reuse (tidak masalah)
    })


@login_required
def kk_export_xlsx(request):
    kks = KartuKeluarga.objects.all().prefetch_related('penduduk_set')

    # Siapkan data
    data = tablib.Dataset()
    data.headers = ['No KK', 'Kepala Keluarga', 'Status', 'Alamat', 'RT', 'RW']

    for kk in kks:
        kepala = kk.penduduk_set.filter(stat_hbkel_1__icontains="Kepala Keluarga").first()
        data.append([
            kk.no_kk,
            kepala.nama_lgkp if kepala else '',
            kepala.stat_hbkel_1 if kepala else '',
            kepala.alamat if kepala else '',
            kk.no_rt,
            kk.no_rw,
        ])

    response = HttpResponse(data.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="kartu_keluarga.xlsx"'
    return response



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

from django.shortcuts import render, get_object_or_404, redirect
from .models import Penduduk
from .forms import PendudukForm
from django.contrib.auth.decorators import login_required

@login_required
def penduduk_edit(request, pk):
    penduduk = get_object_or_404(Penduduk, pk=pk)
    if request.method == "POST":
        form = PendudukForm(request.POST, instance=penduduk)
        if form.is_valid():
            form.save()
            return redirect('penduduk_list')
    else:
        form = PendudukForm(instance=penduduk)
    return render(request, 'kependudukan/penduduk_form.html', {'form': form})



@login_required
def penduduk_list(request):
    search = request.GET.get('q', '')
    penduduks = Penduduk.objects.select_related('no_kk').order_by('-id')  # terbaru di atas

    if search:
        penduduks = penduduks.filter(
            Q(nik__icontains=search) | Q(nama_lgkp__icontains=search)
        )

    # Pagination 100 per halaman
    paginator = Paginator(penduduks, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'kependudukan/penduduk_list.html', {
        'penduduks': page_obj,
        'search': search
    })


@login_required
def penduduk_export_xlsx(request):
    penduduks = Penduduk.objects.select_related('no_kk').order_by('-id')

    dataset = Dataset()
    dataset.headers = ['NIK', 'Nama', 'Jenis Kelamin', 'No KK', 'Hubungan', 'Alamat', 'RT', 'RW']

    for p in penduduks:
        dataset.append([
            p.nik,
            p.nama_lgkp,
            p.get_jenis_klmin_display(),
            p.no_kk.no_kk if p.no_kk else '',
            p.stat_hbkel_1,
            p.alamat,
            p.no_rt,
            p.no_rw
        ])

    response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="penduduk.xlsx"'
    return response

@login_required
def penduduk_detail(request, pk):
    penduduk = get_object_or_404(Penduduk, pk=pk)
    return render(request, 'kependudukan/penduduk_detail.html', {'penduduk': penduduk})