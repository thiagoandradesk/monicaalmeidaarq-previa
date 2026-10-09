/**
 * Botão flutuante de WhatsApp (só em telas largas, via CSS): aparece depois que o
 * hero sai da tela e some quando a seção de contato (que já tem o botão) está
 * visível, para nunca cobrir CTA nem texto.
 */
export function iniciarWhatsFlutuante(): void {
  const botao = document.getElementById('whats-flutuante');
  const hero = document.querySelector('.hero');
  const contato = document.getElementById('contato');
  if (!botao || !hero || !contato || !('IntersectionObserver' in window)) return;

  let heroVisivel = true;
  let contatoVisivel = false;
  const aplicar = () => botao.toggleAttribute('data-visivel', !heroVisivel && !contatoVisivel);

  new IntersectionObserver(
    (entradas) => {
      heroVisivel = entradas[0].isIntersecting;
      aplicar();
    },
    { threshold: 0.05 },
  ).observe(hero);

  new IntersectionObserver(
    (entradas) => {
      contatoVisivel = entradas[0].isIntersecting;
      aplicar();
    },
    { threshold: 0.05 },
  ).observe(contato);
}
