# Literatür özeti — Parziale 2020 (hız–doğruluk ödünleşimi, omurilik modeli)

> Bu dosya makalenin **seçici özetidir** — yerine geçmez. Amacı, makaleyi tekrar
> açmadan modelleme kararı verebilmektir.

## 1 · Künye ve sınıflandırma

- **Yazarlar / yıl:** Antonio Parziale, Rosa Senatore, Angelo Marcelli / 2020 (online: 03 Ocak 2020; kabul: 18 Aralık 2019)
- **Başlık:** Exploring speed–accuracy tradeoff in reaching movements: a neurocomputational model
- **Dergi / cilt / sayfa:** Neural Computing and Applications (online-first; cilt/sayfa künyede yok)
- **DOI / PMC:** 10.1007/s00521-019-04690-z
- **PDF:** `pdf/Exploring_speed_accuracy_tradeoff_in_reaching_movements_a_neurocomputational_model.pdf` (repoya girmez)
- **Özeti çıkaran / tarih:** Claude / 2026-09-06

- **Makale tipi:** bilgisayar modeli
- **Projemizin hangi tarafına bakıyor:** köprü/kapalı döngü (omurilik ağı + kas-iskelet + proprioseptör, tam döngü)
- **Bizim için değeri:** yöntem örneği (omurilik devre mimarisi, gecikme değerleri, kapalı döngü kurulumu); sınırlı ölçüde parametre kaynağı

## 2 · Makalenin sorusu ve ana iddiası
Makale, Fitts kanununun (hareket süresi ile zorluk indeksi arasındaki doğrusal ilişki) hangi sinirsel mekanizmadan doğduğunu sorar. Yazarlar, bir serbestlik dereceli bir kol için omurilik devresi + kas-iskelet + proprioseptör içeren bir neurocomputational model kurar ve erişme (reaching) hareketlerini bu modele öğretir. Ana iddia: hız–doğruluk ödünleşimi kas-iskelet sisteminin içsel (intrinsic) bir özelliği değildir; merkezi sinir sisteminin öğrenilmiş bir hareketi hızlandırmak için seçtiği stratejiden doğan davranışsal bir özelliktir. Sonuçlara göre öğrenilmiş bir hareketin hızı, korteksteki CM (cortico-motoneuronal) hücreler ile alpha motoneuron'lar arasındaki monosynaptic bağlantı üzerinden ayarlanır (Abstract; Bölüm 6).

---

## 3 · NEYİ NASIL YAPMIŞ (yöntem)

### 3a · Denek / malzeme / model
Deneysel denek yoktur; çalışma tümüyle simülasyondur.

- **Omurilik ağı:** IaIN (Ia interneuron), IbIN (Ib interneuron), Renshaw hücresi, PN (propriospinal interneuron), alpha-MN, gamma-MN (static + dynamic) içerir; synergist ve antagonist kas ilişkilerini kurar (Bölüm 3.1; Şekil 2–3; Tablo 4 son satır).
- **Nöron modeli:** rate code yaklaşımı; her model nöronu, benzer bağlantılı bir nöron popülasyonunu temsil eder ve logistic aktivasyon fonksiyonu kullanır (Bölüm 3.2; Eş. 3–4).
- **Kas-iskelet modeli:** tek serbestlik dereceli dirsek (menteşe eklem); omuz ve bilek sabitlenmiştir. İskelet 4 kemikten oluşur: humerus, ulna, radius, el. Üç kas vardır: biceps short, brachialis, triceps lateral. Brachialis'in sardığı kemik yüzeyi silindirik wrapping objesiyle modellenir (Bölüm 3.3; Şekil 4).
- **Kas modeli:** Virtual Muscle v. 4.0 (Hill tipi fenomenolojik + Huxley tipi mekanistik yaklaşımların birleşimi); spindle modeli (Mileusnic 2006), Golgi tendon organı modeli ve metabolik enerji tüketimi modeli içerir (Bölüm 3.3, 3.6).
- **Yazılım:** MSMS (kas-iskelet), SimMechanics/Simulink (dinamik motor), Matlab R2017b; ode45 değişken adımlı çözücü. Donanım: AMD Opteron 6376, 32 GB RAM. 4 s'lik bir hareketin simülasyonu ortalama 39 s sürer (16 değerlendirme ortalaması) (Bölüm 3.6).
- **Öğrenme algoritması:** differential evolution (DE), rand/1 konfigürasyonu; deneme-yanılma ile "good-enough" motor komut repertuvarı öğrenir (Bölüm 3.5).

### 3b · Yöntem adımları
1. Omurilik ağı, literatürdeki ana yolaklara göre kurulur: monosynaptic Ia uyarımı, Renshaw inhibisyonu, Ia/Ib interneuron yolakları, PN yolağı (Bölüm 3.1.1–3.1.6).
2. Kortikal kontrol girdileri tanımlanır: her omurilik nöron havuzuna bir girdi → 24 girdi (21 interneuron + 3 alpha-MN); ayrıca spindle/GTO afferentlerinin presynaptic kazançlarını ve IbIN etkisinin yönünü düzenleyen 19 girdi → toplam 43 corticospinal girdi. Kontrol için toplam 46 değer değiştirilebilir: 40 interneuron girdisi + 3 alpha-MN girdisi + 3 aktivasyon zamanı (t_BI, t_BRA, t_TRI) (Bölüm 3.4).
3. Deney 1 (repertuvar öğrenme): alpha-MN'lere doğrudan CM girdisi KULLANILMADAN, DE ile 40 interneuron girdisi + 3 zaman öğrenilir. İki amaçlı optimizasyon: hedef pozisyona uzaklık + metabolik enerji minimize edilir. Hedefler: dirsek 0°'den 18°, 36°, 72°'ye. Hedef başına 4 DE koşusu → 12 "sanal denek". Son jenerasyonda hedefe 3° içinde kalan çözümler o deneğin motor becerisi sayılır (Bölüm 5.1).
4. Her hareket simülasyonu 4 s sürer: [0, 0.5] s dinlenme (duyusal geri besleme kazanç girdileri −0.5, diğerleri 0); [0.5, 1.5] s girdiler DE çözümüne göre güncellenir; 1.5 s'den sonra girdiler sabit tutulur ve hız ölçülür. Hareket süresi, tepe hızın (Vp) %5'inin aşıldığı andan (t_start) hızın kalıcı olarak %5 Vp altına indiği ana (t_stop) kadar ölçülür (Corcos 1988 protokolü). Enerji, [t_start, t_stop] aralığında üç kasın metabolik enerjisinin toplamıdır (Bölüm 5.1).
5. Çözüm reddetme ölçütleri: (a) dirsek açısı [0°, 145°] dışına çıkarsa; (b) antagonist (triceps) girdileri her iki agonistten önce ya da her ikisinden sonra ateşlenirse (triphasic EMG deseni ihlali); (c) 2°'yi aşan birden fazla yön dönüşü (reversal) varsa; (d) dirsek reversal sonrası fleksiyona devam edip reversal açısını aşarsa; (e) simülasyon sonu açısı ile t_stop açısı farkı 1.5°'yi aşarsa veya son 0.5 s'de ortalama hız 0.3°/s'yi aşarsa (Bölüm 5.1).
6. Deney 2 (Fitts görevi): Corcos 1988 deney tasarımı yeniden üretilir: A ∈ {18°, 36°, 72°}, W ∈ {3°, 6°, 9°, 12°} → 12 görev, 8 farklı ID değeri (Tablo 9). Görev başına 4 sanal denek; her deneğin DE başlangıç popülasyonu, Deney 1'de o mesafe için öğrenilen hareketlerden kurulur. Amaç fonksiyonu: hareket süresini minimize etmek; hedefi aşan veya hedefte kalmayan çözüm reddedilir (Bölüm 5.3).
7. Üç hızlandırma stratejisi karşılaştırılır: Strateji 1 — yalnızca CM→alpha-MN monosynaptic girdileri değiştirilir (3 değer); Strateji 2 — yalnızca aktivasyon zamanları değiştirilir (3 değer); Strateji 3 — yalnızca 40 interneuron girdisi değiştirilir. Her strateji için 8 ID noktasındaki ortalama süreye Fitts regresyon doğrusu oturtulur (Trusted Region algoritması) (Bölüm 5.3).
8. DE yakınsaması, MaxDist ve Diff metrikleriyle ve Friedman aligned ranks + Holm post hoc testleriyle (STAC aracı) değerlendirilir (Bölüm 5.4).

### 3c · Tanım ve birim uyarıları
- **Nöron çıkışı boyutsuzdur:** bütün ateşleme hızları [0, 1] aralığında normalize değerlerdir; presynaptic girdi PI ∈ [−1, 1] (Tablo 1). Bizim NEURON tarafımızda ateşleme Hz cinsindendir; bu modelden sinaptik ağırlık veya hız değeri doğrudan aktarılamaz.
- **Sinaptik ağırlık formülü sayıya bağlıdır:** ağırlık, nöronun aldığı inhibitör/eksitatör girdi SAYISINA göre hesaplanır (Eş. 5: w = −HYP/syn_inh veya 1 + OD/syn_exc). Bu tanım, iletkenlik tabanlı sinapslardan farklıdır.
- **Hareket süresi tanımı:** %5 Vp → %5 Vp aralığıdır; reaksiyon süresi içermez. Fitts deneyleriyle karşılaştırırken bu tanım korunmalıdır.
- **"Descending input" tanımı:** bu modelde YALNIZCA corticospinal yolu temsil eder ve interneuron/MN'lere giden girdiler yalnız eksitatördür; Loeb grubunun modellerinde ([89, 106, 107]) aynı ad hem eksitatör hem inhibitör toplam etkiyi temsil eder (Bölüm 4). Aynı terim iki makalede farklı kapsam taşır.
- **Fitts katsayılarının birimi tabloda verilmemiştir** (Tablo 10); Şekil 8'in zaman ekseni ms olduğundan a ve b pratikte ms ölçeğinde okunur — "yorum:" bu birim çıkarımı makalede açıkça yazmaz.

### 3d · Kullanılan parametreler ve değerleri

| Parametre | Değer | Birim | Nereden (tablo/şekil/sayfa) |
|---|---|---|---|
| Logistic kazanç g | 11 | — | Bölüm 3.2 (kaynak [89]) |
| Logistic bias d | 0.5 | — | Bölüm 3.2 (kaynak [89]) |
| HYP (hyperpolarization sınırı) | 2 | — | Bölüm 3.2 (kaynak [106]) |
| OD (overdrive sınırı) | 2 | — | Bölüm 3.2 (kaynak [106]) |
| Afferent iletim süresi | 10 | ms | Bölüm 4 |
| Interneuron başına merkezi gecikme | 0.5 | ms | Bölüm 4 |
| Efferent iletim süresi | 10 | ms | Bölüm 4 |
| Stretch reflex gecikmesi (türetilen) | 20.5 | ms | Bölüm 4 |
| Golgi tendon reflex gecikmesi (türetilen) | 21 | ms | Bölüm 4 |
| Üst kol kütle / uzunluk | 1.86 / 29 | kg / cm | Tablo 2 |
| Önkol+el kütle / uzunluk | 1.53 / 40 | kg / cm | Tablo 2 |
| Optimal fascicle uzunluğu (biceps / brachialis / triceps lat.) | 21 / 10 / 11.38 | cm | Tablo 3 |
| Optimal tendon uzunluğu (biceps / brachialis / triceps lat.) | 16 / 8 / 9.8 | cm | Tablo 3 |
| Kas kütlesi (biceps / brachialis / triceps lat.) | 200 / 282 / 237 | g | Tablo 3 |
| Lif tipi (üç kas) | %50 yavaş + %50 hızlı | — | Tablo 3 |
| Gamma-MN transfer fonksiyonu | 1 (tek girdi: korteks) | — | Bölüm 3.1.1 |
| DE: F (scaling factor) / CR (crossover) | 0.5 / 0.2 | — | Bölüm 3.5 |
| DE Deney 1: jenerasyon / popülasyon | 600 / 20 | — | Bölüm 5.1 |
| DE Deney 2: toplam değerlendirme | 12 000 | — | Bölüm 5.3 |
| Dirsek eklem açı sınırı | 0 – 145 | ° | Bölüm 5.1 (reddetme ölçütü) |
| Kabul edilen çözüm hassasiyeti | hedefe ≤ 3 | ° | Bölüm 5.1 (kaynak [74]: 2–3° ayrım eşiği) |

---

## 4 · NE SONUÇ BULMUŞ

### 4a · Sayısal sonuçlar

| Büyüklük | Değer | Birim | Nereden | Saçılım (SD/SEM/aralık, n) |
|---|---|---|---|---|
| 18° hedefi: süre | 1.98 | s | Bölüm 5.1 (Tablo 6 verisi) | ±0.39 (SD; n=41 hareket, Tablo 6 satır sayımı) |
| 18° hedefi: enerji | 11.09 | J | Bölüm 5.1 | ±11.96 (SD) |
| 18° hedefi: pozisyon hatası | 0.75 | ° | Bölüm 5.1 | ±0.81 (SD) |
| 36° hedefi: süre | 2.09 | s | Bölüm 5.1 (Tablo 7 verisi) | ±0.55 (SD; n=25, Tablo 7 satır sayımı) |
| 36° hedefi: enerji | 15.34 | J | Bölüm 5.1 | ±15.40 (SD) |
| 36° hedefi: pozisyon hatası | 0.79 | ° | Bölüm 5.1 | ±0.87 (SD) |
| 72° hedefi: süre | 2.19 | s | Bölüm 5.1 (Tablo 8 verisi) | ±0.61 (SD; n=19, Tablo 8 satır sayımı) |
| 72° hedefi: enerji | 14.63 | J | Bölüm 5.1 | ±13.16 (SD) |
| 72° hedefi: pozisyon hatası | 1.66 | ° | Bölüm 5.1 | ±0.99 (SD) |
| En yavaş 18° hareketi (S3-M1-18): süre / enerji | 3.23 / 32.96 | s / J | Tablo 6 | tek hareket |
| En yavaş 36° hareketi (S8-M2-36): süre / enerji / son pozisyon | 2.98 / 1.03 / 34.20 | s / J / ° | Tablo 7; Bölüm 5.1 metni | tek hareket |
| En hızlı 36° hareketi (S6-M2-36): süre / enerji | 1.04 / 21.53 | s / J | Tablo 7 | tek hareket |
| En yavaş 72° hareketi (S12-M4-72): süre / enerji / hata | 3.24 / 52.72 / 2.83 | s / J / ° | Tablo 8; Bölüm 5.1 metni | tek hareket |
| Fitts, Strateji 1: a / b / R² / RMSE | 880.6 / 101.3 / 0.948 / 34.47 | (birim tabloda yok; bkz. 3c) | Tablo 10 | 8 ID noktası |
| Fitts, Strateji 2: a / b / R² / RMSE | 836.2 / 157.9 / 0.582 / 194.18 | (birim tabloda yok) | Tablo 10 | 8 ID noktası |
| Fitts, Strateji 3: a / b / R² / RMSE | 544 / 194.2 / 0.809 / 136.95 | (birim tabloda yok) | Tablo 10 | 8 ID noktası |
| Friedman testi, MaxDist metriği | H0 kabul (istatistik 0.08647, p=0.95768) | — | Bölüm 5.4 | anlamlılık düzeyi 0.05 |
| Friedman testi, Diff metriği | H0 ret (istatistik 6.1728, p=0.03657) | — | Bölüm 5.4 | anlamlılık düzeyi 0.05 |
| Holm post hoc: Strateji 2 vs 3 | H0 ret (p=0.00824) | — | Tablo 11 | Diff medyanları: 1.3985 / 1.2315 / 1.5201 (S1/S2/S3) |

### 4b · Niteliksel bulgular
- "the speed–accuracy tradeoff is not an intrinsic property of the neuromuscular system, but it is a behavioral trait that emerges from the strategy adopted by the central nervous system for executing faster movements" (Abstract).
- Deney 1'de sistem, aynı doğrulukta farklı hızlarda hareket üretebilir — CM→alpha-MN bağlantısı kullanılmadığında Fitts kanunu ortaya ÇIKMAZ (Bölüm 5.2: S2-M9-18 ile S1-M5-18 aynı doğruluğa 0.86 s fark ile ulaşır).
- Hız profilleri asimetrik çan biçimlidir; bu, Kinematic Theory of Rapid Human Movements'ın öngörüsüyle uyumludur (Bölüm 5.2; Şekil 5–7).
- Öğrenilen hareket sayısı hedef mesafe büyüdükçe azalır; yazarlar bunu geniş hareketlerin daha zor kontrol edilmesine bağlar (Bölüm 5.2).
- S3, S5, S9 ve S12 dışındaki her DE koşusunda en hızlı hareket, en yavaşa göre anlamlı biçimde daha çok enerji tüketir (Bölüm 5.2).
- Düşük enerjili çözümler çok yavaş, insan-benzeri görünmeyen fleksiyonlar üretir; yazarlar bunu agonist aktivasyonunu kısıp atalet + antagonistin pasif kuvvetiyle durmaya bağlar (Bölüm 6, "yorum" niteliğinde yazar açıklaması).

### 4c · Yazarların kendi çıkardığı sonuç
Hız–doğruluk ödünleşimi sistemin yapısından değil, önceden öğrenilmiş bir hareketin yalnızca alpha motoneuron aktivasyonu değiştirilerek hızlandırılması stratejisinden doğar; ödünleşim hem motor sistemin yapısının hem de hızlandırma stratejisinin ortak ürünüdür. CM→alpha-MN monosynaptic bağlantısının rollerinden biri, öğrenilmiş hareketin hızını ayarlamaktır. Gelecek işler: Parkinson/Alzheimer/yaşlanma etkileri ve 2B–3B görevlere genişletme (Bölüm 6–7). Yazarların koyduğu sınırlılık: DE'de global optimum garantisi yoktur; çözümler başlangıç durumuna bağlıdır (Bölüm 5.4).

---

## 5 · Projemize ilgisi
- **Doğrudan kullanılabilir mi?** Kısmen. Mimari ve yöntem düzeyinde evet; sayısal düzeyde hayır. Ağ topolojisi (IaIN, IbIN, Renshaw, PN, gamma static/dynamic, presynaptic modülasyon) bizim NEURON tarafında kuracağımız devrenin bire bir kontrol listesi gibidir. Sayılar ise insan dirseği + boyutsuz rate-code değerleri olduğundan aktarılamaz.
- **Hangi büyüklüğümüz veya parametremizle eşleşir?** (1) Devre şeması → NEURON ağ topolojisi kararı; (2) gecikme muhasebesi (afferent + merkezi + efferent = refleks gecikmesi) → bizim modelde de aynı muhasebe kurulmalı, ancak sıçan değerleriyle; (3) Virtual Muscle içindeki spindle modeli Mileusnic 2006'dır — bizim iğcik modeli aday kaynağımızla aynı köken; (4) reddetme ölçütleri (triphasic desen, tek reversal) → hareket makullüğü testleri için fikir.
- **Bilinen sistematik fark:** tür (insan vs Sprague-Dawley sıçanı), eklem (dirsek fleksiyonu vs arka bacak lokomosyonu), nöron modeli (boyutsuz rate-code logistic vs bizim iletkenlik tabanlı NEURON hücreleri, PIC/Cav1.3), görev (istemli erişme, CPG yok), öğrenme (DE ile enerji minimizasyonu; bizde CPG kaynaklı ritmik sürüş planlanır).
- **Nereye girdi olacak:** model yapısı kararı (omurilik devre topolojisi, gecikmelerin yerleştirilmesi) + tartışma/atıf (kapalı döngü omurilik modellerinin gerekçelendirilmesi; Tablo 4 literatür karşılaştırması hazır özet sunar).

## 6 · Bizimle çelişen veya işimize gelmeyen bulgular
- **Rate-code varsayımı bizim yaklaşımımızla çelişir:** makale, spike zamanlamasının bilgi taşımadığını varsayar (Bölüm 3.2). Bizim NEURON tarafımız spike üretir; Ia sinapsına spike zamanlaması girer. Bu makaleden alınacak her devre kararında bu varsayım farkı akılda tutulmalıdır.
- **Gamma motoneuron'lar bu modelde pasif geçittir** (transfer fonksiyonu = 1, tek girdi korteks; Bölüm 3.1.1). Bizim planımızda iğcik duyarlılığının gamma sürüşüyle modülasyonu önemlidir; bu makale o mekanizmayı fiilen devre dışı bırakır.
- **Enerji minimizasyonu amaç fonksiyonudur; lokomosyonda bu amaç tek başına geçerli olmayabilir:** makalenin öğrenme kurgusunun tamamı iki amaçlı DE'ye dayanır. CPG sürüşlü ritmik lokomosyon bu kurguya oturmaz.
- **Fitts sonucu istemli, tek eklemli, öğrenilmiş erişme hareketine aittir;** lokomosyon hız kontrolüne genellenebileceğine dair makalede kanıt yoktur.
- **Girdi biçimi step fonksiyonudur** (Bölüm 4): descending komutlar hareket boyunca sabittir. Bizim modelde CPG çıktısı zamanla değişir; girdi temsili bu yüzden aktarılamaz.

## 7 · Testlere girecek değerler (varsa)
Bu makaleden test çıkmıyor. Sayısal sonuçlar insan dirseği + boyutsuz nöron modeli koşullarına aittir; sıçan arka bacağı doğrulaması için referans aralık sağlamaz. (Gecikme değerleri de insan içindir; sıçanda aksonal mesafeler kısa olduğundan doğrudan test değeri yapılamaz.)

## 8 · Özete alınmayanlar
- Bölüm 2'nin literatür taraması ayrıntıları ve Tablo 4'ün satır satır içeriği (FLETE, Loeb grubu, Buhrmann, Stefanovic, Lan grubu, Teka, Parziale 2015 modellerinin tek tek özellikleri) — omurilik modeli literatürü gerektiğinde önce Tablo 4'e bakılır.
- Şekil 5, 6, 7'deki tek tek hareket eğrileri; Tablo 6–8'in tam satır listeleri (özete yalnız uç değerler alındı).
- Giriş bölümündeki uygulama alanı tartışmaları (BMI, protez, el yazısı tanıma) ve kaynakça.
- Eş. 3–5'in tam cebirsel açılımı (özete sözel tanımları alındı).

## 9 · Açık sorular / doğrulanmayanlar
- Fitts katsayılarının (a, b) birimi makalede açıkça yazılmaz; "yorum:" Şekil 8 ekseninden ms okunur.
- Tablo 6–8'deki n değerleri makale metninde toplam olarak verilmez; özetteki n=41/25/19 değerleri tablo satırlarının sayımıdır.
- "varsayım:" makale, öğrenilen hareket sayısındaki azalmayı kontrol zorluğuna bağlar ama bunun DE arama uzayı etkisinden ayrıştırıldığına dair analiz sunmaz.
- Kas origin/insertion noktalarının sayısal koordinatları makalede verilmez ([40, 98]'den uyarlandığı söylenir); gerekirse Holzbaur 2005 ve Song 2008 açılmalıdır.
