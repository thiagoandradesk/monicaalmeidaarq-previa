# Acessibilidade, motion e performance

Consolidado de: AccessLint (WCAG 2.2), Vercel web-design-guidelines (MIT), Impeccable (Apache-2.0) e Anthropic `frontend-design`/`webapp-testing` (Apache-2.0). Meta: WCAG 2.2 nível AA nos pontos abaixo. Nunca prometer "site 100% acessível".

## Acessibilidade

**Estrutura**
- `lang="pt-BR"`; um `<main>`; `<header>`, `<nav>`, `<footer>`; um H1 e títulos em ordem.
- Link "Pular para o conteúdo" como primeiro item focável.
- Botão é `<button>`, link é `<a href>`. Nada de `<div onclick>`.

**Teclado e foco**
- Tudo que funciona com mouse funciona com Tab/Enter/Espaço/Esc.
- Foco sempre visível: nunca `outline: none` sem substituto (`:focus-visible` com anel de contraste ≥ 3:1).
- Header fixo não esconde o elemento focado (`scroll-margin-top` / `scroll-padding-top`).
- Menu mobile e lightbox: Esc fecha, foco volta para quem abriu, fundo não recebe foco.

**Conteúdo**
- Contraste: texto ≥ 4,5:1; texto grande, ícones, bordas de campo e anel de foco ≥ 3:1. Conferir a paleta e o texto sobre foto.
- `alt` real e específico; imagem decorativa `alt=""`; nunca inventar o que a foto mostra — perguntar ao cliente quando não der para saber.
- Botão só com ícone (WhatsApp, menu, fechar) com `aria-label`.
- Informação nunca só por cor (erro, status, obrigatório).
- Links com texto que faz sentido fora de contexto.

**Toque e zoom**
- Alvos ≥ 24×24 px (WCAG 2.2) — padrão da casa ≥ 44 px.
- Reflow em 320 px sem rolagem lateral; zoom de 200% sem perder conteúdo; nunca `user-scalable=no`.

**Formulários** (ver `formularios-lgpd.md`)
- `<label>` associado; erro em texto com `aria-describedby`; honeypot fora da árvore de acessibilidade.

## Motion

- Um momento autoral por página (ex.: revelação do hero, transição do portfólio). Não aplicar o mesmo fade-up em toda seção.
- Ease-out na entrada; saída mais curta que a entrada; sem bounce/elastic.
- Animar só `transform` e `opacity`; nunca `transition: all`.
- Conteúdo visível sem JavaScript: a animação parte do estado final renderizado e só "aparece" se o JS carregar.
- `@media (prefers-reduced-motion: reduce)`: trocar movimento por fade curto ou nada — alternativa pensada, não só desligar.
- Carrossel e vídeo em loop podem ser pausados.
- GSAP: ScrollTrigger com moderação; nada de "scroll-jacking" que trava a rolagem; testar no celular.

## Performance

**Metas (Core Web Vitals "bom")**: LCP ≤ 2,5 s · INP ≤ 200 ms · CLS ≤ 0,1. Medir com PageSpeed Insights (dados de campo quando houver) depois de publicar.

**Imagens**
- AVIF/WebP via `<picture>`, com `width`/`height` sempre.
- Imagem do hero (LCP): `fetchpriority="high"`, sem lazy, pré-carregada se for background.
- Demais: `loading="lazy" decoding="async"`, com `sizes`/`srcset` para não mandar 2000 px ao celular.
- Remover EXIF/GPS (ex.: `exiftool -all= foto.jpg`, ou exportar sem metadados).

**Fontes**
- Hospedadas no site (woff2), só os pesos usados, `font-display: swap`, `preload` só da principal.

**JavaScript**
- Analytics e pixel com `defer`/`async`, depois do conteúdo e só com consentimento quando usam cookies.
- Em React: carregar sob demanda o que é pesado e não aparece de início (lightbox, mapa, carrossel) com `React.lazy`.
- Não criar componente dentro de componente; não usar `useEffect` para estado derivado; chamadas independentes ao Supabase em paralelo (`Promise.all`).
- Mapa do Google: carregar ao clicar ("Ver no mapa") ou com imagem estática + link, em vez do iframe pesado na carga.

**Números**
- Valores em reais com `Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' })`.
- Nome de marca que não deve ser traduzido pelo navegador: `translate="no"`.
