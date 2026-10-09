import { defineConfig, type Plugin } from 'vite';

/**
 * URL pública da prévia. No build da Vercel, VERCEL_PROJECT_PRODUCTION_URL traz o
 * domínio real do projeto (ex.: previa-monica-almeida.vercel.app); fora dela,
 * VITE_SITE_URL ou o valor padrão. Canonical, og:url, og:image e JSON-LD usam esse valor.
 */
const URL_PADRAO = 'https://previa-monica-almeida.vercel.app';
function urlDoSite(): string {
  const vercel = process.env.VERCEL_PROJECT_PRODUCTION_URL;
  const manual = process.env.VITE_SITE_URL;
  const url = manual || (vercel ? `https://${vercel}` : URL_PADRAO);
  return url.replace(/\/+$/, '');
}

const urlPublica = (): Plugin => ({
  name: 'url-publica-da-previa',
  transformIndexHtml(html) {
    return html.replaceAll(URL_PADRAO, urlDoSite());
  },
});

export default defineConfig({
  // 'mpa': sem fallback para index.html — rota inexistente responde 404 também no preview local.
  appType: 'mpa',
  plugins: [urlPublica()],
  build: {
    target: 'es2022',
    cssTarget: 'chrome100',
    assetsInlineLimit: 2048,
  },
  server: { port: 5173, strictPort: true },
  preview: { port: 4173, strictPort: true },
});
