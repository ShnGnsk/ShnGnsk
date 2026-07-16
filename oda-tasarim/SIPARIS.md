# 1903 — sipariş (algoritma çıktısı)

Asıl dosyalar: `layout.py` → `plan.svg` / `ANALIZ.md`  
AI perspektif fotolar **kullanma** (duvar/kapı kaydırıyor).

## Çizim kilidi
| Sabit | cm |
|-------|-----|
| Kapı başlangıç | **2** |
| Salon–kiriş | **5** |
| Kiriş | **40 × 10** sağa+içe |
| Cam+petek | sağ duvar **orta** |

\* W≈300 D≈320 kapı≈80 cam≈80 — yerinde ölç.

## Algoritma sonucu (W/D varsayılan)
**Strateji B:** masa sağ **üst** bant (petek üstü) → alt duvar oturmaya açık.

| Ürün | cm / konum | Link |
|------|------------|------|
| Masa | **100×60** xDrive — sağ üst bant, petek ÖNÜNE değil | [Trendyol](https://www.trendyol.com/xdrive/ruzgar-oyuncu-masasi-siyah-100x60-p-993862707) |
| Sandalye | oyuncu koltuğu siyah — masanın odanın içine bakan yüzü | [xDrive Akdeniz](https://www.trendyol.com/xdrive/akdeniz-kumas-profesyonel-oyuncu-koltugu-siyah-siyah-p-140003157) |
| PC | siyah kasa — masa üstü/yanı | Trendyol gaming PC |
| TV ünitesi | Alçak banko **≤95×42** (bu pakette) — üst boş duvar, koltuğa bakar | IKEA BESTÅ TV banko / Trendyol 100cm siyah TV ünitesi |
| TV | 50–55" | Trendyol |
| Oturma | **≤130×75** — balkon sağı, TV’ye bakar | Vivense / Trendyol siyah |
| Kitaplık | **~39×100** taban — sol orta (salınım dışı) | IKEA KALLAX 42 / dar raf |
| Halı | ~140×120 orta | Trendyol geometrik S/B |
| Saat | BJK lisanslı — sol duvar | [Trendyol BJK saat](https://www.trendyol.com/besiktas-duvar-saati-x-b146-c35) |
| Aksesuar | yastık/forma | Kartal Yuvası / Trendyol |

## Neden böyle?
1. Üstte kirişten sonra **173 cm boş duvar** → TV  
2. Altta balkon sonrası **~208 cm boş** → oturma (TV’ye bakar)  
3. Sağda cam ortada → masa **petek üst veya alt bantta**; petek önü yasak  
4. Masa **alt** banda konursa 100×60 + 130 oturma **çakışır** → algoritma masayı üste alır  
5. Sol orta → kitaplık (kapılar sola açılır, köşeler salınım)

## Alma
- 140+ ikili + 100×60 masa **alt bantta birlikte** → alma  
- Petek önüne masa → alma  
- Kapı salınımına dolap → alma  
