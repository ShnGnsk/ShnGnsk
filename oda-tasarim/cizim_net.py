#!/usr/bin/env python3
"""
CM-DOĞRU oda çizimi — kullanıcı krokisi.
1) Önce BOŞ oda (kapı/cam/kiriş/girinti/balkon net cm)
2) Sonra mobilya (masa, sandalye, raf, TV, koltuk, halı, perde)
Fotoreal AI yok. Doğaçlama yok.
"""
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
    Rect,
    architecture,
    place_furniture,
)

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

SCALE = 1.55
OX, OY = 120, 70


def X(cm: float) -> float:
    return OX + cm * SCALE


def Y(cm: float) -> float:
    return OY + cm * SCALE


def dim_h(x0: float, x1: float, y: float, label: str, color: str = "#8a1f1f") -> list[str]:
    mx = (x0 + x1) / 2
    return [
        f'<line x1="{X(x0)}" y1="{Y(y)}" x2="{X(x1)}" y2="{Y(y)}" stroke="{color}" stroke-width="1.2"/>',
        f'<line x1="{X(x0)}" y1="{Y(y)-6}" x2="{X(x0)}" y2="{Y(y)+6}" stroke="{color}"/>',
        f'<line x1="{X(x1)}" y1="{Y(y)-6}" x2="{X(x1)}" y2="{Y(y)+6}" stroke="{color}"/>',
        f'<text x="{X(mx)}" y="{Y(y)-8}" text-anchor="middle" font-size="13" font-weight="700" fill="{color}">{label}</text>',
    ]


def dim_v(y0: float, y1: float, x: float, label: str, color: str = "#8a1f1f") -> list[str]:
    my = (y0 + y1) / 2
    return [
        f'<line x1="{X(x)}" y1="{Y(y0)}" x2="{X(x)}" y2="{Y(y1)}" stroke="{color}" stroke-width="1.2"/>',
        f'<line x1="{X(x)-6}" y1="{Y(y0)}" x2="{X(x)+6}" y2="{Y(y0)}" stroke="{color}"/>',
        f'<line x1="{X(x)-6}" y1="{Y(y1)}" x2="{X(x)+6}" y2="{Y(y1)}" stroke="{color}"/>',
        f'<text x="{X(x)+10}" y="{Y(my)+4}" font-size="13" font-weight="700" fill="{color}">{label}</text>',
    ]


def draw_empty_room() -> list[str]:
    """Sadece mimari — mobilya yok."""
    x_cam0 = CAM_SOL_PAY
    x_cam1 = CAM_SOL_PAY + CAM
    y_k0, y_k1 = KAPI, KAPI + KIRIS_ALONG
    y_g0 = y_k1

    p: list[str] = []
    # floor
    p.append(
        f'<rect x="{X(0)}" y="{Y(0)}" width="{W*SCALE}" height="{D*SCALE}" '
        f'fill="#fafafa" stroke="#111" stroke-width="4"/>'
    )
    p.append(
        f'<text x="{X(W/2)}" y="{OY-28}" text-anchor="middle" font-size="20" font-weight="800">'
        f'1) BOŞ ODA — NET CM (doğaçlama yok)</text>'
    )
    p.append(
        f'<text x="{X(W/2)}" y="{OY-8}" text-anchor="middle" font-size="13" fill="#444">'
        f'W={W:.0f} · D={D} · H={H_TAVAN:.0f}</text>'
    )

    # ÜST duvar etiketi
    p.append(
        f'<text x="{X(W/2)}" y="{Y(0)-10}" text-anchor="middle" font-size="14" font-weight="700">'
        f'ÜST DUVAR 295 cm — düz (kapı YOK)</text>'
    )

    # SAĞ: Kapı
    p += [
        f'<rect x="{X(W)-8}" y="{Y(0)}" width="16" height="{KAPI*SCALE}" fill="#fff" stroke="#111" stroke-width="2"/>',
        f'<rect x="{X(W)-8}" y="{Y(0)}" width="16" height="{KAPI*SCALE}" fill="url(#hatch)"/>',
        f'<text x="{X(W)+22}" y="{Y(KAPI/2)+4}" font-size="14" font-weight="800">Kapı {KAPI:.0f} cm</text>',
    ]
    # SAĞ: Kiriş içe 15
    p += [
        f'<rect x="{X(W-KIRIS_ICE)}" y="{Y(y_k0)}" width="{KIRIS_ICE*SCALE}" height="{KIRIS_ALONG*SCALE}" '
        f'fill="#1a1a1a" stroke="#000"/>',
        f'<text x="{X(W)+22}" y="{Y((y_k0+y_k1)/2)+4}" font-size="13" font-weight="800" fill="#8a1f1f">'
        f'Kiriş {KIRIS_ALONG}×{KIRIS_ICE} cm</text>',
        f'<text x="{X(W)+22}" y="{Y((y_k0+y_k1)/2)+20}" font-size="11" fill="#8a1f1f">(içe çıkıntı)</text>',
    ]
    # SAĞ: Girinti
    p += [
        f'<text x="{X(W)+22}" y="{Y((y_g0+D)/2)+4}" font-size="14" font-weight="800" fill="#1e8449">'
        f'Girinti duvar {GIRINTI:.0f} cm</text>',
    ]
    # sağ duvar toplam ölçü
    p += dim_v(0, D, W + 55 / SCALE, f"{D} cm", "#111")

    # ALT: cam + petek
    p += [
        f'<rect x="{X(x_cam0)}" y="{Y(D)-8}" width="{CAM*SCALE}" height="16" fill="#9fd3f0" stroke="#111" stroke-width="2"/>',
        f'<rect x="{X(x_cam0+6)}" y="{Y(D-22)}" width="{(CAM-12)*SCALE}" height="{16*SCALE}" fill="#c8c8c8" stroke="#111"/>',
        f'<text x="{X((x_cam0+x_cam1)/2)}" y="{Y(D)+34}" text-anchor="middle" font-size="14" font-weight="800">'
        f'Cam {CAM:.0f} cm · altında petek</text>',
    ]
    p += dim_h(0, CAM_SOL_PAY, D + 28 / SCALE, f"{CAM_SOL_PAY:.0f}", "#8a1f1f")
    p += dim_h(x_cam0, x_cam1, D + 48 / SCALE, f"Cam {CAM:.0f}", "#1565c0")
    p += dim_h(x_cam1, W, D + 28 / SCALE, f"{CAM_SAG_PAY:.0f}", "#8a1f1f")
    p += dim_h(0, W, D + 70 / SCALE, f"ALT = {W:.0f} cm", "#111")

    # SOL: balkon
    p += [
        f'<rect x="{X(0)-8}" y="{Y(0)}" width="16" height="{BALKON*SCALE}" fill="#fff" stroke="#111" stroke-width="2"/>',
        f'<rect x="{X(0)-8}" y="{Y(0)}" width="16" height="{BALKON*SCALE}" fill="url(#hatch)"/>',
        f'<text x="{X(0)-14}" y="{Y(BALKON/2)+4}" text-anchor="end" font-size="14" font-weight="800">'
        f'Balkon kapısı {BALKON} cm</text>',
        f'<text x="{X(0)-14}" y="{Y((BALKON+D)/2)}" text-anchor="end" font-size="13" font-weight="700" fill="#555">'
        f'Düz duvar {D-BALKON:.0f} cm</text>',
    ]
    p += dim_v(0, BALKON, -35 / SCALE, f"{BALKON}", "#1565c0")
    p += dim_v(BALKON, D, -35 / SCALE, f"{D-BALKON:.0f}", "#555")

    # sağ segment etiketleri (kapı/kiriş/girinti)
    p += dim_v(0, KAPI, W + 28 / SCALE, f"{KAPI:.0f}", "#1565c0")
    p += dim_v(KAPI, y_k1, W + 28 / SCALE, f"{KIRIS_ALONG}", "#8a1f1f")
    p += dim_v(y_g0, D, W + 28 / SCALE, f"{GIRINTI:.0f}", "#1e8449")

    # köşe orijin
    p.append(
        f'<circle cx="{X(0)}" cy="{Y(0)}" r="5" fill="#8a1f1f"/>'
        f'<text x="{X(0)+8}" y="{Y(0)+16}" font-size="11" fill="#8a1f1f">orijin (0,0) sol-üst iç köşe</text>'
    )
    return p


def draw_furniture(items) -> list[str]:
    colors = {
        "masa": "#111",
        "sandalye": "#333",
        "tv_BESTA": "#1a1a1a",
        "raf": "#2c2c2c",
        "oturma": "#222",
        "hali": None,
        "bjk_saat": None,
        "perde": "#444",
    }
    labels = {
        "masa": "Oyuncu masası\n100×60",
        "sandalye": "Oyuncu\nsandalye",
        "tv_BESTA": "TV + BESTÅ\n120×42",
        "raf": "Raf / kütüphane\n100×35",
        "oturma": "Koltuk\n85×80",
        "hali": "Halı 140×120",
        "bjk_saat": "BJK",
        "perde": "Perde/stor\n(cam üstü)",
    }
    p: list[str] = []
    for it in items:
        if it.name == "hali":
            p.append(
                f'<rect x="{X(it.x)}" y="{Y(it.y)}" width="{it.w*SCALE}" height="{it.h*SCALE}" '
                f'fill="url(#rug)" stroke="#111" stroke-width="1.5"/>'
            )
            p.append(
                f'<text x="{X(it.x+it.w/2)}" y="{Y(it.y+it.h/2)}" text-anchor="middle" '
                f'font-size="13" font-weight="700">{labels[it.name]}</text>'
            )
        elif it.name == "sandalye":
            cx, cy = X(it.x + it.w / 2), Y(it.y + it.h / 2)
            p.append(f'<circle cx="{cx}" cy="{cy}" r="{26*SCALE/1.55}" fill="#333" stroke="#8a1f1f" stroke-width="2"/>')
            p.append(f'<text x="{cx}" y="{cy-2}" text-anchor="middle" font-size="10" fill="#fff" font-weight="700">sandalye</text>')
        elif it.name == "bjk_saat":
            cx, cy = X(it.x + 5), Y(it.y + 5)
            p.append(f'<circle cx="{cx}" cy="{cy}" r="14" fill="#fff" stroke="#8a1f1f" stroke-width="3"/>')
            p.append(f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="9" fill="#8a1f1f" font-weight="800">BJK</text>')
        elif it.name == "perde":
            p.append(
                f'<rect x="{X(it.x)}" y="{Y(it.y)}" width="{it.w*SCALE}" height="{it.h*SCALE}" '
                f'fill="#555" fill-opacity="0.35" stroke="#333" stroke-dasharray="4 2"/>'
            )
            p.append(
                f'<text x="{X(it.x+it.w/2)}" y="{Y(it.y+it.h/2)+4}" text-anchor="middle" '
                f'font-size="11" font-weight="700">perde</text>'
            )
        else:
            fill = colors.get(it.name, "#1a1a1a")
            p.append(
                f'<rect x="{X(it.x)}" y="{Y(it.y)}" width="{it.w*SCALE}" height="{it.h*SCALE}" '
                f'fill="{fill}" stroke="#8a1f1f" stroke-width="2"/>'
            )
            lab = labels.get(it.name, it.name).replace("\n", " · ")
            p.append(
                f'<text x="{X(it.x+it.w/2)}" y="{Y(it.y+it.h/2)+4}" text-anchor="middle" '
                f'font-size="11" fill="#fff" font-weight="700">{lab}</text>'
            )
    return p


def place_all():
    """layout + raf + perde."""
    arch = architecture()
    items, notes = place_furniture(arch)
    # Raf / kütüphane — ÜST duvar (295 düz), salınımlardan uzak
    # balkon salınımı 0..93.5, kapı salınımı sağ üst — orta güvenli
    raf = Rect("raf", 100.0, 2.0, 100.0, 35.0, "item")
    items.append(raf)
    notes.append("RAF/KÜTÜPHANE: üst duvar · 100×35 · kapı/balkon salınımı dışında")

    # Perde — cam bandında, petek önünü kapatmayan ince şerit (duvar çizgisinde)
    x_cam0 = CAM_SOL_PAY
    perde = Rect("perde", x_cam0 + 4, D - 8, CAM - 8, 6.0, "item")
    items.append(perde)
    notes.append("PERDE/STOR: cam 97 cm üstü · petek önü boş kalır")
    return arch, items, notes


def svg_shell(extra_h: float = 120) -> tuple[float, float, list[str]]:
    pw = OX + W * SCALE + 200
    ph = OY + D * SCALE + extra_h
    head = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pw:.0f} {ph:.0f}" font-family="Arial,Helvetica,sans-serif">',
        "<defs>",
        '<pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">',
        '<line x1="0" y1="0" x2="0" y2="7" stroke="#666" stroke-width="1.2"/>',
        "</pattern>",
        '<pattern id="rug" width="14" height="14" patternUnits="userSpaceOnUse">',
        '<rect width="14" height="14" fill="#eee"/>',
        '<path d="M0 0L14 14M14 0L0 14" stroke="#222" stroke-width="0.8"/>',
        "</pattern>",
        "</defs>",
    ]
    return pw, ph, head


def emit_bos(path: Path) -> None:
    _, _, head = svg_shell(140)
    body = draw_empty_room()
    body.append(
        f'<text x="{X(W/2)}" y="{Y(D)+100}" text-anchor="middle" font-size="12" fill="#555">'
        f'Sağ: Kapı {KAPI:.0f} + Kiriş {KIRIS_ALONG} + Girinti {GIRINTI:.0f} = {D} · '
        f'Alt: {CAM_SOL_PAY:.0f}+{CAM:.0f}+{CAM_SAG_PAY:.0f}={W:.0f}</text>'
    )
    path.write_text("\n".join(head + body + ["</svg>"]), encoding="utf-8")


def emit_dolu(path: Path) -> None:
    arch, items, notes = place_all()
    _, _, head = svg_shell(160)
    body = draw_empty_room()
    # retitle
    body[1] = (
        f'<text x="{X(W/2)}" y="{OY-28}" text-anchor="middle" font-size="20" font-weight="800">'
        f'2) MOBİLYALI ODA — aynı net cm</text>'
    )
    body += draw_furniture(items)
    cy = Y(D) + 95
    body.append(
        f'<text x="{X(W/2)}" y="{cy}" text-anchor="middle" font-size="13" font-weight="700">'
        f'Masa · Sandalye · Raf/kütüphane · TV · Koltuk · Halı · Perde</text>'
    )
    cy += 16
    for n in notes[:5]:
        body.append(
            f'<text x="{X(W/2)}" y="{cy}" text-anchor="middle" font-size="11" fill="#8a1f1f">'
            f'{n.replace("&","&amp;")[:110]}</text>'
        )
        cy += 14
    path.write_text("\n".join(head + body + ["</svg>"]), encoding="utf-8")
    # also write ANALIZ snippet
    lines = ["# Net çizim mobilya", ""]
    for it in items:
        lines.append(f"- **{it.name}**: ({it.x:.0f},{it.y:.0f}) {it.w:.0f}×{it.h:.0f}")
    lines += ["", "## Notlar"]
    for n in notes:
        lines.append(f"- {n}")
    (ROOT / "CIZIM.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def elev_full(path: Path) -> None:
    """4 duvar tek panoda — cm + mobilya."""
    arch, items, _ = place_all()
    s = 0.9
    pad = 40
    panel_w = W * s + 40
    panel_h = H_TAVAN * s + 70
    pw = pad * 2 + panel_w * 2 + 40
    ph = pad * 2 + panel_h * 2 + 50

    def panel(ox, oy, title, wall_w, draw_fn):
        out = [
            f'<rect x="{ox}" y="{oy}" width="{wall_w*s}" height="{H_TAVAN*s}" fill="#f5f5f5" stroke="#111" stroke-width="2.5"/>',
            f'<text x="{ox+wall_w*s/2}" y="{oy-12}" text-anchor="middle" font-size="13" font-weight="800">{title}</text>',
        ]
        out += draw_fn(ox, oy)
        return out

    def bottom(ox, oy):
        o = [
            f'<rect x="{ox+CAM_SOL_PAY*s}" y="{oy+70*s}" width="{CAM*s}" height="{100*s}" fill="#b9dff5" stroke="#111"/>',
            f'<text x="{ox+(CAM_SOL_PAY+CAM/2)*s}" y="{oy+125*s}" text-anchor="middle" font-size="12" font-weight="700">Cam {CAM:.0f}</text>',
            f'<rect x="{ox+(CAM_SOL_PAY+8)*s}" y="{oy+175*s}" width="{(CAM-16)*s}" height="{22*s}" fill="#bbb" stroke="#111"/>',
            f'<text x="{ox+(CAM_SOL_PAY+CAM/2)*s}" y="{oy+190*s}" text-anchor="middle" font-size="10">petek</text>',
            # perde
            f'<rect x="{ox+CAM_SOL_PAY*s}" y="{oy+60*s}" width="{CAM*s}" height="{12*s}" fill="#444"/>',
            f'<text x="{ox+(CAM_SOL_PAY+CAM/2)*s}" y="{oy+69*s}" text-anchor="middle" font-size="10" fill="#fff">perde/stor</text>',
            f'<text x="{ox+CAM_SOL_PAY*s/2}" y="{oy+18}" text-anchor="middle" font-size="12" fill="#8a1f1f" font-weight="700">{CAM_SOL_PAY:.0f}</text>',
            f'<text x="{ox+(CAM_SOL_PAY+CAM+CAM_SAG_PAY/2)*s}" y="{oy+18}" text-anchor="middle" font-size="12" fill="#8a1f1f" font-weight="700">{CAM_SAG_PAY:.0f}</text>',
        ]
        for it in items:
            if it.name == "masa":
                mh = 75 * s
                o.append(
                    f'<rect x="{ox+it.x*s}" y="{oy+H_TAVAN*s-mh}" width="{it.w*s}" height="{mh}" fill="#111" stroke="#8a1f1f"/>'
                )
                o.append(
                    f'<text x="{ox+(it.x+it.w/2)*s}" y="{oy+H_TAVAN*s-mh/2}" text-anchor="middle" font-size="11" fill="#fff">masa</text>'
                )
        return o

    def right(ox, oy):
        o = [
            f'<rect x="{ox}" y="{oy}" width="{KAPI*s}" height="{H_TAVAN*s}" fill="#eaeaea" stroke="#111" stroke-dasharray="5 3"/>',
            f'<text x="{ox+KAPI*s/2}" y="{oy+H_TAVAN*s/2}" text-anchor="middle" font-size="12" font-weight="800">Kapı {KAPI:.0f}</text>',
            f'<rect x="{ox+KAPI*s}" y="{oy}" width="{KIRIS_ALONG*s}" height="{36*s}" fill="#111"/>',
            f'<text x="{ox+(KAPI+KIRIS_ALONG/2)*s}" y="{oy+22*s}" text-anchor="middle" font-size="11" fill="#fff">Kiriş {KIRIS_ALONG}×{KIRIS_ICE}</text>',
            f'<text x="{ox+(KAPI+KIRIS_ALONG+GIRINTI/2)*s}" y="{oy+H_TAVAN*s/2}" text-anchor="middle" font-size="12" fill="#1e8449" font-weight="800">Girinti {GIRINTI:.0f}</text>',
        ]
        for it in items:
            if it.name == "oturma":
                sh = 85 * s
                o.append(
                    f'<rect x="{ox+(KAPI+KIRIS_ALONG+5)*s}" y="{oy+H_TAVAN*s-sh}" width="{it.h*s}" height="{sh}" fill="#222"/>'
                )
                o.append(
                    f'<text x="{ox+(KAPI+KIRIS_ALONG+5+it.h/2)*s}" y="{oy+H_TAVAN*s-sh/2}" text-anchor="middle" font-size="11" fill="#fff">koltuk</text>'
                )
        return o

    def left(ox, oy):
        o = [
            f'<rect x="{ox}" y="{oy}" width="{BALKON*s}" height="{H_TAVAN*s}" fill="#eaeaea" stroke="#111" stroke-dasharray="5 3"/>',
            f'<text x="{ox+BALKON*s/2}" y="{oy+H_TAVAN*s/2}" text-anchor="middle" font-size="12" font-weight="800">Balkon {BALKON}</text>',
        ]
        for it in items:
            if it.name == "tv_BESTA":
                uh, th = 48 * s, 45 * s
                o.append(
                    f'<rect x="{ox+it.y*s}" y="{oy+H_TAVAN*s-uh}" width="{it.h*s}" height="{uh}" fill="#1a1a1a"/>'
                )
                o.append(
                    f'<rect x="{ox+(it.y+8)*s}" y="{oy+H_TAVAN*s-uh-th}" width="{(it.h-16)*s}" height="{th}" fill="#111"/>'
                )
                o.append(
                    f'<text x="{ox+(it.y+it.h/2)*s}" y="{oy+H_TAVAN*s-uh/2}" text-anchor="middle" font-size="11" fill="#fff">TV</text>'
                )
            if it.name == "bjk_saat":
                cx = ox + (it.y + 5) * s
                cy = oy + 55 * s
                o.append(f'<circle cx="{cx}" cy="{cy}" r="12" fill="#fff" stroke="#8a1f1f" stroke-width="2"/>')
                o.append(f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="8" fill="#8a1f1f" font-weight="800">BJK</text>')
        return o

    def top(ox, oy):
        o = [
            f'<text x="{ox+W*s/2}" y="{oy+H_TAVAN*s/2}" text-anchor="middle" font-size="13" font-weight="700">'
            f'Üst duvar 295 cm düz · geçiş</text>',
        ]
        for it in items:
            if it.name == "raf":
                rh = 180 * s
                o.append(
                    f'<rect x="{ox+it.x*s}" y="{oy+H_TAVAN*s-rh}" width="{it.w*s}" height="{rh}" fill="#2c2c2c" stroke="#8a1f1f"/>'
                )
                o.append(
                    f'<text x="{ox+(it.x+it.w/2)*s}" y="{oy+H_TAVAN*s-rh/2}" text-anchor="middle" font-size="12" fill="#fff">raf / kütüphane</text>'
                )
        return o

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pw:.0f} {ph:.0f}" font-family="Arial,sans-serif">',
        f'<rect width="{pw:.0f}" height="{ph:.0f}" fill="#0d0d0d"/>',
        f'<text x="{pw/2}" y="28" text-anchor="middle" font-size="18" fill="#fff" font-weight="800">'
        f'4 DUVAR — net cm + mobilya</text>',
    ]
    ox1, oy1 = pad, pad + 20
    ox2, oy2 = pad + panel_w + 30, pad + 20
    ox3, oy3 = pad, pad + panel_h + 30
    ox4, oy4 = pad + panel_w + 30, pad + panel_h + 30
    # light panels on dark bg — wrap each
    for ox, oy, title, ww, fn in [
        (ox1, oy1, f"ALT — 107+Cam{CAM:.0f}+91", W, bottom),
        (ox2, oy2, f"SAĞ — Kapı{KAPI:.0f}+Kiriş+Girinti{GIRINTI:.0f}", D, right),
        (ox3, oy3, f"SOL — Balkon{BALKON}+düz", D, left),
        (ox4, oy4, "ÜST — 295 düz + raf", W, top),
    ]:
        parts.append(f'<rect x="{ox-8}" y="{oy-28}" width="{ww*s+16}" height="{H_TAVAN*s+48}" fill="#1a1a1a" rx="6"/>')
        parts.append(f'<text x="{ox+ww*s/2}" y="{oy-10}" text-anchor="middle" font-size="12" fill="#fff" font-weight="700">{title}</text>')
        parts.append(f'<rect x="{ox}" y="{oy}" width="{ww*s}" height="{H_TAVAN*s}" fill="#f5f5f5" stroke="#fff" stroke-width="2"/>')
        parts += fn(ox, oy)

    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    bos_svg = ROOT / "net-oda-bos.svg"
    dolu_svg = ROOT / "net-oda-dolu.svg"
    duvar_svg = ROOT / "net-4-duvar.svg"
    emit_bos(bos_svg)
    emit_dolu(dolu_svg)
    elev_full(duvar_svg)

    for svg, png_name in [
        (bos_svg, "net-oda-bos.png"),
        (dolu_svg, "net-oda-dolu.png"),
        (duvar_svg, "net-4-duvar.png"),
    ]:
        out = ASSETS / png_name
        cairosvg.svg2png(url=str(svg), write_to=str(out), scale=2.0)
        print("PNG", out)

    # sync main plan from dolu
    import shutil

    shutil.copy(ASSETS / "net-oda-dolu.png", ASSETS / "plan-olcekli.png")
    shutil.copy(ASSETS / "net-oda-dolu.png", ASSETS / "plan.png")
    print("OK — cm-doğru çizimler hazır")


if __name__ == "__main__":
    main()
