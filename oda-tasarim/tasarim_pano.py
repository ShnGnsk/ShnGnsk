#!/usr/bin/env python3
"""Tek sayfa tasarım panosu — çizim kriterleri + yerleşim + ürün. AI yok."""
from pathlib import Path

import cairosvg

from layout import CAM, DOOR, D, W, architecture, place_furniture


def main() -> None:
    arch = architecture()
    items, notes = place_furniture(arch)
    band = arch["band"]
    k0, k1 = arch["kiris"]

    by_name = {it.name: it for it in items}

    def row(name: str) -> str:
        it = by_name.get(name)
        if not it:
            return ""
        return f"{name}: {it.w:.0f}×{it.h:.0f} cm @ ({it.x:.0f},{it.y:.0f})"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1600" font-family="Arial,sans-serif">
  <defs>
    <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="6" stroke="#666" stroke-width="1"/>
    </pattern>
    <pattern id="rug" width="10" height="10" patternUnits="userSpaceOnUse">
      <rect width="10" height="10" fill="#eaeaea"/>
      <path d="M0 0L10 10M10 0L0 10" stroke="#222" stroke-width="0.6"/>
    </pattern>
  </defs>
  <rect width="1200" height="1600" fill="#0d0d0d"/>
  <text x="60" y="70" fill="#fff" font-size="42" font-weight="700" font-family="Georgia,serif">1903</text>
  <text x="60" y="105" fill="#c8c8c8" font-size="18">Beşiktaş oyuncu odası — çizim kriterlerine kilitli tasarım</text>
  <text x="60" y="130" fill="#8a1f1f" font-size="14" font-weight="700">AI perspektif YOK · standart kapı {DOOR} · 2li cam {CAM} · W={W}* D={D}*</text>

  <!-- KRITERLER -->
  <rect x="60" y="160" width="1080" height="200" fill="#1a1a1a" stroke="#333"/>
  <text x="80" y="195" fill="#fff" font-size="20" font-weight="700">Senin kriterlerin (değişmez)</text>
  <text x="80" y="230" fill="#ddd" font-size="15">ÜST: 2cm → Salon Kapısı {DOOR}cm → 5cm → Kiriş 40×10 sağa+içe → duvar boşluğu</text>
  <text x="80" y="258" fill="#ddd" font-size="15">ALT: 2cm → Balkon Kapısı {DOOR}cm → duvar boşluğu (oturma burada)</text>
  <text x="80" y="286" fill="#ddd" font-size="15">SAĞ: 2li cam {CAM}cm + petek ORTADA · bant≈{band:.0f}cm · petek önü boş</text>
  <text x="80" y="314" fill="#ddd" font-size="15">SOL: düz duvar (kapı yok) · TV + BJK saat · eğik duvar YOK</text>
  <text x="80" y="342" fill="#aaa" font-size="14">Renk: siyah / beyaz / kırmızı aksan · TR satışı ürünler</text>

  <!-- MINI PLAN -->
  <text x="60" y="410" fill="#fff" font-size="20" font-weight="700">Yerleşim (cm plan)</text>
"""
    # embed simplified plan at scale
    ox, oy = 80, 430
    sc = 1.0  # 1px=1cm for mini? too big. use 0.9
    sc = 0.85
    rw, rh = W * sc, D * sc
    svg += f'<rect x="{ox}" y="{oy}" width="{rw}" height="{rh}" fill="#f7f7f7" stroke="#fff" stroke-width="3"/>'
    # doors
    svg += f'<rect x="{ox+2*sc}" y="{oy-8}" width="{DOOR*sc}" height="12" fill="url(#hatch)" stroke="#111"/>'
    svg += f'<text x="{ox+(2+DOOR/2)*sc}" y="{oy-14}" text-anchor="middle" fill="#8a1f1f" font-size="12" font-weight="700">Salon {DOOR}</text>'
    svg += f'<rect x="{ox+2*sc}" y="{oy+rh-4}" width="{DOOR*sc}" height="12" fill="url(#hatch)" stroke="#111"/>'
    svg += f'<text x="{ox+(2+DOOR/2)*sc}" y="{oy+rh+28}" text-anchor="middle" fill="#8a1f1f" font-size="12" font-weight="700">Balkon {DOOR}</text>'
    # kiriş
    svg += f'<rect x="{ox+k0*sc}" y="{oy}" width="{(k1-k0)*sc}" height="{10*sc}" fill="#111"/>'
    svg += f'<text x="{ox+(k0+k1)/2*sc}" y="{oy+28}" text-anchor="middle" fill="#8a1f1f" font-size="11" font-weight="700">Kiriş 40×10</text>'
    # cam
    svg += f'<rect x="{ox+rw-8}" y="{oy+band*sc}" width="12" height="{CAM*sc}" fill="url(#hatch)" stroke="#111"/>'
    svg += f'<rect x="{ox+rw-22}" y="{oy+(band+15)*sc}" width="14" height="{(CAM-30)*sc}" fill="#c8c8c8" stroke="#111"/>'
    svg += f'<text x="{ox+rw+8}" y="{oy+(band+CAM/2)*sc}" fill="#fff" font-size="12" font-weight="700">2li cam</text>'
    # furniture
    for it in items:
        if it.name == "hali":
            svg += f'<rect x="{ox+it.x*sc}" y="{oy+it.y*sc}" width="{it.w*sc}" height="{it.h*sc}" fill="url(#rug)" stroke="#111"/>'
        elif it.name == "oyuncu_sandalye":
            cx, cy = ox + (it.x + it.w / 2) * sc, oy + (it.y + it.h / 2) * sc
            svg += f'<circle cx="{cx}" cy="{cy}" r="{28*sc}" fill="#333" stroke="#8a1f1f"/>'
        elif it.name.startswith("bjk"):
            cx, cy = ox + (it.x + 4) * sc, oy + (it.y + 4) * sc
            svg += f'<circle cx="{cx}" cy="{cy}" r="10" fill="#fff" stroke="#8a1f1f" stroke-width="2"/>'
            svg += f'<text x="{cx}" y="{cy+4}" text-anchor="middle" fill="#8a1f1f" font-size="8" font-weight="700">BJK</text>'
        else:
            svg += f'<rect x="{ox+it.x*sc}" y="{oy+it.y*sc}" width="{it.w*sc}" height="{it.h*sc}" fill="#1a1a1a" stroke="#8a1f1f"/>'
            svg += f'<text x="{ox+(it.x+it.w/2)*sc}" y="{oy+(it.y+it.h/2)*sc}" text-anchor="middle" fill="#fff" font-size="10">{it.name.split("_")[0]}</text>'

    # legend right of plan
    lx = ox + rw + 40
    ly = oy + 20
    svg += f'<text x="{lx}" y="{ly}" fill="#fff" font-size="16" font-weight="700">Mobilya paketi</text>'
    lines = [
        "1 Masa: xDrive 100×60 END-ON",
        "   sağ üst bant · kısa kenar duvarda",
        "2 Sandalye: siyah oyuncu koltuğu",
        "3 PC: siyah kasa (masa üstü)",
        "4 TV ünitesi: sol duvar BESTÅ",
        "5 TV: 50–55\"",
        "6 Oturma: ≤130cm balkon sağı",
        "7 Halı: geometrik S/B orta",
        "8 Saat: lisanslı BJK sol duvar",
        "9 Aksesuar: yastık/forma BJK",
        "",
        "YASAK:",
        "· petek önüne masa",
        "· kapı salınımına dolap",
        "· eğik duvar uydurma",
    ]
    for i, line in enumerate(lines):
        col = "#8a1f1f" if line.startswith("·") or line.startswith("YASAK") else "#ddd"
        svg += f'<text x="{lx}" y="{ly+30+i*22}" fill="{col}" font-size="14">{line}</text>'

    # bottom notes
    svg += f"""
  <rect x="60" y="820" width="1080" height="120" fill="#1a1a1a" stroke="#333"/>
  <text x="80" y="855" fill="#fff" font-size="18" font-weight="700">Neden böyle?</text>
  <text x="80" y="885" fill="#ccc" font-size="14">2li cam {CAM}cm → sağ bant ≈{band:.0f}cm → 100cm masa duvara PARALEL sığmaz → kısa kenar duvarda (end-on).</text>
  <text x="80" y="910" fill="#ccc" font-size="14">Masa üst sağda yer kaplar → TV sol duvarda. Oturma altta TV’ye / odaya bakar (≤130cm).</text>
  <text x="80" y="935" fill="#aaa" font-size="13">* W ve D yerinde ölç. Dosyalar: plan.svg · gorus-*.svg · SIPARIS.md</text>

  <text x="60" y="1000" fill="#fff" font-size="20" font-weight="700">Koordinat özeti (layout.py)</text>
"""
    y = 1035
    for it in items:
        if it.name.startswith("bjk"):
            continue
        svg += f'<text x="80" y="{y}" fill="#ddd" font-size="14">{row(it.name)}</text>'
        y += 26

    svg += f"""
  <text x="60" y="1280" fill="#8a1f1f" font-size="16" font-weight="700">Sipariş linkleri → SIPARIS.md / index.html</text>
  <text x="60" y="1320" fill="#888" font-size="13">Üretim: python3 layout.py &amp;&amp; python3 gorusler.py &amp;&amp; python3 tasarim_pano.py</text>
  <text x="600" y="1550" text-anchor="middle" fill="#444" font-size="12">1903 · çizim kilitli tasarım panosu</text>
</svg>
"""
    root = Path(__file__).resolve().parent
    (root / "tasarim-pano.svg").write_text(svg, encoding="utf-8")
    out = root / "assets" / "tasarim-pano.png"
    cairosvg.svg2png(url=str(root / "tasarim-pano.svg"), write_to=str(out), scale=2)
    print("OK", out)


if __name__ == "__main__":
    main()
