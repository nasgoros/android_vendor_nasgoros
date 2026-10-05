# Senja — wallpaper nasgorOS

Wallpaper abstrak untuk launcher utama: lipatan biru arang dengan aksen amber
yang selaras dengan warna boot animation nasgorOS. Komposisi atas dibuat tenang
untuk jam dan widget, sementara lipatan utama berada di bagian bawah.

Satu palet yang dirancang untuk pemakaian siang dan malam; ini wallpaper statis,
bukan gambar yang berganti otomatis mengikuti tema atau waktu.

## Aset

- [`nasgor-senja.png`](nasgor-senja.png): PNG RGB, 853×1844 piksel, resolusi asli
  keluaran imagegen. Proporsinya mendekati layar merlinx 1080×2340; Android
  menyesuaikan ukuran dan crop saat wallpaper diterapkan.
- [`PROMPT.md`](PROMPT.md): prompt lengkap dan metode pembuatan.

Dibuat menggunakan tool imagegen bawaan. File PNG disalin utuh ke proyek tanpa
perubahan visual; tidak memerlukan koneksi internet atau tool AI di perangkat.

## Integrasi launcher

`config/features/wallpaper.mk` menyalin aset ke
`/product/etc/wallpapers/nasgor-senja.png` dan menetapkan `ro.config.wallpaper`
ke lokasi tersebut. `WallpaperManager.openRawDefaultWallpaper()` di source
Android membaca properti ini sebelum resource wallpaper bawaan.

Konfigurasi ini menetapkan gambar default sistem; wallpaper yang sudah dipilih
pengguna tidak dipaksa berubah. Wallpaper lock screen dapat mengikuti wallpaper
utama jika pengguna belum menetapkan gambar terpisah.

Perubahan berada di clone `repos/android_vendor_nasgoros`. Gunakan workflow
sinkronisasi biasa ke `src/vendor/nasgoros` sebelum build ROM berikutnya.
Integrasi belum diuji dengan build penuh atau pada HP.

## Memasang sekarang

Salin `nasgor-senja.png` ke HP, buka pemilih wallpaper dari launcher atau
Pengaturan, pilih gambar ini, lalu terapkan pada **Layar utama**.
Tidak perlu menunggu build ROM untuk memakai gambar secara manual.
