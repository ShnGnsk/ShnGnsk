#!/usr/bin/env python3
"""Net ölçü duvar görünüşleri + izometrik — layout.py ile aynı cm."""
from __future__ import annotations

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


def elev_bottom(path: Path) -> None:
    """Alt duvar: 107 | cam 97 | 91 + masa sol bantta."""
    s, pad, H = 1.6, 50, H_TAVAN
    wall = W
    items, _ = place_furniture(architecture())
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pad*2+wall*s:.0f} {pad*2+H*s+60:.0f}" font-family="Arial,sans-serif">',
        f'<text x="{pad+wall*s/2}" y="30" text-anchor="middle" font-size="16" font-weight="700">ALT DUVAR — 107 + Cam 97 + 91 = 295</text>',
        f'<rect x="{pad}" y="{pad}" width="{wall*s}" height="{H*s}" fill="#f4f4f4" stroke="#111" stroke-width="3"/>',
        f'<rect x="{pad+CAM_SOL_PAY*s}" y="{pad+90*s}" width="{CAM*s}" height="{120*s}" fill="#cfe8f5" stroke="#111" stroke-width="2"/>',
        f'<line x1="{pad+(CAM_SOL_PAY+CAM/2)*s}" y1="{pad+90*s}" x2="{pad+(CAM_SOL_PAY+CAM/2)*s}" y2="{pad+210*s}" stroke="#111"/>',
        f'<text x="{pad+(CAM_SOL_PAY+CAM/2)*s}" y="{pad+155*s}" text-anchor="middle" font-size="13" font-weight="700">Cam {CAM:.0f}</text>',
        f'<rect x="{pad+(CAM_SOL_PAY+10)*s}" y="{pad+210*s}" width="{(CAM-20)*s}" height="{28*s}" fill="#bbb" stroke="#111"/>',
        f'<text x="{pad+(CAM_SOL_PAY+CAM/2)*s}" y="{pad+232*s}" text-anchor="middle" font-size="11">Petek (önü BOŞ)</text>',
        f'<text x="{pad+CAM_SOL_PAY*s/2}" y="{pad+40}" text-anchor="middle" font-size="12" fill="#8a1f1f" font-weight="700">{CAM_SOL_PAY:.0f}</text>',
        f'<text x="{pad+(CAM_SOL_PAY+CAM+CAM_SAG_PAY/2)*s}" y="{pad+40}" text-anchor="middle" font-size="12" fill="#8a1f1f" font-weight="700">{CAM_SAG_PAY:.0f}</text>',
    ]
    for it in items:
        if it.name == "masa":
            x = pad + it.x * s
            w = it.w * s
            mh = 75 * s
            by = pad + H * s - mh
            parts.append(f'<rect x="{x}" y="{by}" width="{w}" height="{mh}" fill="#111" stroke="#8a1f1f" stroke-width="2"/>')
            parts.append(f'<text x="{x+w/2}" y="{by+mh/2}" text-anchor="middle" font-size="12" fill="#fff">masa 100x60</text>')
    parts.append(
        f'<text x="{pad+wall*s/2}" y="{pad+H*s+35}" text-anchor="middle" font-size="12" fill="#555">Masa camın SOLUNDA · petek önüne değil</text>'
    )
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def elev_right(path: Path) -> None:
    s, pad, H = 1.6, 50, H_TAVAN
    wall = D
    items, _ = place_furniture(architecture())
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pad*2+wall*s:.0f} {pad*2+H*s+60:.0f}" font-family="Arial,sans-serif">',
        f'<text x="{pad+wall*s/2}" y="30" text-anchor="middle" font-size="16" font-weight="700">SAĞ DUVAR — Kapı 106 + Kiriş 64,5 + Girinti 125</text>',
        f'<rect x="{pad}" y="{pad}" width="{wall*s}" height="{H*s}" fill="#f4f4f4" stroke="#111" stroke-width="3"/>',
        f'<rect x="{pad}" y="{pad}" width="{KAPI*s}" height="{H*s}" fill="#e8e8e8" stroke="#111" stroke-dasharray="6 3"/>',
        f'<text x="{pad+KAPI*s/2}" y="{pad+H*s/2}" text-anchor="middle" font-size="14" font-weight="700">Kapı {KAPI:.0f}</text>',
        f'<rect x="{pad+KAPI*s}" y="{pad}" width="{KIRIS_ALONG*s}" height="{40*s}" fill="#111"/>',
        f'<text x="{pad+(KAPI+KIRIS_ALONG/2)*s}" y="{pad+25*s}" text-anchor="middle" font-size="12" fill="#fff">Kiriş {KIRIS_ALONG}×{KIRIS_ICE}</text>',
        f'<text x="{pad+(KAPI+KIRIS_ALONG+GIRINTI/2)*s}" y="{pad+H*s/2}" text-anchor="middle" font-size="13" fill="#1e8449" font-weight="700">Girinti duvar {GIRINTI:.0f}</text>',
    ]
    for it in items:
        if it.name == "oturma":
            # along wall = it.h, from y_girinti
            x = pad + (KAPI + KIRIS_ALONG + 5) * s
            w = it.h * s
            sh = 80 * s
            by = pad + H * s - sh
            parts.append(f'<rect x="{x}" y="{by}" width="{w}" height="{sh}" fill="#222" stroke="#000"/>')
            parts.append(f'<text x="{x+w/2}" y="{by+sh/2}" text-anchor="middle" font-size="12" fill="#fff">oturma</text>')
    parts.append(
        f'<text x="{pad+wall*s/2}" y="{pad+H*s+35}" text-anchor="middle" font-size="12" fill="#555">106 + 64,5 + 125 = 295,5 · kiriş içe 15cm</text>'
    )
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def elev_left(path: Path) -> None:
    s, pad, H = 1.6, 50, H_TAVAN
    wall = D
    items, _ = place_furniture(architecture())
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pad*2+wall*s:.0f} {pad*2+H*s+60:.0f}" font-family="Arial,sans-serif">',
        f'<text x="{pad+wall*s/2}" y="30" text-anchor="middle" font-size="16" font-weight="700">SOL DUVAR — Balkon {BALKON} + düz {D-BALKON:.0f}</text>',
        f'<rect x="{pad}" y="{pad}" width="{wall*s}" height="{H*s}" fill="#f4f4f4" stroke="#111" stroke-width="3"/>',
        f'<rect x="{pad}" y="{pad}" width="{BALKON*s}" height="{H*s}" fill="#e8e8e8" stroke="#111" stroke-dasharray="6 3"/>',
        f'<text x="{pad+BALKON*s/2}" y="{pad+H*s/2}" text-anchor="middle" font-size="13" font-weight="700">Balkon {BALKON}</text>',
    ]
    for it in items:
        if it.name == "tv_BESTA":
            x = pad + it.y * s
            w = it.h * s
            uh, th = 80 * s, 50 * s
            by = pad + H * s - uh
            parts.append(f'<rect x="{x}" y="{by}" width="{w}" height="{uh}" fill="#1a1a1a" stroke="#000"/>')
            parts.append(f'<rect x="{x+10}" y="{by-th}" width="{w-20}" height="{th}" fill="#111" stroke="#333"/>')
            parts.append(f'<text x="{x+w/2}" y="{by+uh/2}" text-anchor="middle" font-size="12" fill="#fff">BESTÅ + TV</text>')
        if it.name == "bjk_saat":
            cx = pad + (it.y + 5) * s
            cy = pad + 70 * s
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="16" fill="#fff" stroke="#8a1f1f" stroke-width="3"/>')
            parts.append(f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-size="9" fill="#8a1f1f" font-weight="700">BJK</text>')
    parts.append(
        f'<text x="{pad+wall*s/2}" y="{pad+H*s+35}" text-anchor="middle" font-size="12" fill="#555">TV balkon altında · tavan {H_TAVAN:.0f}cm</text>'
    )
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def elev_top(path: Path) -> None:
    s, pad, H = 1.6, 50, H_TAVAN
    wall = W
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pad*2+wall*s:.0f} {pad*2+H*s+60:.0f}" font-family="Arial,sans-serif">',
        f'<text x="{pad+wall*s/2}" y="30" text-anchor="middle" font-size="16" font-weight="700">ÜST DUVAR — 295 cm düz (kapı yok)</text>',
        f'<rect x="{pad}" y="{pad}" width="{wall*s}" height="{H*s}" fill="#f4f4f4" stroke="#111" stroke-width="3"/>',
        f'<text x="{pad+wall*s/2}" y="{pad+H*s/2}" text-anchor="middle" font-size="14" fill="#555">duvar boşluğu 295cm · geçiş / dekor</text>',
        f'<text x="{pad+wall*s/2}" y="{pad+H*s+35}" text-anchor="middle" font-size="12" fill="#555">Kapı sağ üstte (bu duvarda değil)</text>',
        "</svg>",
    ]
    path.write_text("\n".join(parts), encoding="utf-8")


def iso(path: Path) -> None:
    import math

    arch = architecture()
    items, _ = place_furniture(arch)
    c, s0, sc = math.cos(math.radians(30)), math.sin(math.radians(30)), 0.95

    def P(x, y, z=0):
        return (220 + (x - y) * c * sc, 400 + (x + y) * s0 * sc - z * sc)

    def box(x, y, w, h, zh, fill):
        p0, p1, p2, p3 = P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)
        t0, t1, t2, t3 = P(x, y, zh), P(x + w, y, zh), P(x + w, y + h, zh), P(x, y + h, zh)

        def pts(*ps):
            return " ".join(f"{a:.1f},{b:.1f}" for a, b in ps)

        return [
            f'<polygon points="{pts(p3,p2,t2,t3)}" fill="{fill}" stroke="#000" opacity="0.95"/>',
            f'<polygon points="{pts(p1,p2,t2,t1)}" fill="{fill}" stroke="#000" opacity="0.85"/>',
            f'<polygon points="{pts(t0,t1,t2,t3)}" fill="{fill}" stroke="#000"/>',
        ]

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 620" font-family="Arial,sans-serif">',
        '<rect width="720" height="620" fill="#fafafa"/>',
        '<text x="360" y="28" text-anchor="middle" font-size="16" font-weight="700">İZOMETRİK — net kroki cm (AI değil)</text>',
    ]
    fl = [P(0, 0), P(W, 0), P(W, D), P(0, D)]
    parts.append(
        f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in fl)}" fill="#eee" stroke="#111" stroke-width="2"/>'
    )
    # kiriş
    parts += box(W - KIRIS_ICE, KAPI, KIRIS_ICE, KIRIS_ALONG, 40, "#111")
    # cam mark
    parts += box(CAM_SOL_PAY, D - 4, CAM, 4, 110, "#9ec9e0")
    heights = {"masa": 75, "sandalye": 110, "tv_BESTA": 80, "oturma": 80, "hali": 2}
    colors = {"masa": "#1a1a1a", "sandalye": "#333", "tv_BESTA": "#1a1a1a", "oturma": "#222", "hali": "#ccc"}
    for it in items:
        if it.name.startswith("bjk"):
            continue
        zh = heights.get(it.name, 40)
        parts += box(it.x, it.y, it.w, it.h, zh, colors.get(it.name, "#444"))
    parts.append(
        f'<text x="360" y="580" text-anchor="middle" font-size="12" fill="#555">W={W:.0f} D={D} H={H_TAVAN:.0f} · kapı={KAPI:.0f} cam={CAM:.0f} balkon={BALKON}</text>'
    )
    parts.append(
        '<text x="360" y="600" text-anchor="middle" font-size="11" fill="#8a1f1f">Masa cam solu · TV sol · oturma sağ girinti</text>'
    )
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parent
    assets = root / "assets"
    elev_bottom(root / "gorus-alt.svg")
    elev_right(root / "gorus-sag.svg")
    elev_left(root / "gorus-sol.svg")
    elev_top(root / "gorus-ust.svg")
    iso(root / "izometrik.svg")
    for name in ("plan", "gorus-alt", "gorus-sag", "gorus-sol", "gorus-ust", "izometrik"):
        svg = root / ("plan.svg" if name == "plan" else f"{name}.svg")
        out = assets / f"{name}.png"
        cairosvg.svg2png(url=str(svg), write_to=str(out), scale=2)
        print("PNG", out.name)
    import shutil

    shutil.copy(assets / "plan.png", assets / "plan-olcekli.png")
    shutil.copy(assets / "plan.png", assets / "guncel-plan.png")


if __name__ == "__main__":
    main()
