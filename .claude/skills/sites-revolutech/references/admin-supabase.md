# /admin com Supabase — leads e painel

Consolidado de: projetos RevoluTech (PsiqueDelas, CliniDesk), `supabase/agent-skills` (oficial, MIT — com correções) e documentação do Supabase. Confira a documentação atual do Supabase antes de aplicar em produção: a plataforma muda (chaves, painel, Auth).

## Princípios

- **RLS ligado em toda tabela exposta.** Sem policy = ninguém acessa.
- **Visitante (anon) só insere.** Nunca SELECT, UPDATE ou DELETE para anon.
- **Admin é definido por tabela própria** (ou `app_metadata`), nunca por `user_metadata` (o usuário consegue editar).
- **Cadastro público desligado.** Admins entram por convite. Login anônimo desligado.
- **Chave secreta (service_role / `sb_secret_…`) nunca no front-end.** No Lovable/Vite, tudo com prefixo `VITE_` vai para o navegador — só a chave pública (anon/publishable) pode ter esse prefixo.
- **Honeypot no front não basta:** a chave anon é pública e qualquer um pode chamar a API. Por isso o banco valida (CHECK + policy) e, se houver spam, o envio passa por Edge Function.

## Tabela de leads + policies (modelo testado)

Testado em 08/10/2026 em Postgres 16 simulando os papéis do Supabase (`anon`, `authenticated`, `auth.uid()`): anon insere e não lê, altera nem apaga; anon não consegue gravar `status`; logado não-admin vê 0 linhas; admin lê, muda só `status`/`observacoes` e apaga; ninguém lê `private.admins` direto.

```sql
-- 1) Tabela
create table public.leads (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  nome text not null check (char_length(nome) between 2 and 120),
  email text check (email is null or email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
  telefone text check (telefone is null or char_length(telefone) between 8 and 20),
  mensagem text check (mensagem is null or char_length(mensagem) <= 2000),
  consentimento boolean not null check (consentimento),
  consentimento_versao text not null check (char_length(consentimento_versao) <= 40),
  origem text check (origem is null or char_length(origem) <= 200),
  status text not null default 'novo' check (status in ('novo', 'em_contato', 'convertido', 'descartado')),
  observacoes text
);

alter table public.leads enable row level security;

-- 2) Visitante: só INSERT, só nas colunas do formulário
revoke all on public.leads from anon, authenticated;
grant insert (nome, email, telefone, mensagem, consentimento, consentimento_versao, origem)
  on public.leads to anon;

create policy "visitante envia lead"
  on public.leads for insert to anon
  with check (consentimento = true);

-- 3) Admins: tabela fora do schema público
create schema if not exists private;
create table private.admins (
  user_id uuid primary key references auth.users (id) on delete cascade
);

create or replace function private.is_admin()
returns boolean
language sql stable security definer
set search_path = ''
as $$
  select exists (select 1 from private.admins where user_id = (select auth.uid()));
$$;

revoke all on function private.is_admin() from public;
grant usage on schema private to authenticated;
grant execute on function private.is_admin() to authenticated;

-- 4) Admin lê, atualiza status/observações e apaga
grant select, delete on public.leads to authenticated;
grant update (status, observacoes) on public.leads to authenticated;

create policy "admin lê leads" on public.leads
  for select to authenticated using ((select private.is_admin()));
create policy "admin atualiza leads" on public.leads
  for update to authenticated using ((select private.is_admin())) with check ((select private.is_admin()));
create policy "admin apaga leads" on public.leads
  for delete to authenticated using ((select private.is_admin()));

-- 5) Cadastrar um admin (rodar no SQL Editor, com o id do usuário convidado)
-- insert into private.admins (user_id) values ('UUID-DO-USUARIO');
```

Por que assim:

- `grant insert (colunas)` impede o visitante de mandar `status`, `observacoes` ou `created_at` falsos.
- A função `is_admin()` é `security definer` com `search_path = ''` e fica no schema `private` (não exposto pela API). O papel `authenticated` precisa de `USAGE` no schema e `EXECUTE` na função — a policy roda com o papel de quem consulta.
- `(select private.is_admin())` em volta da função faz o Postgres calcular uma vez por consulta, não por linha.
- Usuário logado que não é admin vê **zero** linhas.

## Front-end

- Inserir sem pedir retorno: `supabase.from('leads').insert({...})` **sem** `.select()` — o visitante não tem permissão de leitura, e `.select()` faria a inserção falhar.
- Gravar `consentimento: true` e `consentimento_versao: '2026-10-v1'` (a versão do texto exibido).
- Honeypot preenchido → não chamar o Supabase; mostrar sucesso.
- Exportação CSV no /admin feita com a sessão do admin (passa pelo RLS), nunca com a chave secreta.

## Spam e abuso

Se aparecer spam (ou o cliente tiver volume), mover o envio para uma **Edge Function**:

1. O formulário chama a função, não a tabela.
2. A função valida honeypot, tamanho dos campos e um captcha invisível (ex.: Cloudflare Turnstile) e aplica limite por IP.
3. Só então insere com a chave secreta (que vive apenas na função).
4. Remover o `grant insert` do anon.

`[VERIFICAR]` a documentação atual do Supabase e do captcha escolhido antes de implementar.

## /admin no site

- Rota `/admin` com login (e-mail + senha ou link mágico); aceita colar senha e gerenciador de senhas.
- `<meta name="robots" content="noindex, nofollow">` e `Disallow: /admin` no robots.txt.
- Fora do sitemap e sem link no menu público.
- Tabela acessível: `<th scope="col">`, filtros com label, status com texto (não só cor), foco visível.
- Desktop e mobile também valem aqui (lista em cards no celular, se a tabela não couber).

## QA com evidência (antes de entregar)

Com a **chave anon** (ex.: no console do navegador, em preview):

- [ ] INSERT com consentimento `true` funciona.
- [ ] INSERT com consentimento `false` ou nome vazio é recusado.
- [ ] SELECT, UPDATE e DELETE são negados (SELECT retorna vazio ou erro).
- [ ] INSERT tentando gravar `status` é recusado.

Com um **usuário logado que não é admin**:

- [ ] SELECT retorna 0 linhas; UPDATE/DELETE não afetam nada.

Com o **admin**:

- [ ] Lista, filtra, atualiza status e exporta CSV.

E também:

- [ ] Security Advisor do Supabase sem alertas críticos.
- [ ] Busca por `service_role` e `sb_secret` no build/bundle sem resultado.
- [ ] Cadastro público e login anônimo desligados no painel do Auth.
