# Pilihan aplikasi minimal nasgorOS

Pengguna memilih profil minimal dan meminta **Lineage Setup Wizard dihapus**.
Daftar paket berada di `Android.mk`; produk mengaktifkannya melalui
`config/features/minimal-apps.mk`. Ini mengeluarkan aplikasi dari image ROM,
bukan menghapus repository atau menonaktifkan aplikasi lewat ADB saat boot.

## Aplikasi yang dikeluarkan

| Kelompok | Modul | Dampak |
|---|---|---|
| Setup awal | `LineageSetupWizard` | Boot pertama memakai provisioning AOSP singkat lalu menuju launcher; bahasa, Wi-Fi, akun dan kunci layar diatur melalui Settings |
| Backup tambahan | `Seedvault`, `LocalContactsBackup` | Tidak ada UI backup/restore Seedvault; API backup Android dan provider kontak tetap ada |
| Equalizer tambahan | `AudioFX`, `MusicFX` | Tidak ada aplikasi equalizer bawaan; audio HAL, codec dan efek yang dipakai sistem tetap ada |
| Radio FM | `FMRadio`, `FmRecordingsProvider` | Tidak ada aplikasi FM atau rekaman FM bawaan; layanan modem/telepon dipertahankan |
| Printer tambahan | `BuiltInPrintService`, `PrintRecommendationService` | Tidak ada plugin printer/rekomendasi printer bawaan; `PrintSpooler` tetap ada untuk Save as PDF dan plugin yang dipasang pengguna |
| Screensaver dan hiburan | `BasicDreams`, `PhotoTable`, `EasterEgg` | Screensaver tambahan dan aplikasi easter egg tidak disertakan; wallpaper serta AOD crDroid tetap ada |
| Diagnostik pengembang opsional | `Traceur` | Aplikasi System Tracing tidak disertakan, termasuk pada build eng |
| Browser ringan | `LoraBrowserLite` | Browser bawaan NasgorOS; `Jelly` tetap dikeluarkan |
| Penghapusan sebelumnya | `Jelly`, `ExactCalculator`, `Etar`, `DeskClock`, `Glimpse`, `Gallery2`, `messaging`, `Twelve`, `Recorder` | Jelly, kalkulator, kalender, jam/alarm, galeri, SMS, musik dan perekam tersebut tetap dikeluarkan; Lora Browser Lite disertakan sebagai browser |

Kamera `Aperture`, file manager `Camelot` dan file picker `DocumentsUI` tetap ada.
Launcher, keyboard, WebView/HTMLViewer, telepon/IMS, kontak, provider SMS/MMS,
emergency alert, izin, pemasang APK, jaringan, updater dan aksesibilitas tetap
dipertahankan. HTMLViewer diperlukan halaman lisensi Settings; WebView diperlukan
banyak aplikasi. Jangan menghapusnya hanya karena ukuran APK-nya besar.

Penyedia fitur crDroid yang disertakan: GameSpace, OmniStyle, QuickLook, ThemeStore
dan sidebar. **Sandbox/AppLocker** (Axion) dan **cuaca** (OmniJaws) dihapus bersih
atas permintaan user (2026-10-07): aplikasi, repo manifest, dan kode di framework,
SystemUI, crDroid Settings, QuickLook, `vendor/addons` dan sepolicy. App Lock bawaan
AOSP/Android 17 tetap ada. Lihat bagian "Removed crDroid features" di `FEATURES.md`.

## Boot tanpa wizard

Boot pertama memakai aplikasi **Provision AOSP asli** (modul `Provision` dari
`packages/apps/Provision`, dipasang lewat `handheld_system_ext.mk`) di
`/system_ext/priv-app/Provision/Provision.apk`. Kode AOSP menandai
`DEVICE_PROVISIONED=1` dan `USER_SETUP_COMPLETE=1`, lalu menonaktifkan activity-nya
untuk pengguna tersebut. Tidak ada service pemantau atau wizard baru.

LineageSetupWizard mendeklarasikan `overrides: ["Provision"]`, yang tetap menyingkirkan
Provision walaupun wizard itu sendiri di-override. Karena itu
`nasgoros/android_packages_apps_SetupWizard` (branch `17.0`) adalah fork LineageOS yang
**hanya menghapus baris override itu**. Salinan berganti nama (`NasgorProvision` dengan
`stem: "Provision"`) tidak dipakai lagi: Kati menolaknya karena nama modul `Provision` ganda.

Nama folder harus tetap `Provision`: installer GApps (termasuk LiteGapps) menghapus
`Provision` berdasarkan nama folder saat memasang setup wizard Google. Dengan nama folder
lain aplikasi ini tidak terhapus dan Pixel Setup Wizard *force close* (dikonfirmasi user
2026-10-07).

Jangan mengganti mekanisme ini dengan perintah `settings put` yang berjalan pada
setiap boot, atau menghapus layanan provisioning/backup inti. Saat pengujian nanti,
periksa clean flash, pengguna kedua, reboot, setup kunci layar, notifikasi, Quick
Settings dan navigasi. LiteGapps tetap terpisah; uji pemasangan paket tersebut pada
ROM tanpa wizard ini, termasuk penambahan akun lewat Settings.

## Mengembalikan aplikasi dan port Android berikutnya

Hapus nama modul dari `LOCAL_OVERRIDES_PACKAGES` untuk mengembalikannya; base ROM
juga harus memilih modul itu. Pasangan radio dan backup dikembalikan bersama.
Tanpa Seedvault, overlay `def_backup_transport` memakai default AOSP
(`com.android.localtransport/.LocalTransport`), bukan nilai kosong, karena setup
wizard Google membaca transport aktif saat restore. Jika Seedvault dipulihkan, lepas
overlay tersebut atau pilih transport melalui pengaturan backup. Jika wizard dipulihkan, kembalikan `overrides: ["Provision"]` di fork SetupWizard
(atau pakai repo LineageOS lagi); jangan memasang dua pemilik setup.

Saat pindah Android/ROM, cocokkan ulang nama modul, periksa dependensi `required`
dan override transitif, lalu periksa kembali implementasi AOSP Provision. Detail
umum ada di [PORTING.md](../PORTING.md).

Perubahan ini belum dikompilasi atau diuji di HP. Menghapus APK mengurangi aplikasi
yang disertakan, tetapi penghematan RAM, waktu boot dan peningkatan FPS harus
diukur di perangkat; ukuran APK bukan ukuran penggunaan RAM.

## Browser bawaan NasgorOS

`LoraBrowserLite` dari rilis upstream v1.5.4 dipasang sebagai aplikasi biasa di
partisi product. APK tetap memakai tanda tangan upstream dan dapat diperbarui
normal. Untuk mengecualikannya, set `NASGOROS_WITH_LORA_BROWSER=false` sebelum
produk diwarisi. Sumber, hash dan langkah pembaruan ada di
[apps/LoraBrowserLite/README.md](../apps/LoraBrowserLite/README.md).
