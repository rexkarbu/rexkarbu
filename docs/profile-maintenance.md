# Pemeliharaan Rex's Night Workshop

Profil ini adalah GitHub Profile README untuk [rexkarbu/rexkarbu](https://github.com/rexkarbu/rexkarbu). Root Git workspace: `D:\project\rexkarbu\rexkarbu`. Konten profil menggunakan bahasa Inggris; panduan ini menggunakan bahasa Indonesia. Tidak ada aplikasi atau layanan hosting di repositori ini.

## Desain dan aset tetap

Banner original dipertahankan tanpa perubahan:

- [PNG 1200 × 360](../assets/rexs-night-workshop.png): sumber permanen dan pilihan reduced motion.
- [GIF 1200 × 360](../assets/rexs-night-workshop.gif): 24 frame, loop 3,84 detik; cahaya monitor berubah maksimal 8%.
- [Prompt dan asal banner](banner-prompt.md): catatan pembuatan menggunakan image_gen.
- [Pemisah pixel](../assets/pixel-divider.svg): SVG original 320 × 12, digunakan dua kali secara dekoratif.

Palet aset: charcoal `#0D1117`, midnight blue `#17243A`, sage `#9DB7A5`, amber `#E5B567`, off-white `#E6EDF3`. Teks Markdown tetap mengikuti tema GitHub. Gunakan satu banner, blok proyek vertikal, label kecil, dan informasi penting dalam teks.

Untuk mengganti banner, simpan PNG dengan komposisi yang tetap terbaca pada layar kecil, sesuaikan koordinat `MONITOR` di skrip, lalu jalankan:

```sh
python -m pip install Pillow
python scripts/animate-banner.py
```

Skrip mempertahankan PNG dan menulis ulang GIF. Pillow hanya diperlukan untuk animasi banner; generator aktivitas dan ikon memakai pustaka standar Python. Jika animasi banner tidak diinginkan, ganti elemen `picture` pertama dengan gambar Markdown yang menautkan PNG. Pertahankan alt text.

## Memperbarui proyek pilihan

Urutan yang dikurasi: **NVL Studio → Dashboard Daily → ArthaFlow**. Setiap blok memuat nama bertautan, satu kalimat manfaat, dan metadata teknologi ringkas. Label menggambarkan jenis proyek, bukan status pekerjaan atau tingkat keahlian.

Sebelum memperbarui, periksa visibilitas repositori, README, manifest dependensi, serta kode relevan secara read-only. Jangan mengambil database, data pengguna, atau isi repositori private. Atribut `private` pada `package.json` mengatur publikasi npm, bukan visibilitas GitHub.

Bukti yang diperiksa pada **6 September 2026**:

| Proyek | Dasar konten |
| --- | --- |
| NVL Studio | [README](https://github.com/rexkarbu/nvl-studio/blob/main/README.md): avatar reaktif suara, blinking, layer PNG, penyimpanan proyek, dan OBS. [package.json](https://github.com/rexkarbu/nvl-studio/blob/main/package.json): TypeScript, React, Electron, Vite. API releases mengembalikan daftar kosong. |
| Dashboard Daily | [README](https://github.com/rexkarbu/dashboard-daily/blob/main/README.md): widget, carry-over tugas, catatan lokal, dan cache cuaca. [package.json](https://github.com/rexkarbu/dashboard-daily/blob/main/package.json): TypeScript, React, Electron. [Rilis v0.2.0](https://github.com/rexkarbu/dashboard-daily/releases/tag/v0.2.0) memiliki installer Windows, ZIP, dan SHA256SUMS.txt; bukan draft atau prerelease. |
| ArthaFlow | [Metadata aplikasi](https://github.com/rexkarbu/arthaflow/blob/main/app/layout.js) menyatakan keuangan pribadi. [Halaman transaksi](https://github.com/rexkarbu/arthaflow/blob/main/app/transaksi/page.js), [form transaksi](https://github.com/rexkarbu/arthaflow/blob/main/components/ExpenseForm.js), dan [halaman anggaran](https://github.com/rexkarbu/arthaflow/blob/main/app/budget/page.js) mendukung pemasukan/pengeluaran dan anggaran bulanan/per kategori. [package.json](https://github.com/rexkarbu/arthaflow/blob/main/package.json) serta berkas .js mengonfirmasi JavaScript, React, Next.js. Tidak ada TypeScript pada daftar dependensinya dan tidak ada rilis publik. |

README ArthaFlow masih template Next.js; deskripsi produk berasal dari metadata dan kode di atas. [CategoryBudgetManager](https://github.com/rexkarbu/arthaflow/blob/main/components/CategoryBudgetManager.js) mengonfirmasi anggaran kategori. [IncomeExpenseChart](https://github.com/rexkarbu/arthaflow/blob/main/components/IncomeExpenseChart.js) memakai Recharts, mendukung fokus visualisasi data keuangan. Membaca kode ini bukan pengujian aplikasi atau verifikasi seluruh fiturnya.

Implementasi `addExpense`, `setBudget`, dan `setCategoryBudget` dalam [app/actions.js](https://github.com/rexkarbu/arthaflow/blob/main/app/actions.js) juga diperiksa: terdapat penulisan transaksi serta anggaran bulanan dan kategori. Hanya kode dibaca; database tidak dibuka atau dijalankan.

`Inside the Workshop`, perkenalan, `Tools I Use`, dan `Development Focus` harus tetap selaras dengan ketiga proyek. Fokus menunjukkan ranah implementasi yang terlihat pada proyek, bukan klaim aktivitas real-time. Hanya Dashboard Daily diberi tautan rilis; ketiadaan rilis tidak disamakan dengan proyek ditinggalkan.

Tidak ditemukan screenshot produk yang sesuai pada pohon berkas publik yang diperiksa. Aset karakter NVL bukan screenshot antarmuka. Tata letak teks sengaja lengkap tanpa thumbnail atau mockup buatan.

## Ikon: sumber, lisensi, dan regenerasi

Enam ikon berasal dari [Simple Icons 16.13.0](https://github.com/simple-icons/simple-icons/tree/9ddef18c4247eab3819ec280f07cb8e95dc2a274), commit `9ddef18c4247eab3819ec280f07cb8e95dc2a274`. Tag annotated tersebut telah diurai ke commit di repositori upstream.

- [Lisensi koleksi CC0-1.0](../assets/icons/LICENSE.md).
- [Metadata sumber per ikon](../assets/icons/sources.json), termasuk tautan sumber resmi atau sumber desain asalnya.
- JavaScript memiliki penanda MIT dalam metadata dan [lisensi sumber asli](../assets/icons/JAVASCRIPT-LICENSE.txt) ikut disimpan.
- Entri Electron, React, TypeScript, Next.js, dan Vite pada versi ini tidak mencantumkan lisensi ikon terpisah. CC0 berlaku pada koleksi sesuai upstream; hak merek tetap milik pemiliknya. Lihat [disclaimer Simple Icons](https://github.com/simple-icons/simple-icons/blob/9ddef18c4247eab3819ec280f07cb8e95dc2a274/DISCLAIMER.md).
- Bentuk path ikon dipertahankan. Presentasi memakai tile SVG lokal 80 × 88 px dengan sudut terpotong pixel, latar midnight blue `#17243A`, garis tepi sage `#9DB7A5`, aksen amber `#E5B567`, serta label teks di bawah logo. Logo menggunakan warna sage; Next.js menggunakan off-white. Ikon hanya mengidentifikasi teknologi. Setiap gambar memiliki alt text dan label visual.
- Next.js dan merek terkait adalah merek dagang Vercel, Inc. atau afiliasinya. [Pedoman merek](https://vercel.com/geist/brands) dan [pedoman TypeScript](https://www.typescriptlang.org/branding/) menjadi rujukan penggunaan.

Regenerasi ikon, tanpa npm atau CDN saat profil ditampilkan:

```sh
python scripts/update-icons.py
```

Skrip mengunduh/mempertahankan enam SVG mentah di `assets/icons/raw/` serta lisensi dari revisi yang dipin, lalu menghasilkan ulang tile di `assets/icons/`. Ubah pin hanya setelah meninjau metadata, bentuk ikon, serta lisensi versi pengganti.

## Statistik dan contribution trail

Seluruh gambar pada README memakai path relatif dan sudah tersedia sebelum workflow pertama berjalan. [Snapshot aktivitas](../assets/activity/README.md) menyediakan angka, tanggal, periode, cakupan, sumber, dan tautan versi statis. [data.json](../assets/activity/data.json) adalah masukan untuk reproduksi, bukan data contoh.

Sumber data:

1. [GitHub REST: repositori publik milik rexkarbu](https://api.github.com/users/rexkarbu/repos), dengan semua halaman hasil. Metrik: jumlah repositori publik dan jumlah `stargazers_count` di seluruh repositori tersebut. Cakupan mencakup fork serta repositori profil, tidak tergantung pilihan proyek.
2. [Kalender kontribusi publik GitHub](https://github.com/users/rexkarbu/contributions), diambil tanpa autentikasi. Tanggal, jumlah kontribusi, dan level intensitas dibaca dari sel dan tooltip asli. Jika pemilik akun memilih menampilkan hitungan kontribusi private anonim, kalender publik dapat memuat angka tersebut; nama dan isi repositori private tidak diambil.

Kartu statistik adalah SVG original yang dihasilkan skrip lokal. Tidak ada rating, peringkat, atau persentase kemampuan. Kalender menampilkan rentang tanggal yang betul-betul dikembalikan GitHub, dengan uraian tekstual pada snapshot.

Snake menggunakan [Platane/snk](https://github.com/Platane/snk) pada commit `a041d6c27ba561a39f5be9c26a784812765e434b` (versi paket 3.5.0; commit upstream 25 April 2026). Dokumentasi penggunaan, pengambil data, action entrypoint, solver, serta modul renderer SVG diperiksa. Bundle yang dipakai:

| Berkas sementara upstream | Git blob SHA terverifikasi |
| --- | --- |
| `svg-only/dist/index.js` | `a63c6275053d4d1252c310892bb8bf7ca9b375ab` |
| `svg-only/dist/578.index.js` | `336aa893d04eb8effb9b3cdfdfd98f3bf98dca48` |

Skrip memeriksa hash Git blob sebelum mengeksekusi keduanya. `render-trail.cjs` memetakan snapshot kalender publik ke bentuk respons GraphQL yang diperlukan renderer, tanpa mengubah tanggal, jumlah, atau level. Renderer tidak mengakses API langsung atau menerima token. Permintaan fetch selain kalender yang diharapkan ditolak. Ini memungkinkan regenerasi lokal tanpa personal access token dan memberi data yang sama pada animasi serta versi statis.

Upstream pada pin ini tidak menyertakan berkas LICENSE. Kode generator tidak disalin ke repositori profil; bundle diunduh sementara untuk penggunaan generator yang didokumentasikan upstream. Atribusi Platane/snk dipertahankan pada SVG dan snapshot. Pemisah pixel, kartu statistik, serta tampilan kalender statis dibuat khusus untuk profil ini.

### Menjalankan generator

Prasyarat aktivitas: Python 3.10+ dan Node.js 24. Tidak ada paket Python atau npm tambahan. Dari root repositori:

```sh
python scripts/update-activity.py
python scripts/update-activity.py --validate assets/activity
```

Regenerasi dari snapshot yang sudah ada (tanggal snapshot tidak diubah):

```sh
python scripts/update-activity.py --snapshot assets/activity/data.json
```

Mode ini masih mengunduh dua bundle yang dipin. Untuk reproduksi sepenuhnya offline, sediakan direktori berisi `index.js` dan `578.index.js` dari URL revisi tersebut, lalu tambahkan `--bundle-dir PATH`. Hash keduanya tetap diperiksa.

Dependensi jaringan hanya GitHub REST, halaman kalender GitHub, dan raw.githubusercontent.com untuk bundle. Token opsional `GH_TOKEN` atau `GITHUB_TOKEN` hanya dikirim ke api.github.com untuk batas laju REST; jangan memasukkannya ke berkas atau argumen command. Kalender selalu diambil secara anonim.

Lima output yang wajib lengkap:

- `assets/activity/github-stats.svg`
- `assets/activity/contribution-trail.svg`
- `assets/activity/contribution-trail-static.svg`
- `assets/activity/data.json`
- `assets/activity/README.md`

Semua pengambilan data, render, dan validasi selesai di direktori sementara sebelum aset lama diganti. Parser menolak kalender kosong, hitungan tidak terbaca, tanggal tidak berurutan, atau data tidak valid. Jika GitHub mengubah HTML atau layanan gagal, generator berhenti; jangan mengisi data nol buatan untuk melanjutkan.

### GitHub Actions

[profile-assets.yml](../.github/workflows/profile-assets.yml) menyediakan `workflow_dispatch` dan satu jadwal sehari: **02:17 UTC / 09:17 WIB**. Tidak ada pemicu push atau pull request, sehingga commit aset tidak memicu loop.

- Job `generate`: `contents: read`, checkout tanpa menyimpan kredensial, Node.js 24, pengambilan data publik, validasi, lalu upload artifact.
- Job `publish`: satu-satunya job dengan `contents: write`; mengunduh artifact dari run yang sama, memvalidasi ulang, dan commit hanya lima output di atas.
- `GITHUB_TOKEN` bawaan mencukupi. Tidak diperlukan PAT atau secret tambahan.
- Job publikasi hanya berjalan bila pembuatan artifact berhasil. Snapshot terakhir tetap ada bila jaringan, render, validasi, atau push gagal.
- Commit hanya dibuat jika ada perubahan. Tidak ada force push. Bila branch berubah bersamaan, push dapat gagal; jalankan ulang untuk memakai main terbaru.
- `concurrency` mencegah dua run saling menimpa. Jalankan manual dari `main`; job dibatasi untuk repositori profil ini.

Pin action telah diverifikasi melalui referensi tag upstream:

| Action | Versi | Commit |
| --- | --- | --- |
| actions/checkout | v4.3.0 | `08eba0b27e820071cde6df949e0beb9ba4906955` |
| actions/setup-node | v4.4.0 | `49933ea5288caeca8642d1e84afbd3f7d6820020` |
| actions/upload-artifact | v4.6.2 | `ea165f8d65b6e75b540449e92b4886f43607fa02` |
| actions/download-artifact | v4.3.0 | `d3f86a106a0bac45b974a628896c90dbdf5c8093` |

Pendekatan izin per job dan pin SHA mengikuti [panduan keamanan GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use). Jika aturan perlindungan branch menolak bot push, run akan gagal tanpa mengganti aset remote. Tinjau artifact dan unggah pembaruan melalui alur branch yang diizinkan; jangan menonaktifkan perlindungan secara otomatis.

### Fallback dan pengurangan animasi

Banner menggunakan `picture` dengan PNG untuk `prefers-reduced-motion: reduce`. Contribution trail menggunakan pola yang sama dengan SVG statis. Kalender statis dibuat dari snapshot yang sama dan tidak mengandung animasi.

Kegagalan layanan tidak membuat broken image karena README memuat berkas yang telah di-commit. Tanggal pada kartu dan snapshot menunjukkan umur data terakhir. Untuk menghentikan animasi bagi semua pengunjung, ganti `picture` trail dengan:

```markdown
![Rex's public GitHub contribution calendar](assets/activity/contribution-trail-static.svg)
```

Jangan mengganti aset yang valid dengan placeholder. Jika generator gagal, perbaiki sumber atau parser terlebih dahulu dan jalankan kembali. Jangan mengedit angka statistik secara manual.

## Publikasi

Versi awal sudah ada pada commit `21b66e2`. Perubahan pengayaan dikerjakan di branch `main` tanpa commit atau push otomatis. Tinjau file baru karena `git diff` biasa belum menunjukkan isi berkas untracked:

```sh
git status --short --branch
git diff --check
git diff -- README.md docs/profile-maintenance.md
git add README.md docs/profile-maintenance.md assets/pixel-divider.svg assets/icons assets/activity scripts/update-icons.py scripts/update-activity.py scripts/render-trail.cjs .github/workflows/profile-assets.yml
git diff --cached --stat
git commit -m "Enrich Rex's Night Workshop profile"
git push origin main
```

Setelah push, buka profil dan repositori GitHub. Repositori publik yang namanya sama dengan username akan menampilkan README root sesuai [panduan profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).

Buka tab Actions → **Refresh profile assets** → **Run workflow**, pilih `main`. Pastikan kedua job berhasil, artifact berisi lima output, dan commit bot hanya mengubah `assets/activity/`. Tarik perubahan bot dengan `git pull --ff-only` sebelum pengeditan berikutnya.

## Pemeriksaan

Periksa path gambar dan dokumen, tautan repositori/rilis, alt text, tiga proyek pilihan, bukti teknologi, serta tidak adanya narasi game dari kurasi lama. Periksa 360 px dan 1440 px, tema terang/gelap, serta dua fallback reduced motion. Pastikan banner original tidak berubah.

Preview HTML lokal memakai CSS perkiraan GitHub; konversi API Markdown GitHub memeriksa penerimaan sintaks, tetapi keduanya berbeda dari halaman profil GitHub setelah push. Workflow hanya dapat diverifikasi di runner GitHub setelah berkasnya dipublikasikan. Jangan menyebut run lokal sebagai run GitHub Actions. Tidak ada test suite aplikasi untuk pekerjaan README ini.

### Hasil pemeriksaan pengayaan — 6 September 2026

- Semua path aset dan tautan dokumen lokal pada README/panduan/snapshot tersedia. Empat URL unik proyek dan rilis pada README merespons HTTP 200 tanpa redirect. Tidak ada nama proyek game lama, narasi RPG, atau teknologi game pada README yang dikurasi.
- Kedua banner memiliki SHA-256 yang sama dengan sebelum pengerjaan. Banner dan skrip animasinya tidak diubah.
- Generator ikon dan aktivitas berhasil dijalankan lokal. Snapshot mencatat 7 repositori publik dan 3 bintang. Seluruh 365 tanggal, hitungan, dan level kalender cocok dengan salinan HTML publik yang diunduh secara terpisah: 370 kontribusi pada 27 hari aktif, 7 September 2025–6 September 2026.
- Kartu statistik berukuran 480 × 148 (968 byte); snake animasi dan statis 880 × 192 (29.840 dan 42.961 byte). Browser mengonfirmasi perubahan posisi keempat segmen snake. Versi statis tidak memiliki animasi.
- API Markdown GitHub menerima sintaks (HTTP 200). Preview dari hasil API dengan CSS lokal diperiksa pada 1440 px dan 360 px dalam tema terang/gelap. Semua gambar dimuat dan tidak ada overflow horizontal; screenshot keempat kombinasi ditinjau. Kedua preferensi reduced motion memilih PNG banner serta SVG kalender statis dalam tema terang/gelap.
- `actionlint` 1.7.12 lulus untuk workflow; integritas arsip pemeriksa diverifikasi melalui SHA-256 rilis resmi. Pemeriksaan dilakukan tanpa integrasi ShellCheck. Sintaks Python dan JavaScript diperiksa.
- Simulasi bundle renderer yang gagal pemeriksaan integritas menghasilkan kegagalan tanpa mengubah hash kelima aset yang ada. Langkah instalasi artifact milik job penerbitan direproduksi ke direktori lokal terpisah dan menghasilkan lima file identik.
- `git diff --check` lulus. Belum ada commit/push pengayaan atau run workflow di GitHub. Pengujian aplikasi proyek lain berada di luar cakupan pekerjaan ini.
