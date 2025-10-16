from kependudukan.models import Penduduk, KartuKeluarga

total = Penduduk.objects.count()
print(f"Mulai memproses {total} penduduk...")

created_count = 0
linked_count = 0
errors = 0

for i, p in enumerate(Penduduk.objects.all(), start=1):
    try:
        if not p.no_kk:
            print(f"[{i}/{total}] ⚠️ Penduduk tanpa no_kk: {p.nama_lgkp}")
            continue

        kk_obj, created = KartuKeluarga.objects.get_or_create(no_kk=p.no_kk)
        if created:
            created_count += 1
            print(f"[{i}/{total}] 🆕 KK baru dibuat: {kk_obj.no_kk}")

        # Hubungkan penduduk ke KK
        p.kk = kk_obj
        p.save(update_fields=['kk'])
        linked_count += 1

        if i % 50 == 0:
            print(f"✅ {i}/{total} data selesai...")

    except Exception as e:
        print(f"[{i}/{total}] ❌ Error: {e}")
        errors += 1

print("\nSelesai.")
print(f"Total Penduduk: {total}")
print(f"KK baru dibuat: {created_count}")
print(f"Penduduk terhubung ke KK: {linked_count}")
print(f"Error: {errors}")
