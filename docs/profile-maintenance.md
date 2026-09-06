# Pemeliharaan profil Rex

Repositori: [rexkarbu/rexkarbu](https://github.com/rexkarbu/rexkarbu). Konten pengunjung berada di `README.md` pada root repositori dan menggunakan bahasa Inggris.

## Mengganti banner

- `assets/rexs-night-workshop.png`: versi statis dan sumber animasi.
- `assets/rexs-night-workshop.gif`: versi dengan perubahan cahaya ringan.
- `docs/banner-prompt.md`: prompt serta asal ilustrasi original.
- `scripts/animate-banner.py`: pembuat GIF dari PNG lokal, tanpa layanan gambar.

Pertahankan ukuran sekitar 1200 × 360 piksel dan bentuk utama yang terbaca pada layar kecil. Palet aset: charcoal `#0D1117`, midnight blue `#17243A`, sage `#9DB7A5`, amber `#E5B567`, off-white `#E6EDF3`. Warna teks README mengikuti tema GitHub.

Ganti PNG, lalu sesuaikan area cahaya pada skrip dengan posisi monitor di ilustrasi baru. Dari root repositori:

```sh
python -m pip install Pillow
python scripts/animate-banner.py
```

Pillow adalah satu-satunya dependensi tambahan dan hanya diperlukan untuk membuat ulang animasi. Skrip mempertahankan PNG dan menulis ulang GIF. Tidak diperlukan dependensi untuk menampilkan profil.

Elemen `picture` menampilkan GIF secara normal dan memilih PNG saat browser meminta pengurangan animasi. Untuk memakai versi statis bagi semua pengunjung, ganti seluruh elemen `picture` dengan:

```markdown
![Rex's Night Workshop: a pixel-art desk, monitor, books, plant, and city window at night.](assets/rexs-night-workshop.png)
```

Jika nama aset berubah, perbarui `src`, `srcset`, dan dokumentasi. Gunakan path relatif dengan `/` dan kapitalisasi yang tepat. Pertahankan informasi penting sebagai teks Markdown. Jangan menambahkan CSS, JavaScript, iframe, atau layanan statistik eksternal ke README.

## Memperbarui proyek

Pilih maksimal tiga repositori **publik** berdasarkan manfaat konkret dan dokumentasi, kemudian baca README serta berkas teknologi seperti `package.json` atau `project.godot`. Atribut `private` dalam `package.json` mengatur publikasi npm; visibilitas repositori harus diperiksa terpisah di GitHub.

Untuk setiap proyek, tulis nama bertautan ke repositori, satu kalimat manfaat, dan teknologi utama. Tambahkan demo hanya setelah URL dibuka dan isinya cocok dengan proyek. Localhost, contoh konfigurasi, serta rencana peluncuran bukan demo publik.

Perbarui `Tools I Use` berdasarkan penggunaan nyata tanpa menyimpulkan tingkat keahlian. `Currently Exploring` harus didukung dokumentasi yang masih relevan atau konfirmasi Rex; hapus bagian tersebut jika tidak lagi dapat dipastikan. Jangan mengambil isi repositori private, mengarang pencapaian, atau meninggalkan placeholder.

### Dasar pilihan awal — 6 September 2026

Pencarian `user:rexkarbu is:public` menemukan repositori profil dan enam proyek. Pilihan awal:

| Proyek | Sumber deskripsi dan teknologi |
| --- | --- |
| NVL Studio | [README](https://github.com/rexkarbu/nvl-studio/blob/main/README.md): avatar, respons suara, dan OBS. [package.json](https://github.com/rexkarbu/nvl-studio/blob/main/package.json): TypeScript, React, Electron, Vite. |
| Dashboard Daily | [README](https://github.com/rexkarbu/dashboard-daily/blob/main/README.md): widget cuaca, agenda, tugas, dan catatan. [package.json](https://github.com/rexkarbu/dashboard-daily/blob/main/package.json): TypeScript, React, Electron. |
| Holuf | [README](https://github.com/rexkarbu/Holuf/blob/main/README.md): eksplorasi, dialog, quest, pertempuran, GDScript, dan fokus penyeimbangan. [project.godot](https://github.com/rexkarbu/Holuf/blob/main/project.godot): Godot 4 dan sistem game. |

Perkenalan merangkum jenis proyek tersebut. `Currently Exploring` merujuk pada sistem RPG dan penyeimbangan pertempuran yang terdokumentasi di Holuf, tanpa klaim pengalaman profesional.

Image-API memiliki dokumentasi teknis yang lengkap; pilihan awal menonjolkan dua alat desktop dan satu game agar ragam proyek mudah dibaca. README arthaflow masih template Next.js. README iwed-discord-music-bot menjelaskan fondasi dan `/health`, dengan pemutaran musik belum tersedia pada fase yang didokumentasikan. Jumlah bintang bukan dasar pilihan.

Profil publik belum mencantumkan portfolio atau bio saat diperiksa. Hanya profil GitHub yang ditautkan; tambahkan portfolio dan demo setelah URL publiknya terverifikasi. Sumber pada branch `main` dapat berubah, sehingga perlu ditinjau ulang saat pemeliharaan.

## Menampilkan README di GitHub

GitHub memerlukan repositori publik bernama sama dengan username, dengan `README.md` berisi konten di root. Target ini sudah sesuai dan default branch adalah `main`. Lihat [panduan resmi profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).

Root Git lokal adalah `D:\project\rexkarbu\rexkarbu`, satu tingkat di dalam workspace. Setelah meninjau semua berkas, jalankan dari root Git:

```sh
git status --short --branch
git diff --check
git diff -- README.md
git add README.md assets/rexs-night-workshop.png assets/rexs-night-workshop.gif docs/profile-maintenance.md docs/banner-prompt.md scripts/animate-banner.py
git diff --cached --stat
git commit -m "Create Rex's Night Workshop profile README"
git push origin main
```

Periksa berkas baru secara langsung sebelum commit; `git diff` biasa belum menampilkan berkas yang belum dilacak. Jika remote berubah dan push ditolak, lakukan `git fetch origin`, tinjau serta integrasikan perubahan, lalu coba kembali tanpa force push.

Setelah push, buka [repositori profil](https://github.com/rexkarbu/rexkarbu) dan [profil Rex](https://github.com/rexkarbu). Pastikan banner, tautan, dan isi README muncul. Tidak diperlukan aplikasi, hosting, GitHub Pages, atau workflow terjadwal.

## Pemeriksaan saat memperbarui

- Jalankan `git diff --check`; pastikan semua path lokal tersedia, termasuk PNG pada `srcset`.
- Buka tautan eksternal untuk memeriksa tujuan dan visibilitas.
- Periksa lebar/sempit, terang/gelap, teks alternatif, dan pengurangan animasi.
- Bedakan preview HTML lokal dari halaman GitHub setelah push. Preview lokal tidak membuktikan hasil akhir pada halaman profil.

Tidak diperlukan test suite untuk perubahan README ini.

### Hasil verifikasi implementasi awal

Pada 6 September 2026:

- Keempat URL unik pada README merespons HTTP 200 tanpa mengarah ke URL lain. Status publik diperiksa melalui pencarian GitHub yang dibatasi `is:public`.
- API Markdown GitHub menerima README dalam mode GFM (HTTP 200) dan mempertahankan `picture`, `source`, preferensi reduced motion, path aset, serta tautan.
- HTML dari API tersebut diperiksa dalam browser lokal dengan CSS perkiraan tampilan GitHub pada lebar 1440 px dan 360 px, masing-masing dalam tema terang dan gelap. Semua gambar dimuat, tiga proyek tampil, dan tidak ada overflow horizontal. Screenshot keempat kombinasi ditinjau secara visual; tidak ada error halaman yang dilaporkan browser.
- Preferensi reduced motion pada preview memilih PNG. Kedua aset berukuran 1200 × 360; GIF memiliki 24 frame dengan total durasi 3,84 detik. Perbedaan piksel antarframe hanya berada di dalam monitor.
- Path aset, tautan dokumen lokal, dan whitespace diperiksa. `git diff --check` lulus. Skrip animasi dijalankan dengan Python 3.14 dan Pillow 12.3.0.

Ini adalah pemeriksaan konversi Markdown GitHub dan **preview lokal**, belum pemeriksaan halaman profil GitHub setelah publikasi. CSS lokal hanya pendekatan; tampilan akhir serta pemuatan aset dari GitHub perlu dicek setelah push. Commit dan push belum dilakukan saat serah terima awal.
