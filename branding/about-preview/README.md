# Pratinjau desain Settings About

Buka [index.html](index.html) untuk melihat kedua tema dan mencoba ukuran teks
100–200%. [preview-light-dark.png](preview-light-dark.png) adalah render HTML
dengan ukuran teks normal. Ini **bukan screenshot dari perangkat atau emulator**.
Seluruh model, versi, kapasitas, nama hardware dan clock pada pratinjau adalah
contoh, bukan spesifikasi yang ditanam dalam ROM. Parameter `?scale=2` membuka
pratinjau langsung pada ukuran teks 200%.

Implementasi asli berada di Settings `res/layout/nasgor_about_header.xml`,
`res/drawable/nasgor_about_*`, warna `res/values*/nasgor_about.xml`, serta
`NasgorAboutHeaderPreference.java` dan `NasgorHardwareInfo.java`. PNG 768×480 tampil 104×65 dp dengan
`fitCenter`. Data aplikasi dibaca dari perangkat; tidak ada angka contoh di
layout atau kode produksi.

Header yang sama dipakai pada About phone, versi OS (termasuk Catalyst), dan
About Nasgor OS. Enam kartu berikon menampilkan RAM, internal, CPU, GPU, zRAM,
dan Android, diikuti kartu kernel selebar panel. RAM/internal punya indikator
persentase terpakai dan kapasitas tersedia. Label/detail 12 sp, nilai 18 sp,
kernel 13 sp; semuanya mengikuti pengaturan ukuran teks sistem.
Di Android, kartu metrik disusun vertikal jika window kurang
dari 320 dp atau font scale minimal 1,3. Tinggi teks tetap mengikuti isi tanpa
ellipsis atau pemaksaan ukuran font. Layout tidak memiliki animasi atau polling.
Logo dan nama juga disusun vertikal pada ukuran tersebut agar nama ROM tetap
terbaca. Badge maintainer berikon di kartu utama membaca `ro.nasgoros.maintainer`
(fallback overlay maintainer, lalu tidak diketahui). Contoh nama pada preview
tidak dipakai sebagai fallback dalam aplikasi.

Snapshot dibaca sekali di background ketika header terpasang. Internal adalah
kapasitas filesystem `/data`, bukan kapasitas flash yang diiklankan. CPU menghitung
core yang tersedia di sysfs, termasuk yang offline, dan membaca clock maksimum;
fallback jumlah core mengikuti CPU yang tersedia bagi proses. GPU memakai renderer
EGL dan clock dari node Hz KGSL/devfreq jika dapat dibaca. Clock bukan pengukur
realtime. zRAM memisahkan kapasitas virtual `disksize` dari RAM fisik `mm_stat`,
dan membaca status aktif dari `/proc/swaps`. Kernel memakai `uname().release`.
Nilai yang tidak dapat dibaca ditandai tidak diketahui/tidak tersedia.

Pratinjau HTML menggunakan logo dan warna sumber saat perubahan ini dibuat.
Font, jarak teks dan latar Settings sesungguhnya masih dapat berbeda karena
tema sistem. Periksa ukuran window 320/360 dp, font besar, RTL, tema terang/gelap
serta ketiga entry About ketika build perangkat sudah diizinkan.
