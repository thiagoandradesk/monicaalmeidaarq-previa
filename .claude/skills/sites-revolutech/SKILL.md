---
name: sites-revolutech
description: Método RevoluTech para construir e alterar sites, landing pages e portfólios — briefing, estrutura, design anti-genérico, desenvolvimento, SEO, LGPD, formulários, /obrigado, /admin, publicação e QA obrigatório em desktop e mobile. Usar em qualquer site da RevoluTech ou de cliente, inclusive ajustes pequenos.
---

# Sites — RevoluTech

Esta skill responde: **"Como a RevoluTech constrói um site?"**

Princípio: **site = vitrine; sistema/captação = motor.** O site precisa apresentar bem e funcionar como canal de contato real. O design nasce do negócio do cliente, nunca de um template.

Preços, pacotes e escopo vêm do `contexto-revolutech.md` do Projeto (Essencial, Institucional, Landing Page). Se o pedido passar do pacote, sinalize orçamento personalizado antes de construir. Em conflito, vale a instrução mais recente de Thiago, e esta skill vale mais que skills genéricas de design (ex.: `frontend-design`).

## Regras inegociáveis

- **Não inventar.** Texto, números, depoimentos, clientes, prêmios, anos de experiência, CRP/CAU, endereço, horário: só com fonte do cliente. Faltou → `[VERIFICAR]` no rascunho, e o QA bloqueia publicar com `[VERIFICAR]` na página.
- **Hierarquia de assets:** 1) asset real do cliente → 2) asset real já existente → 3) asset criado para o projeto → 4) geração por IA (só com OK do Thiago) → 5) procedural/genérico. Nada de banco de imagem aleatório. Registre a procedência de cada imagem no plano do site.
- **LOCKED / escopo soberano.** O que foi aprovado não muda. Ajuste mexe só no alvo pedido: sem cor, fonte, raio, sombra, texto ou animação nova fora do pedido. Se a correção exigir mexer em algo LOCKED, pare e pergunte. No fim, liste o que mudou e confirme que o resto ficou idêntico.
- **Desktop e mobile obrigatórios.** Nada está pronto sem conferir 390 px (celular), 768 px (tablet) e 1440 px (desktop), com captura.
- **QA antes de "pronto".** Rodar `scripts/qa_site.py`, abrir e olhar as capturas, conferir o checklist. "Código escrito" não é entrega.
- **Sem padrões manipulativos.** Nada de urgência falsa, contador regressivo, "últimas vagas", pop-up de saída, opt-in pré-marcado, "+10.000 clientes", estatística sem fonte, promessa de posição no Google.
- **Gasto e produção só com OK do Thiago:** geração de imagem paga, plugin/serviço pago, domínio, deploy em produção.
- **Conselhos profissionais.** Saúde e arquitetura têm regras de publicidade (ver "Nichos"). Na dúvida, `[VERIFICAR]` com o cliente.

## Fluxo de trabalho

Use `templates/plano-do-site.md` como fonte da verdade do projeto (páginas, CTAs, assets e procedência, tese visual, itens LOCKED, rodadas de QA).

1. **Briefing e inventário.** Junte o que já existe antes de pedir algo: logo, fotos, textos, redes, site atual, Google Business Profile, materiais anteriores no Projeto. Meça as cores reais do logo/material com `scripts/extrair_paleta.py` (HEX exatos, nunca "a olho"). Liste o que falta como `[VERIFICAR]`.
2. **Estrutura.** Páginas, seções por página, um CTA principal por página, navegação (4–7 itens), URLs em português, minúsculas, com hífen. Essencial: 1 página, ~6 seções. Institucional: até 5 páginas. Site pequeno = no máximo 2 níveis.
3. **Direção visual.** Defina o modo da superfície e escreva a tese visual em 5 linhas antes de codar (ver "Direção visual"). Confira contra `references/anti-generico.md`. Prévia para prospect: "mostra uma direção de linguagem, não o projeto final".
4. **Desenvolvimento.** Stack conforme o projeto: Lovable + Supabase; Vite/React ou Next.js em GitHub → Vercel; HTML/CSS estático é aceitável para o Essencial. Tokens de design em CSS custom properties; componentes reutilizáveis; conteúdo separado do layout.
5. **Conteúdo, SEO, formulários, LGPD.** Seções abaixo + referências.
6. **QA.** Script + olhar as capturas + checklist. Corrija e rode de novo. Máximo de 2 rodadas internas antes de reportar o que ficou pendente — não entre em loop.
7. **Publicação.** Preview → OK do Thiago → produção → domínio/DNS/SSL → QA de novo contra a URL de produção → Search Console. Detalhes em `references/publicacao.md`.

## Direção visual

**Modo por superfície** (decide o que lidera a tela):

| Superfície | O que lidera | Exemplo |
|---|---|---|
| Persuadir | proposta + CTA real | landing page, site de serviço |
| Experiência | a obra/o produto; a interface recua | portfólio de arquiteto, fotógrafo |
| Operar | tarefa e dados, sem enfeite | /admin |
| Ler | texto, ritmo de leitura | blog, página de política |

**Tese visual (5 linhas, antes de codar):** estratégia de cor (contida, comprometida ou imersiva) · tipografia (máx. 2 famílias, papel de cada uma) · layout e grid · tratamento de imagem · o único momento de motion.

**Testes:**
- *Teste da categoria:* se dá para adivinhar a estética só pelo nicho (psicóloga = bege + serifa itálica + terracota; tech = roxo + gradiente), refaça.
- *Teste da troca:* se a frase ou a seção serviria igual para o concorrente, reescreva com algo específico do cliente.
- *Teste da primeira dobra:* em segundos o visitante entende o quê, para quem e o que fazer. Uma hora depois ele lembraria de algo concreto — não só de "um clima".

## Hierarquia visual e spacing

- Um H1 por página, dizendo o que é o negócio. Títulos em hierarquia sem pular nível.
- Hierarquia por tamanho, peso e espaço — não por cor ou caixa-alta em tudo.
- Escala de espaço em múltiplos de 4/8 px, aplicada com consistência. Mais espaço acima do título do que entre título e texto. Proximidade agrupa antes de criar caixas.
- Alterne seções densas e calmas; feche com um bloco final forte (CTA ou contato), não com vazio.
- Corpo ≥ 16 px; linha de 45–75 caracteres; altura de linha ~1,5–1,7 no corpo.
- Contraste: texto ≥ 4,5:1; texto grande, ícones e foco ≥ 3:1 (`extrair_paleta.py --contraste`). Texto sobre foto precisa de área calma ou véu, não de sombra pesada.
- Grid: alinhamentos limpos, cards de mesma linha com a mesma altura, nada encostando na borda, hero sem espaço morto.

## Mobile e desktop

- Sem rolagem lateral em 320–390 px. Imagens com `max-width: 100%`; nada com largura fixa maior que a tela.
- Alvos de toque ≥ 44 px (mínimo absoluto 24 px). Campos com fonte ≥ 16 px (o iPhone dá zoom abaixo disso).
- Menu mobile: abre e fecha por botão com nome acessível, fecha com Esc, foco volta ao botão, trava o scroll do fundo.
- Botão flutuante de WhatsApp não cobre CTA, texto nem a barra inferior do iPhone (`env(safe-area-inset-bottom)`).
- Mesma informação nos dois tamanhos: mobile reorganiza, não esconde conteúdo importante.
- Imagem com recorte próprio para mobile quando o enquadramento desktop não funciona (`<picture>` com `media`).
- Header fixo não esconde o título da seção ao navegar por âncora (`scroll-margin-top`).

## Portfólio

Detalhes e código do lightbox em `references/portfolio.md`.

- Grid 2×2 no desktop, 1 coluna no mobile. Proporção fixa por grid (ex.: 4:3 ou 3:2), `object-fit: cover` com `object-position` definido **foto a foto** — o ponto principal da obra nunca é cortado. Conferir cada crop na captura.
- Badge de categoria só quando ajuda a filtrar. CTA "Visitar site" só quando existir URL real.
- Página de projeto quando houver material: fotos, ficha técnica só com dados reais (local, ano, área), créditos do fotógrafo.
- Lightbox: abre a imagem ampliada; fecha por X, Esc e clique fora; setas ← →; foco preso dentro e devolvido ao item; scroll do fundo travado; swipe no celular; legenda.
- Uma foto decisiva vale mais que cinco medianas: curadoria antes de quantidade.

## CTA e WhatsApp

- O CTA é a ação real funcionando, não um link decorativo. O texto diz o que acontece: "Falar no WhatsApp", "Agendar visita", "Enviar mensagem".
- Um CTA principal por página; secundário só quando há um segundo caminho real.
- WhatsApp: `https://wa.me/55DDDNUMERO?text=` + mensagem codificada (ex.: "Olá, vim pelo site e gostaria de…"). Número confirmado pelo cliente — senão `[VERIFICAR]`.
- Contato também como link `tel:` e e-mail clicável quando o cliente quiser.

## Formulários, LGPD, honeypot e /obrigado

Detalhes em `references/formularios-lgpd.md`.

- Uma coluna; label visível em todo campo (placeholder não é label); `type`, `inputmode` e `autocomplete` corretos; pedir só o necessário.
- Validação ao sair do campo; erro específico ao lado do campo, em texto; nunca apagar o que foi digitado; foco no primeiro erro; botão com estado de envio.
- **LGPD:** checkbox de consentimento **não pré-marcado**, com link para a Política de Privacidade; registrar data/hora e versão do texto aceito; sem enriquecimento de leads.
- **Honeypot:** campo invisível (fora da tela, `tabindex="-1"`, `aria-hidden="true"`, `autocomplete="off"`); se vier preenchido, descartar em silêncio. Honeypot no front não impede envio direto à API — ver `/admin`.
- **/obrigado:** página real após o envio, com `noindex`, fora do sitemap, dizendo o que acontece agora (prazo de resposta, WhatsApp) e um caminho de volta. É onde se mede conversão.
- Política de Privacidade publicada antes do formulário ir ao ar; texto final validado pelo cliente.

## SEO

Checklist completo e modelos em `references/seo-tecnico.md`.

- Title único por página (50–60 caracteres) e meta description (150–160); `lang="pt-BR"`; canonical absoluto; um H1.
- Title, description, canonical, Open Graph e JSON-LD **no HTML servido** — em SPA (Lovable/Vite) o robô do WhatsApp/Facebook não executa JavaScript.
- Open Graph completo com `og:image` absoluta 1200×630; `twitter:card` = `summary_large_image`.
- `sitemap.xml` só com URLs 200, canônicas e indexáveis, `lastmod` real; `robots.txt` com a linha `Sitemap:`.
- JSON-LD com `addressCountry` "BR" e telefone +55; nunca `aggregateRating`/`Review` do próprio negócio.
- 404 personalizada que responde **status 404** de verdade. Favicon.
- Nunca prometer posição no Google.

## /admin

Quando o site tem painel (leads, projetos), seguir `references/admin-supabase.md`: RLS ligado, anon só insere, admin definido em tabela própria, signup público desligado, chave secreta nunca no front, `/admin` com `noindex` e `Disallow: /admin` no robots.txt, QA de permissões com evidência.

## Motion, acessibilidade e performance

Detalhes em `references/acessibilidade-performance.md`.

- **Motion:** um momento autoral, não o mesmo fade-up em toda seção. Ease-out, sem bounce. Conteúdo visível sem JavaScript. `prefers-reduced-motion` com alternativa. GSAP só quando agrega (as skills `gsap-*` cobrem a API; no site valem ScrollTrigger com moderação).
- **Acessibilidade:** teclado em tudo, foco visível, skip link, landmarks, alt real, botões só com ícone com nome acessível.
- **Performance:** imagens AVIF/WebP com `width`/`height`; hero com `fetchpriority="high"` e sem lazy; o resto `loading="lazy"`. Remover EXIF/GPS das fotos. Fontes hospedadas no site, `font-display: swap`. Metas: LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1.

## Nichos

- **Saúde (psicologia e afins):** nome completo e registro profissional (CRP etc.) visíveis; sem depoimentos de pacientes; sem promessa de resultado; sem preço como chamariz; sem sensacionalismo. Regras do conselho do cliente `[VERIFICAR]` (CFP, COFFITO, CFM…).
- **Arquitetura:** a obra lidera (modo Experiência); identificação do arquiteto responsável e registro CAU; autoria e créditos de fotografia; projetos de terceiros nunca como se fossem do cliente.
- **ARCA, VÉLIS, AXIS e STUDIO 26 são demos:** nunca aparecem como clientes ou cases.

## QA — definição de pronto

1. `python3 scripts/qa_site.py <URL> --saida qa/<projeto>` (preview e, depois, produção). Para site local, sirva antes (`npx vite preview`, `npm run preview` ou `python3 -m http.server`). Requer Python com `playwright` e `pillow` e o Chromium do Playwright — se faltar, instale uma vez (`pip install playwright pillow` e `python3 -m playwright install chromium`). Ele confere: rolagem lateral, alvos de toque e fonte de campo no celular; console e requisições com erro; imagens quebradas, sem alt ou sem dimensão; title, description, canonical, H1, lang, OG (inclusive 1200×630), Twitter, JSON-LD; robots.txt, sitemap.xml, 404 real, /obrigado com noindex, /admin bloqueado; formulários (label, consentimento não pré-marcado, honeypot, tipos); links de WhatsApp; texto provisório esquecido. Sai com código 1 se houver alerta.
2. Abra com Read o `home_mosaico.jpg` e as capturas de cada página nos três tamanhos. Olhe: hierarquia, respiro, alinhamento, crops do portfólio, texto cortado, CTA visível, nada sobreposto.
3. Teste manual do que o script não cobre: menu mobile, lightbox (X, Esc, clique fora, setas), envio do formulário **em preview** (nunca gerar lead falso em produção), chegada do lead no destino, /obrigado.
4. Copy: nada inventado, nenhum `[VERIFICAR]`, nenhum clichê da lista anti-genérico.
5. Revisão final com olhar de quem chega pela primeira vez, pelo celular. Nunca autocertificar sem evidência.

## Ao terminar

Responda com: link do preview ou produção, uma linha do que foi entregue, resumo do QA (alertas do script e como foram tratados, o que foi olhado nas capturas), o que ficou LOCKED e o que ainda é `[VERIFICAR]`. Envie o mosaico da home. Sem recapitular cada passo.
