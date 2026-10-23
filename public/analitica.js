/* Google Analytics 4 (G-5JVMW5Z8YM) + eventos de la tienda TicoTime */
(function(){
  var ID = "G-5JVMW5Z8YM";
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function(){ dataLayer.push(arguments); };
  gtag("js", new Date());
  gtag("config", ID);
  var s = document.createElement("script"); s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + ID; document.head.appendChild(s);

  function item(w){ if(!w) return null; var p = w.offer || w.price || 0;
    return {item_id: String(w.ref), item_name: w.name, item_brand: w.brand || "", price: p, quantity: 1, item_category: w.offer ? "Oferta" : "Disponible"}; }
  /* Uso desde la tienda: ttTrack("add_to_cart", reloj) o ttTrack("begin_checkout", [relojes], {payment_type:"Apartado"}) */
  window.ttTrack = function(ev, w, extra){
    try {
      var list = Array.isArray(w) ? w.map(item).filter(Boolean) : (w ? [item(w)] : []);
      var params = {currency: "CRC", value: list.reduce(function(t,i){ return t + i.price; }, 0), items: list};
      if (extra) for (var k in extra) params[k] = extra[k];
      gtag("event", ev, params);
    } catch(e){}
  };
  function ev(name, params){ try { gtag("event", name, params || {}); } catch(e){} }

  /* Clics generales en todas las páginas */
  document.addEventListener("click", function(e){
    var a = e.target.closest && e.target.closest("a"); if (!a) return;
    var h = a.getAttribute("href") || "";
    if (/tiktok\.com/.test(h)) return ev("click_red_social", {red: "TikTok", ubicacion: a.closest("header") ? "encabezado" : "pie"});
    if (/instagram\.com/.test(h)) return ev("click_red_social", {red: "Instagram", ubicacion: a.closest("header") ? "encabezado" : "pie"});
    if (/wa\.me/.test(h)) {
      if (a.id === "send") return; /* el pedido del carrito se mide aparte */
      var m = decodeURIComponent(h).match(/referencia\s+(\d+)/i);
      if (m) return ev("generate_lead", {metodo: "Cotizar catálogo", referencia: m[1], pagina: location.pathname});
      return ev("generate_lead", {metodo: "WhatsApp", pagina: location.pathname, boton: (a.textContent || "").trim().slice(0, 40)});
    }
    if (a.classList.contains("section-card")) return ev("select_content", {content_type: "coleccion", item_id: h.replace(".html", "")});
    if (/\.pdf/.test(h)) return ev("abrir_pdf", {pagina: location.pathname});
    var vr = h.match(/#(?:video|ref)-(\d+)/);
    if (vr) return ev("select_item", {item_list_name: a.closest("#videos") ? "Portada - En video" : a.closest("#heroShow") ? "Portada - Vitrina" : "Portada - Disponibles", items: [{item_id: vr[1]}]});
  }, true);

  /* Reproducción de videos de relojes */
  document.addEventListener("play", function(e){
    var v = e.target; if (!v || v.tagName !== "VIDEO") return;
    var m = (v.currentSrc || v.src || "").match(/videos\/(\d+)\.mp4/);
    ev("video_play", {referencia: m ? m[1] : "", ubicacion: v.id === "hsVid" ? "vitrina portada" : "detalle tienda", automatico: v.id === "hsVid"});
  }, true);
})();
