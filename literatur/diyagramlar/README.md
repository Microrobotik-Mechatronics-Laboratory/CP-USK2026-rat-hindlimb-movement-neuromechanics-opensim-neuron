# literatur/diyagramlar — Model Diyagramları

Bu klasör, projenin **nöron-kas yapısını** gösteren diyagramların **kaynağıdır**. Diyagramlar
Mermaid ile yazılmıştır; VS Code, Obsidian, Typora ve GitHub bunları doğrudan çizer.

## Drift kuralı

Diyagramların **tek doğruluk kaynağı burasıdır.** `../../PREPRINT.md` bu diyagramları kopya
olarak taşır (Markdown transclusion yok). Bir diyagram değişecekse:

1. Önce buradaki dosya düzeltilir.
2. Sonra aynı Mermaid bloğu PREPRINT'teki karşılığına kopyalanır.
3. Değişiklik `SDLC/03_GUNLUK.md`'ye yazılır.

Ters yön (önce PREPRINT'te düzeltip burayı unutmak) **yasaktır**; iki dosya ayrışırsa
bu klasör doğru kabul edilir.

## Diyagramlar

| Dosya | Ne gösterir | PREPRINT bölümü |
|---|---|---|
| `D1_sistem_kapali_dongu.md` | Kapalı döngünün tamamı: NEURON \| köprü \| OpenSim sınırları, taşınan değişkenler, birimler, gecikmeler | 4 |
| `D2_omurilik_devresi.md` | Omurilik devresi hücre düzeyinde: CPG yarım-merkezleri, internöronlar, motonöron havuzları, işaretli bağlantılar | 6 |
| `D3_motonoron_hucre.md` | Tek motonöron: bölmeler, kanal yerleşimi, Cav1.3 PIC hot-spot, Ia sinaps bölgesi | 6 |
| `D4_igcik_afferent.md` | Kas iğciği ve Ia/II afferent yolu, ateşleme denklemleri, sıçan doğrulama aralıkları | 7 |
| `D5_kas_iskelet.md` | 5 segment, 7 bacak serbestlik derecesi, 38 kasın eklem-işlev haritası, Hill kas-tendon birimi | 5 |
| `D6_havuz_kas_eslesme.md` | 38 motonöron havuzu ile 38 kasın eşleşmesi ve resiprokal inhibisyon çiftleri | 6 |
| `D7_yuruyus_zamanlama.md` | Salınım fazı zaman çizelgesi: bildirinin iddia ettiği sıra ile ölçülen sıra | 9 |
| `D8_veri_hatti_dogrulama.md` | İşlem hattı ve doğrulama haritası (hangi büyüklük hangi makaleye hangi aralıkla bağlı) | 12 |

## İşaretleme kuralı

Diyagramlarda ve tablolarda her bileşenin durumu şu etiketlerden biriyle verilir:

- `[ölçüldü]` — bu çalışmada ölçülmüş, `DOGRULAMA.md`'ye işlenmiş.
- `[literatürden]` — bir yayından alınmış; kaynağı satırda yazılıdır.
- `[tasarım]` — bizim model kararımız; henüz ne ölçüm ne de literatür değeri.
- `[varsayım]` — kaynağı olmayan, sonra doğrulanacak seçim.

Kaynağı yazılamayan sayı diyagrama girmez.
