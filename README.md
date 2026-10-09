# Prévia de site — Monica Almeida | Arquitetura que Cuida

Prévia de prospecção da RevoluTech (1 página, noindex). Fonte da verdade: `plano-do-site.md`.

## Rodar

```bash
npm install
npm run dev        # http://localhost:5173
npm run build      # tsc + vite build -> dist/
npm run preview    # http://localhost:4173 (serve dist/)
```

## Assets (só os reais da Monica, ver `assets-manifest.json`)

```bash
npm run assets:baixar      # baixa os originais para assets-originais/ (fora do git)
npm run assets:processar   # recorta faixas, gera WebP/AVIF 480/960/1600 em public/img/
npm run assets:logo        # recorta o logotipo real (creme/verde) + favicons em public/logo/
npm run assets:og          # gera public/og/home.jpg (1200x630)
```

As URLs do manifest expiram em 13/10/2026; depois disso, recoletar pelos permalinks dos posts.

## QA (Python 3.12 + playwright + pillow)

```bash
npm run build && npm run preview
python -X utf8 .claude/skills/sites-revolutech/scripts/qa_site.py http://localhost:4173 --saida qa/previa
python -X utf8 qa/testes-manuais.py http://localhost:4173
```

Alertas esperados por ser prévia: noindex, `Disallow: /`, sem sitemap, sem /obrigado, sem política de privacidade. Detalhes em `plano-do-site.md` §7.

## Publicar (prévia, sem domínio)

Repositório: `thiagoandradesk/monicaalmeidaarq-previa` (remote `origin`). Projeto Vercel `monicaalmeidaarq-previa`, ligado ao repositório: todo push na `main` gera deploy em https://monicaalmeidaarq-previa.vercel.app/.

```bash
git push origin main
python -X utf8 .claude/skills/sites-revolutech/scripts/qa_site.py https://monicaalmeidaarq-previa.vercel.app --saida qa/previa-vercel
```

O upload pelo navegador do GitHub não serve (limite de 100 arquivos por vez; `public/img` tem 115). Canonical, `og:url` e `og:image` seguem `VERCEL_PROJECT_PRODUCTION_URL` no build (ver `vite.config.ts`).
