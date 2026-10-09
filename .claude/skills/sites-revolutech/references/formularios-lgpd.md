# Formulários, LGPD, honeypot, /obrigado e WhatsApp

A RevoluTech não presta assessoria jurídica. Os textos legais (Política de Privacidade, termo de consentimento) são validados pelo cliente. A skill garante a estrutura técnica e os pontos mínimos.

## Formulário

- Uma coluna. Pedir só o necessário (nome + um contato + mensagem curta costuma bastar).
- Label visível em todo campo, associado por `for`/`id`. Placeholder não substitui label.
- Tipos e preenchimento automático:

| Campo | Atributos |
|---|---|
| Nome | `autocomplete="name"` |
| E-mail | `type="email" autocomplete="email" inputmode="email"` |
| Telefone/WhatsApp | `type="tel" autocomplete="tel" inputmode="tel"` |
| Mensagem | `<textarea>` com `maxlength` |

- Fonte dos campos ≥ 16 px; altura ≥ 44 px.
- Validação ao sair do campo (não a cada tecla). Erro em texto, ao lado do campo, ligado por `aria-describedby`, dizendo o problema e como resolver. Nunca apagar o que foi digitado. Ao enviar com erro, foco no primeiro campo com erro.
- Botão com verbo específico ("Enviar mensagem") e estado de envio (desabilita + "Enviando…") para evitar duplo envio.
- Ao lado do formulário: o que acontece depois (prazo real de resposta) e o WhatsApp como alternativa.
- Nada de colar bloqueado, campo de confirmação de e-mail, captcha visual chato (usar invisível se necessário).

## Consentimento LGPD

- Checkbox **não pré-marcado**, obrigatório para enviar, com texto curto e link para a Política de Privacidade:

```html
<label class="consentimento">
  <input type="checkbox" name="consentimento" required>
  Autorizo o uso dos meus dados para retorno deste contato, conforme a
  <a href="/politica-de-privacidade/" target="_blank" rel="noopener">Política de Privacidade</a>.
</label>
```

- Registrar junto do lead: data/hora do envio e a versão do texto de consentimento (ex.: `"2026-10-v1"`).
- Finalidade única: responder ao contato. Marketing por e-mail/WhatsApp precisa de consentimento separado e opcional.
- Nada de enriquecimento de leads (Clay, Apollo etc.) nem envio a terceiros não informados.
- Analytics e pixel que usam cookies: aviso/consentimento de cookies antes de carregar. `[VERIFICAR]` orientação atual da ANPD para o caso do cliente.

### Política de Privacidade — pontos mínimos (texto validado pelo cliente)

- Quem é o controlador (nome/razão social e contato).
- Quais dados são coletados (formulário, e cookies se houver).
- Para quê (finalidade) e com qual base legal.
- Com quem são compartilhados (provedores: hospedagem, banco de dados, e-mail — ex.: Vercel, Supabase), incluindo armazenamento fora do Brasil quando houver.
- Por quanto tempo são guardados.
- Direitos do titular (acesso, correção, exclusão, revogação do consentimento) e como exercê-los.
- Canal de contato do encarregado/responsável.
- Data da última atualização.

## Honeypot

```html
<div class="hp" aria-hidden="true">
  <label for="website">Não preencha este campo</label>
  <input id="website" name="website" type="text" tabindex="-1" autocomplete="off">
</div>
```

```css
.hp { position: absolute; left: -9999px; width: 1px; height: 1px; overflow: hidden; }
```

- Não use `display: none` (alguns robôs ignoram campos ocultos assim) nem `type="hidden"`.
- Se `website` vier preenchido: responder como sucesso e **descartar** o envio, sem avisar o robô.
- O honeypot só filtra robôs simples que usam o formulário. Quem chama a API direto (a chave anon do Supabase é pública) passa por cima — a proteção real fica no servidor (ver `admin-supabase.md`).

## Página /obrigado

- Rota própria (`/obrigado/`), aberta após o envio com sucesso.
- `<meta name="robots" content="noindex, follow">`, fora do sitemap, **sem** `Disallow` no robots.txt.
- Conteúdo: confirma o recebimento, diz o que acontece agora e quando, oferece o WhatsApp e um caminho de volta (home ou portfólio).
- É o ponto de medição de conversão (evento de analytics/pixel com consentimento).
- Não exibir os dados enviados na URL (nada de `?nome=…&telefone=…`).

## WhatsApp

- Link: `https://wa.me/55{DDD}{número}?text={mensagem codificada}` — só dígitos, com 55.
- Mensagem pré-preenchida curta e específica: "Olá, vim pelo site e gostaria de falar sobre…". Codificar com `encodeURIComponent`.
- Número confirmado pelo cliente; enquanto não confirmar, `[VERIFICAR]` e não publicar.
- Botão flutuante: nome acessível (`aria-label="Falar no WhatsApp"`), ≥ 44 px, respeitando `env(safe-area-inset-bottom)`, sem cobrir CTA ou rodapé.

## Testes (sempre em preview)

- Enviar o formulário com dados de teste **no preview**, nunca em produção com o banco real do cliente — se precisar testar em produção, combinar com o cliente e apagar o lead de teste.
- Conferir: chegada do lead no destino (painel, e-mail), /obrigado, honeypot descartando, consentimento obrigatório, erros por campo, envio duplo bloqueado.
