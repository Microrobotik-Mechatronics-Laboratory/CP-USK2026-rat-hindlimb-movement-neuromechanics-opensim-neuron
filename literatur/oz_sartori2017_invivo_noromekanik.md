# Literatür özeti — Sartori 2017 (in vivo nöromekanik, MN → eklem momenti)

> Bu dosya makalenin **seçici özetidir** — yerine geçmez. Amacı, makaleyi tekrar
> açmadan modelleme kararı verebilmektir.

## 1 · Künye ve sınıflandırma

- **Yazarlar / yıl:** Massimo Sartori, Utku Ş. Yavuz, Dario Farina / 2017 (kabul: 14 Eylül 2017; yayın: 18 Ekim 2017)
- **Başlık:** In Vivo Neuromechanics: Decoding Causal Motor Neuron Behavior with Resulting Musculoskeletal Function
- **Dergi / cilt / sayfa:** Scientific Reports, 7: 13465
- **DOI / PMC:** 10.1038/s41598-017-13766-6
- **PDF:** `pdf/In_Vivo_Neuromechanics_Decoding_Causal_Motor_Neuron_Behavior_with_Resulting_Musculoskeletal_Function.pdf` (repoya girmez)
- **Özeti çıkaran / tarih:** Claude / 2026-09-06

- **Makale tipi:** karma (deneysel ölçüm + bilgisayar modeli)
- **Projemizin hangi tarafına bakıyor:** köprü (motoneuron çıkışı → kas aktivasyonu → OpenSim tarzı Hill modeli → eklem momenti; açık döngü)
- **Bizim için değeri:** yöntem örneği (motoneuron sürüşünden u(t) üretme formülasyonu) + doğrulama referansı (açık döngü, kör doğrulama felsefesi) + sınırlı parametre kaynağı (aktivasyon dinamiği kısıtları)

## 2 · Makalenin sorusu ve ana iddiası
Makale, omurilik motoneuron aktivitesi ile eklem mekanik fonksiyonu arasındaki nedensel bağın sağlam insanda in vivo gözlenip gözlenemeyeceğini sorar. Yazarlar, HD-EMG'den ayrıştırılan alpha motoneuron deşarjlarını, kişiye özel kalibre edilmiş bir kas-iskelet modelini AÇIK DÖNGÜ (hiçbir düzeltici geri besleme olmadan) sürmek için kullanır ve görülmemiş koşullarda ayak bileği momentini kör tahmin eder. Ana iddia: eklem momenti yalnızca dekode edilmiş motoneuron bilgisiyle doğru tahmin edilebilir; bu, motoneuron aktivitesi ile moment kontrolü arasında nedensel ilişkinin gözlenebildiğini gösterir (Abstract; s. 2).

---

## 3 · NEYİ NASIL YAPMIŞ (yöntem)

### 3a · Denek / malzeme / model
- **Denekler:** 4 sağlıklı erkek; yaş 30 ± 1.9 yıl, kütle 68.3 ± 1.3 kg, boy 184 ± 2.1 cm. Etik onay: University Medical Center Göttingen, onay no 01/10/12; Helsinki Deklarasyonu (Methods, s. 10).
- **Görev:** dinamometrede (Biodex M3) oturarak izometrik ayak bileği plantar-dorsi fleksiyon kasılmaları; monitördeki referans izi takip edilir. Denek 1–3: %30, 50, 70, 90 MVC (değişken moment eğimi); denek 4: %20, 30, 40, 50, 60 MVC (sabit eğim, 10 %MVC/s). Her koşul 3 bilek açısında (anatomik, 10° dorsi, 10° plantar) ve 4 tekrar; diz 60°'de sabitlenir (Methods, s. 10).
- **Kayıt:** 256 kanallı HD-EMG (EMG-USB2, OT Bioelettronica), 2048 Hz, 12 bit; üç adet 64 kanallı grid (tibialis anterior, soleus, gastrocnemius medialis) + iki adet 32 kanallı grid (gastrocnemius lateralis, peroneus grubu); elektrot arası 10 mm; monopolar kayıt → bipolar türetme. Toplam 7 musculotendon ünitesi (MTU) temsil edilir (Methods, s. 10). Ayrıca kuvvet platformu (Bertec, 2048 Hz), 7 kameralı hareket yakalama (Qualisys, 256 Hz), 18 retro-reflektif işaretleyici (Methods, s. 10).

### 3b · Yöntem adımları
1. HD-EMG 10–500 Hz bant geçiren filtreden geçirilir ve convolutive blind source separation (deconvolution) ile motoneuron deşarjlarına ayrıştırılır; yalnız PNR ≥ 0.9 olan motoneuron'lar raporlanır (Methods, s. 10).
2. Tek MN spike train'leri birleştirilip cumulative spike train (CST) oluşturulur; ardışık spike aralığının tersi ile deşarj hızı DR hesaplanır (Eş. 1); DR 500 örneklik kayan pencereyle düzleştirilir (s. 11).
3. DR desenleri, myotomal harita (Kendall) ağırlıklarıyla L4–S3 omurilik segmentlerine haritalanır (Eş. 2, s. 11).
4. CST, kritik sönümlü, doğrusal, ikinci derece özyinelemeli filtreden geçirilerek nöral aktivasyon u(t) üretilir (Eş. 3): u(t) = α·x(t−d) − β1·u(t−1) − β2·u(t−2); kısıtlar β1 = C1 + C2, β2 = C1·C2, α − β1 − β2 = 1, −1 < C1, C2 < 0; d elektromekanik gecikmedir. u(t), CST'ye ayrışmayan artık EMG ile toplanır (s. 11).
5. Aktivasyon doğrusal olmayan biçim faktöründen geçirilir (Eş. 4): a(t) = (e^{A·u(t)} − 1)/(e^A − 1), −3 < A < 0 (s. 11).
6. OpenSim ile jenerik alt ekstremite geometri modeli deneğe ölçeklenir: 5 serbestlik derecesi (kalça 3, diz 1, bilek 1), 7 MTU. MTU uzunluk/moment kolları, eklem açılarının fonksiyonu olarak çok boyutlu kübik B-spline'larla sentezlenir. Hill tipi kas modeli MTU kuvvetini, eklem dinamiği bileşeni momenti hesaplar (Methods, s. 11).
7. Offline kalibrasyon (simulated annealing): C1, C2, A (bütün MTU'lara ortak); iki kuvvet katsayısı (0.5–1.5 aralığında; dorsi ve plantar grupları ayrı ayrı ölçekler); tendon slack length ±%8 ve optimal fiber length ±%3 aralığında ayarlanır. Kalibrasyon verisi: denek başına en düşük %MVC koşulundan 6 deneme (denek 1–3: %30 MVC; denek 4: %20 MVC) (Methods, s. 12).
8. Doğrulama: kalibrasyonda kullanılmayan 207 deneme (denek başına 50, 48, 49, 60; 51.7 ± 5.6) üzerinde, deneysel moment bilgisi olmadan (kör), açık döngü tahmin; R², NRMSE ve Chebyshev %90 güven aralığı (beklenen aralık = ortalama ± 3.16·SD) hesaplanır (Methods, s. 12).
9. Karşılaştırma: aynı tahmin, MN deşarjları yerine interferent HD-EMG doğrusal zarflarıyla tekrarlanır (30 Hz yüksek geçiren, tam dalga doğrultma, 2 Hz alçak geçiren, zirveye normalize; Methods s. 10; sonuç Şekil S1).

### 3c · Tanım ve birim uyarıları
- **"Neural drive" tanımı:** kasa giden net nöral sürüş = dekode edilen MN havuzunun CST'si; havuz, gerçek havuzun yalnızca bir alt kümesidir (s. 6). Bizim modelde neural drive, simüle MN havuzunun tamamından gelir — kapsam farkı vardır.
- **Aktivasyon iki katmanlıdır:** u(t) (nöral aktivasyon, Eş. 3) ile a(t) (kas aktivasyonu, Eş. 4) ayrı büyüklüklerdir; a(t) doğrusal olmayan dönüşümün çıktısıdır. OpenSim'e giden "activation" bu a(t)'dir; iki katman birbirine karıştırılmamalıdır.
- **NRMSE tanımı:** RMSE, deneysel büyüklüğün karekök ortalama karesel TOPLAMINA normalize edilir (s. 12) — zirveye veya aralığa normalize NRMSE tanımlarıyla karşılaştırılamaz.
- **DR birimi pps'tir (pulses per second)** ve CST üzerinden havuz düzeyinde tanımlıdır; tek hücre ISI analiziyle karıştırılmamalıdır (Eş. 1, s. 11).
- **%cycle ekseni:** %0 dorsi-fleksiyon fazının başlangıcı, %100 plantar-fleksiyon fazının bitişidir (Şekil 4 açıklaması).

### 3d · Kullanılan parametreler ve değerleri

| Parametre | Değer | Birim | Nereden |
|---|---|---|---|
| HD-EMG örnekleme / bant | 2048 / 10–500 | Hz | Methods, s. 10 |
| PNR eşiği | ≥ 0.9 | — | Methods, s. 10 |
| DR düzleştirme penceresi | 500 | örnek | s. 11 |
| Eş. 3 kısıtları | β1=C1+C2; β2=C1·C2; α−β1−β2=1; −1<C1,C2<0 | — | s. 11 |
| Biçim faktörü A aralığı | −3 < A < 0 | — | Eş. 4, s. 11 |
| Kuvvet katsayısı aralığı | 0.5 – 1.5 | — | Methods, s. 12 |
| Tendon slack length ayar aralığı | ±8 | % | Methods, s. 12 |
| Optimal fiber length ayar aralığı | ±3 | % | Methods, s. 12 |
| Geometri modeli | 5 DOF, 7 MTU | — | Methods, s. 11 |
| Kalibrasyon verisi | 6 deneme/denek (en düşük %MVC) | — | Methods, s. 12 |
| Chebyshev aralığı | ortalama ± 3.16·SD | — | Methods, s. 12 |
| Dinamometre moment filtresi | 2 (alçak geçiren) | Hz | Methods, s. 10 |
| GRF/marker filtresi | 6 (alçak geçiren, 4. derece Butterworth) | Hz | Methods, s. 10 |

## 4 · NE SONUÇ BULMUŞ

### 4a · Sayısal sonuçlar

| Büyüklük | Değer | Birim | Nereden | Saçılım (SD/SEM/aralık, n) |
|---|---|---|---|---|
| Kas başına dekode edilen MN sayısı | > 10 (ortalama) | adet | s. 2 | soleus 13–29; tibant 12–26; gasmed 3–17; gaslat 2–12; peroneus 5–14 |
| Toplam dekode MN (7 kas) | 56.7 | adet | s. 5, s. 8 | ±10.2 |
| Tek MN deşarj hızı üst sınırı | ≤ 44.4 | pps | s. 2 (fizyolojik aralık, kaynak [35]) | tibant 3.3–40.3; soleus 3.9–40.1; peroneus 5.9–42.7; gasmed 4.6–44.3; gaslat 9.7–44.4 |
| Sakral segment aktivitesi (%20→%30 MVC, plantar) | 96.4 → 106.3 | pps | s. 2, Şekil 3 | — |
| Lumbar segment aktivitesi (%20→%30 MVC, dorsi) | 57.6 → 70.6 | pps | s. 2, Şekil 3 | — |
| Toplam MN ateşlemesi %20→%90 MVC (soleus) | 208.0 → 268.9 | pps | s. 4 | ±19.9 → ±99.2 |
| Toplam MN ateşlemesi %20→%90 MVC (tibialis anterior) | 278.6 → 374.4 | pps | s. 4 | ±95.6 → ±118.5 |
| Doğrulama denemesi sayısı | 207 (50, 48, 49, 60) | deneme | s. 5, s. 12 | denek başına 51.7 ± 5.6 |
| Kör tahmin R² aralığı | 0.82 – 0.99 | — | s. 5, Şekil 8 | Chebyshev %90 alt sınırı R² = 0.88 |
| Kör tahmin NRMSE aralığı | 0.13 – 0.58 | — | s. 5, Şekil 8 | Chebyshev üst sınırı NRMSE = 0.57 |
| R² > 0.9 olan tahmin oranı | 97 | % | s. 5 | 207 tahmin içinde |
| NRMSE < 0.4 olan tahmin oranı | 87 | % | s. 5 | 207 tahmin içinde |
| Tipik değerler | R² 0.96; NRMSE 0.3 | — | s. 6 | ±0.03; ±0.02 |
| Moment–MN aktivasyon şekil benzerliği (MN tabanlı) | R² ort. 0.97 | — | s. 6 | ±0.01; aralık 0.87–1 |
| Aynı benzerlik (HD-EMG doğrusal zarf ile) | R² ort. 0.92 | — | s. 6, Şekil S1 | ±0.05; aralık 0.67–0.98 |
| Kas bazında moment–aktivasyon R² (soleus) | 0.97 | — | s. 5, Şekil 5 | ±0.01; aralık 0.91–0.99 |
| Kas bazında R² (tibialis anterior) | 0.97 | — | s. 5, Şekil 5 | ±0.02; aralık 0.88–0.99 |
| Görülmemiş %MVC koşulu sayısı (ekstrapolasyon) | 15 | koşul | s. 9 | — |

### 4b · Niteliksel bulgular
- "the modulation of total motor neuron firing was a predominant mechanism of net joint moment control" (s. 4): zamanla değişen momentin şekli, CST'den türetilen nöral aktivasyonun şeklini taklit eder.
- Kas-iskelet sistemi, omurilik segment çıkışının doğal bir alçak geçiren filtresi gibi davranır; kuvvet modülasyonundan sorumlu CST bileşeni düşük frekans bandındadır (s. 9).
- Yavaş aktivasyon profilleri, MN havuzlarına inen ortak sinaptik girdiyi (common drive) yansıtır; ortak sürüşün, %20–%90 MVC aralığında mekanik fonksiyon modülasyonunun birincil nöral mekanizması olduğu öne sürülür (s. 9).
- Görülmemiş koşullarda başarı, modelin girdi-çıktı ezberlemediğini, nöromekanik dönüşümü gerçekten sentezlediğini gösterir (s. 9).
- Yazarların yorumu: bu formülasyonda kaslar omurilik nöral çıkışının "biyolojik yükselteçleri" olur; kas-iskelet modeli, deşarjları kuvvete çeviren dinamik süreçtir (s. 8).

### 4c · Yazarların kendi çıkardığı sonuç
İnsan merkezi sinir sistemine bir pencere açan yeni bir paradigma önerilmiştir: HD-EMG uzamsal örnekleme + MN dekodlama + nöral veri sürüşlü kas-iskelet modeli, alpha-MN'lerin ürettiği mekanik kuvvetleri in vivo gözlemeyi sağlar. Sınırlılıklar: 4 denek (genellenebilirlik sınırlı); tek kas-tendon düzeyinde doğrulama yapılmamıştır (insanda tek kas kuvveti ölçülemediği için). Gelecek işler: zaman ölçekleri arası ekstrapolasyon, lokomosyon gibi dinamik kasılmalara taşıma, nöro-mekanik insan-makine arayüzleri (s. 9).

---

## 5 · Projemize ilgisi
- **Doğrudan kullanılabilir mi?** Kısmen — formülasyon düzeyinde evet. MN spike train → CST → ikinci derece filtre u(t) → doğrusal olmayan a(t) → Hill modeli zinciri, bizim "motonöron çıkışı → kas aktivasyonu u(t)" köprümüzün yayımlanmış bir şablonudur. Sayısal katsayılar (C1, C2, A) deneğe özel kalibre edildiğinden aktarılamaz; ama kısıt aralıkları (3d tablosu) başlangıç noktası verir.
- **Hangi büyüklüğümüz veya parametremizle eşleşir?** (1) Eş. 3–4 → bizim NEURON MN çıktısını OpenSim aktivasyonuna çeviren ara katman; (2) açık döngü + kör doğrulama kurgusu → bizim doğrulama protokolü tasarımı (kapalı döngüyü açıp yalnız MN sürüşüyle moment tahmini bir ara doğrulama basamağı olabilir); (3) "kas-iskelet = alçak geçiren filtre" bulgusu → CPG/MN çıktımızın yüksek frekans bileşenlerinin moment üzerinde neden az iz bırakacağının mekanizması.
- **Bilinen sistematik fark:** tür (insan vs sıçan), kas grubu (bilek plantar/dorsi fleksörleri vs arka bacak), koşul (izometrik vs lokomosyon; makale kendisi lokomosyona taşınmayı "future work" ilan eder, s. 9), MN kaynağı (in vivo dekodlanmış vs bizde NEURON ile simüle), döngü (açık vs bizde Ia geri beslemeli kapalı).
- **Nereye girdi olacak:** model yapısı kararı (MN→aktivasyon dönüşümünün matematiği) + doğrulama testi tasarımı (kör, görülmemiş koşul ilkesi) + tartışma/atıf.

## 6 · Bizimle çelişen veya işimize gelmeyen bulgular
- **Makale açık döngünün yeterliliğini gösterir; bizim projemizin çekirdeği kapalı döngüdür.** İzometrik moment kontrolünde geri besleme düzeltmesi olmadan R² 0.82–0.99 elde edilmesi, "Ia geri beslemesi moment üretimi için gerekli" varsayımımızı bu koşulda desteklemez. Karşı okuma: görev izometriktir ve iğcik uzunluk değişimi minimaldir; lokomosyonda aynı sonuç beklenemez (yazarlar da dinamik kasılmaları future work sayar, s. 9).
- **Yöntem ölçülmüş MN deşarjı gerektirir; bizde ölçüm yok, simülasyon var.** Nedensellik iddiası "gerçek deşarj → model" yönünde kurulmuştur; bizim yönümüz "simüle deşarj → model"dir ve bu makale simüle deşarjın gerçekçiliği hakkında hiçbir şey söylemez.
- **Kalibrasyon deneğe özel deneysel moment verisi ister** (6 deneme); sıçan modelimizde birebir karşılığı olan kalibrasyon verisi (in vivo bilek momenti) elimizde yoktur — kalibrasyon stratejisi doğrudan kopyalanamaz.
- **DR üst sınırı 44.4 pps insan motor ünitelerine aittir** (kaynak [35]); sıçan MN ateşleme hızları için doğrulama eşiği olarak kullanılamaz.

## 7 · Testlere girecek değerler (varsa)
Bu makaleden test çıkmıyor. Bütün sayısal sonuçlar insan bileği izometrik koşuluna ve deneğe özel kalibrasyona bağlıdır; sıçan modeli için referans aralık üretmez. (Doğrulama FELSEFESİ — kör, görülmemiş koşul, R²+NRMSE çifti — test tasarımına girer ama sayı taşımaz.)

## 8 · Özete alınmayanlar
- Supplementary Video S1 (soleus için spike→kuvvet dönüşümünün görselleştirmesi) ve Şekil S1'in tam içeriği.
- Şekil 7'deki MTU başına ara değişken izleri (fiber length, pennation angle, tendon length, tendon force zaman serileri).
- Myotomal haritalama ağırlıkları k_ij (kaynak [54–56]'ya gönderilir; makalede sayı verilmez).
- Giriş bölümünün literatür gerekçelendirmesi ve 61 maddelik kaynakça.
- "Data and code are available upon request" notu (Accession codes, s. 12).

## 9 · Açık sorular / doğrulanmayanlar
- C1, C2, A ve elektromekanik gecikme d'nin kalibre edilmiş sayısal değerleri makalede raporlanmaz; yalnız kısıt aralıkları verilir.
- Gastrocnemius medialis %90 MVC toplam ateşleme saçılımı metinde "±122.1.6" biçiminde basılmıştır (s. 4) — baskı hatasıdır, gerçek değer belirsizdir; bu sayı kullanılacaksa yazarlardan/başka kaynaktan doğrulanmalıdır.
- "varsayım:" özet, Şekil 8'in R²/NRMSE aralıklarını metindeki değerlerle eşit kabul eder; şekilden bağımsız sayı okunmamıştır.
- Hill modeli parametrelerinin tam listesi kaynak [52, 61]'e gönderilir; gerekirse Sartori 2012 açılmalıdır.
