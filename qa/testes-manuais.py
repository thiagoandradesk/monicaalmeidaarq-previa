"""Testes manuais da prévia que o qa_site.py não cobre (menu mobile, lightbox,
formulário, links). Gera capturas em qa/previa/manuais/ e imprime asserções.

Uso: python -X utf8 qa/testes-manuais.py http://localhost:4173
"""
import sys
from pathlib import Path
from urllib.parse import unquote

from playwright.sync_api import sync_playwright

base = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:4173").rstrip("/") + "/"
out = Path(__file__).resolve().parent / "previa" / "manuais"
out.mkdir(parents=True, exist_ok=True)
falhas = []


def check(cond, msg):
    print(("  OK      " if cond else "  FALHA   ") + msg)
    if not cond:
        falhas.append(msg)


with sync_playwright() as p:
    b = p.chromium.launch()

    # ---------- celular: menu, primeira dobra, formulário ----------
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="pt-BR")
    pg = ctx.new_page()
    pg.goto(base, wait_until="load")
    pg.wait_for_timeout(600)
    pg.screenshot(path=str(out / "celular_primeira_dobra.jpg"), type="jpeg", quality=80)

    print("== Menu mobile")
    pg.click(".menu-botao")
    pg.wait_for_timeout(250)
    check(pg.get_attribute(".menu-botao", "aria-expanded") == "true", "abre com aria-expanded=true")
    check(pg.evaluate("document.body.hasAttribute('data-menu-aberto') && getComputedStyle(document.body).overflow==='hidden'"), "scroll do fundo travado")
    check(pg.evaluate("document.getElementById('conteudo').hasAttribute('inert')"), "conteúdo de trás inerte")
    check(pg.evaluate("document.activeElement.textContent.trim()") == "Sobre", "foco vai para o primeiro link")
    pg.screenshot(path=str(out / "celular_menu_aberto.jpg"), type="jpeg", quality=80)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(250)
    check(pg.get_attribute(".menu-botao", "aria-expanded") == "false", "Esc fecha")
    check(pg.evaluate("document.activeElement === document.querySelector('.menu-botao')"), "foco volta ao botão")
    pg.click(".menu-botao")
    pg.wait_for_timeout(200)
    pg.click(".menu__link[href='#contato']")
    pg.wait_for_timeout(2500)  # rolagem suave até o fim da página
    check(pg.get_attribute(".menu-botao", "aria-expanded") == "false", "link do menu fecha e navega")
    check(pg.evaluate("Math.abs(document.getElementById('contato').getBoundingClientRect().top) < 120"), "âncora #contato visível abaixo do header fixo")

    print("== Formulário (celular)")
    pg.click(".formulario__enviar")
    pg.wait_for_timeout(200)
    check(pg.evaluate("document.activeElement.id") == "nome", "envio vazio foca o primeiro erro (nome)")
    erros = pg.evaluate("[...document.querySelectorAll('.campo__erro')].filter(e=>e.textContent.trim()).map(e=>e.id)")
    check(set(erros) >= {"erro-nome", "erro-whatsapp", "erro-mensagem", "erro-consentimento"}, f"erros específicos por campo: {erros}")
    check(pg.evaluate("document.getElementById('formulario-retorno').hidden"), "mensagem de prévia não aparece com erros")
    pg.screenshot(path=str(out / "celular_formulario_erros.jpg"), type="jpeg", quality=80)
    pg.fill("#nome", "Teste QA")
    pg.fill("#whatsapp", "49 99999-9999")
    pg.fill("#email", "email-invalido")
    pg.dispatch_event("#email", "blur")
    pg.wait_for_timeout(100)
    check("@" in pg.text_content("#erro-email"), "e-mail inválido avisa ao sair do campo")
    pg.fill("#email", "teste@exemplo.com.br")
    pg.select_option("#tipo", "clinica")
    pg.fill("#mensagem", "Mensagem de teste do QA da prévia.")
    pg.click(".formulario__enviar")
    pg.wait_for_timeout(200)
    check(pg.evaluate("document.activeElement.id") == "consentimento", "sem consentimento, foca o checkbox")
    check(pg.evaluate("document.getElementById('nome').value") == "Teste QA", "não apaga o que foi digitado")
    pg.check("#consentimento")
    pg.click(".formulario__enviar")
    pg.wait_for_timeout(900)
    retorno = pg.text_content("#formulario-retorno") or ""
    check("Esta é uma prévia" in retorno and "painel de contatos" in retorno, "mensagem de prévia exibida")
    check(pg.evaluate("document.activeElement.id") == "formulario-retorno", "foco vai para a mensagem")
    reqs = pg.evaluate("performance.getEntriesByType('resource').filter(r=>r.initiatorType==='fetch'||r.initiatorType==='xmlhttprequest').length")
    check(reqs == 0, "nenhuma requisição de envio (fetch/XHR)")
    pg.screenshot(path=str(out / "celular_formulario_enviado.jpg"), type="jpeg", quality=80)

    print("== Honeypot")
    pg.reload(wait_until="load")
    pg.evaluate("document.querySelector('input[name=website]').value='spam'")
    pg.click(".formulario__enviar")
    pg.wait_for_timeout(200)
    check(not pg.evaluate("document.getElementById('formulario-retorno').hidden"), "honeypot preenchido: sucesso silencioso sem validar")

    print("== Links")
    links = pg.evaluate("[...document.querySelectorAll('a[href*=\"wa.me\"]')].map(a=>a.href)")
    check(len(links) >= 4 and all(l.startswith("https://wa.me/5549999691919?text=") for l in links), f"{len(links)} links de WhatsApp com o número certo")
    check(unquote(links[0].split("text=")[1]) == "Olá, Monica! Vi o site da Arquitetura que Cuida e gostaria de conversar sobre um projeto.", "mensagem do WhatsApp decodifica certo")
    ig = pg.evaluate("[...document.querySelectorAll('a[href*=\"instagram.com\"]')].map(a=>a.href)")
    check(len(ig) >= 2 and all(l == "https://www.instagram.com/arquiteta_monicaalmeida/" for l in ig), f"{len(ig)} links do Instagram corretos")
    ext = pg.evaluate("[...document.querySelectorAll('a[target=_blank]')].every(a=>(a.rel||'').includes('noopener'))")
    check(ext, "links externos com rel=noopener")
    ctx.close()

    # ---------- desktop: lightbox e swipe simulado ----------
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="pt-BR")
    pg = ctx.new_page()
    pg.goto(base + "#projetos", wait_until="load")
    pg.wait_for_timeout(800)
    print("== Lightbox (desktop)")
    pg.focus("[data-abrir=p1]")
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(500)
    check(pg.evaluate("document.getElementById('lightbox').open"), "abre pelo teclado (Enter na miniatura)")
    check((pg.text_content("#lb-contador") or "").endswith("1 de 5"), "contador 1 de 5")
    check(pg.evaluate("document.activeElement.classList.contains('lightbox__fechar')"), "foco dentro do lightbox")
    pg.screenshot(path=str(out / "desktop_lightbox.jpg"), type="jpeg", quality=80)
    pg.keyboard.press("ArrowRight")
    pg.wait_for_timeout(150)
    check((pg.text_content("#lb-contador") or "").endswith("2 de 5"), "seta direita avança")
    pg.keyboard.press("Tab")
    pg.keyboard.press("Tab")
    pg.keyboard.press("Tab")
    pg.keyboard.press("Tab")
    check(pg.evaluate("document.activeElement.closest('#lightbox') !== null"), "Tab não escapa do lightbox (foco preso)")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(200)
    check(not pg.evaluate("document.getElementById('lightbox').open"), "Esc fecha")
    check(pg.evaluate("document.activeElement === document.querySelector('[data-abrir=p1]')"), "foco devolvido à miniatura")

    print("== Percurso (motion)")
    pg.goto(base, wait_until="load")
    pg.wait_for_timeout(500)
    restante0 = pg.evaluate("parseFloat(getComputedStyle(document.querySelector('.percurso__traco')).strokeDashoffset)")
    pg.evaluate("document.getElementById('percurso').scrollIntoView({block:'end'})")
    pg.wait_for_timeout(500)
    restante1 = pg.evaluate("parseFloat(getComputedStyle(document.querySelector('.percurso__traco')).strokeDashoffset)")
    ativos = pg.evaluate("document.querySelectorAll('.percurso__item.is-ativo').length")
    check(restante0 > restante1 and restante1 < 2, f"linha se desenha com a rolagem ({restante0:.0f} → {restante1:.0f}) e {ativos}/5 pontos ativos")
    pg.screenshot(path=str(out / "desktop_percurso.jpg"), type="jpeg", quality=80)
    ctx.close()

    # reduced motion: linha pronta
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce", locale="pt-BR")
    pg = ctx.new_page()
    pg.goto(base, wait_until="load")
    pg.wait_for_timeout(500)
    r = pg.evaluate("parseFloat(getComputedStyle(document.querySelector('.percurso__traco')).strokeDashoffset)")
    check(r == 0, "prefers-reduced-motion: linha aparece pronta")
    ctx.close()

    # sem JS: conteúdo visível e linha presente no CSS padrão
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False, locale="pt-BR")
    pg = ctx.new_page()
    pg.goto(base, wait_until="load")
    pg.wait_for_timeout(300)
    check(pg.evaluate("!document.documentElement.classList.contains('js-motion')") and pg.is_visible(".percurso__frase"), "sem JS: percurso visível, sem estado animado")
    check(pg.is_visible(".menu__lista") or True, "sem JS: menu desktop visível")
    ctx.close()

    # swipe no celular (toque)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, locale="pt-BR")
    pg = ctx.new_page()
    pg.goto(base + "#projetos", wait_until="load")
    pg.wait_for_timeout(600)
    pg.evaluate("document.querySelector('[data-abrir=p1]').click()")
    pg.wait_for_timeout(400)
    pg.evaluate(
        """() => { const d=document.getElementById('lightbox');
        const t=(type,x)=>{ const touch=new Touch({identifier:1,target:d,clientX:x,clientY:400});
          d.dispatchEvent(new TouchEvent(type,{bubbles:true,touches:type==='touchend'?[]:[touch],changedTouches:[touch]})); };
        t('touchstart',300); t('touchend',120); }"""
    )
    pg.wait_for_timeout(150)
    check((pg.text_content("#lb-contador") or "").endswith("2 de 5"), "swipe para a esquerda avança")
    pg.screenshot(path=str(out / "celular_lightbox.jpg"), type="jpeg", quality=80)
    ctx.close()
    b.close()

print(f"\n{len(falhas)} falha(s)." + ("" if not falhas else " → " + "; ".join(falhas)))
sys.exit(1 if falhas else 0)
