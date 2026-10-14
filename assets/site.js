/* NLS Paint — JS comum a todas as páginas (menu, pincelada, antes/depois, lightbox, formulário, mapa estático).
   Efeitos exclusivos da home (galeria presa e gota que vira mapa) ficam em home.js. */
(function(){
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var PAGE = document.body.getAttribute('data-page') || 'other';
  var clamp = function(v,a,b){ return Math.min(b==null?1:b, Math.max(a||0, v)); };
  var range = function(p,a,b){ return clamp((p-a)/(b-a)); };
  var ease = function(t){ return t<.5 ? 2*t*t : 1-Math.pow(-2*t+2,2)/2; };
  var easeOut = function(t){ return 1-Math.pow(1-t,3); };
  var $ = function(s, r){ return (r || document).querySelector(s); };
  var $$ = function(s, r){ return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function onFrame(fn){ var q=false; function run(){ q=false; fn(); } function req(){ if(!q){ q=true; requestAnimationFrame(run); } } addEventListener('scroll',req,{passive:true}); addEventListener('resize',req); req(); }
  function inView(els, fn, th){
    if (!('IntersectionObserver' in window)) { els.forEach(fn); return; }
    var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting){ io.unobserve(e.target); fn(e.target); } }); }, {threshold: th || .4, rootMargin: '0px 0px -30% 0px'});
    els.forEach(function(el){ io.observe(el); });
  }

  /* ---------- menu + dropdown ---------- */
  var burger = $('.burger');
  burger.addEventListener('click', function(){
    var open = document.body.classList.toggle('menu-open');
    burger.setAttribute('aria-expanded', open);
  });
  var dd = $('.dd');
  if (dd){
    var ddb = dd.querySelector('button');
    ddb.addEventListener('click', function(e){ e.stopPropagation(); var o = dd.classList.toggle('open'); ddb.setAttribute('aria-expanded', o); });
    document.addEventListener('click', function(e){ if (!dd.contains(e.target)){ dd.classList.remove('open'); ddb.setAttribute('aria-expanded', false); } });
    addEventListener('keydown', function(e){ if (e.key === 'Escape'){ dd.classList.remove('open'); ddb.setAttribute('aria-expanded', false); } });
  }

  /* ---------- voltar ao topo ---------- */
  var toTop = $('#toTop');
  onFrame(function(){ toTop.classList.toggle('on', scrollY > innerHeight * .8); });
  toTop.addEventListener('click', function(e){ e.preventDefault(); scrollTo({top:0, behavior: reduced ? 'auto' : 'smooth'}); });

  /* ---------- notas do protótipo ---------- */
  var nb = $('#notesBtn');
  nb.addEventListener('click', function(){ var on = document.body.classList.toggle('notes'); nb.setAttribute('aria-pressed', on); nb.textContent = on ? '✕ Esconder notas' : '📝 Notas do protótipo'; });

  /* ---------- eventos GA4 (simulados) com page_type ---------- */
  function track(name, params){
    params = Object.assign({page_type: PAGE, page: location.pathname}, params || {});
    if (window.gtag) gtag('event', name, params); else console.log('[GA4]', name, params);
  }
  window.NLS_TRACK = track;
  document.addEventListener('click', function(e){ var a = e.target.closest('[data-ev]'); if (a) track(a.getAttribute('data-ev')); });

  /* ---------- efeito 5: pincelada ---------- */
  var BR = {d:'M10 24 C 70 15, 170 12, 292 20', w:14, streaks:[[-5,2.5],[4,2],[7,1.5]]};
  var kws = $$('.kw'), uid = 0;
  kws.forEach(function(el){
    var id = 'br' + (uid++), color = el.getAttribute('data-color') || '#9E1B24';
    var streaks = BR.streaks.map(function(s){ return '<path d="' + BR.d + '" pathLength="1" transform="translate(0 ' + s[0] + ')" stroke="' + color + '" stroke-width="' + s[1] + '" opacity=".55" fill="none" stroke-linecap="round"/>'; }).join('');
    el.insertAdjacentHTML('beforeend', '<svg class="brush" viewBox="0 0 300 40" preserveAspectRatio="none" aria-hidden="true"><defs><filter id="' + id + 'f" x="-10%" y="-40%" width="120%" height="180%"><feTurbulence type="fractalNoise" baseFrequency=".05 .4" numOctaves="2" seed="' + uid + '"/><feDisplacementMap in="SourceGraphic" scale="7"/></filter></defs><g filter="url(#' + id + 'f)"><path d="' + BR.d + '" pathLength="1" stroke="' + color + '" stroke-width="' + BR.w + '" fill="none" stroke-linecap="round"/>' + streaks + '</g></svg>');
  });
  // títulos dentro do hero aparecem já pintados (sem atrasar o LCP)
  kws.forEach(function(el){ if (el.closest('.hero,.about-hero')) setTimeout(function(){ el.classList.add('drawn'); }, reduced ? 0 : 350); });
  inView(kws.filter(function(el){ return !el.closest('.hero,.about-hero'); }), function(el){ if (reduced) el.classList.add('drawn'); else setTimeout(function(){ el.classList.add('drawn'); }, 250); }, 1);


  /* ---------- antes e depois ---------- */
  $$('.ba').forEach(function(ba){
    var manual = false, dragging = false;
    function setX(pct){ ba.style.setProperty('--x', clamp(pct, 0, 100) + '%'); }
    onFrame(function(){
      if (manual) return;
      var r = ba.getBoundingClientRect();
      var p = reduced ? .5 : range(innerHeight - r.top, r.height * .7, innerHeight * .55 + r.height * .5);
      setX(100 - ease(p) * 50);
    });
    function fromEvent(e){ var r = ba.getBoundingClientRect(); setX((e.clientX - r.left) / r.width * 100); }
    ba.addEventListener('pointerdown', function(e){ manual = dragging = true; ba.setPointerCapture(e.pointerId); fromEvent(e); });
    ba.addEventListener('pointermove', function(e){ if (dragging) fromEvent(e); });
    ba.addEventListener('pointerup', function(){ dragging = false; });
    ba.addEventListener('pointercancel', function(){ dragging = false; });
  });

  /* ---------- lightbox (grade de fotos do projeto) ---------- */
  var lb = $('#lb');
  if (lb){
    var shots = $$('.pgrid button'), cur = 0, lbImg = $('img', lb), lbCap = $('.nav p', lb), lbCount = $('header span', lb);
    function open(i){
      cur = (i + shots.length) % shots.length;
      var im = shots[cur].querySelector('img');
      lbImg.src = im.getAttribute('src'); lbImg.alt = im.alt;
      var cap = shots[cur].querySelector('.cap');
      lbCap.textContent = cap ? cap.textContent : im.alt; lbCount.textContent = (cur + 1) + ' / ' + shots.length;
      lb.classList.add('open'); document.body.style.overflow = 'hidden';
    }
    function close(){ lb.classList.remove('open'); document.body.style.overflow = ''; }
    shots.forEach(function(b, i){ b.addEventListener('click', function(){ open(i); }); });
    $('.close', lb).addEventListener('click', close);
    $('.prev', lb).addEventListener('click', function(){ open(cur - 1); });
    $('.next', lb).addEventListener('click', function(){ open(cur + 1); });
    lb.addEventListener('click', function(e){ if (e.target === lb || e.target.classList.contains('stage')) close(); });
    addEventListener('keydown', function(e){ if (!lb.classList.contains('open')) return; if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') open(cur - 1); if (e.key === 'ArrowRight') open(cur + 1); });
    var sx = null;
    lb.addEventListener('touchstart', function(e){ sx = e.touches[0].clientX; }, {passive:true});
    lb.addEventListener('touchend', function(e){ if (sx == null) return; var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) open(cur + (dx < 0 ? 1 : -1)); sx = null; });
  }

  /* ---------- formulário (simulado) ---------- */
  var form = $('#quoteForm');
  if (form){
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var req = $$('[required]', form);
      req.forEach(function(f){ f.style.borderColor = ''; });
      var bad = req.filter(function(f){ return !f.value.trim(); });
      if (bad.length){ bad.forEach(function(f){ f.style.borderColor = '#9E1B24'; }); bad[0].focus(); return; }
      var data = {}; new FormData(form).forEach(function(v, k){ data[k] = v; });
      track('form_submit', {service: data.service, town: data.town});
      if (form.getAttribute('action')){
        fetch(form.action, {method: 'POST', body: new FormData(form), headers: {Accept: 'application/json'}})
          .then(function(){ form.classList.add('sent'); }, function(){ form.submit(); });
      } else form.classList.add('sent');
    });
  }

  /* ---------- mapa estático (versão parada da gota da home) ---------- */
  var mapbox = $('#mapbox');
  if (mapbox && mapbox.classList.contains('static') && window.NLS_TOWNS){
    var T1 = NLS_TOWNS.t1, T2 = NLS_TOWNS.t2, focus = mapbox.getAttribute('data-focus');
    var LON0 = -72.12, LAT0 = 42.60, KX = Math.cos(42.2 * Math.PI / 180) * 69.17, KY = 69.17, S = 10.6, W = 820, H = 640;
    var P = function(lat, lon){ return [(lon - LON0) * KX * S, (LAT0 - lat) * KY * S]; };
    var poly = function(pts){ return pts.map(function(p){ var q = P(p[0], p[1]); return q[0].toFixed(1) + ',' + q[1].toFixed(1); }).join(' '); };
    var LAND = [[42.62,-72.2],[42.62,-70.95],[42.55,-70.92],[42.47,-70.95],[42.42,-70.99],[42.37,-71.03],[42.33,-71.04],[42.30,-70.97],[42.27,-70.93],[42.26,-70.84],[42.25,-70.77],[42.20,-70.72],[42.10,-70.66],[41.85,-70.60],[41.85,-71.10],[41.70,-71.17],[41.60,-71.22],[41.60,-72.2]];
    var BAY = [[41.60,-71.36],[41.66,-71.30],[41.73,-71.27],[41.79,-71.33],[41.82,-71.39],[41.76,-71.41],[41.68,-71.42],[41.60,-71.42]];
    var BORDERS = [[[42.02,-72.2],[42.02,-71.80],[42.02,-71.38],[41.90,-71.38],[41.78,-71.33],[41.70,-71.18]],[[42.02,-71.80],[41.60,-71.80]]];
    var base = P(T1[0][2], T1[0][3]);
    var towns = T1.map(function(t){ return {n:t[0], lat:t[2], lon:t[3], tier:1}; }).concat(T2.map(function(t){ return {n:t[0], lat:t[2], lon:t[3], tier:2}; }));
    towns.forEach(function(t){ var q = P(t.lat, t.lon); t.x = q[0]; t.y = q[1]; t.d = Math.hypot(t.x - base[0], t.y - base[1]); });
    var MAXD = Math.max.apply(null, towns.map(function(t){ return t.d; })) + 24;
    var NEAR = Math.max.apply(null, towns.filter(function(t){ return t.tier === 1; }).map(function(t){ return t.d; })) + 46;
    var LEFT = (window.NLS_MAP || {}).left || {}, DY = (window.NLS_MAP || {}).dy || {};
    var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><defs>' +
      '<clipPath id="land"><polygon points="' + poly(LAND) + '"/></clipPath>' +
      '<filter id="goo" x="-30%" y="-30%" width="160%" height="160%"><feTurbulence type="fractalNoise" baseFrequency=".012" numOctaves="3" seed="4"/><feDisplacementMap in="SourceGraphic" scale="46"/></filter>' +
      '<radialGradient id="wet"><stop offset="0" stop-color="#2A4C80"/><stop offset=".7" stop-color="#0A1E3D"/><stop offset="1" stop-color="#06142A"/></radialGradient>' +
      '<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#C6D1DE" stroke-width="1"/></pattern></defs>' +
      '<rect width="' + W + '" height="' + H + '" fill="url(#grid)" opacity=".7"/>' +
      '<polygon points="' + poly(LAND) + '" fill="#F5F2EC" stroke="#BBC5D3" stroke-width="2"/>' +
      '<g clip-path="url(#land)"><g filter="url(#goo)"><circle cx="' + base[0] + '" cy="' + base[1] + '" r="' + (8 + NEAR) + '" fill="url(#wet)" opacity=".9"/></g></g>' +
      '<polygon points="' + poly(BAY) + '" fill="#D9E2EC" stroke="#BBC5D3" stroke-width="1.5"/>';
    BORDERS.forEach(function(l){ svg += '<polyline points="' + poly(l) + '" fill="none" stroke="#9AA6B8" stroke-width="2" stroke-dasharray="6 6"/>'; });
    var lbl = function(text, lat, lon, cls){ var q = P(lat, lon); return '<text class="' + cls + '" x="' + q[0].toFixed(1) + '" y="' + q[1].toFixed(1) + '">' + text + '</text>'; };
    svg += lbl('MASSACHUSETTS', 42.55, -71.85, 'state') + lbl('RHODE ISLAND', 41.70, -71.60, 'state') + lbl('CONNECTICUT', 41.80, -71.98, 'state');
    svg += '<circle cx="' + base[0] + '" cy="' + base[1] + '" r="' + MAXD + '" fill="rgba(158,27,36,.06)" stroke="#9E1B24" stroke-width="2.5" stroke-dasharray="10 8"/>';
    var bos = P(42.36, -71.06), pvd = P(41.824, -71.413);
    svg += '<text class="landmark" x="' + (bos[0] - 8) + '" y="' + bos[1] + '" text-anchor="end">Boston</text><text class="landmark" x="' + pvd[0] + '" y="' + (pvd[1] + 4) + '" text-anchor="middle">Providence</text>';
    towns.forEach(function(t, k){
      var left = LEFT[t.n], dy = DY[t.n] || 0, isF = focus === t.n, cls = 'town on t' + t.tier + (k === 0 || isF ? ' base' : '');
      svg += '<g class="' + cls + '"><circle cx="' + t.x.toFixed(1) + '" cy="' + t.y.toFixed(1) + '" r="' + (k === 0 || isF ? 9 : t.tier === 1 ? 6.5 : 4.5) + '"/>' +
        '<text class="lbl" x="' + (t.x + (left ? -10 : 10)).toFixed(1) + '" y="' + (t.y + 5 + dy).toFixed(1) + '"' + (left ? ' text-anchor="end"' : '') + '>' + t.n + '</text></g>';
    });
    if (focus){ var f = towns.filter(function(t){ return t.n === focus; })[0]; if (f) svg += '<path d="M0 -46 C 12 -24 20 -12 20 2 A 20 20 0 1 1 -20 2 C -20 -12 -12 -24 0 -46 Z" fill="#9E1B24" stroke="#fff" stroke-width="3" transform="translate(' + f.x.toFixed(1) + ',' + (f.y - 30).toFixed(1) + ') scale(.7)"/>'; }
    svg += '</svg>';
    mapbox.innerHTML = svg;
  }
})();
