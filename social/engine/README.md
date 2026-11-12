# Reels automáticos de relojes disponibles (TicoTime CR)

Video vertical 1080×1920 de ~20–24 s por reloj disponible: precio grande desde el primer segundo,
fotos que se deslizan y se mueven, 3 características que aparecen una por una, voz de hombre tico
(edge-tts `es-CR-JuanNeural`), música sintetizada de fondo y cierre con "Apartalo con ₡X" + WhatsApp 8640-0835.
Se publica en Instagram + Facebook (Reel) + TikTok con Metricool, usando el enlace raw de GitHub del video.

## 🎄 TEMPORADA NAVIDEÑA (del 12 de noviembre al 24 de diciembre de 2026) — MANDA SOBRE EL PROCEDIMIENTO NORMAL
Johel quiere que TODA la campaña se enfoque en **regalos de Navidad**: ganchos de regalo, opciones para regalar,
promocionar el WhatsApp **8640-0835** y **ticotimecr.com**, los modelos disponibles, y siempre decir que
**conseguimos cualquier modelo** por encargo. Desde el 25 de diciembre se vuelve al procedimiento normal.

### A. Reel diario de un reloj (martes, miércoles, viernes, sábado y domingo)
Igual que el procedimiento normal, pero el spec lleva además:
- `"navidad": true` → el motor pone la etiqueta roja "REGALO DE NAVIDAD" (o "REGALO EN OFERTA"), nieve suave, el gancho en
  rojo los primeros 2 s, y el cierre con WhatsApp + ticotimecr.com + "¿Buscás otro modelo? ¡Te lo conseguimos!". La voz agrega sola
  el número, la página y "si buscás otro modelo, te lo conseguimos".
- `"gancho"`: pregunta corta (≤ 34 letras) que se lee arriba del reloj. Rotá y no repitás el de los últimos 3 Reels:
  "¿No sabés qué regalarle a él?" · "¿Ya tenés el regalo de papá?" · "El regalo que sí va a usar" · "¿Regalo para tu novio?" ·
  "Regalo de Navidad listo" · "¿Qué le regalás a tu hermano?" · "Regalo para el que lo tiene todo" · "¿Intercambio de regalos?"
  (reloj de dama: "¿No sabés qué regalarle a ella?" · "El regalo para mamá" · "¿Regalo para tu novia?").
- `"say"` empieza con el gancho dicho en voz (p. ej. "¿No sabés qué regalarle a él esta Navidad?") y después el modelo,
  el precio y DOS características (no tres: el cierre navideño es más largo).
- Ejemplo: `specs/muestra-navidad-367.json`. Motor: `make_reel.py` (el mismo).

### B. Reel "opciones de regalo" (LUNES y JUEVES, 19:00) — reemplaza el Reel de un reloj de ese día
Un solo video con 3 (o 4) relojes disponibles: gancho → "OPCIÓN 1, 2, 3" con foto y precio → cierre con todos,
"¿Buscás otro modelo? ¡Te lo conseguimos!", WhatsApp y página. Motor: `python3 social/engine/make_regalos.py specs/<AAAA-MM-DD>-regalos.json`
(≈1,5 min). Ejemplo: `specs/muestra-regalos-el.json`.
- Spec: `{"titulo":"3 regalos para él","sub":"por menos de ₡50.000","voz_intro":"¿No sabés qué regalarle a él esta Navidad? Aquí tenés tres opciones por menos de cincuenta mil colones.","items":[{"ref","name","price","oferta","say":"Opción uno: <modelo corto>, a <precio en palabras>."}, ...]}`
- Temas (rotá, no repitás el anterior): "3 regalos para él · por menos de ₡50.000" · "Regalos por menos de ₡40.000" ·
  "Regalos que brillan · dorados" · "Para el que lo tiene todo" (los de mayor precio) · "Regalos en oferta" (si hay ≥3 con oferta) ·
  "3 regalos para ella" (solo si hay ≥3 de dama disponibles).
- Solo relojes de la hoja Web con foto, con el precio de HOY (si tiene oferta, va la oferta). Que el `sub` sea verdad (revisá los precios).
- Revisá con Read un cuadro de cada parte (gancho, una opción y el cierre) antes de publicar.
- tiktokData.title: el `titulo` (p. ej. "3 regalos para él por menos de ₡50.000").
- En la cola de Metricool, un día cuenta como cubierto si ya tiene un Reel con "Ref. N" o con "1️⃣" (Reel de opciones).
- En `publicados.md` anotalo con ref `REGALOS` y en modelo el título + las refs (p. ej. "3 regalos para él: 494, 407, 532").

### C. Texto de la publicación en temporada navideña (reemplaza el del paso 8)
Reel de un reloj:
```
🎁 <gancho>
<name>

⌚ ₡<precio>        ← o "🔥 Precio web: ₡<oferta> (antes ₡<precio>) · solo en ticotimecr.com"
💳 Apartalo con ₡<adelanto> y terminás de pagar con el aguinaldo
🛡️ Original, con garantía de 3 meses
🚚 Envíos a todo el país
🔎 ¿Buscás otro modelo? Te lo conseguimos por encargo

👉 Escribinos al WhatsApp 8640-0835
🌐 Mirá todos los disponibles en ticotimecr.com
⚡ Cada día un reloj distinto a precio relámpago: el Reloj del día, solo en la página
Ref. <ref>

#regalosdenavidad #navidadcr #regalosparaél #relojescr #relojescostarica #invicta #relojesoriginales #costarica
```
Reel de opciones: igual, pero arriba "🎁 <titulo> <sub>" y una línea por reloj: "1️⃣ <modelo> · ₡<precio> (Ref. N)", sin "Ref." al final.

### Campaña "visitá la página" (desde 12-nov-2026)
- Las ofertas se llaman **"Precio web"** (la etiqueta del video ya lo dice cuando el reloj tiene oferta).
- Todos los textos llevan la línea del **Reloj del día** (ver plantilla arriba) y "🌐 ticotimecr.com".
- La página muestra la rifa con los números libres en vivo: en los textos de rifa poné "Mirá los números libres en ticotimecr.com".

### D. Reels elegantes con IA (martes y viernes) en temporada
Mismo procedimiento, pero el texto empieza con "🎁 ¿Cuánto creés que cuesta este regalo?" y antes de los hashtags agrega
"🔎 ¿Buscás otro modelo? Te lo conseguimos" y "🌐 Mirá todos los disponibles en ticotimecr.com". Escenas con ambiente navideño
cuando se pueda (luces de Navidad desenfocadas al fondo, caja de regalo abierta junto al reloj, árbol iluminado), sin texto.

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

## Reels ELEGANTES con IA (tarea "Reels elegantes IA", martes y viernes)
Estilo marca de lujo: clip de IA de 15 s a pantalla completa, letra fina (Lora), juego "¿Cuánto creés que cuesta?",
cierre azul marino con logo TicoTime y precio revelado. Motor: `social/engine/make_elegante.py` (ejemplo: `specs/2026-11-04-402-elegante.json`).
Costo objetivo: **13 créditos** (foto 3 + video 10). Plan Starter: 200 créditos al mes (renueva el día 4).

1. Créditos: `get_credit_balance`. Si quedan **menos de 20**, NO generes nada y avisá a Johel en una línea.
2. Elegí UN reloj de la hoja Web (preferí los de mayor precio o en oferta, con fotos oficiales en `social/fotos/<ref>_*`)
   que no tenga Reel elegante en los últimos 30 días (`publicados.md`, filas con "elegante") ni Reel normal programado ese mismo día o el siguiente.
3. Escena (variá; no repitas la de los últimos 3 elegantes): mano en volante de noche · muñeca sobre mesa de café con taza ·
   escritorio de oficina con laptop · atardecer en la playa (Guanacaste) · bar/terraza de noche · chaqueta de cuero en la ciudad · mano sobre la mesa de un restaurante.
   Reloj de dama → muñeca de mujer.
4. Foto (3 créditos): `generate_image` modelo `gemini-3-pro-image-preview`, 9:16, `referenceImageUrls` = 1–2 fotos oficiales (raw de GitHub).
   Prompt: "Close-up cinematic photograph… ONE <left> hand/wrist … wearing EXACTLY the watch in the reference images (<descripción>)…
   keep every detail identical… tight close-up, the watch is the hero and fills about half of the frame width, in the center,
   dial facing the camera, anatomically correct, one hand only… <escena>… No text, no extra logos, no faces."
   Bajala con la acción (línea `ai_<ref>_<escena> <url>` en `social/fotos/urls.txt`, push, esperar `gh run`, pull) y REVISALA con Read:
   una sola mano lógica, reloj grande e idéntico al original. Si está mal, UN solo reintento corrigiendo el prompt. Si vuelve a salir mal, pará y avisá.
5. Video (10 créditos): `generate_video` modelo **`MiniMax H3 Max Turbo`**, duration 15, resolution 720p, orientation 9:16,
   `firstFrameUrls` = esa foto, idempotencyKey único. Prompt: una sola toma continua, cámara que se acerca lentamente hasta que la esfera
   llena el cuadro, luces/reflejos que pasan, mano relajada con movimientos mínimos, "keep the watch exactly the same… no morphing, no extra hands, no text".
   Esperá con `wait_for_generation`, bajalo con la acción y revisá 6–8 cuadros (ffmpeg) antes de usarlo. Si el reloj se deforma, no lo publiqués y avisá.
6. Spec `specs/<AAAA-MM-DD>-<ref>-elegante.json`: `{"ref","name"(corto, sin número),"line":"<3 datos cortos con ·>","price","oferta","clip":"social/fotos/ai_<ref>_<escena>.mp4","feats":[3 frases de la ficha],"pregunta":"¿Cuánto creés que cuesta?"}`
   y `python3 social/engine/make_elegante.py social/engine/specs/<slug>.json`. Revisá la portada y un cuadro del cierre (precio legible).
7. Commit + push, línea en `publicados.md` (con "(elegante IA)"), y `createScheduledPost` el MISMO día a las **20:00** en facebook + instagram + tiktok,
   Reel, `instagramData.isAiGenerated: true`, `tiktokData {title:"¿Cuánto creés que cuesta?", isAigc:true, privacyOption:PUBLIC_TO_EVERYONE, commercialContentOwnBrand:true}`.
   Texto: "¿Cuánto creés que cuesta este <modelo>? 🤔 Pausá, comentá tu respuesta y después mirá el final del video." + 1 línea de características +
   "🛡️ 100 % original, con garantía de 3 meses / 💳 Apartalo y pagalo en tractos / 🚚 Envíos a todo el país / 👉 Escribinos al WhatsApp 8640-0835 / 🌐 ticotimecr.com / Ref. <ref>" + hashtags.
8. SendUserMessage corto: reloj, escena, hora de publicación, créditos gastados y créditos restantes.
