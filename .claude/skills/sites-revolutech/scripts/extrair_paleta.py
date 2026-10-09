#!/usr/bin/env python3
"""Paleta real de um asset do cliente + checagem de contraste — RevoluTech.

Uso:
    python3 extrair_paleta.py logo.png [foto.jpg ...] [--cores 8]
    python3 extrair_paleta.py --contraste "#0B1B3F" "#FFFFFF"

1) Mede as cores que existem de fato na imagem (logo, foto da fachada, print do
   Instagram do cliente) e devolve HEX + % de área, juntando tons quase iguais.
   Pixels transparentes são ignorados (logos em PNG). O resultado é determinístico.
   Serve para tirar HEX exatos do material do CLIENTE ou da RevoluTech — nunca para
   copiar a identidade de terceiros.
2) Calcula a razão de contraste WCAG entre duas cores (texto x fundo).
   Alvos: texto normal >= 4,5:1; texto grande (>= 24px, ou 19px negrito) e ícones/foco >= 3:1.

Requer Pillow.
"""
import sys
import argparse
from PIL import Image


def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rel_lum(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((rel_lum(a), rel_lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def to_lab(rgb):
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116  # noqa: E731
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(a, b):
    la, lb = to_lab(a), to_lab(b)
    return sum((p - q) ** 2 for p, q in zip(la, lb)) ** 0.5


def palette(path, n):
    im = Image.open(path)
    im = im.convert("RGBA")
    im.thumbnail((400, 400))
    data = im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata()
    px = [p[:3] for p in data if p[3] >= 200]  # ignora transparência
    if not px:
        return []
    solid = Image.new("RGB", (len(px), 1))
    solid.putdata(px)
    q = solid.quantize(colors=max(n * 2, 8), method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    cols = []
    for c, idx in counts:
        rgb = tuple(pal[idx * 3: idx * 3 + 3])
        for item in cols:  # junta tons quase iguais (ΔE < 6)
            if delta_e(item[1], rgb) < 6:
                item[0] += c
                break
        else:
            cols.append([c, rgb])
    cols.sort(reverse=True)
    return [("#%02X%02X%02X" % rgb, 100 * c / total) for c, rgb in cols[:n] if 100 * c / total >= 0.5]  # ignora serrilhado < 0,5%


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("imagens", nargs="*")
    ap.add_argument("--cores", type=int, default=8)
    ap.add_argument("--contraste", nargs=2, metavar=("COR_A", "COR_B"))
    a = ap.parse_args()
    if a.contraste:
        r = contrast(hex_to_rgb(a.contraste[0]), hex_to_rgb(a.contraste[1]))
        verdict = "OK texto normal" if r >= 4.5 else ("só texto grande/ícone" if r >= 3 else "REPROVADO")
        print(f"{a.contraste[0]} x {a.contraste[1]}: {r:.2f}:1 — {verdict}")
        return
    if not a.imagens:
        ap.print_help()
        sys.exit(2)
    for path in a.imagens:
        print(f"== {path}")
        for hx, pct in palette(path, a.cores):
            rgb = hex_to_rgb(hx)
            print(f"  {hx}  {pct:5.1f}%   contraste c/ branco {contrast(rgb, (255,255,255)):.2f}:1 · c/ preto {contrast(rgb, (0,0,0)):.2f}:1")


if __name__ == "__main__":
    main()
