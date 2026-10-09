#!/usr/bin/env node
/**
 * Gera a imagem Open Graph 1200x630 (public/og/home.jpg) a partir do render do
 * hero (odonto-02, asset real) e do logotipo recortado (creme). Sem texto
 * renderizado por fonte do sistema: só assets reais sobre o verde da marca.
 */
import sharp from 'sharp';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const W = 1200;
const H = 630;
const PAINEL = 520; // largura do painel verde com o logotipo

await mkdir(path.join(raiz, 'public', 'og'), { recursive: true });

const foto = await sharp(path.join(raiz, 'public', 'img', 'projeto-consultorio-odonto-02-1080.webp'))
  .resize({ width: W - PAINEL, height: H, fit: 'cover', position: 'centre' })
  .toBuffer();

const logo = await sharp(path.join(raiz, 'public', 'logo', 'logo-creme.png'))
  .resize({ width: 340, withoutEnlargement: true })
  .toBuffer();
const lm = await sharp(logo).metadata();

const linha = await sharp({ create: { width: 2, height: H, channels: 4, background: '#A0805F' } }).png().toBuffer();

await sharp({ create: { width: W, height: H, channels: 3, background: '#324937' } })
  .composite([
    { input: foto, left: PAINEL, top: 0 },
    { input: linha, left: PAINEL - 1, top: 0 },
    { input: logo, left: Math.round((PAINEL - lm.width) / 2), top: Math.round((H - lm.height) / 2) },
  ])
  .jpeg({ quality: 86, mozjpeg: true })
  .toFile(path.join(raiz, 'public', 'og', 'home.jpg'));

console.log('public/og/home.jpg gerado (1200x630)');
