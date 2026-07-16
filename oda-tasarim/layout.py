#!/usr/bin/env python3
"""
1903 — boş alan algoritması
Çizim sabitleri kilitli. Mobilya yalnızca hesaplanan boş dikdörtgenlere sığarsa yerleştirilir.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# --- Çizim sabitleri (kullanıcı kilitleri) ---
GAP_START = 2  # cm, sol duvardan kapı öncesi
GAP_KIRIS = 5  # cm, salon kapısı – kiriş
KIRIS_W = 40
KIRIS_D = 10  # odaya içe

# --- Yerinde ölçülünce güncellenecek varsayımlar ---
W = 300  # *
D = 320  # *
DOOR = 80  # *
CAM = 80  # *

# Petek önü ısı payı (mobilya yapışmaz)
PETEK_CLEAR = 25
# Kapı salınımı: menteşe kapının soluna yakın, içe sola (sol duvara yaslanır)
# → alt/üst boş duvarlar salınımdan büyük ölçüde kurtulur; yine de 10 cm pay
DOOR_MARGIN = 10
WALK = 70  # minimum yürüyüş koridoru


@dataclass
class Rect:
    name: str
    x: float  # sol-üst, cm (oda içi, sol-üst köşe = 0,0)
    y: float
    w: float
    h: float
    kind: str  # forbid | zone | item

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
    band = (D - CAM) / 2  # cam ortada → eşit bant
    salon = (GAP_START, GAP_START + DOOR)  # x aralığı
    kiris_x0 = GAP_START + DOOR + GAP_KIRIS
    kiris_x1 = kiris_x0 + KIRIS_W
    balkon = (GAP_START, GAP_START + DOOR)

    forbid = [
        Rect("salon_salinim", salon[0], 0, DOOR, DOOR, "forbid"),
        Rect("balkon_salinim", balkon[0], D - DOOR, DOOR, DOOR, "forbid"),
        Rect("kiris", kiris_x0, 0, KIRIS_W, KIRIS_D, "forbid"),
        Rect("petek_onu", W - PETEK_CLEAR, band, PETEK_CLEAR, CAM, "forbid"),
    ]

    zones = [
        Rect(
            "Z1_ust_bos_duvar",
            kiris_x1,
            0,
            W - kiris_x1,
            90,
            "zone",
        ),  # kiriş sonrası üst duvar — TV
        Rect(
            "Z2_alt_bos_duvar",
            balkon[1] + DOOR_MARGIN,
            D - 95,
            W - (balkon[1] + DOOR_MARGIN),
            95,
            "zone",
        ),  # balkon sağı — oturma
        Rect(
            "Z3a_sag_petek_ustu",
            W - 120,
            0,
            120,
            band,
            "zone",
        ),  # sağ üst bant — masa (tercih: oturma kurtulur)
        Rect(
            "Z3b_sag_petek_alti",
            W - 120,
            band + CAM,
            120,
            band,
            "zone",
        ),  # sağ alt bant — masa yedek
        Rect(
            "Z4_sol_orta",
            0,
            DOOR + DOOR_MARGIN,
            90,
            D - 2 * (DOOR + DOOR_MARGIN),
            "zone",
        ),  # sol orta — kitaplık
    ]

    return {
        "band": band,
        "salon": salon,
        "balkon": balkon,
        "kiris": (kiris_x0, kiris_x1),
        "forbid": forbid,
        "zones": zones,
    }


def place_furniture(arch: dict) -> tuple[list[Rect], list[str]]:
    """Öncelik: dolaşım > (masa+TV+oturma birlikte sığsın) > kitaplık > halı.

    STRATEJİ B (tercih): masa sağ ÜST bantta (petek üstü) → alt duvar tamamen oturmaya kalır.
    STRATEJİ A (yedek): masa sağ ALT bantta → oturma otomatik kısalır.
    """
    notes: list[str] = []
    items: list[Rect] = []
    band = arch["band"]
    kiris_x0, kiris_x1 = arch["kiris"]
    seat_x0 = arch["balkon"][1] + DOOR_MARGIN
    chair_w, chair_d = 60.0, 60.0

    # Masa adayları — TR'de satılan: xDrive 100x60 önce (üst bantta oturmayı bozmaz)
    desk_candidates = [
        (100.0, 60.0, "xDrive Ruzgar 100x60"),
        (100.0, 50.0, "oyuncu masa 100x50"),
        (100.0, 45.0, "oyuncu masa 100x45 / Retodesign"),
        (100.0, 36.0, "IKEA FJALLBO 100x36"),
    ]

    def try_pack(strategy: str):
        """strategy: 'above' | 'below' → (ok, desk, chair, tv, seat, note_list)"""
        local: list[str] = []
        for length, depth, label in desk_candidates:
            if band < length + 8:
                continue
            if strategy == "above":
                desk = Rect("masa", W - depth, 8, depth, length, "item")
                if desk.y2 > band - 5:
                    desk.h = band - 5 - desk.y
                # sandalye masanın altına (oda ortasına), petek önüne yapışmadan
                chair = Rect(
                    "oyuncu_sandalye",
                    desk.x - chair_w - 5,
                    desk.y2 + 5,
                    chair_w,
                    chair_d,
                    "item",
                )
                # sandalye petek önü yasak bölgesine girerse kaydır
                petek = next(f for f in arch["forbid"] if f.name == "petek_onu")
                if chair.overlaps(petek, gap=0):
                    chair.x = min(chair.x, petek.x - chair_w - 5)
            else:
                desk = Rect("masa", W - depth, band + CAM + 8, depth, length, "item")
                if desk.y2 > D - 8:
                    desk.h = D - 8 - desk.y
                chair = Rect(
                    "oyuncu_sandalye",
                    desk.x - chair_w - 5,
                    desk.y + max(0, (desk.h - chair_d) / 2),
                    chair_w,
                    chair_d,
                    "item",
                )

            # TV üst boş — masa üstteyse TV sola, masa ile 10cm pay
            tv_w, tv_d = 120.0, 42.0
            tv_x = kiris_x1 + 8
            tv_max = (desk.x - 10) if strategy == "above" else (W - 10)
            if tv_x + tv_w > tv_max:
                tv_w = tv_max - tv_x
            if tv_w < 80:
                local.append(f"{label}: TV icin ust bos yetersiz")
                continue
            tv = Rect("tv_BESTA", tv_x, 0, tv_w, tv_d, "item")

            # Oturma alt boş — üst stratejide sandalye SE'yi yemez
            seat_depth = 75.0
            if strategy == "above":
                seat_x1 = W - 15  # sağ alt köşe boş
            else:
                seat_x1 = chair.x - 10
            seat_w = seat_x1 - seat_x0
            if seat_w < 70:
                local.append(f"{label}/{strategy}: oturma {seat_w:.0f}cm yetmez")
                continue
            seat_w = min(seat_w, 130.0)
            seat = Rect("oturma", seat_x0, D - seat_depth, seat_w, seat_depth, "item")

            # çakışma
            clash = False
            for a, b in ((desk, tv), (desk, seat), (chair, seat), (chair, tv), (desk, chair)):
                if a.overlaps(b, gap=3):
                    clash = True
                    break
            if clash:
                local.append(f"{label}/{strategy}: cakisma")
                continue

            score = seat_w + tv_w + desk.w  # büyük oturma + TV tercih
            return True, desk, chair, tv, seat, [
                f"STRATEJI {'B masa UST bant' if strategy=='above' else 'A masa ALT bant'}",
                f"MASA: {label}",
                f"Oturma {seat_w:.0f}cm | TV {tv_w:.0f}cm | masa {length:.0f}x{depth:.0f}",
            ], score
        return False, None, None, None, None, local, -1

    # Önce B (üst), olmazsa A (alt)
    best = None
    for strat in ("above", "below"):
        ok, desk, chair, tv, seat, msg, score = try_pack(strat)
        if ok and (best is None or score > best[0]):
            best = (score, desk, chair, tv, seat, msg)
            if strat == "above" and seat.w >= 110:
                break  # iyi paket

    if not best:
        notes.append("RED: hicbir masa+tv+oturma paketi sigmadi — W/D/cam olc")
        return items, notes

    _, desk, chair, tv, seat, msg = best
    notes.extend(msg)
    items.extend([desk, chair, tv, seat])

    # --- Kitaplık: sol orta ---
    book_d = 39.0
    book_h = 100.0
    book_y = 90.0
    left_y0 = DOOR + DOOR_MARGIN
    left_y1 = D - DOOR - DOOR_MARGIN
    if left_y1 - left_y0 >= book_h:
        book_y = left_y0 + (left_y1 - left_y0 - book_h) / 2
        book = Rect("kitaplik", 0, book_y, book_d, book_h, "item")
        if not any(book.overlaps(it, gap=3) for it in items if it.name != "hali"):
            items.append(book)
        else:
            notes.append("Kitaplik cakisti — kitaplar TV unitesinde")
            book_d = 0
    else:
        notes.append("Kitaplik sol orta sigmadi — kitaplar TV unitesinde")
        book_d = 0

    # --- Halı ---
    rug_x = (book_d + 10) if book_d else 50
    rug_x2 = min(desk.x - 5, W - 80)
    rug_y = tv.h + 15
    rug_y2 = seat.y - 10
    if rug_x2 - rug_x >= 80 and rug_y2 - rug_y >= 60:
        items.append(
            Rect(
                "hali",
                rug_x,
                rug_y,
                min(140, rug_x2 - rug_x),
                min(120, rug_y2 - rug_y),
                "item",
            )
        )

    # --- Saat (duvar) ---
    items.append(Rect("bjk_saat_duvar", 2, max(20, book_y - 8), 8, 8, "item"))

    # Zone Z3 label note
    if desk.y < band:
        notes.append("Masa petek UST bandinda — petek onu bos; alt duvar oturmaya acik")
    else:
        notes.append("Masa petek ALT bandinda")

    # global overlap raporu
    for i, a in enumerate(items):
        if a.kind != "item":
            continue
        for b in items[i + 1 :]:
            if b.kind != "item":
                continue
            if a.name.startswith("bjk") or b.name.startswith("bjk"):
                continue
            if a.name == "hali" or b.name == "hali":
                continue  # halı mobilya altına girebilir
            if a.overlaps(b, gap=3):
                notes.append(f"ÇAKIŞMA: {a.name} × {b.name}")

    # dolaşım: salon → balkon sol şerit
    corridor = Rect("koridor", 45, DOOR, 60, D - 2 * DOOR, "zone")
    for it in items:
        if it.name in ("hali", "bjk_saat_duvar"):
            continue
        if it.overlaps(corridor, gap=0) and it.name not in ("kitaplik",):
            # kitaplık sol duvarda koridorun kenarında olabilir
            if it.x2 > corridor.x + 20 and it.name != "kitaplik":
                notes.append(f"UYARI: {it.name} orta koridora taşıyor")

    notes.append(
        f"ÖZET W={W}* D={D}* kapı={DOOR}* cam={CAM}* → sağ bant={band:.0f}cm | "
        f"üst boş={W - kiris_x1:.0f}cm | alt boş≈{W - DOOR - GAP_START - DOOR_MARGIN:.0f}cm"
    )
    return items, notes


def cm_to_px(cm: float, scale: float = 1.2) -> float:
    return cm * scale


def emit_svg(arch: dict, items: list[Rect], notes: list[str], path: Path) -> None:
    scale = 1.2
    ox, oy = 80, 50  # SVG origin
    pw = cm_to_px(W) + 200
    ph = cm_to_px(D) + 220

    def X(cm: float) -> float:
        return ox + cm_to_px(cm)

    def Y(cm: float) -> float:
        return oy + cm_to_px(cm)

    band = arch["band"]
    kiris_x0, kiris_x1 = arch["kiris"]
    salon0, salon1 = arch["salon"]
    bal0, bal1 = arch["balkon"]

    parts: list[str] = [
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
        # oda çerçevesi
        f'<rect x="{X(0)}" y="{Y(0)}" width="{cm_to_px(W)}" height="{cm_to_px(D)}" fill="#fafafa" stroke="#111" stroke-width="3"/>',
    ]

    # yasak bölgeler (açık kırmızı)
    for f in arch["forbid"]:
        parts.append(
            f'<rect x="{X(f.x)}" y="{Y(f.y)}" width="{cm_to_px(f.w)}" height="{cm_to_px(f.h)}" '
            f'fill="#c0392b" fill-opacity="0.18" stroke="#c0392b" stroke-dasharray="4 2"/>'
        )
        parts.append(
            f'<text x="{X(f.x + f.w/2)}" y="{Y(f.y + f.h/2)}" text-anchor="middle" font-size="8" fill="#8a1f1f">{f.name}</text>'
        )

    # boş bölgeler (yeşil)
    for z in arch["zones"]:
        parts.append(
            f'<rect x="{X(z.x)}" y="{Y(z.y)}" width="{cm_to_px(z.w)}" height="{cm_to_px(z.h)}" '
            f'fill="#1e8449" fill-opacity="0.10" stroke="#1e8449" stroke-dasharray="3 3"/>'
        )

    # kapılar
    parts.append(
        f'<rect x="{X(salon0)}" y="{Y(0)-6}" width="{cm_to_px(DOOR)}" height="12" fill="url(#hatch)" stroke="#111"/>'
    )
    parts.append(
        f'<text x="{X((salon0+salon1)/2)}" y="{Y(0)-12}" text-anchor="middle" font-size="11" font-weight="700">Salon Kapisi</text>'
    )
    parts.append(
        f'<path d="M{X(salon0)} {Y(0)} A{cm_to_px(DOOR)} {cm_to_px(DOOR)} 0 0 1 {X(salon0)} {Y(DOOR)}" '
        f'fill="none" stroke="#888" stroke-dasharray="3 2"/>'
    )

    parts.append(
        f'<rect x="{X(bal0)}" y="{Y(D)-6}" width="{cm_to_px(DOOR)}" height="12" fill="url(#hatch)" stroke="#111"/>'
    )
    parts.append(
        f'<text x="{X((bal0+bal1)/2)}" y="{Y(D)+22}" text-anchor="middle" font-size="11" font-weight="700">Balkon Kapisi</text>'
    )
    parts.append(
        f'<path d="M{X(bal0)} {Y(D)} A{cm_to_px(DOOR)} {cm_to_px(DOOR)} 0 0 0 {X(bal0)} {Y(D-DOOR)}" '
        f'fill="none" stroke="#888" stroke-dasharray="3 2"/>'
    )

    # kiriş
    parts.append(
        f'<rect x="{X(kiris_x0)}" y="{Y(0)}" width="{cm_to_px(KIRIS_W)}" height="{cm_to_px(KIRIS_D)}" fill="#111"/>'
    )
    parts.append(
        f'<text x="{X((kiris_x0+kiris_x1)/2)}" y="{Y(KIRIS_D)+14}" text-anchor="middle" font-size="10" fill="#8a1f1f" font-weight="700">Kiris 40x10</text>'
    )

    # cam + petek ortada
    parts.append(
        f'<rect x="{X(W)-6}" y="{Y(band)}" width="12" height="{cm_to_px(CAM)}" fill="url(#hatch)" stroke="#111"/>'
    )
    parts.append(
        f'<rect x="{X(W-15)}" y="{Y(band+10)}" width="{cm_to_px(12)}" height="{cm_to_px(CAM-20)}" fill="#c8c8c8" stroke="#111"/>'
    )
    parts.append(
        f'<text x="{X(W)+8}" y="{Y(band + CAM/2)}" font-size="11" font-weight="700">Cam ORTA</text>'
    )
    parts.append(
        f'<text x="{X(W)+8}" y="{Y(band + CAM/2)+14}" font-size="10" fill="#8a1f1f">Petek</text>'
    )
    parts.append(
        f'<text x="{X(W)+8}" y="{Y(band/2)}" font-size="10" fill="#8a1f1f" font-weight="700">{band:.0f}*</text>'
    )
    parts.append(
        f'<text x="{X(W)+8}" y="{Y(band + CAM + band/2)}" font-size="10" fill="#8a1f1f" font-weight="700">{band:.0f}*</text>'
    )

    # ölçü etiketleri
    parts.append(
        f'<text x="{X(1)}" y="{Y(0)-12}" font-size="10" fill="#8a1f1f" font-weight="700">2</text>'
    )
    parts.append(
        f'<text x="{X(GAP_START+DOOR+GAP_KIRIS/2)}" y="{Y(0)-12}" font-size="10" fill="#8a1f1f" font-weight="700">5cm</text>'
    )

    colors = {
        "masa_xDrive": "#111",
        "oyuncu_sandalye": "#333",
        "tv_BESTA_alt": "#1a1a1a",
        "oturma": "#222",
        "kitaplik": "#1a1a1a",
        "hali": None,
        "bjk_saat_duvar": None,
    }

    for it in items:
        if it.name == "hali":
            parts.append(
                f'<rect x="{X(it.x)}" y="{Y(it.y)}" width="{cm_to_px(it.w)}" height="{cm_to_px(it.h)}" '
                f'fill="url(#rug)" stroke="#111"/>'
            )
            parts.append(
                f'<text x="{X(it.x+it.w/2)}" y="{Y(it.y+it.h/2)}" text-anchor="middle" font-size="9">hali {it.w:.0f}x{it.h:.0f}</text>'
            )
        elif it.name == "bjk_saat_duvar":
            parts.append(
                f'<circle cx="{X(it.x+4)}" cy="{Y(it.y+4)}" r="9" fill="#fff" stroke="#8a1f1f" stroke-width="2"/>'
            )
            parts.append(
                f'<text x="{X(it.x+4)}" y="{Y(it.y+6)}" text-anchor="middle" font-size="7" fill="#8a1f1f" font-weight="700">BJK</text>'
            )
        elif it.name == "oyuncu_sandalye":
            cx, cy = X(it.x + it.w / 2), Y(it.y + it.h / 2)
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{cm_to_px(28)}" fill="#333" stroke="#8a1f1f" stroke-width="1.5"/>')
            parts.append(
                f'<text x="{cx}" y="{cy+3}" text-anchor="middle" font-size="7" fill="#fff">sandalye</text>'
            )
        else:
            fill = colors.get(it.name, "#111")
            parts.append(
                f'<rect x="{X(it.x)}" y="{Y(it.y)}" width="{cm_to_px(it.w)}" height="{cm_to_px(it.h)}" '
                f'fill="{fill}" stroke="#8a1f1f" stroke-width="1.5"/>'
            )
            label = f"{it.name} {it.w:.0f}x{it.h:.0f}" if it.w >= it.h else f"{it.name} {it.h:.0f}x{it.w:.0f}"
            parts.append(
                f'<text x="{X(it.x+it.w/2)}" y="{Y(it.y+it.h/2)}" text-anchor="middle" font-size="8" fill="#fff">{label}</text>'
            )

    # zone labels
    zone_labels = {
        "Z1_ust_bos_duvar": "Z1 TV",
        "Z2_alt_bos_duvar": "Z2 oturma",
        "Z3a_sag_petek_ustu": "Z3a masa",
        "Z3b_sag_petek_alti": "Z3b yedek",
        "Z4_sol_orta": "Z4 kitaplik",
    }
    for z in arch["zones"]:
        parts.append(
            f'<text x="{X(z.x + 4)}" y="{Y(z.y + 12)}" font-size="9" fill="#1e8449" font-weight="700">{zone_labels.get(z.name, z.name)}</text>'
        )

    # alt notlar
    cy = Y(D) + 50
    parts.append(
        f'<text x="{X(W/2)}" y="{cy}" text-anchor="middle" font-size="13" font-weight="700">ALGORITMA PLAN — bos alanlara yerlesim</text>'
    )
    cy += 16
    parts.append(
        f'<text x="{X(W/2)}" y="{cy}" text-anchor="middle" font-size="10" fill="#555">'
        f"yesil=bos bolge | kirmizi=yasak (kapi/kiris/petek) | * yerinde olc | olcek 1.2px=1cm</text>"
    )
    cy += 14
    def esc(s: str) -> str:
        return (
            s.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    for n in notes[:8]:
        parts.append(
            f'<text x="{X(W/2)}" y="{cy}" text-anchor="middle" font-size="9" fill="#8a1f1f">{esc(n[:110])}</text>'
        )
        cy += 12

    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def emit_report(arch: dict, items: list[Rect], notes: list[str], path: Path) -> None:
    band = arch["band"]
    _, kiris_x1 = arch["kiris"]
    lines = [
        "# Yerleşim analizi (algoritma)",
        "",
        "## 1) Mimari kilit",
        f"- W={W}* D={D}* kapı={DOOR}* cam={CAM}*",
        f"- Üst: 2 + kapı + 5 + kiriş40 → üst boş duvar = **{W - kiris_x1:.0f} cm**",
        f"- Sağ: cam ortada → bant = **{band:.0f} cm** (petek önü +{PETEK_CLEAR}cm yasak)",
        f"- Alt: balkon sonrası boş ≈ **{W - DOOR - GAP_START - DOOR_MARGIN:.0f} cm**",
        f"- Sol orta (salınımlar arası) ≈ **{D - 2*(DOOR + DOOR_MARGIN):.0f} cm**",
        "",
        "## 2) Boş bölgeler → fonksiyon",
        "| Bölge | Duvar | Fonksiyon | Neden |",
        "|-------|-------|-----------|-------|",
        "| Z1 | Üst, kiriş sonrası | TV ünitesi | En uzun boş duvar; koltuğa bakar |",
        "| Z2 | Alt, balkon sağı | Oturma | İkinci uzun boş duvar; TV’ye bakar |",
        "| Z3a | Sağ, petek üstü | Masa+PC+sandalye (tercih) | Alt duvarı oturmaya bırakır |",
        "| Z3b | Sağ, petek altı | Masa yedek | Üst sığmazsa; oturma kısalır |",
        "| Z4 | Sol orta | Kitaplık | Kapı salınımlarının arasında |",
        "",
        "## 3) Yerleşen ürünler (cm)",
    ]
    for it in items:
        if it.kind == "item":
            lines.append(f"- **{it.name}**: x={it.x:.0f} y={it.y:.0f} → {it.w:.0f}×{it.h:.0f} cm")
    lines += ["", "## 4) Algoritma notları"]
    for n in notes:
        lines.append(f"- {n}")
    lines += [
        "",
        "## 5) Mantık özeti",
        "- AI perspektif fotoğraf duvar/kapı uydurabilir → **sipariş gerçeği bu plan + cm**.",
        "- 300×320 odada **100×60 masa + 140 ikili koltuk aynı anda sığmaz**; algoritma oturmayı otomatik kısar.",
        "- Ayrı uzun kitaplık + geniş TV + derin masa seçilirse birini küçült.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parent
    arch = architecture()
    items, notes = place_furniture(arch)
    emit_svg(arch, items, notes, root / "plan.svg")
    emit_report(arch, items, notes, root / "ANALIZ.md")
    print("OK plan.svg + ANALIZ.md")
    for n in notes:
        print(" ·", n)
    for it in items:
        print(f"   {it.name}: ({it.x:.0f},{it.y:.0f}) {it.w:.0f}x{it.h:.0f}")


if __name__ == "__main__":
    main()
