# Portfólio, crops e lightbox

## Grid

- Desktop: 2×2 (ou 2 colunas) para dar escala às imagens. Mobile: 1 coluna.
- Uma proporção por grid (ex.: `aspect-ratio: 4 / 3` ou `3 / 2`). Cards da mesma linha com a mesma altura.
- Título do projeto, categoria (badge só se ajudar a filtrar) e local/ano — só dados reais.
- CTA "Visitar site" apenas quando existir URL real do projeto.

## Crops

```css
.projeto img {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  object-position: var(--foco, 50% 50%);
}
```

```html
<img src="/img/casa-aria-fachada.webp" alt="Casa Aria, fachada ao entardecer"
     width="1600" height="1200" style="--foco: 50% 70%" loading="lazy" decoding="async">
```

- Defina `--foco` **foto a foto**: o ponto principal da obra (porta, volume, sala) nunca é cortado.
- Foto vertical em grid horizontal: escolha outro enquadramento, outra foto, ou `object-fit: contain` com fundo neutro da paleta — nunca um crop que mutile.
- Mobile com enquadramento diferente: `<picture>` com `<source media="(max-width: 600px)">` apontando para um crop próprio.
- Confira cada crop nas capturas do QA (celular e desktop).
- Créditos do fotógrafo quando o cliente informar.

## Lightbox (HTML nativo `<dialog>`)

O `<dialog>` com `showModal()` já entrega: Esc fecha, fundo inerte, foco preso dentro e devolvido ao elemento que abriu. Falta acrescentar: clique fora, setas, trava de rolagem e swipe.

```html
<ul class="galeria">
  <li><button class="thumb" data-full="/img/casa-aria-1.webp" data-legenda="Casa Aria — fachada">
        <img src="/img/casa-aria-1-thumb.webp" alt="Casa Aria — fachada" width="800" height="600" loading="lazy">
      </button></li>
  <!-- … -->
</ul>

<dialog id="lightbox" aria-label="Imagem ampliada">
  <figure>
    <img id="lb-img" alt="">
    <figcaption id="lb-legenda"></figcaption>
  </figure>
  <button class="lb-prev" aria-label="Imagem anterior">‹</button>
  <button class="lb-next" aria-label="Próxima imagem">›</button>
  <button class="lb-fechar" aria-label="Fechar">×</button>
</dialog>
```

```css
#lightbox { padding: 0; border: 0; max-width: 100vw; max-height: 100dvh; background: transparent; }
#lightbox::backdrop { background: rgb(0 0 0 / .88); }
#lightbox img { max-width: 92vw; max-height: 86dvh; object-fit: contain; display: block; }
#lightbox button { min-width: 44px; min-height: 44px; }
body:has(#lightbox[open]) { overflow: hidden; }
```

```js
(() => {
  const dlg = document.getElementById('lightbox');
  const img = document.getElementById('lb-img');
  const leg = document.getElementById('lb-legenda');
  const thumbs = [...document.querySelectorAll('.galeria .thumb')];
  let i = 0;
  const show = (n) => {
    i = (n + thumbs.length) % thumbs.length;
    img.src = thumbs[i].dataset.full;
    img.alt = thumbs[i].dataset.legenda || '';
    leg.textContent = thumbs[i].dataset.legenda || '';
  };
  thumbs.forEach((t, n) => t.addEventListener('click', () => { show(n); dlg.showModal(); }));
  dlg.querySelector('.lb-fechar').addEventListener('click', () => dlg.close());
  dlg.querySelector('.lb-prev').addEventListener('click', () => show(i - 1));
  dlg.querySelector('.lb-next').addEventListener('click', () => show(i + 1));
  dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });   // clique fora (no backdrop)
  dlg.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') show(i + 1);
    if (e.key === 'ArrowLeft') show(i - 1);
  });
  let x0 = null;                                                                     // swipe no celular
  dlg.addEventListener('touchstart', (e) => { x0 = e.touches[0].clientX; }, { passive: true });
  dlg.addEventListener('touchend', (e) => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) show(i + (dx < 0 ? 1 : -1));
    x0 = null;
  });
})();
```

- O clique fora funciona porque o `<dialog>` tem `padding: 0` e o conteúdo não ocupa a área do backdrop: clicar fora da figura cai no próprio `dialog`.
- Em React/Lovable, a mesma lógica vale; carregar o lightbox sob demanda (`React.lazy`) se for pesado.
- Teste no QA: abrir pelo clique e pelo teclado (Enter na miniatura), fechar por X, Esc e clique fora, setas, foco voltando para a miniatura, fundo sem rolar, swipe no celular.
