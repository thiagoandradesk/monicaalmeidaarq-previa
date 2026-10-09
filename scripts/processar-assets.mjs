#!/usr/bin/env node
/**
 * Processa os assets originais (assets-originais/) para public/img/:
 *  - recorta as faixas verdes com texto embutido (mantém y 0–880 de 1080) nos
 *    grupos indicados em RECORTAR_FAIXA;
 *  - gera WebP e AVIF em 480, 960 e 1600 px de largura (sem ampliar: para
 *    originais de 1080 px, a maior variante é a largura nativa);
 *  - remove EXIF/ICC/XMP (sharp descarta metadados por padrão).
 *
 * Uso: node scripts/processar-assets.mjs
 * Saída: public/img/<id>-<largura>.{webp,avif} e public/img/manifest.json
 */
import sharp from 'sharp';
import { readFile, readdir, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const origem = path.join(raiz, 'assets-originais');
const destino = path.join(raiz, 'public', 'img');
const LARGURAS = [480, 960, 1600];
const RECORTAR_FAIXA = new Set(['retrato-sobre', 'projeto-area-de-espera', 'projeto-consultorio-visao']);
const ALTURA_UTIL = 880; // de 1080: abaixo disso fica a faixa verde com "Sobre"/"Projetos"/"Visão"

const manifest = JSON.parse(await readFile(path.join(raiz, 'assets-manifest.json'), 'utf8'));
await mkdir(destino, { recursive: true });
const arquivos = await readdir(origem);
const saida = {};

for (const item of manifest.itens) {
  if (item.tipo === 'logo') continue; // o logotipo tem script próprio (recortar-logo.mjs)
  const arq = arquivos.find((f) => f.startsWith(item.id + '.'));
  if (!arq) {
    console.error(`x ${item.id}: original não encontrado em assets-originais/`);
    continue;
  }
  let img = sharp(path.join(origem, arq)).rotate(); // aplica orientação EXIF antes de descartá-la
  const meta = await img.metadata();
  let { width, height } = meta;
  if (RECORTAR_FAIXA.has(item.grupo)) {
    const h = Math.round((ALTURA_UTIL / 1080) * height);
    img = img.extract({ left: 0, top: 0, width, height: h });
    height = h;
  }
  const base = await img.toColourspace('srgb').toBuffer();
  const larguras = [...new Set(LARGURAS.map((w) => Math.min(w, width)))].sort((a, b) => a - b);
  const variantes = [];
  for (const w of larguras) {
    const h = Math.round((height / width) * w);
    const redim = sharp(base).resize({ width: w, withoutEnlargement: true });
    const nomeBase = `${item.id}-${w}`;
    await redim.clone().webp({ quality: 80, effort: 5 }).toFile(path.join(destino, `${nomeBase}.webp`));
    await redim.clone().avif({ quality: 58, effort: 5 }).toFile(path.join(destino, `${nomeBase}.avif`));
    variantes.push({ largura: w, altura: h });
  }
  saida[item.id] = {
    grupo: item.grupo,
    tipo: item.tipo,
    post: item.post,
    indice_carrossel: item.indice_carrossel,
    recorte: RECORTAR_FAIXA.has(item.grupo) ? `y 0-${ALTURA_UTIL} de 1080 (faixa verde removida)` : 'integral',
    proporcao: +(width / height).toFixed(4),
    variantes,
  };
  console.log(`ok ${item.id}: ${width}x${height} -> ${larguras.join('/')} px (webp+avif)`);
}

await writeFile(path.join(destino, 'manifest.json'), JSON.stringify(saida, null, 1));
console.log(`\n${Object.keys(saida).length} imagens processadas -> public/img/`);
