# Pratinjau desain Settings About

Buka [index.html](index.html) untuk melihat kedua tema dan mencoba ukuran teks
100–200%. [preview-light-dark.png](preview-light-dark.png) adalah render HTML
dengan ukuran teks normal. Ini **bukan screenshot dari perangkat atau emulator**.
Model, versi ROM, chipset, Android, dan RAM pada pratinjau adalah contoh.

Implementasi asli berada di Settings `res/layout/nasgor_about_header.xml`,
`res/drawable/nasgor_about_*`, warna `res/values*/nasgor_about.xml`, serta
`NasgorAboutHeaderPreference.java`. PNG 768×480 tampil 192×120 dp dengan
`fitCenter`. Data aplikasi dibaca dari perangkat; tidak ada angka contoh di
layout atau kode produksi.

Header yang sama dipakai pada About phone, versi OS (termasuk Catalyst), dan
About Nasgor OS. Di Android, kartu metrik disusun vertikal jika window kurang
dari 360 dp atau font scale minimal 1,3. Tinggi teks tetap mengikuti isi tanpa
ellipsis atau pemaksaan ukuran font. Layout tidak memiliki animasi atau polling.

Pratinjau HTML menggunakan logo dan warna sumber saat perubahan ini dibuat.
Font, jarak teks dan latar Settings sesungguhnya masih dapat berbeda karena
tema sistem. Periksa ukuran window 320/360 dp, font besar, RTL, tema terang/gelap
serta ketiga entry About ketika build perangkat sudah diizinkan.
