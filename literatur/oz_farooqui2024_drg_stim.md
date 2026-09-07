# Literatür özeti — Farooqui ve ark. 2024 (DRG stimülasyonunda seçicilik: morfoloji + uzamsal dağılım)

> Bu dosya makalenin **seçici özetidir** — yerine geçmez. Amacı, makaleyi tekrar
> açmadan modelleme kararı verebilmektir.

## 1 · Künye ve sınıflandırma

- **Yazarlar / yıl:** Juhi Farooqui, Ameya C. Nanivadekar (eşit katkılı), Marco Capogrosso, Scott F. Lempka, Lee E. Fisher — 2024
- **Başlık:** The effects of neuron morphology and spatial distribution on the selectivity of dorsal root ganglion stimulation
- **Dergi / cilt / sayfa:** Journal of Neural Engineering, 21, 056030
- **DOI / PMC:** DOI 10.1088/1741-2552/ad7760 (Open Access; veri: github.com/pitt-rnel/DRG-model-data2024; nöron modeli: modeldb.science/2018004)
- **PDF:** `pdf/The_effects_of_neuron_morphology_and_spatial_distribution_on_the_selectivity_of_dorsal_root_ganglion_stimulation.pdf` (repoya girmez)
- **Özeti çıkaran / tarih:** Claude (Deniz'in isteğiyle) / 06.09.2026

- **Makale tipi:** bilgisayar modeli (FEM + NEURON birleşik simülasyon)
- **Projemizin hangi tarafına bakıyor:** nöron (NEURON) — duyusal afferent akson modelleme yöntemi; doğrudan konu (DRG stimülasyonu, nöroprotez) bizim kapalı döngünün dışında
- **Bizim için değeri:** yöntem örneği (birincil: NEURON'da pseudounipolar duyusal nöron / MRG tabanlı duyusal akson modellemesi) · dolaylı parametre kaynağı (akson/soma/AIS iletkenlik değerleri, feline)

## 2 · Makalenin sorusu ve ana iddiası

Protez kullanıcılarına dokunsal geri besleme için DRG (dorsal root ganglion) uyarımı umut vericidir; ama klinik açıdan tercih edilen epineural makroelektrotların, çok daha küçük temas alanlı penetran mikroelektrotlarla karşılaştırılabilir seçicilik göstermesi (önceki kedi deneyi, Nanivadekar ve ark. 2019) açıklanamıyordu. Yazarlar bu mekanizmayı anatomik ve nörofizyolojik olarak gerçekçi hesaplamalı modellerle aramış. Ana iddia: DRG'nin kendine özgü anatomisi — hücre gövdelerinin çevrede (circumference), aksonların iç bölgede yoğunlaşması — ve pseudounipolar morfoloji, epineural uyarımda aktivasyonun soma bitişiğindeki AIS'te (axon initial segment) başlamasını ve geniş dinamik aralık oluşmasını sağlar; penetran elektrot ise t-junction ve aksonları uyarır. Bu yüzden epineural DRG uyarımı, invaziv olmadan yüksek seçicilik verebilir.

---

## 3 · NEYİ NASIL YAPMIŞ (yöntem)

### 3a · Denek / malzeme / model

- Model tipi: iki katmanlı hesaplamalı model. (1) FEM (finite element method): feline L6 DRG'nin ve çevre dokuların anatomik/elektriksel kopyası, 0,0001 mm çözünürlük (makalede böyle yazıyor; bkz. Bölüm 9); uyarımın hücre dışı potansiyel alanını hesaplıyor. (2) NEURON 7.7: çok bölmeli pseudounipolar nöron modelleri bu potansiyel alanına yerleştirilip transmembran iyonik akım dinamiği simüle ediliyor. Zaman adımı 5 µs, simülasyon süresi 10 ms.
- Nöron tipleri: Aα (büyük çap; kas innerve eden) ve Aβ (orta çap; deri reseptörü) — yalnız bu ikisi modele alınmış. Akson çapları 6–20 µm arası sürekli dağılımdan (feline histolojiye lognormal fit; Lloyd ve Chang 1948 verisi).
- Akson modeli: McIntyre–Richardson–Grill (MRG 2002) memeli motor akson çift-kablo modeli, duyusal aksona dönüştürülmüş iyon kanalı değişiklikleriyle (aşağıda 3b-4).
- Üç DRG konfigürasyonu: (1) axon-only (yalnız geçiş aksonları), (2) random (pseudounipolar nöronlar rastgele), (3) realistic (hücre gövdeleri literatürdeki gerçek dağılımla çevreye yoğun; Ostrowski 2017, Sperry 2020). Her model 10.000–20.000 nöron.
- Elektrotlar (önceki kedi deneyindekilerin kopyası): (1) epineural platin elektrot, 375 µm çaplı temas, DRG dorsal yüzeyinde; (2) tek şaftlı Utah dizisi, DRG merkezine 1 mm penetrasyon, uç 50 µm boy × tabanda 22,5 µm çap.

### 3b · Yöntem adımları

1. FEM geometrisi: DRG genişlemesi prolat sferoit (yarı-büyük eksen 3,7 mm; yarı-küçük eksen 1,5 mm); periferik ve dorsal kök dalları 15 cm uzunluğunda, 0,75 mm yarıçaplı silindirler, sferoide merkezden 3,25 mm'de bağlı; 20 µm epineuryum kılıfı; çevrede intraforaminal doku (3,25 mm yarıçap) ve kemik (17,2 mm yarıçap) silindirleri; dışta salin, dış yüzeyler 0 V sınır koşulu.
2. Yazarlar 1 mA'lik birim akımı temas yüzeyinden sürüp alanı çözmüş; simülasyonda bu alan −1 ve istenen genlikle ölçeklenerek katodik-öncü darbe modellenmiş.
3. Uyarım darbesi: bifazik, yük dengeli, katodik-öncü; katodik faz 80 µs, hemen ardından yarı genlikte ve iki kat sürede anodik faz. Alım eşiği (recruitment threshold) her nöron için genlik üzerinde ikili arama (binary search) ile bulunmuş.
4. Nöron modeli bölümleri: soma + AIS + stem akson (t-junction'da biten) + t-junction'dan ayrılan periferik ve dorsal kök aksonları; ayrıca gövdesiz "axons of passage". Ayrıntılar: periferik/dorsal kök aksonları 50'şer adet 1 µm'lik Ranvier düğümü; geçiş aksonları 100 düğüm. Duyusal dönüşüm: düğüm ve internoda hızlı K (Kf) eklendi; internoda yavaş K (Ks), kaçak (Lk) ve HCN kanalları eklendi; düğüm Lk 6→8 mS/cm² (başlangıç hiperpolarizasyonunu azaltmak için); Ks β hız sabitinin A parametresi 0,06 (AHP'yi deneysel değere oturtmak için).
5. Sürekli çap temsili: MRG'nin ayrık çap seti yerine, iletkenlik/internodal mesafe/miyelin lamella sayısının çapla ilişkisine eğri uydurulmuş (curve fitting) ve 6–20 µm arası modeller bu eğrilerden kurulmuş. Dorsal kök akson çapı = periferik çapın 0,87'si (Şekil 2b'de "0,87D − 0,67 µm" olarak çizili; s. 4–5).
6. Soma: büyük bir akson düğümü gibi tanımlı; çapı ve boyu periferik akson çapıyla 2,78 çarpanıyla ölçekleniyor (Şekil 2b'de "2,78D + 40,56 µm"; bkz. Bölüm 9); soma Naf/Nap kanal yoğunluğu 300 kanal/µm² (akson düğümündeki 2.000'den düşürülmüş; freeze-fracture verisi, Matsumoto ve Rosenbluth 1985).
7. AIS üç parça: proksimal 6 µm (Naf/Nap 1.000 kanal/µm²), ara 194 µm (600 kanal/µm²), distal 1 µm (düğümle aynı, 2.000 kanal/µm²; literatürdeki "heminode"). Stem akson: dört internodal bölge özel miyelin kalınlığı/uzunluğuyla; AIS dahil sabit 784 µm.
8. Doğrulama: Aβ (7,3 µm) ve Aα (16,0 µm) için AP şekli parametreleri literatür aralıklarıyla karşılaştırılmış (Tablo 3; iki parametre aralık dışı — Bölüm 6'da). CV, periferik akson çapıyla doğrusal, çarpan 5,29. AIS kanal yoğunluğu duyarlılık analizi: her iki AIS bölümü 800 kanal/µm²'yi aşınca gerçekdışı spontan ateşleme.
9. Yerleştirme: özel 3B paketleme algoritması. Realistic: her nöron için %10 olasılıkla gövde DRG hacminde tamamen rastgele; kalan %90'da gövde çevre halkasına (açıya göre kesme yarıçapı: 30°–150° arasında toplam yarıçapın 2/3'ü, aksi halde 4/5'i; boylamda orta noktadan ±2.000 µm); gövdeler dışa, stem aksonlar merkeze yönelik (±10°); çakışma kontrolü var. Random: tamamen rastgele konum + rastgele stem yönelimi. Axon-only: yalnız rastgele geçiş aksonları.
10. Örnekleme: her model×elektrot için simüle nöronlardan 2.500'lük rastgele alt örneklem, 100 tekrar. Axon-only modelde karşılaştırılabilirlik için hacim kısıtı: penetran için merkez 800 µm yarıçap (~7.700 akson); epineural için merkez çizgisinin >537 µm üstü (~6.400 nöron).
11. Çıktılar: ilk aktive olan nöronların aktivasyon bölgesi (AIS / stem / t-junction / pseudounipolar akson / geçiş aksonu), elektrot eşikleri, alım eğrisi eğimi (dinamik aralık ölçüsü), Aα–Aβ ayrışması, elektrot konum kaydırma testleri (+0,75 mm distal, −0,75 mm proksimal, +0,75 mm lateral).

### 3c · Tanım ve birim uyarıları

- **"Elektrot eşiği" = tek bir nöronu aktive eden minimum genlik** (hesaplamalı modelde); önceki kedi deneyindeki eşik ise tek bir periferik sinir dalının seçici aktivasyonu. İki eşik sayısal olarak karşılaştırılamaz; yalnız epineural/penetran oranı karşılaştırılabilir (~10 kat, iki çalışmada da).
- **"Dinamik aralık" burada alım eğrisinin doğrusal bölümüne uydurulan regresyon doğrusunun eğimidir; küçük eğim = geniş aralık.** Algısal ayırt edilebilirlik ölçülmemiştir; yazarlar bunu açıkça söylüyor.
- **n kanal yoğunlukları kanal/µm², iletkenlikler S/cm²** — iki ayrı birim ailesi; karıştırılmamalı.
- **"Realistic" bile basitleştirilmiş:** glomerüler (dolambaçlı) stem trajektorisi ve stem aksonun gövdeyi sarması modellenmemiş (Tartışma).
- DRG iletkenliği anizotropik: boylamasına 0,6, enine 0,083 S/m — izotropik varsayım yapılmamalı.

### 3d · Kullanılan parametreler ve değerleri

Doku iletkenlikleri (Tablo 1, s. 4):

| Parametre | Değer | Birim | Nereden |
|---|---|---|---|
| Gri madde | 0,23 | S/m | Tablo 1 |
| DRG boylamasına / enine | 0,6 / 0,083 | S/m | Tablo 1 |
| Epineuryum | 0,6 | S/m | Tablo 1 |
| Kemik | 0,02 | S/m | Tablo 1 |
| Ekstranöral doku | 0,25 | S/m | Tablo 1 |
| Kapsülasyon (encapsulation) dokusu | 0,17 | S/m | Tablo 1 |
| Platin | 9,4 × 10⁶ | S/m | Tablo 1 |

Nöron modeli elektrik parametreleri (Tablo 2, s. 6):

| Parametre | Değer | Birim | Nereden |
|---|---|---|---|
| Aksoplazmik özdirenç | 70 | Ω·cm | Tablo 2 |
| Spesifik membran kapasitansı | 2 (internodal bölmelerde çapla ölçekli) | µF/cm² | Tablo 2 |
| Miyelin iletkenliği / kapasitansı (lamella başına) | 0,001 / 0,1 | S/cm² / µF/cm² | Tablo 2 |
| Soma: Naf / Nap | 0,45 / 0,0015 | S/cm² | Tablo 2 |
| AIS proksimal: Naf / Nap | 1,5 / 0,005 | S/cm² | Tablo 2 |
| AIS ara: Naf / Nap | 0,90 / 0,003 | S/cm² | Tablo 2 |
| Düğüm: Naf / Nap / Kf / Ks / Lk | 3 / 0,01 / 0,02737 / 0,04106 / 0,008 | S/cm² | Tablo 2 |
| Soma ve AIS kanal yoğunlukları | soma 300; AIS 1.000/600/2.000; düğüm 2.000 | kanal/µm² | Bölüm 2.4–2.5, s. 5–6 |
| Stem akson toplam boyu (AIS dahil) | 784 | µm | Bölüm 2.6, s. 6 |
| Akson çap dağılımı | 6–20 (lognormal, feline) | µm | Şekil 2c, s. 5 |
| Dorsal kök / periferik çap oranı | 0,87 | — | Bölüm 2.3, s. 4 |
| Soma boyut ölçekleme çarpanı | 2,78 | — | Bölüm 2.4, s. 5 |
| Uyarım darbesi | katodik 80 µs; anodik ½ genlik × 2 süre | — | Bölüm 2.9, s. 8 |
| Zaman adımı / simülasyon süresi | 5 µs / 10 ms | — | Bölüm 2.9, s. 7–8 |

### Doğrulama değerleri (Tablo 3, s. 7; * = literatür aralığı dışında):

| Parametre | Model değeri | Literatür aralığı |
|---|---|---|
| Aβ (7,3 µm): soma AP genliği | 118,62 mV | 109,72 ± 11,21 mV |
| Aβ: soma AP süresi | 0,71 ms | 1,29 ± 0,59 ms |
| Aβ: soma AHP genliği | 3,48 mV* | 7,9 ± 4,2 mV |
| Aβ: akson AP genliği | 102,59 mV | 109,72 ± 11,21 mV |
| Aβ: iletim hızı | 33,09 m/s | 18,87 ± 16,32 m/s |
| Aα (16,0 µm): soma AP genliği | 118,86 mV | 109,72 ± 11,21 mV |
| Aα: soma AP süresi | 0,71 ms | 0,98 ± 0,2 ms |
| Aα: soma AHP genliği | 3,36 mV | 6,5 ± 4,2 mV |
| Aα: akson AP genliği | 103,71 mV | 109,72 ± 11,21 mV |
| Aα: iletim hızı | 81,95 m/s* | 89,7 ± 7,6 m/s |

---

## 4 · NE SONUÇ BULMUŞ

### 4a · Sayısal sonuçlar

| Büyüklük | Değer | Birim | Nereden | Saçılım (SD/SEM/aralık, n) |
|---|---|---|---|---|
| Genel elektrot eşiği — epineural (axon-only / random / realistic) | 21,15 / 26,04 / 22,36 | µA | Tablo 4, s. 10 | tüm hücreler üzerinden tek değer |
| Genel elektrot eşiği — penetran | 1,45 / 1,33 / 1,16 | µA | Tablo 4, s. 10 | — |
| Medyan eşik (100 alt örneklem) — epineural | 21,52 / 28,38 / 28,53 | µA | Tablo 4, s. 10 | IQR: (21,15–21,82) / (26,04–30,98) / (25,10–31,76) |
| Medyan eşik — penetran | 3,92 / 1,60 / 2,56 | µA | Tablo 4, s. 10 | IQR: (2,66–5,85) / (1,33–2,45) / (1,16–3,59) |
| Kedi deneyi (empirik) medyan seçici eşik: epineural / penetran | 117,93 / 10,98 | µA | Tablo 4, s. 10 | model ve deney arasında ~10 kat oran uyumu |
| Alım eğrisi eğimi (medyan) — epineural (axon-only / random / realistic) | 8,00 / 1,62 / 1,87 | nöron/µA (yorum: eğim) | Tablo 5, s. 11 | 100 alt örneklem; küçük eğim = geniş dinamik aralık |
| Alım eğrisi eğimi — penetran | 8,09 / 3,20 / 6,48 | nöron/µA | Tablo 5, s. 11 | epineural < penetran her modelde; Kruskal–Wallis p ≪ 0,001 |
| Model benzerlik skoru S (random↔realistic) | epineural −0,633; penetran 0,934 | — | Bölüm 3.1, s. 9–10 | ilk 20 nöron, 100 alt örneklem medyanı |
| Elektrot kaydırma benzerlikleri (merkeze göre) | epineural: 0,842 (+0,75x) / 0,930 (−0,75x) / 1,0 (+0,75z); penetran: 0,980 / 0,987 / −1,121 (+0,75z lateral) | — | Bölüm 3.5, s. 13 | lateral kaydırılmış penetran belirgin sapıyor |
| Klinik stimülatör bağlamı: 100 µA adımla | penetran tüm nöronları 1 adımda; epineural 4 adımda | — | Bölüm 3.3, s. 13 | model içi çıkarım; Tartışma'yla çelişiyor, bkz. Bölüm 9 |
| 1 µA adımla ayırt edilebilir basamak | penetran ~100; epineural ~400 | adet | Bölüm 3.3, s. 13 | model içi çıkarım |

### 4b · Niteliksel bulgular

- **Aktivasyon bölgesi elektrota göre ayrışıyor:** realistic modelde epineural elektrot düşük eşikli nöronları ağırlıkla AIS'te (ve yakın geçiş aksonlarında) ateşliyor; penetran elektrot t-junction ve aksonlarda. Penetran için random ve realistic modeller neredeyse aynı davranıyor; epineural için çok farklı (Şekil 3, s. 9).
- **Somada hiç spike başlamıyor** (hiçbir koşulda); ama soma komşu bölmelerin elektriksel ortamını t-junction'a kadar etkiliyor: katodik fazda soma depolarize olurken AIS/stem/t-junction ters yanıt veriyor (Tartışma, s. 15).
- **Mekanizma yoğunluk üzerinden:** hücre gövdeleri aksonlardan çok büyük olduğu için gövde-zengin çevre bölgesi seyrek paketlenir; epineural elektrot büyük hacim uyarsa da aktive nöron sayısı aynı oranda artmaz → sığ alım eğrisi, geniş dinamik aralık (Tartışma, s. 15–16).
- **Eşik belirleyicileri:** penetran eşikler ağırlıkla elektrot–nöron mesafesine bağlı, lif çapına az duyarlı; epineural eşiklerde mesafe + lif çapı birlikte etkili (Şekil 4, s. 11).
- **Aα ve Aβ alım eğrileri ayrışmıyor:** hiçbir genlikte bir tip diğerini dışlayarak alınamıyor (Şekil 5d, s. 12–13) — duyusal modalite hedeflemesi bu yolla mümkün görünmüyor.
- **Epineural elektrot konum kaymasına dayanıklı; penetran elektrot lateral kaymada davranış değiştiriyor** (Şekil 6, s. 14).

### 4c · Yazarların kendi çıkardığı sonuç

DRG'nin pseudounipolar morfolojisi ve gövde/akson uzamsal ayrımı, epineural uyarıma hem seçicilik hem geniş dinamik aralık kazandırır; bu, mevcut klinik epineural elektrotlarla fokal duyusal geri besleme verilebileceğini düşündürür. Sınırlılıklar (yazarların sayımıyla): basitleştirilmiş akson trajektorileri (glomerulus ve gövde sarımı yok), model–deney eşik metriklerinin farklılığı, algısal çıktının modellenememesi; insan denemeleri gerekir (Tartışma ve Sonuç, s. 14–17).

---

## 5 · Projemize ilgisi

- **Doğrudan kullanılabilir mi?** Hayır (konu olarak): DRG uyarımı ve nöroprotez, sıçan arka bacak kapalı-döngü modelimizin parçası değil. Evet (yöntem olarak): NEURON'da duyusal afferent modelleme zincirinin güncel ve açık kodlu bir örneği.
- **Hangi büyüklüğümüz veya parametremizle eşleşir?** Bizim kas iğciği Ia/II afferent aksonlarımızı NEURON'da fiziksel akson olarak modellemek gerekirse: (1) MRG çift-kablo modelinin duyusal iyon kanalı modifikasyonları (Kf ekleme, Lk artırma, Ks β ayarı — bu makale + Graham 2019 + Gaines 2018 zinciri); (2) sürekli çap için eğri uydurma yaklaşımı; (3) CV–çap doğrusal ölçekleme (çarpan 5,29, feline) → afferent iletim gecikmelerinin çap dağılımından türetilmesi. Model kodu ModelDB 2018004'te indirilebilir.
- **Bilinen sistematik fark:** tür (feline ↔ sıçan; çap dağılımı ve CV çarpanı türe göre değişir); bölge (DRG gövde/AIS dinamiği ↔ bizde afferentin periferik/santral iletimi yeter; t-junction ve soma modellememize muhtemelen gerek yok); bağlam (dış elektrik uyarımı ↔ bizde iğcik reseptör potansiyelinden doğal ateşleme).
- **Nereye girdi olacak:** yöntem örneği. Parametre alınacaksa birincil zincir izlenmeli: MRG 2002 (akson), Gaines 2018 (duyusal/motor ayrımı), Graham 2019 (DRG duyusal nöron); bu makale o zincirin uygulanmış ve doğrulanmış bir bileşimidir.

## 6 · Bizimle çelişen veya işimize gelmeyen bulgular

- **Motor akson modeli duyusal aksona dönüştürülmeden kullanılamaz.** Bizim Ia afferentimizi "MRG'yi olduğu gibi al" diye modellersek bu makalenin düzelttiği hatayı işleriz: duyusal aksonda Kf/Ks/HCN farklıdır ve AHP/tekrarlı ateşleme davranışı değişir (Bölüm 2.3, s. 4–6).
- **Doğrulama sapmaları:** Aβ soma AHP genliği (3,48 mV, literatür 7,9±4,2) ve Aα CV (81,95 m/s, literatür 89,7±7,6) aralık dışı (Tablo 3). Yani bu parametre seti bile AHP'yi sistematik küçük üretiyor; aynı seti alırsak aynı sapmayı alırız.
- **Çapla seçicilik yok:** DRG uyarımında Aα, Aβ'dan ayrıştırılamıyor. "Büyük lif önce, seçici alınır" sezgisi burada tutmuyor; yazarlar periferik sinirdeki ters alım sırası beklentisiyle (ref. 79) bu bulgunun gerilimini kendileri not ediyor. Afferent tiplerini elektrikle seçici uyarma fikri ileride gündeme gelirse bu bulgu aleyhte kanıttır.
- **İşimize gelmeyen kapsam:** kas iğciği reseptör dinamiği, ateşleme kodlaması ve doğal (mekanik kaynaklı) afferent aktivite bu makalede hiç yok; iğcik→Ia dönüşümü için başka kaynak gerekir (ör. Mileusnic 2006).

## 7 · Testlere girecek değerler (varsa)

Bu makaleden test çıkmıyor. Gerekçe: doğrulanabilir çıktılar (eşikler, alım eğrileri) DRG-elektrot geometrisine özgü; bizim modelde karşılığı olan tek büyüklük CV–çap ilişkisi, onun da birincil kaynağı Boyd ve Kalu (1979, kedi) — test gerekirse oradan ve sıçan verisinden kurulmalı.

## 8 · Özete alınmayanlar

- Supplemental şekiller (CV ölçekleme fiti, AIS duyarlılık analizi eğrileri, log ölçekli dinamik aralık, gerilim izleri) — makale gövdesinde yalnız atıf var.
- Benzerlik skorunun (S) tam matematiği (N vektörleri üzerinde R² regresyonu; Bölüm 3.1, s. 9–10) — özet yalnız sonuç değerlerini aldı.
- Giriş bölümündeki nöroprotez/duyusal geri besleme literatür taraması (ref. 1–31) ve klinik DRG stimülatör onay süreci.
- Şekil 4'ün nokta bulutları (eşik–mesafe–çap ilişkisinin ham dağılımları).
- Yerleştirme algoritmasının çakışma/red kurallarının kod düzeyi ayrıntısı (GitHub deposunda).

## 9 · Açık sorular / doğrulanmayanlar

- **FEM çözünürlüğü "0,0001 mm" (= 0,1 µm) yazılmış** (Bölüm 2.1, s. 4). 17 mm yarıçaplı hacim için bu değer olağanüstü ince; birim veya basamak hatası olabilir. Doğrulanamadı; FEM ayrıntısı gerekirse GitHub deposuna bakılmalı.
- **Soma ölçeklemesi:** metin "2,78 çarpanıyla doğrusal" diyor; Şekil 2b "2,78D + 40,56 µm" (afin) gösteriyor. Varsayım: şekildeki afin biçim uygulanan biçimdir; metin kısaltılmış anlatımdır. Kod görülmeden kesinleştirilemez.
- **Stimülatör adımı iç çelişkisi:** Sonuçlar (Bölüm 3.3, s. 13), 100 µA adımla penetran için 1 adım / epineural için 4 adım ve 1 µA adımla 100'e karşı 400 basamak diyor; Tartışma (s. 16) aynı karşılaştırmayı Digitimer DS8r üzerinden 2 adıma karşı 5 adım olarak veriyor. Hangisi geçerli, makaleden çıkarılamıyor; özet tablosuna Sonuçlar'daki değerler alındı.
- Eğim (Tablo 5) birimi makalede açıkça yazılmamış; "her 1 µA artışta eklenen nöron sayısı" tanımından nöron/µA çıkarımı bizim yorumumuzdur (yorum olarak işaretli).
- Aβ soma AP süresi (0,71 ms; literatür 1,29±0,59) Tablo 3'te yıldızsız ama aralığın alt kenarına yakın; yazarlar yalnız iki parametreyi aralık dışı ilan ediyor.
