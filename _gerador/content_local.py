# -*- coding: utf-8 -*-
"""Conteúdo de SEO local acrescentado no site completo: novas páginas de cidade e os dados da home.
RASCUNHO escrito a partir de geografia pública — o Maicow precisa revisar (bairros onde ele realmente trabalha)."""
from content import CITY_PAGES

# ---------------------------------------------------------------- novas páginas de cidade (gatilho batido: ≥1 projeto publicado na cidade)
CITY_PAGES['North Smithfield'] = {
  'slug':'north-smithfield-ri','state':'RI','hero':'/img/stock/drywall-sanding-before-painting-north-smithfield-ri.webp',
  'local':[
    'North Smithfield wraps around the west side of Woonsocket, so most homes in town are five to ten minutes from us — close enough to stop by after another job and measure.',
    'We work in Slatersville, Forestdale, Union Village and Primrose: historic mill-village houses with lots of trim and old layers of paint, mid-century ranches and capes, and newer colonials off Route 146A. Landlords with units near the Woonsocket line call us for quick turnovers between tenants.',
    'Older homes here often have plaster walls and original woodwork, so we patch, prime and caulk carefully before any color goes on.'
  ],
  'facts':[('From Woonsocket','~5–10 min'),('Villages','Slatersville · Forestdale · Union Village · Primrose'),('Common homes','Mill houses, ranches, colonials'),('Estimate visit','Same week')],
  'near':['Woonsocket','Smithfield','Lincoln','Blackstone','Mendon'],
  'faq':[('Do you work on older mill-village homes in Slatersville?','Yes. Older houses need more scraping, priming and caulking, and we include that prep in the quote so there are no surprises.'),
         ('Can you turn over a rental unit in North Smithfield quickly?',"Usually in 1–3 days: patching, caulking and fresh paint, scheduled around your next tenant's move-in date.")],
}
CITY_PAGES['Smithfield'] = {
  'slug':'smithfield-ri','state':'RI','hero':'/img/stock/craftsman-exterior-painting-smithfield-ri.webp',
  'local':[
    "Smithfield is about fifteen to twenty minutes south of Woonsocket on Route 146 and Route 104, and we're in town regularly from spring to fall.",
    'We paint colonials, raised ranches and capes in Greenville, Georgiaville, Esmond and Stillwater, and the newer neighborhoods near Bryant University and Route 7 — from a single bedroom to a full exterior repaint.',
    'Many Smithfield homes sit on wooded lots near the ponds and orchards, which means shade, moisture and mildew on the siding. A soft wash and a mildew-resistant exterior paint make the new finish last.'
  ],
  'facts':[('From Woonsocket','~15–20 min'),('Villages','Greenville · Georgiaville · Esmond · Stillwater'),('Common homes','Colonials, raised ranches, capes'),('Estimate visit','Same week')],
  'near':['North Smithfield','Lincoln','Woonsocket','Cumberland'],
  'faq':[('Do you charge more to drive to Smithfield?','No. Pricing is the same in every town we serve, and estimates are always free.'),
         ('My siding has green mildew — do I need to paint or just wash?',"Often a soft wash is enough. If the paint is chalky or peeling under the mildew, we'll show you photos and quote a repaint instead.")],
}
CITY_PAGES['Blackstone'] = {
  'slug':'blackstone-ma','state':'MA','hero':'/img/stock/new-england-saltbox-exterior-blackstone-ma.webp',
  'local':[
    'Blackstone sits right across the state line from Woonsocket — most of town is five minutes from us up Route 122 — so Massachusetts customers here get the same fast response as our Rhode Island neighbors.',
    'We paint older two- and three-family homes near the river and Blackstone center, capes and ranches in East Blackstone and Waterford, and farmhouses and barns on the bigger lots toward Mendon.',
    'Wood clapboard and old porches are common in town, so exterior jobs here start with careful scraping, priming bare wood and re-caulking windows before two finish coats.'
  ],
  'facts':[('From Woonsocket','~5 min'),('Areas','Blackstone center · East Blackstone · Waterford'),('Common homes','Multifamilies, capes, farmhouses'),('Estimate visit','Same week')],
  'near':['Woonsocket','Bellingham','Mendon','North Smithfield','Cumberland'],
  'faq':[("Do you serve Massachusetts even though you're based in Rhode Island?",'Yes. Blackstone is right next door to Woonsocket, and we work across the state line every week at the same prices.'),
         ('Can you paint a barn or outbuilding along with the house?','Yes. We quote barns, sheds and garages together with the house so everything matches.')],
}
CITY_PAGES['Bellingham'] = {
  'slug':'bellingham-ma','state':'MA','hero':'/img/stock/kitchen-cabinet-painting-bellingham-ma.webp',
  'local':[
    'Bellingham is about fifteen minutes north of Woonsocket via Route 126, close to I-495, and we paint homes and businesses there throughout the year.',
    'Most homes we see are ranches, split-levels and capes from the 1960s to the 1980s in North and South Bellingham and around Caryville, plus newer colonials — great candidates for interior updates, kitchen repaints and fresh exteriors.',
    'We also work with shops and small commercial spaces along Route 126 and Hartford Avenue: garage floors, epoxy coatings and bright, washable walls and ceilings.'
  ],
  'facts':[('From Woonsocket','~15 min'),('Areas','North Bellingham · South Bellingham · Caryville'),('Common homes','Ranches, split-levels, colonials'),('Estimate visit','Same week')],
  'near':['Blackstone','Woonsocket','Mendon','Franklin','Milford'],
  'faq':[('Do you paint commercial spaces in Bellingham?','Yes — shops, garages and offices. We can work early, late or on Saturdays so your business stays open.'),
         ('Do you do epoxy garage floors in Bellingham?','Yes. We grind, repair and coat garage and shop floors, and add color flakes and an anti-slip topcoat on request.')],
}

# ---------------------------------------------------------------- home (= página de Woonsocket)
HOME = {
  'title':'House Painters in Woonsocket, RI | NLS Paint',
  'desc':'Local house painters in Woonsocket, RI. Interior & exterior painting, epoxy floors and power washing in RI & MA. Text photos for a same-day free quote.',
  'hero':'/img/stock/white-colonial-house-exterior-painting-woonsocket-ri.webp',
  # parágrafo local da cidade-base (Woonsocket não ganha página própria: a home é a página dela)
  'local':[
    'Woonsocket is home base. We paint the triple-deckers and mill-era multifamilies in Social, Fairmount and the Globe, the capes and colonials in the North End and East Woonsocket, and storefronts and commercial buildings across the city.',
    'Triple-deckers and older multifamilies are a specialty: tall walls, lots of porches and trim, and landlords who need units turned over between tenants without losing a month of rent.',
    "Because we're local, we can come out the same week for a free estimate and start small jobs within days."
  ],
  'local_facts':[('Based in','Woonsocket, RI 02895'),('Neighborhoods','North End · East Woonsocket · Social · Fairmount · Globe · Bernon'),('Common homes','Triple-deckers, multifamilies, capes'),('Hours','Mon–Sat 7am–7pm')],
  'faq':[
    ('Do you charge for estimates?',"No. Estimates are always free — just text us a few photos, or we'll come out for bigger jobs."),
    ('Do you paint furnished homes?',"Yes. We move and cover your furniture and floors before we start, and put everything back when we're done."),
    ('Who buys the paint?',"We do. Paint and materials are included in your quote, and you choose the colors. If you already have paint, tell us and we'll quote labor only."),
    ('How fast can you start?',"Small jobs often start within a week. We'll give you a start date with your quote."),
    ('What payment do you accept?','Cash, check, Zelle and Venmo. A small deposit (about 20%) covers materials on bigger jobs.'),
    ('Do you charge extra to travel to my town?','No. The price is the same in Woonsocket and in every town we serve in Rhode Island and Massachusetts.'),
  ],
  # galeria presa: (slug do projeto, foto). A ordem é a ordem da galeria.
  'gallery':[
    ('commercial-repaint-metal-building-woonsocket-ri','/img/commercial-exterior-repaint-woonsocket-ri-wide.webp'),
    ('living-room-hallway-repaint-lincoln-ri','/img/stock/living-room-refresh-lincoln-ri.webp'),
    ('exterior-repaint-colonial-cumberland-ri','/img/stock/cape-style-home-exterior-cumberland-ri.webp'),
    ('exterior-siding-repaint-cumberland-ri','/img/exterior-siding-spray-painting-cumberland-ri.webp'),
    ('kitchen-walls-cabinets-bellingham-ma','/img/stock/kitchen-cabinet-painting-bellingham-ma.webp'),
    ('craftsman-exterior-painting-smithfield-ri','/img/stock/craftsman-exterior-painting-smithfield-ri.webp'),
  ],
}
