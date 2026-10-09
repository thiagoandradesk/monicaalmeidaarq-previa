#!/usr/bin/env node
/**
 * Baixa os assets reais da Monica listados em assets-manifest.json para
 * assets-originais/<id>.<ext> (pasta fora do git).
 *
 * Uso: node scripts/baixar-assets.mjs [--forcar]
 *
 * As URLs assinadas do Instagram expiram (ver "validade_urls" no manifest).
 * Se alguma responder 403/410, o script lista os permalinks que precisam ser
 * recoletados e sai com código 1 — a recoleta é feita à parte, pelo post.
 */
import { readFile, writeFile, mkdir, stat } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const manifestPath = path.join(raiz, 'assets-manifest.json');
const destino = path.join(raiz, 'assets-originais');
const forcar = process.argv.includes('--forcar');

const UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36';

function extensaoDe(url, contentType) {
  const p = new URL(url).pathname.toLowerCase();
  const m = p.match(/\.(jpe?g|png|webp|avif|gif)$/);
  if (m) return m[1] === 'jpeg' ? 'jpg' : m[1];
  if (contentType?.includes('webp')) return 'webp';
  if (contentType?.includes('png')) return 'png';
  return 'jpg';
}

async function existe(p) {
  try {
    const s = await stat(p);
    return s.size > 0;
  } catch {
    return false;
  }
}

const manifest = JSON.parse(await readFile(manifestPath, 'utf8'));
await mkdir(destino, { recursive: true });

const falhas = [];
let baixados = 0;
let pulados = 0;

for (const item of manifest.itens) {
  const extPrevista = extensaoDe(item.url_original);
  const alvoPrevisto = path.join(destino, `${item.id}.${extPrevista}`);
  if (!forcar && (await existe(alvoPrevisto))) {
    pulados++;
    continue;
  }
  try {
    const r = await fetch(item.url_original, {
      headers: { 'user-agent': UA, accept: 'image/avif,image/webp,image/*,*/*;q=0.8' },
      redirect: 'follow',
    });
    if (!r.ok) {
      falhas.push({ id: item.id, status: r.status, post: item.post, indice: item.indice_carrossel });
      console.error(`✗ ${item.id}: HTTP ${r.status}`);
      continue;
    }
    const buf = Buffer.from(await r.arrayBuffer());
    const ext = extensaoDe(item.url_original, r.headers.get('content-type'));
    const alvo = path.join(destino, `${item.id}.${ext}`);
    await writeFile(alvo, buf);
    baixados++;
    console.log(`✓ ${item.id}.${ext} (${(buf.length / 1024).toFixed(0)} KB)`);
  } catch (e) {
    falhas.push({ id: item.id, status: e?.message ?? String(e), post: item.post, indice: item.indice_carrossel });
    console.error(`✗ ${item.id}: ${e?.message ?? e}`);
  }
}

console.log(`\n${baixados} baixado(s), ${pulados} já existente(s), ${falhas.length} falha(s).`);
if (falhas.length) {
  console.log('\nRecoletar pelo permalink (sem login):');
  for (const f of falhas) console.log(`  ${f.id} → ${f.post} (slide ${f.indice}) [${f.status}]`);
  process.exit(1);
}
