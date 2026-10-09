# Plano do site — Monica Almeida | Arquitetura que Cuida · v1 (prévia de prospecção)

> Fonte da verdade da prévia. Monica é **prospect**, não cliente. Tudo marcado `[VERIFICAR]` não aparece na página.
> Pesquisa feita em 09/10/2026 (Instagram, Facebook, Linktree, LinkedIn público, cadastros de empresa, Vibe Prospecting). Construção da prévia em 09/10/2026 (Claude Code).
> Etapas: Briefing ☑ · Estrutura ☑ · Direção visual ☑ · Desenvolvimento ☑ · Conteúdo/SEO ☑ · QA preview ☑ · Publicação Vercel ☐ (aguarda login) · OK Thiago ☐ · Envio à Monica ☐

---

## 0. Dossiê da pesquisa

### Quem é

- **Monica Almeida**, arquiteta especializada em ambientes de saúde, Chapecó/SC. Atende "Brasil, online e presencial" (bio do Instagram).
- Empresa registrada como Monica Almeida Arquitetura Ltda, em Chapecó, desde 2019 (cadastros públicos) `[VERIFICAR]`.
- Formação: PUC-RS, segundo o resumo público do LinkedIn `[VERIFICAR]`.
- Registro CAU: **não encontrado** `[VERIFICAR]`. É obrigatório no site final.

### Canais (e o problema que eles mostram)

| Canal | Como a marca aparece | Observação |
|---|---|---|
| Instagram [@arquiteta_monicaalmeida](https://www.instagram.com/arquiteta_monicaalmeida/) | "Monica Almeida \| Arquitetura para Saúde" · bio "Arquitetura que Cuida / Neuroarquitetura + Experiência do Paciente / Projetos • Consultoria • Palestras / Brasil \| Online e presencial" | ~3,5 mil seguidores, ~585 posts. **Link da bio é um Linktree.** |
| [Linktree](https://linktr.ee/arquitetamonica) | "Arquiteta Monica Almeida" | Só 3 botões: Consultorias (WhatsApp), WhatsApp, Facebook. Nenhum lugar com projetos, consultoria ou palestras. O botão "WhatsApp" aponta para 554999691919 (sem o 9) e o "Consultorias" para 5549999691919 `[VERIFICAR se os dois funcionam]`. |
| [Facebook (página)](https://www.facebook.com/monicaalmeidaarquiteturaeinteriores/) | "Monica Almeida Arquitetura Hospitalar" · "Arquitetura e Interiores" | 527 seguidores. Endereço: Av. Getúlio Vargas, 681S, sala 103. |
| Facebook (perfil) | "Monica Almeida Arquitetura da Saúde" | Criadora digital. |
| LinkedIn (empresa) | "MONICA ALMEIDA Arquiteta da Saúde" | Diz "a número #1 do Sul": **não usar** (sem fonte). |

**Leitura comercial:** são 4 nomes diferentes para a mesma marca e 3 endereços diferentes nos cadastros (Getúlio Vargas 681S; Nereu Ramos 75D sala 1306B; Rua João Goulart 693). O site resolve isso: um endereço oficial da marca "Arquitetura que Cuida".

**Momento:** em 25 e 26/09/2026 ela relançou o Instagram com logotipo novo ("Arquitetura que Cuida") e uma série de posts fixados: **Sobre · Projetos · Visão**. O perfil já está organizado como um menu de site, mas o link da bio leva a um Linktree. É uma marca nova sem casa própria.

### Conceito e voz (palavras dela, dos posts)

- **"Arquitetura que Cuida: espaços pensados para funcionar bem e acolher pessoas."**
- **"O cuidado começa antes do atendimento."** Continua: "Ele começa na chegada, na forma como encontramos o caminho, na luz, no som e no lugar onde esperamos."
- "Minha visão de arquitetura para a saúde começa com uma pergunta: como as pessoas vivem este espaço?"
- "Observo o caminho de quem chega, a espera, a privacidade, a iluminação e as condições de trabalho de quem cuida."
- "Uno arquitetura, neuroarquitetura e experiência do paciente para ajudar profissionais e instituições de saúde a criar ambientes mais claros, acolhedores e adequados ao cuidado."
- Pilares citados: neuroarquitetura, experiência do paciente, design salutogênico.
- Serviços: **Projetos · Consultoria · Palestras**.
- Pergunta-assinatura (fecha vários posts): "Que experiência você gostaria de oferecer a quem entra no seu espaço?"
- Público: profissionais e instituições de saúde (consultórios médicos e odontológicos, clínicas, hospitais).

### Identidade visual

- **Logotipo:** monograma feito de arcos + "ARQUITETURA" (sans geométrica fina, espaçada) + "QUE CUIDA" (sans geométrica seminegrito, espaçada) + traço curto. Creme sobre verde. **Vetor oficial:** pedir à Monica `[VERIFICAR]`. Nunca redesenhar.
- **Paleta medida** (`extrair_paleta.py`, confirmada em 09/10 sobre os recortes do projeto — ver §2):

| Papel | HEX | Origem | Contraste |
|---|---|---|---|
| Verde da marca | `#324937` | faixas "Sobre / Projetos / Visão" (86–88% da área das faixas) | com creme 8,27:1 · com branco 9,80:1 |
| Verde do logotipo | `#43523F` | fundo do post do logotipo (96% do post) | com creme 7,04:1 |
| Creme | `#F6EADC` | logotipo e títulos sobre o verde | — |
| Caramelo | `#A0805F` (aprox.) | couro das poltronas nos projetos | material, não marca: só em linhas e pontos (2,68:1 sobre verde: **reprovado como texto**) |
| Mármore | `#E3E3DE` | pisos e bancadas dos renders | — |
| Greige | `#A09C94` | paredes dos renders | 2,74:1 com branco: **não usar em texto** |

- **Tipografia observada:** títulos dos posts em serifa; logotipo em sans geométrica. Decisão da prévia em §4.
- **Motivo recorrente:** o **arco**. Está no monograma e nas divisórias em arco com moldura dourada dos consultórios que ela projeta.

### Projetos disponíveis (renders publicados por ela)

| Projeto | Posts | Imagens | O que ela diz |
|---|---|---|---|
| P1 · Consultório médico-odontológico (arcos dourados, mármore, couro caramelo) | DaoJdKJmNt2 (4), DaoJKzlGAwB (2), Ddv5OsPFQ-j (1, com faixa "Visão") | 7 | "Cada detalhe comunica cuidado." Ambiente "sofisticado, acolhedor e atemporal"; iluminação, materiais nobres, cores suaves e layout funcional para reduzir a ansiedade. |
| P2 · Recepção de clínica oftalmológica (painéis ripados em madeira) | DaoGjFKmDML | 10 (4096 px) | Iluminação para conforto visual, menos ofuscamento; materiais naturais, cores suaves; neuroarquitetura e design salutogênico para transformar a espera em acolhimento. **O nome da clínica aparece no render: não citar** `[VERIFICAR]`. |
| P3 · Área de espera (poltronas caramelo, painel vazado, vista da cidade) | Ddv5H8NFXAr (1, com faixa "Projetos") | 1 | "Os assentos convidam à permanência, o painel vazado organiza o espaço sem fechá-lo e a luz natural aproxima o ambiente da cidade." |

- São **renders de projeto**, não fotos de obra. Apresentados como "Projeto · …".
- Local, ano, área e nome do cliente: desconhecidos. Não exibidos.
- **Retrato:** foto profissional dela (blazer verde), post Ddv5DZ1FVvq, com faixa "Sobre" embutida (recortada).
- **Não usar:** posts de "mood" com paisagens e pessoas (aparentam ser imagens ilustrativas, não projetos dela) e reels (um mostra a marca de um hospital `[VERIFICAR]`).
- Origem, links e instruções de recorte de cada imagem: `assets-manifest.json`.

---

## 1. Briefing (prévia)

- **Negócio:** arquitetura para ambientes de saúde: projetos, consultorias e palestras.
- **Pacote a propor:** Site Institucional, R$ 1.199 (até 5 páginas). Upsell natural: Captação Simples (formulário + painel de contatos) `[preço VERIFICAR]`, porque ela atende online em todo o Brasil.
- **Objetivo do site:** reunir a marca nova num lugar só, mostrar projetos com profundidade e transformar visita em conversa (WhatsApp/formulário).
- **Público e como chega:** médicos, dentistas, clínicas e instituições de saúde; chega pelo Instagram, por indicação e por palestras.
- **Restrições:** CAU obrigatório no site final `[VERIFICAR]`; sem "número 1", sem métricas, sem depoimentos inventados; projetos de terceiros nunca como dela; nome de clínica-cliente só com autorização.
- **Domínio:** não encontrado `[VERIFICAR]`.
- **Contato oficial:** WhatsApp (49) 99969-1919 (publicado por ela) · Instagram @arquiteta_monicaalmeida · e-mail `[VERIFICAR]` · endereço `[VERIFICAR]` (não publicado na prévia).

## 2. Inventário de assets (prévia)

Procedência de tudo: **asset real da cliente** (posts públicos do Instagram, baixados por `scripts/baixar-assets.mjs` em 09/10/2026, antes de as URLs expirarem). Processamento: `scripts/processar-assets.mjs` (recorte das faixas, WebP+AVIF em 480/960/1600 px, sem EXIF/ICC), `scripts/recortar-logo.mjs` (logotipo e favicons), `scripts/gerar-og.mjs` (OG 1200×630). Originais ficam em `assets-originais/` (fora do git).

| ID (manifest) | Uso na prévia | Recorte / proporção | `object-position` | Arquivo |
|---|---|---|---|---|
| logo-01 | logotipo do header, rodapé, 404, OG; favicons | área medida no original: x 316–776, y 529–873 (monograma 545–726, ARQUITETURA 753–797, QUE CUIDA 813–838, traço 854–857). A área do prompt (x 300–770, y 690–1020) estava deslocada: conferido na imagem. Alfa pela luminância contra `#43523F`; comparado com `ref/logo_ref_*.png` | — | `public/logo/logo-creme.png`, `logo-verde.png`, `monograma-*.png`, `favicon-32/192/512.png`, `apple-touch-icon.png` |
| projeto-consultorio-odonto-02 | **hero** (máscara em arco, proporção 0,72) e OG | integral | 50% 50% (arcos dos dois lados, cadeira ao centro) | `public/img/projeto-consultorio-odonto-02-{480,960,1080}.{webp,avif}` |
| projeto-consultorio-odonto-01 | **grid P1** (5:4) e lightbox P1 1/5 | integral | 50% 55% (arcos + cadeira + mesa ao fundo) | `…-odonto-01-*` |
| projeto-consultorio-04 | lightbox P1 2/5 | integral | contain | `…-consultorio-04-*` |
| projeto-consultorio-03 | lightbox P1 3/5 | integral | contain | `…-consultorio-03-*` |
| projeto-consultorio-01 | lightbox P1 5/5 | integral | contain | `…-consultorio-01-*` |
| projeto-recepcao-oftalmologia-04 | **grid P2** (5:4) e lightbox P2 1/3 | integral | 50% 50% (poltronas + ripado + luz natural; sem logotipo da clínica) | `…-oftalmologia-04-{480,960,1600}` |
| projeto-recepcao-oftalmologia-06 | lightbox P2 2/3 | integral | contain | `…-oftalmologia-06-*` |
| projeto-recepcao-oftalmologia-08 | lightbox P2 3/3 | integral | contain | `…-oftalmologia-08-*` |
| projeto-area-de-espera-01 | **grid P3** (5:4) e lightbox P3 1/1 | y 0–880 de 1080 (faixa "Projetos" removida) | 50% 60% (poltronas, painel vazado e cidade) | `…-area-de-espera-01-*` |
| retrato-sobre-01 | **Sobre** (máscara em arco 4:5) | y 0–880 de 1080 (faixa "Sobre" removida) | 42% 50% (rosto centrado, flores à direita) | `retrato-sobre-01-*` |

Não usados (e por quê): `projeto-consultorio-02` (quase igual ao 01); `projeto-consultorio-visao-01` (mesmo render do odonto-01, com faixa); `projeto-recepcao-oftalmologia-01, 02, 03, 05, 07, 09, 10` (logotipo da clínica legível na parede — regra 4). Curadoria feita sobre `qa/contact-sheet-*.jpg` e `qa/teste-crops.jpg`.

- **Paleta confirmada** (09/10, `extrair_paleta.py` sobre os recortes): faixas "Visão"/"Sobre" = `#324937` (86,4% / 88,4%); post do logotipo = `#43523F` (96,1%); renders dominados por greige/mármore (`#939087`, `#C5C1B8`, `#CCCAC5`) e caramelo (`#A99276`, `#755A3E`).
- **Contraste dos pares usados em texto:** creme × verde 8,27:1 ✓ · creme-2 `#D9CDBE` × verde 6,26:1 ✓ · verde × creme 8,27:1 ✓ · verde-texto-2 `#5C6B57` × creme 4,79:1 ✓ · caramelo-claro `#C9A77E` × verde 4,34:1 (só numeração ≥ 22 px) · caramelo-escuro `#8A6A4A` × creme 4,18:1 (só a borda do campo com erro e links em hover; o texto do erro é verde) · caramelo `#A0805F` × verde 2,68:1 ✗ (só linha e pontos, decorativos).
- **Fontes:** Libre Baskerville 400/400i + Montserrat 300/400/500/600, woff2 em `public/fonts/` (@fontsource, OFL), `font-display: swap`, preload das duas principais.
- **Faltando:** vetor do logotipo, nomes das fontes da marca, fotos de obra, dados dos projetos — tudo `[VERIFICAR]`.

## 3. Estrutura do site final (Institucional, 5 páginas)

| Página | URL | Objetivo | CTA principal |
|---|---|---|---|
| Home | `/` | apresentar a Arquitetura que Cuida e levar à conversa | Conversar sobre meu projeto |
| Sobre | `/sobre/` | trajetória, abordagem, CAU | Conversar sobre meu projeto |
| Projetos | `/projetos/` (+ `/projetos/<slug>/`) | portfólio com lightbox | Quero um projeto assim |
| Consultoria e Palestras | `/consultoria-e-palestras/` | formatos online/presencial, temas | Solicitar consultoria / Convidar para palestra |
| Contato | `/contato/` | formulário + WhatsApp | Enviar mensagem |
| Obrigado | `/obrigado/` | confirmar envio (noindex) | WhatsApp |
| Privacidade | `/politica-de-privacidade/` | LGPD | — |

Menu: Sobre · Projetos · Consultoria e Palestras · Contato.

## 3b. Estrutura da PRÉVIA (1 página: a Home) — construída

1. **Faixa de prévia** (caramelo-escuro, topo): "Prévia de site desenvolvida pela RevoluTech para Monica Almeida. Mostra uma direção de linguagem, não a versão final."
2. **Header** (sticky, verde): logotipo real · Sobre · Projetos · Como trabalho · Contato · "Falar no WhatsApp". Mobile: botão com nome, Esc fecha, foco volta, scroll travado, fundo `inert`.
3. **Hero:** H1 "Arquitetura para ambientes de saúde" + "O cuidado começa antes do atendimento." (itálico, caramelo-claro) + "Ele começa na chegada, na forma como encontramos o caminho, na luz, no som e no lugar onde esperamos." + CTAs. Imagem odonto-02 com máscara em arco.
4. **Manifesto:** "Minha visão… começa com uma pergunta:" → H2 "Como as pessoas vivem este espaço?" → "Observo o caminho de quem chega…". Percurso em 5 pontos (Chegada e caminho · Espera · Privacidade · Luz e som · Quem cuida) com fragmentos literais das frases dela; linha caramelo que se desenha com a rolagem; fecho "Arquitetura que Cuida: espaços pensados para funcionar bem e acolher pessoas."
5. **Projetos:** P1 (7 col) + P2 (5 col, escalonado) + P3 (7 col deslocado). Textos das legendas dela. Lightbox `<dialog>` com X, Esc, clique fora, setas, swipe, foco preso/devolvido, legenda e contador.
6. **Como trabalho:** lista editorial Projetos · Consultoria · Palestras + "Online e presencial, em todo o Brasil."
7. **Sobre:** retrato em arco + "Sou Monica Almeida, arquiteta especializada em ambientes de saúde." + "Uno arquitetura…" + "Chapecó/SC · atendimento em todo o Brasil, online e presencial." + link do Instagram. Sem CAU.
8. **Contato:** H2 "Que experiência você gostaria de oferecer a quem entra no seu espaço?" + WhatsApp + formulário de demonstração (nome, WhatsApp, e-mail opcional, tipo de espaço, mensagem, consentimento não pré-marcado, honeypot). Envio não vai a lugar nenhum: valida e mostra "Esta é uma prévia. No site final, sua mensagem chega direto no seu painel de contatos."
9. **Rodapé** (verde do logotipo): logotipo · Instagram · WhatsApp · "Chapecó/SC · atendimento em todo o Brasil, online e presencial" · crédito "Prévia RevoluTech".
10. Extras: botão flutuante de WhatsApp só em ≥ 1280 px, aparece depois do hero e some na seção de contato (no celular o header já tem o botão); `404.html` com caminho de volta.

## 4. Direção visual

- **Modo:** Experiência (o projeto lidera) com CTA claro de Persuadir.
- **Tese visual:**
  1. **Cor:** comprometida com o verde dela (`#324937`) como superfície das seções-âncora (hero, manifesto, contato), alternando com branco (projetos, sobre) e creme (como trabalho, formulário). Caramelo só em linhas finas, pontos e numeração do percurso, hover e faixa de prévia.
  2. **Tipografia (decidida 09/10):** **Libre Baskerville** para títulos e frases dela; **Montserrat** 300/400/500 para menu, rótulos e corpo. Teste em `qa/fontes/compara.png`: contra o "Visão" dos posts, a Libre Baskerville ficou mais próxima no contraste de traço e no desenho clássico (Lora é mais caligráfica); contra o "ARQUITETURA QUE CUIDA" do logotipo, Montserrat 300 reproduz o traço fino e o espaçamento. `[VERIFICAR com a Monica]` as fontes oficiais da marca.
  3. **Layout:** editorial em 12 colunas, assimétrico (7/5 nos projetos, coluna fixa no manifesto), respiro generoso. O **arco** aparece em 2 lugares: hero e retrato.
  4. **Imagem:** só renders e retrato reais dela, sem faixas embutidas, crop conferido foto a foto (§2). Nada de banco de imagem nem IA.
  5. **Motion (único momento):** linha caramelo que se desenha ligando os 5 pontos do percurso conforme a rolagem (`src/percurso.ts`, scroll + rAF, geometria medida no DOM). Sem JS, a linha já aparece pronta; com `prefers-reduced-motion`, idem.
- **Teste da categoria:** o esperado para "arquitetura de saúde" seria branco hospitalar com azul ou verde-menta. Aqui a cor vem da marca dela. Passa.
- **Teste da troca:** percurso do paciente, pergunta-assinatura e arcos são dela. Passa.
- **Teste da primeira dobra (390 e 1440):** H1, frase da marca, CTA e começo do arco visíveis sem espaço morto (`qa/previa/manuais/celular_primeira_dobra.jpg`, `qa/previa/capturas/home_desktop.jpg`).
- **Itens da lista anti-genérico usados de propósito:** numeração 01–05 (o percurso é uma sequência real); um rótulo em caixa-alta acima do H2 do manifesto (é a frase dela, "Minha visão… começa com uma pergunta:", não um kicker genérico).

## 5. Técnico

- **Stack:** Vite 8 (vanilla + TypeScript), HTML/CSS com tokens em custom properties, sem framework. Scripts de assets em Node + sharp.
- **Repositório:** GitHub privado `previa-monica-almeida` — a criar (precisa de `gh auth login` do Thiago). · **Projeto Vercel:** `previa-monica-almeida` — a criar (precisa de `vercel login`). · **URL de preview:** `https://previa-monica-almeida.vercel.app/` (se o nome estiver ocupado, a Vercel sufixa; canonical/OG seguem `VERCEL_PROJECT_PRODUCTION_URL` no build).
- **Formulário:** demonstração, sem destino (regra da prévia). Texto do consentimento sem link de política (não existe política publicada); no site final, registrar a versão do texto aceito.
- **/admin:** não. **Analytics/pixel:** não.
- **Headers (vercel.json):** `X-Robots-Tag: noindex, nofollow` em tudo; cache imutável para `/img`, `/logo`, `/fonts`, `/og`.

## 6. SEO (prévia)

| Página | Title (63) | Description (156) | OG image |
|---|---|---|---|
| Home | Monica Almeida \| Arquitetura que Cuida — Arquitetura para Saúde | Arquitetura para ambientes de saúde em Chapecó/SC e em todo o Brasil: projetos, consultoria e palestras que unem neuroarquitetura e experiência do paciente. | `/og/home.jpg` 1200×630 (logotipo creme sobre verde + render odonto-02), 59 KB |

- JSON-LD: `LocalBusiness` (nome, telefone +55-49-99969-1919, Chapecó/SC/BR sem logradouro, areaServed Brasil, sameAs Instagram) + `Person` (Monica Almeida, Arquiteta) + `WebSite`. Sem avaliação, sem endereço, sem CAU.
- `robots.txt`: `Disallow: /` (intencional) · sem `sitemap.xml` (intencional) · `<meta name="robots" content="noindex, nofollow">` na home e na 404 · `404.html` real.

## 7. QA

| Data | Ambiente | Alertas do script | Revisão das capturas | Pendências |
|---|---|---|---|---|
| 09/10/2026 | preview local (`vite preview`, 4173), 2 rodadas internas | **8 alertas, todos esperados/justificados:** (1) robots sem `Sitemap:`; (2) `Disallow: /`; (3) sem sitemap.xml; (4) página com noindex — os quatro são a regra 7 da prévia; (5) "404 parece vazia" — é o 404 do vite preview; na Vercel serve `404.html`, conferir após deploy; (6) og:image 404 — a URL é absoluta para a Vercel ainda não publicada; conferir após deploy; (7) formulário sem link para Política de Privacidade — não existe política na prévia (documentado no texto do consentimento); (8) "texto provisório: TODO/todo" — **falso positivo**: o regex `\bTODO\b` com `re.I` casa com a palavra "todo" de "em todo o Brasil" (texto obrigatório da regra 9). INFO: checkbox de consentimento com 24 px (mínimo WCAG; o rótulo inteiro é clicável). Rodada 1 ainda tinha 2 alertas meus, corrigidos: `<img>` vazio do lightbox contado como quebrado (placeholder) e honeypot contado como alvo < 24 px / fonte < 16 px (dimensionado dentro do contêiner de 1 px). | Mosaico 390/768/1440 e capturas completas revisadas: hierarquia (H1 > destaque > frase), respiro, alinhamento das colunas, crops (arcos do hero inteiros, cadeira e mesa no P1, poltronas no P2, poltronas+painel+cidade no P3, rosto no retrato), nenhum texto cortado, CTA visível na primeira dobra, faixa de prévia presente, nada sobreposto. Bug achado e corrigido na rodada 2: atributo `height` do `<img>` prendia a altura (grid alto demais, arco com bloco verde). Testes manuais (`qa/testes-manuais.py`): 34/34 OK — menu mobile, formulário (erros, foco, consentimento, mensagem de prévia, sem fetch/XHR), honeypot, links WhatsApp/Instagram, lightbox (teclado, setas, ciclo, Esc, X, clique fora, foco preso/devolvido, swipe, imagem única), linha do percurso (desenha, reduced-motion, sem JS). | Deploy na Vercel + QA contra a URL publicada (alertas 5 e 6 devem sumir). |

Grep final (`[VERIFICAR]`, lorem, placeholder, TODO, nomes de cliente, "número 1"): nenhuma ocorrência no `index.html`/`404.html` além do falso positivo "todo".

## 8. Abordagem sugerida (1ª mensagem: Instagram DM ou WhatsApp)

> Oi, Monica! Tudo bem? Sou o Thiago, da RevoluTech. Vi o lançamento da Arquitetura que Cuida no seu Instagram. O "o cuidado começa antes do atendimento" resume muito bem o seu trabalho.
>
> Notei que hoje o link da bio leva para o Linktree, sem um lugar que reúna seus projetos, a consultoria e as palestras. A gente desenvolve sites e sistemas para profissionais de saúde, e eu montei uma prévia de como poderia ficar o site da Arquitetura que Cuida, com a sua identidade.
>
> Posso te mandar o link para você ver?

Sem preço na 1ª mensagem. Preço (Site Institucional, R$ 1.199) depois que ela vir a prévia.

## 9. Pendências `[VERIFICAR]` (não vão para a página)

- Número do CAU.
- Endereço oficial (3 versões nos cadastros).
- E-mail profissional.
- Vetor oficial do logotipo e nomes das fontes da marca (prévia usa Libre Baskerville + Montserrat).
- Nome, local e ano de cada projeto; autorização para citar clientes (ex.: clínica oftalmológica) e para usar os renders no site final.
- Domínio.
- Se o botão "WhatsApp" do Linktree (número sem o 9) funciona.
- Texto da Política de Privacidade e do consentimento (site final).

## 10. Registro de decisões

| Data | Decisão | Por |
|---|---|---|
| 09/10/2026 | Lead nº 1 da lista de arquitetura SC+RS; prévia personalizada | Thiago |
| 09/10/2026 | Fluxo: pesquisa e assets no Cowork; construção e deploy da prévia no Claude Code | Thiago |
| 09/10/2026 | Logotipo recortado em x 316–776 / y 529–873 (medido), não na área aproximada do prompt | Claude (conferido na imagem) |
| 09/10/2026 | P2 usa só as 3 imagens sem o logotipo da clínica (04, 06, 08) | Claude (regra 4) |
| 09/10/2026 | Hero = odonto-02 (arcos dos dois lados); grid P1 = odonto-01 | Claude (curadoria em contact sheet) |
| 09/10/2026 | Libre Baskerville + Montserrat; Lora descartada (mais caligráfica e na lista de fontes batidas) | Claude `[VERIFICAR com a Monica]` |
| 09/10/2026 | Caramelo `#A0805F` nunca em texto (2,68:1 sobre verde); numeração em `#C9A77E` | Claude (extrair_paleta.py --contraste) |
| 09/10/2026 | Botão flutuante de WhatsApp só em ≥ 1280 px, oculto no hero e no contato | Claude (regra "não cobrir CTA nem texto") |
| 09/10/2026 | Canonical/OG seguem `VERCEL_PROJECT_PRODUCTION_URL` no build (plugin em `vite.config.ts`) | Claude |
| 09/10/2026 | Python 3.12 instalado (winget, escopo de usuário) com playwright+pillow para o QA; rodar `qa_site.py` com `python -X utf8` no Windows | Claude (skill: "instale uma vez") |
