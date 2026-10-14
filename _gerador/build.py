# -*- coding: utf-8 -*-
"""Gera o site completo nlspaint.com (protótipo SEO local): home + serviços + projetos + cidades + institucionais,
sitemap.xml, robots.txt e um relatório de SEO on-page.

Uso:  python _gerador/build.py      (a partir de site-completo/)
"""
import datetime, glob, json, os, re, urllib.parse
from html import escape
from content import T1, T2, BANDS, SERVICES, SVC, PROJECTS, PROJ, CITY_PAGES, SERVICE_CITY, BUSINESS as B, STATE_NAME, wiki
from content_local import HOME

try:
    from PIL import Image
except ImportError:  # sem Pillow o site sai igual, só sem width/height nas imagens
    Image = None

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
# Produção: python _gerador/build.py   ·   Homologação: NLS_ENV=dev python _gerador/build.py
# Em dev o site sai com URLs de https://dev.nlspaint.com e bloqueado para buscadores (noindex), para não competir com o domínio real.
ENV = os.environ.get('NLS_ENV', 'prod')
STAGING = ENV != 'prod'
SITE = 'https://dev.nlspaint.com' if STAGING else 'https://nlspaint.com'
BIZ = SITE + '/#business'
PERSON = SITE + '/about/#maicow'
TEL = 'tel:' + B['phone_e164']
PHONE = B['phone']
NAP_CITY = '%s, %s %s' % (B['city'], B['state'], B['zip'])
TODAY = datetime.date.today().isoformat()

GA_ID = ''        # TODO: ID do GA4 (G-XXXXXXX). Vazio = eventos só no console.
FORM_ACTION = ''  # TODO: endpoint do Formspree/Web3Forms. Vazio = envio simulado.

PAGES = []        # registro para sitemap.xml e relatório

def sms(service=None):
    what = (service.lower() + ' ') if service else 'painting '
    body = "Hi Maicow, I'd like a free %sestimate. My town is: " % what
    return 'sms:%s?&body=%s' % (B['phone_e164'], urllib.parse.quote(body))

def strip(s): return re.sub('<[^>]+>', '', s).replace('&amp;', '&')
def ym(d):
    y, m = d.split('-'); return ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(m)-1] + ' ' + y
def city_label(p): return '%s, %s' % (p['city'], p['state'])
def city_url(name):
    if name == B['city']: return '/'
    c = CITY_PAGES.get(name)
    return '/service-areas/%s/' % c['slug'] if c else None
TOWN = {t[0]: t for t in T1 + T2}
def state_of(name): return TOWN[name][1] if name in TOWN else None
def place(name, st=None):
    """Cidade como entidade: nome + estado + sameAs da Wikipedia (desambigua Lincoln RI de Lincoln NE etc.)."""
    st = st or state_of(name)
    return {'@type':'City','name':'%s, %s' % (name, st),'sameAs':wiki(name, st),'containedInPlace':{'@type':'State','name':STATE_NAME[st]}}
def icon(i, cls=''): return '<svg%s><use href="#%s"/></svg>' % (' class="%s"' % cls if cls else '', i)
ARR = icon('i-arrow')
# posição dos rótulos no mapa SVG (left = texto à esquerda do ponto; dy = deslocamento vertical)
MAP_LABELS = {'left':{'North Smithfield':1,'Smithfield':1,'Blackstone':1,'Mendon':1,'Upton':1,'Sherborn':1,'Wayland':1,'Sudbury':1,'Concord':1,'Carlisle':1,'Hingham':1,'Bellingham':1},
              'dy':{'Blackstone':-8,'Woonsocket':-12,'Lincoln':8,'Smithfield':8,'Cumberland':4,'Norfolk':-4,'Wrentham':10,'Sherborn':6,'Dover':-4,'Wayland':-6,'Weston':-6,'Cohasset':14,'Franklin':-6,'Bellingham':12}}

# ---------------------------------------------------------------- imagens: width/height reais (evita CLS)
_DIMS = {}
def dims(src):
    if src not in _DIMS:
        _DIMS[src] = None
        f = os.path.join(ROOT, src.lstrip('/'))
        if Image and os.path.exists(f):
            with Image.open(f) as im: _DIMS[src] = im.size
    return _DIMS[src]

def img(src, alt, eager=False, pos=None, cls=None, extra=''):
    d = dims(src)
    a = ['src="%s"' % src, 'alt="%s"' % escape(alt)]
    if d: a.append('width="%d" height="%d"' % d)
    if cls: a.append('class="%s"' % cls)
    a.append('fetchpriority="high"' if eager else 'loading="lazy" decoding="async"')
    if pos: a.append('style="object-position:%s"' % pos)
    if extra: a.append(extra)
    return '<img %s>' % ' '.join(a)

def roll(src, alt, pos=None, eager=False):
    return '<div class="roll">%s</div>' % img(src, alt, eager, pos)

# ---------------------------------------------------------------- sprites
SPRITE = open(os.path.join(HERE, 'sprites.svg'), encoding='utf-8').read().strip()

# ---------------------------------------------------------------- schema: a empresa (um nó só, mesmo @id em todas as páginas)
def business_node():
    d = {
      '@type':'HousePainter','@id':BIZ,'name':B['name'],'url':SITE+'/',
      'description':'Local house painters in Woonsocket, RI: interior and exterior painting, ceilings and trim, epoxy floors, power washing and drywall repair for homes, rentals and businesses in Rhode Island and Massachusetts.',
      'telephone':B['phone_schema'],
      'logo':SITE+'/img/logo-nls.webp','image':[SITE+'/img/og-image.jpg', SITE+HOME['hero']],
      'priceRange':'$$','currenciesAccepted':'USD','paymentAccepted':B['payment'],
      'address':{'@type':'PostalAddress','addressLocality':B['city'],'addressRegion':B['state'],'postalCode':B['zip'],'addressCountry':'US'},
      'geo':{'@type':'GeoCoordinates','latitude':B['lat'],'longitude':B['lon']},
      'openingHoursSpecification':[{'@type':'OpeningHoursSpecification','dayOfWeek':B['days'],'opens':B['opens'],'closes':B['closes']}],
      'areaServed':[place(t[0], t[1]) for t in T1] + [
          {'@type':'GeoCircle','geoMidpoint':{'@type':'GeoCoordinates','latitude':B['lat'],'longitude':B['lon']},'geoRadius':str(int(B['radius_mi'] * 1609))}],
      'founder':{'@id':PERSON},
      'knowsAbout':[s['long'] for s in SERVICES] + ['Wallpaper Removal','Caulking','Rental Turnover Painting'],
      'hasOfferCatalog':{'@type':'OfferCatalog','name':'Painting services','itemListElement':[
          {'@type':'Offer','itemOffered':{'@type':'Service','@id':SITE+'/services/%s/#service' % s['slug'],'name':s['long'],'url':SITE+'/services/%s/' % s['slug']}} for s in SERVICES]},
    }
    if B['gbp']: d['hasMap'] = B['gbp']
    if B['same_as'] or B['gbp']: d['sameAs'] = ([B['gbp']] if B['gbp'] else []) + B['same_as']
    if B['legal']: d['legalName'] = B['legal']
    return d

def webpage(path, name, typ='WebPage', extra=None, desc=None, image=None):
    d = {'@type':typ,'@id':SITE+path+'#webpage','url':SITE+path,'name':name,'isPartOf':{'@id':SITE+'/#website'},'about':{'@id':BIZ},'inLanguage':'en-US','dateModified':TODAY}
    if desc: d['description'] = desc
    if image: d['primaryImageOfPage'] = {'@type':'ImageObject','url':SITE+image}
    if path != '/': d['breadcrumb'] = {'@id':SITE+path+'#breadcrumb'}
    if extra: d.update(extra)
    return d

def bc_schema(path, trail):
    return {'@type':'BreadcrumbList','@id':SITE+path+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':SITE+u} for i,(n,u) in enumerate(trail)]}

def faq_schema(path, faq):
    return {'@type':'FAQPage','@id':SITE+path+'#faq','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faq]}

# ---------------------------------------------------------------- <head>
def head(title, desc, path, graph, og=None, preload=None, noindex=False, geo=None, images=None, ptype='other'):
    og = og or '/img/og-image.jpg'
    geo = geo or (B['city'], B['state'], B['lat'], B['lon'])
    g = {'@context':'https://schema.org','@graph':[
        {'@type':'WebSite','@id':SITE+'/#website','url':SITE+'/','name':B['name'],'inLanguage':'en-US','publisher':{'@id':BIZ}},
        business_node()] + graph}
    if not noindex:
        PAGES.append({'path':path,'title':title,'desc':desc,'images':images or ([og] if og else []),'type':ptype})
    ogd = dims(og)
    ga = ''
    if GA_ID:
        ga = ('<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
              '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date());gtag("config","%s",{page_type:"%s"});</script>\n') % (GA_ID, GA_ID, ptype)
    return '''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="geo.region" content="US-{st}">
<meta name="geo.placename" content="{city}">
<meta name="geo.position" content="{lat};{lon}">
<meta name="ICBM" content="{lat}, {lon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="NLS Paint">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{ogimg}">{ogdims}
<meta property="og:image:alt" content="{title}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0A1E3D">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/img/favicon-48.png" sizes="48x48" type="image/png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,800;1,900&family=Barlow:wght@400;500;600;700&display=swap">
{preload}<link rel="stylesheet" href="/assets/site.css">
{ga}<script type="application/ld+json">
{ld}
</script>
</head>
'''.format(title=escape(title), desc=escape(desc), robots='noindex, nofollow' if STAGING else ('noindex, follow' if noindex else 'index, follow, max-image-preview:large'),
           url=SITE + path, st=geo[1], city=escape('%s, %s' % (geo[0], geo[1])), lat=geo[2], lon=geo[3],
           ogimg=SITE + og, ogdims=('\n<meta property="og:image:width" content="%d">\n<meta property="og:image:height" content="%d">' % ogd) if ogd else '',
           preload=('<link rel="preload" as="image" href="%s" fetchpriority="high">\n' % preload) if preload else '',
           ga=ga, ld=json.dumps(g, ensure_ascii=False, indent=1))

# ---------------------------------------------------------------- header / footer
def header(active, path, sms_href, page_type):
    svc_links = ''.join('<a href="/services/%s/"%s>%s<span><b>%s</b><small>%s</small></span></a>' % (
        s['slug'], ' aria-current="page"' if path.startswith('/services/%s/' % s['slug']) else '', img(s['menu_img'], ''), s['name'], s['short']) for s in SERVICES)
    svc_links += '<a href="/services/" class="dd-all"><span><b>All services</b><small>Compare all 6 + wallpaper removal</small></span></a>'
    def nav(href, label, key):
        return '<a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if active == key else '', label)
    d_svc = ''.join('<a href="/services/%s/">%s</a>' % (s['slug'], s['name']) for s in SERVICES)
    return '''<body data-page="%(pt)s">
<script>document.documentElement.classList.add('js')</script>
<a class="skip" href="#main">Skip to content</a>
%(sprite)s

<header class="hdr" data-note="Header igual em todas as páginas: logo · Services ▾ (6 + hub /services/) · Projects · Service Areas · About · Contact · Text us.">
  <div class="wrap">
    <a class="logo" href="/" aria-label="NLS Paint — house painters in Woonsocket, RI — home"><img src="/img/logo-nls.webp" alt="NLS Paint house painters logo" width="57" height="46"></a>
    <nav aria-label="Main">
      <div class="dd%(svccur)s"><button type="button" aria-expanded="false" aria-haspopup="true">Services<svg><use href="#i-chev"/></svg></button><div class="dd-menu">%(svc)s</div></div>
      %(n1)s
      %(n2)s
      %(n3)s
      %(n4)s
    </nav>
    <a class="btn btn-wine hdr-cta" href="%(sms)s" data-ev="click_text"><svg><use href="#i-sms"/></svg>Text us</a>
    <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="drawer"><span></span></button>
  </div>
</header>
<div class="drawer" id="drawer">
  <a class="d-lbl" href="/services/">Services</a>
  <div class="d-svc">%(dsvc)s</div>
  <a href="/projects/">Projects</a>
  <a href="/service-areas/">Service Areas</a>
  <a href="/about/">About</a>
  <a href="/contact/">Contact</a>
  <div class="d-nap"><span>%(nap)s</span><span>%(hours)s</span><a href="%(tel)s" data-ev="click_call">%(phone)s</a></div>
</div>
''' % {'pt':page_type, 'sprite':SPRITE, 'svc':svc_links, 'svccur':' cur' if active == 'services' else '', 'sms':sms_href, 'dsvc':d_svc, 'phone':PHONE,
       'nap':NAP_CITY, 'hours':B['hours'], 'tel':TEL,
       'n1':nav('/projects/','Projects','projects'), 'n2':nav('/service-areas/','Service Areas','areas'), 'n3':nav('/about/','About','about'), 'n4':nav('/contact/','Contact','contact')}

def crumbs(trail):
    items = []
    for i, (n, u) in enumerate(trail):
        if i == len(trail) - 1: items.append('<li><span aria-current="page">%s</span></li>' % escape(n))
        else: items.append('<li><a href="%s">%s</a></li>' % (u, escape(n)))
    return '<nav class="crumbs" aria-label="Breadcrumb" data-note="Breadcrumbs visíveis + schema BreadcrumbList (o Google mostra o caminho no resultado)."><ol class="wrap">%s</ol></nav>\n' % ''.join(items)

def footer(sms_href, extra_tail='', scripts=''):
    cities = ''
    for t in T1:
        u = city_url(t[0]); label = '%s, %s' % (t[0], t[1])
        cities += '<li><a href="%s">%s</a></li>' % (u, label) if u else '<li>%s</li>' % label
    svc = ''.join('<li><a href="/services/%s/">%s</a></li>' % (s['slug'], s['name'].replace(' & Caulking','')) for s in SERVICES)
    gbp = '<p><a href="%s" rel="noopener">See us on Google</a></p>' % B['gbp'] if B['gbp'] else ''
    return '''
<footer class="foot" data-note="Footer: NAP idêntico ao Google Meu Negócio (sem rua) + horário · 6 serviços · cidades da camada 1, todas com página.">
  <div class="wrap foot-grid">
    <div class="nap f-nap">
      <a class="logo" href="/"><img src="/img/logo-nls.webp" alt="NLS Paint" width="104" height="84" loading="lazy"></a>
      <b>%(name)s</b>
      <p>%(nap)s</p>
      <p><a href="%(tel)s" data-ev="click_call">%(phone)s</a></p>
      <p>%(hours)s</p>
      %(gbp)s
    </div>
    <div class="f-svc">
      <h2 class="f-h">Services</h2>
      <ul>%(svc)s</ul>
    </div>
    <div class="f-areas">
      <h2 class="f-h">Main Areas</h2>
      <ul class="cities">%(cities)s</ul>
      <p class="more-towns">…and many more towns nearby. <a href="/service-areas/">See all areas</a></p>
    </div>
    <div class="f-co">
      <h2 class="f-h">Company</h2>
      <ul><li><a href="/projects/">Projects</a></li><li><a href="/service-areas/">Service Areas</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy/">Privacy</a></li></ul>
    </div>
  </div>
  <div class="wrap bottom"><span>© %(year)s NLS Paint · House painters in Woonsocket, RI &amp; nearby towns</span><span>Interior painting · Exterior painting · Epoxy floors · Power washing</span></div>
</footer>

<div class="mbar">
  <a class="btn btn-wine" href="%(sms)s" data-ev="click_text"><svg><use href="#i-sms"/></svg>Text — free quote</a>
  <a class="btn btn-navy" href="%(tel)s" data-ev="click_call"><svg><use href="#i-call"/></svg>Call</a>
</div>
%(extra)s
<a class="to-top" href="#top" id="toTop" aria-label="Back to top"><svg><use href="#i-up"/></svg></a>
<button class="notes-btn" type="button" id="notesBtn" aria-pressed="false">📝 Notas do protótipo</button>
<script>window.NLS_TOWNS=%(towns)s;window.NLS_MAP=%(map)s</script>
<script src="/assets/site.js" defer></script>
%(scripts)s</body>
</html>
''' % {'name':B['name'], 'nap':NAP_CITY, 'hours':B['hours'], 'gbp':gbp, 'tel':TEL, 'phone':PHONE, 'svc':svc, 'cities':cities, 'sms':sms_href,
       'extra':extra_tail, 'towns':json.dumps({'t1':T1,'t2':T2}), 'map':json.dumps(MAP_LABELS), 'scripts':scripts, 'year':TODAY[:4]}

# ---------------------------------------------------------------- blocos reutilizáveis
def quote_section(service=None, town=None, title='Ready for a <span class="kw">fresh coat</span>?', lead=None, page='/'):
    sname = SVC[service]['name'] if service else None
    opts = ''.join('<option%s>%s</option>' % (' selected' if sname == s['name'] else '', s['name']) for s in SERVICES)
    opts += '<option>Wallpaper Removal</option><option>Other</option>'
    towns = ''.join('<option%s>%s, %s</option>' % (' selected' if town == t[0] else '', t[0], t[1]) for t in T1 + T2) + '<option>Other</option>'
    lead = lead or 'The fastest way: text us a few photos of your space. We reply the same day with your quote.'
    note = 'Formulário único: nome, telefone, cidade, serviço, mensagem. Serviço%s pré-preenchido; campo oculto “page” leva a URL de origem. Envio %s.' % (
        ' e cidade' if town else '', 'para ' + FORM_ACTION if FORM_ACTION else 'simulado (configurar FORM_ACTION no build.py)')
    action = ' action="%s" method="post"' % FORM_ACTION if FORM_ACTION else ''
    return '''
<section class="sec final" id="quote" data-note="%(note)s">
  <div class="wrap final-grid">
    <div>
      <span class="kicker" style="color:#F2A3A8">Free estimate</span>
      <h2 style="color:#fff">%(title)s</h2>
      <p class="lead" style="color:#AFC0D9">%(lead)s</p>
      <div class="ctas">
        <a class="btn btn-wine" href="%(sms)s" data-ev="click_text"><svg><use href="#i-sms"/></svg>Text us photos — free quote</a>
        <span class="or">or</span>
        <a class="btn btn-ghost" href="%(tel)s" data-ev="click_call"><svg><use href="#i-call"/></svg>Call %(phone)s</a>
      </div>
    </div>
    <form class="quote" id="quoteForm"%(action)s novalidate>
      <div class="fields" style="display:grid;gap:14px">
        <h3>Request a free quote</h3>
        <div class="row">
          <label>Name<input name="name" autocomplete="name" required></label>
          <label>Phone<input name="phone" type="tel" autocomplete="tel" required></label>
        </div>
        <div class="row">
          <label>Town<select name="town" required><option value="">Choose your town</option>%(towns)s</select></label>
          <label>Service<select name="service" required><option value="">Choose a service</option>%(opts)s</select></label>
        </div>
        <label>Message <span style="font-weight:500;color:var(--muted)">(optional)</span><textarea name="message" placeholder="Rooms, size, timeline…"></textarea></label>
        <input type="hidden" name="page" value="%(page)s">
        <button class="btn btn-wine" type="submit">Send request</button>
        <p class="hint">No need to upload photos — we'll text you to ask for them.</p>
      </div>
      <div class="ok">Thanks! We'll text you back today.%(proto)s</div>
    </form>
  </div>
</section>
''' % {'note':escape(note), 'title':title, 'lead':lead, 'sms':sms(sname), 'tel':TEL, 'phone':PHONE, 'towns':towns, 'opts':opts,
       'page':SITE + page, 'action':action, 'proto':'' if FORM_ACTION else ' (Prototype: nothing was sent.)'}

def pcard(p, label=None):
    s = SVC[p['service']]
    return '''<a class="pcard" href="/projects/%(slug)s/">
  %(roll)s
  <div class="pc-body">
    <div class="pc-meta"><span class="pill svc-p">%(sname)s</span><span class="pill"><svg><use href="#i-pin"/></svg>%(cl)s</span>%(lab)s</div>
    <h3>%(card)s</h3>
    <p>%(sum)s</p>
    <span class="go">See the project %(arr)s</span>
  </div>
</a>''' % {'slug':p['slug'], 'roll':roll(p['photos'][0][0], '%s in %s' % (s['long'], city_label(p))),
           'sname':s['name'], 'cl':city_label(p), 'card':p['card'], 'sum':escape(p['summary'].split('. ')[0].rstrip('.') + '.'), 'arr':ARR,
           'lab':'<span class="pill">%s</span>' % label if label else ''}

def faq_block(faq, kicker='FAQ', title='Good <span class="kw">questions</span>', lead='Still wondering about something? Text us — a real person answers.', note='FAQ (schema FAQPage com o MESMO texto visível). Respostas são sugestões: confirmar com o Maicow.'):
    items = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (escape(q), escape(a)) for q, a in faq)
    return '''
<section class="sec faq" id="faq" data-note="%s">
  <div class="wrap faq-grid">
    <div>
      <span class="kicker">%s</span>
      <h2>%s</h2>
      <p class="lead">%s</p>
    </div>
    <div>%s</div>
  </div>
</section>
''' % (escape(note), kicker, title, lead, items)

def steps_block(steps, title, note, cls='steps svc-steps'):
    icons = ['i-camera', 'i-doc', 'i-roller']
    lis = ''.join('<li><svg class="ic"><use href="#%s"/></svg><h3>%s</h3><p>%s</p></li>' % (icons[i], escape(h), escape(t)) for i, (h, t) in enumerate(steps))
    return '''
<section class="sec" id="how" data-note="%s">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">How it works</span><h2>%s</h2></div>
    <ol class="%s">%s</ol>
  </div>
</section>
''' % (escape(note), title, cls, lis)

def rel_block(slugs, title='You might also <span class="kw">need</span>', kicker='Related services'):
    cards = ''.join('<a href="/services/%s/">%s<span><b>%s</b><small>%s</small></span><span class="arr">%s</span></a>' % (
        s, img(SVC[s]['menu_img'], SVC[s]['long']), SVC[s]['name'], SVC[s]['short'], ARR) for s in slugs)
    return '''
<section class="sec alt tight" data-note="Serviços relacionados (2–3): reforçam a malha de links internos.">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">%s</span><h2>%s</h2></div>
    <div class="rel">%s</div>
  </div>
</section>
''' % (kicker, title, cards)

def towns_list(names):
    lis = ''
    for n in names:
        u = city_url(n); st = state_of(n) or 'RI'
        lis += '<li><a href="%s">%s%s, %s</a></li>' % (u, icon('i-pin'), n, st) if u else '<li><span>%s%s, %s</span></li>' % (icon('i-pin'), n, st)
    return '<ul class="towns">%s</ul>' % lis

def cta_band(sms_href, title='Got photos? <span class="kw" data-color="#0A1E3D">Text them.</span>', text='Send a few pictures and your town — we reply the same day with a price.'):
    return '''
<section class="cta-band" data-note="Faixa de CTA no meio da página (Text é o CTA principal).">
  <div class="wrap">
    <div><h2>%s</h2><p>%s</p></div>
    <a class="btn btn-white" href="%s" data-ev="click_text"><svg><use href="#i-sms"/></svg>Text us photos — free quote</a>
  </div>
</section>
''' % (title, text, sms_href)

def collage(srcs, alt):
    imgs = ''.join(img(src, '', i == 0) for i, src in enumerate(srcs[:3]))
    return '<div class="collage" aria-hidden="true">%s</div>' % imgs

def local_block(city, paras, facts, kicker, title, note):
    fl = ''.join('<li><small>%s</small><b>%s</b></li>' % (escape(a), escape(b)) for a, b in facts)
    return '''
<section class="sec" id="local" data-note="%s">
  <div class="wrap intro-grid">
    <div><span class="kicker">%s</span><h2>%s</h2></div>
    <div class="local">%s<ul class="localfacts">%s</ul></div>
  </div>
</section>
''' % (escape(note), kicker, title, ''.join('<p>%s</p>' % t for t in paras), fl)

def write(path, html):
    out = os.path.join(ROOT, path.strip('/').replace('/', os.sep), 'index.html') if path.endswith('/') else os.path.join(ROOT, path.strip('/'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline='\n') as f: f.write(html)
    print('  ', path)

def projects_for(service, city=None):
    main = [p for p in PROJECTS if p['service'] == service and (not city or p['city'] == city)]
    also = [p for p in PROJECTS if service in p.get('also', []) and (not city or p['city'] == city)]
    srt = lambda L: sorted(L, key=lambda p: p['date'], reverse=True)
    return srt(main), srt(also)

def page_open(active, path, sms_href, ptype, trail=None):
    h = header(active, path, sms_href, ptype) + '<main id="main">\n<span id="top"></span>\n'
    return h + (crumbs(trail) if trail else '')

# ================================================================= HOME (= página de Woonsocket)
def home():
    path = '/'; sms_href = sms(None)
    gal = [(PROJ[slug], src) for slug, src in HOME['gallery']]
    graph = [webpage(path, HOME['title'], desc=HOME['desc'], image=HOME['hero'],
                     extra={'spatialCoverage':place(B['city'], B['state'])}),
             faq_schema(path, HOME['faq'])]
    h = head(HOME['title'], HOME['desc'], path, graph, og=HOME['hero'], preload=HOME['hero'], ptype='home',
             images=[HOME['hero']] + [src for _, src in gal])
    h += page_open('', path, sms_href, 'home')
    h += '''
<section class="hero" data-note="Hero — 1 foto forte, sem animação (LCP). H1 sem cidade (pedido anterior); a cidade está no title, na meta description, no schema, no bloco “House painting in Woonsocket” e no footer.">
  %(img)s
  <div class="wrap">
    <span class="kicker">Replying today · Free estimates</span>
    <h1>Local House Painters <em>Near You</em></h1>
    <p>Interior &amp; exterior house painting for homes, rentals and businesses in your neighborhood. Careful prep, clean lines and a finish that lasts. Text a few photos and get your painting quote the same day.</p>
    <div class="ctas">
      <a class="btn btn-wine" href="%(sms)s" data-ev="click_text"><svg><use href="#i-sms"/></svg>Text us photos — free quote</a>
      <a class="btn btn-ghost" href="%(tel)s" data-ev="click_call"><svg><use href="#i-call"/></svg>Call %(phone)s</a>
    </div>
    <div class="meta">
      <span><svg><use href="#i-clock"/></svg>%(hours)s</span>
      <span><svg><use href="#i-pin"/></svg>Local &amp; owner-operated · %(nap)s</span>
    </div>
  </div>
</section>

<section class="trust" aria-label="Why homeowners choose NLS Paint" data-note="Faixa de confiança — 4 selos. Sem “Licensed &amp; Insured” até ter LLC e seguro.">
  <ul class="wrap">
    <li><i><svg><use href="#i-bolt"/></svg></i>Same-day reply</li>
    <li><i><svg><use href="#i-tag"/></svg></i>Free estimates</li>
    <li><i><svg><use href="#i-home"/></svg></i>Homes &amp; businesses</li>
    <li><i><svg><use href="#i-star"/></svg></i>5+ years experience</li>
  </ul>
</section>
''' % {'img':img(HOME['hero'], 'Freshly painted white colonial house exterior by local house painters in Woonsocket, RI', True), 'sms':sms_href, 'tel':TEL, 'phone':PHONE, 'hours':B['hours'], 'nap':NAP_CITY}

    # serviços
    cards = []
    for i, s in enumerate(SERVICES):
        cls = 'svc feat' if i == 0 else ('svc wide' if i == len(SERVICES) - 1 else 'svc')
        tag = '<span class="tag">Most requested</span>' if i == 0 else ''
        small = 'Siding, trim, doors &amp; shutters — power washed and scraped first' if i == 0 else s['short'].replace('&', '&amp;')
        im = s['menu_img'] if s['slug'] != 'interior-painting' else '/img/stock/interior-living-room-painting-lincoln-ri.webp'
        cards.append('''      <a class="%s" href="/services/%s/">
        %s
        %s<span class="arrow"><svg><use href="#i-arrow"/></svg></span>
        <div class="cap"><h3>%s</h3><small>%s</small></div>
      </a>''' % (cls, s['slug'], roll(im, '%s in Woonsocket, RI' % s['long'], '50% 35%' if i == 0 else None), tag, s['long'] if i == 0 else s['name'].replace('&', '&amp;'), small))
    h += '''
<section class="sec" id="services" data-note="Serviços — 6 cards com link para /services/… (Exterior em destaque). Pincelada no título.">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">Painting services</span>
      <h2>What we <span class="kw">paint</span></h2>
      <p class="lead">Interior and exterior house painting, plus the prep and repair work that makes the finish last — in Woonsocket, Cumberland, Lincoln and nearby towns. <a href="/services/" style="color:var(--wine);font-weight:700">Compare all services</a></p>
    </div>
    <div class="svc-grid">
%s
      <a class="svc-extra" href="/services/interior-painting/#wallpaper-removal"><i><svg><use href="#i-roller"/></svg></i><div><small class="kicker" style="margin:0 0 4px;font-size:.75rem">Also</small><b>Wallpaper Removal</b><span>Old paper stripped, walls repaired and ready for fresh paint.</span><em>Ask about it <svg><use href="#i-arrow"/></svg></em></div></a>
    </div>
  </div>
</section>
''' % '\n'.join(cards)

    # antes e depois
    ba_src = '/img/stock/living-room-before-after-cumberland-ri.webp'
    h += '''
<section class="sec ba-sec" data-note="Antes e depois — revela com o scroll, depois arrasta. O “antes” é a mesma foto com filtro: trocar por um par real do mesmo ângulo.">
  <div class="wrap ba-grid">
    <div>
      <span class="kicker">Before &amp; after</span>
      <h2>Same room. <span class="kw">New life.</span></h2>
      <p class="lead">Tired, yellowed walls turned into a bright, clean living room in two days — furniture moved, floors covered, trim caulked. <a href="/projects/wallpaper-removal-interior-repaint-cumberland-ri/" style="color:var(--wine);font-weight:700">See the project</a></p>
      <ul class="facts">
        <li><b>Service</b><a href="/services/interior-painting/">Interior painting</a></li>
        <li><b>Town</b><a href="/service-areas/cumberland-ri/">Cumberland, RI</a></li>
        <li><b>Time</b>2 days</li>
      </ul>
    </div>
    <div>
      <div class="ba" style="--x:100%%">
        %s
        %s
        <span class="lbl b">Before</span><span class="lbl a">After</span>
        <div class="bar"><span class="knob"><svg><use href="#i-drag"/></svg></span></div>
      </div>
      <p class="ba-note"><svg><use href="#i-drag"/></svg>Drag to compare</p>
    </div>
  </div>
</section>
''' % (img(ba_src, 'Living room before interior painting in Cumberland, RI', cls='before'), img(ba_src, 'Living room after interior painting in Cumberland, RI', cls='after'))

    # galeria presa (imagens no HTML = rastreáveis; o JS só anima)
    layers = ''
    for i, (p, src) in enumerate(gal):
        s = SVC[p['service']]
        layers += img(src, '%s — %s in %s' % (s['long'], p['card'], city_label(p)), extra='data-t="%s" data-s="%s" data-c="%s" data-d="%s" data-u="/projects/%s/"' % (
            escape(p['card']), escape(s['name'].split(' &')[0]), city_label(p), escape(p['summary'].split('. ')[0].rstrip('.') + '.'), p['slug']))
    first = gal[0][0]
    h += '''
<section class="gal-sec" id="projects" data-note="Galeria presa — fotos trocam por recorte. As 6 imagens já estão no HTML (indexáveis, com alt serviço + cidade); cada uma leva ao projeto.">
  <div class="wrap gal-intro">
    <span class="kicker">Recent projects</span>
    <h2>Our <span class="kw">work</span> around Woonsocket</h2>
    <p class="lead">Homes, rentals and commercial buildings across Rhode Island and Massachusetts.</p>
  </div>
  <div class="gal-pin" id="galPin">
    <div class="gal-sticky">
      <div class="gal">
        <div class="frame" id="galFrame">%s</div>
        <div class="info">
          <div class="num swap" id="gNum">01<small>/ %02d</small></div>
          <h3 class="swap" id="gTitle"><a href="/projects/%s/">%s</a></h3>
          <div class="meta swap" id="gMeta"><span>%s</span><span>%s</span></div>
          <p class="desc swap" id="gDesc"></p>
          <div class="ticks" id="gTicks"></div>
        </div>
      </div>
    </div>
  </div>
  <div class="gal-more"><a class="btn" href="/projects/">See all %d projects <svg><use href="#i-arrow"/></svg></a></div>
</section>
''' % (layers, len(gal), first['slug'], escape(first['card']), SVC[first['service']]['name'].split(' &')[0], city_label(first), len(PROJECTS))

    h += steps_block([('Text us photos','Snap a few pictures of the rooms or the outside of the house and send them to %s.' % PHONE),
                      ('Same-day quote','We reply the same day with a clear price. Bigger jobs get a free visit.'),
                      ('We paint','We protect your floors and furniture, paint, clean up every day and walk you through the finish.')],
                     'A quote in <span class="kw">3 steps</span>', 'Como funciona — 3 passos.', cls='steps')

    h += '''
<section class="sec who" data-note="Quem vai pintar — foto do Maicow (PENDENTE) + 1 frase. Link para /about/.">
  <div class="wrap who-grid">
    <div class="photo">
      %s
      <span class="pending">Placeholder · Maicow's photo here</span>
      <span class="badge">Owner on<b>every job</b></span>
    </div>
    <div>
      <span class="kicker" style="color:#F2A3A8">Who's painting your home</span>
      <h2>Hi, I'm <span class="kw">Maicow</span></h2>
      <p class="quote">“You call me, you get me. I quote it, I paint it, and I don't leave until you love it.”</p>
      <p class="sig">— Maicow, owner of NLS Paint · <a href="/about/" style="color:#F2A3A8">Read my story</a></p>
      <ul>
        <li><svg><use href="#i-check"/></svg>Furniture and floors always protected</li>
        <li><svg><use href="#i-check"/></svg>Clean-up at the end of every day</li>
        <li><svg><use href="#i-check"/></svg>Reply the same day, every time</li>
      </ul>
    </div>
  </div>
</section>

<section class="sec" data-note="Para quem pintamos — 4 públicos.">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">Who we paint for</span>
      <h2>Painting for <span class="kw">homes &amp; business</span></h2>
    </div>
    <div class="aud">
      <div><svg><use href="#i-home"/></svg><b>Homeowners</b><span>Single rooms to full exterior repaints.</span></div>
      <div><svg><use href="#i-key"/></svg><b>Landlords</b><span>Fast rental turnovers between tenants.</span></div>
      <div><svg><use href="#i-sign"/></svg><b>Realtors</b><span>Pre-listing touch-ups that help homes sell.</span></div>
      <div><svg><use href="#i-hammer"/></svg><b>Contractors</b><span>Reliable paint sub for your projects.</span></div>
    </div>
  </div>
</section>
''' % roll('/img/stock/paint-roller-maicow-placeholder.webp', 'Maicow, owner and house painter at NLS Paint in Woonsocket, RI')

    # bloco local de Woonsocket (novo: a home é a página da cidade-base)
    h += local_block(B['city'], HOME['local'], HOME['local_facts'], 'Our home town', 'House painting in <span class="kw">Woonsocket, RI</span>',
                     'NOVO · SEO local: a home é a página de Woonsocket (cidade do Google Meu Negócio). Parágrafo local com bairros e tipos de casa. RASCUNHO: confirmar com o Maicow.')

    # área de atendimento (cidades no HTML, com link quando há página)
    def chip(t):
        u = city_url(t[0])
        return '<li>%s%s, %s%s</li>' % ('<a href="%s">' % u if u else '', t[0], t[1], '</a>' if u else '')
    h += '''
<section class="sec area" id="areas" data-note="Área de atendimento — gota cai em Woonsocket e “pinta” as cidades. Cidades escritas no HTML (antes eram injetadas por JS e o Google podia não ver) e com link para as páginas de cidade.">
  <div class="wrap area-grid">
    <div>
      <span class="kicker">Service areas</span>
      <h2>Painters near <span class="kw">you</span></h2>
      <p class="lead">Based in %s and painting homes in the towns around it. <a href="/service-areas/" style="color:var(--wine);font-weight:700">See every town</a></p>
    </div>
    <div class="mapbox" id="mapbox" role="img" aria-label="Map of NLS Paint service area around Woonsocket, Rhode Island"></div>
    <div class="area-list">
      <div class="tier">
        <h3><i></i>Your neighbors</h3>
        <ul class="chips t1chips" id="t1">%s</ul>
      </div>
      <div class="tier">
        <h3><i style="background:var(--navy)"></i>We also serve</h3>
        <ul class="chips" id="t2">%s</ul>
      </div>
      <p class="ask">Don't see your town? <a href="%s" data-ev="click_text">Text us</a> — we likely cover it.</p>
    </div>
  </div>
</section>

<section class="sec reviews" data-note="Avaliações — RESERVADO E OCULTO até existirem avaliações reais no Google. Sem schema Review/AggregateRating antes disso.">
  <div class="wrap"><div class="ph">Google reviews will appear here once real reviews exist.</div></div>
</section>
''' % (NAP_CITY, ''.join(chip(t) for t in T1), ''.join(chip(t) for t in T2), sms_href)

    h += faq_block(HOME['faq'])
    h += quote_section(None, page=path)
    h += '</main>\n' + footer(sms_href, scripts='<script src="/assets/home.js" defer></script>\n')
    write(path, h)

# ================================================================= HUB DE SERVIÇOS (novo)
def services_hub():
    path = '/services/'; sms_href = sms(None)
    trail = [('Home','/'),('Services', path)]
    title = 'Painting Services in Woonsocket, RI | NLS Paint'
    desc = 'Exterior & interior painting, ceilings & trim, epoxy floors, power washing and drywall repair in Woonsocket, RI & nearby towns. Free quotes by text.'
    graph = [webpage(path, 'Painting Services in Woonsocket, RI', 'CollectionPage', desc=desc), bc_schema(path, trail),
             {'@type':'ItemList','@id':SITE+path+'#list','itemListElement':[{'@type':'ListItem','position':i+1,'url':SITE+'/services/%s/' % s['slug'],'name':s['long']} for i, s in enumerate(SERVICES)]}]
    h = head(title, desc, path, graph, og=SERVICES[0]['hero'], ptype='services_hub', images=[s['hero'] for s in SERVICES])
    h += page_open('services', path, sms_href, 'services_hub', trail)
    h += '''<section class="hero plain" data-note="NOVO · Hub /services/ — o breadcrumb “Services” agora aponta para uma página real (antes era /#services). Mira buscas genéricas tipo “painting services Woonsocket RI”.">
  <div class="wrap">
    <span class="kicker">6 services · one local painter</span>
    <h1>Painting Services in <em>Woonsocket, RI</em></h1>
    <p>Everything a house needs to look freshly painted — inside and out — plus the prep and repairs that make the finish last. Same price in every town we serve in RI &amp; MA.</p>
    <div class="ctas"><a class="btn btn-wine" href="%s" data-ev="click_text"><svg><use href="#i-sms"/></svg>Text us photos — free quote</a><a class="btn btn-ghost" href="%s" data-ev="click_call"><svg><use href="#i-call"/></svg>Call %s</a></div>
  </div>
  %s
</section>
''' % (sms_href, TEL, PHONE, collage([SERVICES[0]['hero'], SERVICES[1]['hero'], SERVICES[3]['hero']], 'Painting services'))
    rows = ''
    for i, s in enumerate(SERVICES):
        n = len(projects_for(s['slug'])[0])
        rows += '''
<section class="sec%s" data-note="Resumo do serviço + link para a página completa (texto curto e diferente da página do serviço para não duplicar conteúdo).">
  <div class="wrap split%s">
    <div class="ph">%s</div>
    <div>
      <span class="kicker">%s</span>
      <h2><a href="/services/%s/" style="text-decoration:none;color:inherit">%s</a></h2>
      <p class="lead">%s</p>
      <ul class="ticklist">%s</ul>
      <p style="margin:22px 0 0"><a class="link-more" href="/services/%s/">%s in Woonsocket &amp; nearby %s</a></p>
    </div>
  </div>
</section>
''' % (' alt' if i % 2 else '', ' rev' if i % 2 else '', roll(s['hero'], '%s in Woonsocket, RI' % s['long'], s['hero_pos']), '%d project%s' % (n, '' if n == 1 else 's') if n else s['short'],
       s['slug'], s['long'].replace('&', '&amp;'), s['lead'], ''.join('<li>%s %s</li>' % (icon('i-check'), escape(a)) for a, _ in s['included'][:4]), s['slug'], s['long'].replace('&', '&amp;'), ARR)
    h += rows
    h += cta_band(sms_href)
    h += quote_section(None, title='Not sure which <span class="kw">service</span>?', lead='Text us photos and tell us what bothers you — peeling paint, stains, an ugly floor. We\'ll tell you what it needs and what it costs, the same day.', page=path)
    h += '</main>\n' + footer(sms_href)
    write(path, h)

# ================================================================= SERVIÇO
def service_page(s, city=None, local=None, hero=None):
    slug = s['slug']
    if hero: s = dict(s, hero=hero, hero_pos='50% 50%')
    if city:
        cp = CITY_PAGES[city]; st = cp['state']
        path = '/service-areas/%s/%s/' % (cp['slug'], slug); ptype = 'service_city'
        h1 = '%s in <em>%s, %s</em>' % (s['long'].replace('&', '&amp;'), city, st)
        title = '%s in %s, %s | NLS Paint' % (s['long'], city, st)
        desc = '%s in %s, %s by a local painter %s away in Woonsocket. Prep done right, two coats, same-day quotes by text.' % (s['long'], city, st, cp['facts'][0][1].lstrip('~'))
        trail = [('Home','/'),('Service Areas','/service-areas/'),('%s, %s' % (city, st), '/service-areas/%s/' % cp['slug']),(s['name'], path)]
        area = [place(city, st)]
        t = TOWN[city]; geo = (city, st, t[2], t[3])
    else:
        path = '/services/%s/' % slug; ptype = 'service'
        h1, title, desc = s['h1'], s['title'], s['desc']
        trail = [('Home','/'),('Services','/services/'),(s['name'], path)]
        area = [place(t[0], t[1]) for t in T1]
        geo = None
    sms_href = sms(s['name'])
    main, also = projects_for(slug, city)
    faq = s['faq'] if not city else CITY_PAGES[city]['faq'] + s['faq'][:2]
    graph = [webpage(path, strip(h1), desc=desc, image=s['hero']), bc_schema(path, trail),
             {'@type':'Service','@id':SITE+path+'#service','name':strip(h1),'serviceType':s['long'],'description':s['lead'],'provider':{'@id':BIZ},'url':SITE+path,
              'areaServed':area,'image':SITE+s['hero'],
              'hasOfferCatalog':{'@type':'OfferCatalog','name':'What\'s included','itemListElement':[{'@type':'Offer','itemOffered':{'@type':'Service','name':a,'description':b}} for a, b in s['included']]}},
             faq_schema(path, faq)]
    h = head(title, desc, path, graph, og=s['hero'], preload=s['hero'], geo=geo, ptype=ptype, images=[s['hero']] + [p['photos'][0][0] for p in main[:6]])
    h += page_open('services', path, sms_href, ptype, trail)

    gate = '<span class="gate">Página por gatilho · Serviço × cidade</span><br>' if city else ''
    alt_where = '%s, %s' % (city, CITY_PAGES[city]['state']) if city else 'Woonsocket, RI'
    h += '''<section class="hero sub" data-note="%s">
  %s
  <div class="wrap">
    %s<span class="kicker">Free estimates · Same-day reply</span>
    <h1>%s</h1>
    <p>%s</p>
    <div class="ctas">
      <a class="btn btn-wine" href="%s" data-ev="click_text"><svg><use href="#i-sms"/></svg>Text us photos — free quote</a>
      <a class="btn btn-ghost" href="%s" data-ev="click_call"><svg><use href="#i-call"/></svg>Call %s</a>
    </div>
    <div class="meta"><span><svg><use href="#i-clock"/></svg>%s</span><span><svg><use href="#i-pin"/></svg>%s</span></div>
  </div>
</section>
''' % (escape('Hero — foto real do serviço + H1 com a cidade + 2 CTAs. Sem animação (LCP).' + (' H1/title/schema/geo focados em %s.' % city if city else '')),
       img(s['hero'], '%s in %s' % (s['long'], alt_where), True, s['hero_pos']), gate, h1, s['lead'], sms_href, TEL, PHONE, B['hours'],
       ('%s from Woonsocket' % CITY_PAGES[city]['facts'][0][1] if city else 'Woonsocket, RI &amp; nearby towns'))

    intro = ''.join('<p%s>%s</p>' % (' class="big"' if i == 0 else '', t) for i, t in enumerate(s['intro']))
    if city:
        intro = '<p class="big"><strong>Local, not a franchise.</strong> %s</p>' % local[0] + ''.join('<p>%s</p>' % t for t in local[1:]) + '<p>%s</p>' % s['intro'][1]
    h += '''
<section class="sec" data-note="O que está incluso — o conteúdo único de cada serviço (500–900 palavras no total).">
  <div class="wrap">
    <div class="intro-grid">
      <div><span class="kicker">%s</span><h2>What's <span class="kw">included</span></h2></div>
      <div class="prose">%s</div>
    </div>
    <ul class="incl" style="margin-top:34px">%s</ul>
  </div>
</section>
''' % (escape(s['long']) + (' · %s' % city if city else ''), intro,
       ''.join('<li>%s<b>%s</b><span>%s</span></li>' % (icon('i-check'), escape(a), escape(b)) for a, b in s['included']))

    if s.get('wallpaper') and not city:
        h += '''
<section class="sec extra-sec" id="wallpaper-removal" data-note="Seção Wallpaper Removal (dentro de Interior Painting). Remoção sim, instalação não.">
  <div class="wrap split rev">
    <div class="ph">%s</div>
    <div>
      <span class="kicker">Also inside</span>
      <h2>Wallpaper <span class="kw">removal</span></h2>
      <p class="lead">Old wallpaper stripped, walls repaired and ready for fresh paint — without gouges or glue showing through.</p>
      <ul class="ticklist">
        <li>%s Scored and steamed off, layer by layer</li>
        <li>%s All glue residue washed off the wall</li>
        <li>%s Torn spots skim-coated and sanded smooth</li>
        <li>%s Sealed with a primer made for papered walls</li>
        <li>%s Painted in two coats — or left primed and ready</li>
      </ul>
      <p style="margin:18px 0 0;color:var(--muted)">We remove wallpaper; we don't install it.</p>
    </div>
  </div>
</section>
''' % ((roll('/img/stock/bedroom-wallpaper-removal-cumberland-ri.webp', 'Bedroom walls after wallpaper removal and repainting in Cumberland, RI'),) + (icon('i-check'),) * 5)

    cards = [pcard(p) for p in main[:6]] + [pcard(p, 'Part of this job') for p in also[:max(0, 3 - len(main))]]
    where = '%s, %s' % (city, CITY_PAGES[city]['state']) if city else 'around Woonsocket'
    h += '''
<section class="sec alt" id="projects" data-note="Projetos — cards automáticos filtrados pelo serviço%s, com a cidade em cada card (sinal local + prova real).">
  <div class="wrap">
    <div class="sec-head row">
      <div><span class="kicker">Recent projects</span><h2>%s <span class="kw">%s</span></h2></div>
      <a class="link-more" href="/projects/">All projects %s</a>
    </div>
    <div class="pcards three">%s</div>
  </div>
</section>
''' % (' e pela cidade' if city else '', escape(s['name']) if not city else 'Exteriors in', where if city else 'jobs', ARR, ''.join(cards))

    h += steps_block(s['steps'], 'Your quote in <span class="kw">3 steps</span>', 'Processo — os 3 passos da home com o texto ajustado ao serviço.')
    h += cta_band(sms_href)
    h += faq_block(faq, kicker='%s FAQ' % s['name'], title='Common <span class="kw">questions</span>')
    if not city:
        done = []
        for p in main + also:
            if p['city'] not in done: done.append(p['city'])
        others = [t[0] for t in T1 if t[0] not in done]
        local_links = ''.join('<li><a href="/service-areas/%s/%s/">%s%s in %s</a></li>' % (CITY_PAGES[x['city']]['slug'], slug, icon('i-pin'), s['name'], x['city'])
                              for x in SERVICE_CITY if x['service'] == slug)
        h += '''
<section class="sec tight" data-note="“Towns where we've done this” — gerado a partir dos projetos, com link para as páginas de cidade (e serviço × cidade quando existe).">
  <div class="wrap two-col">
    <div><span class="kicker">Service areas</span><h2>Towns where we've done <span class="kw">this</span></h2><p class="lead">Based in %s and painting in the towns around it.</p></div>
    <div>%s%s<p class="towns-note">Also near you: %s. <a href="/service-areas/" style="color:var(--wine);font-weight:700">See all areas</a></p></div>
  </div>
</section>
''' % (NAP_CITY, towns_list(done), ('<ul class="towns" style="margin-top:10px">%s</ul>' % local_links) if local_links else '',
       ', '.join('<a href="%s">%s, %s</a>' % (city_url(n), n, state_of(n)) if city_url(n) else '%s, %s' % (n, state_of(n)) for n in others) or 'every town in our service area')
    else:
        h += '''
<section class="sec tight" data-note="Links de volta para a página da cidade e para a página geral do serviço.">
  <div class="wrap two-col">
    <div><span class="kicker">More in %s</span><h2>Everything we paint in <span class="kw">%s</span></h2></div>
    <div class="rel" style="grid-template-columns:1fr">
      <a href="/service-areas/%s/">%s<span><b>House painters in %s</b><small>All services &amp; projects in town</small></span><span class="arr">%s</span></a>
      <a href="/services/%s/">%s<span><b>%s</b><small>Our full %s page</small></span><span class="arr">%s</span></a>
    </div>
  </div>
</section>
''' % (city, city, CITY_PAGES[city]['slug'], img(CITY_PAGES[city]['hero'], ''), city, ARR, slug, img(s['menu_img'], ''), s['long'], s['name'].lower(), ARR)
    h += rel_block(s['related'])
    h += quote_section(slug, town=city, title='Get your %s <span class="kw">quote</span>' % s['name'].split(' &')[0].lower(), page=path)
    h += '</main>\n' + footer(sms_href)
    write(path, h)

# ================================================================= PROJETO
def project_page(p):
    s = SVC[p['service']]; path = '/projects/%s/' % p['slug']
    sms_href = sms(s['name']); cl = city_label(p)
    trail = [('Home','/'),('Projects','/projects/'),(p['title'], path)]
    alt = lambda i: '%s in %s — photo %d' % (s['long'], cl, i + 1)
    t = TOWN[p['city']]
    cu = city_url(p['city'])
    graph = [webpage(path, p['title'], desc=p['summary'], image=p['photos'][0][0]), bc_schema(path, trail),
             {'@type':'CreativeWork','@id':SITE+path+'#project','name':p['title'],'abstract':p['summary'],'creator':{'@id':BIZ},'dateCreated':p['date'],
              'genre':s['long'],'about':{'@id':SITE+'/services/%s/#service' % p['service']},
              'locationCreated':{'@type':'Place','name':cl,'address':{'@type':'PostalAddress','addressLocality':p['city'],'addressRegion':p['state'],'addressCountry':'US'},
                                 'geo':{'@type':'GeoCoordinates','latitude':t[2],'longitude':t[3]},'sameAs':wiki(p['city'], p['state'])},
              'image':[{'@type':'ImageObject','contentUrl':SITE+ph[0],'caption':'%s — %s' % (cap, cl)} for ph, cap in [(x, x[1]) for x in p['photos']]]}]
    cover = p['photos'][0][0]
    ptitle = p['title'] + (' | NLS Paint' if len(p['title']) <= 48 else '')
    pdesc = '%s in %s (%s): photos, the prep we did and the colors we used. Text us for a free quote.' % (p['card'], cl, s['long'].lower())
    h = head(ptitle, pdesc, path, graph, og=cover, preload=cover, geo=(p['city'], p['state'], t[2], t[3]), ptype='project', images=[ph[0] for ph in p['photos']])
    h += page_open('projects', path, sms_href, 'project', trail)
    h += '''<section class="hero sub" data-note="%s">
  %s
  <div class="wrap">
    <span class="kicker">%s · %s</span>
    <h1>%s</h1>
    <div class="chips-row"><a href="/services/%s/">%s%s</a>%s<span>%s%s</span></div>
  </div>
</section>
''' % (escape('Capa + H1 (serviço + cidade). ' + p.get('note', '')), img(cover, alt(0), True), s['name'], ym(p['date']), escape(p['title']),
       p['service'], icon('i-roller'), s['name'], ('<a href="%s">%s%s</a>' % (cu, icon('i-pin'), cl)) if cu else '<span>%s%s</span>' % (icon('i-pin'), cl), icon('i-cal'), ym(p['date']))
    city_html = '<a href="%s">%s</a>' % (cu, cl) if cu else cl
    h += '''<section class="qfacts" aria-label="Project facts" data-note="Fatos rápidos: serviço · cidade (link para a página da cidade) · tipo de imóvel · duração. Nunca o endereço.">
  <ul class="wrap">
    <li><small>Service</small><b><a href="/services/%s/">%s</a></b></li>
    <li><small>Town</small><b>%s</b></li>
    <li><small>Property</small><b>%s</b></li>
    <li><small>Duration</small><b>%s</b></li>
  </ul>
</section>
''' % (p['service'], s['name'], city_html, p['type'], p['duration'])
    colors = ''
    if p.get('colors'):
        colors = '<p class="mini-h">Colors &amp; products</p><div class="swatches">%s</div>' % ''.join('<span><i style="background:%s"></i>%s</span>' % (c, escape(n)) for n, c in p['colors'])
    also = ''
    if p.get('also'):
        also = '<p class="mini-h">Also on this job</p><ul class="towns">%s</ul>' % ''.join('<li><a href="/services/%s/">%s</a></li>' % (a, SVC[a]['name']) for a in p['also'])
    h += '''
<section class="sec" data-note="Texto: summary (2–4 frases) + detalhes. Cores/produtos opcionais.">
  <div class="wrap intro-grid">
    <div><span class="kicker">The project</span><h2>What we <span class="kw">did</span></h2></div>
    <div class="prose"><p class="big">%s</p>%s%s%s</div>
  </div>
</section>
''' % (escape(p['summary']), ''.join('<p>%s</p>' % escape(b) for b in p['body']), colors, also)
    shots = ''.join('<button type="button" aria-label="Open photo %d: %s">%s%s<span class="cap">%s</span></button>' % (
        i + 1, escape(cap), roll(src, '%s — %s' % (alt(i), cap)), '<span class="cover">Cover</span>' if i == 0 else '', escape(cap)) for i, (src, cap) in enumerate(p['photos']))
    ba = ''
    if p.get('ba'):
        ba = '''<div style="margin-top:34px"><div class="ba" style="--x:100%%">%s%s<span class="lbl b">Before</span><span class="lbl a">After</span><div class="bar"><span class="knob"><svg><use href="#i-drag"/></svg></span></div></div><p class="ba-note"><svg><use href="#i-drag"/></svg>Drag to compare</p></div>''' % (
            img(p['ba'], s['long'] + ' in ' + cl + ' — before', cls='before'), img(p['ba'], s['long'] + ' in ' + cl + ' — after', cls='after'))
    elif p.get('pair'):
        ba = '''<div class="pcards" style="margin-top:34px"><div class="pcard" style="cursor:default"><div class="roll">%s</div><div class="pc-body"><span class="pill" style="justify-self:start;background:var(--navy);color:#fff;border-color:var(--navy)">Before</span></div></div><div class="pcard" style="cursor:default"><div class="roll">%s</div><div class="pc-body"><span class="pill svc-p" style="justify-self:start">After</span></div></div></div>''' % (
            img(p['pair'][0], s['long'] + ' in ' + cl + ' — before'), img(p['pair'][1], s['long'] + ' in ' + cl + ' — after'))
    h += '''
<section class="sec alt" data-note="Grade de fotos (mín. 4, 1 capa) com lightbox + antes/depois. alt = serviço + cidade + legenda. Fotos entram no sitemap de imagens.">
  <div class="wrap">
    <div class="sec-head row"><div><span class="kicker">Photos</span><h2>Job <span class="kw">photos</span></h2></div><span class="fcount" style="margin:0">%d photos · tap to enlarge</span></div>
    <div class="pgrid">%s</div>
    %s
  </div>
</section>
''' % (len(p['photos']), shots, ba)
    same = sorted([q for q in PROJECTS if q['city'] == p['city'] and q['slug'] != p['slug']], key=lambda q: q['date'], reverse=True)[:3]
    more_title = 'More projects in <span class="kw">%s</span>' % p['city'] if same else 'More <span class="kw">%s</span> projects' % s['name'].split(' &')[0].lower()
    if len(same) < 3:
        same += [q for q in PROJECTS if q['service'] == p['service'] and q['slug'] != p['slug'] and q not in same][:3 - len(same)]
    if len(same) < 3:
        same += [q for q in sorted(PROJECTS, key=lambda q: q['date'], reverse=True) if q['slug'] != p['slug'] and q not in same][:3 - len(same)]
    if len(same) and same[0]['city'] == p['city'] and any(q['city'] != p['city'] for q in same):
        more_title = 'More projects in <span class="kw">%s</span> &amp; nearby' % p['city']
    links = '<a class="link-more" href="/services/%s/">%s in Woonsocket &amp; nearby %s</a>' % (p['service'], s['long'], ARR)
    if cu and cu != '/': links += '<a class="link-more" href="%s">House painters in %s %s</a>' % (cu, cl, ARR)
    h += '''
<section class="sec" data-note="“More projects in [cidade]” + link para o serviço e para a página da cidade.">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Keep looking</span><h2>%s</h2></div>
    <div class="pcards three">%s</div>
    <div style="display:flex;flex-wrap:wrap;gap:12px 28px;margin-top:26px">%s</div>
  </div>
</section>
''' % (more_title, ''.join(pcard(q) for q in same), links)
    h += quote_section(p['service'], town=p['city'], title='Want a result <span class="kw">like this</span>?', page=path)
    lb = '''<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Project photos">
  <header><span></span><button class="close" type="button" aria-label="Close">✕</button></header>
  <div class="stage"><img alt=""></div>
  <div class="nav"><button class="prev" type="button" aria-label="Previous photo"><svg><use href="#i-arrow"/></svg></button><p></p><button class="next" type="button" aria-label="Next photo"><svg><use href="#i-arrow"/></svg></button></div>
</div>'''
    h += '</main>\n' + footer(sms_href, lb)
    write(path, h)

# ================================================================= HUB DE PROJETOS
def projects_hub():
    path = '/projects/'; sms_href = sms(None)
    trail = [('Home','/'),('Projects', path)]
    ps = sorted(PROJECTS, key=lambda p: p['date'], reverse=True)
    desc = 'Photos of real interior, exterior, epoxy and power washing jobs in Woonsocket, Cumberland, Lincoln and nearby towns in RI & MA. Free quotes by text.'
    graph = [webpage(path, 'Painting Projects Around Woonsocket, RI', 'CollectionPage', desc=desc), bc_schema(path, trail),
             {'@type':'ItemList','@id':SITE+path+'#list','itemListElement':[{'@type':'ListItem','position':i+1,'url':SITE+'/projects/%s/' % p['slug'],'name':p['title']} for i, p in enumerate(ps)]}]
    h = head('Painting Projects Around Woonsocket, RI | NLS Paint', desc, path, graph, og=ps[0]['photos'][0][0], ptype='projects_hub', images=[p['photos'][0][0] for p in ps])
    h += page_open('projects', path, sms_href, 'projects_hub', trail)
    h += '''<section class="hero plain" data-note="Hub /projects/ — mais recentes primeiro, sem filtros. Cada card tem serviço + cidade.">
  <div class="wrap">
    <span class="kicker">Portfolio · %d projects</span>
    <h1>Painting Projects Around <em>Woonsocket, RI</em></h1>
    <p>Real homes, rentals and businesses we've painted in Rhode Island and Massachusetts. Tap a project to see every photo.</p>
    <div class="ctas"><a class="btn btn-wine" href="%s" data-ev="click_text"><svg><use href="#i-sms"/></svg>Text us photos — free quote</a></div>
  </div>
  %s
</section>
''' % (len(ps), sms_href, collage(['/img/metal-building-half-painted-woonsocket-ri.webp','/img/porch-steps-white-railings-woonsocket-ri.webp','/img/exterior-siding-spray-painting-cumberland-ri.webp'], 'Recent painting projects'))
    # projetos agrupados por cidade abaixo da grade: links extras para as páginas de cidade
    by_city = ''
    for t in T1:
        n = [p for p in ps if p['city'] == t[0]]
        if n: by_city += '<li><a href="%s">%s%s, %s · %d</a></li>' % (city_url(t[0]), icon('i-pin'), t[0], t[1], len(n))
    h += '''
<section class="sec" data-note="Grade de 2 colunas, mais recentes primeiro.">
  <div class="wrap">
    <div class="pcards" id="plist">%s</div>
    <div class="two-col" style="margin-top:48px"><div><span class="kicker">By town</span><h2>Projects near <span class="kw">you</span></h2></div><div><ul class="towns">%s</ul></div></div>
  </div>
</section>
''' % (''.join(pcard(p) for p in ps), by_city)
    h += cta_band(sms_href, 'Your house <span class="kw" data-color="#0A1E3D">could be next</span>', 'Text us a few photos and your town — we reply the same day.')
    h += '</main>\n' + footer(sms_href)
    write(path, h)

# ================================================================= ÁREAS
def service_areas():
    path = '/service-areas/'; sms_href = sms(None)
    trail = [('Home','/'),('Service Areas', path)]
    desc = 'House painting in Woonsocket, Cumberland, Lincoln, Smithfield, Blackstone, Bellingham and more towns in RI & MA. Same price everywhere. Text us your town.'
    graph = [webpage(path, 'Areas We Serve Around Woonsocket, RI', 'CollectionPage', desc=desc,
                     extra={'spatialCoverage':[place(t[0], t[1]) for t in T1 + T2]}), bc_schema(path, trail)]
    h = head('Areas We Serve Around Woonsocket, RI | NLS Paint', desc, path, graph, ptype='service_areas')
    h += page_open('areas', path, sms_href, 'service_areas', trail)
    h += '''<section class="hero plain" data-note="/service-areas/ — lista TODAS as cidades em texto (camada 1 com link para a página da cidade).">
  <div class="wrap">
    <span class="kicker">Rhode Island &amp; Massachusetts</span>
    <h1>Areas We Serve Around <em>Woonsocket, RI</em></h1>
    <p>We're based in %s and paint homes and businesses in the towns around it — from the Blackstone Valley up to the MetroWest suburbs. Same price in every town.</p>
    <div class="ctas"><a class="btn btn-wine" href="%s" data-ev="click_text"><svg><use href="#i-sms"/></svg>Text us your town</a><a class="btn btn-ghost" href="%s" data-ev="click_call"><svg><use href="#i-call"/></svg>Call %s</a></div>
  </div>
  %s
</section>
''' % (NAP_CITY, sms_href, TEL, PHONE, collage(['/img/stock/green-colonial-exterior-painting-cumberland-ri.webp','/img/stock/living-room-refresh-lincoln-ri.webp','/img/stock/new-england-saltbox-exterior-blackstone-ma.webp'], 'Homes painted around Woonsocket'))
    cards = ''
    for i, t in enumerate(T1):
        n = sum(1 for p in PROJECTS if p['city'] == t[0]); u = city_url(t[0])
        sub = '%d project%s' % (n, '' if n == 1 else 's') if n else 'Serving now'
        if i == 0:
            cards += '<a class="t1card base" href="/"><span class="st">%s</span><b>%s</b><small>Our home base · %s</small><em>Home page %s</em></a>' % (t[1], t[0], sub, ARR)
        elif u:
            c = CITY_PAGES[t[0]]
            cards += '<a class="t1card" href="%s"><span class="st">%s</span><b>%s</b><small>%s · %s</small><em>House painters in %s %s</em></a>' % (u, t[1], t[0], sub, c['facts'][0][1], t[0], ARR)
        else:
            cards += '<div class="t1card"><span class="st">%s</span><b>%s</b><small>%s</small><span class="soon">Town page coming soon</span></div>' % (t[1], t[0], sub)
    rings = ''
    for label, names in BANDS:
        rings += '<div class="ring"><h3>%s<small>%d towns</small></h3>%s</div>' % (label, len(names), towns_list(names))
    h += '''
<section class="sec area" data-note="Mapa estilizado em SVG estático. Sem Google Maps embutido.">
  <div class="wrap area-grid">
    <div>
      <span class="kicker">Service map</span>
      <h2>Painters near <span class="kw">you</span></h2>
      <p class="lead">The dark area is where we paint every week. The dashed ring shows how far we go — about %d miles from Woonsocket.</p>
    </div>
    <div class="mapbox static" id="mapbox" role="img" aria-label="Map of NLS Paint service area around Woonsocket, Rhode Island"></div>
    <div class="area-list">
      <ul class="ticklist">
        <li>%s Same price in every town — no travel fee</li>
        <li>%s Free estimates by text, or a visit for bigger jobs</li>
        <li>%s Same-day reply, Mon–Sat</li>
      </ul>
    </div>
  </div>
</section>
''' % ((B['radius_mi'],) + (icon('i-check'),) * 3)
    h += '''
<section class="sec" data-note="Camada 1 “Your neighbors”: todas as cidades já têm página (gatilho: ≥1 projeto + texto local).">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Tier 1</span><h2>Your <span class="kw">neighbors</span></h2><p class="lead">The towns closest to Woonsocket, where we paint most often.</p></div>
    <div class="t1cards">%s</div>
  </div>
</section>
<section class="sec alt" data-note="Camada 2 “We also serve”, por faixa de distância. Franklin, Milford e Holliston entraram (preferência do Maicow na entrevista). Cada cidade vira página quando bater o gatilho.">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Tier 2</span><h2>We also <span class="kw">serve</span></h2><p class="lead">Grouped by driving distance from Woonsocket, RI.</p></div>
    <div class="rings">%s</div>
    <p class="sameday" style="margin-top:28px">Don't see your town? <a href="%s" data-ev="click_text" style="color:var(--wine)">Text us</a> — we likely cover it.</p>
  </div>
</section>
''' % (cards, rings, sms_href)
    h += quote_section(None, title='Painting in <span class="kw">your town</span>?', page=path)
    h += '</main>\n' + footer(sms_href)
    write(path, h)

# ================================================================= CIDADE (gatilho)
def city_page(city):
    c = CITY_PAGES[city]; st = c['state']; path = '/service-areas/%s/' % c['slug']
    sms_href = sms(None); t = TOWN[city]
    trail = [('Home','/'),('Service Areas','/service-areas/'),('%s, %s' % (city, st), path)]
    ps = sorted([p for p in PROJECTS if p['city'] == city], key=lambda p: p['date'], reverse=True)
    title = 'House Painters in %s, %s | NLS Paint' % (city, st)
    desc = 'House painters in %s, %s: interior & exterior painting, power washing and repairs, %s from Woonsocket. Text photos for a same-day quote.' % (city, st, c['facts'][0][1].lstrip('~'))
    graph = [webpage(path, 'House Painters in %s, %s' % (city, st), desc=desc, image=c['hero'], extra={'spatialCoverage':place(city, st)}), bc_schema(path, trail),
             {'@type':'Service','@id':SITE+path+'#service','name':'House painting in %s, %s' % (city, st),'serviceType':'House Painting','provider':{'@id':BIZ},
              'areaServed':place(city, st),'url':SITE+path,
              'hasOfferCatalog':{'@type':'OfferCatalog','name':'Painting services in %s' % city,'itemListElement':[{'@type':'Offer','itemOffered':{'@id':SITE+'/services/%s/#service' % s['slug']}} for s in SERVICES]}},
             faq_schema(path, c['faq'])]
    h = head(title, desc, path, graph, og=c['hero'], preload=c['hero'], geo=(city, st, t[2], t[3]), ptype='city', images=[c['hero']] + [p['photos'][0][0] for p in ps])
    h += page_open('areas', path, sms_href, 'city', trail)
    h += '''<section class="hero sub" data-note="Página de cidade — GATILHO: ≥1 projeto publicado na cidade + parágrafo local escrito à mão. H1 “House Painters in [cidade], [UF]”.">
  %s
  <div class="wrap">
    <span class="gate">Página por gatilho</span><br>
    <span class="kicker">Local painters · %s from Woonsocket</span>
    <h1>House Painters in <em>%s, %s</em></h1>
    <p>Interior and exterior painting, power washing and repairs for %s homes, rentals and businesses — from a local painter just down the road in Woonsocket.</p>
    <div class="ctas">
      <a class="btn btn-wine" href="%s" data-ev="click_text"><svg><use href="#i-sms"/></svg>Text us photos — free quote</a>
      <a class="btn btn-ghost" href="%s" data-ev="click_call"><svg><use href="#i-call"/></svg>Call %s</a>
    </div>
  </div>
</section>
''' % (img(c['hero'], 'House painting in %s, %s' % (city, st), True), c['facts'][0][1], city, st, city, sms_href, TEL, PHONE)
    h += local_block(city, c['local'], c['facts'], 'Painting in %s' % city, 'Your neighbors in <span class="kw">Woonsocket</span>',
                     'Parágrafo local ESCRITO À MÃO: bairros/vilas, tipos de casa, distância. É o que diferencia a página (evita “doorway page”). RASCUNHO: confirmar com o Maicow.')
    h += '''
<section class="sec alt" data-note="Projetos nesta cidade (automático) — a prova local que libera a página.">
  <div class="wrap">
    <div class="sec-head row"><div><span class="kicker">Local work</span><h2>Projects in <span class="kw">%s</span></h2></div><a class="link-more" href="/projects/">All projects %s</a></div>
    <div class="pcards three">%s</div>
  </div>
</section>
''' % (city, ARR, ''.join(pcard(p) for p in ps))
    svc = ''
    for s in SERVICES:
        sc = [x for x in SERVICE_CITY if x['city'] == city and x['service'] == s['slug']]
        href = '/service-areas/%s/%s/' % (c['slug'], s['slug']) if sc else '/services/%s/' % s['slug']
        svc += '<a href="%s">%s<span>%s</span></a>' % (href, img(s['menu_img'], '%s in %s, %s' % (s['long'], city, st)), s['name'])
    h += '''
<section class="sec" data-note="Serviços (links para os 6; aponta para a página serviço × cidade quando ela existe).">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Services in %s</span><h2>What we paint in <span class="kw">%s</span></h2></div>
    <div class="svc-mini">%s</div>
  </div>
</section>
''' % (city, city, svc)
    h += '''
<section class="sec area" data-note="Cidades vizinhas (links quando a página existe) + mapa estático com a cidade destacada.">
  <div class="wrap area-grid">
    <div><span class="kicker">Nearby</span><h2>Towns near <span class="kw">%s</span></h2><p class="lead">We also paint in the towns next door.</p></div>
    <div class="mapbox static" id="mapbox" data-focus="%s" role="img" aria-label="Map showing %s, %s and nearby towns served by NLS Paint"></div>
    <div class="area-list">%s<p class="towns-note"><a href="/service-areas/" style="color:var(--wine);font-weight:700">See every town we serve</a></p></div>
  </div>
</section>
''' % (city, city, city, st, towns_list(c['near']))
    h += faq_block(c['faq'], kicker='%s FAQ' % city, title='Painting in <span class="kw">%s</span>' % city, note='FAQ curto da cidade (FAQPage) + CTA.')
    h += quote_section(None, town=city, title='Free quote in <span class="kw">%s</span>' % city, page=path)
    h += '</main>\n' + footer(sms_href)
    write(path, h)

# ================================================================= ABOUT
def about():
    path = '/about/'; sms_href = sms(None)
    trail = [('Home','/'),('About', path)]
    desc = 'NLS Paint is owned and run by Maicow, a house painter in Woonsocket, RI with 8 years of experience. You call him, he quotes it, he paints it.'
    graph = [webpage(path, 'Meet Maicow — Your Woonsocket House Painter', 'AboutPage', desc=desc, extra={'mainEntity':{'@id':PERSON}}), bc_schema(path, trail),
             {'@type':'Person','@id':PERSON,'name':'Maicow','jobTitle':'Owner & house painter','worksFor':{'@id':BIZ},
              'homeLocation':place(B['city'], B['state']),'knowsAbout':['House painting','Interior painting','Exterior painting','Epoxy floor coating']}]
    h = head('Meet Maicow — Your Woonsocket House Painter | NLS Paint', desc, path, graph, preload='/img/stock/paint-roller-maicow-placeholder.webp', ptype='about')
    h += page_open('about', path, sms_href, 'about', trail)
    h += '''<section class="about-hero who" data-note="H1 + foto com a camisa da empresa (PENDENTE: placeholder). Person no schema como founder da empresa (E-E-A-T).">
  <div class="wrap who-grid">
    <div class="photo">
      <div class="roll">%s</div>
      <span class="pending">Placeholder · Maicow's photo here</span>
      <span class="badge">8 years<b>painting</b></span>
    </div>
    <div>
      <span class="kicker" style="color:#F2A3A8">About NLS Paint</span>
      <h1>Meet <span class="kw">Maicow</span> — Your Woonsocket House Painter</h1>
      <p class="quote">“You call me, you get me. I quote it, I paint it, and I don't leave until you love it.”</p>
      <p class="sig">— Maicow, owner of NLS Paint</p>
      <div class="ctas" style="display:flex;flex-wrap:wrap;gap:12px;margin-top:22px">
        <a class="btn btn-wine" href="%s" data-ev="click_text"><svg><use href="#i-sms"/></svg>Text Maicow</a>
        <a class="btn btn-ghost" href="%s" data-ev="click_call"><svg><use href="#i-call"/></svg>Call %s</a>
      </div>
    </div>
  </div>
</section>
''' % (img('/img/stock/paint-roller-maicow-placeholder.webp', 'Maicow, owner and house painter at NLS Paint in Woonsocket, RI', True), sms_href, TEL, PHONE)
    h += '''
<section class="sec" data-note="História curta na voz dele. RASCUNHO montado com dados da entrevista: reescrever com o Maicow.">
  <div class="wrap intro-grid">
    <div><span class="kicker">My story</span><h2>Why I <span class="kw">paint</span></h2></div>
    <div class="story">
      <span class="pending-txt">Draft — to be written with Maicow</span>
      <p>I've been painting for about eight years — first in Brazil, and now here in Rhode Island and Massachusetts.</p>
      <p>I started NLS Paint because I like doing the whole job myself: I look at your house, I give you the price, and I'm the one holding the brush. When a job is big, I bring a helper I trust, but I'm on site every day.</p>
      <p>Interiors are my favorite — taking a tired room and making it feel new in a day or two. Exteriors are where the prep really matters, and I never skip it.</p>
      <p>I use paint I trust, mostly Benjamin Moore and Sherwin-Williams. And I answer every message the same day, because I know how hard it is to get a painter to call you back.</p>
      <p>Most of my work is around Woonsocket — <a href="/service-areas/cumberland-ri/">Cumberland</a>, <a href="/service-areas/lincoln-ri/">Lincoln</a>, <a href="/service-areas/north-smithfield-ri/">North Smithfield</a>, <a href="/service-areas/blackstone-ma/">Blackstone</a> and <a href="/service-areas/bellingham-ma/">Bellingham</a> — but I'll drive further for the right job.</p>
    </div>
  </div>
</section>
'''
    h += '''
<section class="sec alt" data-note="3 compromissos concretos e verificáveis.">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">My promise</span><h2>3 things you can <span class="kw">count on</span></h2></div>
    <ul class="promise">
      <li>%s<b>Your home protected</b><span>Furniture moved and covered, floors and plants protected before any paint is opened.</span><em>%sEvery job, every room</em></li>
      <li>%s<b>Clean every day</b><span>Tools packed, chips picked up and rooms usable again at the end of each day — not just the last one.</span><em>%sDaily clean-up</em></li>
      <li>%s<b>Same-day reply</b><span>Text or call and you'll hear back the same day, Monday to Saturday, with a clear price.</span><em>%sMon–Sat 7am–7pm</em></li>
    </ul>
  </div>
</section>
''' % (icon('i-shield'), icon('i-check'), icon('i-broom'), icon('i-check'), icon('i-bolt'), icon('i-check'))
    picks = ['commercial-repaint-metal-building-woonsocket-ri', 'porch-steps-railings-woonsocket-ri', 'exterior-siding-repaint-cumberland-ri', 'epoxy-floor-garage-shop-bellingham-ma']
    strip_html = ''.join('<a href="/projects/%s/">%s<span>%s · %s</span></a>' % (q, roll(PROJ[q]['photos'][1 if q.startswith('commercial') else 0][0], '%s in %s' % (SVC[PROJ[q]['service']]['long'], city_label(PROJ[q]))), PROJ[q]['card'], city_label(PROJ[q])) for q in picks)
    h += '''
<section class="sec" data-note="Fotos dele trabalhando, puxadas dos projetos.">
  <div class="wrap">
    <div class="sec-head row"><div><span class="kicker">On the job</span><h2>Recent <span class="kw">work</span></h2></div><a class="link-more" href="/projects/">All projects %s</a></div>
    <div class="strip">%s</div>
  </div>
</section>
''' % (ARR, strip_html)
    h += '''
<section class="sec alt tight" data-note="Para quem pintamos (mesmo bloco da home).">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Who I paint for</span><h2>Homes, rentals &amp; <span class="kw">business</span></h2></div>
    <div class="aud">
      <div><svg><use href="#i-home"/></svg><b>Homeowners</b><span>Single rooms to full exterior repaints.</span></div>
      <div><svg><use href="#i-key"/></svg><b>Landlords</b><span>Fast rental turnovers between tenants.</span></div>
      <div><svg><use href="#i-sign"/></svg><b>Realtors</b><span>Pre-listing touch-ups that help homes sell.</span></div>
      <div><svg><use href="#i-hammer"/></svg><b>Contractors</b><span>Reliable paint sub for your projects.</span></div>
    </div>
  </div>
</section>
'''
    h += quote_section(None, title='Let\'s talk about <span class="kw">your project</span>', page=path)
    h += '</main>\n' + footer(sms_href)
    write(path, h)

# ================================================================= CONTATO
def contact():
    path = '/contact/'; sms_href = sms(None)
    trail = [('Home','/'),('Contact', path)]
    desc = 'Text photos to %s for a free painting estimate in Woonsocket, RI and nearby towns. Same-day reply, %s.' % (PHONE, B['hours'])
    graph = [webpage(path, 'Get a Free Painting Estimate', 'ContactPage', desc=desc, extra={'mainEntity':{'@id':BIZ}}), bc_schema(path, trail)]
    h = head('Get a Free Painting Estimate | NLS Paint, Woonsocket RI', desc, path, graph, ptype='contact')
    h += page_open('contact', path, sms_href, 'contact', trail)
    h += '''<section class="hero plain" data-note="H1 “Get a Free Painting Estimate”.">
  <div class="wrap">
    <span class="kicker">Replying today · Free estimates</span>
    <h1>Get a Free <em>Painting Estimate</em></h1>
    <p>The fastest way is a text with a few photos. You'll get a clear price the same day — no visit needed for most jobs.</p>
  </div>
  %s
</section>
''' % collage(['/img/porch-steps-trim-painting-woonsocket-ri.webp','/img/stock/interior-living-room-painting-lincoln-ri.webp','/img/metal-building-after-gray-woonsocket-ri.webp'], 'Recent work')
    gbp = '<a class="g" href="%s" rel="noopener">%s See us on Google</a>' % (B['gbp'], icon('i-google')) if B['gbp'] else '<span class="g" data-note="PENDENTE: link do Google Meu Negócio (BUSINESS[\'gbp\'] no content.py).">%s See us on Google</span>' % icon('i-google')
    h += '''
<section class="sec" data-note="3 botões: Text photos (principal) · Call · formulário. NAP IDÊNTICO ao Google Meu Negócio (mesmo nome, cidade, CEP, telefone, horário). Sem mapa com pino (service-area business).">
  <div class="wrap contact-grid">
    <div>
      <span class="kicker">Pick one</span>
      <h2>3 ways to <span class="kw">reach us</span></h2>
      <div class="bigbtns" style="margin-top:24px">
        <a class="bigbtn main" href="%(sms)s" data-ev="click_text"><i>%(isms)s</i><span><b>Text photos<span class="tag">FASTEST</span></b><small>Send pictures + your town to %(phone)s</small></span><span class="arr">%(arr)s</span></a>
        <a class="bigbtn" href="%(tel)s" data-ev="click_call"><i>%(icall)s</i><span><b>Call</b><small>%(phone)s · %(hours)s</small></span><span class="arr">%(arr)s</span></a>
        <a class="bigbtn" href="#quote"><i>%(iform)s</i><span><b>Fill out the form</b><small>We'll text you back to ask for photos</small></span><span class="arr">%(arr)s</span></a>
      </div>
      <p class="sameday">We reply the same day.</p>
    </div>
    <aside class="napcard">
      <h2>NLS Paint</h2>
      <dl>
        <dt>Location</dt><dd>%(nap)s</dd>
        <dt>Phone</dt><dd><a href="%(tel)s" data-ev="click_call">%(phone)s</a></dd>
        <dt>Hours</dt><dd>%(hours)s</dd>
        <dt>Service area</dt><dd>Serving Woonsocket and nearby towns in RI &amp; MA — <a href="/service-areas/">see all towns</a></dd>
        <dt>Payment</dt><dd>Cash, check, Zelle &amp; Venmo</dd>
      </dl>
      %(gbp)s
    </aside>
  </div>
</section>
''' % {'sms':sms_href, 'tel':TEL, 'phone':PHONE, 'arr':ARR, 'isms':icon('i-sms'), 'icall':icon('i-call'), 'iform':icon('i-form'), 'gbp':gbp, 'nap':NAP_CITY, 'hours':B['hours']}
    h += quote_section(None, title='Request a <span class="kw">free quote</span>', lead='Prefer a form? Leave your name, phone and town — we\'ll text you back today to ask for a few photos.', page=path)
    h += '</main>\n' + footer(sms_href)
    write(path, h)

# ================================================================= PRIVACIDADE
def privacy():
    path = '/privacy/'; sms_href = sms(None)
    trail = [('Home','/'),('Privacy', path)]
    desc = 'How NLS Paint uses the information you send through our quote form and the analytics on this website.'
    h = head('Privacy Policy | NLS Paint', desc, path, [webpage(path, 'Privacy Policy', desc=desc), bc_schema(path, trail)], ptype='privacy')
    h += page_open('', path, sms_href, 'privacy', trail)
    h += '''<section class="hero plain" data-note="Texto simples cobrindo GA4 e os dados do formulário. RASCUNHO: revisar.">
  <div class="wrap"><span class="kicker">Last updated: October 2026</span><h1>Privacy <em>Policy</em></h1><p>Short and plain: what we collect, why, and what we don't do with it.</p></div>
</section>
<section class="sec">
  <div class="wrap prose">
    <h2>What we collect</h2>
    <p>When you fill out the quote form, we receive your <strong>name, phone number, town, the service you need and your message</strong>, plus the page you sent it from. When you text or call us, we see your phone number and anything you choose to send, like photos.</p>
    <h2>How we use it</h2>
    <ul><li>To reply to you and prepare your estimate.</li><li>To schedule and do the work, and follow up afterwards.</li></ul>
    <p>We don't sell or rent your information, and we don't add you to marketing lists.</p>
    <h2>Website analytics</h2>
    <p>This site uses <strong>Google Analytics 4</strong> to count visits and see which pages lead to a text, a call or a form. Google Analytics uses cookies and collects information such as pages viewed, device type and approximate location. It doesn't tell us who you are. You can opt out with the <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">Google Analytics opt-out add-on</a>.</p>
    <h2>Form delivery</h2>
    <p>The quote form is delivered to our email by a form service (Formspree or Web3Forms), which processes the data only to send it to us.</p>
    <h2>Photos of your property</h2>
    <p>We only publish photos of a job with your permission. We never publish your street address — at most the town — and we remove location data from every photo before it goes online.</p>
    <h2>Questions</h2>
    <p>Text or call <a href="%s">%s</a> and we'll answer, or ask us to delete what we have about you.</p>
  </div>
</section>
''' % (TEL, PHONE)
    h += '</main>\n' + footer(sms_href)
    write(path, h)

# ================================================================= 404
def not_found():
    path = '/404.html'; sms_href = sms(None)
    h = head('Page Not Found | NLS Paint', 'This page doesn\'t exist. See our painting services in Woonsocket, RI or text us for a free quote.', '/404.html', [], noindex=True)
    h += page_open('', path, sms_href, '404')
    svc = ''.join('<a href="/services/%s/">%s<span>%s</span></a>' % (s['slug'], img(s['menu_img'], s['long']), s['name']) for s in SERVICES)
    h += '''<section class="sec" data-note="404: noindex + links para os 6 serviços + CTA.">
  <div class="wrap">
    <div class="nf">
      <div class="big404" aria-hidden="true">404<span class="drip"></span></div>
      <h1 style="font-size:clamp(2rem,6vw,3rem);color:var(--navy);margin-top:12px">This wall is <span class="kw">still blank</span></h1>
      <p>The page you're looking for doesn't exist or has moved. Try one of our services below — or just text us.</p>
      <div class="ctas"><a class="btn btn-wine" href="%s" data-ev="click_text"><svg><use href="#i-sms"/></svg>Text us photos — free quote</a><a class="btn btn-line" href="/">Back to home</a></div>
    </div>
    <div class="svc-mini" style="margin-top:48px">%s</div>
  </div>
</section>
''' % (sms_href, svc)
    h += '</main>\n' + footer(sms_href)
    write(path, h)

# ================================================================= sitemap + robots
PRIORITY = {'home':'1.0','services_hub':'0.8','service':'0.9','city':'0.8','service_city':'0.7','projects_hub':'0.7','service_areas':'0.8','project':'0.6','about':'0.5','contact':'0.6','privacy':'0.2'}
def sitemap():
    xs = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for p in PAGES:
        imgs = ''.join('<image:image><image:loc>%s</image:loc></image:image>' % escape(SITE + i) for i in dict.fromkeys(p['images']))
        xs.append('  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority>%s</url>' % (SITE + p['path'], TODAY, PRIORITY.get(p['type'], '0.5'), imgs))
    xs.append('</urlset>')
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n') as f: f.write('\n'.join(xs) + '\n')
    with open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8', newline='\n') as f:
        if STAGING: f.write('# Ambiente de homologação: todas as páginas têm noindex (meta + cabeçalho X-Robots-Tag).\nUser-agent: *\nAllow: /\n')
        else: f.write('User-agent: *\nAllow: /\nDisallow: /_gerador/\n\nSitemap: %s/sitemap.xml\n' % SITE)
    # nginx: em dev manda o cabeçalho X-Robots-Tag em tudo (imagens inclusive)
    conf = open(os.path.join(HERE, 'nginx.conf.tpl'), encoding='utf-8').read()
    conf = conf.replace('{{robots}}', '    add_header X-Robots-Tag "noindex, nofollow" always;\n' if STAGING else '')
    with open(os.path.join(ROOT, 'nginx.conf'), 'w', encoding='utf-8', newline='\n') as f: f.write(conf)
    print('   /sitemap.xml (%d URLs)  /robots.txt' % len(PAGES))

# ================================================================= relatório de SEO on-page
def report():
    issues, rows = [], []
    titles, descs = {}, {}
    files = [f for f in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True) if '_gerador' not in f]
    for f in sorted(files):
        rel = '/' + os.path.relpath(f, ROOT).replace(os.sep, '/').replace('index.html', '')
        html = open(f, encoding='utf-8').read()
        title = strip(re.search(r'<title>(.*?)</title>', html).group(1))
        desc = re.search(r'<meta name="description" content="(.*?)">', html).group(1).replace('&amp;', '&')
        h1 = len(re.findall(r'<h1[ >]', html))
        noalt = len(re.findall(r'<img(?![^>]*\balt=)[^>]*>', html))
        nodim = len(re.findall(r'<img(?![^>]*\bwidth=)[^>]*src="/[^"]+"[^>]*>', html))
        words = len(re.sub(r'\s+', ' ', strip(re.sub(r'(?s)<(script|style|svg|header|footer|nav)[^>]*>.*?</\1>', ' ', html))).split())
        for h in re.findall(r'href="(/[^"#]*)', html):
            target = os.path.join(ROOT, h.lstrip('/').replace('/', os.sep))
            if not (os.path.isfile(target) or os.path.isfile(os.path.join(target, 'index.html'))):
                issues.append('%s → link quebrado %s' % (rel, h))
        for s in re.findall(r'src="(/[^"]+)"', html):
            if not os.path.isfile(os.path.join(ROOT, s.lstrip('/'))): issues.append('%s → imagem inexistente %s' % (rel, s))
        if '404' not in rel:
            if len(title) > 60: issues.append('%s → title com %d caracteres (> 60)' % (rel, len(title)))
            if len(desc) > 160: issues.append('%s → description com %d caracteres (> 160)' % (rel, len(desc)))
            titles.setdefault(title, []).append(rel); descs.setdefault(desc, []).append(rel)
        if h1 != 1: issues.append('%s → %d H1' % (rel, h1))
        if noalt: issues.append('%s → %d imagens sem alt' % (rel, noalt))
        for blk in re.findall(r'<script type="application/ld\+json">\n(.*?)\n</script>', html, re.S): json.loads(blk)
        rows.append('| `%s` | %d | %d | %d | %d |' % (rel, len(title), len(desc), h1, words))
    issues += ['title duplicado: %s' % v for v in titles.values() if len(v) > 1]
    issues += ['description duplicada: %s' % v for v in descs.values() if len(v) > 1]
    out = ['# Relatório de SEO on-page', '', 'Gerado por `build.py` em %s. %d páginas, %d no sitemap.' % (TODAY, len(files), len(PAGES)), '',
           '## Problemas', ''] + (['- ' + i for i in issues] or ['Nenhum: títulos ≤ 60, descriptions ≤ 160, 1 H1 por página, todas as imagens com alt, nenhum link interno quebrado, JSON-LD válido.']) + [
           '', '## Páginas', '', '| URL | title | description | H1 | palavras |', '|---|---|---|---|---|'] + rows
    with open(os.path.join(HERE, 'seo-report.md'), 'w', encoding='utf-8', newline='\n') as f: f.write('\n'.join(out) + '\n')
    print('\nRelatório: _gerador/seo-report.md — %d problema(s)' % len(issues))
    for i in issues: print('  !', i)

# ================================================================= run
if __name__ == '__main__':
    print('Gerando site (%s: %s) em' % (ENV, SITE), ROOT)
    for p in PROJECTS:
        assert len(p['photos']) >= 4, p['slug'] + ': mínimo 4 fotos'
        for f in [ph[0] for ph in p['photos']]: assert os.path.exists(ROOT + f), f
    for c, d in CITY_PAGES.items():
        assert any(p['city'] == c for p in PROJECTS), c + ': página de cidade sem projeto (gatilho não batido)'
    home(); services_hub()
    for s in SERVICES: service_page(s)
    for p in PROJECTS: project_page(p)
    projects_hub(); service_areas()
    for c in CITY_PAGES: city_page(c)
    for sc in SERVICE_CITY: service_page(SVC[sc['service']], sc['city'], sc['local'], sc.get('hero'))
    about(); contact(); privacy(); not_found()
    sitemap(); report()
    print('ok')
