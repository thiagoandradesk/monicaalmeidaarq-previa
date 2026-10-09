/**
 * Formulário de demonstração da prévia: valida de verdade (ao sair do campo e no
 * envio), mantém o que foi digitado, foca o primeiro erro e, em vez de enviar,
 * mostra a mensagem combinada. Honeypot preenchido -> "sucesso" silencioso.
 * Nada é enviado a lugar nenhum nesta prévia.
 */
const MENSAGEM_PREVIA = 'Esta é uma prévia. No site final, sua mensagem chega direto no seu painel de contatos.';

type Campo = HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement;

const regras: Record<string, (c: Campo) => string> = {
  nome: (c) => {
    const v = c.value.trim();
    if (!v) return 'Informe seu nome.';
    if (v.length < 2) return 'O nome precisa ter pelo menos 2 letras.';
    return '';
  },
  whatsapp: (c) => {
    const d = c.value.replace(/\D/g, '');
    if (!d) return 'Informe seu WhatsApp com DDD, por exemplo (49) 99999-9999.';
    if (d.length < 10 || d.length > 13) return 'Confira o número: use DDD + número, só dígitos contam.';
    return '';
  },
  email: (c) => {
    const v = c.value.trim();
    if (!v) return '';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) return 'Confira o e-mail: faltou o @ ou o domínio.';
    return '';
  },
  mensagem: (c) => {
    const v = c.value.trim();
    if (!v) return 'Conte, em poucas linhas, sobre o seu espaço.';
    if (v.length < 10) return 'A mensagem precisa ter pelo menos 10 caracteres.';
    return '';
  },
  consentimento: (c) => ((c as HTMLInputElement).checked ? '' : 'Para enviar, é preciso autorizar o uso dos dados para o retorno.'),
};

export function iniciarFormulario(): void {
  const form = document.getElementById('formulario') as HTMLFormElement | null;
  if (!form) return;
  const retorno = form.querySelector<HTMLElement>('#formulario-retorno');
  const botao = form.querySelector<HTMLButtonElement>('.formulario__enviar');
  const campos = Array.from(form.querySelectorAll<Campo>('input, select, textarea')).filter((c) => c.name in regras);

  const erroDe = (c: Campo) => document.getElementById(`erro-${c.name}`);

  const validar = (c: Campo): boolean => {
    const msg = regras[c.name](c);
    const el = erroDe(c);
    if (el) el.textContent = msg;
    if (msg) c.setAttribute('aria-invalid', 'true');
    else c.removeAttribute('aria-invalid');
    return !msg;
  };

  campos.forEach((c) => {
    c.addEventListener('blur', () => validar(c));
    // depois de marcado com erro, limpa assim que ficar válido (sem validar a cada tecla antes disso)
    c.addEventListener('input', () => {
      if (c.getAttribute('aria-invalid') === 'true') validar(c);
    });
    if (c.type === 'checkbox') c.addEventListener('change', () => validar(c));
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!retorno || !botao) return;

    const hp = form.querySelector<HTMLInputElement>('input[name="website"]');
    if (hp && hp.value.trim()) {
      // robô: responde como sucesso e descarta
      retorno.textContent = MENSAGEM_PREVIA;
      retorno.hidden = false;
      return;
    }

    const invalidos = campos.filter((c) => !validar(c));
    if (invalidos.length) {
      invalidos[0].focus();
      return;
    }

    botao.disabled = true;
    const rotulo = botao.textContent;
    botao.textContent = 'Enviando…';
    window.setTimeout(() => {
      botao.disabled = false;
      botao.textContent = rotulo;
      retorno.textContent = MENSAGEM_PREVIA;
      retorno.hidden = false;
      retorno.focus();
    }, 500);
  });
}
