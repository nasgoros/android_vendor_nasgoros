# Logo Nasgor OS

Logo aktif menggunakan ilustrasi **nasi goreng di piring datar** yang sama
persis dengan boot animasi: telur, cabai dan mentimun. Sumber yang dapat diedit
adalah `../../bootanimation/logo.svg` (Apache-2.0). Semua PNG dirender langsung
dari SVG tersebut melalui `generate.py`, sehingga bentuk dan warna konsisten.
Nama merek ketika ditulis terpisah adalah **Nasgor OS**.

| File PNG | Ukuran | Pemakaian |
|---|---|---|
| `proyek.png` | 1024×1024 | Master transparan; juga disalin ke `proyek.png` di root workspace sesuai permintaan |
| `nasgor-os-logo-transparent.png` | 1024×1024 | Salinan master untuk website dan penggunaan umum |
| `nasgor-os-avatar-dark.png` | 1024×1024 | Foto profil GitHub, SourceForge, Telegram dengan latar gelap; disalin sebagai `proyek-avatar.png` di root workspace |
| `nasgor-about-mark.png` | 768×480 | Aset ringan untuk header Settings About, ruang transparan atas/bawah dikurangi |

Pertahankan proporsi gambar. Avatar persegi juga dapat dipotong melingkar.
Master transparan tetap memiliki alpha; jangan menambahkan latar putih untuk
resource Settings karena halaman mendukung tema terang dan gelap.

## Membuat ulang

Dari root workspace, gunakan environment dengan dependensi
`bootanimation/requirements.txt`:

```bash
/tmp/nasgor-bootanimation-venv/bin/python \
  repos/android_vendor_nasgoros/branding/logo/generate.py \
  --project-copy proyek.png \
  --avatar-copy proyek-avatar.png \
  --settings-res repos/android_packages_apps_Settings/res
```

Resource Android adalah `res/drawable-nodpi/nasgor_about_mark.png`, ditampilkan
104×65 dp dengan `fitCenter` oleh `res/layout/nasgor_about_header.xml`. Tidak ada
tint atau latar pada gambar. Resource menggantikan ikon vektor huruf n lama.
Header dipakai bersama oleh About phone, halaman versi OS (XML/Catalyst), dan
About Nasgor OS di pengaturan crDroid.

Header menampilkan logo dan nama merek di tengah, badge versi, kartu perangkat,
serta kartu Android/RAM yang tersusun vertikal pada window sempit atau font besar.
Warna latar, garis tepi, teks dan badge memiliki varian siang/malam. Pratinjau
desain dengan data contoh tersedia di [About preview](../about-preview/index.html).

Perubahan resource dan layout disimpan dalam
`patches/packages_apps_Settings/0001-nasgor-branding-and-version.patch`.
Sesudah regenerasi resource, ekspor ulang patch Settings dengan `git diff HEAD
--binary` (sertakan file baru dengan intent-to-add) agar port Android berikutnya
membawa PNG yang sama. Generator aset tidak mengompilasi ROM atau memasang
perubahan ke HP. Foto profil layanan eksternal tidak diubah oleh generator.
