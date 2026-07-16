#!/usr/bin/env python3
"""
Çizimden birebir duvar görünüşleri + izometrik.
AI yok — koordinatlar layout.py ile aynı.
"""
from __future__ import annotations

from pathlib import Path

import cairosvg

from layout import (
    CAM,
    DOOR,
    D,
    GAP_KIRIS,
    GAP_START,
    KIRIS_D,
    KIRIS_W,
    W,
    architecture,
    place_furniture,
)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def elev_left(items, path: Path) -> None:
    """Sol duvara bakış: duvar boyu = D (y), yükseklik 250cm."""
    wall = D
    H = 250
    s = 1.5  # px/cm
    pad = 50
    # item along wall = item.y, depth into room ignored (front face)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pad*2+wall*s} {pad*2+H*s+40}" font-family="Arial,sans-serif">',
        f'<text x="{pad+wall*s/2}" y="28" text-anchor="middle" font-size="16" font-weight="700">SOL DUVAR — TV (cizimden)</text>',
        f'<rect x="{pad}" y="{pad}" width="{wall*s}" height="{H*s}" fill="#f4f4f4" stroke="#111" stroke-width="3"/>',
    ]
    # door marks at ends (salon top y=0, balkon y=D) — openings on TOP/BOTTOM walls meet left corners
    parts.append(
        f'<text x="{pad+10}" y="{pad+20}" font-size="11" fill="#8a1f1f">Salon kapi kosesı →</text>'
    )
    parts.append(
        f'<text x="{pad+wall*s-10}" y="{pad+H*s-10}" text-anchor="end" font-size="11" fill="#8a1f1f">← Balkon kapi kosesı</text>'
    )
    for it in items:
        if it.name == "tv_BESTA":
            # along wall: y .. y+h ; unit height 80 + TV 50
            x = pad + it.y * s
            w = it.h * s
            uh, th = 80 * s, 50 * s
            by = pad + H * s - uh
            parts.append(
                f'<rect x="{x}" y="{by}" width="{w}" height="{uh}" fill="#1a1a1a" stroke="#000"/>'
            )
            parts.append(
                f'<rect x="{x+8}" y="{by-th}" width="{w-16}" height="{th}" fill="#111" stroke="#333"/>'
            )
            parts.append(
                f'<text x="{x+w/2}" y="{by+uh/2}" text-anchor="middle" font-size="12" fill="#fff">BESTA TV {it.h:.0f}cm</text>'
            )
        if it.name == "bjk_saat_duvar":
            cx = pad + (it.y + 4) * s
            cy = pad + 80 * s
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="18" fill="#fff" stroke="#8a1f1f" stroke-width="3"/>')
            parts.append(
                f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-size="10" fill="#8a1f1f" font-weight="700">BJK</text>'
            )
    parts.append(
        f'<text x="{pad+wall*s/2}" y="{pad+H*s+28}" text-anchor="middle" font-size="12" fill="#555">'
        f"Duvar boyu D={wall}* cm · kapilar bu duvarda YOK · sadece TV+saat</text>"
    )
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def elev_right(items, arch, path: Path) -> None:
    """Sağ duvara bakış: cam ortada 140, petek, masa üst bantta."""
    wall = D
    H = 250
    s = 1.5
    pad = 50
    band = arch["band"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pad*2+wall*s} {pad*2+H*s+50}" font-family="Arial,sans-serif">',
        f'<text x="{pad+wall*s/2}" y="28" text-anchor="middle" font-size="16" font-weight="700">SAG DUVAR — 2li cam ORTA + masa (cizimden)</text>',
        f'<rect x="{pad}" y="{pad}" width="{wall*s}" height="{H*s}" fill="#f4f4f4" stroke="#111" stroke-width="3"/>',
    ]
    # window centered
    wx = pad + band * s
    ww = CAM * s
    wy = pad + 90 * s
    wh = 120 * s
    parts.append(
        f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="#cfe8f5" stroke="#111" stroke-width="2"/>'
    )
    # 2 leaf
    parts.append(
        f'<line x1="{wx+ww/2}" y1="{wy}" x2="{wx+ww/2}" y2="{wy+wh}" stroke="#111" stroke-width="2"/>'
    )
    parts.append(
        f'<text x="{wx+ww/2}" y="{wy+wh/2}" text-anchor="middle" font-size="13" font-weight="700">2li CAM {CAM}cm</text>'
    )
    # petek under window
    parts.append(
        f'<rect x="{wx+10}" y="{wy+wh}" width="{ww-20}" height="{25*s}" fill="#bbb" stroke="#111"/>'
    )
    parts.append(
        f'<text x="{wx+ww/2}" y="{wy+wh+18*s}" text-anchor="middle" font-size="11">Petek (onu BOS)</text>'
    )
    # band labels
    parts.append(
        f'<text x="{pad+band*s/2}" y="{pad+40}" text-anchor="middle" font-size="12" fill="#8a1f1f" font-weight="700">bant {band:.0f}*</text>'
    )
    parts.append(
        f'<text x="{pad+(band+CAM+band/2)*s}" y="{pad+40}" text-anchor="middle" font-size="12" fill="#8a1f1f" font-weight="700">bant {band:.0f}*</text>'
    )
    for it in items:
        if it.name == "masa":
            # plan: y=along, h=along size; desk height 75
            x = pad + it.y * s
            w = it.h * s
            mh = 75 * s
            by = pad + H * s - mh
            parts.append(
                f'<rect x="{x}" y="{by}" width="{w}" height="{mh}" fill="#111" stroke="#8a1f1f" stroke-width="2"/>'
            )
            parts.append(
                f'<text x="{x+w/2}" y="{by+mh/2}" text-anchor="middle" font-size="11" fill="#fff">masa end-on</text>'
            )
            # monitor
            parts.append(
                f'<rect x="{x+w*0.2}" y="{by-40}" width="{w*0.6}" height="40" fill="#222" stroke="#000"/>'
            )
        if it.name == "oyuncu_sandalye":
            cx = pad + (it.y + it.h / 2) * s
            cy = pad + H * s - 40
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="#333" stroke="#8a1f1f"/>')
            parts.append(
                f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="9" fill="#fff">sandalye</text>'
            )
    parts.append(
        f'<text x="{pad+wall*s/2}" y="{pad+H*s+30}" text-anchor="middle" font-size="12" fill="#555">'
        f"Kapı YOK · cam ORTA {CAM}cm · masa petek UST bandinda · petek onu bos</text>"
    )
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def elev_top(arch, path: Path) -> None:
    """Üst duvar: 2 | salon90 | 5 | kiriş40 | boş."""
    wall = W
    H = 250
    s = 1.5
    pad = 50
    k0, k1 = arch["kiris"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pad*2+wall*s} {pad*2+H*s+50}" font-family="Arial,sans-serif">',
        f'<text x="{pad+wall*s/2}" y="28" text-anchor="middle" font-size="16" font-weight="700">UST DUVAR — Salon kapisi + kiris (cizimden)</text>',
        f'<rect x="{pad}" y="{pad}" width="{wall*s}" height="{H*s}" fill="#f4f4f4" stroke="#111" stroke-width="3"/>',
    ]
    # 2cm stub
    parts.append(
        f'<rect x="{pad}" y="{pad}" width="{GAP_START*s}" height="{H*s}" fill="#ddd" stroke="#111"/>'
    )
    # door
    dx = pad + GAP_START * s
    parts.append(
        f'<rect x="{dx}" y="{pad}" width="{DOOR*s}" height="{H*s}" fill="#e8e8e8" stroke="#111" stroke-dasharray="6 3"/>'
    )
    parts.append(
        f'<text x="{dx+DOOR*s/2}" y="{pad+H*s/2}" text-anchor="middle" font-size="14" font-weight="700">Salon Kapisi {DOOR}cm</text>'
    )
    # 5cm
    gx = pad + (GAP_START + DOOR) * s
    parts.append(
        f'<rect x="{gx}" y="{pad}" width="{GAP_KIRIS*s}" height="{H*s}" fill="#ddd" stroke="#111"/>'
    )
    parts.append(
        f'<text x="{gx+GAP_KIRIS*s/2}" y="{pad+30}" text-anchor="middle" font-size="11" fill="#8a1f1f" font-weight="700">5</text>'
    )
    # kiriş protrusion indicator on ceiling line
    kx = pad + k0 * s
    parts.append(
        f'<rect x="{kx}" y="{pad}" width="{KIRIS_W*s}" height="{30*s}" fill="#111"/>'
    )
    parts.append(
        f'<text x="{kx+KIRIS_W*s/2}" y="{pad+20*s}" text-anchor="middle" font-size="12" fill="#fff">Kiris 40x10</text>'
    )
    parts.append(
        f'<text x="{pad+(k1+W)/2*s}" y="{pad+H*s/2}" text-anchor="middle" font-size="13" fill="#555">duvar boslugu</text>'
    )
    parts.append(
        f'<text x="{pad+wall*s/2}" y="{pad+H*s+30}" text-anchor="middle" font-size="12" fill="#555">'
        f"2 + {DOOR} + 5 + 40 + bos = W={W}* · egik duvar YOK</text>"
    )
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def elev_bottom(items, path: Path) -> None:
    """Alt duvar: 2 | balkon90 | oturma."""
    wall = W
    H = 250
    s = 1.5
    pad = 50
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pad*2+wall*s} {pad*2+H*s+50}" font-family="Arial,sans-serif">',
        f'<text x="{pad+wall*s/2}" y="28" text-anchor="middle" font-size="16" font-weight="700">ALT DUVAR — Balkon kapisi + oturma (cizimden)</text>',
        f'<rect x="{pad}" y="{pad}" width="{wall*s}" height="{H*s}" fill="#f4f4f4" stroke="#111" stroke-width="3"/>',
    ]
    parts.append(
        f'<rect x="{pad}" y="{pad}" width="{GAP_START*s}" height="{H*s}" fill="#ddd" stroke="#111"/>'
    )
    dx = pad + GAP_START * s
    parts.append(
        f'<rect x="{dx}" y="{pad}" width="{DOOR*s}" height="{H*s}" fill="#e8e8e8" stroke="#111" stroke-dasharray="6 3"/>'
    )
    parts.append(
        f'<text x="{dx+DOOR*s/2}" y="{pad+H*s/2}" text-anchor="middle" font-size="14" font-weight="700">Balkon Kapisi {DOOR}cm</text>'
    )
    for it in items:
        if it.name == "oturma":
            x = pad + it.x * s
            w = it.w * s
            sh = 80 * s
            by = pad + H * s - sh
            parts.append(
                f'<rect x="{x}" y="{by}" width="{w}" height="{sh}" fill="#222" stroke="#000"/>'
            )
            parts.append(
                f'<text x="{x+w/2}" y="{by+sh/2}" text-anchor="middle" font-size="13" fill="#fff">oturma {it.w:.0f}cm</text>'
            )
    parts.append(
        f'<text x="{pad+wall*s/2}" y="{pad+H*s+30}" text-anchor="middle" font-size="12" fill="#555">'
        f"2 + {DOOR} + bos · oturma balkon SAGINDA · salinima girmez</text>"
    )
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def iso_view(items, arch, path: Path) -> None:
    """Basit izometrik — AI değil, aynı cm kutular."""
    # iso: x' = (x-y)*cos30, y' = (x+y)*sin30 - z
    import math

    c = math.cos(math.radians(30))
    s = math.sin(math.radians(30))
    sc = 1.1

    def iso(x, y, z=0):
        return (200 + (x - y) * c * sc, 420 + (x + y) * s * sc - z * sc)

    def poly_box(x, y, w, h, zh, fill, stroke="#000"):
        # floor rect extruded
        p0 = iso(x, y, 0)
        p1 = iso(x + w, y, 0)
        p2 = iso(x + w, y + h, 0)
        p3 = iso(x, y + h, 0)
        t0 = iso(x, y, zh)
        t1 = iso(x + w, y, zh)
        t2 = iso(x + w, y + h, zh)
        t3 = iso(x, y + h, zh)
        def pts(*ps):
            return " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in ps)

        return [
            f'<polygon points="{pts(p3,p2,t2,t3)}" fill="{fill}" stroke="{stroke}" opacity="0.95"/>',
            f'<polygon points="{pts(p1,p2,t2,t1)}" fill="{fill}" stroke="{stroke}" opacity="0.85"/>',
            f'<polygon points="{pts(t0,t1,t2,t3)}" fill="{fill}" stroke="{stroke}"/>',
        ]

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 620" font-family="Arial,sans-serif">',
        '<rect width="700" height="620" fill="#fafafa"/>',
        '<text x="350" y="28" text-anchor="middle" font-size="16" font-weight="700">IZOMETRIK — cizim koordinatlari (AI degil)</text>',
    ]
    # room floor
    fl = [
        iso(0, 0),
        iso(W, 0),
        iso(W, D),
        iso(0, D),
    ]
    parts.append(
        f'<polygon points="{" ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in fl)}" fill="#eee" stroke="#111" stroke-width="2"/>'
    )
    # walls low
    for (x, y, w, h) in [(0, 0, W, 0), (0, 0, 0, D), (W, 0, 0, D), (0, D, W, 0)]:
        pass
    # kiriş
    k0, k1 = arch["kiris"]
    parts += poly_box(k0, 0, KIRIS_W, KIRIS_D, 40, "#111")
    # cam mark on right wall as blue panel
    band = arch["band"]
    parts += poly_box(W - 4, band, 4, CAM, 120, "#9ec9e0")
    # furniture
    heights = {
        "masa": 75,
        "oyuncu_sandalye": 110,
        "tv_BESTA": 80,
        "oturma": 80,
        "hali": 2,
        "bjk_saat_duvar": 0,
        "kitaplik": 147,
    }
    colors = {
        "masa": "#1a1a1a",
        "oyuncu_sandalye": "#333",
        "tv_BESTA": "#1a1a1a",
        "oturma": "#222",
        "hali": "#ccc",
        "kitaplik": "#1a1a1a",
    }
    for it in items:
        if it.name.startswith("bjk"):
            continue
        zh = heights.get(it.name, 40)
        if zh <= 0:
            continue
        parts += poly_box(it.x, it.y, it.w, it.h, zh, colors.get(it.name, "#444"))

    # labels
    parts.append(
        '<text x="350" y="580" text-anchor="middle" font-size="12" fill="#555">'
        f"W={W}* D={D}* · kapi={DOOR} · 2li cam={CAM} · ayni layout.py</text>"
    )
    parts.append(
        '<text x="350" y="600" text-anchor="middle" font-size="11" fill="#8a1f1f">'
        "Sol=TV · Sag ust=masa end-on · Alt=oturma · Cam sag ORTA</text>"
    )
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parent
    assets = root / "assets"
    arch = architecture()
    items, notes = place_furniture(arch)

    elev_left(items, root / "gorus-sol.svg")
    elev_right(items, arch, root / "gorus-sag.svg")
    elev_top(arch, root / "gorus-ust.svg")
    elev_bottom(items, root / "gorus-alt.svg")
    iso_view(items, arch, root / "izometrik.svg")

    for name in (
        "gorus-sol",
        "gorus-sag",
        "gorus-ust",
        "gorus-alt",
        "izometrik",
        "plan",
    ):
        svg = root / f"{name}.svg"
        if not svg.exists() and name == "plan":
            svg = root / "plan.svg"
        out = assets / f"{name}.png"
        cairosvg.svg2png(url=str(svg if name != "plan" else root / "plan.svg"), write_to=str(out), scale=2)
        print("PNG", out.name)

    # also copy gorus pngs named clearly
    print("OK gorusler")
    for n in notes[:6]:
        print(" ·", n)


if __name__ == "__main__":
    main()
