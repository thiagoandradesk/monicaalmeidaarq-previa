# Publicação — GitHub → Vercel → domínio

Fluxo da RevoluTech: **Claude Code → GitHub → Vercel → domínio (DNS na Hostinger)**. Lovable publica pelo próprio painel ou exporta para GitHub. Confira a documentação atual da Vercel e da Hostinger antes de mexer em DNS — telas e valores mudam.

## Regras

- **Preview é livre; produção só com OK explícito do Thiago.**
- Trabalhe em branch (`site/ajuste-hero`), não direto na `main` quando a `main` publica em produção.
- `git add` só dos arquivos alterados, nomeados — nunca `git add .` sem olhar o `git status`.
- Nunca subir `.env`, chaves, `.vercel/`, fotos não aprovadas, backups ou `node_modules`. Conferir o `.gitignore`.
- **Nunca deploy anônimo** ou em conta/projeto que não seja o do cliente/RevoluTech. Nunca instalar CLI global ou criar projeto Vercel sem avisar.
- Depois de qualquer deploy: abrir a URL e rodar `scripts/qa_site.py` contra ela. "Deploy concluído" não é QA.

## Checklist de lançamento

**Antes**
- [ ] QA do preview sem alertas (ou alertas justificados) e capturas revisadas.
- [ ] Nenhum `[VERIFICAR]`, texto provisório ou dado de teste no site.
- [ ] Política de Privacidade publicada; formulário testado em preview.
- [ ] `robots.txt` de produção **sem** `Disallow: /` (preview pode bloquear; produção não).
- [ ] `sitemap.xml` com o domínio final.
- [ ] Canonical e `og:url` com o domínio final (não `*.vercel.app`).
- [ ] Favicon, `og:image` 1200×630 e título de cada página.

**Domínio e DNS**
- [ ] Domínio adicionado ao projeto na Vercel; seguir os registros que a Vercel indicar (geralmente registro A para o domínio raiz e CNAME para `www`) — `[VERIFICAR]` no painel da Vercel no momento.
- [ ] Na Hostinger, editar só os registros necessários; anotar os valores antigos antes de trocar.
- [ ] Escolher a versão principal (com ou sem `www`) e redirecionar a outra com 301, em um salto.
- [ ] HTTPS ativo (a Vercel emite o certificado automaticamente após o DNS propagar).
- [ ] E-mail do cliente no mesmo domínio: **não mexer em registros MX/TXT de e-mail** sem saber o que são.

**SPA e 404**
- Rewrite "tudo para `/index.html`" transforma qualquer endereço inexistente em página 200 (soft 404). Prefira: páginas pré-renderizadas (um HTML por rota) ou rewrites só das rotas reais, e um `404.html` que a hospedagem sirva com status 404. `[VERIFICAR]` a configuração atual da Vercel para o framework do projeto.
- Conferir com `qa_site.py` ("rota inexistente responde 404 real").

**Depois**
- [ ] `python3 scripts/qa_site.py https://dominio.com.br --saida qa/<cliente>-prod`.
- [ ] Testar o link no WhatsApp (prévia com imagem e título corretos).
- [ ] Search Console: verificar o domínio, enviar o sitemap, inspecionar a home.
- [ ] Perfil da Empresa no Google com nome, endereço, telefone e site iguais aos do site.
- [ ] Analytics (se contratado) recebendo eventos, inclusive a conversão em `/obrigado`.
- [ ] Registrar no Projeto: URL de produção, repositório, projeto na Vercel e data — sem senhas ou tokens.
- [ ] Garantia técnica de 2 meses começa a contar da publicação.
