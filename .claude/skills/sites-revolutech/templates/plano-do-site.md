# Plano do site — <Cliente> · v<N>

> Fonte da verdade do projeto. Itens **[LOCKED]** não mudam sem aprovação explícita. Tudo que não foi confirmado pelo cliente fica como `[VERIFICAR]` e não vai para produção.
> Etapas: Briefing ☐ · Estrutura ☐ · Direção visual ☐ · Desenvolvimento ☐ · Conteúdo/SEO/LGPD ☐ · QA preview ☐ · OK Thiago ☐ · Produção ☐ · QA produção ☐

---

## 1. Briefing

- **Cliente / negócio:**
- **Pacote contratado:** (Essencial · Institucional · Landing Page · personalizado) — escopo conforme contexto
- **Objetivo principal do site:** (contato pelo WhatsApp, agendamento, portfólio, captação de leads…)
- **Público e como chega:** (Instagram, Google, indicação…)
- **Diferenciais reais (ditos pelo cliente):**
- **Concorrentes / referências que o cliente citou:** (o que gosta e o que não quer)
- **Restrições:** (conselho profissional — CRP/CAU/…, o que não pode aparecer, LGPD)
- **Domínio:** (já tem? onde está o DNS?)
- **Contato oficial:** WhatsApp `[VERIFICAR]` · e-mail · Instagram · endereço (publicar ou não?)

## 2. Inventário de assets

| ID | Asset | Procedência (cliente / existente / criado / IA com OK / procedural) | Arquivo | Status |
|---|---|---|---|---|
| A1 | Logo | cliente | | |

- **Paleta medida** (`extrair_paleta.py`): HEX + % + contraste
- **Fontes:** (da marca? licença?)
- **Faltando:** (lista com `[VERIFICAR]`)

## 3. Estrutura

| Página | URL | Objetivo | Seções | CTA principal |
|---|---|---|---|---|
| Home | `/` | | | |
| Obrigado | `/obrigado/` | confirmar envio | — | voltar / WhatsApp |
| Privacidade | `/politica-de-privacidade/` | LGPD | — | — |

Menu (4–7 itens):

## 4. Direção visual

- **Modo:** (Persuadir · Experiência · Operar · Ler)
- **Tese visual (5 linhas):**
  1. Cor:
  2. Tipografia:
  3. Layout/grid:
  4. Imagem:
  5. Momento de motion:
- **Teste da categoria / da troca / da primeira dobra:** (anotar o resultado)
- **Itens da lista anti-genérico usados de propósito e por quê:**

## 5. Técnico

- **Stack:** (Lovable + Supabase · Vite/React · Next.js · HTML estático)
- **Repositório:** · **Projeto Vercel:** · **URL de preview:**
- **Formulário:** destino (Supabase / e-mail / Edge Function) · versão do consentimento
- **/admin:** sim/não · admins convidados
- **Analytics/pixel:** sim/não · aviso de cookies

## 6. SEO

| Página | Title (50–60) | Description (150–160) | OG image |
|---|---|---|---|

- JSON-LD: tipo · dados confirmados
- robots.txt · sitemap.xml · 404

## 7. QA

| Data | Ambiente | Alertas do script | Revisão das capturas | Pendências |
|---|---|---|---|---|

## 8. Registro de decisões e LOCKED

| Data | Decisão / item LOCKED | Aprovado por | Motivo |
|---|---|---|---|
