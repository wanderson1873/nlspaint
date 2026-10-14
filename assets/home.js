/* NLS Paint — efeitos exclusivos da home: galeria presa (#6) e gota que vira mapa (#7).
   As fotos da galeria e as listas de cidades já vêm no HTML (indexáveis); aqui só animamos. */
(function(){
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var clamp = function(v,a,b){ return Math.min(b==null?1:b, Math.max(a||0, v)); };
  var range = function(p,a,b){ return clamp((p-a)/(b-a)); };
  var ease = function(t){ return t<.5 ? 2*t*t : 1-Math.pow(-2*t+2,2)/2; };
  var easeOut = function(t){ return 1-Math.pow(1-t,3); };
  function onFrame(fn){ var q=false; function run(){ q=false; fn(); } function req(){ if(!q){ q=true; requestAnimationFrame(run); } } addEventListener('scroll',req,{passive:true}); addEventListener('resize',req); req(); }
  function inView(els, fn, th){
    if (!('IntersectionObserver' in window)) { els.forEach(fn); return; }
    var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting){ io.unobserve(e.target); fn(e.target); } }); }, {threshold: th || .4, rootMargin: '0px 0px -30% 0px'});
    els.forEach(function(el){ io.observe(el); });
  }
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

  /* ---------- galeria presa ---------- */
  var galPin = document.getElementById('galPin'), frame = document.getElementById('galFrame');
  if (galPin && frame){
    var layers = Array.prototype.slice.call(frame.querySelectorAll('img')), N = layers.length, ticks = document.getElementById('gTicks');
    galPin.style.setProperty('--n', N);
    var CLIPS = [null,
      function(t){ return 'inset(' + (100 - t * 100) + '% 0 0 0)'; },
      function(t){ return 'inset(0 0 0 ' + (100 - t * 100) + '%)'; },
      function(t){ return 'circle(' + (t * 75) + '% at 50% 50%)'; },
      function(t){ var a = t * 170; return 'polygon(0 0,' + a + '% 0,' + (a - 70) + '% 100%,0 100%)'; },
      function(t){ return 'inset(0 ' + (100 - t * 100) + '% 0 0)'; }
    ];
    var clip = function(i, t){ return CLIPS[1 + (i - 1) % (CLIPS.length - 1)](t); };
    layers.forEach(function(im, i){
      im.removeAttribute('loading');  // as camadas ficam empilhadas: carregar todas
      if (i) im.style.clipPath = clip(i, 0);
      ticks.insertAdjacentHTML('beforeend', '<i><b></b></i>');
    });
    var bars = ticks.querySelectorAll('b'), swaps = document.querySelectorAll('.gal .swap');
    var gNum = document.getElementById('gNum'), gTitle = document.getElementById('gTitle'), gMeta = document.getElementById('gMeta'), gDesc = document.getElementById('gDesc');
    var pad = function(n){ return (n < 10 ? '0' : '') + n; };
    var shown = -1, timer;
    function show(i){
      if (i === shown) return;
      var first = shown < 0; shown = i;
      function fill(){
        var d = layers[i].dataset;
        gNum.innerHTML = pad(i + 1) + '<small>/ ' + pad(N) + '</small>';
        gTitle.innerHTML = '<a href="' + d.u + '">' + esc(d.t) + '</a>';
        gMeta.innerHTML = '<span>' + esc(d.s) + '</span><span>' + esc(d.c) + '</span>';
        gDesc.textContent = d.d;
        swaps.forEach(function(s){ s.classList.remove('out'); });
      }
      if (first || reduced) { fill(); return; }
      swaps.forEach(function(s){ s.classList.add('out'); });
      clearTimeout(timer); timer = setTimeout(fill, 200);
    }
    frame.style.cursor = 'pointer';
    frame.addEventListener('click', function(){ location.href = layers[Math.max(shown, 0)].dataset.u; });
    onFrame(function(){
      var r = galPin.getBoundingClientRect(), span = r.height - (innerHeight - 64);
      var p = span > 0 ? clamp(-r.top / span) : 0;
      var s = range(p, .03, .95) * (N - 1), active = 0;
      for (var i = 1; i < N; i++){
        var t = reduced ? (s >= i - .5 ? 1 : 0) : ease(range(s - (i - 1), .15, .85));
        layers[i].style.clipPath = clip(i, t);
        if (t > .5) active = i;
      }
      bars.forEach(function(b, k){ b.style.transform = 'scaleX(' + (k <= active ? 1 : 0) + ')'; });
      show(active);
    });
  }

  /* ---------- gota que vira mapa ---------- */
  var mapbox = document.getElementById('mapbox');
  if (!mapbox || mapbox.classList.contains('static') || !window.NLS_TOWNS) return;
  var T1 = NLS_TOWNS.t1, T2 = NLS_TOWNS.t2;
  var LON0 = -72.12, LAT0 = 42.60, KX = Math.cos(42.2 * Math.PI / 180) * 69.17, KY = 69.17, S = 10.6, W = 820, H = 640;
  function P(lat, lon){ return [(lon - LON0) * KX * S, (LAT0 - lat) * KY * S]; }
  function poly(pts){ return pts.map(function(p){ var q = P(p[0], p[1]); return q[0].toFixed(1) + ',' + q[1].toFixed(1); }).join(' '); }
  var LAND = [[42.62,-72.2],[42.62,-70.95],[42.55,-70.92],[42.47,-70.95],[42.42,-70.99],[42.37,-71.03],[42.33,-71.04],[42.30,-70.97],[42.27,-70.93],[42.26,-70.84],[42.25,-70.77],[42.20,-70.72],[42.10,-70.66],[41.85,-70.60],[41.85,-71.10],[41.70,-71.17],[41.60,-71.22],[41.60,-72.2]];
  var BAY = [[41.60,-71.36],[41.66,-71.30],[41.73,-71.27],[41.79,-71.33],[41.82,-71.39],[41.76,-71.41],[41.68,-71.42],[41.60,-71.42]];
  var BORDERS = [[[42.02,-72.2],[42.02,-71.80],[42.02,-71.38],[41.90,-71.38],[41.78,-71.33],[41.70,-71.18]],[[42.02,-71.80],[41.60,-71.80]]];
  var base = P(T1[0][2], T1[0][3]);
  var towns = T1.map(function(t, i){ return {n:t[0], lat:t[2], lon:t[3], tier:1, i:i}; }).concat(T2.map(function(t, i){ return {n:t[0], lat:t[2], lon:t[3], tier:2, i:i}; }));
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
    '<g clip-path="url(#land)"><g filter="url(#goo)"><circle id="blob" cx="' + base[0] + '" cy="' + base[1] + '" r="0" fill="url(#wet)" opacity=".9"/></g></g>' +
    '<polygon points="' + poly(BAY) + '" fill="#D9E2EC" stroke="#BBC5D3" stroke-width="1.5"/>';
  BORDERS.forEach(function(l){ svg += '<polyline points="' + poly(l) + '" fill="none" stroke="#9AA6B8" stroke-width="2" stroke-dasharray="6 6"/>'; });
  function lbl(text, lat, lon, cls){ var q = P(lat, lon); return '<text class="' + cls + '" x="' + q[0].toFixed(1) + '" y="' + q[1].toFixed(1) + '">' + text + '</text>'; }
  svg += lbl('MASSACHUSETTS', 42.55, -71.85, 'state') + lbl('RHODE ISLAND', 41.70, -71.60, 'state') + lbl('CONNECTICUT', 41.80, -71.98, 'state');
  svg += '<circle id="reach" cx="' + base[0] + '" cy="' + base[1] + '" r="0" fill="rgba(158,27,36,.06)" stroke="#9E1B24" stroke-width="2.5" stroke-dasharray="10 8" opacity="0"/>';
  var bos = P(42.36, -71.06), pvd = P(41.824, -71.413);
  svg += '<text class="landmark" x="' + (bos[0] - 8) + '" y="' + bos[1] + '" text-anchor="end">Boston</text><text class="landmark" x="' + pvd[0] + '" y="' + (pvd[1] + 4) + '" text-anchor="middle">Providence</text>';
  svg += '<g id="towns">';
  towns.forEach(function(t, k){
    var left = LEFT[t.n], dy = DY[t.n] || 0, cls = 'town t' + t.tier + (k === 0 ? ' base' : '');
    svg += '<g class="' + cls + '"><circle cx="' + t.x.toFixed(1) + '" cy="' + t.y.toFixed(1) + '" r="' + (k === 0 ? 9 : t.tier === 1 ? 6.5 : 4.5) + '"/>' +
      '<text class="lbl" x="' + (t.x + (left ? -10 : 10)).toFixed(1) + '" y="' + (t.y + 5 + dy).toFixed(1) + '"' + (left ? ' text-anchor="end"' : '') + '>' + t.n + '</text></g>';
  });
  svg += '</g><g id="splash" opacity="0"><circle id="ring" cx="' + base[0] + '" cy="' + base[1] + '" r="0" fill="none" stroke="#0A1E3D" stroke-width="4"/>';
  for (var k = 0; k < 8; k++) svg += '<circle class="dot" cx="' + base[0] + '" cy="' + base[1] + '" r="' + (3 + (k % 3) * 2) + '" fill="#0A1E3D" data-a="' + (k / 8 * Math.PI * 2 + .3) + '"/>';
  svg += '</g><path id="drop" d="M0 -46 C 12 -24 20 -12 20 2 A 20 20 0 1 1 -20 2 C -20 -12 -12 -24 0 -46 Z" fill="#9E1B24" transform="translate(' + base[0] + ',-60)"/></svg>';
  mapbox.innerHTML = svg;

  var groups = mapbox.querySelectorAll('#towns .town');
  var chips1 = document.querySelectorAll('#t1 li'), chips2 = document.querySelectorAll('#t2 li');
  var reach = mapbox.querySelector('#reach'), blob = mapbox.querySelector('#blob'), drop = mapbox.querySelector('#drop'), splash = mapbox.querySelector('#splash'), ring = mapbox.querySelector('#ring'), dots = mapbox.querySelectorAll('.dot');

  function drawMap(p){
    var fall = range(p, 0, .16), y = -60 + (base[1] + 60) * fall * fall;
    drop.setAttribute('transform', 'translate(' + base[0] + ',' + y.toFixed(1) + ') scale(' + (1 - fall * .2).toFixed(3) + ',' + (1 + fall * .25).toFixed(3) + ')');
    drop.style.opacity = fall >= 1 ? 0 : 1;
    var sp = range(p, .16, .28);
    splash.setAttribute('opacity', sp > 0 && sp < 1 ? (1 - sp).toFixed(2) : 0);
    ring.setAttribute('r', (sp * 70).toFixed(1));
    dots.forEach(function(d, k){ var a = +d.getAttribute('data-a'), dist = easeOut(sp) * (40 + (k % 3) * 18); d.setAttribute('cx', (base[0] + Math.cos(a) * dist).toFixed(1)); d.setAttribute('cy', (base[1] + Math.sin(a) * dist).toFixed(1)); });
    var near = easeOut(range(p, .18, .55)) * NEAR, far = easeOut(range(p, .5, 1)) * MAXD, rad = Math.max(near, far);
    blob.setAttribute('r', (fall >= 1 ? 8 + near : 0).toFixed(1));
    reach.setAttribute('r', far.toFixed(1));
    reach.setAttribute('opacity', far > near ? 1 : 0);
    towns.forEach(function(t, k){
      var on = fall >= 1 && (k === 0 || t.d <= rad);
      groups[k].classList.toggle('on', on);
      var chip = (t.tier === 1 ? chips1 : chips2)[t.i];
      if (chip) chip.classList.toggle('on', on);
    });
  }
  drawMap(reduced ? 1 : 0);
  if (!reduced) inView([mapbox], function(){
    var t0 = null, DUR = 4200;
    function step(ts){ if (!t0) t0 = ts; var p = clamp((ts - t0) / DUR); drawMap(p); if (p < 1) requestAnimationFrame(step); }
    requestAnimationFrame(step);
  }, .3);
})();
