#!/usr/bin/env python3
"""Lee productos de Amazon desde GitHub Actions y guarda tools/amazon_resultados.json.
tools/amazon_buscar.txt: ASINs semilla (uno por línea). Línea 'filtro: palabra' = solo seguir
enlaces relacionados cuyo texto contenga esa palabra. Línea 'max: N' = cuántos productos leer."""
import json, os, re, time, urllib.request
from bs4 import BeautifulSoup
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
lines = [l.strip() for l in open(os.path.join(ROOT, "tools/amazon_buscar.txt")) if l.strip() and not l.startswith("#")]
filtro = [l.split(":", 1)[1].strip().lower() for l in lines if l.lower().startswith("filtro:")]
mx = int(([l.split(":", 1)[1] for l in lines if l.lower().startswith("max:")] or ["40"])[0])
cola = [l for l in lines if re.fullmatch(r"[A-Z0-9]{10}", l)]
vistos, out, fallos = set(), [], 0
def get(asin):
    req = urllib.request.Request(f"https://www.amazon.com/dp/{asin}", headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9", "Accept": "text/html"})
    h = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")
    if "productTitle" not in h: raise RuntimeError("captcha/sin producto")
    return h
while cola and len(out) < mx and fallos < 8:
    a = cola.pop(0)
    if a in vistos: continue
    vistos.add(a)
    try: h = get(a)
    except Exception as e:
        fallos += 1; print("fallo", a, e); time.sleep(5); continue
    s = BeautifulSoup(h, "html.parser")
    t = s.select_one("#productTitle"); t = t.get_text(" ", strip=True) if t else ""
    p = s.select_one("#corePrice_feature_div .a-offscreen, #corePriceDisplay_desktop_feature_div .a-offscreen, .a-price .a-offscreen")
    usd = float(re.sub(r"[^\d.]", "", p.text)) if p and re.search(r"\d", p.text) else None
    m = re.search(r'"hiRes":"(https://m\.media-amazon\.com/images/I/[^"]+)"', h) or re.search(r'"large":"(https://m\.media-amazon\.com/images/I/[^"]+)"', h)
    av = s.select_one("#availability"); av = av.get_text(" ", strip=True) if av else ""
    br = s.select_one("#bylineInfo"); br = br.get_text(" ", strip=True) if br else ""
    bullets = [li.get_text(" ", strip=True) for li in s.select("#feature-bullets li")][:6]
    out.append({"asin": a, "title": t, "usd": usd, "img": m.group(1) if m else "", "disp": av, "marca": br, "bullets": bullets})
    print("ok", a, usd, t[:70], flush=True)
    for x in s.select('a[href*="/dp/"]'):
        mm = re.search(r"/dp/([A-Z0-9]{10})", x.get("href", "")); tx = (x.get_text(" ", strip=True) + " " + x.get("href", "")).lower()
        if mm and mm.group(1) not in vistos and (not filtro or any(f in tx for f in filtro)): cola.append(mm.group(1))
    time.sleep(2)
json.dump(out, open(os.path.join(ROOT, "tools/amazon_resultados.json"), "w"), ensure_ascii=False, indent=1)
print(len(out), "productos")
