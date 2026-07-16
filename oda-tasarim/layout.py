#!/usr/bin/env python3
"""
1903 — NET ÖLÇÜ planı (kullanıcı krokisi)
Doğaçlama yok. Tüm cm OLCULER.md ile aynı.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# ===== NET ÖLÇÜLER (kilit) =====
W = 295.0
D = 295.5  # 106 + 64.5 + 125
H_TAVAN = 255.0

KAPI = 106.0  # sağ üst
BALKON = 93.5  # sol üst
KIRIS_ALONG = 64.5  # sağ duvar boyunca, kapıdan sonra
KIRIS_ICE = 15.0  # odaya içe
GIRINTI = 125.0  # sağ duvar alt segment

CAM = 97.0
CAM_SOL_PAY = 107.0  # alt duvarda camdan sola
CAM_SAG_PAY = 91.0  # alt duvarda camdan sağa  (107+97+91=295)

PETEK_CLEAR = 25.0
DOOR_MARGIN = 8.0


@dataclass
class Rect:
    name: str
    x: float
    y: float
    w: float
    h: float
    kind: str = "item"

    @property
    def x2(self) -> float:
        return self.x + self.w

    @property
    def y2(self) -> float:
        return self.y + self.h

    def overlaps(self, o: "Rect", gap: float = 0) -> bool:
        return not (
            self.x2 + gap <= o.x
            or o.x2 + gap <= self.x
            or self.y2 + gap <= o.y
            or o.y2 + gap <= self.y
        )


def architecture() -> dict:
    # sağ duvar y parçaları
    y_kapi0, y_kapi1 = 0.0, KAPI
    y_kiris0, y_kiris1 = KAPI, KAPI + KIRIS_ALONG
    y_gir0, y_gir1 = y_kiris1, D  # 170.5 → 295.5

    # alt duvar cam
    x_cam0 = CAM_SOL_PAY
    x_cam1 = CAM_SOL_PAY + CAM

    forbid = [
        Rect("kapi_salinim", W - KAPI, 0, KAPI, KAPI, "forbid"),  # yaklaşık içe yay
        Rect("balkon_salinim", 0, 0, BALKON, BALKON, "forbid"),
        Rect("kiris", W - KIRIS_ICE, y_kiris0, KIRIS_ICE, KIRIS_ALONG, "forbid"),
        Rect("petek_onu", x_cam0, D - PETEK_CLEAR, CAM, PETEK_CLEAR, "forbid"),
    ]
    zones = [
        Rect("Z_masa_cam_solu", 0, D - 90, CAM_SOL_PAY, 90, "zone"),
        Rect("Z_tv_sol", 0, BALKON + DOOR_MARGIN, 90, D - BALKON - DOOR_MARGIN - 40, "zone"),
        Rect("Z_oturma_girinti", W - 100, y_gir0, 100, GIRINTI, "zone"),
        Rect("Z_ust_bos", 40, 0, W - 80, 90, "zone"),
    ]
    return {
        "forbid": forbid,
        "zones": zones,
        "y_kapi": (y_kapi0, y_kapi1),
        "y_kiris": (y_kiris0, y_kiris1),
        "y_girinti": (y_gir0, y_gir1),
        "x_cam": (x_cam0, x_cam1),
    }


def place_furniture(arch: dict) -> tuple[list[Rect], list[str]]:
    notes: list[str] = []
    items: list[Rect] = []
    x_cam0, x_cam1 = arch["x_cam"]
    y_gir0, y_gir1 = arch["y_girinti"]

    notes.append(f"NET: W={W} D={D} H={H_TAVAN} | kapı={KAPI} balkon={BALKON} cam={CAM}")
    notes.append(f"Kiriş {KIRIS_ALONG}×{KIRIS_ICE} | girinti duvar {GIRINTI} | cam pay {CAM_SOL_PAY}|{CAM}|{CAM_SAG_PAY}")

    # 1) MASA — alt duvar, camın SOLU (107 cm bant). 100×60 sığar.
    desk_len, desk_dep = 100.0, 60.0
    if CAM_SOL_PAY < desk_len + 6:
        desk_len = CAM_SOL_PAY - 6
        notes.append(f"Masa boyu {desk_len:.0f}cm'ye kırpıldı (cam sol pay {CAM_SOL_PAY})")
    desk = Rect("masa", 4.0, D - desk_dep - 2, desk_len, desk_dep, "item")
    # petek ile çakışma kontrol
    petek = next(f for f in arch["forbid"] if f.name == "petek_onu")
    if desk.overlaps(petek, gap=2):
        desk.w = min(desk.w, x_cam0 - 6 - desk.x)
        notes.append("Masa petekten uzaklaştırıldı")
    items.append(desk)
    notes.append(f"MASA: alt-sol cam yanı · {desk.w:.0f}×{desk.h:.0f} · petek ÖNÜNE değil YANINA")

    # sandalye masanın üstünde (oda içine)
    chair = Rect("sandalye", desk.x + 20, desk.y - 65, 60, 60, "item")
    items.append(chair)

    # 2) TV — sol duvar, balkon altında
    tv_h = 120.0
    tv_y0 = BALKON + DOOR_MARGIN + 10
    if tv_y0 + tv_h > D - 30:
        tv_h = D - 30 - tv_y0
    tv = Rect("tv_BESTA", 0, tv_y0, 42, tv_h, "item")
    items.append(tv)
    notes.append(f"TV: sol duvar · BESTÅ {tv.h:.0f}×42 · balkon salınımı altında")

    # 3) OTURMA — sağ girinti duvar boyunca, TV'ye (sola) bakar
    seat_depth = 75.0
    seat_w = min(120.0, GIRINTI - 10)
    seat = Rect(
        "oturma",
        W - seat_depth - 2,
        y_gir0 + 5,
        seat_depth,
        seat_w,
        "item",
    )
    # kapı/kiriş ile çakışma
    if seat.y < arch["y_kiris"][1] + 5:
        seat.y = arch["y_kiris"][1] + 5
        seat.h = min(seat.h, D - seat.y - 5)
    items.append(seat)
    notes.append(f"OTURMA: sağ girinti · {seat.h:.0f}×{seat.w:.0f} (duvar boyunca×derinlik) · TV'ye bakar")

    # 4) HALI orta
    rug = Rect("hali", 55, 100, 140, 120, "item")
    items.append(rug)

    # 5) BJK saat sol duvar TV üstü
    items.append(Rect("bjk_saat", 2, tv.y - 15, 10, 10, "item"))

    # çakışma raporu
    for i, a in enumerate(items):
        for b in items[i + 1 :]:
            if a.name in ("hali", "bjk_saat") or b.name in ("hali", "bjk_saat"):
                continue
            if a.overlaps(b, gap=2):
                notes.append(f"ÇAKIŞMA: {a.name} × {b.name}")

    return items, notes


def emit_svg(arch: dict, items: list[Rect], notes: list[str], path: Path) -> None:
    scale = 1.4
    ox, oy = 70, 50

    def X(cm: float) -> float:
        return ox + cm * scale

    def Y(cm: float) -> float:
        return oy + cm * scale

    pw = ox + W * scale + 160
    ph = oy + D * scale + 200
    x_cam0, x_cam1 = arch["x_cam"]
    y_k0, y_k1 = arch["y_kiris"]
    y_g0, y_g1 = arch["y_girinti"]

    p: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pw:.0f} {ph:.0f}" font-family="Arial,sans-serif">',
        "<defs>",
        '<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">',
        '<line x1="0" y1="0" x2="0" y2="6" stroke="#666" stroke-width="1"/>',
        "</pattern>",
        '<pattern id="rug" width="10" height="10" patternUnits="userSpaceOnUse">',
        '<rect width="10" height="10" fill="#eee"/>',
        '<path d="M0 0L10 10M10 0L0 10" stroke="#222" stroke-width="0.7"/>',
        "</pattern>",
        "</defs>",
        f'<rect x="{X(0)}" y="{Y(0)}" width="{W*scale}" height="{D*scale}" fill="#fafafa" stroke="#111" stroke-width="3"/>',
        f'<text x="{X(W/2)}" y="28" text-anchor="middle" font-size="16" font-weight="700">NET PLAN — W={W:.0f} · D={D} · H={H_TAVAN:.0f}</text>',
    ]

    # yasak
    for f in arch["forbid"]:
        p.append(
            f'<rect x="{X(f.x)}" y="{Y(f.y)}" width="{f.w*scale}" height="{f.h*scale}" '
            f'fill="#c0392b" fill-opacity="0.15" stroke="#c0392b" stroke-dasharray="4 2"/>'
        )

    # üst duvar etiketi
    p.append(f'<text x="{X(W/2)}" y="{Y(0)-8}" text-anchor="middle" font-size="12" font-weight="700">ÜST DUVAR 295cm (düz)</text>')

    # sağ: kapı
    p.append(
        f'<rect x="{X(W)-6}" y="{Y(0)}" width="12" height="{KAPI*scale}" fill="url(#hatch)" stroke="#111"/>'
    )
    p.append(
        f'<text x="{X(W)+10}" y="{Y(KAPI/2)}" font-size="12" font-weight="700">Kapı {KAPI:.0f}</text>'
    )
    # kiriş
    p.append(
        f'<rect x="{X(W-KIRIS_ICE)}" y="{Y(y_k0)}" width="{KIRIS_ICE*scale}" height="{KIRIS_ALONG*scale}" fill="#111"/>'
    )
    p.append(
        f'<text x="{X(W)+10}" y="{Y((y_k0+y_k1)/2)}" font-size="11" fill="#8a1f1f" font-weight="700">Kiriş {KIRIS_ALONG}×{KIRIS_ICE}</text>'
    )
    # girinti
    p.append(
        f'<text x="{X(W)+10}" y="{Y((y_g0+y_g1)/2)}" font-size="11" fill="#1e8449" font-weight="700">Girinti {GIRINTI:.0f}</text>'
    )

    # alt: cam + petek
    p.append(
        f'<rect x="{X(x_cam0)}" y="{Y(D)-6}" width="{CAM*scale}" height="12" fill="url(#hatch)" stroke="#111"/>'
    )
    p.append(
        f'<rect x="{X(x_cam0+8)}" y="{Y(D-18)}" width="{(CAM-16)*scale}" height="{14*scale}" fill="#c8c8c8" stroke="#111"/>'
    )
    p.append(
        f'<text x="{X((x_cam0+x_cam1)/2)}" y="{Y(D)+28}" text-anchor="middle" font-size="12" font-weight="700">Cam {CAM:.0f} · altında petek</text>'
    )
    p.append(
        f'<text x="{X(CAM_SOL_PAY/2)}" y="{Y(D)+28}" text-anchor="middle" font-size="11" fill="#8a1f1f">{CAM_SOL_PAY:.0f}</text>'
    )
    p.append(
        f'<text x="{X(x_cam1+CAM_SAG_PAY/2)}" y="{Y(D)+28}" text-anchor="middle" font-size="11" fill="#8a1f1f">{CAM_SAG_PAY:.0f}</text>'
    )

    # sol: balkon
    p.append(
        f'<rect x="{X(0)-6}" y="{Y(0)}" width="12" height="{BALKON*scale}" fill="url(#hatch)" stroke="#111"/>'
    )
    p.append(
        f'<text x="{X(0)-12}" y="{Y(BALKON/2)}" text-anchor="end" font-size="11" font-weight="700">Balkon {BALKON}</text>'
    )

    # mobilya
    for it in items:
        if it.name == "hali":
            p.append(
                f'<rect x="{X(it.x)}" y="{Y(it.y)}" width="{it.w*scale}" height="{it.h*scale}" fill="url(#rug)" stroke="#111"/>'
            )
            p.append(
                f'<text x="{X(it.x+it.w/2)}" y="{Y(it.y+it.h/2)}" text-anchor="middle" font-size="11">halı</text>'
            )
        elif it.name == "sandalye":
            cx, cy = X(it.x + it.w / 2), Y(it.y + it.h / 2)
            p.append(f'<circle cx="{cx}" cy="{cy}" r="{28*scale/1.4}" fill="#333" stroke="#8a1f1f"/>')
            p.append(f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="9" fill="#fff">sandalye</text>')
        elif it.name == "bjk_saat":
            cx, cy = X(it.x + 5), Y(it.y + 5)
            p.append(f'<circle cx="{cx}" cy="{cy}" r="12" fill="#fff" stroke="#8a1f1f" stroke-width="2"/>')
            p.append(f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="8" fill="#8a1f1f" font-weight="700">BJK</text>')
        else:
            p.append(
                f'<rect x="{X(it.x)}" y="{Y(it.y)}" width="{it.w*scale}" height="{it.h*scale}" fill="#1a1a1a" stroke="#8a1f1f" stroke-width="1.5"/>'
            )
            p.append(
                f'<text x="{X(it.x+it.w/2)}" y="{Y(it.y+it.h/2)}" text-anchor="middle" font-size="10" fill="#fff">{it.name}</text>'
            )

    cy = Y(D) + 55
    p.append(f'<text x="{X(W/2)}" y="{cy}" text-anchor="middle" font-size="13" font-weight="700">Beşiktaş oyuncu odası — kroki cm kilitli</text>')
    cy += 18
    for n in notes[:7]:
        p.append(
            f'<text x="{X(W/2)}" y="{cy}" text-anchor="middle" font-size="10" fill="#8a1f1f">'
            f'{n.replace("&","&amp;").replace("<","&lt;")[:120]}</text>'
        )
        cy += 14
    p.append("</svg>")
    path.write_text("\n".join(p), encoding="utf-8")


def emit_analiz(items: list[Rect], notes: list[str], path: Path) -> None:
    lines = [
        "# Analiz — net kroki",
        "",
        "## Ölçü",
        f"- W = **{W:.0f} cm** (107 + cam 97 + 91)",
        f"- D = **{D} cm** (kapı 106 + kiriş 64,5 + girinti 125)",
        f"- Kiriş içe = **{KIRIS_ICE:.0f} cm**",
        f"- Tavan = **{H_TAVAN:.0f} cm**",
        "",
        "## Yerleşim mantığı",
        "1. **Masa** alt-sol: cam sol payı 107 cm → 100×60 masa sığar; petek önüne değil **yanına**.",
        "2. **TV** sol duvar: balkon (93,5) altında uzun düz duvar.",
        "3. **Oturma** sağ girinti (125 cm): TV’ye bakar; kapı/kiriş zonunun altında.",
        "4. Üst 295 cm düz: geçiş + dekor; ağır depo yok.",
        "",
        "## Ürünler (cm)",
    ]
    for it in items:
        lines.append(f"- **{it.name}**: ({it.x:.0f},{it.y:.0f}) {it.w:.0f}×{it.h:.0f}")
    lines += ["", "## Notlar"]
    for n in notes:
        lines.append(f"- {n}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parent
    arch = architecture()
    items, notes = place_furniture(arch)
    emit_svg(arch, items, notes, root / "plan.svg")
    emit_analiz(items, notes, root / "ANALIZ.md")
    print("OK")
    for n in notes:
        print(" ·", n)
    for it in items:
        print(f"   {it.name}: ({it.x:.1f},{it.y:.1f}) {it.w:.0f}x{it.h:.0f}")


if __name__ == "__main__":
    main()
