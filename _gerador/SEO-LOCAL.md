# SEO local — o que o site já faz e o que falta

## No site (feito)

**Entidade e NAP**
- Um único `HousePainter` (`@id https://nlspaint.com/#business`) em todas as páginas, com nome, telefone, Woonsocket RI 02895 (sem rua), coordenadas, horário, formas de pagamento, `priceRange`, catálogo dos 6 serviços e `founder` → Maicow.
- `areaServed`: as 7 cidades da camada 1 como `City` com `sameAs` da Wikipedia (desambigua "Lincoln, RI" de outros Lincolns) + um `GeoCircle` de 70 mi.
- NAP idêntico em header (menu), footer, contato e schema — puxado de `BUSINESS` no `content.py`. Mudou algo no Google Meu Negócio? Muda só ali.

**Páginas que rankeiam para "serviço + cidade"**
- Home = página de Woonsocket (cidade do GMN), agora com bloco local próprio (bairros, triple-deckers).
- 6 páginas de serviço com "in Woonsocket, RI" no H1/title, schema `Service` + `FAQPage`.
- **6 páginas de cidade** (todas as da camada 1 — cada uma já tem ≥1 projeto, então o gatilho foi batido): texto local único, projetos da cidade, serviços, cidades vizinhas, FAQ próprio, `geo.*` da cidade, `Service` com `areaServed` da cidade.
- 1 página serviço × cidade (Cumberland × exterior), seguindo a regra de só abrir com conteúdo diferente.
- Hub `/services/` novo (o breadcrumb "Services" apontava para `/#services`).

**Técnico**
- `sitemap.xml` com sitemap de imagens (as fotos dos projetos com cidade no nome do arquivo entram no Google Imagens) + `robots.txt`.
- Canonical absoluto, `robots` meta, Open Graph completo com dimensões, Twitter card, favicons.
- `BreadcrumbList` com `@id`, `WebPage` com `dateModified` e imagem principal.
- Todas as imagens com `width`/`height` reais (sem CLS), `alt` serviço + cidade, lazy fora do hero, hero com `preload`.
- Na home, cidades, galeria e lista do formulário agora vêm no HTML (antes eram injetadas por JS).
- FAQ do schema com o mesmo texto visível na página.
- nginx: `www` → raiz, sem barra → com barra (301), 404 real, `_gerador/` bloqueado.
- Relatório automático (`seo-report.md`): title ≤ 60, description ≤ 160, 1 H1, alt, links internos quebrados, JSON-LD válido, duplicados.

## Fora do site (o que mais pesa no map pack)

1. **Google Meu Negócio** — categoria principal *House painter*; secundárias *Painter*, *Pressure washing service*, *Drywall contractor*. Área de atendimento = cidades da camada 1. Endereço oculto. Site → `https://nlspaint.com/`. Depois preencha `BUSINESS['gbp']` e `gbp_review` e rode o build.
2. **Avaliações** — pedir no fim de todo serviço (link curto do GMN por SMS). Só depois de existirem: bloco de reviews na home e `/reviews/`. Nunca `AggregateRating` sem avaliação real.
3. **Citações com o MESMO NAP** — Bing Places, Apple Business Connect, Yelp, Nextdoor, Facebook, Thumbtack, Angi, BBB. Cada perfil criado entra em `BUSINESS['same_as']`.
4. **Fotos** — 1–2 por semana no GMN, com a cidade na legenda. Toda obra nova vira projeto no site (≥4 fotos, EXIF/GPS removido).
5. **Search Console** — enviar `sitemap.xml`; revisar todo mês as buscas "[serviço] [cidade]" para abrir novas páginas serviço × cidade.

## Pendências de conteúdo (marcadas no modo notas)

- Textos locais das cidades novas e de Woonsocket são **rascunho** — o Maicow confirma bairros onde trabalha.
- Projetos com fotos de banco e textos ilustrativos: trocar pelos reais antes de publicar.
- Foto do Maicow, `GA_ID`, `FORM_ACTION`, link do GMN.
- H1 da home ficou "Local House Painters Near You" (decisão anterior). Para SEO local, "House Painters in Woonsocket, RI" é mais forte — vale reconsiderar.
- Franklin, Milford e Holliston entraram na camada 2 (preferência citada na entrevista); conferir distâncias.
