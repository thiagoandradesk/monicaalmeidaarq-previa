/**
 * Menu mobile acessível: botão com nome, aria-expanded, Esc fecha, foco volta ao
 * botão, foco preso dentro do header enquanto aberto, scroll do fundo travado e
 * conteúdo de trás inerte.
 */
const FOCAVEIS = 'a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])';

export function iniciarMenu(): void {
  const botao = document.querySelector<HTMLButtonElement>('.menu-botao');
  const menu = document.getElementById('menu');
  const topo = document.getElementById('topo');
  if (!botao || !menu || !topo) return;

  const mq = window.matchMedia('(max-width: 59.99rem)');
  const fora = () => [document.getElementById('conteudo'), document.querySelector('footer'), document.getElementById('whats-flutuante')];

  const abrir = () => {
    menu.setAttribute('data-aberto', '');
    botao.setAttribute('aria-expanded', 'true');
    botao.setAttribute('aria-label', 'Fechar menu');
    document.body.setAttribute('data-menu-aberto', '');
    fora().forEach((el) => el?.setAttribute('inert', ''));
    const primeiro = menu.querySelector<HTMLElement>(FOCAVEIS);
    primeiro?.focus();
  };

  const fechar = (devolverFoco = true) => {
    if (!menu.hasAttribute('data-aberto')) return;
    menu.removeAttribute('data-aberto');
    botao.setAttribute('aria-expanded', 'false');
    botao.setAttribute('aria-label', 'Abrir menu');
    document.body.removeAttribute('data-menu-aberto');
    fora().forEach((el) => el?.removeAttribute('inert'));
    if (devolverFoco) botao.focus();
  };

  botao.addEventListener('click', () => (menu.hasAttribute('data-aberto') ? fechar() : abrir()));

  // link do menu: fecha e deixa a âncora rolar
  menu.addEventListener('click', (e) => {
    const alvo = e.target as HTMLElement;
    if (alvo.closest('a[href^="#"]')) fechar(false);
  });

  topo.addEventListener('keydown', (e) => {
    if (!menu.hasAttribute('data-aberto')) return;
    if (e.key === 'Escape') {
      e.preventDefault();
      fechar();
      return;
    }
    if (e.key === 'Tab') {
      const focaveis = [botao, ...Array.from(menu.querySelectorAll<HTMLElement>(FOCAVEIS))];
      const primeiro = focaveis[0];
      const ultimo = focaveis[focaveis.length - 1];
      if (e.shiftKey && document.activeElement === primeiro) {
        e.preventDefault();
        ultimo.focus();
      } else if (!e.shiftKey && document.activeElement === ultimo) {
        e.preventDefault();
        primeiro.focus();
      }
    }
  });

  // ao crescer para desktop, garante estado limpo
  mq.addEventListener('change', (ev) => {
    if (!ev.matches) fechar(false);
  });
}
