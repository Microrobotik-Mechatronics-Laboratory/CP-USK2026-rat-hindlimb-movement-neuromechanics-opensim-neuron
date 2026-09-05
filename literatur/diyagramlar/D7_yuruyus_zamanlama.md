# D7 — Salınım fazı zamanlaması: iddia edilen sıra ile ölçülen sıra

Kaynak veri: `veri/u_swing_v2.csv` — ters dinamik + statik optimizasyon çıktısı, salınım
aralığı gait %65–100, 71 örnek, çevrim süresi T = 0,387 s.

## Bildirinin iddiası

> "Salınım fazının başında kalça fleksörleri, ortasında ayak bileği dorsifleksörleri, sonunda
> kalça ekstansörleri etkindir."

```mermaid
flowchart LR
    A["%65<br/>salinim baslangici"] --> B["kalca fleksorleri"]
    B --> C["ayak bilegi dorsifleksorleri"]
    C --> D["kalca ekstansorleri"]
    D --> E["%100<br/>basma baslangici"]
```

## Ölçülen sıra

```mermaid
flowchart LR
    A2["%65"] --> B2["diz ekstansor %66.5<br/>kalca fleksor %68.5"]
    B2 --> C2["diz fleksor %76.0"]
    C2 --> D2["ayak bilegi dorsifleksor %85.5"]
    D2 --> E2["ayak bilegi plantarfleksor %87.0"]
    E2 --> F2["%100"]
```

**Sonuç: son iki halka yer değiştiriyor.** Ayak bileği dorsifleksörü fazın *ortasında* değil,
son üçte birinde tepe yapıyor; kalça ekstansörleri ise salınım boyunca zaten çok zayıf.

## Kas kas ölçüm (tepe aktivasyon zamanı)

Yalnız tepe aktivasyonu 0,005'i geçen kaslar; kalan 25 kas salınım boyunca sessizdir.

| Kas | Tepe `a` | Tepe zamanı (gait %) | `a > 0,01` penceresi | Modelin moment kolundan işlevi |
|---|---|---|---|---|
| IP | 0,0770 | 69,0 | %65–100 | kalça fleksör |
| BFa | 0,0568 | 81,0 | %67–100 | **kararsız** (r_kalça −1,01, kararlılık 0,62) |
| GMa | 0,0458 | 82,5 | %65–100 | modelde kalça **fleksör** (+5,39) |
| FDL | 0,0439 | 87,0 | %78,5–100 | plantar fleksör / parmak fleksörü |
| RF | 0,0436 | 66,5 | %65–100 | kalça fleksör + diz ekstansör |
| OE | 0,0280 | 72,0 | %65–100 | **kararsız** |
| TA | 0,0184 | 85,5 | %65–96 | dorsifleksör |
| BFp | 0,0128 | 65,0 | %65–67 | kalça ekstansör + diz fleksör |
| Pop | 0,0125 | 76,0 | %73,5–81 | diz fleksör |
| STp | 0,0118 | 77,0 | %70,5–82 | kalça ekstansör + diz fleksör |
| GMe | 0,0097 | 71,5 | — | kalça fleksör (zayıf) |
| TFL | 0,0087 | 65,0 | — | kalça fleksör |
| CF | 0,0054 | 100,0 | — | kalça ekstansör |

## Grup düzeyinde (moment kolu işaretine göre gruplanmış)

| Grup | Toplam aktivasyon | Grup tepe zamanı | Aktivasyon ağırlık merkezi |
|---|---|---|---|
| Kalça fleksörleri (IP, TFL, RF, GMe, GMa) | 7,851 | %68,5 | %78,4 |
| Kalça fleksörleri (GMa hariç) | 5,511 | %68,0 | %77,4 |
| Diz ekstansörleri (VL, VI, VM, RF) | 1,431 | %66,5 | %76,5 |
| Diz fleksörleri (Pop, MG, LG, Pla) | 0,502 | %76,0 | %77,4 |
| Kalça ekstansörleri (13 kas) | **0,883** | %65,0 | %79,2 |
| Ayak bileği dorsifleksörleri (TA, EDL, Per) | 1,197 | %85,5 | %81,1 |
| Ayak bileği plantar fleksörleri (7 kas) | 1,444 | %87,0 | %86,3 |

## Zaman çizelgesi

```
gait %      65        70        75        80        85        90        95       100
            |---------|---------|---------|---------|---------|---------|---------|
IP          #########################################################################
RF          ##########################################################...............
TFL         ###......................................................................
GMe         .....######..............................................................
BFp         ###......................................................................
STp         ..............########...................................................
Pop         ..................######.................................................
BFa         ....#####################################################################
GMa         #########################################################################
TA          #####################################################################....
FDL         ..........................######################################. ........
            ^tepe: RF 66.5  IP 69.0        Pop 76 STp 77   BFa 81 GMa 82.5  TA 85.5  FDL 87
```

## Bu ölçümün sınırları

1. **Gruplandırma tartışmalı.** Eski gruplandırma GMa ve BFa'yı kalça ekstansörü sayıyordu;
   modelin kendi moment kolları GMa'yı **fleksör** (+5,39 mm), BFa'yı ise **kararsız**
   (−1,01 mm, işaret kararlılığı 0,62) gösteriyor (`D5`). Bildirideki "sonunda kalça
   ekstansörleri" cümlesi, GMa ve BFa ekstansör sayılırsa yaklaşık doğrulanır (%81–82,5);
   modelin moment kolları esas alınırsa doğrulanmaz. **Önce GMa çelişkisi çözülmelidir.**
2. **Tüm aktivasyonlar küçük** (`a` ≤ 0,077). Statik optimizasyonun min Σa² çözümü, zayıf
   uyarılmış kasları eşit dağıtma eğilimindedir; sıralama gürültüye duyarlı olabilir.
3. **"Etkin" ölçütü tepe zamanı alındı.** Bildiri bir etkinlik *penceresi* kastediyor olabilir;
   pencere tanımıyla sıra değişebilir (yukarıdaki zaman çizelgesinde pek çok kasın penceresi salınımın
   tamamını kaplıyor).
4. Salınım fazı, ayağın yere değmediği ve yer tepki kuvveti gerektirmeyen aralık olarak alınmıştır
   (bildiri yöntemi); basma fazı bu çalışmanın kapsamı dışındadır.
