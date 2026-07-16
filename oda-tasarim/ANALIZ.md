# Yerleşim analizi (algoritma)

## 1) Mimari kilit
- W=300* D=320* kapı=80* cam=80*
- Üst: 2 + kapı + 5 + kiriş40 → üst boş duvar = **173 cm**
- Sağ: cam ortada → bant = **120 cm** (petek önü +25cm yasak)
- Alt: balkon sonrası boş ≈ **208 cm**
- Sol orta (salınımlar arası) ≈ **140 cm**

## 2) Boş bölgeler → fonksiyon
| Bölge | Duvar | Fonksiyon | Neden |
|-------|-------|-----------|-------|
| Z1 | Üst, kiriş sonrası | TV ünitesi | En uzun boş duvar; koltuğa bakar |
| Z2 | Alt, balkon sağı | Oturma | İkinci uzun boş duvar; TV’ye bakar |
| Z3a | Sağ, petek üstü | Masa+PC+sandalye (tercih) | Alt duvarı oturmaya bırakır |
| Z3b | Sağ, petek altı | Masa yedek | Üst sığmazsa; oturma kısalır |
| Z4 | Sol orta | Kitaplık | Kapı salınımlarının arasında |

## 3) Yerleşen ürünler (cm)
- **masa**: x=240 y=8 → 60×100 cm
- **oyuncu_sandalye**: x=175 y=113 → 60×60 cm
- **tv_BESTA**: x=135 y=0 → 95×42 cm
- **oturma**: x=92 y=245 → 130×75 cm
- **kitaplik**: x=0 y=110 → 39×100 cm
- **hali**: x=49 y=57 → 140×120 cm
- **bjk_saat_duvar**: x=2 y=102 → 8×8 cm

## 4) Algoritma notları
- STRATEJI B masa UST bant
- MASA: xDrive Ruzgar 100x60
- Oturma 130cm | TV 95cm | masa 100x60
- Masa petek UST bandinda — petek onu bos; alt duvar oturmaya acik
- ÖZET W=300* D=320* kapı=80* cam=80* → sağ bant=120cm | üst boş=173cm | alt boş≈208cm

## 5) Mantık özeti
- AI perspektif fotoğraf duvar/kapı/cam uydurur → **tasarım değildir**; sadece `plan.svg` + bu analiz.
- Masa **alt** banda konursa 100×60 + 130 oturma çakışır → algoritma masayı **üst banda** alır (Strateji B).
- TV **üst boş duvarda**, oturma **altta** → birbirine bakar (sol duvara TV koyup alta koltuk = yan bakış, yanlış).
- 140 cm ikili yerine **≤130 cm**; TV ünitesi bu pakette **≈95 cm** (masa üst sağda yer kapladığı için).
- Yeniden üret: `python3 layout.py` (W/D/DOOR/CAM değiştirilebilir).
