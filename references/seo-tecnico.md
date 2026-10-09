# SEO técnico — checklist e modelos

Consolidado de: contexto RevoluTech §4.12, marketingskills (Corey Haines, MIT), claude-seo (AgriciDaniel, MIT) e diretrizes públicas do Google. Reescrito para sites pequenos brasileiros. Não promete posição no Google — garante que o site está tecnicamente correto.

## Por página

- `<html lang="pt-BR">` e `<meta name="viewport" content="width=device-width, initial-scale=1">` (sem `user-scalable=no`).
- `<title>` único, 50–60 caracteres: o que é + onde/para quem + marca. Ex.: "Arquitetura residencial em Itajaí | Estúdio X".
- Meta description única, 150–160 caracteres, descrevendo a página de verdade.
- Canonical absoluto apontando para a própria URL (com a barra final consistente).
- Um H1; H2/H3 em ordem.
- URL em português, minúscula, com hífen: `/projetos/casa-aria`.
- Links internos com texto descritivo.
- Todo o essencial (title, description, canonical, OG, JSON-LD) **no HTML servido**.

### SPA (Lovable / Vite / React Router)

O robô do WhatsApp, Facebook e LinkedIn não executa JavaScript. Em SPA:

- No mínimo, o `index.html` precisa ter title, description e OG da home já escritos.
- Para páginas internas com OG próprio, usar pré-renderização (gerar HTML por rota no build) ou framework com SSR/SSG. `[VERIFICAR]` a ferramenta de pré-render compatível com o projeto antes de instalar.
- Rotas inexistentes precisam responder 404 real (ver `publicacao.md`).

## Open Graph e Twitter

```html
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Nome do Cliente">
<meta property="og:title" content="Título da página">
<meta property="og:description" content="Descrição curta e específica.">
<meta property="og:url" content="https://dominio.com.br/pagina/">
<meta property="og:image" content="https://dominio.com.br/og/pagina.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Descrição da imagem">
<meta name="twitter:card" content="summary_large_image">
```

- `og:image` **absoluta**, 1200×630, JPG ou PNG, < 300 KB, com a identidade do cliente (logo real, foto real). Texto grande e centralizado — o WhatsApp corta as bordas na prévia.
- Teste a prévia colando o link no WhatsApp (conversa consigo mesmo) depois de publicar.

## robots.txt

```
User-agent: *
Allow: /
Disallow: /admin

Sitemap: https://dominio.com.br/sitemap.xml
```

- `/obrigado` **não** vai no `Disallow` — ela precisa ser rastreável para o robô ver o `noindex`. Fica fora do sitemap e com `<meta name="robots" content="noindex, follow">`.
- `/admin`: `Disallow` (regra da casa) + `noindex` na página de login.
- Robôs de IA: separar os de **busca** (aparecer em respostas: OAI-SearchBot, Claude-SearchBot, PerplexityBot) dos de **treino** (GPTBot, ClaudeBot, Google-Extended). Por padrão, permitir os de busca; bloquear os de treino só se o cliente pedir. `[VERIFICAR]` nomes atuais dos robôs antes de publicar.
- Preview na Vercel não deve ser indexado (a Vercel costuma enviar `X-Robots-Tag: noindex` em URLs de preview — `[VERIFICAR]` no projeto).

## sitemap.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://dominio.com.br/</loc><lastmod>2026-10-08</lastmod></url>
  <url><loc>https://dominio.com.br/projetos/</loc><lastmod>2026-10-08</lastmod></url>
</urlset>
```

- Só URLs com status 200, canônicas e indexáveis. Sem `/obrigado`, `/admin`, `/login`.
- `lastmod` com a data real da última mudança. `priority` e `changefreq` são ignorados pelo Google — não precisa.

## JSON-LD

Um bloco `@graph` por site (na home, ou em todas as páginas), com `@id` fixo:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "LocalBusiness",
      "@id": "https://dominio.com.br/#negocio",
      "name": "Nome do Cliente",
      "url": "https://dominio.com.br/",
      "image": "https://dominio.com.br/og/home.jpg",
      "logo": "https://dominio.com.br/logo.png",
      "telephone": "+55-47-99999-9999",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Rua Exemplo, 123",
        "addressLocality": "Itajaí",
        "addressRegion": "SC",
        "postalCode": "88300-000",
        "addressCountry": "BR"
      },
      "areaServed": "Itajaí e região",
      "sameAs": ["https://www.instagram.com/perfil"]
    },
    {
      "@type": "WebSite",
      "@id": "https://dominio.com.br/#site",
      "url": "https://dominio.com.br/",
      "name": "Nome do Cliente",
      "inLanguage": "pt-BR",
      "publisher": { "@id": "https://dominio.com.br/#negocio" }
    }
  ]
}
</script>
```

(Os valores acima são exemplo de formato. No site, só dados reais do cliente.)

- Use o tipo mais específico que exista e seja verdadeiro (ex.: `Dentist`, `MedicalClinic`, `Restaurant`). `ProfessionalService` é desaconselhado pelo próprio Schema.org.
- Arquiteto: não existe tipo `Architect`. Use `LocalBusiness` (escritório) + `Person` (arquiteto responsável) com `hasCredential` para o registro CAU, se o cliente quiser.
- Profissional de saúde: `LocalBusiness` ou subtipo médico adequado + `Person` com o registro. `[VERIFICAR]` o subtipo.
- Atende em casa ou só online: sem endereço publicado; use `areaServed`.
- **Proibido:** `aggregateRating` e `Review` sobre o próprio negócio; HowTo (aposentado); dados inventados.
- Nome, endereço e telefone idênticos no site, no JSON-LD e no Perfil da Empresa no Google.
- Validar no Rich Results Test e no validator.schema.org.

## Imagens

- Formatos modernos (AVIF/WebP) com fallback via `<picture>`.
- `width` e `height` em toda `<img>` (evita CLS).
- Imagem principal (LCP): `fetchpriority="high"`, sem `loading="lazy"`. As demais: `loading="lazy" decoding="async"`.
- Peso de referência: hero < 200–300 KB; imagens de conteúdo < 100–150 KB.
- `alt` descritivo e real; imagem decorativa com `alt=""`.
- Nome de arquivo descritivo: `casa-aria-fachada.webp`.
- **Remover EXIF/GPS** das fotos do cliente antes de publicar (privacidade e LGPD).

## Desempenho (Core Web Vitals)

- LCP ≤ 2,5 s · INP ≤ 200 ms · CLS ≤ 0,1.
- Fontes hospedadas no próprio site (woff2), `font-display: swap`, preload só da fonte principal.
- Scripts de terceiros (analytics, pixel) com `defer`/`async`, carregados depois do conteúdo — e só com consentimento quando usarem cookies.
- Sem `transition: all`; animar só `transform` e `opacity`.

## Depois de publicar

- HTTPS em tudo, sem conteúdo misto; uma única versão do domínio (com ou sem `www`) e redirect 301 da outra, em um salto.
- Search Console: verificar o domínio, enviar o sitemap, pedir indexação da home.
- Perfil da Empresa no Google com a mesma categoria, nome, endereço e telefone do site.
- Bing Webmaster Tools (importa do Search Console).
