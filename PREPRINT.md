# PREPRINT — Sıçan Arka Bacağının Nöromekanik Kapalı-Döngü Modeli

> **Bu dosya nedir:** Konferans bildirisinin **metin tabanlı çalışma alanı.** Çıktı bir poster
> olacak (sözlü anlatım + görsel ağırlıklı), ama burada her şey açık açık yazılır: hangi
> iddiayı hangi kanıta dayandırdığımız, neyin doğrulandığı, neyin henüz iddia olduğu.
>
> **Neden "preprint":** poster önünde araştırmacıya sözlü anlattığımız şeyin yazılı hali.
> Poster metni buradan damıtılır, tersi değil.
>
> Bilimsel doğrulama defteri ayrıdır: `04_kapali_dongu/02_DOGRULAMA_KAYDI.md`.
> Proje durumu: `SDLC/00_DURUM.md`.

---

## 1 · Ne yapmaya çalışıyoruz

Sprague-Dawley sıçanının **yürüyüşünü** modelliyoruz. Amaç, lokomosyonu *in silico* üretmek:
canlı hayvana ihtiyaç duymadan, omurilikten kasa uzanan **kapalı döngüyü** bilgisayarda
kurmak.

Döngünün akışı:

```
omurilik (NEURON)                                    kas-iskelet (OpenSim)
  merkezi örüntü üreteci (CPG)
        │
        ▼
  internöronlar
        │
        ▼
  motonöron havuzu ────── aktivasyon u(t) ──────►  Hill tipi kas modeli
        ▲                                                │
        │                                                ▼
        │                                          eklem momenti, hareket
        │                                                │
        └────── Ia / II afferent r(t) ◄────── kas iğciği ┘
```

Sinir komutu kası çalıştırır, hareket duyusal geri besleme üretir, geri besleme komutu
yeniler. Kapalı olan budur. Bu döngünün anlaşılması omurilik yaralanmasında **nöroprotez**
geliştirme çalışmalarının temelidir.

**Ekip:** iki kişi. **Nöron tarafı** (NEURON: CPG, internöronlar, motonöron havuzu, Ia
afferent) ve **mekanik taraf** (OpenSim: kas-iskelet, Hill kas modeli, ID/SO). Bu depo
ikisinin buluştuğu yerdir; köprünün tanımı `SDLC/01_PROJE.md`'dedir.

**Kas modeli:** Hill tipi. Depodaki `.osim` modelinde 38 kasın tamamı `Thelen2003Muscle`
(Hill tipi bir uygulama) olarak tanımlıdır.

---

## 2 · Bildiri özeti (kabul edilen metin — DOKUNULMAZ)

> Bu bölüm **referanstır, düzenlenmez.** Aşağıdaki her cümle bir taahhüttür; çalışmanın
> ona sadık kalması gerekir. Sapma gerekirse bölüm 4'te tartışılır.

**Amaç:** Lokomosyon, sinir komutlarıyla kasların hareket ürettiği ve duyusal geri beslemenin
komutları yenilediği kapalı döngüdür. Bu döngünün anlaşılması, omurilik yaralanmalarında
nöroprotez geliştirme çalışmaları için önemlidir. Bilgisayar modelleri, döngüye ilişkin
hipotezlerin canlı modellere ihtiyaç olmadan denenmesini sağlamaktadır. Çalışmanın amacı,
sıçan arka bacak kas-iskelet modelini omurilik sinir modeliyle birleştirip döngünün bilgisayar
modelini oluşturmaktır.

**Gereç-Yöntem:** Sprague-Dawley sıçanının anatomik modelinde, omurga, pelvis, femur, tibia ve
ayak segmentlerini kapsayan Johnson ve ark. (2008) kas-iskelet modeli temel alınmıştır. Kas
yolları, sıçan anatomi atlasıyla kontrol edilip güncellenmiştir. Kas-iskelet sisteminin kinetik
ve kinematiği OpenSim yazılımında Hill oranı kullanılarak hesaplanmıştır. Maksimum kuvvet
tanımları, kas kesit alanı ölçümleri kullanılarak tanımlanmıştır. Uyluk, baldır ve ayak
kütleleri ile eylemsizlik büyüklükleri, literatür çalışmalarından model boyutuna
ölçeklenmiştir. Modele, sıçan yürüyüşünden ölçülmüş kemik eklem açıları uygulanmıştır.
Çözümleme, ayağın yere değmediği ve yer tepki kuvveti gerektirmeyen salınım fazında
yapılmıştır. Ters dinamik ile bu fazın gerektirdiği eklem momentleri hesaplanmıştır. Statik
optimizasyon uygulanarak momentler toplam kas eforu en az olacak biçimde dağıtılmış ve her
kasın aktivasyon zaman serisi elde edilmiştir. Döngünün diğer yarısı olan omurilik devresi
için, sinir hücrelerini simüle eden NEURON yazılımı seçilmiştir.

**Bulgular:** Ekstansör kasların diz moment kolları pozitif, fleksör kasların ise negatif
işaretlidir. Quadriceps kaslarında moment kol uzunluğu yaklaşık olarak +3,7 mm'dir.
Semimembranosus kasında ise -4,1 mm olarak hesaplanmıştır. Modelin kas yolu geometrisinden
hesapladığı moment kolları, kaynak çalışmanın deneysel ölçümleriyle uyumludur. Salınım fazının
başında kalça fleksörleri, ortasında ayak bileği dorsifleksörleri, sonunda kalça ekstansörleri
etkindir.

**Sonuç:** Kapalı döngünün kas-iskelet tarafı oluşturulmuş ve salınım fazı kas aktivasyonları
elde edilmiştir. Deneysel çalışmalar ile model güncellenip basma fazı çözülecektir. Model,
hipotezlerin invaziv deneyler olmadan sınanmasına ve nöroprotez çalışmalarına temel
oluşturacaktır.

**Anahtar Kelimeler:** lokomosyon, NEURON, nöromekanik modelleme, OpenSim, sıçan arka bacağı

---

## 3 · Taahhüt kontrol listesi

Bildirideki her yöntem cümlesinin karşılığı depoda var mı:

| # | Bildiri taahhüdü | Durum | Kanıt / yer |
|---|---|---|---|
| 1 | Johnson ve ark. (2008) tabanlı kas-iskelet modeli (omurga, pelvis, femur, tibia, ayak) | var | `01_model/rat_hindlimb_faz1a.osim`; 5 segment doğrulandı (DOGRULAMA H2) |
| 2 | Kas yolları anatomi atlasıyla kontrol edilip **güncellenmiş** | **çelişki** | bkz. bölüm 4.2 |
| 3 | OpenSim + Hill tipi kas | var | 38 kas `Thelen2003Muscle` |
| 4 | F_max kas kesit alanından | kısmen | `.osim`'de 0,2-18,8 N gerçek değerler var; `build_osim.py` 10 N yer tutucu koyuyor (DOGRULAMA A) |
| 5 | Kütle/eylemsizlik literatürden ölçeklenmiş | doğrulanmadı | bağımsız ölçüm yapılmadı |
| 6 | Ölçülmüş kemik eklem açıları uygulanmış | var | `02_veri/rat_walk_bone_smooth.mot` |
| 7 | Salınım fazı, GRF gerektirmeyen çözümleme | var | `03_kod/kod_02_swing_id_so.py` |
| 8 | Ters dinamik ile eklem momentleri | var | aynı betik (ID) |
| 9 | Statik optimizasyon ile kas aktivasyonları | var | `02_veri/u_swing_v2.csv` |
| 10 | Omurilik devresi için NEURON seçilmiş | seçildi, kurulmadı | İP-4a sürüyor; `inline-supplementary-material-1/` |
| 11 | Quadriceps diz moment kolu ~ +3,7 mm | ölçüldü | RF +3,70 · VL +3,73 · VI +3,72 · VM +3,70 |
| 12 | Semimembranosus -4,1 mm | **çelişki** | ölçülen -3,87 mm; bkz. bölüm 4.1 |
| 13 | Moment kolları kaynak çalışmanın **deneysel ölçümleriyle uyumlu** | **çelişki** | bkz. bölüm 4.3 |
| 14 | Salınım fazı kas etkinlik sırası (kalça fleksör → ayak bileği dorsifleksör → kalça ekstansör) | doğrulanmadı | `u_swing_v2.csv`'den yeniden okunmalı |

---

## 4 · Bildiri ile doğrulanmış durum arasındaki farklar

> Bunlar poster önünde sorulabilecek sorulardır; hazırlıksız yakalanmamak için açık yazılıyor.
> Kaynak: `04_kapali_dongu/02_DOGRULAMA_KAYDI.md` (27.07.2026 bağımsız ölçüm oturumu).

### 4.1 · Semimembranosus: bildiri -4,1 mm, ölçüm -3,87 mm

Bildiri **-4,1 mm** yazıyor. 27.07.2026 doğrulama oturumunda iki ayrı türev yöntemiyle ölçülen
değer **-3,87 mm** (diz açısı -120°, sarma açık ve kapalı halde aynı). Fark 0,23 mm, yani
yaklaşık %6.

Olası açıklamalar: farklı diz açısında ölçülmüş olması, farklı model sürümü, ya da bildiriye
yuvarlanarak/başka bir kaynaktan girmiş olması. **Karar gerekiyor** — bkz. bölüm 7, açık soru 1.

### 4.2 · "Kas yolları güncellenmiştir" iddiası

Depodaki modelde **38 kasın hepsi tam iki noktalıdır** (via point yok). Johnson ise Tablo 6'da
quadriceps'in dört başı, TA, EDL, TP, FDL, FHL ve Peronei için birer **via point** kaydetmiştir
(DOGRULAMA H4). Yani model, kaynak çalışmanın kas yolu topolojisini yeniden üretmiyor.

Ayrıca koordinatlar birebir değil: portun quadriceps insertion'ı tibia çerçevesinde
(2,60 · 37,50 · 0,50) mm, Johnson'ınki (2,03 · 40,99 · 1,68) mm.

"Anatomi atlasıyla kontrol edilip güncellenmiştir" cümlesi, **hangi kasların hangi yönde
güncellendiği** yazılmadan savunulamaz. Güncelleme yapıldıysa kaydı bulunmalı; yapılmadıysa
cümle poster metninde daraltılmalı.

### 4.3 · "Moment kolları deneysel ölçümlerle uyumludur" iddiası

Bu, bildirinin en kırılgan cümlesi. Doğrulama kaydının söyledikleri:

- **Johnson Şekil 3'teki quadriceps eğrisiyle karşılaştırma YAPILMADI** (DOGRULAMA D bölümü:
  "Tek eksik geometri doğrulaması budur").
- Quadriceps'in +3,7 mm'sini **anatomi değil, `femur_dist` WrapTorus üretiyor.** Sarma
  kapatıldığında quadriceps modelde *fleksör* oluyor (-0,65 … -1,18 mm). Değer torusun
  `inner_radius` alanına doğrudan bağlı: 2 mm → 2,94 · **4 mm → 3,71** · 5 mm → 4,02 (H1).
- Johnson'ın kendi via point'i taşınıp sarma kapatıldığında dört baş **+1,01 … +1,51 mm**
  veriyor — işaret doğru ama büyüklük yarıdan az ve dört başın kümelenmesi kayboluyor.
  Yani "0,03 mm içinde kümelenme" torusun imzasıdır, anatomik bulgu değildir.
- Johnson moment kolunu **farklı tanımlıyor** (kas etki doğrultusu birim vektörü ile yarıçap
  vektörünün çapraz çarpımı); bizimki `r = -dL/dθ`. İki tanımın aynı sayıyı vermesi zorunlu
  değildir (H6).
- İki yöntemle doğrulama iddiası da zayıf: `computeMomentArm` ve `getLength` + merkezi fark
  **aynı kas yolunu ve aynı sarma motorunu** kullanıyor; uyuşma türevi doğrular, geometriyi
  değil (H5).

**En savunulabilir sayı semimembranosus'tur:** -3,87 mm değeri sarmadan tamamen bağımsızdır
(sarma açık/kapalı fark 0,00 mm).

### 4.4 · Bildiri, projenin gerisinde

Bildiri "basma fazı **çözülecektir**" diyor. Depoda basma fazı (`u_stance_v4.csv`) ve refleks+CPG
ile emergent kapalı-döngü yürüyüş (İP-3, teslim 9of9) **zaten var**. Bu bir çelişki değil,
fazlalık: poster bildiriye sadık kalıp bunları "devam eden çalışma" olarak sunabilir.

---

## 5 · Poster metni (çalışma alanı)

> Bildiriye sadık, doğrulanmış ifadelerle yazılacak. Her iddianın yanına kanıtı konur;
> kanıtı olmayan cümle postere girmez.

### 5.1 · Giriş
<!-- doldurulacak -->

### 5.2 · Yöntem
<!-- doldurulacak: model, Hill kas, ID+SO, NEURON tarafı -->

### 5.3 · Bulgular
<!-- doldurulacak: moment kolları, salınım fazı aktivasyon sırası -->

### 5.4 · Tartışma ve sınırlılıklar
<!-- bölüm 4'teki farklar burada dürüstçe yer alır -->

---

## 6 · Sözlü anlatım için hazır cevaplar

`02_DOGRULAMA_KAYDI.md` E bölümünde hakem/araştırmacı sorularına hazır cevaplar var
(+3,7 mm nereden geliyor, iki yöntem ne kadar bağımsız, NEURON çıktısı nerede, ön uzuv nerede,
tırıs verisi nereden). Poster önünde bunlar sorulacaktır; oradan tekrar okunmalı.

---

## 7 · Açık sorular (karar bekliyor)

1. **Semimembranosus -4,1 mm mi, -3,87 mm mi?** Bildirideki sayı hangi ölçümden geldi?
   Poster hangisini yazacak?
2. **"Kas yolları güncellenmiştir" cümlesi neye dayanıyor?** Bir güncelleme kaydı var mı,
   yoksa cümle daraltılmalı mı?
3. **NEURON tarafı posterde nereye kadar iddia edilecek?** Bildiri yalnız "seçilmiştir" diyor;
   İP-4a bitmezse posterde sonuç gösterilemez.
4. **Salınım fazı kas etkinlik sırası** (kalça fleksör → dorsifleksör → kalça ekstansör)
   `u_swing_v2.csv`'den yeniden ölçülüp doğrulanmalı.
