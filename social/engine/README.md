# Reels automáticos de relojes disponibles (TicoTime CR)

Video vertical 1080×1920 de ~20–24 s por reloj disponible: precio grande desde el primer segundo,
fotos que se deslizan y se mueven, 3 características que aparecen una por una, voz de hombre tico
(edge-tts `es-CR-JuanNeural`), música sintetizada de fondo y cierre con "Apartalo con ₡X" + WhatsApp 8640-0835.
Se publica en Instagram + Facebook (Reel) + TikTok con Metricool, usando el enlace raw de GitHub del video.

## Datos fijos
- Hoja de inventario: `1ArPB40GKsrGG0xw9znNU754ZgsH0C_hpiagp0HW1sig`, rango `Web!A1:D80` (ref, modelo, precio, oferta) = relojes disponibles HOY.
- Fichas (nombre, sub, desc) de cada ref: `public/disponibles.js` (`window.STOCK`).
- Metricool: brandId `7542714`, timezone `America/Guatemala`.
- URL pública: `https://raw.githubusercontent.com/JohelGB/Ticotimecr/main/social/reels/<archivo>`
- Historial: `social/reels/publicados.md`.

## Procedimiento (tarea programada "Reels de disponibles")
1. `git pull --rebase origin main` y `bash social/engine/setup.sh` (debe decir `setup ok`).
2. Leé la hoja Web y, con `getScheduledPosts` (desde ahora hasta 8 días), mirá qué días de los próximos 7 ya tienen un Reel
   NO borrador con línea "Ref. N". Horarios: lunes a viernes alternando 12:30 y 19:00; sábado 12:30, domingo 18:00. Nunca a las 7 am.
3. Para cada día sin Reel (máximo 3 por corrida), elegí un reloj disponible que NO tenga Reel programado y que no aparezca en
   `publicados.md` en los últimos 14 días. Preferí los que están en oferta y los que llevan más tiempo sin publicarse.
   Solo refs que tengan foto (`public/assets/disponibles/<ref>.webp` o `social/fotos/<ref>_*`).
4. Fotos: si no hay `social/fotos/<ref>_*`, agregá una línea `<ref> <número de modelo>` a `social/fotos/buscar.txt`
   (el número de modelo sale del nombre, p. ej. 49909), commit + push, esperá a que termine la acción
   `gh run list --workflow bajar-fotos.yml` (≈1 min) y `git pull`. Si no encuentra fotos, igual sirve la foto de la página.
5. Spec `social/engine/specs/<AAAA-MM-DD>-<ref>.json` (mirá `specs/v3-*.json` como ejemplo de estilo):
   `{"ref","name","price","oferta"(o null),"feats":[3 frases cortas ≤ 30 letras],"say":"..."}`
   - `price`/`oferta` de la hoja Web; `name` de disponibles.js.
   - `say`: 3–4 oraciones cortas en español tico, números en palabras: "<modelo corto>, [en oferta] a <precio en palabras> colones. <característica 1>. <característica 2>. <característica 3>."
     Solo datos que estén en la ficha `desc` de disponibles.js (nada inventado). El motor agrega solo "Original y con garantía. Apartalo con …, y escribinos al WhatsApp."
6. `python3 social/engine/make_reel.py social/engine/specs/<slug>.json` → `social/reels/reel-<slug>.mp4` y `.jpg` (≈2 min cada uno).
   Revisá el `.jpg` con Read (que se vea el reloj, el precio y el nombre sin cortarse).
7. Agregá la línea a `publicados.md`, `git add social && git commit && git push origin main`; comprobá con curl que el raw responda 200.
8. `createScheduledPost` (blogId 7542714) con providers facebook + instagram + tiktok, `facebookData {type: REEL}`,
   `instagramData {type: REEL, showReelOnFeed: true}`, `tiktokData {title: "<modelo> a ₡X" o "<modelo> en oferta", privacyOption: PUBLIC_TO_EVERYONE, commercialContentOwnBrand: true}`,
   `media: [raw mp4]`, `videoThumbnailUrl: raw jpg`, y este texto (montos con punto de miles):
   ```
   <name>
   <frase corta con 1 emoji>

   🔥 En oferta: ₡<oferta> (antes ₡<precio>)      ← o "⌚ ₡<precio>" si no hay oferta
   💳 Apartalo con ₡<adelanto> y pagalo en tractos   ← 25.000 si final ≥ 100.000; 20.000 si ≥ 50.000; si no 15.000
   🛡️ Original, con garantía de 3 meses
   🚚 Envíos a todo el país

   👉 Escribinos al WhatsApp 8640-0835 y es tuyo
   🌐 ticotimecr.com
   Ref. <ref>

   #relojescr #relojescostarica #invicta #invictacr #relojesoriginales #costarica   (Casio: #casio #casiocr en vez de invicta)
   ```
9. Resumen corto en español con SendUserMessage: qué Reels quedaron programados (fecha, hora, modelo, precio). Si no hacía falta ninguno, no mandes nada.

## Intro con IA (Everygen, opcional — cuesta créditos)
Receta probada (13 créditos por reloj, Venom Hydra 4-nov-2026):
1. `generate_image` modelo `gemini-3-pro-image-preview` (3 créditos), 9:16, `referenceImageUrls` = foto oficial del reloj (raw de GitHub),
   prompt: "EXACTLY the watch in the reference… keep every detail identical…" + escena de estudio oscuro con luz de borde del color del reloj, sin texto.
   Revisá la imagen antes de seguir (que el reloj sea idéntico).
2. `generate_video` modelo `Kling 3.0 Turbo`, 5 s, portrait, `firstFrameUrls` = esa imagen (10 créditos), prompt de cámara lenta
   que avanza y gira un poco, humo, brillo de luz; "keep the watch exactly the same".
3. Bajar el mp4 y la imagen con la acción (líneas `ai_<ref>_intro <url>` y `ai_<ref>_frame <url>` en `social/fotos/urls.txt`).
4. En el spec: `"intro":"social/fotos/ai_<ref>_intro.mp4","extra_photos":["social/fotos/ai_<ref>_frame.jpg"]`.
Solo hacerlo cuando Johel lo pida (gasta créditos de su plan).
