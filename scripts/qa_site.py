#!/usr/bin/env python3
"""QA de site — RevoluTech.

Uso:
    python3 qa_site.py <URL> [--saida qa/site] [--paginas 15]

Exemplos:
    python3 qa_site.py http://localhost:4173
    python3 qa_site.py https://cliente.com.br --saida qa/cliente-prod

Requer: Python 3.9+, playwright (com Chromium) e Pillow.

O que faz:
  - rastreia as páginas internas a partir da URL (até --paginas);
  - captura cada página em 390x844 (celular), 768x1024 (tablet) e 1440x900 (desktop);
  - mede rolagem lateral, alvos de toque pequenos e fonte de campo < 16px no celular;
  - confere console, requisições com erro, imagens quebradas/sem alt/sem dimensão;
  - confere SEO técnico (title, description, canonical, H1, lang, OG, Twitter, JSON-LD);
  - confere robots.txt, sitemap.xml, 404 real, /obrigado com noindex, /admin bloqueado;
  - confere formulários (label, consentimento LGPD não pré-marcado, honeypot, tipos);
  - confere links de WhatsApp e texto provisório esquecido (Lorem, [VERIFICAR], TODO).

Saída: relatorio.txt com OK/ALERTA/INFO, capturas por página e viewport e um mosaico
da home nos três tamanhos. Código de saída 0 = sem alertas, 1 = há alertas, 2 = erro de uso.
O relatório NÃO substitui olhar as capturas.
"""
import argparse
import io
import json
import re
import sys
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("playwright não instalado (pip install playwright)")
    sys.exit(2)
try:
    from PIL import Image
except ImportError:
    Image = None

VIEWPORTS = [("celular", 390, 844), ("tablet", 768, 1024), ("desktop", 1440, 900)]
PLACEHOLDERS = re.compile(
    r"lorem ipsum|\[VERIFICAR\]|\bTODO\b|\bTBD\b|XXXX|\(00\) ?0000|seu@email|exemplo@|example\.com|"
    r"nome do cliente|\[NOME|placeholder",
    re.I,
)
CONSENT_RE = re.compile(r"privacidade|lgpd|consinto|concordo|autorizo|aceito", re.I)
HONEYPOT_NAME_RE = re.compile(r"honey|hp_|website|url|company|empresa_fake|bot|fax", re.I)

report_lines = []
counts = {"ALERTA": 0, "OK": 0, "INFO": 0}


def log(msg=""):
    print(msg)
    report_lines.append(msg)


def ok(msg):
    counts["OK"] += 1
    log(f"  OK      {msg}")


def alert(msg):
    counts["ALERTA"] += 1
    log(f"  ALERTA  {msg}")


def info(msg):
    counts["INFO"] += 1
    log(f"  INFO    {msg}")


def slug_for(url, base):
    path = urlparse(url).path.strip("/") or "home"
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", path)[:60]


def same_origin(url, base):
    a, b = urlparse(url), urlparse(base)
    return (a.scheme, a.netloc) == (b.scheme, b.netloc)


def check_site_files(req, base, crawled_paths):
    log("== Arquivos do site")
    origin = f"{urlparse(base).scheme}://{urlparse(base).netloc}"

    r = req.get(origin + "/robots.txt")
    robots = r.text() if r.ok else ""
    if not r.ok:
        alert(f"robots.txt ausente (HTTP {r.status})")
    else:
        ok("robots.txt existe")
        if re.search(r"^\s*sitemap:\s*https?://", robots, re.I | re.M):
            ok("robots.txt aponta o sitemap")
        else:
            alert("robots.txt sem linha 'Sitemap: https://…'")
        if re.search(r"^\s*disallow:\s*/\s*$", robots, re.I | re.M):
            alert("robots.txt bloqueia o site inteiro (Disallow: /) — só aceitável em preview")

    r = req.get(origin + "/sitemap.xml")
    if not r.ok:
        alert(f"sitemap.xml ausente (HTTP {r.status})")
    else:
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text())
        ok(f"sitemap.xml com {len(locs)} URL(s)")
        bad = [u for u in locs if not u.startswith("https://") and "localhost" not in u and "127.0.0.1" not in u]
        if bad:
            alert(f"sitemap com URL sem https: {bad[:3]}")
        if any(re.search(r"/obrigado|/admin|/login", u) for u in locs):
            alert("sitemap inclui /obrigado, /admin ou /login (devem ficar fora)")
        if re.search(r"<priority>|<changefreq>", r.text()):
            info("sitemap usa priority/changefreq (o Google ignora; pode remover)")

    r = req.get(origin + "/pagina-inexistente-qa-revolutech")
    if r.status == 404:
        ok("rota inexistente responde 404 real")
        if len(r.text()) < 200:
            alert("página 404 parece vazia/padrão — fazer 404 personalizada com caminho de volta")
    else:
        alert(f"rota inexistente responde HTTP {r.status} (deveria ser 404 — comum em SPA na Vercel; configurar)")

    r = req.get(origin + "/obrigado")
    if r.ok:
        if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', r.text(), re.I):
            ok("/obrigado existe e tem noindex")
        else:
            alert("/obrigado existe mas sem meta robots noindex")
    else:
        info("/obrigado não encontrado (obrigatório se o site tem formulário)")

    r = req.get(origin + "/admin")
    if r.status < 400:
        if re.search(r"^\s*disallow:\s*/admin", robots, re.I | re.M):
            ok("/admin existe e está bloqueado no robots.txt")
        else:
            alert("/admin existe mas não está em 'Disallow: /admin' no robots.txt")
    else:
        info("/admin não encontrado (ok se o site não tem painel)")


def page_checks(page, url, base, is_home):
    """Checagens de conteúdo/SEO/formulários na viewport desktop."""
    data = page.evaluate(
        r"""() => {
      const q = s => document.querySelector(s);
      const meta = n => (q(`meta[name="${n}"]`)||q(`meta[property="${n}"]`)||{}).content || null;
      const imgs = [...document.images].map(i => ({src: i.currentSrc || i.src, alt: i.getAttribute('alt'),
         w: i.getAttribute('width'), h: i.getAttribute('height'), ok: i.complete ? i.naturalWidth > 0 : true,
         lazy: i.loading, rect: i.getBoundingClientRect().top}));
      const heads = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => +h.tagName[1]);
      const ld = [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent);
      const links = [...document.querySelectorAll('a[href]')].map(a => a.href);
      const forms = [...document.querySelectorAll('form')].map(f => {
        const fields = [...f.querySelectorAll('input,select,textarea')].filter(e => !['submit','button','hidden','reset','image'].includes(e.type));
        const labelOf = e => {
          if (e.getAttribute('aria-label') || e.getAttribute('aria-labelledby')) return true;
          if (e.id && document.querySelector(`label[for="${CSS.escape(e.id)}"]`)) return true;
          return !!e.closest('label');
        };
        const visible = e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
          const onScreen = r.right > 0 && r.bottom > 0 && r.left < Math.max(innerWidth, document.documentElement.scrollWidth) && r.top < document.documentElement.scrollHeight;
          const clipped = cs.clipPath && cs.clipPath !== 'none' || (cs.clip && cs.clip !== 'auto');
          return r.width > 1 && r.height > 1 && onScreen && !clipped && !e.closest('[aria-hidden="true"]') && cs.visibility !== 'hidden' && cs.display !== 'none' && +cs.opacity > 0.01; };
        const labelText = e => { let t = ''; if (e.id) { const l = document.querySelector(`label[for="${CSS.escape(e.id)}"]`); if (l) t += l.innerText; }
          const w = e.closest('label'); if (w) t += ' ' + w.innerText; return (t + ' ' + (e.getAttribute('aria-label')||'')).trim(); };
        return {
          action: f.getAttribute('action'),
          fields: fields.map(e => ({tag: e.tagName.toLowerCase(), type: e.type, name: e.name || e.id || '',
            visible: visible(e), labeled: labelOf(e), checked: !!e.checked, label: labelText(e).slice(0,120),
            autocomplete: e.getAttribute('autocomplete'), tabindex: e.getAttribute('tabindex'),
            ariaHidden: e.getAttribute('aria-hidden') || (e.closest('[aria-hidden="true"]') ? 'true' : null)})),
        };
      });
      return {
        title: document.title, lang: document.documentElement.lang,
        description: meta('description'), robots: meta('robots'),
        canonical: (q('link[rel="canonical"]')||{}).href || null,
        og: {title: meta('og:title'), description: meta('og:description'), image: meta('og:image'), url: meta('og:url'), type: meta('og:type')},
        twitter: meta('twitter:card'), viewport: meta('viewport'),
        favicon: !!q('link[rel~="icon"]'),
        imgs, heads, ld, links, forms,
        text: document.body ? document.body.innerText : '',
      };
    }"""
    )
    path = urlparse(url).path or "/"
    is_obrigado = bool(re.search(r"/obrigad", path))
    is_admin = bool(re.search(r"/admin|/login", path))

    # --- SEO básico
    t = (data["title"] or "").strip()
    if not t:
        alert("sem <title>")
    elif len(t) > 65:
        alert(f"title com {len(t)} caracteres (ideal 50–60): \"{t[:70]}…\"")
    else:
        ok(f"title ({len(t)} car.)")
    d = (data["description"] or "").strip()
    if not d and not is_obrigado and not is_admin:
        alert("sem meta description")
    elif d and not (70 <= len(d) <= 165):
        info(f"meta description com {len(d)} caracteres (ideal 150–160)")
    elif d:
        ok("meta description")
    if not (data["lang"] or "").lower().startswith("pt"):
        alert(f"<html lang> é '{data['lang']}' (esperado pt-BR)")
    if not data["viewport"] or "width=device-width" not in data["viewport"]:
        alert("sem meta viewport width=device-width")
    elif "user-scalable=no" in data["viewport"] or "maximum-scale=1" in data["viewport"]:
        alert("meta viewport bloqueia zoom (user-scalable=no / maximum-scale=1)")
    if data["canonical"]:
        if not same_origin(data["canonical"], base) and "localhost" not in base:
            info(f"canonical aponta para outro domínio: {data['canonical']}")
        else:
            ok("canonical presente")
    elif not is_obrigado and not is_admin:
        alert("sem link rel=canonical")
    h1 = data["heads"].count(1)
    if h1 != 1 and not is_admin:
        alert(f"{h1} H1 na página (esperado 1)")
    skips = [(a, b) for a, b in zip(data["heads"], data["heads"][1:]) if b > a + 1]
    if skips:
        info(f"hierarquia de títulos pula nível {skips[:3]}")
    if is_home and not data["favicon"]:
        alert("sem favicon")

    noindex = bool(data["robots"] and "noindex" in data["robots"].lower())
    if is_obrigado or is_admin:
        (ok if noindex else alert)(f"{path} {'tem' if noindex else 'sem'} meta robots noindex")
    elif noindex:
        alert("página com noindex (só aceitável em preview, /obrigado ou /admin)")

    # --- Open Graph / Twitter (páginas públicas)
    if not is_obrigado and not is_admin:
        miss = [k for k in ("title", "description", "image", "url") if not data["og"][k]]
        if miss:
            alert(f"Open Graph incompleto: falta og:{', og:'.join(miss)}")
        else:
            ok("Open Graph completo")
        if data["og"]["image"]:
            if not re.match(r"https?://", data["og"]["image"]):
                alert(f"og:image com URL relativa ({data['og']['image']}) — WhatsApp/Facebook exigem URL absoluta")
            check_og_image(page, urljoin(url, data["og"]["image"]))
        if not data["twitter"]:
            info("sem twitter:card (recomendado summary_large_image)")

    # --- JSON-LD
    for raw in data["ld"]:
        try:
            obj = json.loads(raw)
        except Exception:
            alert("JSON-LD inválido (não faz parse)")
            continue
        s = json.dumps(obj, ensure_ascii=False)
        types = re.findall(r'"@type":\s*"([^"]+)"', s)
        ok(f"JSON-LD: {', '.join(sorted(set(types)))[:120]}")
        if re.search(r'"aggregateRating"|"@type":\s*"Review"', s):
            alert("JSON-LD com aggregateRating/Review do próprio negócio (proibido: avaliação autoatribuída)")
        if re.search(r'"@type":\s*"HowTo"', s):
            info("JSON-LD HowTo foi aposentado pelo Google")
        if PLACEHOLDERS.search(s):
            alert("JSON-LD com texto provisório")
        m = re.search(r'"addressCountry":\s*"([^"]+)"', s)
        if m and m.group(1).upper() not in ("BR", "BRASIL", "BRAZIL"):
            alert(f"JSON-LD addressCountry = {m.group(1)}")

    # --- Imagens
    imgs = data["imgs"]
    broken = [i["src"] for i in imgs if not i["ok"]]
    no_alt = [i["src"] for i in imgs if i["alt"] is None]
    no_dim = [i["src"] for i in imgs if not (i["w"] and i["h"])]
    if broken:
        alert(f"{len(broken)} imagem(ns) quebrada(s): {[b[-60:] for b in broken[:3]]}")
    if no_alt:
        alert(f"{len(no_alt)} imagem(ns) sem atributo alt: {[b[-50:] for b in no_alt[:3]]}")
    if no_dim:
        info(f"{len(no_dim)} imagem(ns) sem width/height no HTML (risco de CLS)")
    if imgs and not broken and not no_alt:
        ok(f"{len(imgs)} imagem(ns) carregadas com alt")

    # --- Formulários
    for idx, f in enumerate(data["forms"], 1):
        fields = f["fields"]
        vis = [x for x in fields if x["visible"]]
        hidden_inputs = [x for x in fields if not x["visible"] and x["type"] not in ("checkbox", "radio")]
        unl = [x["name"] or x["type"] for x in vis if not x["labeled"] and x["type"] not in ("checkbox",)]
        tag = f"form #{idx}"
        if unl:
            alert(f"{tag}: campo(s) sem label: {unl[:5]}")
        else:
            ok(f"{tag}: campos com label")
        hp = [x for x in hidden_inputs if HONEYPOT_NAME_RE.search(x["name"] or "") or x["tabindex"] == "-1"]
        if hp:
            ok(f"{tag}: honeypot encontrado ({hp[0]['name']})")
            if not all(x["tabindex"] == "-1" and x["ariaHidden"] for x in hp):
                info(f"{tag}: honeypot deve ter tabindex=-1 e aria-hidden=true")
        else:
            alert(f"{tag}: honeypot não encontrado")
        consent = [x for x in vis if x["type"] == "checkbox" and CONSENT_RE.search(x["label"])]
        if not consent:
            alert(f"{tag}: sem checkbox de consentimento LGPD visível")
        else:
            if any(x["checked"] for x in consent):
                alert(f"{tag}: consentimento LGPD vem pré-marcado (proibido)")
            else:
                ok(f"{tag}: consentimento LGPD não pré-marcado")
        for x in vis:
            nm = (x["name"] or "").lower()
            if re.search(r"mail", nm) and x["type"] != "email":
                alert(f"{tag}: campo '{x['name']}' devia ser type=email")
            if re.search(r"tel|fone|whats|celular", nm) and x["type"] != "tel":
                alert(f"{tag}: campo '{x['name']}' devia ser type=tel")
            if re.search(r"nome|name|mail|tel|fone|celular", nm) and not x["autocomplete"]:
                info(f"{tag}: campo '{x['name']}' sem autocomplete")
    if data["forms"] and not any(re.search(r"privacidade|privacy", l, re.I) for l in data["links"]):
        alert("página com formulário sem link para Política de Privacidade")

    # --- WhatsApp
    wa = [l for l in data["links"] if re.search(r"wa\.me/|api\.whatsapp\.com|whatsapp://", l)]
    for l in sorted(set(wa)):
        num = re.search(r"wa\.me/(\d+)|phone=(\d+)", l)
        digits = (num.group(1) or num.group(2)) if num else ""
        if not re.fullmatch(r"55\d{10,11}", digits or ""):
            alert(f"link de WhatsApp com número fora do padrão 55+DDD+número: {l[:80]}")
        elif "text=" not in l:
            info(f"WhatsApp sem mensagem pré-preenchida: {l[:60]}")
        else:
            ok(f"WhatsApp {digits[:4]}… com mensagem")

    # --- Texto provisório
    hits = sorted(set(m.group(0) for m in PLACEHOLDERS.finditer(data["text"] or "")))
    if hits:
        alert(f"texto provisório na página: {hits[:5]}")

    return [l for l in data["links"]]


def check_og_image(page, src):
    try:
        r = page.request.get(src)
        if not r.ok:
            alert(f"og:image não carrega (HTTP {r.status})")
            return
        if Image is None:
            info("Pillow ausente: tamanho da og:image não conferido")
            return
        w, h = Image.open(io.BytesIO(r.body())).size
        if (w, h) == (1200, 630):
            ok("og:image 1200×630")
        else:
            alert(f"og:image {w}×{h} (padrão 1200×630)")
    except Exception as e:  # noqa: BLE001
        alert(f"og:image não verificada ({type(e).__name__})")


def layout_checks(page, vp_name, vw):
    data = page.evaluate(
        r"""(vw) => {
      const doc = document.documentElement;
      const over = doc.scrollWidth > vw + 1;
      const culprits = [];
      if (over) {
        for (const el of document.querySelectorAll('body *')) {
          const r = el.getBoundingClientRect();
          if (r.right > vw + 1 && r.width > 0 && getComputedStyle(el).position !== 'fixed') {
            let ok = false, p = el.parentElement;
            while (p && p !== document.body) { const o = getComputedStyle(p).overflowX; if (o === 'hidden' || o === 'clip' || o === 'auto' || o === 'scroll') { ok = true; break; } p = p.parentElement; }
            if (!ok) culprits.push(el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0,2).join('.') : '') + ` (${Math.round(r.right)}px)`);
          }
          if (culprits.length >= 5) break;
        }
      }
      const small = [], tiny = [];
      for (const el of document.querySelectorAll('a[href], button, [role="button"], input:not([type=hidden]), select, textarea, summary')) {
        const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
        if (r.width < 1 || r.height < 1 || cs.visibility === 'hidden') continue;
        if (el.tagName === 'A' && el.closest('p, li, label, small, figcaption, td, dd')) continue; // link dentro de texto corrido (exceção WCAG 2.5.8)
        const m = Math.min(r.width, r.height);
        const name = (el.innerText || el.getAttribute('aria-label') || el.name || el.tagName).trim().slice(0, 30);
        if (m < 24) tiny.push(name); else if (m < 40) small.push(name);
      }
      const smallFont = [...document.querySelectorAll('input:not([type=hidden]):not([type=checkbox]):not([type=radio]), select, textarea')]
        .filter(e => e.getBoundingClientRect().width > 1 && parseFloat(getComputedStyle(e).fontSize) < 16).map(e => e.name || e.id || e.type);
      return {over, sw: doc.scrollWidth, culprits, small, tiny, smallFont};
    }""",
        vw,
    )
    if data["over"]:
        alert(f"[{vp_name}] rolagem lateral: largura {data['sw']}px > {vw}px — culpados: {data['culprits']}")
    else:
        ok(f"[{vp_name}] sem rolagem lateral")
    if vp_name == "celular":
        if data["tiny"]:
            alert(f"[celular] {len(data['tiny'])} alvo(s) de toque < 24px: {data['tiny'][:5]}")
        if data["small"]:
            info(f"[celular] {len(data['small'])} alvo(s) de toque entre 24 e 40px (confortável ≥ 44px): {data['small'][:5]}")
        if data["smallFont"]:
            alert(f"[celular] campo(s) com fonte < 16px (iPhone dá zoom): {data['smallFont'][:5]}")


def settle(page):
    """Rola até o fim para disparar lazy-load e animações de entrada, depois volta ao topo."""
    page.evaluate(
        """async () => { const h = () => document.documentElement.scrollHeight;
          for (let y = 0; y < h(); y += Math.max(400, innerHeight * 0.8)) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
          scrollTo(0, h()); await new Promise(r => setTimeout(r, 400)); scrollTo(0, 0); await new Promise(r => setTimeout(r, 300)); }"""
    )


def main():
    ap = argparse.ArgumentParser(description="QA de site — RevoluTech")
    ap.add_argument("url")
    ap.add_argument("--saida", default=None)
    ap.add_argument("--paginas", type=int, default=15)
    a = ap.parse_args()
    base = a.url if a.url.endswith("/") else a.url + "/"
    out = Path(a.saida or f"qa/{urlparse(base).netloc.replace(':', '_')}")
    (out / "capturas").mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        req = p.request.new_context(ignore_https_errors=False)
        log(f"== QA de site: {base}")
        try:
            check_site_files(req, base, [])
        except Exception as e:  # noqa: BLE001
            alert(f"não foi possível conferir robots/sitemap/404 ({type(e).__name__}: {str(e)[:80]})")

        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, locale="pt-BR")
        page = ctx.new_page()
        console_errs, failed = [], []
        page.on("console", lambda m: console_errs.append(m.text[:160]) if m.type == "error" else None)
        page.on("pageerror", lambda e: console_errs.append(f"pageerror: {str(e)[:160]}"))
        page.on("response", lambda r: failed.append(f"{r.status} {r.url[:100]}") if r.status >= 400 and "favicon" not in r.url else None)

        queue, seen, pages = deque([base]), set(), []
        while queue and len(pages) < a.paginas:
            url = urldefrag(queue.popleft())[0]
            if url in seen:
                continue
            seen.add(url)
            if re.search(r"\.(pdf|jpe?g|png|webp|avif|svg|zip|mp4)$", url, re.I):
                continue
            log(f"\n== Página {urlparse(url).path or '/'}")
            console_errs.clear(); failed.clear()
            try:
                resp = page.goto(url, wait_until="load", timeout=45000)
            except Exception as e:  # noqa: BLE001
                alert(f"não carregou ({type(e).__name__})")
                continue
            if resp and resp.status >= 400:
                alert(f"HTTP {resp.status}")
                continue
            page.wait_for_timeout(1200)
            settle(page)
            links = page_checks(page, url, base, is_home=(url == base))
            if console_errs:
                alert(f"{len(console_errs)} erro(s) no console: {console_errs[:3]}")
            else:
                ok("console sem erros")
            if failed:
                alert(f"{len(failed)} requisição(ões) com erro: {failed[:4]}")
            pages.append(url)
            for l in links:
                l = urldefrag(l)[0]
                if same_origin(l, base) and l not in seen and not re.search(r"/admin|/login|mailto:|tel:", l):
                    queue.append(l)
        ctx.close()

        log("\n== Responsividade (captura por viewport)")
        shots_home = []
        for name, w, h in VIEWPORTS:
            c = browser.new_context(viewport={"width": w, "height": h}, locale="pt-BR",
                                    is_mobile=(name == "celular"), has_touch=(name != "desktop"),
                                    device_scale_factor=2 if name == "celular" else 1)
            pg = c.new_page()
            for url in pages:
                try:
                    pg.goto(url, wait_until="load", timeout=45000)
                    pg.wait_for_timeout(800)
                    settle(pg)
                except Exception as e:  # noqa: BLE001
                    alert(f"[{name}] {urlparse(url).path} não carregou ({type(e).__name__})")
                    continue
                log(f"-- {name} {w}x{h} {urlparse(url).path or '/'}")
                layout_checks(pg, name, w)
                f = out / "capturas" / f"{slug_for(url, base)}_{name}.jpg"
                pg.screenshot(path=str(f), full_page=True, type="jpeg", quality=70)
                if url == base:
                    shots_home.append(f)
            c.close()
        browser.close()

    if Image and len(shots_home) == 3:
        # mosaico: celular | tablet | desktop, cada um com 500px de largura e até 1800px de altura
        scaled = []
        for s in shots_home:
            im = Image.open(s).convert("RGB")
            ratio = 500 / im.width
            h_full = max(1, int(im.height * ratio))
            scaled.append(im.resize((500, h_full)).crop((0, 0, 500, min(h_full, 1800))))
        mos = Image.new("RGB", (500 * 3 + 40, max(s.height for s in scaled) + 20), "white")
        x = 10
        for s in scaled:
            mos.paste(s, (x, 10)); x += 510
        mos.save(out / "home_mosaico.jpg", quality=75)

    log(f"\nRESULTADO: {counts['ALERTA']} alerta(s), {counts['OK']} ok, {counts['INFO']} info — {len(pages)} página(s)")
    log("Revise com os próprios olhos: home_mosaico.jpg e a pasta capturas/ (celular, tablet, desktop).")
    (out / "relatorio.txt").write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Relatório: {out / 'relatorio.txt'}")
    sys.exit(1 if counts["ALERTA"] else 0)


if __name__ == "__main__":
    main()
