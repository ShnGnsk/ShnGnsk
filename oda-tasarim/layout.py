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

# --- Kullanıcı: standart kapı + 2'li cam | W/D hâlâ yerinde ölç (*) ---
W = 300  # *
D = 320  # *
DOOR = 90  # standart oda/salon kapısı (duvar boşluğu ~90 cm, kanat ~80)
CAM = 140  # 2'li (çift kanat) cam — sağ duvar boyunca tipik genişlik
# Not: cam büyüyünce bant=(D-CAM)/2 küçülür → 100'lük masa sığmayabilir; algoritma kısaltır.

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

    2'li cam → bant daralır. Bant < masa boyu ise masa KISA KENARI duvarda (end-on).
    """
    notes: list[str] = []
    items: list[Rect] = []
    band = arch["band"]
    kiris_x0, kiris_x1 = arch["kiris"]
    seat_x0 = arch["balkon"][1] + DOOR_MARGIN
    chair_w, chair_d = 60.0, 60.0
    petek = next(f for f in arch["forbid"] if f.name == "petek_onu")

    notes.append(
        f"Kilit: standart kapi={DOOR}cm | 2li cam={CAM}cm | bant=(D-cam)/2={band:.0f}cm"
    )

    # (duvar_boyu, oda_icine, etiket, orient) — parallel veya end-on
    desk_candidates: list[tuple[float, float, str, str]] = []
    for length, depth, label in [
        (100.0, 60.0, "xDrive Ruzgar 100x60"),
        (100.0, 50.0, "oyuncu masa 100x50"),
        (90.0, 50.0, "oyuncu masa 90x50"),
        (80.0, 60.0, "oyuncu masa 80x60"),
        (100.0, 45.0, "oyuncu masa 100x45"),
        (100.0, 36.0, "IKEA FJALLBO 100x36"),
    ]:
        # paralel: uzun kenar duvarda
        desk_candidates.append((length, depth, f"{label} paralel", "parallel"))
        # end-on: kisa kenar duvarda (dar bant / 2li cam)
        desk_candidates.append((depth, length, f"{label} end-on (kisa kenar duvarda)", "endon"))

    def place_desk(strategy: str, along: float, into: float, orient: str):
        """along = sağ duvar boyunca, into = odaya. Sandalye uzun kenarda (oturmayı yemez)."""
        if band < along + 6:
            return None, None
        if strategy == "above":
            y0 = 6.0
            if y0 + along > band - 4:
                return None, None
            desk = Rect("masa", W - into, y0, into, along, "item")
            if orient == "endon":
                # uzun kenarın altına otur — x masa ile hizalı kalır, alt oturma kurtulur
                cx = desk.x + max(0.0, (desk.w - chair_w) / 2)
                cy = desk.y2 + 5
                chair = Rect("oyuncu_sandalye", cx, cy, chair_w, chair_d, "item")
                if chair.overlaps(petek, gap=2):
                    chair.x = min(chair.x, petek.x - chair_w - 5)
                    if chair.overlaps(petek, gap=2):
                        return None, None
            else:
                chair = Rect(
                    "oyuncu_sandalye",
                    desk.x - chair_w - 5,
                    desk.y2 + 5,
                    chair_w,
                    chair_d,
                    "item",
                )
                if chair.overlaps(petek, gap=2):
                    chair.x = petek.x - chair_w - 5
        else:
            y0 = band + CAM + 6
            if y0 + along > D - 6:
                return None, None
            desk = Rect("masa", W - into, y0, into, along, "item")
            if orient == "endon":
                # uzun kenarın üstüne (petekten uzak içe) otur
                cx = desk.x + max(0.0, (desk.w - chair_w) / 2)
                cy = desk.y - chair_d - 5
                if cy < band + CAM + PETEK_CLEAR:
                    # petek bandına giriyorsa batı kısa uca ama masa dibine yakın
                    cx = desk.x - chair_w - 5
                    cy = desk.y + max(0.0, (desk.h - chair_d) / 2)
                chair = Rect("oyuncu_sandalye", cx, cy, chair_w, chair_d, "item")
                if chair.overlaps(petek, gap=2):
                    return None, None
            else:
                chair = Rect(
                    "oyuncu_sandalye",
                    desk.x - chair_w - 5,
                    desk.y + max(0.0, (desk.h - chair_d) / 2),
                    chair_w,
                    chair_d,
                    "item",
                )
        if chair.x < 40 or chair.y < 0 or chair.y2 > D:
            return None, None
        return desk, chair

    def place_tv_seat(strategy: str, desk: Rect, chair: Rect, tv_on_left: bool):
        seat_depth = 75.0
        # oturma sağ sınırı: SE köşedeki masa/sandalye
        blockers = [desk.x - 8]
        if chair.y2 > D - seat_depth - 20:  # sandalye alt bölgedeyse
            blockers.append(chair.x - 8)
        if strategy == "below" or chair.y > band:
            blockers.append(chair.x - 8)
            blockers.append(desk.x - 8)

        if tv_on_left:
            left_y0 = DOOR + DOOR_MARGIN
            left_clear = D - 2 * (DOOR + DOOR_MARGIN)
            tv_h = min(120.0, left_clear)
            tv_y = left_y0 + (left_clear - tv_h) / 2
            tv = Rect("tv_BESTA", 0, tv_y, 42.0, tv_h, "item")
            # üst strateji + sandalye üstteyse alt duvar neredeyse tam boş
            if strategy == "above" and chair.y2 < D - seat_depth - 30:
                seat_x1 = W - 15
            else:
                seat_x1 = min(blockers + [W - 15])
        else:
            tv_w, tv_d = 120.0, 42.0
            tv_x = kiris_x1 + 8
            tv_max = W - 10
            if strategy == "above":
                tv_max = min(tv_max, desk.x - 10)
                if chair.y < 80:
                    tv_max = min(tv_max, chair.x - 5)
            if tv_x + tv_w > tv_max:
                tv_w = tv_max - tv_x
            if tv_w < 80:
                return None, None
            tv = Rect("tv_BESTA", tv_x, 0, tv_w, tv_d, "item")
            if strategy == "above" and chair.y2 < D - seat_depth - 30:
                seat_x1 = W - 15
            else:
                seat_x1 = min(blockers + [W - 15])

        seat_w = seat_x1 - seat_x0
        if seat_w < 70:
            return None, None
        seat_w = min(130.0, seat_w)
        seat = Rect("oturma", seat_x0, D - seat_depth, seat_w, seat_depth, "item")
        return tv, seat

    def clashes(desk, chair, tv, seat) -> bool:
        pairs = ((desk, tv), (desk, seat), (chair, seat), (chair, tv), (desk, chair))
        return any(a.overlaps(b, gap=3) for a, b in pairs)

    best = None
    fail_notes: list[str] = []
    # 2'li cam dar bant: önce end-on + gerekirse TV solda
    for strategy in ("above", "below"):
        for along, into, label, orient in desk_candidates:
            desk, chair = place_desk(strategy, along, into, orient)
            if desk is None:
                continue
            # end-on üst + derin → TV genelde sol; paralel / alt → TV üst dene
            if orient == "endon" and strategy == "above" and into >= 80:
                tv_options = (True, False)
            else:
                tv_options = (False, True)
            for use_left in tv_options:
                tv, seat = place_tv_seat(strategy, desk, chair, use_left)
                if tv is None or seat is None:
                    continue
                if clashes(desk, chair, tv, seat):
                    continue
                score = seat.w + (tv.w if tv.h < 50 else tv.h) + min(along, into)
                if not use_left:
                    score += 40
                if strategy == "above":
                    score += 20
                if orient == "parallel":
                    score += 15
                # 2'li cam: bant dar → 100'luk masa ancak end-on; bunu ödüllendir
                if band < 100 and orient == "endon" and into >= 100:
                    score += 55
                if "xDrive" in label and into >= 100:
                    score += 25
                msg = [
                    f"STRATEJI {'B ust' if strategy=='above' else 'A alt'} | {orient}",
                    f"MASA: {label} (duvarda {along:.0f} / ice {into:.0f})",
                    f"TV: {'sol duvar' if use_left else 'ust bos duvar'} | oturma {seat.w:.0f}cm",
                ]
                if best is None or score > best[0]:
                    best = (score, desk, chair, tv, seat, msg, use_left)

    if not best:
        notes.append(
            f"RED: paket sigmadi. Bant={band:.0f}cm (2li cam {CAM}). "
            "D olc; cam duvar boyu olc; daha kisa masa gerekebilir."
        )
        notes.extend(fail_notes[:5])
        return items, notes

    _, desk, chair, tv, seat, msg, tv_on_left = best
    notes.extend(msg)
    items.extend([desk, chair, tv, seat])
    # kitaplık bayrağı: TV soldaysa kitap TV ile birlikte
    notes.append("TV_ON_LEFT" if tv_on_left else "TV_ON_TOP")

    # --- Kitaplık: TV soldaysa kitap TV ünitesinde; değilse sol orta ---
    book_d = 0.0
    book_y = tv.y if tv_on_left else 90.0
    if tv_on_left:
        notes.append("Kitaplar TV unitesinde (sol) — ayri kitaplik yok")
    else:
        book_d = 39.0
        book_h = 100.0
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
    rug_x = max(50.0, (tv.x2 + 8) if tv_on_left else (book_d + 10 if book_d else 50))
    rug_x2 = min(desk.x - 5, chair.x - 5, W - 60)
    rug_y = 50.0 if tv_on_left else (tv.h + 15)
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
    saat_y = (tv.y - 10) if tv_on_left else max(20.0, book_y - 8)
    items.append(Rect("bjk_saat_duvar", 2, max(15.0, saat_y), 8, 8, "item"))

    if desk.y < band:
        notes.append("Masa petek UST bandinda — petek onu bos")
    else:
        notes.append("Masa petek ALT bandinda")
    notes.append(
        f"2li cam sonucu: bant {band:.0f}cm — "
        + ("paralel masa sigdi" if desk.h >= 90 or desk.w <= 50 else "end-on / kisa kenar duvarda")
    )

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
        f"ÖZET W={W}* D={D}* | standart kapi={DOOR} | 2li cam={CAM} → bant={band:.0f}cm | "
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
        f'<text x="{X((salon0+salon1)/2)}" y="{Y(0)-12}" text-anchor="middle" font-size="11" font-weight="700">Salon Kapisi {DOOR:.0f}</text>'
    )
    parts.append(
        f'<path d="M{X(salon0)} {Y(0)} A{cm_to_px(DOOR)} {cm_to_px(DOOR)} 0 0 1 {X(salon0)} {Y(DOOR)}" '
        f'fill="none" stroke="#888" stroke-dasharray="3 2"/>'
    )

    parts.append(
        f'<rect x="{X(bal0)}" y="{Y(D)-6}" width="{cm_to_px(DOOR)}" height="12" fill="url(#hatch)" stroke="#111"/>'
    )
    parts.append(
        f'<text x="{X((bal0+bal1)/2)}" y="{Y(D)+22}" text-anchor="middle" font-size="11" font-weight="700">Balkon Kapisi {DOOR:.0f}</text>'
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
        f'<text x="{X(W)+8}" y="{Y(band + CAM/2)}" font-size="11" font-weight="700">2li Cam</text>'
    )
    parts.append(
        f'<text x="{X(W)+8}" y="{Y(band + CAM/2)+14}" font-size="10" fill="#8a1f1f">ORTA {CAM:.0f}cm</text>'
    )
    parts.append(
        f'<text x="{X(W)+8}" y="{Y(band + CAM/2)+28}" font-size="10" fill="#333">Petek</text>'
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
        f"- W={W}* D={D}* (oda hâlâ yerinde ölç)",
        f"- Kapı = **{DOOR} cm** (standart oda/salon duvar boşluğu)",
        f"- Cam = **{CAM} cm** (2'li / çift kanat, sağ duvar boyunca)",
        f"- Üst: 2 + kapı + 5 + kiriş40 → üst boş duvar = **{W - kiris_x1:.0f} cm**",
        f"- Sağ: cam ortada → bant = **{band:.0f} cm** (petek önü +{PETEK_CLEAR}cm yasak)",
        f"- Alt: balkon sonrası boş ≈ **{W - DOOR - GAP_START - DOOR_MARGIN:.0f} cm**",
        f"- Sol orta (salınımlar arası) ≈ **{D - 2*(DOOR + DOOR_MARGIN):.0f} cm**",
        "",
        "## 2) Boş bölgeler → fonksiyon",
        "| Bölge | Duvar | Fonksiyon | Neden |",
        "|-------|-------|-----------|-------|",
        "| Z1 | Üst, kiriş sonrası | TV veya boş | 2li cam + end-on masa üstteyse TV sola kayar |",
        "| Z2 | Alt, balkon sağı | Oturma ≤130 | TV’ye / odaya bakar |",
        "| Z3a | Sağ, petek üstü | Masa (tercih) | Bant dar → kısa kenar duvarda (end-on) |",
        "| Z3b | Sağ, petek altı | Masa yedek | |",
        "| Z4 | Sol orta | TV+kitap veya kitaplık | 2li cam paketinde genelde TV burada |",
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
        "- Standart kapı **90** + 2li cam **140** → sağ bant ≈90 cm → **100 cm masa duvara paralel sığmaz**.",
        "- Çözüm: xDrive 100×60 **kısa kenarı duvarda** (end-on), petek üst bandında.",
        "- TV sol duvarda (masa üst sağı doldurduğu için); oturma altta ≤130.",
        "- W ve D hâlâ yerinde ölç (*). Cam tam cm farklıysa `CAM` değerini layout.py’de güncelle.",
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
