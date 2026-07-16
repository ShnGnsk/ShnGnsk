# Yerleşim analizi (algoritma)

## 1) Mimari kilit
- W=300* D=320* (oda hâlâ yerinde ölç)
- Kapı = **90 cm** (standart oda/salon duvar boşluğu)
- Cam = **140 cm** (2'li / çift kanat, sağ duvar boyunca)
- Üst: 2 + kapı + 5 + kiriş40 → üst boş duvar = **163 cm**
- Sağ: cam ortada → bant = **90 cm** (petek önü +25cm yasak)
- Alt: balkon sonrası boş ≈ **198 cm**
- Sol orta (salınımlar arası) ≈ **120 cm**

## 2) Boş bölgeler → fonksiyon
| Bölge | Duvar | Fonksiyon | Neden |
|-------|-------|-----------|-------|
| Z1 | Üst, kiriş sonrası | TV veya boş | 2li cam + end-on masa üstteyse TV sola kayar |
| Z2 | Alt, balkon sağı | Oturma ≤130 | TV’ye / odaya bakar |
| Z3a | Sağ, petek üstü | Masa (tercih) | Bant dar → kısa kenar duvarda (end-on) |
| Z3b | Sağ, petek altı | Masa yedek | |
| Z4 | Sol orta | TV+kitap veya kitaplık | 2li cam paketinde genelde TV burada |

## 3) Yerleşen ürünler (cm)
- **masa**: x=200 y=6 → 100×60 cm
- **oyuncu_sandalye**: x=210 y=71 → 60×60 cm
- **tv_BESTA**: x=0 y=100 → 42×120 cm
- **oturma**: x=102 y=245 → 130×75 cm
- **hali**: x=50 y=50 → 140×120 cm
- **bjk_saat_duvar**: x=2 y=90 → 8×8 cm

## 4) Algoritma notları
- Kilit: standart kapi=90cm | 2li cam=140cm | bant=(D-cam)/2=90cm
- STRATEJI B ust | endon
- MASA: xDrive Ruzgar 100x60 end-on (kisa kenar duvarda) (duvarda 60 / ice 100)
- TV: sol duvar | oturma 130cm
- TV_ON_LEFT
- Kitaplar TV unitesinde (sol) — ayri kitaplik yok
- Masa petek UST bandinda — petek onu bos
- 2li cam sonucu: bant 90cm — end-on / kisa kenar duvarda
- ÖZET W=300* D=320* | standart kapi=90 | 2li cam=140 → bant=90cm | üst boş=163cm | alt boş≈198cm

## 5) Mantık özeti
- Standart kapı **90** + 2li cam **140** → sağ bant ≈90 cm → **100 cm masa duvara paralel sığmaz**.
- Çözüm: xDrive 100×60 **kısa kenarı duvarda** (end-on), petek üst bandında.
- TV sol duvarda (masa üst sağı doldurduğu için); oturma altta ≤130.
- W ve D hâlâ yerinde ölç (*). Cam tam cm farklıysa `CAM` değerini layout.py’de güncelle.
