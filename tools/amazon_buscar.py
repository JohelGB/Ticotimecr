#!/usr/bin/env python3
"""Busca en Amazon (desde GitHub Actions) y guarda resultados en tools/amazon_resultados.json.
tools/amazon_buscar.txt: una búsqueda por línea (o 'asin:B0XXXX' para leer un producto puntual)."""
import json, os, re, time, urllib.request, urllib.parse
from bs4 import BeautifulSoup
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
def get(u):
    for k in range(3):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9", "Accept": "text/html"})
            h = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")
            if "captcha" in h.lower()[:20000] and "s-result-item" not in h and "productTitle" not in h: raise RuntimeError("captcha")
            return h
        except Exception as e:
            print("reintento", u[:80], e); time.sleep(4 + 4 * k)
    return ""
out = {}
for q in [l.strip() for l in open(os.path.join(ROOT, "tools/amazon_buscar.txt")) if l.strip() and not l.startswith("#")]:
    res = []
    for page in (1, 2):
        h = get("https://www.amazon.com/s?" + urllib.parse.urlencode({"k": q, "page": page}))
        s = BeautifulSoup(h, "html.parser")
        for d in s.select("div[data-asin][data-component-type=s-search-result]"):
            a = d.get("data-asin"); t = d.select_one("h2"); p = d.select_one(".a-price .a-offscreen"); im = d.select_one("img.s-image")
            if not (a and t and p and im): continue
            pr = re.sub(r"[^\d.]", "", p.text)
            rt = d.select_one("span.a-icon-alt"); nr = d.select_one("span.a-size-base.s-underline-text")
            res.append({"asin": a, "title": t.get_text(" ", strip=True), "usd": float(pr) if pr else None,
                        "img": im.get("src"), "rating": rt.text if rt else "", "reviews": nr.text if nr else ""})
        time.sleep(3)
    print(q, len(res)); out[q] = res
json.dump(out, open(os.path.join(ROOT, "tools/amazon_resultados.json"), "w"), ensure_ascii=False, indent=1)
