"""Fotos de la tienda (Disponibles).

Lee la pestaña "Web" de la hoja (la misma que usa la página), busca qué referencias
no tienen foto en public/assets/disponibles/ y las consigue:
  1. Si la referencia está en tools/fotos_tienda.txt  ->  "<ref> <url de la foto>"  o  "<ref> <sku invicta>"
  2. Si no, y el modelo es Invicta y trae el número (ej. "Invicta Aviator 28100"), la busca en invictastores.com
Guarda cada foto como public/assets/disponibles/<ref>.webp y escribe public/fotos.js con la lista
de referencias que tienen foto, para que la página la muestre aunque el reloj no esté en disponibles.js.
Para reemplazar una foto: borrar el .webp (o poner la línea en fotos_tienda.txt con "!" al inicio: "!543 <url>").
"""
import csv, io, json, os, re, sys, urllib.parse, urllib.request
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "public", "assets", "disponibles")
UA = {"User-Agent": "Mozilla/5.0"}


def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read()


def sheet_rows():
    js = open(os.path.join(ROOT, "public", "disponibles.js"), encoding="utf8").read()
    url = re.search(r'SHEET_CSV\s*=\s*"([^"]+)"', js).group(1)
    text = get(url).decode("utf8")
    rows = list(csv.reader(io.StringIO(text)))[1:]
    out = []
    for r in rows:
        ref = re.sub(r"\D", "", (r[0] if r else "") or "")
        if ref:
            out.append((int(ref), (r[1] if len(r) > 1 else "").strip()))
    return out


def manual():
    m = {}
    p = os.path.join(ROOT, "tools", "fotos_tienda.txt")
    if not os.path.exists(p):
        return m
    for line in open(p, encoding="utf8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) < 2:
            continue
        force = parts[0].startswith("!")
        ref = re.sub(r"\D", "", parts[0])
        if ref:
            m[int(ref)] = (parts[1].strip(), force)
    return m


def invicta_img(sku):
    j = json.loads(get("https://www.invictastores.com/search/suggest.json?q=" + urllib.parse.quote(sku)
                       + "&resources[type]=product&resources[limit]=5"))
    prods = [x for x in j["resources"]["results"].get("products", []) if sku in (x["title"] + x["handle"])]
    if not prods:
        return None
    d = json.loads(get("https://www.invictastores.com/products/" + prods[0]["handle"] + ".js"))
    if not d.get("images"):
        return None
    u = d["images"][0]
    u = "https:" + u if u.startswith("//") else u
    return u.split("?")[0] + "?width=1400"


def save_webp(data, ref):
    im = Image.open(io.BytesIO(data))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    # recortar el borde blanco sobrante y dejar un margen pequeño
    diff = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).convert("L").point(lambda v: 255 if v > 18 else 0)
    box = diff.getbbox()
    if box:
        pad = int(max(box[2] - box[0], box[3] - box[1]) * 0.04)
        box = (max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))
        im = im.crop(box)
    im.thumbnail((700, 700))
    im.save(os.path.join(DIR, f"{ref}.webp"), "WEBP", quality=84)


def main():
    rows = sheet_rows()
    man = manual()
    have = lambda r: os.path.exists(os.path.join(DIR, f"{r}.webp"))
    sin_foto = []
    for ref, modelo in rows:
        src, force = man.get(ref, (None, False))
        if have(ref) and not force:
            continue
        try:
            url = None
            if src:
                url = src if src.startswith("http") else invicta_img(re.sub(r"\D", "", src))
            elif re.search(r"invicta", modelo, re.I):
                skus = re.findall(r"\b\d{4,6}\b", modelo)
                for s in skus:
                    url = invicta_img(s)
                    if url:
                        break
            if not url:
                sin_foto.append((ref, modelo))
                print("SIN FOTO", ref, modelo)
                continue
            save_webp(get(url), ref)
            print("ok", ref, modelo, url)
        except Exception as e:
            sin_foto.append((ref, modelo))
            print("FALLO", ref, modelo, e)
    refs = sorted(int(f.split(".")[0]) for f in os.listdir(DIR) if re.fullmatch(r"\d+\.webp", f))
    with open(os.path.join(ROOT, "public", "fotos.js"), "w", encoding="utf8") as f:
        f.write("// Referencias con foto en assets/disponibles/ (lo genera tools/fotos_tienda.py)\n")
        f.write("window.FOTOS = " + json.dumps(refs) + ";\n")
    if sin_foto:
        print("\nFaltan fotos (agregalas en tools/fotos_tienda.txt como \"<ref> <url>\"):")
        for r, m in sin_foto:
            print(" ", r, m)


if __name__ == "__main__":
    main()
