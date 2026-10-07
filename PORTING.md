# Catatan porting fitur nasgorOS

Basis saat ini: **Android 17 / LineageOS 24.0**. Catatan ini menjelaskan cara
membawa fitur ke Android 18 atau ROM lain; bukan pernyataan bahwa port Android 18
sudah dibuat atau diuji. Jangan mengubah branch `17.0` untuk mengejar Android 18.

## Letak fitur dan batas dependensi

| Fitur | Sumber yang dibawa | Integrasi produk | Ketergantungan / risiko |
|---|---|---|---|
| Boot animasi nasi goreng 2D | `bootanimation/` termasuk generator, SVG, ZIP dan preview | `config/features/bootanimation.mk` | Rendah; format ZIP Android dan mekanisme pemasangan bootanimation milik ROM tujuan |
| Wallpaper Senja | `wallpapers/` | `config/features/wallpaper.mk` | Rendah; WallpaperManager, lokasi `/product/etc/wallpapers`, properti `ro.config.wallpaper` |
| Info FPS/CPU/GPU/RAM dan overlay | repo `android_packages_apps_NasgorSettings`, folder `performance/`, manifest, resource dan allowlist | `config/features/settings.mk` | Sedang; API platform FPS/task/window, SettingsLib, platform signing dan izin privileged |
| Hub pengaturan sistem tambahan | repo NasgorSettings, `LineagePartsTiles` dan XML hub | modul Settings yang sama | Sedang; membutuhkan `LineageParts` dan `LineagePreferenceLib` |
| Profil aplikasi minimal + boot tanpa wizard | `removed-packages/`, `apps/Provision/`, `overlay/minimal/` | `config/features/minimal-apps.mk` | Rendah–sedang; override modul AOSP Provision, allowlist, default backup dan penyelesaian setup tiap pengguna |
| UI About | Settings `NasgorAboutHeaderPreference`, layout, palette terang/gelap; crDroid `NasgorAbout` | patch Settings dan crDroid Settings | Sedang; periksa XML dan binding Catalyst, jangan menghapus controller/info legal bawaan |
| Seluruh kustomisasi crDroid Settings | manifest terpisah, `ports/crdroid/sources.lock.json`, `patches/` | `config/crdroid.mk`, `overlay/crdroid/` | Tinggi; versi Settings, framework, SystemUI, SDK, native, sepolicy dan penyedia fitur harus cocok |

Info FPS berada di aplikasi sendiri. `TaskFpsMonitor` mengelola callback FPS,
`PerformanceFragment` berisi satu sakelar, `FpsSettings` menyimpan status dan posisi,
dan `FpsOverlayService` menampilkan penghitung yang bisa digeser tanpa notifikasi
(service biasa; aplikasi masuk `allow-in-power-save` lewat sysconfig). Saat port,
pastikan sysconfig itu ikut terpasang. Tidak ada perintah root atau service crDroid. App secara keseluruhan masih memakai library Lineage untuk hub lama;
menyalin APK ke ROM lain tidak cukup untuk melakukan port.

FPS berasal dari frame aplikasi aktif. Hz layar tetap data terpisah. Jika
`/proc/stat`, sysfs atau driver tidak memberikan data, tampilkan tidak tersedia.
Jangan menambahkan izin SELinux luas atau angka perkiraan agar indikator terlihat
berfungsi. Info GPU saat ini berisi renderer, vendor dan OpenGL ES, bukan beban GPU.

## Profil minimal dan halaman About

Pilihan terbaru menghapus aplikasi tambahan termasuk Seedvault, AudioFX dan
Lineage Setup Wizard. Detail dan cara mengembalikannya ada di
[removed-packages/README.md](removed-packages/README.md). `NasgorProvision` memakai
AOSP Provision untuk menandai setup selesai lalu menonaktifkan activity-nya.
Periksa ulang perilaku per-user dan override transitif saat ganti base Android.
Layanan backup inti, kamera, file picker, WebView dan provider crDroid tetap ada.

UI About memakai satu `NasgorAboutHeaderPreference` untuk About phone, versi
firmware dan tab About NasgorOS. Angka OS/model/chipset/RAM dibaca dari perangkat,
warna tersedia di `values` serta `values-night`, dan tidak ada polling atau gambar
bitmap besar. Logo piring memakai PNG transparan 512×320 dari
`branding/logo/generate.py`, ditampilkan 128×80 dp dengan `fitCenter`; sumbernya
SVG yang sama dengan boot animasi. Pastikan `drawable-nodpi/nasgor_about_mark.png`
terbawa pada patch, tanpa drawable vektor lama dengan nama yang sama.
`LogoPreference.kt` menyediakan binding Catalyst agar tampilan baru
juga dipakai ketika layar firmware tidak lagi membaca XML. Key controller bawaan,
IMEI, detail keamanan, build-number/developer options dan halaman legal dipertahankan.
Saat upgrade, uji ukuran font besar, layar kecil, mode malam, dan jalur pencarian.

## Memilih modul

`config/features.mk` menjadi pintu masuk fitur. Set nilai berikut **sebelum**
produk meng-inherit `vendor/nasgoros/product.mk`:

```make
NASGOROS_WITH_BOOTANIMATION := true
NASGOROS_WITH_WALLPAPER := true
NASGOROS_WITH_SETTINGS := true
NASGOROS_WITH_CRDROID_SETTINGS := true
NASGOROS_WITH_LORA_BROWSER := true
NASGOROS_WITH_ZIMUX := true
```

Default keenamnya `true`. Kustomisasi crDroid membutuhkan aplikasi NasgorSettings;
kombinasi crDroid aktif dan Settings nonaktif ditolak oleh konfigurasi. ROM lain
juga dapat meng-inherit satu `config/features/*.mk` langsung tanpa membawa
branding, daftar aplikasi yang dihapus, atau target rilis nasgorOS.

`NASGOROS_WITH_CRDROID_SETTINGS=false` hanya melepas konfigurasi produk crDroid.
Flag ini **tidak** mengembalikan framework/SystemUI yang sudah diganti. Untuk
profil dasar tanpa port crDroid, gunakan checkout terpisah, hilangkan include
`snippets/nasgor-crdroid.xml` dari `snippets/nasgoros.xml`, lalu sinkronkan manifest
dasar. Jangan menerapkan seri patch crDroid pada profil dasar. Jangan mencampur
output build dua profil; gunakan output directory yang berbeda.

## Alur pindah ke Android 18

1. Buat branch `18.0` untuk repo nasgorOS dan manifest dasar Android 18. Simpan
   branch `17.0`, lockfile dan patch lamanya untuk pemeliharaan Android 17.
2. Mulai di checkout terpisah dari baseline ROM tujuan yang bisa dibangun.
   Port bootanimation dan wallpaper lebih dahulu. Sesuaikan `TARGET_BOOTANIMATION`
   bila ROM tersebut memasang ZIP dengan modul atau `PRODUCT_COPY_FILES`; pastikan
   hanya satu mekanisme memasang bootanimation ke tujuan yang sama. Periksa juga
   agar ROM tujuan tidak menetapkan `ro.config.wallpaper` dua kali.
3. Bawa repo NasgorSettings. Periksa API `WindowManager.registerTaskFpsCallback`,
   `TaskFpsCallback`, `ActivityManager.getRunningTasks`, tipe jendela overlay,
   foreground service dan aturan notifikasi pada **source Android tujuan**.
   Cocokkan SettingsLib, tema, permission allowlist, platform signing dan partisi
   `system_ext`. Jika ROM tidak memiliki LineageParts/SDK, pisahkan hub tersebut
   beserta library-nya; pertahankan activity monitor dan kontrak intent di bawah.
4. Untuk crDroid, pilih revisi upstream yang cocok dengan Android 18. Perbarui
   `sources.lock.json` dan manifest bersamaan: SHA, branch, path dan alasan
   dependensi. Jangan memakai SHA framework Android 17 bersama Settings Android
   18, dan jangan mengganti semua nomor branch secara otomatis: resource aplikasi
   pada port Android 17 ini memang memakai branch upstream `16.0`.
5. Terapkan ulang **maksud** setiap patch kecil pada baseline baru. Jika upstream
   sudah memiliki perbaikan yang sama, hapus patch dan entri `series.json` yang
   tidak diperlukan. Jangan memaksa patch yang konflik atau mengganti file besar
   dengan salinan dari Android 17. Pertahankan copyright dan lisensi upstream.
6. Perbarui inventaris preference, nama paket di `config/crdroid.mk`, overlay
   branding, dependensi runtime, dan pengecualian modul bootanimation/font.
   Paket provider diperlukan agar opsi Settings mempunyai implementasi nyata.
7. Jalankan pemeriksaan statis di bawah. Setelah kompilasi diizinkan, bangun
   komponen, kemudian ROM lengkap. Uji boot dan fitur pada perangkat sebelum rilis.

Untuk merlinx, pertahankan `TARGET_2ND_ARCH := arm` dan kompatibilitas kernel
32-bit: binary vendor MediaTek tetap membutuhkannya. nasgorOS tetap vanilla;
LiteGapps dipasang terpisah. Jangan meng-inherit seluruh produk crDroid/addons
hanya untuk memperbaiki satu dependensi fitur.

## Kontrak yang harus dipertahankan

- Entry Settings: `com.nasgoros.settings.NasgorSettingsActivity`.
- Monitor: `com.nasgoros.settings.performance.PerformanceActivity`.
- Hub tambahan: boolean intent extra `com.nasgoros.settings.SYSTEM_SETTINGS=true`.
- `ro.nasgoros.crdroid_settings=true` memilih host crDroid dari entry NasgorOS.
  Ini memilih navigasi UI, bukan sakelar untuk menghapus seluruh backend.
- `ro.nasgoros.version` dan `ro.nasgoros.display.version` untuk versi sendiri;
  jangan menimpa `ro.lineage.*`.
- Service overlay hanya berjalan setelah pengguna menyalakannya. Hentikan
  sampling/callback ketika layar mati atau terkunci; sediakan tombol Hentikan.

## Catatan seri patch Android 17

| Patch | Tujuan | Titik pemeriksaan saat upgrade |
|---|---|---|
| `packages_apps_crDroidSettings/0001-*` | Tab performa, About NasgorOS, akses hub tambahan, satu entry homepage | Fragment, resource, tab pager dan controller homepage |
| `packages_apps_Settings/0001-*` | Versi NasgorOS, nonaktifkan pengingat donasi/lookup maintainer crDroid | Manifest receiver dan controller About phone |
| `vendor_addons/0001-*` | Hindari modul bootanimation ganda | Modul yang sudah disediakan base ROM |
| `packages_overlays_Lineage/0001-*` | Pakai definisi font addons tanpa modul duplikat | Tiga overlay font dan `fonts_customization.xml`; tetap pertahankan LineageBlackTheme |

Patch disimpan terpisah dari repo upstream. `patches/apply.py` memeriksa semua
SHA dan konflik sebelum menulis, melewati patch yang sudah diterapkan, dan
`--verify` tidak menulis source. `patches/apply.sh` adalah pembungkusnya.

## Pemeriksaan tanpa kompilasi

Dari workspace pengembangan yang memiliki full clone di `repos/`:

```bash
python3 repos/android_vendor_nasgoros/patches/apply.py --clones repos --verify
python3 repos/android_vendor_nasgoros/tools/check-crdroid-port.py \
  --clones repos --manifest repos/android
```

Pemeriksaan mencakup pin manifest, XML, tujuan intent, definisi paket produk,
dan reproduksi patch pada salinan sementara. Ini tidak menggantikan Soong,
kompilasi, pemeriksaan SELinux, atau uji HP. Setelah sumber masuk ke source tree,
ikuti alur aplikasi patch di [ports/crdroid/README.md](ports/crdroid/README.md).

Uji perangkat setelah upgrade: navigasi seluruh tab, fitur sesuai hardware,
FPS saat berpindah aplikasi, CPU/GPU yang tidak terbaca, overlay saat kunci layar,
aksi Hentikan, reboot, bootanimation, wallpaper, dan kompatibilitas LiteGapps.

## Menambah fitur berikutnya

Utamakan asset/overlay (tingkat 1), lalu aplikasi sendiri (tingkat 2). Gunakan
patch framework (tingkat 3) hanya jika diperlukan. Buat modul konfigurasi sendiri,
catat flag, dependensi, file, risiko konflik dan cara verifikasi di `FEATURES.md`.
Untuk patch upstream, simpan perubahan sekecil mungkin, catat SHA sumber dan
perbarui `series.json`. Jangan menggabungkan fitur baru dengan edit kosmetik besar
yang membuat port berikutnya sulit ditinjau.


### Default performa dan efek visual

Modul ini memakai overlay produk untuk default skala animasi 0,5× dan blur
nonaktif, serta nilai framework agar screensaver tidak berjalan otomatis. Patch framework-nya terdaftar
di `patches/series.json`; terapkan sesudah sync dengan `patches/apply.py`. Default
crDroid untuk Pulse ambient juga nonaktif, sedangkan Pulse visualizer pada trek
sudah memakai default nonaktif (cuaca OmniJaws dihapus). Kontrol tetap tersedia agar
pengguna dapat menyalakan fitur. Wallpaper live tetap dapat dipilih, hanya tidak
dipaksa menjadi wallpaper bawaan. Default SettingsProvider tidak menimpa setelan
yang sudah ada saat upgrade.

### Aplikasi APK bawaan

Lora Browser Lite dan Zimux berada di `apps/` dengan flag produk masing-masing.
Pertahankan APK bertanda tangan upstream tanpa repacking. Untuk system app,
library native yang memerlukan ekstraksi harus dipasang oleh build: aturan
`Android.mk` memilih ABI utama dan menyalin library ke direktori di samping APK.
Saat port Android 18, periksa kembali aturan Make prebuilt, path library, SDK
aplikasi, dan pembaruan APK dengan signature yang sama. Detail versi/checksum dan
pembaruan Zimux ada di [apps/Zimux/README.md](apps/Zimux/README.md).
