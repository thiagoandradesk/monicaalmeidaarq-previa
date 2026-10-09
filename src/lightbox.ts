/**
 * Lightbox com <dialog> nativo (Esc fecha, fundo inerte, foco preso e devolvido),
 * mais: clique fora, setas, swipe, legenda, contador e scroll do fundo travado (CSS).
 * Cada projeto carrega suas imagens num <script type="application/json">.
 */
const PLACEHOLDER = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';

type Imagem = { base: string; max: number; alt: string };
type Galeria = { titulo: string; imagens: Imagem[] };

export function iniciarLightbox(): void {
  const dlg = document.getElementById('lightbox') as HTMLDialogElement | null;
  const img = document.getElementById('lb-img') as HTMLImageElement | null;
  const legenda = document.getElementById('lb-legenda');
  const contador = document.getElementById('lb-contador');
  if (!dlg || !img || !legenda || !contador || typeof dlg.showModal !== 'function') return;

  const galerias = new Map<string, Galeria>();
  document.querySelectorAll<HTMLElement>('.projeto[data-galeria]').forEach((art) => {
    const dados = art.querySelector<HTMLScriptElement>('.projeto__dados');
    const titulo = art.querySelector('.projeto__tipo')?.textContent?.trim() ?? '';
    if (!dados) return;
    try {
      galerias.set(art.dataset.galeria!, { titulo, imagens: JSON.parse(dados.textContent || '[]') });
    } catch {
      /* JSON inválido: projeto fica sem lightbox */
    }
  });

  let atual: Galeria | null = null;
  let i = 0;
  let origem: HTMLElement | null = null;

  const srcDe = (im: Imagem, largura: number) => `/img/${im.base}-${largura}.webp`;

  const mostrar = (n: number) => {
    if (!atual) return;
    const total = atual.imagens.length;
    i = ((n % total) + total) % total;
    const im = atual.imagens[i];
    img.src = srcDe(im, im.max);
    img.srcset = `${srcDe(im, 960)} 960w, ${srcDe(im, im.max)} ${im.max}w`;
    img.sizes = '92vw';
    img.alt = im.alt;
    legenda.textContent = im.alt;
    contador.textContent = total > 1 ? `${atual.titulo} · ${i + 1} de ${total}` : atual.titulo;
    // pré-carrega a próxima
    if (total > 1) {
      const prox = atual.imagens[(i + 1) % total];
      const pre = new Image();
      pre.src = srcDe(prox, prox.max);
    }
  };

  const abrir = (id: string, indice: number, quemAbriu: HTMLElement) => {
    const g = galerias.get(id);
    if (!g || !g.imagens.length) return;
    atual = g;
    origem = quemAbriu;
    dlg.toggleAttribute('data-unica', g.imagens.length === 1);
    mostrar(indice);
    dlg.showModal();
    dlg.querySelector<HTMLButtonElement>('.lightbox__fechar')?.focus();
  };

  document.querySelectorAll<HTMLButtonElement>('[data-abrir]').forEach((b) => {
    b.addEventListener('click', () => abrir(b.dataset.abrir!, Number(b.dataset.indice || 0), b));
  });

  dlg.querySelector('.lightbox__fechar')?.addEventListener('click', () => dlg.close());
  dlg.querySelector('.lightbox__anterior')?.addEventListener('click', () => mostrar(i - 1));
  dlg.querySelector('.lightbox__proxima')?.addEventListener('click', () => mostrar(i + 1));

  // clique fora da figura (no próprio dialog, que cobre a tela)
  dlg.addEventListener('click', (e) => {
    const alvo = e.target as HTMLElement;
    if (alvo === dlg || alvo.classList.contains('lightbox__figura')) dlg.close();
  });

  dlg.addEventListener('keydown', (e) => {
    if (!atual || atual.imagens.length < 2) return;
    if (e.key === 'ArrowRight') {
      e.preventDefault();
      mostrar(i + 1);
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      mostrar(i - 1);
    }
  });

  // swipe no celular
  let x0: number | null = null;
  dlg.addEventListener('touchstart', (e) => (x0 = e.touches[0].clientX), { passive: true });
  dlg.addEventListener('touchend', (e) => {
    if (x0 === null || !atual || atual.imagens.length < 2) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) mostrar(i + (dx < 0 ? 1 : -1));
    x0 = null;
  });

  dlg.addEventListener('close', () => {
    img.removeAttribute('srcset');
    img.src = PLACEHOLDER;
    origem?.focus();
    origem = null;
    atual = null;
  });
}
