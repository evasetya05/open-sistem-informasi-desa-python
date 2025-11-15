from django.shortcuts import render, redirect
from apps.layanan.models import Antrian, AntrianSession
from apps.layanan.forms import DaftarAntrianForm
from django.utils import timezone
from django.contrib import messages
from django.views.generic import DetailView
from apps.layanan.models import Antrian
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



def daftar_antrian(request, session_id=None):
    if session_id:
        session = get_object_or_404(AntrianSession, id=session_id)
    else:
        session = AntrianSession.objects.filter(aktif=True, tanggal=timezone.localdate()).first()

    if not session:
        messages.warning(request, "Antrian belum dibuka hari ini.")
        return render(request, "antrian/tutup.html")

    if request.method == 'POST':
        form = DaftarAntrianForm(request.POST)
        if form.is_valid():
            antrian = form.save(commit=False)
            antrian.session = session
            antrian.nomor = Antrian.objects.filter(session=session).count() + 1
            antrian.save()
            return redirect('lihat_nomor', pk=antrian.pk)
        else:
            messages.error(request, "Formulir tidak valid. Silakan periksa kembali.")
    else:
        form = DaftarAntrianForm()

    return render(request, 'antrian/daftar.html', {
        'form': form,
        'session': session
    })



@login_required
def panggil_antrian(request):
    semua_sesi = AntrianSession.objects.order_by('-tanggal')  # untuk dropdown
    session_id = request.GET.get('session_id')

    # Gunakan session dari parameter jika ada, kalau tidak pakai default: aktif hari ini
    if session_id:
        session = get_object_or_404(AntrianSession, id=session_id)
    else:
        session = AntrianSession.objects.filter(aktif=True, tanggal=timezone.localdate()).first()

    if not session:
        messages.warning(request, "Tidak ada sesi antrian aktif.")
        return render(request, "antrian/tutup.html")

    antrian = Antrian.objects.filter(session=session, sudah_dipanggil=False).order_by('nomor').first()

    if request.method == 'POST' and antrian:
        antrian.sudah_dipanggil = True
        antrian.save()
        messages.success(request, f"Memanggil nomor {antrian.nomor} - {antrian.nama}")
        return redirect(f"{request.path}?session_id={session.id}")

    if not antrian:
        messages.info(request, "Semua antrian sudah dipanggil.")

    context = {
        'semua_sesi': semua_sesi,
        'session': session,
        'antrian': antrian,
    }
    return render(request, "antrian/panggil.html", context)


class AntrianDetailView(DetailView):
    model = Antrian
    template_name = 'antrian/detail.html'

def lihat_nomor(request, pk):
    antrian = get_object_or_404(Antrian, pk=pk)
    return render(request, 'antrian/nomor.html', {'antrian': antrian})


@login_required
def buat_kegiatan_antrian(request):
    all_sessions = AntrianSession.objects.all().order_by('-tanggal')

    for session in all_sessions:
        session.full_url = request.build_absolute_uri(
            reverse('daftar_antrian_dengan_session', args=[session.id])
        )

    if request.method == 'POST':
        kegiatan = request.POST.get('kegiatan')
        tanggal = timezone.localdate()

        session = AntrianSession.objects.create(
            tanggal=tanggal,
            aktif=True,
            kegiatan=kegiatan
        )

        session.full_url = request.build_absolute_uri(
            reverse('daftar_antrian_dengan_session', args=[session.id])
        )

        return render(request, 'antrian/buat_kegiatan.html', {
            'session': session,
            'full_url': session.full_url,
            'all_sessions': all_sessions
        })

    return render(request, 'antrian/buat_kegiatan.html', {
        'all_sessions': all_sessions
    })

@login_required
def riwayat_antrian(request):
    sessions = AntrianSession.objects.order_by('-tanggal')  # daftar sesi antrian
    selected_session = None
    antrian_dilayani = []

    session_id = request.GET.get('session_id')
    if session_id:
        selected_session = get_object_or_404(AntrianSession, id=session_id)
        antrian_dilayani = Antrian.objects.filter(session=selected_session, sudah_dipanggil=True)

    return render(request, 'antrian/riwayat_antrian.html', {
        'sessions': sessions,
        'selected_session': selected_session,
        'antrian_dilayani': antrian_dilayani,
    })

