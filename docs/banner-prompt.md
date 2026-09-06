# Prompt banner original

Ilustrasi dibuat pada 6 September 2026 dengan tool bawaan `image_gen`, tanpa gambar referensi eksternal. Edit kedua menggunakan ilustrasi pertama sebagai satu-satunya target.

## Prompt awal

```text
Use case: stylized-concept.
Asset type: original pixel-art banner for Rex's GitHub profile, "Rex's Night Workshop".
Primary request: A quiet nighttime desk workshop with a monitor, books, a small potted plant, and a broad window overlooking an urban skyline. Make a distinctive original composition.
Style/medium: refined crisp pixel art, flat blocks of color, deliberate stepped silhouettes, limited palette, minimal dithering; large readable shapes rather than excessive detail.
Composition/framing: very wide horizontal banner around 1200 by 360 pixels (10:3 aspect ratio); if a different output ratio is required, keep all essential objects inside a centered 10:3 safe area with extra background above and below. A long desk spans the lower part; an asymmetrically arranged monitor, book stack and small plant form the foreground; a large city-view window balances the room. All four requested objects must remain distinct when the image is reduced to phone width. Calm margins, cohesive scene, no surrounding frame or mockup.
Lighting/mood: midnight, quiet and inviting; soft sage monitor light and small amber city lights, subtle warm light on the desk.
Color palette: charcoal #0D1117, midnight blue #17243A, sage #9DB7A5, amber #E5B567, off-white #E6EDF3. Base the entire asset on these five colors and restrained nearby shades.
Text: none. Any monitor marks should be abstract non-legible blocks, not words.
Constraints: original composition; no people or characters, no avatars, no logos, no watermark, no Minecraft imagery or mountain scenes, no wave banner, no gradients or blurry photographic textures.
```

## Prompt penyesuaian komposisi

```text
Use case: precise-object-edit.
Edit the supplied workshop illustration into a much wider and shallower GitHub banner. Output image dimensions: 1536 x 512 pixels, a panorama with exactly 3:1 width-to-height ratio.
Preserve the visual identity, palette, desk, sage monitor on the left, amber desk lamp, stack of books and small plant on the right, and city window. Recompose and simplify to fit all the monitor, books, plant, lamp and desk surface inside the shallow panorama; reduce the height of the window and remove the upper wall shelf and everything below the desktop. Leave 26 pixels of expendable background at both top and bottom so a center crop to 10:3 preserves all essential objects.
Refine to clean pixel-art blocks with hard stepped edges and no blurry texture, using charcoal #0D1117, midnight blue #17243A, sage #9DB7A5, amber #E5B567, off-white #E6EDF3 and restrained nearby shades.
No text, logos, characters or watermark. The requested change is the wide banner framing, no new subject or theme.
```

## Hasil dan pemrosesan lokal

Generator menghasilkan ilustrasi kedua berukuran 1536 × 1024 dengan ruang kosong di atas dan bawah. Area `(left=0, top=302, right=1536, bottom=763)` dipotong, kemudian diperkecil menjadi 1200 × 360 menggunakan nearest-neighbor untuk mempertahankan tepi pixel art. PNG final disimpan di `assets/rexs-night-workshop.png`; PNG ini adalah sumber permanen untuk membuat ulang GIF, sehingga file sementara generator tidak diperlukan.

Bila mengekspor ulang hasil generator dengan komposisi yang sama, gunakan Python dan Pillow:

```python
from PIL import Image

with Image.open("workshop-generated.png") as image:
    banner = image.crop((0, 302, 1536, 763))
    banner = banner.resize((1200, 360), Image.Resampling.NEAREST)
    banner.convert("RGB").save("assets/rexs-night-workshop.png", optimize=True)
```

Nama `workshop-generated.png` pada contoh adalah berkas keluaran generator yang hendak diproses, bukan dependensi repositori. Untuk ilustrasi berbeda, tentukan ulang area pemotongan agar objek utama tetap utuh.

Animasi lokal dibuat oleh [scripts/animate-banner.py](../scripts/animate-banner.py) dari PNG final. Hanya cahaya di dalam layar monitor yang berubah, dengan penurunan kecerahan maksimal 8%, 24 frame, dan loop 3,84 detik. Palet GIF dibagikan antarframe agar area lain tetap stabil. Versi statis tetap tersedia melalui `picture` saat preferensi reduced motion aktif.

Lihat [panduan pemeliharaan](profile-maintenance.md) untuk menjalankan skrip dan mengganti banner.

