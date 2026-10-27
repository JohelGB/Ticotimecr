// Relojes disponibles (entrega inmediata). Cada reloj es pieza única.
// Aquí van las fotos, descripciones y precios de respaldo. Lo que está disponible y su precio se leen de la hoja (ver abajo).
window.STOCK = [
  {ref:400,img:"assets/disponibles/400.webp",brand:"Invicta",name:"Invicta S1 Rally Dragon 49013",price:110000,c:"#1b1b1f",
   sub:"Automático · Esfera esqueleto · 41 mm",
   desc:["Movimiento automático: no usa batería, se carga con el movimiento de la muñeca.",
         "Esfera esqueleto con dragón dorado en relieve; se ve el mecanismo por dentro.",
         "Caja de 41 mm en acero inoxidable con bisel negro y tornillos dorados.",
         "Cristal Flame Fusion, resistente a rayones.",
         "Correa de silicón blanca, cómoda para uso diario.",
         "Resistente al agua 30 m: salpicaduras y lluvia, no para nadar.",
         "Garantía TicoTime de 3 meses."]},
  {ref:402,img:"assets/disponibles/402.webp",brand:"Invicta",name:"Invicta S1 Rally Interstellar 49009",price:105000,c:"#1f4f9a",
   sub:"Automático · Esfera esqueleto · 41 mm · Azul",
   desc:["Movimiento automático (calibre JX 2801): no usa batería, se carga con el movimiento de la muñeca.",
         "Esfera esqueleto con motivo espacial: la Tierra, la Luna y un astronauta, con el mecanismo a la vista.",
         "Caja de 41 mm en acero inoxidable negro con tornillos en el bisel.",
         "Cristal Flame Fusion, resistente a rayones.",
         "Correa de silicón azul con hebilla.",
         "Resistente al agua 30 m: salpicaduras y lluvia, no para nadar.",
         "Garantía TicoTime de 3 meses."]},
  {ref:404,img:"assets/disponibles/404.webp",brand:"Invicta",name:"Invicta S1 Rally Interstellar 49010",price:105000,c:"#1b1b1f",
   sub:"Automático · Esfera esqueleto · 41 mm · Blanco",
   desc:["Movimiento automático: no usa batería, se carga con el movimiento de la muñeca.",
         "Esfera esqueleto con motivo espacial: la Tierra, la Luna y un astronauta, con el mecanismo a la vista.",
         "Caja de 41 mm en acero inoxidable negro con tornillos en el bisel.",
         "Cristal Flame Fusion, resistente a rayones.",
         "Correa de silicón blanca con hebilla.",
         "Resistente al agua 30 m: salpicaduras y lluvia, no para nadar.",
         "Garantía TicoTime de 3 meses."]},
  {ref:489,img:"assets/disponibles/489.webp",brand:"Invicta",name:"Invicta Grand Diver 28950",price:63500,c:"#c9a245",
   sub:"Automático · Dorado · 200 m",
   desc:["Movimiento automático: no usa batería, se carga con el movimiento de la muñeca.",
         "Caja y brazalete en tono dorado.",
         "Esfera dorada con ventana de fecha.",
         "Bisel giratorio estilo buzo.",
         "Resistente al agua 200 m: sirve para nadar y hacer snorkel.",
         "Garantía TicoTime de 3 meses."]},
  {ref:491,img:"assets/disponibles/491.webp",brand:"Invicta",name:"Invicta Celestial Caelestis 48562",price:55000,c:"#e9e3d0",
   sub:"Multifunción · 45 mm · Dorado y acero · Cristales",
   desc:["Movimiento de cuarzo, a batería, con día, fecha y segundero.",
         "Caja redonda de 45 mm en acero inoxidable.",
         "Esfera con 126 cristales tipo pavé y bisel con 36 cristales.",
         "Brazalete de acero inoxidable de dos tonos, dorado y plateado, con cristales.",
         "Resistente al agua 50 m: salpicaduras, lluvia y piscina de vez en cuando; no para bucear.",
         "Garantía TicoTime de 3 meses."]},
  {ref:486,img:"assets/disponibles/486.webp",brand:"Invicta",name:"Invicta Speedway Torvane 49909",price:51500,c:"#c9a245",
   sub:"Cronógrafo · Dorado · 200 m",
   desc:["Cronógrafo con tres subesferas y ventana de fecha.",
         "Caja y brazalete en tono dorado, esfera dorada.",
         "Bisel taquimétrico, para medir velocidad.",
         "Resistente al agua 200 m: sirve para nadar y hacer snorkel.",
         "Garantía TicoTime de 3 meses."]},
  {ref:490,img:"assets/disponibles/490.webp",brand:"Invicta",name:"Invicta Aviator Blanco",price:48500,c:"#f2f2ee",
   sub:"Multifunción · Dorado y blanco",
   desc:["Caja en tono dorado y esfera blanca con tres subesferas, incluida la del día de la semana.",
         "Bisel con escalas de aviador (millas náuticas y kilómetros).",
         "Correa de silicón blanca con textura.",
         "Garantía TicoTime de 3 meses."]},
  {ref:323,img:"assets/disponibles/323.webp",brand:"Invicta",name:"Invicta Bolt Valkir 69796",price:62500,c:"#6fb7d8",
   sub:"Cronógrafo · 52 mm · Acero · Esfera celeste",
   desc:["Caja grande de 52 mm en acero, con el bisel de cable trenzado típico de la línea Bolt.",
         "Esfera celeste con cronógrafo y subesferas.",
         "Brazalete de acero a juego con la caja.",
         "Corona de presión.",
         "Cristal Flame Fusion, resistente a rayones.",
         "Garantía TicoTime de 3 meses."]},
  {ref:356,img:"assets/disponibles/356.webp",brand:"Invicta",name:"Invicta Bolt Dorado Esfera Negra",price:62500,c:"#1b1b1f",
   sub:"Cronógrafo · 52 mm · Dorado y negro",
   desc:["Movimiento de cuarzo VD54, a batería.",
         "Caja grande de 52 mm en acero inoxidable tono dorado, con el cable negro típico de la línea Bolt.",
         "Esfera negra con cronógrafo, tres subesferas y escala taquimétrica.",
         "Brazalete de acero en tono dorado.",
         "Garantía TicoTime de 3 meses."]},
  {ref:338,img:"assets/disponibles/338.webp",brand:"Invicta",name:"Invicta Venom Hydra 48237",price:60000,c:"#b3202a",
   sub:"Cronógrafo · 52 mm · Rojo y negro",
   desc:["Caja grande de 52 mm en acero con acabado rojo.",
         "Esfera de metal negra con números rojos, cronógrafo, subesfera de 24 horas y fecha.",
         "Bisel unidireccional.",
         "Corona de rosca, que sella mejor la caja.",
         "Cristal mineral.",
         "Correa de silicón negra con detalles rojos.",
         "Garantía TicoTime de 3 meses."]},
  {ref:423,img:"assets/disponibles/423.webp",brand:"Invicta",name:"Invicta Pro Diver Velsari 30602",price:60000,c:"#c9a245",
   sub:"Automático · 42 mm · Dorado",
   desc:["Movimiento automático japonés NH35A con 24 rubíes: no usa batería, se carga con el movimiento de la muñeca.",
         "Caja de 42 mm y brazalete en tono dorado.",
         "Esfera dorada con ventana de fecha, edición especial.",
         "Bisel giratorio estilo buzo.",
         "Garantía TicoTime de 3 meses."]},
  {ref:331,img:"assets/disponibles/331.webp",brand:"Invicta",name:"Invicta Aviator Ascend 39895",price:59900,c:"#3a3f47",
   sub:"50 mm · Oro rosa y gris",
   desc:["Caja de 50 mm en acero con acabado oro rosa.",
         "Esfera de metal gris con un avión de combate en relieve y números en oro rosa.",
         "Bisel unidireccional con textura.",
         "Corona de presión y cristal Flame Fusion, resistente a rayones.",
         "Correa de silicón gris.",
         "Garantía TicoTime de 3 meses."]},
  {ref:337,img:"assets/disponibles/337.webp",brand:"Invicta",name:"Invicta Aviator Skyshock 39304",price:58500,c:"#1fb5c4",
   sub:"50 mm · Negro y turquesa",
   desc:["Caja de 50 mm en acero con acabado negro.",
         "Esfera negra con tres subesferas plateadas, incluida la del día de la semana.",
         "Bisel con escalas de aviador (millas náuticas, kilómetros y libras).",
         "Corona de presión y cristal Flame Fusion, resistente a rayones.",
         "Correa de silicón color turquesa.",
         "Garantía TicoTime de 3 meses."]},
  {ref:367,img:"assets/disponibles/367.webp",brand:"Invicta",name:"Invicta Bolt Vanguard 46037",price:56500,c:"#e0b81f",
   sub:"Cronógrafo · 50 mm · Amarillo y negro",
   desc:["Caja de 50 mm en acero con acabado negro y el cable amarillo típico de la línea Bolt.",
         "Esfera de metal negra con cronógrafo, tres subesferas y fecha.",
         "Bisel fijo.",
         "Corona de presión y cristal Flame Fusion, resistente a rayones.",
         "Correa de silicón amarilla con detalles negros.",
         "Garantía TicoTime de 3 meses."]},
  {ref:208,img:"assets/disponibles/208.webp",brand:"Invicta",name:"Invicta Pro Diver House of Cards 50524",price:55000,c:"#1f6b4a",
   sub:"40 mm · Acero · Esfera de cartas",
   desc:["Movimiento de cuarzo japonés PC32, a batería.",
         "Caja de 40 mm en acero con corona de rosca.",
         "Esfera verde con diseño de cartas de póker y ventana de fecha.",
         "Bisel unidireccional negro.",
         "Cristal mineral y brazalete de acero inoxidable.",
         "Garantía TicoTime de 3 meses."]},
  {ref:317,img:"assets/disponibles/317.webp",brand:"Invicta",name:"Invicta Pro Diver México",price:49500,c:"#2e7d4a",
   sub:"Acero · Bisel verde y rojo · Sin segundero",
   desc:["Foto de referencia de un modelo muy parecido: el reloj disponible es la versión sin segundero. Pedinos fotos reales por WhatsApp.",
         "Bisel giratorio en verde y rojo, los colores de México.",
         "Esfera plateada con textura de olas y ventana de fecha.",
         "Caja y brazalete de acero.",
         "Garantía TicoTime de 3 meses."]},
  {ref:332,img:"assets/disponibles/332.webp",brand:"Invicta",name:"Invicta Pro Diver Impact 28003",price:49500,c:"#1f4f9a",
   sub:"Multifunción · 50 mm · Azul · 100 m",
   desc:["Movimiento de cuarzo IM-Q-168, a batería.",
         "Caja de 50 mm en acero inoxidable con bisel azul.",
         "Esfera azul con subesferas de día, fecha y 24 horas.",
         "Resistente al agua 100 m: sirve para nadar, no para bucear.",
         "Correa de silicón azul.",
         "Garantía TicoTime de 3 meses."]},
  {ref:479,img:"assets/disponibles/479.webp",brand:"Casio",name:"Casio MTP-E740-4AVDF Naranja",price:75000,c:"#e8722a",
   sub:"Día y fecha · Acero · Esfera naranja · 50 m",
   desc:["Movimiento de cuarzo japonés, a batería.",
         "Esfera naranja con ventana de día y fecha (el día se muestra en inglés o en español).",
         "Caja y brazalete de acero inoxidable.",
         "Resistente al agua 50 m: salpicaduras, lluvia y piscina de vez en cuando; no para bucear.",
         "Garantía TicoTime de 3 meses."]},
  {ref:480,img:"assets/disponibles/480.webp",brand:"Casio",name:"Casio MTP-1381D-7AVDF Plateado",price:49900,c:"#d9dbe0",
   sub:"Día y fecha · Acero · Esfera plateada · 50 m",
   desc:["Movimiento de cuarzo japonés, a batería.",
         "Esfera plateada con diseño radial, el día de la semana completo arriba y la fecha abajo.",
         "Caja y brazalete de acero inoxidable.",
         "Resistente al agua 50 m: salpicaduras, lluvia y piscina de vez en cuando; no para bucear.",
         "Nuevo. Garantía TicoTime de 3 meses."]},
  {ref:388,img:"assets/disponibles/388.webp",brand:"Casio",name:"Casio MTP-1370D-7A3VDF Blanco",price:49500,c:"#f2f2ee",
   sub:"Día y fecha · Acero · Esfera blanca · 50 m",
   desc:["Movimiento de cuarzo, a batería.",
         "Esfera blanca con el día de la semana completo arriba y la fecha abajo.",
         "Caja y brazalete de acero inoxidable.",
         "Resistente al agua 50 m: salpicaduras, lluvia y piscina de vez en cuando; no para bucear.",
         "Original y nuevo. Garantía TicoTime de 3 meses."]},
  {ref:349,img:"assets/disponibles/349.webp",brand:"Invicta",name:"Invicta Aviator Chase",price:48500,c:"#1b1b1f",
   sub:"Cronógrafo · Acero · Esfera negra",
   desc:["Foto real del reloj disponible, nuevo con su etiqueta.",
         "Esfera negra estilo aviador con números verdes luminosos.",
         "Cronógrafo con tres subesferas y ventana de fecha.",
         "Caja y brazalete de acero.",
         "Garantía TicoTime de 3 meses."]},
  {ref:419,img:"assets/disponibles/419.webp",brand:"Invicta",name:"Invicta Speedway Multifunción 46856",price:47000,c:"#2e7d4a",
   sub:"Multifunción · 42 mm · Dorado y verde",
   desc:["Caja de 42 mm con bisel de 12 lados en tono dorado.",
         "Esfera verde con subesferas de día, fecha y 24 horas.",
         "Brazalete en tono dorado a juego con la caja.",
         "Garantía TicoTime de 3 meses."]},
  {ref:494,img:"assets/disponibles/494.webp",brand:"Invicta",name:"Invicta Speedway 49334 Verde",price:47000,c:"#1f7a45",
   sub:"Dorado · Esfera verde · Segundero pequeño",
   desc:["Caja en tono dorado con bisel facetado de estilo moderno.",
         "Esfera verde con efecto rayos de sol y subesfera de segundos.",
         "Brazalete de acero en tono dorado a juego.",
         "Garantía TicoTime de 3 meses."]},
  {ref:407,img:"assets/disponibles/407.webp",brand:"Invicta",name:"Invicta Speedway Victorious 51137",price:45500,c:"#7fd0c4",
   sub:"42 mm · Acero · Esfera tiffany",
   desc:["Caja de 42 mm en acero con bisel de 12 lados.",
         "Esfera color tiffany con subesfera de segundos.",
         "Brazalete de acero a juego con la caja.",
         "Corona de presión y cristal mineral.",
         "Garantía TicoTime de 3 meses."]},
  {ref:443,img:"assets/disponibles/443.webp",brand:"Invicta",name:"Invicta Pro Diver 22095",price:45000,c:"#c9a245",
   sub:"Dorado · Bisel negro",
   desc:["Caja y brazalete de acero en tono dorado.",
         "Esfera dorada con textura y ventana de fecha.",
         "Bisel giratorio negro con números dorados.",
         "Garantía TicoTime de 3 meses."]},
  {ref:465,img:"assets/disponibles/465.webp",brand:"Invicta",name:"Invicta Pro Diver Visions from Above 51051",price:44500,c:"#2bb3a3",
   sub:"43 mm · Acero · Esfera de playa",
   desc:["Caja de 43 mm en acero.",
         "Esfera y bisel ilustrados con una escena de playa vista desde arriba: palmeras, arena, mar y bañistas.",
         "Ventana de fecha a las 3.",
         "Bisel giratorio estilo buzo.",
         "Brazalete de acero a juego con la caja.",
         "Garantía TicoTime de 3 meses."]},
  {ref:473,img:"assets/disponibles/473.webp",brand:"Invicta",name:"Invicta Speedway Multifunción 46855",price:42000,c:"#c9a245",
   sub:"Multifunción · 42 mm · Dorado",
   desc:["Caja de 42 mm con bisel de 12 lados, todo en tono dorado.",
         "Esfera dorada con subesferas de día, fecha y 24 horas.",
         "Brazalete en tono dorado a juego con la caja.",
         "Garantía TicoTime de 3 meses."]},
  {ref:447,img:"assets/disponibles/447.webp",brand:"Invicta",name:"Invicta Pro Diver Ironwave 47577",price:39900,c:"#c9a245",
   sub:"Multifunción · 46 mm · Dorado",
   desc:["Caja de 46 mm y brazalete en tono dorado.",
         "Esfera dorada con subesferas de día, fecha y 24 horas.",
         "Bisel giratorio negro con números dorados.",
         "Garantía TicoTime de 3 meses."]},
  {ref:422,img:"assets/disponibles/422.webp",brand:"Invicta",name:"Invicta Speedway Coeurlyn 48578 (set con pulsera)",price:39800,c:"#1b1b1f",
   sub:"Dama · 34 mm · Dorado y acero",
   desc:["Set de regalo: reloj de dama más pulsera de cadena con dije de corazón.",
         "Caja de 34 mm con bisel dorado de 12 lados.",
         "Esfera negra con índices dorados.",
         "Brazalete de dos tonos, dorado y acero.",
         "Garantía TicoTime de 3 meses."]},
  {ref:313,img:"assets/disponibles/313.webp",brand:"Invicta",name:"Invicta Pro Diver Digital 48370",price:39500,c:"#2b2f36",
   sub:"Analógico y digital · 46,5 mm · Acero · 50 m",
   desc:["Hora con agujas y pantalla digital al mismo tiempo (movimientos de cuarzo IM-D-002 e IM-Q-198), a batería.",
         "Caja de 46,5 mm en acero inoxidable con bisel giratorio negro.",
         "Esfera negra con detalles en turquesa.",
         "Brazalete de acero inoxidable.",
         "Resistente al agua 50 m: salpicaduras, lluvia y piscina de vez en cuando; no para bucear.",
         "Garantía TicoTime de 3 meses."]},
  {ref:347,img:"assets/disponibles/347.webp",brand:"Invicta",name:"Invicta Specialty Compass 34013",price:38500,c:"#1f4f9a",
   sub:"45 mm · Acero · Azul",
   desc:["Caja de 45 mm en acero plateado.",
         "Esfera negra con detalles blancos y azules.",
         "Bisel fijo en negro y blanco.",
         "Corona de presión.",
         "Correa de silicón azul.",
         "Garantía TicoTime de 3 meses."]},
  {ref:292,img:"assets/disponibles/292.webp",brand:"Dulunwe",name:"Dulunwe 6077 Automático",price:49500,c:"#e9e9e9",
   sub:"Automático · Dos tonos · Esfera de panal",
   desc:["Movimiento automático mecánico: no usa batería, se carga con el movimiento de la muñeca.",
         "Esfera plateada con textura de panal, índices dorados y ventana de fecha.",
         "Agujas e índices luminosos para ver la hora en la oscuridad.",
         "Bisel estriado dorado y brazalete de dos tonos, dorado y acero.",
         "Resistente al agua para uso diario: salpicaduras y lluvia.",
         "Garantía TicoTime de 3 meses."]},
  {ref:481,img:"assets/disponibles/481.webp",brand:"G-Shock",name:"Casio G-Shock DW-9052 Negro",price:53000,c:"#1b1b1f",
   sub:"Digital · Negro · 200 m",
   desc:["Reloj digital Casio G-Shock, resistente a golpes.",
         "Resistente al agua 200 m: sirve para nadar y hacer snorkel.",
         "Cronómetro de 1/100 de segundo, cuenta regresiva y varias alarmas.",
         "Calendario automático y segunda hora para otro país.",
         "Luz para ver la pantalla en la oscuridad.",
         "Batería de aproximadamente 2 años.",
         "Garantía TicoTime de 3 meses."]},
  {ref:308,img:"assets/disponibles/308.webp",brand:"Skmei",name:"Skmei Militar Analógico Digital",price:32000,c:"#2b2f36",
   sub:"Analógico y digital · Acero · Plateado",
   desc:["Hora con agujas y tres pantallas digitales.",
         "Cronómetro de 1/100 de segundo, cuenta regresiva y alarma.",
         "Tres husos horarios y bisel con ciudades del mundo.",
         "Luz EL para ver la pantalla en la oscuridad.",
         "Caja y brazalete de acero inoxidable.",
         "Resistente al agua 30 m: salpicaduras y lluvia, no para nadar.",
         "Garantía TicoTime de 3 meses."]},
  {ref:279,img:"assets/disponibles/279.webp",brand:"Activa",name:"Activa Summit ACW8082-014",price:33000,c:"#e0c41f",
   sub:"Digital · 50 mm · Unisex",
   desc:["Reloj digital deportivo de la línea Activa, de Invicta.",
         "Caja de 50 mm, unisex.",
         "Cronómetro de 1/100 de segundo, alarma, campanada por hora y día de la semana.",
         "Luz para ver la pantalla en la oscuridad.",
         "Resistente a golpes.",
         "Resistente al agua 3 bar (30 m): salpicaduras y lluvia, no para nadar.",
         "Garantía TicoTime de 3 meses."]},
];
/* Videos por referencia: "ref": "assets/videos/<ref>.mp4" (póster <ref>.jpg al lado) */
window.VIDEOS = {356:"assets/videos/356.mp4", 208:"assets/videos/208.mp4", 337:"assets/videos/337.mp4", 347:"assets/videos/347.mp4", 367:"assets/videos/367.mp4", 338:"assets/videos/338.mp4", 349:"assets/videos/349.mp4", 323:"assets/videos/323.mp4", 423:"assets/videos/423.mp4", 422:"assets/videos/422.mp4", 443:"assets/videos/443.mp4", 494:"assets/videos/494.mp4", 317:"assets/videos/317.mp4", 332:"assets/videos/332.mp4", 331:"assets/videos/331.mp4", 313:"assets/videos/313.mp4", 491:"assets/videos/491.mp4", 490:"assets/videos/490.mp4", 407:"assets/videos/407.mp4", 400:"assets/videos/400.mp4", 402:"assets/videos/402.mp4", 404:"assets/videos/404.mp4"};
window.WA = "50686400835";
/* Adelanto para apartar según el precio (con oferta si tiene): menos de ₡50.000 → ₡15.000; de ₡50.000 a ₡99.999 → ₡20.000; ₡100.000 o más → ₡25.000 */
window.apartado = function(p){ return p >= 100000 ? 25000 : p >= 50000 ? 20000 : 15000; };
window.SOCIAL = {tiktok:"https://www.tiktok.com/@ticotimecr", instagram:"https://www.instagram.com/ticotimecr"};

// Inventario en vivo: la lista de referencias y precios se lee de la pestaña "Web" de la hoja de Google
// (publicada como CSV): columnas ref, modelo, precio y oferta (precio de oferta, opcional). Las fotos y descripciones salen de la lista de arriba, emparejadas por referencia.
// Si la hoja no responde, la página usa la lista de arriba tal cual.
window.SHEET_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR3xKgoquWA_UmxVYaOq5sEkirjU5EurUTfgIOxSSOoPtCifBpTK9tdBa-0ujbwPz4u0v-nYLB3xYgJ/pub?gid=777001&single=true&output=csv";

(function(){
  function parseCSV(text){
    var rows=[], row=[], cell="", q=false;
    for (var i=0;i<text.length;i++){
      var ch=text[i];
      if (q){ if (ch=='"'){ if (text[i+1]=='"'){ cell+='"'; i++; } else q=false; } else cell+=ch; }
      else if (ch=='"') q=true;
      else if (ch==','){ row.push(cell); cell=""; }
      else if (ch=='\n'||ch=='\r'){ if (ch=='\r'&&text[i+1]=='\n') i++; row.push(cell); rows.push(row); row=[]; cell=""; }
      else cell+=ch;
    }
    if (cell!==""||row.length){ row.push(cell); rows.push(row); }
    return rows;
  }
  function guessBrand(name){
    if (/g-?\s?shock/i.test(name)) return "G-Shock";
    var w=(name.trim().split(/\s+/)[0]||"Otros"); return w.charAt(0).toUpperCase()+w.slice(1).toLowerCase();
  }
  function tidy(name){ name=name.trim(); return name.charAt(0).toUpperCase()+name.slice(1); }
  window.loadStock = function(){
    var base = window.STOCK.slice();
    if (!window.SHEET_CSV || !window.fetch) return Promise.resolve(base);
    var ctrl = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function(){ if (ctrl) ctrl.abort(); }, 7000);
    var url = window.SHEET_CSV + (window.SHEET_CSV.indexOf("?")>=0 ? "&" : "?") + "t=" + Date.now();
    return fetch(url, {cache:"no-store", signal: ctrl ? ctrl.signal : undefined})
      .then(function(r){ if (!r.ok) throw new Error("http "+r.status); return r.text(); })
      .then(function(text){
        var byRef = {}; base.forEach(function(s){ byRef[s.ref]=s; });
        var out = [], seen = {};
        parseCSV(text).slice(1).forEach(function(r){
          var ref = parseInt(String(r[0]||"").replace(/\D/g,""),10);
          var price = parseInt(String(r[2]||"").replace(/\D/g,""),10);
          if (!ref || !price || seen[ref]) return; seen[ref]=1;
          var offer = parseInt(String(r[3]||"").replace(/\D/g,""),10);
          var d = byRef[ref], c;
          if (d) { c = {}; for (var k in d) c[k]=d[k]; c.price = price; }
          else c = {ref:ref, brand:guessBrand(r[1]||""), name:tidy(r[1]||("Reloj "+ref)), price:price, c:"#2b2f36"};
          delete c.offer;
          if (offer > 0 && offer < price) c.offer = offer;
          out.push(c);
        });
        if (!out.length) throw new Error("vacío");
        return out;
      })
      .catch(function(){ return base; })
      .then(function(list){ list.forEach(function(s){ if (window.VIDEOS[s.ref]) s.video = window.VIDEOS[s.ref]; }); return list;
      })
      .catch(function(){ return base; })
      .then(function(list){ clearTimeout(timer); return list; });
  };
})();

