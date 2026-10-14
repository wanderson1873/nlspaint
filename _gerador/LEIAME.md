# Site completo nlspaint.com (protótipo SEO local)

Junta a home do `home-prototipo`, as páginas internas e as decisões de `nlspaint/docs/` em um site só, **gerado inteiro** por um script (inclusive a home). Não edite os HTML gerados: edite o conteúdo/templates e rode de novo.

```
python _gerador/build.py
```

Para ver: `python -m http.server 8767 --directory site-completo` e abra http://localhost:8767 (os links são absolutos).

| Arquivo | O que tem |
|---|---|
| `content.py` | NAP da empresa (`BUSINESS`), cidades (camadas 1 e 2), 6 serviços, 12 projetos, páginas de Cumberland/Lincoln e serviço × cidade |
| `content_local.py` | Páginas novas de cidade (North Smithfield, Smithfield, Blackstone, Bellingham) e conteúdo da home (bloco de Woonsocket, FAQ, galeria) |
| `build.py` | Templates, JSON-LD, sitemap.xml, robots.txt e o relatório de SEO. No topo: `GA_ID` e `FORM_ACTION` |
| `sprites.svg` | Ícones |
| `seo-report.md` | Gerado a cada build: title/description/H1/palavras por página + problemas |
| `../assets/site.css` | CSS de todas as páginas (editar direto) |
| `../assets/site.js` | Menu, pincelada, antes/depois, lightbox, formulário, mapa estático, eventos GA4 |
| `../assets/home.js` | Só da home: galeria presa e gota que vira mapa |
| `../nginx.conf`, `../Dockerfile` | Deploy no EasyPanel (substitui o "em construção" de `nlspaint/`) |

**33 páginas:** home · `/services/` + 6 serviços · `/projects/` + 12 projetos · `/service-areas/` + 6 cidades + 1 serviço × cidade · about · contact · privacy · 404.

O build **falha** se um projeto tiver menos de 4 fotos, se uma foto não existir, ou se uma página de cidade não tiver projeto na cidade (regra do gatilho).

O botão amarelo **📝 Notas do protótipo** mostra em cada bloco o que ele é e o que ainda é provisório. Veja `SEO-LOCAL.md` para o que foi feito e o que falta fora do site.
