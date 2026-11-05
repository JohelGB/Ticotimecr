#!/usr/bin/env python3
"""Revisa las Ofertas del día (public/ofertas.js) y la pestaña Lujo (public/lujo.js) contra Amazon.
Corre en GitHub Actions (Amazon no bloquea las páginas de producto desde ahí).
- Ofertas: quita las que ya no tienen ≥15 % de descuento o no están disponibles y rellena hasta 30
  con candidatos de tools/ofertas_pool.txt (≥25 % de descuento, ≥8 de dama, máx. 8 por marca).
- Lujo: actualiza precio y "antes" de cada reloj; si se agota lo marca agotado (la página lo oculta).
No escribe dólares ni enlaces de Amazon en la página: solo colones.
"""
import json, math, os, re, random, sys, time, datetime, urllib.request
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
CR = datetime.timezone(datetime.timedelta(hours=-6))
TC, TAX, TRAIDA = 462, 1.07, 4000
N_OFERTAS, MIN_DAMA, MAX_MARCA, CANDIDATOS_POR_CORRIDA = 30, 8, 8, int(os.environ.get("CANDIDATOS", "150"))

def ganancia_oferta(usd):
    return 18000 if usd < 40 else 25000 if usd < 100 else 35000 if usd < 200 else 45000 if usd < 350 else 55000

def colones(usd, g):
    return int(math.ceil((usd * TAX * TC + TRAIDA + g) / 500.0) * 500)

def money(s):
    m = re.search(r"\$\s*([\d,]+\.?\d*)", s or "")
    return float(m.group(1).replace(",", "")) if m else None

FALLOS = [0]
def fetch(asin, tries=2):
    if FALLOS[0] >= 6:
        return None  # Amazon está frenando: no insistir en esta corrida
    t = time.time()
    for k in range(tries):
        try:
            req = urllib.request.Request(f"https://www.amazon.com/dp/{asin}", headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9", "Accept": "text/html"})
            html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
            if "captcha" in html.lower()[:20000] and "productTitle" not in html:
                raise RuntimeError("captcha")
            print(f"{asin} {time.time()-t:.1f}s", flush=True)
            FALLOS[0] = 0
            return html
        except Exception as e:
            time.sleep(3)
    FALLOS[0] += 1
    print(f"{asin} sin respuesta", flush=True)
    return None

def seg(html, marker, n=40000):
    i = html.find(marker)
    return html[i:i + n] if i >= 0 else ""

def parse(html):
    out = {"ok": False}
    m = re.search(r'id="productTitle"[^>]*>([^<]+)<', html)
    if not m:
        return out
    out["ok"] = True
    out["title"] = re.sub(r"\s+", " ", m.group(1)).strip()
    segs = [x for x in (seg(html, 'id="corePrice_feature_div"'), seg(html, 'id="corePriceDisplay_desktop_feature_div"'), seg(html, 'id="apex_desktop"')) if x]
    price = lst = None
    for sg in segs:
        box = BeautifulSoup(sg, "html.parser")
        if price is None:
            for sel in (".priceToPay .a-offscreen", ".apex-pricetopay-value .a-offscreen", ".a-price:not(.a-text-price) .a-offscreen"):
                el = box.select_one(sel)
                if el and money(el.get_text()):
                    price = money(el.get_text()); break
        if lst is None:
            for sel in (".apex-basisprice-value .a-offscreen", ".basisPrice .a-offscreen"):
                el = box.select_one(sel)
                if el and money(el.get_text()):
                    lst = money(el.get_text()); break
    if lst is None:
        m2 = re.search(r'(?:List Price|Typical price)[^$]{0,200}\$([\d,]+\.\d{2})', html)
        if m2: lst = float(m2.group(1).replace(",", ""))
    if lst is not None and price is not None and lst <= price: lst = None
    out["price"], out["list"] = price, lst
    avt = re.sub(r"<[^>]+>", " ", seg(html, 'id="availability"', 3000)).lower()
    out["available"] = out["price"] is not None and "currently unavailable" not in avt
    m = re.search(r"Item model number\s*</span>\s*<span[^>]*>\s*([^<]+)", html) or re.search(r"Item model number[^<]*</th>\s*<td[^>]*>\s*([^<]+)", html)
    out["model"] = (m.group(1).replace("\u200e", "").strip() if m else "")
    return out

LINEAS = {
    "Invicta": ["Pro Diver", "Speedway", "Bolt", "Angel", "Wildflower", "S1 Rally", "Aviator", "Specialty", "Reserve", "Venom", "Coalition Forces", "Objet D Art", "Subaqua", "I-Force", "Racing", "Vintage", "Celestial", "Lupah"],
    "Casio": ["Enticer", "Edifice", "Illuminator", "Duro", "Vintage", "Pro Trek", "Sheen"],
    "G-Shock": ["Mudmaster", "Rangeman", "Frogman", "Baby-G"],
    "Citizen": ["Eco-Drive", "Promaster", "Corso", "Chandler", "Brycen", "Axiom", "Sport Luxury"],
    "Seiko": ["5 Sports", "Presage", "Prospex", "Essentials", "Astron", "Coutura"],
    "Bulova": ["Marine Star", "Precisionist", "Lunar Pilot", "Sutton", "Surveyor", "Crystal", "Classic", "Maquina"],
}

def nombre(brand, title, model, cat):
    linea = next((l for l in LINEAS.get(brand, []) if l.lower() in title.lower()), "")
    mod = model.split()[0] if model else ""
    if not mod:
        m = re.search(r"\b([A-Z]{1,5}-?\d{2,5}[A-Z0-9-]*|\d{4,5})\b", title)
        mod = m.group(1) if m else ""
    n = " ".join(x for x in [brand, linea, mod] if x)
    if cat == "D" and "dama" not in n.lower():
        n += " Dama"
    return re.sub(r"\s+", " ", n).strip()

def main():
    t0 = time.time()
    now = datetime.datetime.now(CR)
    of_path = os.path.join(ROOT, "public/ofertas.js")
    raw = open(of_path, encoding="utf-8").read()
    items = [json.loads(l.strip().rstrip(",")) for l in raw.splitlines() if l.strip().startswith('{"id"')]
    disp = open(os.path.join(ROOT, "public/disponibles.js"), encoding="utf-8").read()
    pool = []
    for l in open(os.path.join(ROOT, "tools/ofertas_pool.txt"), encoding="utf-8"):
        if l.startswith("#") or not l.strip(): continue
        a, b, c, img, t = (l.rstrip("\n").split("|") + [""] * 5)[:5]
        pool.append({"asin": a, "brand": b, "cat": c, "img": img, "title": t})
    est_path = os.path.join(ROOT, "tools/ofertas_estado.json")
    est = json.load(open(est_path)) if os.path.exists(est_path) else {"offset": 0}

    # 1) revisar las actuales
    keep, salieron, cambios, verificadas = [], 0, 0, 0
    for e in items:
        asin = e["id"][2:]
        h = fetch(asin); time.sleep(random.uniform(1.5, 3.0))
        if h is None:
            keep.append(e); continue  # no se pudo revisar: se deja igual
        d = parse(h)
        print("actual", asin, "ok" if d["ok"] else "noparse", "disp" if d.get("available") else "nodisp", "lista" if d.get("list") else "sinlista", flush=True)
        if not d["ok"]:
            keep.append(e); continue  # página rara (captcha o cambio): se deja igual
        verificadas += 1
        if not d["available"] or not d["list"]:
            salieron += 1; continue
        g = ganancia_oferta(d["price"])
        price, antes = colones(d["price"], g), colones(d["list"], g)
        off = round((1 - price / antes) * 100)
        if off < 15:
            salieron += 1; continue
        if (price, antes) != (e["price"], e["antes"]): cambios += 1
        e.update(price=price, antes=antes, off=off)
        keep.append(e)

    # 2) rellenar con candidatos del pool (rotando)
    usados = {e["id"][2:] for e in keep}
    nuevos = 0
    if len(keep) < N_OFERTAS and pool:
        off0 = est.get("offset", 0) % len(pool)
        orden = pool[off0:] + pool[:off0]
        revisados = 0
        for cnd in orden:
            if len(keep) >= N_OFERTAS or revisados >= CANDIDATOS_POR_CORRIDA: break
            a = cnd["asin"]
            if a in usados or a in disp: continue
            marca_n = sum(1 for e in keep if e["brand"] == cnd["brand"])
            damas = sum(1 for e in keep if e["cat"] == "D")
            faltan = N_OFERTAS - len(keep)
            if marca_n >= MAX_MARCA: continue
            if cnd["cat"] == "H" and MIN_DAMA - damas >= faltan: continue
            revisados += 1
            h = fetch(a); time.sleep(random.uniform(1.5, 3.0))
            if not h: continue
            d = parse(h)
            print("cand", a, "ok" if d["ok"] else "noparse", "disp" if d.get("available") else "nodisp", "lista" if d.get("list") else "sinlista", (f"{round((1-d['price']/d['list'])*100)}%" if d.get("list") and d.get("price") else ""), flush=True)
            if not d["ok"] or not d["available"] or not d["list"] or d["price"] < 20: continue
            if (1 - d["price"] / d["list"]) < (0.20 if cnd["brand"] == "Invicta" else 0.25): continue
            m5 = re.search(r"\b(\d{4,5})\b", d.get("model", ""))
            if cnd["brand"] == "Invicta" and m5 and m5.group(1) in disp: continue
            g = ganancia_oferta(d["price"])
            price, antes = colones(d["price"], g), colones(d["list"], g)
            off = round((1 - price / antes) * 100)
            if off < 15: continue
            keep.append({"id": "A-" + a, "name": nombre(cnd["brand"], d["title"], d["model"], cnd["cat"]), "cat": cnd["cat"], "brand": cnd["brand"],
                         "price": price, "antes": antes, "off": off, "img": f"https://m.media-amazon.com/images/I/{cnd['img']}._AC_SL600_.jpg", "eta": "15 a 20 días"})
            usados.add(a); nuevos += 1
        est["offset"] = (off0 + revisados + 1) % len(pool)

    keep.sort(key=lambda e: -e["off"])
    out = "/* TicoTime CR — Ofertas del día. Se actualiza automáticamente. */\nwindow.OFERTAS = {\n  revisado: \"%s\",\n  items: [\n%s\n  ]\n};\n" % (
        (now.strftime("%Y-%m-%dT%H:%M:00-06:00") if verificadas >= max(5, len(items) // 3) else re.search(r'revisado: "([^"]+)"', raw).group(1)), ",\n".join("    " + json.dumps(e, ensure_ascii=False) for e in keep))
    open(of_path, "w", encoding="utf-8").write(out)
    json.dump(est, open(est_path, "w"))
    print(f"Ofertas: {verificadas} verificadas, {len(keep)} en total, {nuevos} nuevas, {salieron} salieron, {cambios} cambiaron de precio")

    # 3) lujo
    src_path = os.path.join(ROOT, "tools/lujo_src.json")
    lj_path = os.path.join(ROOT, "public/lujo.js")
    if os.path.exists(src_path) and os.path.exists(lj_path):
        src = json.load(open(src_path, encoding="utf-8"))
        t = open(lj_path, encoding="utf-8").read()
        L = [json.loads(l.strip().rstrip(",")) for l in t.splitlines() if l.strip().startswith('{"id"')]
        ch = 0
        for e in L:
            cfg = src.get(e["id"][2:])
            if not cfg: continue
            h = fetch(e["id"][2:]); time.sleep(random.uniform(1.5, 3.0))
            if not h: continue
            d = parse(h)
            if not d["ok"] or not d["available"]:
                if not e.get("agotado"): e["agotado"] = True; ch += 1
                continue
            e.pop("agotado", None)
            price = colones(d["price"], cfg["g"])
            antes = colones(d["list"], cfg["g"]) if d["list"] and d["list"] > d["price"] * 1.05 else None
            if price != e["price"] or antes != e.get("antes"): ch += 1
            e["price"] = price
            if antes: e["antes"] = antes
            else: e.pop("antes", None)
        head = t[:t.index("window.LUJO")]
        open(lj_path, "w", encoding="utf-8").write(head + "window.LUJO = [\n" + ",\n".join("  " + json.dumps(e, ensure_ascii=False) for e in L) + "\n];\n")
        print(f"Lujo: {len(L)} relojes, {ch} cambios")

if __name__ == "__main__":
    main()
