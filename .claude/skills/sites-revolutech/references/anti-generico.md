# Anti-genérico — o que denuncia site feito por IA ou template

Consolidado de: experiência da RevoluTech (contexto §9.1), `frontend-design` (Anthropic, Apache-2.0), Impeccable (Paul Bakaus, Apache-2.0), Genjutsu (MIT) e `web-artifacts-builder` (Anthropic). Reescrito e adaptado para sites de pequenos negócios brasileiros.

Use esta lista **antes de codar** (na tese visual) e **no QA** (olhando as capturas). Cada item é recusado por padrão; só entra com motivo ligado ao negócio do cliente.

## Estrutura e layout

- Grade de cards ícone + título + texto como espinha do site ("3 benefícios", "4 serviços" em cards iguais).
- Cards dentro de cards.
- Hero de métricas ("+500 clientes · 98% satisfação · 10 anos") — e números sem fonte são proibidos de qualquer forma.
- Tudo centralizado, seção após seção, com a mesma largura e o mesmo ritmo.
- Eyebrow/kicker em caixa-alta acima de todo título ("NOSSOS SERVIÇOS").
- Numeração 01 / 02 / 03 quando o conteúdo não é uma sequência real.
- Destaque colorido em uma palavra de cada título.
- Raio de borda igual em tudo, sombra suave igual em tudo.
- Seção de depoimentos inventados; logos de "clientes" sem autorização.
- Faixa de "confiança" com selos genéricos.
- Rodapé gigante com colunas de links que não existem.

## Cor e superfície

- Gradiente roxo/azul "tech" sem relação com a marca; texto em gradiente.
- Vidro fosco (glassmorphism) decorativo.
- Borda lateral colorida grossa em cards ("acento" de 4 px à esquerda).
- Sombra dura deslocada estilo neobrutalismo sem motivo.
- Paleta escolhida pela categoria em vez da marca (ver teste da categoria).
- Texto secundário cinza neutro sobre fundo colorido — tinja o cinza com o matiz do fundo.
- Claro ou escuro escolhido por moda; decida pela cena real de uso (quem acessa, onde, quando).

## Tipografia

- Fontes batidas usadas sem justificativa: Inter como display, Playfair, Cormorant, Fraunces, Lora, DM Sans/Serif, Plus Jakarta, Outfit, Space Grotesk, Poppins. Podem ser usadas — com motivo.
- Monoespaçada como "fantasia tech".
- Mais de 2 famílias.
- Tracking muito negativo em títulos (abaixo de −0,04em) ou caixa-alta espaçada em todo rótulo.
- Linhas de texto com mais de ~80 caracteres.
- Fonte carregada de CDN externo quando pode ser hospedada no site.

## Imagem

- Banco de imagem genérico (aperto de mão, equipe sorrindo no notebook, prédio de vidro).
- Ilustração 3D genérica, blob, emoji no lugar de ícone.
- Ícone genérico para cada item da lista.
- Foto do cliente substituída por geração "mais bonita".
- Crop que corta o ponto principal da foto.

## Motion

- Mesmo fade-up em toda seção ao rolar.
- Bounce, elastic, parallax em tudo.
- Animação que esconde conteúdo até o JavaScript carregar.
- Cursor customizado, partículas, efeito "porque dá".
- Um momento autoral bem feito vale mais que dez efeitos.

## Texto (PT-BR)

Recuse e reescreva:

- Jargão de agência: "soluções inovadoras", "transforme sua presença digital", "leve seu negócio ao próximo nível", "excelência e compromisso", "qualidade e confiança", "seu sucesso é nossa missão".
- Estruturas típicas de IA: "Não é X, é Y."; "Sem X, sem Y, sem Z."; pergunta retórica que se responde na frase seguinte; tríades em todo parágrafo; travessão em todo título.
- Promessas vagas ou não comprováveis: "os melhores", "referência no mercado", "resultados garantidos".
- Urgência falsa: "últimas vagas", "só hoje", contadores.
- Frase que serviria para o concorrente (teste da troca).
- CTA vago: "Saiba mais", "Clique aqui". Prefira o que acontece: "Ver projetos", "Falar no WhatsApp".

Texto bom é específico: nome do bairro, tipo de obra, quem atende, como funciona o primeiro contato, prazo real.

## Calibração final

Antes de apresentar, pergunte:

1. Se eu tirar o logo, dá para saber de quem é o site?
2. Uma pessoa que nunca viu o negócio entende o que é e o que fazer em 5 segundos, no celular?
3. Tem algo nesta página que o cliente não disse ou não comprovou?
4. Qual é o único momento memorável? Ele serve ao negócio?
5. Algum item desta lista aparece sem motivo?
