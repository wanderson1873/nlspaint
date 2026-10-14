# NLS Paint — branch `dev` (homologação)

Site completo (protótipo SEO local) publicado em **https://dev.nlspaint.com**, bloqueado para buscadores (noindex).
A branch `main` continua com a página "em construção" de nlspaint.com.

- O site é gerado: edite `_gerador/content.py`, `_gerador/content_local.py` ou `_gerador/build.py` e rode
  `NLS_ENV=dev python _gerador/build.py` (dev) ou `python _gerador/build.py` (produção, nlspaint.com).
- Commit dos HTML gerados + push na `dev` → o EasyPanel rebuilda o serviço de dev.
- Detalhes: `_gerador/LEIAME.md` e `_gerador/SEO-LOCAL.md`.
