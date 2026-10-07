# Boot animation Nasgor OS

Logo nasi goreng 2D dengan telur, mentimun, dan cabai; tulisan **Nasgor OS** di
bawahnya. Latar hitam, uap naik perlahan, dan loading oranye–kuning bergerak
bolak-balik. Logo dibuat sebagai vektor asli di `logo.svg` (Apache-2.0).

- `bootanimation.zip`: aset boot Android; **bukan ZIP untuk di-flash melalui recovery**.
- `preview/preview.html`: buka di browser untuk pratinjau dengan proporsi merlinx.
- `preview/preview.gif`: intro, dua putaran loading, dan simulasi fade-out.
- `preview/preview.png`: gambar diam dari frame ZIP.
- `preview/preview-phone.png`: komposisi pada layar 1080×2340, diperkecil 50%.
- `generate.py`: generator ZIP dan pratinjau dari SVG yang sama.

## Playback Android

Kanvas 1080×1080 diposisikan di tengah layar, 30 fps. Ukuran ini untuk target
merlinx dengan lebar layar 1080 piksel; tinggi layar sisanya tetap hitam.

1. `part0`: intro 36 frame (1,2 detik), logo dan tulisan muncul bertahap.
2. `part1`: loop 72 frame (2,4 detik), berulang sampai Android selesai boot.
3. Tipe `f` meminta Android memudarkan animasi selama 12 frame (0,4 detik)
   dari posisi loop saat itu. Tidak perlu menunggu satu putaran loading selesai.

Loading bersifat dekoratif, tanpa persentase progres. GIF hanya pratinjau 15 fps;
PNG di dalam ZIP berjalan pada 30 fps. Lihat implementasi format di
`frameworks/base/cmds/bootanimation/FORMAT.md` dan `BootAnimation.cpp`.

Semua entri ZIP memakai **STORE**, berisi PNG RGB tanpa alpha. `trim.txt`
menempatkan frame 500×620 pada posisi `+290+200` di kanvas, mengurangi area
tekstur sekitar 73% dibanding menyimpan seluruh kanvas. Warna PNG tetap RGB
agar warna logo dan gradasi tidak berubah antarframe.

## Membuat ulang

Dari root workspace yang memiliki folder `src/` dan `repos/`:

```bash
python3 -m venv /tmp/nasgor-bootanimation-venv
/tmp/nasgor-bootanimation-venv/bin/python -m pip install \
  -r repos/android_vendor_nasgoros/bootanimation/requirements.txt
/tmp/nasgor-bootanimation-venv/bin/python \
  repos/android_vendor_nasgoros/bootanimation/generate.py \
  src/external/google-fonts/rubik/Rubik-Medium.ttf \
  repos/android_vendor_nasgoros/bootanimation/bootanimation.zip \
  --preview-dir repos/android_vendor_nasgoros/bootanimation/preview
```

CairoSVG membutuhkan library Cairo di host (`libcairo2` pada Debian/Ubuntu).
Font rilis memakai Rubik Medium yang sudah tersedia di source AOSP, berlisensi
OFL di `external/google-fonts/rubik/LICENSE`. Font tidak perlu dipasang pada HP;
tulisan sudah menjadi bagian dari setiap PNG.

Metadata ZIP dibuat tetap sehingga input dan lingkungan render yang sama
menghasilkan ZIP identik. Pratinjau membaca kembali PNG dari ZIP yang dihasilkan.

## Integrasi ROM

`config/features/bootanimation.mk` sudah menetapkan:

```make
TARGET_BOOTANIMATION := vendor/nasgoros/bootanimation/bootanimation.zip
```

Perubahan dikerjakan di clone `repos/android_vendor_nasgoros`. Setelah perubahan
masuk repository ROM, sinkronkan `src/vendor/nasgoros` melalui workflow biasa
sebelum build ROM berikutnya. Generasi ZIP tidak memperbarui source tree `src/`
atau ROM yang sudah terpasang. Validasi format dan pratinjau tidak menggantikan
uji boot pada perangkat.
