# Banner: The Lantern Passage

Banner utama adalah ilustrasi 2D original dengan penjelajah berjubah merah kusam yang berjalan melewati reruntuhan taman bawah tanah. Kamera tetap; lengkungan, lumut, akar di tepi, serta jalur batu membentuk beberapa lapisan kedalaman. Tidak ada teks di dalam gambar.

## Berkas dan sumber

| Berkas | Fungsi |
| --- | --- |
| [lantern-passage.gif](../assets/banner/lantern-passage.gif) | Animasi default pada README. |
| [lantern-passage.png](../assets/banner/lantern-passage.png) | Frame representatif di tengah perjalanan, untuk reduced motion. |
| [garden.png](../assets/banner/source/garden.png) | Ilustrasi lingkungan tanpa karakter, 2172 × 724. |
| [traveler-sheet.png](../assets/banner/source/traveler-sheet.png) | Satu lembar karakter: kepala/tubuh berjubah, kaki, lengan, dan panel kain. |
| [prompts.md](../assets/banner/source/prompts.md) | Kedua prompt asli dan asal ilustrasi. |
| [render-lantern-passage.py](../scripts/render-lantern-passage.py) | Pemisahan bagian karakter, rig, compositing, dan ekspor. |
| [render-info.json](../assets/banner/render-info.json) | Spesifikasi hasil, ukuran byte, dan SHA-256 sumber. |

Ilustrasi dibuat dengan tool bawaan `image_gen` pada 7 September 2026. Atmosfer ilustrasi fantasi 2D menjadi inspirasi; desain penjelajah dan susunan lingkungan dibuat sendiri. Tidak ada sprite, screenshot, logo, atau potongan gameplay Hollow Knight/Silksong yang digunakan. Tidak ada aset seni pihak ketiga yang perlu diunduh untuk render ulang. Lisensi ikon teknologi yang sudah ada tetap dijelaskan di [panduan profil](profile-maintenance.md).

Generator mengembalikan lembar karakter RGB dengan pola checkerboard, meskipun prompt meminta transparansi. Skrip mengubah piksel latar netral terang yang terhubung ke tepi menjadi alpha, merapikan tepi pada resolusi sumber, lalu memotong empat bagian. Wajah dan pakaian selalu berasal dari gambar yang sama; tidak ada generasi gambar terpisah per frame.

## Gerakan

- Karakter bergerak dari x=400 ke x=800, lalu kembali. Masing-masing perjalanan memakai 3,2 detik; akselerasi dan perlambatan berlangsung lembut selama 0,24 detik di tiap ujung.
- Setiap perjalanan berisi lima siklus langkah lengkap. Saat kaki menyentuh tanah, koordinat horizontalnya di dunia tetap; lutut mengikuti dua ruas kaki melalui inverse kinematics. Kaki yang berganti posisi diangkat, termasuk ketika merapatkan atau membuka posisi kaki saat berhenti.
- Jeda di tiap ujung mencakup merapatkan kaki, berbalik, dan menyiapkan langkah berikutnya. Pergantian arah memakai pencerminan rig dengan penyempitan perspektif singkat, bukan perubahan bentuk wajah. Ini animasi cutout 2D; tidak ada gambar wajah depan tambahan.
- Lengan mengayun bergantian, tubuh mengikuti langkah, dan gerak napas ringan mengisi jeda. Bagian bawah jubah dilengkungkan dengan fase tertunda, sedangkan panel kain belakang bergerak pada lapisannya sendiri.
- Tiga cahaya lampu berdenyut lembut; bentuk lampunya tetap. Lapisan kabut bergerak perlahan dan 12 partikel amber melayang. Fase lingkungan berulang tepat pada sambungan loop. Tidak ada gerakan kamera, zoom, atau penggeseran seluruh latar.

## Render ulang

Jalankan dari root repositori. Lingkungan yang benar-benar digunakan: Python 3.14, Pillow 12.3.0, NumPy 2.5.1.

```sh
python -m pip install Pillow==12.3.0 numpy==2.5.1
python scripts/render-lantern-passage.py
```

Perintah ini hanya membaca sumber lokal dan menulis GIF, PNG, serta manifest hasil. Tidak memerlukan token, akses jaringan, layanan video, atau panggilan image_gen baru. Tidak ada workflow harian untuk banner.

Parameter ekspor:

```sh
python scripts/render-lantern-passage.py --duration 10 --fps 16 --colors 192
```

- `--duration`: panjang loop dalam detik. Seluruh timeline diskalakan bersama, sehingga langkah tetap terikat pada jarak dan animasi lingkungan tetap tersambung. Default 9 detik.
- `--fps`: rata-rata jumlah frame per detik. Default 16. GIF menyimpan waktu dalam kelipatan 10 ms; ekspor default memakai delay 60/70 ms, total tepat 9000 ms.
- `--colors`: jumlah warna dalam palet bersama. Default 192; jangan menurunkannya tanpa memeriksa wajah, jubah, dan gradasi kabut.
- `--output`: direktori hasil alternatif untuk mencoba perubahan tanpa menimpa banner aktif.
- `--frames`: direktori opsional untuk PNG tiap frame. Gunakan folder review di luar repositori; frame sementara tidak diperlukan untuk regenerasi.

Contoh pemeriksaan terpisah:

```sh
python scripts/render-lantern-passage.py --output ../.profile-review/banner-candidate --frames ../.profile-review/banner-frames
```

Skrip memakai seed partikel tetap `260907`, supersampling 2× untuk karakter, satu palet GIF bersama tanpa dithering, serta frame disposal 1 dengan optimasi area berubah. Latar tidak digambar ulang oleh model. GIF default 1200 × 360, 144 frame, loop tanpa batas, **1.290.457 byte** (sekitar 1,29 MB); PNG **717.223 byte**. Manifest dihasilkan ulang setiap render dan menjadi rujukan jika parameter berubah.

## Mengganti warna atau ilustrasi

Warna sumber memakai charcoal/midnight untuk bayangan, sage/teal untuk taman, ivory untuk wajah dan tepi tudung, merah kusam untuk jubah, dan amber untuk lampu. Warna efek cahaya dan kabut dapat diubah pada konstanta `PALETTE` dalam skrip. Warna lukisan dan pakaian tertanam pada kedua PNG sumber: edit sumber tersebut, pertahankan dimensi dan posisi bagian rig, lalu render ulang. Mengubah `PALETTE` saja tidak mewarnai ulang seluruh ilustrasi.

Jika mengganti susunan gambar, sesuaikan kotak potong pada `extract_parts()`, titik sendi pada `render_character()`, posisi lampu pada `atmosphere()`, serta garis pijakan `GROUND`. Jangan menggunakan koordinat lama untuk lembar karakter berbeda. Jalur berjalan harus tetap rata; latar dipotong ke rasio 10:3 lalu diperkecil dengan Lanczos, tanpa pengulangan tile atau peregangan rasio.

## README dan fallback

Elemen `picture` pertama memakai GIF sebagai `img`, PNG sebagai `source` untuk `prefers-reduced-motion: reduce`, alt text yang menjelaskan adegan, dan atribut lebar 1200. Ukuran gambar mengikuti kontainer GitHub. Tidak ada JavaScript atau CSS tambahan pada README.

Sumber dan hasil tersimpan lokal sehingga kegagalan layanan eksternal tidak merusak banner. Untuk menampilkan versi statis kepada semua pengunjung, ubah `src` pada `img` menjadi PNG. Banner pixel art sebelumnya tetap tersedia bersama skripnya; langkah pemulihan ada di [panduan pemeliharaan](profile-maintenance.md#desain-dan-aset-tetap).

## Pemeriksaan sebelum publikasi

Putar GIF sebenarnya sekurang-kurangnya tiga putaran. Periksa langkah kaki, arah hadap, kontak tanah, jeda/putaran, gerak jubah, partikel, serta sambungan akhir-awal. Jangan menyimpulkan kelancaran hanya dari PNG atau contact sheet. Periksa juga 360 px dan desktop, tema terang/gelap, serta pilihan PNG saat reduced motion aktif.

Preview HTML lokal menggunakan hasil API Markdown GitHub dengan CSS perkiraan. Ini memeriksa sintaks dan pemilihan aset, tetapi bukan bukti tampilan banner baru pada halaman GitHub yang sudah dipublikasikan. Setelah commit/push, buka profil GitHub dan periksa lagi pemutaran serta reduced motion di browser pengunjung.

### Hasil pemeriksaan 7 September 2026

- API Markdown GitHub menerima README baru (HTTP 200). Preview lokal diperiksa pada viewport 360 dan 1440 px, tema terang serta gelap. Semua 11 gambar termuat tanpa overflow horizontal; PNG banner dan kalender statis terpilih ketika reduced motion aktif.
- GIF benar-benar diputar di Chromium selama 29 detik. [Screencast Chrome DevTools](https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-startScreencast) menangkap 464 frame dari browser; tiga putaran lengkap masing-masing mencakup seluruh 144 frame GIF. Setiap tangkapan cocok piksel demi piksel dengan frame GIF yang didekode. Pergantian loop tercatat sekitar 9,1, 18,1, dan 27,1 detik sejak perekaman dimulai.
- Sampel urutan pemutaran dari ketiga putaran ditinjau secara visual: langkah, kaki terangkat, tangan, panel jubah, arah hadap, serta peralihan berhenti/berjalan terbaca. Ilustrasi latar tanpa karakter mencegah figur ganda. Seluruh 144 frame GIF cocok dengan hasil compositing yang dimaksud, sehingga optimasi GIF tidak meninggalkan bayangan frame sebelumnya.
- Titik pijak kaki saat fase kontak tanah diverifikasi pada timeline rapat: selisih numeriknya kurang dari `1e-9` piksel sebelum pembulatan raster. Frame master pada t=0 dan t=9 identik. Ini memeriksa rig dan sambungan loop, bukan klaim pengamatan manusia terhadap setiap piksel.
- Isi README setelah banner, ikon, statistik, contribution trail, workflow aktivitas, serta aset dan skrip banner lama dipastikan tidak berubah. Path gambar dan `git diff --check` diperiksa.

**Batas pemeriksaan:** antarmuka agen menerima gambar, bukan video yang dapat ditonton langsung. Pemeriksaan gerak di atas memakai urutan frame dari pemutaran browser yang sebenarnya serta validasi seluruh frame; ini tidak diklaim sebagai penontonan video langsung selama tiga putaran. Perekam WebM bawaan browser gagal karena FFmpeg tidak tersedia; screencast digunakan tanpa memasang dependensi tambahan. Pengujian profil GitHub yang sudah dipublikasikan masih memerlukan commit/push. Tidak ada aset ilustrasi atau animasi yang masih berupa placeholder.
