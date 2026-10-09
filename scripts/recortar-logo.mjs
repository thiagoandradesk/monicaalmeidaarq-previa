#!/usr/bin/env node
/**
 * Recorta o logotipo real do post de lançamento (logo-01) e gera PNG transparente
 * em creme (#F6EADC) e em verde (#324937), com alfa calculado pela luminância de
 * cada pixel contra o fundo do post (#43523F). Também gera o monograma isolado e
 * os favicons. Sem vetorizar, sem redesenhar: só recorte + alfa.
 *
 * Coordenadas medidas no original 1080x1080 (perfil de linhas claras):
 *   monograma y 545-726 (x 405-684) · ARQUITETURA y 753-797 · QUE CUIDA y 813-838 · traço y 854-857
 *   caixa total x 332-760, y 545-857 -> recorte com margem de 16 px.
 */
import sharp from 'sharp';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const origem = path.join(raiz, 'assets-originais', 'logo-01.jpg');
const destino = path.join(raiz, 'public', 'logo');
await mkdir(destino, { recursive: true });
await mkdir(path.join(raiz, 'qa'), { recursive: true });

const FUNDO = [0x43, 0x52, 0x3f]; // #43523F
const CREME = [0xf6, 0xea, 0xdc]; // #F6EADC
const VERDE = [0x32, 0x49, 0x37]; // #324937
const lum = (r, g, b) => 0.2126 * r + 0.7152 * g + 0.0722 * b;
const L0 = lum(...FUNDO);
const L1 = lum(...CREME);

async function alfaDe(regiao) {
  const { data, info } = await sharp(origem)
    .extract(regiao)
    .removeAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });
  const n = info.width * info.height;
  const alfa = Buffer.alloc(n);
  for (let i = 0; i < n; i++) {
    const l = lum(data[i * 3], data[i * 3 + 1], data[i * 3 + 2]);
    let a = (l - L0) / (L1 - L0);
    if (a < 0.06) a = 0; // ruído de JPEG no fundo
    if (a > 1) a = 1;
    alfa[i] = Math.round(a * 255);
  }
  return { alfa, width: info.width, height: info.height };
}

function solido(cor, { alfa, width, height }) {
  const out = Buffer.alloc(width * height * 4);
  for (let i = 0; i < width * height; i++) {
    out[i * 4] = cor[0];
    out[i * 4 + 1] = cor[1];
    out[i * 4 + 2] = cor[2];
    out[i * 4 + 3] = alfa[i];
  }
  return sharp(out, { raw: { width, height, channels: 4 } }).png({ compressionLevel: 9 });
}

// 1) Logotipo completo (monograma + ARQUITETURA QUE CUIDA + traço)
const completo = await alfaDe({ left: 316, top: 529, width: 460, height: 344 });
await solido(CREME, completo).toFile(path.join(destino, 'logo-creme.png'));
await solido(VERDE, completo).toFile(path.join(destino, 'logo-verde.png'));

// 2) Monograma isolado (para favicon e OG)
const mono = await alfaDe({ left: 389, top: 529, width: 312, height: 214 });
await solido(CREME, mono).toFile(path.join(destino, 'monograma-creme.png'));
await solido(VERDE, mono).toFile(path.join(destino, 'monograma-verde.png'));

// 3) Favicons: monograma creme sobre quadrado verde da marca
const monoPng = await solido(CREME, mono).toBuffer();
for (const tam of [512, 192, 180, 32]) {
  const margem = Math.round(tam * 0.16);
  const mini = await sharp(monoPng)
    .resize({ width: tam - margem * 2, height: tam - margem * 2, fit: 'inside' })
    .toBuffer();
  const m = await sharp(mini).metadata();
  await sharp({ create: { width: tam, height: tam, channels: 4, background: '#324937' } })
    .composite([{ input: mini, left: Math.round((tam - m.width) / 2), top: Math.round((tam - m.height) / 2) }])
    .png()
    .toFile(path.join(destino, tam === 180 ? 'apple-touch-icon.png' : `favicon-${tam}.png`));
}

// 4) Prova visual: creme sobre verde e verde sobre creme, lado a lado
await sharp({ create: { width: 460 * 2 + 30, height: 344 + 20, channels: 3, background: '#F6EADC' } })
  .composite([
    { input: await sharp({ create: { width: 460, height: 344, channels: 3, background: '#43523F' } }).png().toBuffer(), left: 10, top: 10 },
    { input: await solido(CREME, completo).toBuffer(), left: 10, top: 10 },
    { input: await solido(VERDE, completo).toBuffer(), left: 480, top: 10 },
  ])
  .jpeg({ quality: 90 })
  .toFile(path.join(raiz, 'qa', 'logo-prova.jpg'));
console.log('logo-creme.png, logo-verde.png, monograma-*.png, favicons e qa/logo-prova.jpg gerados');
