# -*- coding: utf-8 -*-
"""Conteúdo do protótipo (equivale às content collections do Astro no site final).
Textos em inglês. Projetos e textos locais são FICTÍCIOS/ILUSTRATIVOS onde marcado em `note`."""

# ---------------------------------------------------------------- cidades
# [nome, UF, lat, lon] — mesmas da home
T1 = [['Woonsocket','RI',42.003,-71.515],['Cumberland','RI',41.967,-71.433],['Lincoln','RI',41.921,-71.435],['North Smithfield','RI',41.966,-71.550],['Smithfield','RI',41.922,-71.549],['Blackstone','MA',42.018,-71.541],['Bellingham','MA',42.087,-71.475]]
T2 = [['Franklin','MA',42.083,-71.397],['Milford','MA',42.140,-71.516],['Mendon','MA',42.106,-71.552],['Upton','MA',42.174,-71.602],['Medway','MA',42.141,-71.396],['Wrentham','MA',42.067,-71.328],['Norfolk','MA',42.119,-71.325],['Holliston','MA',42.200,-71.425],['Dover','MA',42.246,-71.283],['Sherborn','MA',42.239,-71.370],['Westwood','MA',42.214,-71.224],['Wellesley','MA',42.297,-71.293],['Weston','MA',42.367,-71.303],['Wayland','MA',42.363,-71.361],['Lexington','MA',42.447,-71.225],['Concord','MA',42.460,-71.349],['Sudbury','MA',42.384,-71.416],['Carlisle','MA',42.529,-71.350],['Hingham','MA',42.242,-70.889],['Cohasset','MA',42.242,-70.804]]
BANDS = [
    ('Up to 15 mi', ['Franklin','Milford','Mendon','Upton','Medway','Wrentham','Norfolk']),
    ('15–25 mi', ['Holliston','Dover','Sherborn','Westwood']),
    ('25–35 mi', ['Wellesley','Weston','Wayland']),
    ('35–50 mi', ['Lexington','Concord','Sudbury']),
    ('50–70 mi', ['Carlisle','Hingham','Cohasset']),
]
STATE_NAME = {'RI':'Rhode Island', 'MA':'Massachusetts'}
def wiki(name, st):
    """Página da cidade na Wikipedia: vira `sameAs` no schema (ajuda o Google a ligar o nome ao lugar certo)."""
    return 'https://en.wikipedia.org/wiki/%s,_%s' % (name.replace(' ', '_'), STATE_NAME[st].replace(' ', '_'))

# ---------------------------------------------------------------- empresa (NAP — tem que bater 100% com o Google Meu Negócio)
BUSINESS = {
  'name':'NLS Paint',
  'legal':'',                       # TODO: nome da LLC quando abrir
  'phone':'(774) 586-9824', 'phone_e164':'+17745869824', 'phone_schema':'+1-774-586-9824',
  'city':'Woonsocket', 'state':'RI', 'zip':'02895',
  'lat':42.0029, 'lon':-71.5148,   # centro de Woonsocket (sem endereço de rua: service-area business)
  'hours':'Mon–Sat 7am–7pm', 'opens':'07:00', 'closes':'19:00',
  'days':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],
  'payment':'Cash, Check, Zelle, Venmo',
  'radius_mi':70,
  'founded':'2026',
  'gbp':'',        # TODO: link do perfil no Google (https://g.page/... ou maps.app.goo.gl/...)
  'gbp_review':'', # TODO: link "escrever avaliação" do Google
  'same_as':[],    # TODO: Instagram, Facebook, Nextdoor, Thumbtack, Yelp, BBB — só perfis que existem e com o MESMO NAP
}

# ---------------------------------------------------------------- serviços
SERVICES = [
 {
  'slug':'exterior-painting','name':'Exterior Painting','long':'Exterior House Painting','short':'Siding, trim, doors & shutters',
  'title':'Exterior House Painting in Woonsocket, RI | NLS Paint',
  'desc':'Exterior house painting in Woonsocket, RI & nearby towns: power washing, scraping, priming and two finish coats. Text photos for a same-day quote.',
  'h1':'Exterior House Painting in <em>Woonsocket, RI</em> &amp; Nearby Towns',
  'kw':'outside',
  'hero':'/img/stock/green-colonial-exterior-painting-cumberland-ri.webp','hero_pos':'50% 40%',
  'menu_img':'/img/exterior-siding-spray-painting-cumberland-ri.webp',
  'lead':'Siding, trim, doors and shutters painted to handle New England winters — with the prep work most painters skip.',
  'intro':[
    '<strong>New England weather is hard on paint.</strong> Freezing winters, wet springs and summer sun make siding peel, trim crack and doors fade faster than in most of the country.',
    'That is why every exterior job we take on starts with prep: we power wash the house, scrape and sand every loose spot, caulk the gaps and prime bare wood before a single finish coat goes on. Paint only lasts as long as the surface underneath it.',
    'We paint clapboard and shingle siding, vinyl and aluminum, trim, soffits and fascia, porches, railings, doors, shutters and garage doors — on single-family homes, multifamily rentals and commercial buildings around Woonsocket, RI and the Blackstone Valley.'
  ],
  'included':[
    ('Power washing','Dirt, chalk and mildew washed off so the new paint bonds to the surface, not to the grime.'),
    ('Scraping & sanding','Loose and peeling paint removed, edges feathered smooth so they don\'t show through.'),
    ('Caulking & glazing','Gaps around windows, doors and trim sealed against water and drafts.'),
    ('Spot priming','Bare wood and repairs primed with an exterior primer that blocks stains and tannins.'),
    ('Two finish coats','Premium exterior paint (Benjamin Moore or Sherwin-Williams) brushed, rolled or sprayed.'),
    ('Trim, doors & shutters','Crisp lines on trim, front doors, shutters, railings and garage doors.'),
    ('Property protection','Plants, walkways, windows and fixtures covered and masked before we spray.'),
    ('Clean-up & walkthrough','Paint chips picked up every day and a final walkthrough with you before we leave.'),
  ],
  'steps':[
    ('Text us photos','Send a photo of each side of the house to (774) 586-9824. Tell us your town.'),
    ('Same-day quote','We reply the same day. Bigger homes get a free visit to measure and check the siding.'),
    ('We prep & paint','We pick dry days above 50°F, prep, paint and walk the house with you at the end.'),
  ],
  'faq':[
    ('When is the best time to paint a house exterior in Rhode Island?','From May to October. Paint needs dry days above about 50°F, so we schedule around the weather and keep you posted if rain moves the start date.'),
    ('How long does an exterior paint job last?','With proper prep and two coats of quality paint, siding usually looks good for 7–10 years. Trim and doors facing the sun may need a touch-up sooner.'),
    ('Can you paint vinyl or aluminum siding?','Yes. We clean it, use a vinyl-safe paint and help you choose a color that won\'t warp the siding in the sun.'),
    ('Do I need to be home while you paint?','No. We just need access to outdoor water and power. Most customers go to work and get photo updates by text.'),
  ],
  'related':['power-washing','ceilings-and-trim','drywall-repair'],
  'icon':'i-home',
 },
 {
  'slug':'interior-painting','name':'Interior Painting','long':'Interior Painting','short':'Walls, rooms & whole homes',
  'title':'Interior Painting in Woonsocket, RI | NLS Paint',
  'desc':'Interior painting in Woonsocket, RI & nearby towns. Furniture and floors protected, walls patched, two clean coats. Wallpaper removal too. Free quote.',
  'h1':'Interior Painting in <em>Woonsocket, RI</em> &amp; Nearby Towns',
  'kw':'inside',
  'hero':'/img/stock/interior-living-room-painting-lincoln-ri.webp','hero_pos':'50% 50%',
  'menu_img':'/img/stock/interior-living-room-painting-lincoln-ri.webp',
  'lead':'Single rooms, whole homes and rental turnovers — furniture protected, walls repaired and a clean, even finish.',
  'intro':[
    '<strong>A fresh coat changes how a room feels</strong> — but only if the walls underneath are smooth and the lines are sharp.',
    'Before we paint, we move and cover your furniture, protect the floors, fill nail holes and dents, caulk gaps along the trim and prime any stains. Then two coats go on the walls, so the color is even from every angle.',
    'Interior work is Maicow\'s favorite kind of job. Bedrooms, living rooms, kitchens, hallways, stairways and basements — in furnished homes, empty rentals and homes getting ready to sell.'
  ],
  'included':[
    ('Furniture moved & covered','We move what we can, cover the rest in plastic and put everything back.'),
    ('Floors protected','Drop cloths and floor paper down before any can is opened.'),
    ('Patching & sanding','Nail holes, dents and small cracks filled and sanded flush.'),
    ('Caulking','Gaps between walls, baseboards and casings sealed for clean lines.'),
    ('Stain-blocking primer','Water stains, marker and repairs primed so they don\'t bleed through.'),
    ('Two coats on walls','Even color and sheen, cut in by hand along ceilings and trim.'),
    ('Ceilings & trim on request','Add ceilings, baseboards, doors and casings to the same visit.'),
    ('Daily clean-up','Tools packed and rooms usable again at the end of each day.'),
  ],
  'steps':[
    ('Text us photos','A photo of each room plus rough sizes is enough for most quotes.'),
    ('Same-day quote','We reply the same day with a price per room and a start date.'),
    ('We paint','We protect, prep and paint — most bedrooms are done in a single day.'),
  ],
  'faq':[
    ('Can you paint while we\'re living in the house?','Yes. We work room by room, keep the rest of the house usable and clean up at the end of every day.'),
    ('How long does it take to paint a room?','Most bedrooms take one day, including prep and two coats. A whole floor usually takes 2–4 days.'),
    ('Which paint finish should I use?','Usually eggshell for living areas and bedrooms, satin for kitchens and baths, flat for ceilings and semi-gloss for trim. We\'ll suggest the right one for each room.'),
    ('Do you remove wallpaper?','Yes. We strip it, clean off the glue, repair the wall and prime it so the new paint looks smooth. We don\'t install wallpaper.'),
  ],
  'related':['ceilings-and-trim','drywall-repair','epoxy-floors'],
  'icon':'i-roller',
  'wallpaper':True,
 },
 {
  'slug':'ceilings-and-trim','name':'Ceilings & Trim','long':'Ceiling & Trim Painting','short':'Crisp lines, no drips',
  'title':'Ceiling & Trim Painting in Woonsocket, RI | NLS Paint',
  'desc':'Ceiling and trim painting in Woonsocket, RI: baseboards, doors, casings, crown molding, railings and porch steps. Clean lines. Text for a free quote.',
  'h1':'Ceiling &amp; Trim Painting in <em>Woonsocket, RI</em> &amp; Nearby Towns',
  'kw':'details',
  'hero':'/img/porch-steps-white-railings-woonsocket-ri.webp','hero_pos':'50% 40%',
  'menu_img':'/img/porch-steps-trim-painting-woonsocket-ri.webp',
  'lead':'Baseboards, doors, casings, crown molding, railings and ceilings — the details that make a paint job look professional.',
  'intro':[
    '<strong>Trim is where you can tell a pro from a weekend job.</strong> Drips on the baseboards, gaps in the corners and brush marks on doors stand out every time you walk by.',
    'We sand and caulk every joint, use a stain-blocking primer on ceilings and finish trim in a hard, washable semi-gloss. Doors get both sides and the edges. Ceilings get cut in by hand and rolled in one direction so there\'s no flashing.',
    'Inside and out: baseboards, window and door casings, crown molding, stair railings and spindles, porch railings, steps and decks.'
  ],
  'included':[
    ('Ceilings','Flat ceiling paint, stain-blocking primer on water marks, even roller passes.'),
    ('Baseboards & casings','Sanded, caulked and finished in a durable semi-gloss.'),
    ('Doors','Both sides and all edges, brushed or sprayed off the hinges when needed.'),
    ('Crown molding','Clean lines where the wall meets the ceiling.'),
    ('Stairs & railings','Spindles, handrails and risers painted, treads stained or painted.'),
    ('Porch steps & railings','Exterior trim, porch floors and steps with porch & floor paint.'),
    ('Caulking every joint','Gaps and nail holes filled so the trim reads as one clean piece.'),
    ('Careful masking','Floors, walls and hardware masked so the lines stay sharp.'),
  ],
  'steps':[
    ('Text us photos','Show us the rooms, doors or porch — and any water stains on the ceiling.'),
    ('Same-day quote','We quote per room, per door or for the whole house, the same day.'),
    ('We paint','Sand, caulk, prime and finish — and leave with a clean floor.'),
  ],
  'faq':[
    ('Can you cover water stains on the ceiling?','Yes, once the leak is fixed. We seal the stain with a stain-blocking primer first so it doesn\'t come back through the new paint.'),
    ('Do you paint popcorn ceilings?','Yes, we can roll or spray them. Removing popcorn texture is a separate job that we quote on its own.'),
    ('Brush or spray for trim and doors?','Both. We brush most trim in occupied homes and spray doors and trim in empty homes or new construction for the smoothest finish.'),
    ('Can you paint porch steps and railings?','Yes. We scrape, prime and use a porch & floor paint made for foot traffic and weather.'),
  ],
  'related':['interior-painting','exterior-painting','drywall-repair'],
  'icon':'i-brush',
 },
 {
  'slug':'epoxy-floors','name':'Epoxy Floors','long':'Epoxy Floor Coating','short':'Garages, basements & shops',
  'title':'Epoxy Garage Floor Coating in Woonsocket, RI | NLS Paint',
  'desc':'Epoxy floor coating for garages, basements and shops in Woonsocket, RI & nearby towns. Grinding, crack repair, color flakes, clear topcoat. Free quote.',
  'h1':'Epoxy Floor Coating in <em>Woonsocket, RI</em> &amp; Nearby Towns',
  'kw':'tough',
  'hero':'/img/commercial-garage-interior-painting-bellingham-ma.webp','hero_pos':'50% 70%',
  'menu_img':'/img/commercial-garage-interior-painting-bellingham-ma.webp',
  'lead':'A tough, easy-to-clean floor for garages, basements and workshops — prepped right so it doesn\'t peel.',
  'intro':[
    '<strong>Epoxy fails when the concrete isn\'t prepped.</strong> That\'s why most peeling garage floors you see were rolled straight onto a dusty slab.',
    'We test the slab for moisture, repair cracks and pits, then grind or etch the concrete so the coating can grab it. After a primer and a thick base coat, we add color flakes if you want them and seal everything with a clear topcoat.',
    'The result is a floor that shrugs off oil, salt and road grime and cleans up with a mop — in residential garages, basements, workshops and small commercial spaces.'
  ],
  'included':[
    ('Moisture test','We check the slab first so the coating doesn\'t lift from below.'),
    ('Crack & pit repair','Cracks, chips and holes filled and ground flush.'),
    ('Grinding or etching','The concrete is opened up so the epoxy can bond.'),
    ('Primer coat','A penetrating primer for maximum grip.'),
    ('Epoxy base coat','A thick, even base coat in your choice of color.'),
    ('Color flakes (optional)','Decorative flakes that hide dirt and add texture.'),
    ('Clear topcoat','A UV-stable topcoat for shine and chemical resistance.'),
    ('Anti-slip additive','Added to the topcoat on request for wet areas.'),
  ],
  'steps':[
    ('Text us photos','Send photos of the floor and its size in square feet (or the garage size).'),
    ('Same-day quote','We reply the same day; most floors get a quick visit to check the slab.'),
    ('We coat the floor','Prep and coating usually take 2–3 days, then the floor cures.'),
  ],
  'faq':[
    ('How soon can I park on my new epoxy floor?','You can walk on it after about 24 hours. Wait about 72 hours before parking, and up to a week for a full cure in cold weather.'),
    ('Will the epoxy peel from hot tires?','Not when the concrete is ground and primed properly — that prep is what stops hot-tire peeling.'),
    ('Can you do basement floors?','Yes, as long as the moisture test passes. If the slab is damp we\'ll tell you before we start.'),
    ('Is an epoxy floor slippery?','It can be when wet. Color flakes and an anti-slip additive in the topcoat add grip.'),
  ],
  'related':['power-washing','interior-painting','ceilings-and-trim'],
  'icon':'i-layers',
 },
 {
  'slug':'power-washing','name':'Power Washing','long':'Power Washing','short':'Siding, decks & driveways',
  'title':'Power Washing in Woonsocket, RI | Siding & Decks | NLS Paint',
  'desc':'Power washing in Woonsocket, RI & nearby towns: soft wash for siding, decks, porches, fences and driveways. Mildew removed. Text photos for a quote.',
  'h1':'Power Washing in <em>Woonsocket, RI</em> &amp; Nearby Towns',
  'kw':'clean',
  'hero':'/img/power-washing-siding-prep-lincoln-ri.webp','hero_pos':'50% 55%',
  'menu_img':'/img/power-washing-siding-prep-lincoln-ri.webp',
  'lead':'Soft washing for siding, decks, porches, fences and driveways — on its own or as the first step before we paint.',
  'intro':[
    '<strong>Green streaks and black spots on the siding aren\'t dirt — they\'re mildew and algae.</strong> Rinsing them with a hose won\'t remove them, and blasting them with high pressure can damage the siding.',
    'We use a soft wash: a cleaning solution that kills mildew at the root, followed by a low-pressure rinse that\'s safe for vinyl, wood, painted siding and trim. Driveways and walkways get more pressure where it\'s safe.',
    'Power washing is included in every exterior painting job, and it\'s also a great once-a-year service to keep a home looking freshly painted for longer.'
  ],
  'included':[
    ('Siding soft wash','Vinyl, wood, aluminum and painted siding cleaned at safe pressure.'),
    ('Mildew & algae treatment','Green and black growth treated, not just rinsed.'),
    ('Decks & porches','Wood and composite decks, porch floors and steps.'),
    ('Fences','Wood and vinyl fences cleaned on both sides.'),
    ('Driveways & walkways','Concrete and pavers cleaned of dirt and stains.'),
    ('Gutters (outside)','The outside face of the gutters brightened.'),
    ('Plant protection','Plants rinsed before and after so the solution doesn\'t harm them.'),
    ('Pre-paint prep','The first step of every exterior repaint.'),
  ],
  'steps':[
    ('Text us photos','Show us each side of the house, the deck or the driveway.'),
    ('Same-day quote','We reply the same day with a price — usually without a visit.'),
    ('We wash','Most homes are done in a single morning. We just need an outdoor faucet.'),
  ],
  'faq':[
    ('Will power washing damage my vinyl siding?','Not the way we do it. We soft wash siding with low pressure and a cleaning solution, so nothing is forced behind the panels.'),
    ('Do you power wash before painting?','Always. Every exterior painting job starts with a full wash so the new paint bonds properly.'),
    ('How often should I wash my house?','Once a year or every two years keeps mildew under control, especially on the north side of the house.'),
    ('Do you need my water?','Yes, we connect to an outdoor faucet. Water use is about the same as watering the lawn.'),
  ],
  'related':['exterior-painting','ceilings-and-trim','epoxy-floors'],
  'icon':'i-drop',
 },
 {
  'slug':'drywall-repair','name':'Drywall Repair & Caulking','long':'Drywall Repair & Caulking','short':'Patch, sand, seal, paint',
  'title':'Drywall Repair & Caulking in Woonsocket, RI | NLS Paint',
  'desc':'Drywall repair and caulking in Woonsocket, RI: holes, cracks, nail pops, water damage and gaps sealed, then painted to match. Text photos for a quote.',
  'h1':'Drywall Repair &amp; Caulking in <em>Woonsocket, RI</em> &amp; Nearby Towns',
  'kw':'repair',
  'hero':'/img/stock/drywall-patching-spackle-north-smithfield-ri.webp','hero_pos':'50% 40%',
  'menu_img':'/img/stock/drywall-repair-north-smithfield-ri.webp',
  'lead':'Holes, cracks, nail pops and gaps fixed and painted to match — so the repair disappears.',
  'intro':[
    '<strong>A great paint job starts with a smooth wall.</strong> Holes, dents and cracks show right through new paint, especially on walls that catch sunlight.',
    'We cut out and patch damaged drywall, tape and mud the seams, sand everything flush and match the texture. Then we prime the repair and paint the whole wall, so you don\'t see a patch in a different sheen.',
    'Caulking is the other half of the job: gaps around trim, baseboards, tubs and windows are sealed so the lines look clean and drafts and water stay out. Ideal for rental turnovers, homes going on the market and anyone tired of looking at that doorknob hole.'
  ],
  'included':[
    ('Holes & doorknob damage','Small and large holes patched with mesh or new drywall.'),
    ('Nail pops & dents','Popped screws reset and dents filled flush.'),
    ('Cracks & seams','Cracked seams and corners re-taped and mudded.'),
    ('Water damage','Damaged drywall cut out and replaced after the leak is fixed.'),
    ('Texture matching','Repairs blended to match the wall around them.'),
    ('Interior caulking','Trim, baseboards, crown, tubs, sinks and windows sealed.'),
    ('Exterior caulking','Gaps in siding, trim and windows sealed against water.'),
    ('Prime & paint to match','The whole wall painted so the repair disappears.'),
  ],
  'steps':[
    ('Text us photos','A close-up of each repair plus a photo of the whole wall.'),
    ('Same-day quote','We reply the same day — small repairs can often be added to a paint job.'),
    ('We fix & paint','Patch, dry, sand, prime and paint — usually in 1–2 visits.'),
  ],
  'faq':[
    ('Can you match my existing wall color?','Yes. Bring us the leftover can or we\'ll color-match a chip from the wall. We paint the whole wall so the sheen matches too.'),
    ('Do you take small repair jobs?','Yes. Many customers bundle a few repairs with a room or two of painting, which is the best value.'),
    ('Can you fix cracks in the ceiling?','Yes. We re-tape and mud ceiling cracks and repaint the ceiling so the repair blends in.'),
    ('Do you do rental turnovers?','Yes — patching, caulking and repainting between tenants is one of our most common jobs for landlords.'),
  ],
  'related':['interior-painting','ceilings-and-trim','exterior-painting'],
  'icon':'i-hammer',
 },
]
SVC = {s['slug']: s for s in SERVICES}

# ---------------------------------------------------------------- projetos
# photos: (arquivo, legenda curta). A primeira é a capa.
PROJECTS = [
 {
  'slug':'commercial-repaint-metal-building-woonsocket-ri','title':'Commercial Metal Building Repaint in Woonsocket, RI','card':'Metal building repaint',
  'service':'exterior-painting','also':['power-washing'],'city':'Woonsocket','state':'RI','date':'2026-09','type':'Commercial','duration':'4 days',
  'photos':[('/img/metal-building-half-painted-woonsocket-ri.webp','Halfway there — new gray next to the old faded blue'),('/img/metal-building-before-blue-woonsocket-ri.webp','Before: faded, chalky blue metal siding'),('/img/metal-building-repaint-in-progress-woonsocket-ri.webp','Spraying the second coat, ground covered'),('/img/metal-building-after-gray-woonsocket-ri.webp','After: clean gray finish along the whole wall'),('/img/commercial-metal-building-painting-woonsocket-ri.webp','Finished side wall from the parking lot'),('/img/metal-building-after-detail-woonsocket-ri.webp','Detail: even coverage on the ribbed panels')],
  'pair':('/img/commercial-exterior-repaint-woonsocket-ri-wide.webp','/img/metal-building-after-gray-woonsocket-ri.webp'),
  'summary':'A faded, chalky blue metal building got a full exterior repaint in a clean modern gray. We power washed the panels, primed the rusty spots and sprayed two coats for an even finish on the ribbed siding.',
  'body':['Metal siding loses its color to the sun and gets a chalky film that new paint won\'t stick to. We started with a full power wash to remove the chalk, then spot-primed every rusty screw and scratch with a rust-inhibiting primer.','The panels were sprayed with two coats of a direct-to-metal acrylic, with drop cloths along the base of the wall and the HVAC units covered. The business stayed open the whole time.'],
  'colors':[('Gray, satin','#8A8F92'),('Rust-inhibiting primer','#B44A2E')],
  'note':'FOTOS REAIS do Maicow (WhatsApp). Texto, data e duração são suposições: confirmar.',
 },
 {
  'slug':'exterior-siding-repaint-cumberland-ri','title':'Exterior Siding Repaint in Cumberland, RI','card':'Dark siding repaint',
  'service':'exterior-painting','also':['power-washing'],'city':'Cumberland','state':'RI','date':'2026-08','type':'Single-family','duration':'5 days',
  'photos':[('/img/exterior-siding-spray-painting-cumberland-ri.webp','Spray-applied finish on the dark siding'),('/img/exterior-siding-spray-detail-cumberland-ri.webp','Detail: even coat down to the foundation line'),('/img/siding-prep-scraping-cumberland-ri.webp','Prep: scraped and patched siding before primer'),('/img/siding-power-washing-prep-cumberland-ri.webp','Power washer set up for the pre-paint wash')],
  'summary':'Weathered, peeling siding on a ranch home was power washed, scraped, patched and primed, then sprayed in a deep charcoal for a modern look that hides dirt and holds up to winter.',
  'body':['The old paint was failing in sheets on the sunny side of the house. We washed the whole house, scraped every loose area, filled the cracks and primed the bare wood.','Two coats of exterior acrylic were sprayed and back-brushed for an even finish, with the windows, walkway and plants fully covered.'],
  'colors':[('Charcoal, low-luster','#2F3438'),('White trim','#F2F0EA')],
  'note':'FOTOS REAIS (WhatsApp); cidade e textos ilustrativos.',
 },
 {
  'slug':'porch-steps-railings-woonsocket-ri','title':'Porch Steps & Railings Painted in Woonsocket, RI','card':'Porch steps & railings',
  'service':'ceilings-and-trim','also':['exterior-painting'],'city':'Woonsocket','state':'RI','date':'2026-07','type':'Single-family','duration':'2 days',
  'photos':[('/img/porch-steps-white-railings-woonsocket-ri.webp','Finished front steps and white railings'),('/img/porch-steps-trim-painting-woonsocket-ri.webp','From the walkway: crisp white trim, deep red treads'),('/img/porch-stair-treads-close-up-woonsocket-ri.webp','Close-up of the new porch & floor paint'),('/img/porch-stairs-painted-treads-woonsocket-ri.webp','Treads and risers, sharp lines between colors')],
  'summary':'Worn front steps and railings were scraped, primed and painted in a two-tone finish — bright white railings and risers with deep red porch-paint treads — for a sharp first impression.',
  'body':['Foot traffic and snow shovels had worn the old paint down to bare wood on the treads. We scraped and sanded everything, primed the bare spots and used a porch & floor enamel made for traffic and weather.','The railings and risers got two coats of exterior white, with every line between the two colors cut in by hand.'],
  'colors':[('Railings & risers, white','#F4F3EE'),('Treads, deep red porch paint','#6E2422')],
  'note':'FOTOS REAIS (WhatsApp + Instagram).',
 },
 {
  'slug':'wallpaper-removal-interior-repaint-cumberland-ri','title':'Wallpaper Removal & Interior Repaint in Cumberland, RI','card':'Wallpaper removal & repaint',
  'service':'interior-painting','also':['drywall-repair','ceilings-and-trim'],'city':'Cumberland','state':'RI','date':'2026-06','type':'Single-family','duration':'3 days',
  'photos':[('/img/stock/living-room-before-after-cumberland-ri.webp','Living room after: bright walls, fresh trim'),('/img/stock/bedroom-wallpaper-removal-cumberland-ri.webp','Bedroom where the old wallpaper came down'),('/img/stock/interior-painting-prep-masking-lincoln-ri.webp','Masking and floor protection before painting'),('/img/stock/drywall-sanding-before-painting-north-smithfield-ri.webp','Skim-coating the walls after the paper came off')],
  'ba':'/img/stock/living-room-before-after-cumberland-ri.webp',
  'summary':'Dated wallpaper in a living room and bedroom was stripped, the walls were repaired and skim-coated, and both rooms were painted in a soft neutral with fresh white trim.',
  'body':['Two layers of old wallpaper came off with steam and scoring. We washed off all the glue residue, skim-coated the torn spots and sealed the walls with a primer made for walls that had wallpaper.','Then two coats of eggshell on the walls, flat white on the ceilings and semi-gloss on the trim. The furniture was moved and covered the whole time.'],
  'colors':[('Walls, soft greige','#CFC8BC'),('Trim, white semi-gloss','#F5F4EF')],
  'note':'FOTOS DE BANCO (ilustrativas). O antes/depois usa a mesma foto com filtro, como na home.',
 },
 {
  'slug':'living-room-hallway-repaint-lincoln-ri','title':'Living Room & Hallway Repaint in Lincoln, RI','card':'Living room & hallway',
  'service':'interior-painting','also':[],'city':'Lincoln','state':'RI','date':'2026-05','type':'Single-family','duration':'2 days',
  'photos':[('/img/stock/living-room-refresh-lincoln-ri.webp','Living room in warm neutrals'),('/img/stock/interior-living-room-painting-lincoln-ri.webp','Bright walls behind the sofa'),('/img/stock/interior-painting-prep-masking-lincoln-ri.webp','Prep: floors covered and trim masked'),('/img/stock/bedroom-interior-painting-woonsocket-ri.webp','Bedroom repainted on the same visit')],
  'summary':'A living room, hallway and one bedroom were repainted in warm neutrals with bright white trim and ceilings, finished in two days with the furniture protected.',
  'body':['The walls had years of scuffs and a few old anchors. We patched and sanded every hole, caulked the baseboards and primed the repairs before two coats of paint.','Ceilings were rolled in flat white and the trim got a fresh semi-gloss so the new colors pop.'],
  'colors':[('Walls, warm beige','#D9CFC0'),('Ceilings, flat white','#F7F6F2')],
  'note':'FOTOS DE BANCO (ilustrativas).',
 },
 {
  'slug':'power-washing-siding-deck-lincoln-ri','title':'Siding Power Washing in Lincoln, RI','card':'Siding soft wash',
  'service':'power-washing','also':[],'city':'Lincoln','state':'RI','date':'2026-05','type':'Single-family','duration':'1 day',
  'photos':[('/img/power-washing-siding-prep-lincoln-ri.webp','Soft wash set-up along the side of the house'),('/img/power-washing-siding-detail-lincoln-ri.webp','Clean siding and trim after the rinse'),('/img/stock/painter-on-ladder-exterior-wall-lincoln-ri.webp','Rinsing the upper wall from the ladder'),('/img/stock/paint-roller-exterior-wall-woonsocket-ri.webp','Ready for paint on the next visit')],
  'summary':'Mildew-stained siding was soft washed and rinsed at low pressure, getting the house ready for a fresh coat of paint later in the season.',
  'body':['Green mildew had taken over the shady side of the house. We applied a soft-wash solution, let it work and rinsed at low pressure so nothing was forced behind the siding.','The plants were rinsed before and after, and the whole job was done in one morning.'],
  'note':'Fotos reais (casa amarela) + banco. Mesma casa do projeto de Cumberland: trocar quando houver fotos reais.',
 },
 {
  'slug':'epoxy-floor-garage-shop-bellingham-ma','title':'Garage Shop Floor & Walls in Bellingham, MA','card':'Shop floor & walls',
  'service':'epoxy-floors','also':['interior-painting'],'city':'Bellingham','state':'MA','date':'2026-09','type':'Commercial','duration':'3 days',
  'photos':[('/img/commercial-garage-interior-painting-bellingham-ma.webp','Shop interior prepped for the floor coating'),('/img/garage-shop-floor-detail-bellingham-ma.webp','Floor ground and cleaned before the primer'),('/img/garage-shop-ceiling-walls-bellingham-ma.webp','Ceiling and walls masked for spraying'),('/img/stock/concrete-floor-prep-epoxy-bellingham-ma.webp','Base coat going down section by section')],
  'summary':'An auto shop\'s concrete floor was ground, repaired and coated with epoxy, and the walls and ceiling were sprayed white to brighten the work bays.',
  'body':['Oil stains and cracks covered the slab. We degreased, ground the concrete, filled the cracks and laid a primer before a thick gray base coat.','The ceiling and upper walls were sprayed in bright white with the lifts and equipment wrapped in plastic.'],
  'colors':[('Floor, epoxy gray','#7B8085'),('Walls & ceiling, white','#F3F2EE')],
  'note':'1 FOTO REAL (garagem) + recortes e banco. Confirmar se houve epóxi nesse serviço.',
 },
 {
  'slug':'kitchen-walls-cabinets-bellingham-ma','title':'Kitchen Walls & Cabinets in Bellingham, MA','card':'Kitchen walls & cabinets',
  'service':'interior-painting','also':['ceilings-and-trim'],'city':'Bellingham','state':'MA','date':'2026-04','type':'Single-family','duration':'3 days',
  'photos':[('/img/stock/kitchen-cabinet-painting-bellingham-ma.webp','Crisp white kitchen walls and cabinets'),('/img/stock/kitchen-walls-cabinets-painting-bellingham-ma.webp','Shaker cabinets after two coats'),('/img/stock/open-kitchen-interior-painting-bellingham-ma.webp','Open kitchen and dining area'),('/img/stock/cabinet-trim-masking-prep-bellingham-ma.webp','Counters and floors masked before priming')],
  'summary':'A dark, dated kitchen got crisp white walls, freshly painted cabinets and new ceiling paint — making the whole space feel bigger and brighter.',
  'body':['Cabinet doors were removed, degreased, sanded and primed with a bonding primer, then finished with a hard cabinet enamel.','The walls and ceiling were painted while the doors cured, and everything was rehung and adjusted on the last day.'],
  'colors':[('Cabinets, white enamel','#F4F3EF'),('Walls, light gray','#DCDDDA')],
  'note':'FOTOS DE BANCO (ilustrativas). Armários: o Maicow terceiriza quando necessário.',
 },
 {
  'slug':'drywall-repair-rental-turnover-north-smithfield-ri','title':'Rental Turnover: Drywall Repair in North Smithfield, RI','card':'Rental turnover repairs',
  'service':'drywall-repair','also':['interior-painting'],'city':'North Smithfield','state':'RI','date':'2026-03','type':'Multifamily','duration':'2 days',
  'photos':[('/img/stock/drywall-patching-spackle-north-smithfield-ri.webp','Patching holes between tenants'),('/img/stock/drywall-sanding-before-painting-north-smithfield-ri.webp','Sanding the repairs flush'),('/img/stock/drywall-putty-knife-repair-smithfield-ri.webp','Second coat of compound on a seam'),('/img/stock/drywall-repair-north-smithfield-ri.webp','Opened wall before new drywall went in')],
  'summary':'Between tenants, a two-bedroom apartment got every hole, dent and crack repaired, the trim caulked and the walls repainted so the landlord could list it the same week.',
  'body':['Anchors, doorknob holes and a water-damaged section in the bathroom wall were repaired. We replaced the damaged drywall, taped and mudded the seams and matched the texture.','Then all the walls were primed where repaired and painted in the landlord\'s standard white.'],
  'note':'FOTOS DE BANCO (ilustrativas).',
 },
 {
  'slug':'exterior-repaint-colonial-cumberland-ri','title':'Colonial Exterior Repaint in Cumberland, RI','card':'Colonial exterior repaint',
  'service':'exterior-painting','also':['ceilings-and-trim'],'city':'Cumberland','state':'RI','date':'2026-07','type':'Single-family','duration':'6 days',
  'photos':[('/img/stock/green-colonial-exterior-painting-cumberland-ri.webp','Sage green clapboard with white trim'),('/img/stock/cape-style-home-exterior-cumberland-ri.webp','Porch and front trim refreshed'),('/img/stock/painter-on-ladder-exterior-wall-lincoln-ri.webp','Cutting in the upper trim from the ladder'),('/img/stock/paint-roller-exterior-wall-woonsocket-ri.webp','Rolling the finish coat')],
  'summary':'A classic New England colonial was scraped, primed and repainted in sage green with bright white trim, bringing back its original character.',
  'body':['Old clapboard siding had peeling paint on the south and west sides. We scraped, sanded and spot-primed every bare board and replaced the failed caulk around the windows.','Two coats of sage green went on the siding and two coats of white on the trim, porch and window casings.'],
  'colors':[('Siding, sage green','#7D8B6A'),('Trim, white','#F5F4EF')],
  'note':'FOTOS DE BANCO (ilustrativas).',
 },
 {
  'slug':'craftsman-exterior-painting-smithfield-ri','title':'Craftsman Exterior Painting in Smithfield, RI','card':'Craftsman exterior',
  'service':'exterior-painting','also':[],'city':'Smithfield','state':'RI','date':'2026-06','type':'Single-family','duration':'5 days',
  'photos':[('/img/stock/craftsman-exterior-painting-smithfield-ri.webp','Deep-tone siding with contrasting trim'),('/img/stock/paint-roller-exterior-wall-woonsocket-ri.webp','Rolling the base coat'),('/img/stock/painter-on-ladder-exterior-wall-lincoln-ri.webp','Second coat on the upper walls'),('/img/stock/white-colonial-house-exterior-painting-woonsocket-ri.webp','Neighbor\'s house we painted the year before')],
  'summary':'A craftsman home got deep-tone siding with contrasting trim, ready for New England winters.',
  'body':['We washed, scraped and primed the siding, then applied two coats of a deep-base exterior paint with a matching trim color picked from the stone foundation.'],
  'note':'FOTOS DE BANCO (ilustrativas).',
 },
 {
  'slug':'farmhouse-exterior-painting-blackstone-ma','title':'Farmhouse Exterior Painting in Blackstone, MA','card':'Farmhouse exterior',
  'service':'exterior-painting','also':['power-washing'],'city':'Blackstone','state':'MA','date':'2026-05','type':'Single-family','duration':'6 days',
  'photos':[('/img/stock/white-colonial-house-exterior-painting-woonsocket-ri.webp','White farmhouse with the wraparound porch'),('/img/stock/new-england-saltbox-exterior-blackstone-ma.webp','Barn and saltbox on the same property'),('/img/stock/painter-on-ladder-exterior-wall-lincoln-ri.webp','Upper walls from the ladder'),('/img/stock/paint-roller-exterior-wall-woonsocket-ri.webp','Rolling the finish coat')],
  'summary':'A white farmhouse with a wraparound porch was washed, scraped and repainted, including the porch ceiling, railings and the barn next to it.',
  'body':['The porch ceiling got a classic light blue, and the railings and spindles were hand-brushed in semi-gloss white.'],
  'colors':[('Siding, white','#F4F3EE'),('Porch ceiling, haint blue','#BFD8D9')],
  'note':'FOTOS DE BANCO (ilustrativas).',
 },
]
PROJ = {p['slug']: p for p in PROJECTS}

# ---------------------------------------------------------------- páginas de cidade (por gatilho)
CITY_PAGES = {
 'Cumberland': {
  'slug':'cumberland-ri','state':'RI','hero':'/img/exterior-siding-spray-painting-cumberland-ri.webp',
  'local':[
    'Cumberland is about ten minutes from our base in Woonsocket — straight down Mendon Road — so we can usually stop by for a free estimate the same week.',
    'We paint a lot of the town\'s classic capes, colonials and raised ranches, from Cumberland Hill and Arnold Mills to Diamond Hill, plus the older mill-village multifamilies around Valley Falls and Lonsdale that landlords need turned over fast between tenants.',
    'Exteriors here take a beating from the wind off the reservoirs and the Blackstone River, so we never skip the wash, scrape and prime before the finish coats.'
  ],
  'facts':[('From Woonsocket','~10 min'),('Neighborhoods','Cumberland Hill · Valley Falls · Arnold Mills · Diamond Hill'),('Common homes','Capes, colonials, raised ranches'),('Estimate visit','Same week')],
  'near':['Woonsocket','Lincoln','Blackstone','Bellingham','Wrentham'],
  'faq':[('Do you charge extra to come to Cumberland?','No. Cumberland is right next door to Woonsocket, and estimates are always free.'),('How soon can you start a job in Cumberland?','Small jobs often start within a week. Exteriors are scheduled from May to October.')],
 },
 'Lincoln': {
  'slug':'lincoln-ri','state':'RI','hero':'/img/stock/living-room-refresh-lincoln-ri.webp',
  'local':[
    'Lincoln is about fifteen minutes from Woonsocket down Route 146, and we\'re in town most weeks.',
    'We paint everything from the colonials and split-levels around Lime Rock and Lincoln Woods to the older homes and mill housing in Manville, Albion, Saylesville and Fairlawn — interiors in winter, exteriors and power washing from spring to fall.',
    'Many Lincoln homes sit under big trees, so mildew on the shady side of the siding is common. A soft wash before painting takes care of it.'
  ],
  'facts':[('From Woonsocket','~15 min'),('Neighborhoods','Lime Rock · Manville · Albion · Fairlawn'),('Common homes','Colonials, split-levels, mill houses'),('Estimate visit','Same week')],
  'near':['Woonsocket','Cumberland','Smithfield','North Smithfield'],
  'faq':[('Do you charge extra to come to Lincoln?','No. Pricing is the same in every town we serve, and estimates are free.'),('Do you paint in the winter in Lincoln?','Yes — winter is our interior season. Exteriors run from May to October.')],
 },
}
# serviço × cidade (por gatilho): só exterior, camada 1
SERVICE_CITY = [
 {'city':'Cumberland','service':'exterior-painting','hero':'/img/stock/cape-style-home-exterior-cumberland-ri.webp',
  'local':['Most exteriors we paint in Cumberland are wood clapboard colonials and capes on Cumberland Hill and around Arnold Mills, plus vinyl-sided raised ranches near Diamond Hill. The wood homes need the most prep: years of sun on the south side leave peeling paint that has to be scraped and primed before any color goes on.','Because we\'re only ten minutes away in Woonsocket, we can move fast when a dry week opens up in the forecast — which matters in a short New England painting season.']},
]
