/**
 * Único momento de motion da página: uma linha fina caramelo se desenha ligando
 * os 5 pontos do percurso do paciente conforme a rolagem.
 *
 * - Sem JS: o CSS já mostra a linha pronta e os pontos cheios.
 * - Com prefers-reduced-motion: a linha aparece pronta (sem animação).
 * - A geometria é medida no DOM (centro de cada ponto), então funciona em
 *   qualquer largura; recalcula em resize.
 */
export function iniciarPercurso(): void {
  const raiz = document.getElementById('percurso');
  const svg = raiz?.querySelector<SVGSVGElement>('.percurso__linha');
  const traco = raiz?.querySelector<SVGPathElement>('.percurso__traco');
  const itens = raiz ? Array.from(raiz.querySelectorAll<HTMLElement>('.percurso__item')) : [];
  const pontos = itens.map((li) => li.querySelector<HTMLElement>('.percurso__ponto'));
  if (!raiz || !svg || !traco || itens.length < 2 || pontos.some((p) => !p)) return;

  const reduzido = window.matchMedia('(prefers-reduced-motion: reduce)');
  let comprimento = 0;
  let centros: number[] = []; // y relativo ao raiz
  let ticking = false;

  const medir = () => {
    const r = raiz.getBoundingClientRect();
    svg.setAttribute('viewBox', `0 0 ${r.width} ${r.height}`);
    svg.setAttribute('width', String(r.width));
    svg.setAttribute('height', String(r.height));
    const pts = pontos.map((p) => {
      const b = p!.getBoundingClientRect();
      return { x: b.left - r.left + b.width / 2, y: b.top - r.top + b.height / 2 };
    });
    centros = pts.map((p) => p.y);
    // começa um pouco acima do primeiro ponto e termina no último
    const d = [`M ${pts[0].x} ${Math.max(0, pts[0].y - 48)}`, ...pts.map((p) => `L ${p.x} ${p.y}`)].join(' ');
    traco.setAttribute('d', d);
    comprimento = traco.getTotalLength();
    traco.style.setProperty('--comprimento', String(comprimento));
    atualizar();
  };

  const atualizar = () => {
    ticking = false;
    if (reduzido.matches) {
      traco.style.setProperty('--restante', '0');
      itens.forEach((li) => li.classList.add('is-ativo'));
      return;
    }
    const r = raiz.getBoundingClientRect();
    // a "frente" da linha é a altura em que o olhar costuma estar: 72% da viewport
    const frente = window.innerHeight * 0.72 - r.top;
    const fim = centros[centros.length - 1];
    const progresso = Math.min(1, Math.max(0, frente / fim));
    traco.style.setProperty('--restante', String(comprimento * (1 - progresso)));
    itens.forEach((li, n) => li.classList.toggle('is-ativo', frente >= centros[n] - 4));
  };

  const aoRolar = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(atualizar);
  };

  document.documentElement.classList.add('js-motion');
  medir();
  window.addEventListener('scroll', aoRolar, { passive: true });
  window.addEventListener('resize', medir);
  if ('ResizeObserver' in window) new ResizeObserver(medir).observe(raiz);
  reduzido.addEventListener('change', atualizar);
  // fontes carregadas mudam a altura dos itens
  document.fonts?.ready.then(medir);
}
