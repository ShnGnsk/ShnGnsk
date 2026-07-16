#!/usr/bin/env python3
"""Tek pano: net ölçüler + yerleşim + alışveriş özeti."""
from pathlib import Path

import cairosvg

from layout import (
    BALKON,
    CAM,
    CAM_SAG_PAY,
    CAM_SOL_PAY,
    D,
    GIRINTI,
    H_TAVAN,
    KAPI,
    KIRIS_ALONG,
    KIRIS_ICE,
    W,
    architecture,
    place_furniture,
)


def main() -> None:
    arch = architecture()
    items, notes = place_furniture(arch)
    sc, ox, oy = 0.9, 70, 420

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1680" font-family="Arial,sans-serif">
<rect width="1200" height="1680" fill="#0d0d0d"/>
<text x="60" y="70" fill="#fff" font-size="42" font-weight="700" font-family="Georgia,serif">1903</text>
<text x="60" y="105" fill="#ccc" font-size="18">Net kroki · Beşiktaş oyuncu odası · doğaçlama yok</text>
<text x="60" y="130" fill="#8a1f1f" font-size="15" font-weight="700">W={W:.0f} · D={D} · H={H_TAVAN:.0f} · Kapı {KAPI:.0f} · Balkon {BALKON} · Cam {CAM:.0f}</text>

<rect x="60" y="160" width="1080" height="210" fill="#1a1a1a" stroke="#333"/>
<text x="80" y="195" fill="#fff" font-size="20" font-weight="700">Kroki ölçüleri (kilit)</text>
<text x="80" y="230" fill="#ddd" font-size="15">ÜST: 295 cm düz duvar</text>
<text x="80" y="258" fill="#ddd" font-size="15">SAĞ: Kapı {KAPI:.0f} + Kiriş {KIRIS_ALONG}×{KIRIS_ICE:.0f} + Girinti {GIRINTI:.0f} = {D}</text>
<text x="80" y="286" fill="#ddd" font-size="15">ALT: {CAM_SOL_PAY:.0f} + Cam {CAM:.0f} (altında petek) + {CAM_SAG_PAY:.0f} = {W:.0f}</text>
<text x="80" y="314" fill="#ddd" font-size="15">SOL: Balkon {BALKON} + düz duvar {D-BALKON:.0f}</text>
<text x="80" y="348" fill="#aaa" font-size="14">Yasak: petek önü · kapı salınımı · kiriş hacmi · uydurma eğik duvar</text>

<text x="60" y="405" fill="#fff" font-size="20" font-weight="700">Yerleşim</text>
<rect x="{ox}" y="{oy}" width="{W*sc}" height="{D*sc}" fill="#f7f7f7" stroke="#fff" stroke-width="3"/>
"""
    # doors marks
    svg += f'<rect x="{ox+W*sc-8}" y="{oy}" width="10" height="{KAPI*sc}" fill="#999"/>'
    svg += f'<rect x="{ox-8}" y="{oy}" width="10" height="{BALKON*sc}" fill="#999"/>'
    svg += f'<rect x="{ox+(W-KIRIS_ICE)*sc}" y="{oy+KAPI*sc}" width="{KIRIS_ICE*sc}" height="{KIRIS_ALONG*sc}" fill="#111"/>'
    svg += f'<rect x="{ox+CAM_SOL_PAY*sc}" y="{oy+D*sc-8}" width="{CAM*sc}" height="10" fill="#8ab"/>'
    for it in items:
        if it.name == "hali":
            svg += f'<rect x="{ox+it.x*sc}" y="{oy+it.y*sc}" width="{it.w*sc}" height="{it.h*sc}" fill="#ddd" stroke="#111"/>'
        elif it.name == "sandalye":
            svg += f'<circle cx="{ox+(it.x+it.w/2)*sc}" cy="{oy+(it.y+it.h/2)*sc}" r="{22*sc}" fill="#333" stroke="#8a1f1f"/>'
        elif it.name.startswith("bjk"):
            svg += f'<circle cx="{ox+(it.x+5)*sc}" cy="{oy+(it.y+5)*sc}" r="9" fill="#fff" stroke="#8a1f1f" stroke-width="2"/>'
        else:
            svg += f'<rect x="{ox+it.x*sc}" y="{oy+it.y*sc}" width="{it.w*sc}" height="{it.h*sc}" fill="#1a1a1a" stroke="#8a1f1f"/>'
            svg += f'<text x="{ox+(it.x+it.w/2)*sc}" y="{oy+(it.y+it.h/2)*sc}" text-anchor="middle" fill="#fff" font-size="10">{it.name[:8]}</text>'

    lx = ox + W * sc + 40
    svg += f'<text x="{lx}" y="{oy+20}" fill="#fff" font-size="16" font-weight="700">Alışveriş (TR)</text>'
    shop = [
        "1 Boya Andezit / antrasit soft mat",
        "2 xDrive masa 100x60 ~6650₺",
        "3 xDrive Akdeniz koltuk ~13-15k₺",
        "4 PC siyah kasa",
        "5 IKEA BESTÅ 120 ~27500₺",
        "6 TV 50-55\"",
        "7 Oturma ≤120 sağ girinti",
        "8 Halı geometrik S/B",
        "9 BJK lisanslı saat",
        "10 BJK yastık/forma",
        "",
        "Detay + link: SIPARIS.md",
    ]
    for i, line in enumerate(shop):
        svg += f'<text x="{lx}" y="{oy+50+i*22}" fill="#ddd" font-size="14">{line}</text>'

    svg += f"""
<rect x="60" y="820" width="1080" height="100" fill="#1a1a1a" stroke="#333"/>
<text x="80" y="855" fill="#fff" font-size="16" font-weight="700">Neden bu yerleşim?</text>
<text x="80" y="885" fill="#ccc" font-size="14">Cam sol payı 107cm → 100lik masa sığar (petek yanına). Sol uzun duvar → TV. Sağ girinti 125cm → oturma TV'ye bakar.</text>
<text x="80" y="905" fill="#aaa" font-size="13">Üretim: python3 layout.py &amp;&amp; python3 gorusler.py &amp;&amp; python3 tasarim_pano.py</text>

<text x="60" y="960" fill="#fff" font-size="18" font-weight="700">Koordinat</text>
"""
    y = 990
    for it in items:
        if it.name.startswith("bjk"):
            continue
        svg += f'<text x="80" y="{y}" fill="#ddd" font-size="14">{it.name}: ({it.x:.0f},{it.y:.0f}) {it.w:.0f}×{it.h:.0f} cm</text>'
        y += 24

    svg += '<text x="600" y="1640" text-anchor="middle" fill="#444" font-size="12">1903 · net kroki tasarım panosu</text></svg>'
    root = Path(__file__).resolve().parent
    (root / "tasarim-pano.svg").write_text(svg, encoding="utf-8")
    out = root / "assets" / "tasarim-pano.png"
    cairosvg.svg2png(url=str(root / "tasarim-pano.svg"), write_to=str(out), scale=2)
    print("OK", out)


if __name__ == "__main__":
    main()
