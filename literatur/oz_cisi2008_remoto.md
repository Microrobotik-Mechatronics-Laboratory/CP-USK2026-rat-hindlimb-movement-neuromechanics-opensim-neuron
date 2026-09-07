# Literatür özeti — Cisi & Kohn 2008 (ReMoto omurilik simülatörü)

> Bu dosya makalenin **seçici özetidir** — yerine geçmez. Amacı, makaleyi tekrar
> açmadan modelleme kararı verebilmektir.

## 1 · Künye ve sınıflandırma

- **Yazarlar / yıl:** Rogerio R. L. Cisi, André F. Kohn — 2008
- **Başlık:** Simulation system of spinal cord motor nuclei and associated nerves and muscles, in a Web-based architecture
- **Dergi / cilt / sayfa:** Journal of Computational Neuroscience, 25, 520–542
- **DOI / PMC:** DOI 10.1007/s10827-008-0092-8
- **PDF:** `pdf/Simulation_system_of_spinal_cord_motor_nuclei_and_associated_nerves_and_muscles__in_a_Web-based_architecture.pdf` (repoya girmez)
- **Özeti çıkaran / tarih:** Claude (Deniz'in isteğiyle) / 06.09.2026

- **Makale tipi:** bilgisayar modeli + yöntem/araç (simülatör tanıtımı; içinde küçük bir doğrulama deneyi var)
- **Projemizin hangi tarafına bakıyor:** nöron (motonöron havuzu + internöron ağı) ve köprü (motonöron çıkışı → kas kuvveti/EMG)
- **Bizim için değeri:** yöntem örneği (birincil) · model yapısı kararı için referans · sınırlı parametre kaynağı (kedi/insan verisi, doğrudan aktarılamaz)

## 2 · Makalenin sorusu ve ana iddiası

Yazarlar, insan omuriliğinin kas kontrolünden sorumlu devresini (motonöron havuzları, internöronlar, duyusal afferentler, inen yollar) web üzerinden çalıştırılabilir tek bir simülatörde toplamak istemiş. Simülatörün adı ReMoto'dur ve http://remoto.leb.usp.br adresinde açık kaynak olarak sunulmuştur. Ana iddia şudur: iki bölmeli basitleştirilmiş nöron modelleriyle kurulan bu ağ, hem tek nöron düzeyindeki özellikleri (AHP, f×I ilişkisi, ateşleme adaptasyonu) hem de ağ düzeyindeki insan elektrofizyolojisi bulgularını (size-principle alımı, H-refleksi ve depresyonu, kuvvet üretimi, EMG) yeniden üretebilir. Simülatör, insanda ölçülemeyen büyüklüklere (havuzdaki bütün motonöronların ateşleme zamanları gibi) erişim sağlar.

---

## 3 · NEYİ NASIL YAPMIŞ (yöntem)

### 3a · Denek / malzeme / model

- Model tipi: iki bölmeli (soma + dendrit) integrate-and-fire motonöron modeli; internöronlar tek bölmeli. Bölme geometrisi silindirik.
- Nöron tipleri: motonöronlar S, FR, FF olarak ayrılmış (Burke ve ark. 1973 sınıflaması). İnternöronlar: Renshaw hücresi (RC), Ia inhibitör internöron (IaIn), Ib inhibitör internöron (IbIn).
- Varsayılan devre: ayak bileği fleksiyon/ekstansiyonu — SOL, MG, LG (ekstansör) ve TA (fleksör) kasları.
- Ölçek: 2.000'den fazla nöron ve 2.000.000 sinaps eklenebilir (Abstract). Örnek büyük simülasyon: 6.054 nöron, yaklaşık 2.400.000 sinaps (Bölüm 3.7, s. 537).
- Yazılım: Java, web tabanlı (Tomcat + Struts + HSQLDB + JFreeChart); Model-View-Control mimarisi; paralel thread'ler (Bölüm 2.1, s. 524).
- Entegrasyon: 4. derece Runge–Kutta, varsayılan adım 0,05 ms (Bölüm 2.1, s. 523).
- Parametre kökeni: akson parametreleri hariç bütün nöron parametreleri kedi verisinden alınmış ve insana benzer varsayılmış (Jankowska ve Hammar 2002'ye dayanarak; Bölüm 2.2, s. 524).
- Nöron sayıları insan+kedi literatüründen derlenmiş tahminlerdir; internöron sayıları performans için bilinçli olarak düşük tutulmuş, sinaptik parametreler bunu telafi edecek şekilde ayarlanmıştır (Bölüm 2, s. 522 ve Tartışma, s. 538).

### 3b · Yöntem adımları

1. Yazarlar nöron sayılarını Tablo 1'deki varsayılanlarla kurmuş (aşağıda 3d'de).
2. Yazarlar motonöronları omurilik boyunca gerçek kolonları taklit eden çizgisel kolonlara yerleştirmiş: her çekirdekte MN'ler boyuta göre (S < FR < FF) kaudalden rostrale sıralı ve eşit aralıklı. SOL 18,0 mm'lik kolon; MG aynı orijinden 10,0 mm (SOL ile örtüşür); LG 10,0–18,0 mm arası; TA ayrı kolonda 7,5 mm (Bölüm 2, s. 522). Dayanak: MG çekirdeği 6–7 mm'ye yayılmış en çok 300 MN → 50 MN/mm yoğunluk (Burke ve ark. 1977).
3. Yazarlar RC, IaIn ve IbIn gruplarını ekstansör ve fleksör çekirdeklerin MN'leri arasına eşit dağıtmış.
4. Membran dinamiği: soma bölmesinde Cs ile paralel gls (kaçak), gKs + gKf (potasyum) ve gNa (sodyum) iletkenlikleri; dendritte Cd + gld; iki bölmeyi gc bağlıyor (Denklem 1–8, s. 525). Voltaja bağlı hız sabitleri Destexhe (1997) darbe tabanlı modeliyle basitleştirilmiş: eşik aşıldığında 0,6 ms süren dikdörtgen darbeler α/β hızlarını değiştiriyor; AHP, yavaş potasyum iletkenliği (q² terimli gKs) ile üretiliyor (s. 525–526).
5. Akson yapısal olarak değil işlevsel olarak modellenmiş: eşik üstü uyarımda spike üreten bir algoritma; somatik/aksonal spike'lar iletim hızıyla orantılı gecikmeyle hedefe ulaşıyor. Antidromik spike ortodromik spike ile çarpışıp yok olabiliyor; çarpışma yoksa antidromik spike RC'leri uyarıyor ve gecikmeyle somada spike doğuruyor (s. 526–527).
6. Sinaps: iletkenlik değişimi olarak; iki durumlu Markov modeli (Destexhe ve ark. 1994a), gsyn(t) = gmax·r(t); hesap Lytton (1996) algoritmasıyla hızlandırılmış (Bölüm 2.2.3, s. 527).
7. Sinaptik depresyon: her presinaptik spike'ta salınabilir nörotransmitter deposu s(t), p oranı kadar azalıyor ve τ zaman sabitiyle üstel toparlanıyor (Kohn ve ark. 1995; Abbott ve ark. 1997). Değerler 3d'de (s. 527–528).
8. RC bağlantı ağırlığı mesafeyle azalıyor: weight = a / (a + d²); d = RC–MN rostro-kaudal mesafesi (Denklem 10, s. 528).
9. Sinaptik gürültü: her MN'ye bağımsız Poisson süreçleriyle sürülen eksitatör/inhibitör iletkenlikler (s. 528).
10. Motor ünite twitch'i: kritik sönümlü 2. derece sistemin impuls yanıtı (Fuglevand ve ark. 1993; Denklem 11–13); "impulse invariance" tekniğiyle ayrık zamanda fark denklemi olarak çözülmüş (Denklem 14–17, s. 528–529). Tetanik kuvvette sert (hard) doyum uygulanmış.
11. MUAP: 1. ve 2. derece Hermite–Rodriguez fonksiyonları (bifazik/trifazik; her MU %50 olasılıkla HR1 veya HR2); yüzey bipolar elektrot varsayımı: 8 mm çap, 20 mm ayrım (Denklem 18–19, s. 529).
12. EMG: MUAP genliği mesafeyle üstel zayıflıyor (Denklem 20), süresi mesafeyle uzuyor (Denklem 21); bant geçiren dijital filtre var (s. 529–530).
13. Duyusal afferentler (Ia, Ib) sinir uyarımına spike ile yanıt veriyor; projeksiyon oranı %0–100 arası seçilebiliyor ve hedef havuzdan rastgele seçim yapılıyor (Bölüm 2.2.5, s. 530).
14. İnen yollar: her akson bağımsız spike üreteci; ISI dağılımı Poisson veya kesik Gauss; ortalama ISI darbe/rampa/sinüs/kare sinyalle modüle edilebiliyor (Bölüm 2.2.6, s. 530).
15. Ayar/doğrulama iki aşamalı: önce tek nöron özellikleri (Zengel ve ark. 1985 membran özellikleri, f×I), sonra ağ bütünü insan verisine (kuvvet, EMG, ISI dağılımları, H-refleks) göre ad-hoc ayarlanmış (Bölüm 2.3, s. 530–531).

### 3c · Tanım ve birim uyarıları

- **Membran potansiyeli referansı dinlenim = 0 mV.** Bütün potansiyeller dinlenim gerilimine göre verilmiş: ENa = +120 mV, EK = −10 mV, El = 0 mV; sinaps tersinme potansiyelleri eksitatör +70 mV, inhibitör −16 mV (s. 525, 527). Bizim NEURON kurulumumuz mutlak mV kullanır (dinlenim ≈ −70 mV civarı); bu makaleden değer taşınırsa ~70 mV kaydırma yapılmadan taşınan her değer yanlış olur.
- İletkenlikler birim alana değil bölme geometrisine göre hesaplanıyor (Denklem 5–6: gld = 2π·r·l / Rm); spesifik direnç (kΩ.cm²) ile hücre başına iletkenlik (µS) karıştırılmamalı.
- Kuvvet birimi gram-force (gf); makaledeki laboratuvar deneyi ise tork (Nm) ölçmüş — Şekil 9 ve 10'un ordinatları farklı büyüklüklerdir, doğrudan karşılaştırılamaz (s. 534).
- "pps" = pulses/s = spikes/s (s. 527).
- MN spike zamanları iki farklı referansla kaydedilebiliyor: kas son plağına varış anı veya somada üretim anı (s. 536). Karşılaştırma yapılacaksa hangi referansın kullanıldığı kontrol edilmeli.
- Rheobase somaya akım enjeksiyonuyla tanımlı; akson eşiği ise sinire dış elektrik uyarımının eşiği (mA) — ikisi ayrı parametrelerdir (Tablo 2).

### 3d · Kullanılan parametreler ve değerleri

Varsayılan nöron sayıları (Tablo 1, s. 522):

| Parametre | Değer | Birim | Nereden (tablo/şekil/sayfa) |
|---|---|---|---|
| MN S — SOL / MG / LG / TA | 800 / 250 / 200 / 250 | adet | Tablo 1, s. 522 |
| MN FR — SOL / MG / LG / TA | 50 / 125 / 100 / 50 | adet | Tablo 1, s. 522 |
| MN FF — SOL / MG / LG / TA | 50 / 125 / 100 / 50 | adet | Tablo 1, s. 522 |
| Ia afferent — SOL / MG / LG / TA | 400 / 80 / 76 / 280 | adet | Tablo 1, s. 522 |
| Ib afferent — SOL / MG / LG / TA | 200 / 40 / 38 / 140 | adet | Tablo 1, s. 522 |
| RC / IaIn / IbIn (ekstansör grubu ve fleksör grubu, her biri) | 350 | adet | Tablo 1, s. 522 |

Motonöron parametre aralıkları, tip içinde MN indeksine göre doğrusal interpolasyonla dağıtılıyor (Tablo 2, s. 526; aralıklar min–maks):

| Parametre | Değer (S / FR / FF) | Birim | Nereden |
|---|---|---|---|
| Rheobase akımı | 3,5–6,5 / 6,5–17,5 / 17,5–25,1 | nA | Tablo 2, s. 526 |
| Soma çapı | 77,5–82,5 / 82,5–87,5 / 87,5–113 | µm | Tablo 2, s. 526 |
| Soma boyu | 77,5–82,5 / 82,5–87,5 / 87,5–113 | µm | Tablo 2, s. 526 |
| Soma spesifik direnci | 1,15–1,05 / 1,05–0,95 / 0,95–0,65 | kΩ.cm² | Tablo 2, s. 526 |
| Dendrit çapı | 41,5–62,5 / 62,5–83,5 / 83,5–92,5 | µm | Tablo 2, s. 526 |
| Dendrit boyu | 5,5–6,8 / 6,8–8,1 / 8,1–10,6 | mm | Tablo 2, s. 526 |
| Dendrit spesifik direnci | 14,4–10,7 / 10,7–6,95 / 6,95–6,05 | kΩ.cm² | Tablo 2, s. 526 |
| Akson eşiği (sinir uyarımı) | 18,0–12,4 / 12,4–12,2 / 12,2–12,0 | mA | Tablo 2, s. 526 |
| Akson iletim hızı | 44,0–47,0 / 47,0–50,0 / 50,0–53,0 | m/s | Tablo 2, s. 526 |

Diğer hücre ve sinaps parametreleri:

| Parametre | Değer | Birim | Nereden |
|---|---|---|---|
| Membran spesifik kapasitansı (Cm) | 1,0 | µF/cm² | s. 526 (Barret ve Crill 1974; Fleshman ve ark. 1988) |
| Sitoplazma özdirenci (Ri) | 70,0 | Ω.cm | s. 526 |
| AHP hız sabitleri (varsayılan) | αQ = 1,5; βQ = 0,025 | ms⁻¹ | s. 526 |
| Darbe (pulse) süresi — hız sabitleri | 0,6 | ms | s. 526 |
| MN mutlak refrakter periyodu | 5,0 (→ maks 200 pps) | ms | s. 527 (Powers 1993) |
| Esyn eksitatör / inhibitör | 70 / −16 | mV (dinlenim = 0 referanslı) | s. 527 |
| Depresyon Ia→MN: p / τ | 0,11 / 1.500 | — / ms | s. 528 |
| Depresyon MN→RC: p / τ | 0,50 / 200 | — / ms | s. 528 |
| RC→MN ağırlık: a (mesafe zayıflaması) | 0,22 (1,4 mm'de gücün %10'u) | — (d: mm) | Denklem 10, s. 528 |
| MN→RC ağırlık: a | 0,01 (kollateral yayılımı ≤ 1 mm) | — (d: mm) | s. 528 |
| Twitch kuvveti (S / FR / FF) | 10,5–12,5 / 12,5–30,0 / 30,0–50,0 | gf | Tablo 3, s. 529 |
| Tetanik kuvvet (S / FR / FF) | 40,0–50,0 / 50,0–120,0 / 120,0–200,0 | gf | Tablo 3, s. 529 |
| Kontraksiyon süresi (S / FR / FF) | 110–100 / 73,5–55,5 / 82,3–56,9 | ms | Tablo 3, s. 529 |
| MUAP AM parametresi (S / FR / FF) | 0,105–0,125 / 0,125–0,30 / 0,30–0,50 | µV | Tablo 3, s. 529 |
| MUAP λM parametresi (S / FR / FF) | 0,80–0,70 / 0,70–0,60 / 0,60–0,50 | ms | Tablo 3, s. 529 (metinle çelişiyor; bkz. Bölüm 9) |
| EMG genlik zayıflama sabiti τat | 5,0 | mm⁻¹ (makalede böyle basılmış; bkz. Bölüm 9) | s. 530 |
| MUAP süre genişleme sabiti C | 0,1 | mm⁻¹ | s. 530 |
| Kas kesit çapı SOL / MG / LG / TA | 18,4 / 17,0 / 18,8 / 18,8 | mm | s. 530 (Maganaris ve ark. 1998) |
| Ia afferent iletim hızı / akson eşiği | 69,0–65,0 / 6,0–18,0 | m/s / mA | Tablo 4, s. 530 |
| Ib afferent iletim hızı / akson eşiği | 66,0–62,0 / 13,0–22,0 | m/s / mA | Tablo 4, s. 530 |
| Motor akson boyu (varsayılan) | 0,8 | m | s. 527 |
| PTN: uyarım noktası → omurilik / son plak | 0,6 / 0,2 | m | s. 527 |
| CPN: uyarım noktası → omurilik / son plak | 0,66 / 0,14 | m | s. 527 |
| Sinir uyarım darbe süresi | 1,0 (tek seçenek) | ms | Tablo 4 üstü metin, s. 530 |

İnternöron elektrotonik özellikleri Bui ve ark. (2003) verisinden tek bölmeye uyarlanmış; IbIn ≈ IaIn varsayılmış; RC parametreleri burst atacak şekilde ayarlanmış (s. 526–527). Sayısal değerleri makalede değil, simülatörün "V-d conductances" panelinde (özet buraya alınamadı; bkz. Bölüm 8).

---

## 4 · NE SONUÇ BULMUŞ

### 4a · Sayısal sonuçlar

| Büyüklük | Değer | Birim | Nereden | Saçılım (SD/SEM/aralık, n) |
|---|---|---|---|---|
| Model MN giriş direnci (S / FR / FF) | 1,6 / 0,9 / 0,6 | MΩ | Tablo 5, s. 531 | literatür aralığı: 1,6–0,9–0,6 |
| Model MN membran zaman sabiti | 10,4 / 8,0 / 5,9 | ms | Tablo 5, s. 531 | literatür: 10,4–8,0–5,9 |
| Model AHP genliği | 4,9 / 4,3 / 3,0 | mV | Tablo 5, s. 531 | literatür: 4,9–4,3–3,0 |
| Model AHP süresi | 160 / 87 / 67 | ms | Tablo 5, s. 531 | literatür: 161–78–65 |
| f×I eğimi, 1. segment | 2,7 / 2,5 / 3,6 | pps/nA | Tablo 5, s. 531 | literatür: 1–3 |
| f×I eğimi, 2. segment | 6,3 / 3,8 / 4,9 | pps/nA | Tablo 5, s. 531 | literatür: 3–8 |
| RC burst yanıtı (PTN eşik üstü uyarım) | 10 spike + sonradan 2 spike | adet | Şekil 5, s. 532 | tek örnek simülasyon |
| Rampa inen sürüşte kuvvet düzeyi (1.000 ms'de) | ~%50 MVC | — | Şekil 7 metni, s. 532 | — |
| 100 S'li havuzda MN 50 time-to-peak (aralık 100–110 ms iken) | 105 | ms | s. 533 | — |
| Twitch half-relaxation süresi | ~170 | ms | s. 533 | insan verisinden büyük görünüyor (yazarların notu) |
| F×f eğrisi (S MN, 2–40 Hz) | doğrusal; 40 gf'te doyum; eğim %7,9/Hz | — | s. 533 | insan ayak parmağı ekstansörleri ve kedi MG aralığında |
| ISI — TA MN 1 (Poisson 300 pps, 100 akson) | ortalama 53,79; SD 4,63; CV 0,086; çarpıklık 0,232 | ms | Şekil 12a metni, s. 535 | — |
| ISI — TA MN 91 | ortalama 75,27; SD 15,41; CV 0,205; çarpıklık 1,201 | ms | Şekil 12b metni, s. 535 | — |
| H-refleks deneyi: uyarım genliği | 14,0 | mA | Şekil 13 metni, s. 535 | — |
| M dalgası / H yanıtı gecikmesi | ~5 / ~29 | ms | s. 536 | — |
| H-refleks / M dalgası alım eğrileri uyarım aralığı | 10–20 | mA | Şekil 14, s. 536 | deneysel aralık içinde (Floeter ve Kohn 1997) |
| H-refleks depresyonu protokolü | 1 Hz, 10 darbe; genlik platoya düşüyor | — | Şekil 15, s. 536–537 | deneysel aralık içinde |
| Performans: 10 s H-depresyon simülasyonu | 8,9 | dk | Bölüm 3.7, s. 536 | 2× Xeon 3,0 GHz dual core sunucu |
| Performans: 1 s, tüm çekirdekler (6.054 nöron, ~2.400.000 sinaps) | 13,1 | dk | Bölüm 3.7, s. 537 | — |

### 4b · Niteliksel bulgular

- **Ateşleme adaptasyonu kısa:** her üç MN tipinde adaptasyon "ilk bir-iki interspike aralığından sonra pratikte bitiyor" (Şekil 6, s. 532). Yazarlar bunun gerçek MN'lerdeki daha karmaşık geç adaptasyon fazlarını temsil etmediğini açıkça söylüyor.
- **Size-principle alımı kendiliğinden çıkıyor:** rampa inen sürüşte hem yeni ünite alımı (küçükten büyüğe) hem hız artışı görülüyor; sinaptik gürültü yüzünden alım sırasında yerel değişimler olabiliyor (Şekil 7–8, s. 532–533).
- **Küçük MN daha hızlı ateşliyor:** aynı sürüşte küçük MN'nin ortalama hızı büyük MN'ninkinden yüksek (Şekil 7).
- **Hızlı ateşleyen MN'de ISI CV'si düşük:** aynı MN iki farklı sürüş şiddetiyle simüle edilince de bulunmuş (s. 535). ISI histogramı hızlı ateşlemede Gauss benzeri, yavaşta sağa çarpık.
- **Twitch interpolasyonu simülasyonu, laboratuvardaki insan deneyiyle (36 yaşında erkek denek, pedal-tork ölçer, popliteal fossa'ya 100 µs darbe) genel davranış olarak uyumlu** (Şekil 9–10, s. 534). Yazarlar bunun simülatörün nörofizyolojik deney sonuçlarını öngörebileceğini düşündürdüğünü söylüyor.
- **Deterministik durumda minimum ateşleme hızı MN boyutuyla artıyor** (Bölüm 3'te gösterilmemiş; Tartışma, s. 538'de belirtiliyor).
- **MU senkronizasyonu algoritmik değil, doğal olarak kurulabiliyor:** inen sürüşün bağlantı diverjansı seçilerek (Tartışma, s. 538).

### 4c · Yazarların kendi çıkardığı sonuç

Simülatör, tek nöron düzeyinde ve ağ düzeyinde insan elektrofizyolojisiyle uyumlu davranışlar üretmektedir; en kritik ayar parametreleri voltaja bağlı iletkenliklerdir. Hücresel parametrelerin çoğu insan verisi olmadığı için kediden alınmıştır ve devre parametreleri insan verisini üretecek şekilde ayarlanmıştır. Yazarların saydığı sınırlılıklar: kısa adaptasyon, dendritik PIC (persistent inward current) yokluğu (L-tipi Ca kanalı gelecekte eklenmeli), doğrusal F×f, sert tetanik doyum, izometrik kuvvet, kas iğciği ve Golgi tendon organı modellerinin yokluğu (Tartışma, s. 537–539).

---

## 5 · Projemize ilgisi

- **Doğrudan kullanılabilir mi?** Kısmen. Sayısal parametreler doğrudan aktarılamaz (kedi→insan karışımı; bizim hedef Sprague-Dawley sıçanı). Ama mimari doğrudan örnek: motonöron havuzu → MU twitch toplamı → kas kuvveti köprüsü, bizim "motonöron çıkışı → kas aktivasyonu u(t)" köprümüzün basitleştirilmiş bir emsalidir.
- **Hangi büyüklüğümüz veya parametremizle eşleşir?** (1) Motonöron havuzu yapısı (S/FR/FF ayrımı, indeksle interpolasyon, size-principle); (2) RC/IaIn/IbIn internöron katmanı; (3) Ia→MN sinaptik depresyonu (p, τ formülasyonu); (4) RC bağlantısının mesafeye bağlı ağırlığı (Denklem 10) — bizim NEURON ağımızda kolon geometrisi kurulursa aynı formül adaydır.
- **Bilinen sistematik fark:** tür (kedi parametreleri + insan kasları ↔ bizim sıçan); kaslar (ayak bileği insan kasları ↔ sıçan arka bacak); kuvvet izometrik ve tek eklem ↔ bizim OpenSim çok eklemli dinamik; potansiyel referansı (dinlenim = 0 mV ↔ NEURON mutlak mV); nöron modeli integrate-and-fire ↔ bizim NEURON iletkenlik tabanlı model.
- **Nereye girdi olacak:** model yapısı kararı (havuz mimarisi, depresyon formülasyonu, RC ağırlık şeması) + yöntem örneği (ağ düzeyinde doğrulama stratejisi: önce tek hücre, sonra ağ). Parametre seçimi için ancak dolaylı: makalenin işaret ettiği birincil kaynaklar (Zengel 1985, Fleshman 1988, Fuglevand 1993, Destexhe 1994/1997) üzerinden gidilmeli.

## 6 · Bizimle çelişen veya işimize gelmeyen bulgular

- **PIC yok.** Bizim motonöron modelimizin merkezinde PIC/Cav1.3 var; bu simülatör PIC içermiyor ve yazarlar L-tipi Ca kanalını yalnızca "gelecek iş" olarak öneriyor (s. 537). Yani bu makale, PIC'li modelimize doğrulama desteği vermez; PIC'siz bir modelin de insan ağ davranışının önemli kısmını üretebildiğini gösterir — PIC eklemenin ağ düzeyinde ne kattığını ayrıca gerekçelendirmemiz gerekir.
- **Kapalı döngünün duyusal bacağı yok.** Kas iğciği ve GTO modelleri yok; Ia/Ib ateşlemesi yalnızca dış elektrik uyarımıyla üretiliyor. Bizim r(t) → Ia geri beslememiz için bu simülatör emsal değildir.
- **Kuvvet tarafı bilinçli olarak basit:** doğrusal F×f (gerçekte sigmoidal), sert doyum, izometrik, "catch" ve "sag" özellikleri yok (s. 538). Bizim Hill tipi OpenSim kas modelimizle karşılaştırıldığında bu simülatörün kas çıktısı doğrulama referansı olamaz.
- **Half-relaxation ~170 ms, insan verisinden büyük** — twitch modelinin bozunumu yavaş (s. 533). Aynı 2. derece twitch formülasyonunu alırsak aynı sapmayı miras alırız.
- **Adaptasyon eksik temsil ediliyor** (yalnızca erken faz; s. 537): uzun süreli lokomosyon simülasyonlarında geç adaptasyonun yokluğu ateşleme hızlarını olduğundan yüksek tutabilir.

## 7 · Testlere girecek değerler (varsa)

Bu makaleden doğrudan test çıkmıyor. Gerekçe: makalenin doğrulama hedefi insan elektrofizyolojisidir, model parametreleri kediden gelir; bizim referans türümüz sıçandır. Motonöron membran özellikleri (Rin, τm, AHP) test yapılacaksa birincil kaynak bu makale değil, makalenin kullandığı Zengel ve ark. (1985) olmalıdır — o da kedidir ve tür farkı gerekçelendirilmelidir.

## 8 · Özete alınmayanlar

- Simülatörün internöron ve iletkenlik varsayılan değerleri: makale bunları yazmıyor, çevrimiçi "V-d conductances" paneline yönlendiriyor (s. 526–527). Sayı gerekirse simülatörün kendisine veya kaynak koduna gidilmeli.
- Denklem 11–21'in tam biçimleri ve türetmeleri (twitch ayrıklaştırması, HR fonksiyonları, EMG zayıflama) — özet yalnız yapıyı verdi.
- Yazılım mimarisi ayrıntıları (JDBC, JSP, servlet katmanları; Şekil 2 konfigürasyon ekranı).
- Tartışmadaki diğer simülatörlerle karşılaştırma paragrafları (Bashor 1998, Subramanian 2005, Stienen 2007, Uchiyama ve Windhorst 2007) — bizim için ikincil literatür haritası; gerekirse s. 521 ve 537–539.
- Şekil 4, 6, 8, 9, 11'in ham eğrileri.

## 9 · Açık sorular / doğrulanmayanlar

- **λM iç çelişkisi:** Tablo 3 λM'yi 0,50–0,80 ms aralığında veriyor; metin ise "MUAP time factor (λM) 5–40 ms arasında seçildi" diyor (ikisi de s. 529). Hangisinin geçerli olduğu makaleden çıkarılamıyor; λM kullanılacaksa simülatör kaynak kodundan doğrulanmalı.
- **τat birimi:** zayıflama formülü V = V0·exp(−d/τat) mesafe boyutunda bir sabit gerektirir; makale "τat was set at 5.0 mm⁻¹" yazıyor (s. 530). Varsayım: kastedilen 5,0 mm'dir ve birim baskı hatasıdır; doğrulanmadı.
- **AHP süresi FR/FF sapması:** model 87/67 ms, referans 78/65 ms (Tablo 5). Yazarlar yorum yapmıyor; uyum iddiası S tipi kadar sıkı değil.
- İnternöron parametrelerinin "burst atacak / tek spike atacak şekilde" ad-hoc ayarlandığı açık; hangi değerlerin biyofiziksel, hangilerinin uydurma olduğu makaleden ayrıştırılamıyor.
