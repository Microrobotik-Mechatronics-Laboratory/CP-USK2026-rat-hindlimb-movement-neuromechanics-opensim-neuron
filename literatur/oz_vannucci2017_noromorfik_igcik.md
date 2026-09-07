# Literatür özeti — Vannucci 2017 (spike tabanlı kas iğciği modeli)

> Bu dosya makalenin **seçici özetidir** — yerine geçmez. Amacı, makaleyi tekrar
> açmadan modelleme kararı verebilmektir.

## 1 · Künye ve sınıflandırma

- **Yazarlar / yıl:** Lorenzo Vannucci, Egidio Falotico, Cecilia Laschi / 2017 (kabul: 30 Mayıs 2017; yayın: 14 Haziran 2017)
- **Başlık:** Proprioceptive Feedback through a Neuromorphic Muscle Spindle Model
- **Dergi / cilt / sayfa:** Frontiers in Neuroscience, cilt 11, makale 341
- **DOI / PMC:** 10.3389/fnins.2017.00341
- **PDF:** `pdf/Proprioceptive_Feedback_through_a_Neuromorphic_Muscle_Spindle_Model.pdf` (repoya girmez)
- **Özeti çıkaran / tarih:** Claude / 2026-09-06

- **Makale tipi:** yöntem/araç (model uyarlaması + iki platformda implementasyon + robotik gösterimler)
- **Projemizin hangi tarafına bakıyor:** nöron tarafı sınırında duyu köprüsü (kas iğciği Ia/II afferent modeli — bizim r(t) → Ia sinapsı hattımız)
- **Bizim için değeri:** yöntem örneği (Mileusnic modelini spike tabanlı hale getirme ve sadeleştirme) + doğrulama referansı (uzatma protokolü ve beklenen davranışlar); parametrelerin asıl kaynağı Mileusnic 2006'dır

## 2 · Makalenin sorusu ve ana iddiası
Makale, proprioseptif bilgiyi (kas uzunluğu ve uzama hızı) biyolojik olarak gerçekçi spike aktivitesine çeviren, tamamen spike tabanlı bir kas iğciği modelinin kurulup kurulamayacağını sorar. Yazarlar, Mileusnic 2006 iğcik modelini (bag1, bag2, chain intrafusal lifleri; fusimotor modülasyon; Ia ve II afferentleri) spike girdi/çıktıyla çalışacak biçimde uyarlar, NEST simülatöründe ve SpiNNaker nöromorfik donanımında gerçekler. İddia: model, hem simüle hem fiziksel robotlarda enkoder değerlerini biyolojik olarak makul afferent spike aktivitesine gerçek zamanlıya varan hızlarda çevirebilir ve kapalı duyu-motor döngüleri için bir yapı taşı sunar (Abstract; Bölüm 4).

---

## 3 · NEYİ NASIL YAPMIŞ (yöntem)

### 3a · Denek / malzeme / model
Deneysel denek yoktur; çalışma model uyarlaması + implementasyon + robotik gösterimdir.

- **Taban model:** Mileusnic et al. 2006. Üç intrafusal lif tipi (bag1, bag2, chain) aynı fonksiyon biçimiyle, lif tipine göre farklı parametrelerle modellenir. Girdiler: fascicle uzunluğu L (ve türevleri) + fusimotor aktivasyon düzeyi (f_dynamic, f_static). Her lif, sensory bölge (saf elastik) + polar bölge (yay + paralel kasılabilir eleman) olarak modellenir; lif gerilimi T diferansiyel denklemle hesaplanır (Bölüm 2.1).
- **Afferent birleşimi:** rate_II = rate_bag2 + rate_chain (Eş. 3); rate_Ia, bag1 ile II aktivitesinin S ağırlıklı toplamıdır ve kısmi occlusion etkisini modeller (Eş. 4). Gamma dynamic yalnız bag1'i, gamma static bag2 + chain'i etkiler (Bölüm 2.1; Şekil 1).
- **Parametre değerleri bu makalede verilmez;** Mileusnic 2006 Tablo 1'e gönderilir ve kedi soleus kayıtlarına optimize edilmiş oldukları belirtilir (Bölüm 2.1; Bölüm 3).
- **Platformlar:** NEST (nokta-nöron spiking simülatörü; yeni nöron modeli olarak eklenmiş) ve SpiNNaker SpiNN-5 kartı (48 çip × 18 çekirdek; sabit noktalı aritmetik; C ile geliştirilmiş, PyNN arayüzünden çağrılır) (Bölüm 2.3). Referans: MATLAB Simulink implementasyonu (Bölüm 3.1).

### 3b · Yöntem adımları
1. **Sadeleştirme:** L̈ = 0 alınır; gerekçe, ivme bilgisinin gürültülü/erişilemez olduğu gömülü uygulamalarda çift integralin kararsızlığıdır. Etki ölçülür: orijinal modelin Simulink implementasyonunda, ivmeli ve ivmesiz afferent hızlar arasındaki ortalama fark çoğu durumda %1'in altındadır. Gerilim denklemi birinci derece ODE'ye indirgenir (Eş. 8); girdiler yalnız L, L̇, f_dynamic, f_static olur (Bölüm 2.1).
2. **Fusimotor girdinin spike'laştırılması:** orijinal modeldeki Hill tipi denklem + alçak geçiren filtre (anlık gamma-MN ateşleme hızı ister) yerine spike integrasyonu konur: her gelen spike anlık yanıt + üstel sönümle eklenir, aktivasyon f [0, 1] aralığında tutulur (Eş. 10–11).
3. **Parametre kimliklendirme:** r (maksimum impuls yanıtı) ve τ (sönüm süresi), {10, 50, 75, 100, 150} spike/s'lik sabit gamma sürüşleriyle üretilmiş referans maksimum aktivasyon veri setine karşı taranır (0.01 ≤ r ≤ 0.4; 100 ms ≤ τ ≤ 500 ms). Hata ölçüsü: magnitude error (maksimum düzey farkı) + shape error (%90'a ulaşma anındaki fark; referans: f_dynamic 343 ms'de, f_static 471 ms'de %90'a ulaşır — Mileusnic 2006'dan). Seçilen değerler ortalama %7 hata verir (Bölüm 2.2).
4. **Çıktının spike'laştırılması:** Ia ve II hızlarından Poisson süreciyle spike üretilir; SpiNNaker'da P{spike, δt} = rate·δt yaklaşıklığı kullanılır (δt = 1 ms) (Bölüm 2.3).
5. **Doğrulama:** üç implementasyon (Simulink referans, NEST, SpiNNaker) aynı uzatma görevini koşar: L = 0.95·L0 sabit 1.1 s → 0.11·L0/s hızla uzatma 1.1 s → L = 1.08·L0 sabit 1.1 s. Üç fusimotor koşul: sürüş yok; gamma_dynamic = 70 spike/s; gamma_static = 70 spike/s. Spike hızı 30 ms'lik kutularla hesaplanır. NEST'te 200 iğcik (400 düğüm), SpiNNaker'da 100 iğcik (200 düğüm; çekirdek başına bellek sınırı) (Bölüm 3.1).
6. **Gösterimler:** (a) Neurorobotics Platform'da simüle iCub dirseği — agonist/antagonist kas çifti geometrik kas uzunluğu denklemleriyle (Eş. 13–16), sinüzoidal hareket 45° tepe-tepe, 0.2 Hz, 125° merkezli, gamma_dynamic = 70 spike/s; (b) simüle fare boynu — üç-link zincir (Eş. 17–20), Braitenberg tipi Y-maze ekran deneyi, ekranlar 6 s'de bir değişir, gamma_dynamic = 70 spike/s; (c) fiziksel iCub neck roll eklemi — SpiNNaker'a canlı enkoder aktarımı için C++ middleware; sinüzoidal 30° tepe-tepe, 0.5 Hz, her uçta 1 s bekleme (periyot 4 s); gamma_dynamic = 80, gamma_static = 40 spike/s; eklem hızı tek adımlı sayısal türevle üretilir (Bölüm 3.2).

### 3c · Tanım ve birim uyarıları
- **Uzunluk birimi L0'dır:** L ve L̇, dinlenme fascicle uzunluğu L0 cinsinden normalize verilir (Bölüm 2.1 sonu). Bizim OpenSim tarafımız metre kullanır; iğcik modeline girerken normalize etme adımı atlanamaz.
- **f (aktivasyon, 0–1) ile gamma (spike/s) farklı büyüklüklerdir:** gamma-MN ateşleme hızı, spike integrasyonuyla f'ye çevrilir; ikisini karıştırmak modeli yanlış sürer (Bölüm 2.2).
- **"Rate" çıktısı Poisson üretiminden ÖNCEKİ deterministik hızdır;** kaydedilen spike train'lerden hız, 30 ms kutulamayla geri hesaplanır — kutulama genişliği değişirse eğriler değişir (Bölüm 3.1).
- **Chain lifinin static aktivasyonu bag2'ninkinin 0.829 katıdır** (ortalama ölçek faktörü); orijinal modelde chain doygunluk fonksiyonuyla farklı hesaplanır — iki tanım aynı değildir (Bölüm 2.2).
- **NEST'te bir iğcik = iki model örneği:** NEST nöronunun tek çıkış kanalı olduğundan Ia ve II ayrı birimlerle (Boolean bayrak) simüle edilir; n iğcik için 2n birim kurulur (Bölüm 2.3).

### 3d · Kullanılan parametreler ve değerleri

| Parametre | Değer | Birim | Nereden |
|---|---|---|---|
| r_dynamic / τ_dynamic | 0.08 / 310 | — / ms | Bölüm 2.2 |
| r_static / τ_static | 0.09 / 425 | — / ms | Bölüm 2.2 |
| Chain static aktivasyon ölçeği (bag2'ye göre) | 0.829 | — | Bölüm 2.2 |
| Parametre kimliklendirme ortalama hatası | 7 | % | Bölüm 2.2 |
| Spike integrasyonunun doğru çalıştığı gamma aralığı | 30 – 150 | spike/s | Bölüm 2.2 |
| f_dynamic / f_static %90'a ulaşma süresi (referans) | 343 / 471 | ms | Bölüm 2.2 (Mileusnic 2006'dan) |
| L̈ = 0 sadeleştirmesinin etkisi | < 1 (çoğu durumda) | % ort. fark | Bölüm 2.1 |
| Doğrulama uzatma protokolü | 0.95·L0 (1.1 s) → 0.11·L0/s (1.1 s) → 1.08·L0 (1.1 s) | — | Bölüm 3.1 |
| Doğrulama fusimotor koşulları | yok; gamma_dyn = 70; gamma_stat = 70 | spike/s | Bölüm 3.1 |
| Hız kutulaması | 30 | ms | Bölüm 3.1 |
| SpiNNaker simülasyon adımı δt | 1 | ms | Bölüm 2.3 |
| Lif parametreleri (KSR, KPR, C, R, a, S, X, β, Γ...) | bu makalede yok | — | Mileusnic 2006, Tablo 1'e gönderme (Bölüm 2.1) |

---

## 4 · NE SONUÇ BULMUŞ

### 4a · Sayısal sonuçlar

| Büyüklük | Değer | Birim | Nereden | Saçılım (SD/SEM/aralık, n) |
|---|---|---|---|---|
| NEST doğrulama görevi ortalama simülasyon süresi / gerçek zaman faktörü | 7.51 / 0.44 | s / — | Bölüm 3.1 | i7-2760QM |
| NEST sürekli koşu: 100 Ia afferenti, 1 s | 0.48 | s | Bölüm 3.1 | karşılaştırma: 100 LIF 0.06 s; 100 adaptif LIF 0.81 s |
| SpiNNaker | gerçek zamanlı; 200 iğcik tek çekirdekte | — | Bölüm 3.1 | donanım kapasitesinin %1'i |
| iCub dirsek deneyi gerçek zaman faktörü | 0.16 | — | Bölüm 3.2 | 200 iğcik + fizik simülasyonu birlikte |
| Fare boynu deneyi gerçek zaman faktörü | 0.17 | — | Bölüm 3.2 | — |
| Fiziksel iCub (SpiNNaker) kaynak kullanımı | 2 çekirdek; kapasitenin %0.2'si | — | Bölüm 3.2 | 200 iğcik, iki popülasyon |

### 4b · Niteliksel bulgular
- Fusimotor sürüş yokken: kas kasılıyken iğcik aktivitesi sıfırdır; uzatma başlayınca artar, uzatma sürerken yükselir, sonra düşüp bir düzeyde durulur; Ia ile II birbirine çok benzer (Bölüm 3.1; Şekil 3).
- gamma_dynamic = 70 spike/s altında Ia ile II kökten ayrışır: yalnız dynamic sürüşten etkilenen Ia'nın yanıtı özellikle uzama fazında büyük ölçüde artar (uzama hızına duyarlılık artışı) (Bölüm 3.1; Şekil 3).
- gamma_static, hem Ia hem II duyarlılığını genel olarak artırır ve kas kasılıyken bile duyusal geri besleme sağlar (Bölüm 3.1; Şekil 3).
- NEST ve SpiNNaker hız eğrileri Simulink referansına çok yakındır (daha gürültülü); L̈'nin atılması ve spike integrasyonu, ateşleme hızı davranışlarını anlamlı biçimde değiştirmez (Bölüm 3.1).
- Fiziksel iCub denemesinde Ia ve II yalnız hareket sırasında ayrışır; baş dururken neredeyse eşitlenir — yazarlara göre merkezi sinir sistemi modeli, gamma-MN'leri uygun sürerek hareketi ve farklı gerilme düzeylerini ayırt edebilir (Bölüm 3.2; Şekil 9).
- Sınırlılıklar (yazarların kendi listesi): spike integrasyonu <30 spike/s'te aktivasyonu olduğundan düşük, >150 spike/s'te olduğundan yüksek tahmin eder; NEST implementasyonu L, L̇ atamak için durdurulup yeniden başlatılmak zorundadır; SpiNNaker sabit noktalı aritmetik doğruluğu sınırlar (Bölüm 4).

### 4c · Yazarların kendi çıkardığı sonuç
Spike tabanlı, iki platformda doğrulanmış bir proprioseptif çeviri mekanizması sunulmuştur; iki ve üç ardışık linkli kinematik yapılar için enkoder→kas uzunluğu genel çevrim denklemleri türetilmiştir. Model, gamma sürüş modülasyonu araştırmaları için test yatağıdır ve büyük ölçekli NEST simülasyonlarına ve karmaşık biyomekanik modellere bağlanabilir (Bölüm 4).

---

## 5 · Projemize ilgisi
- **Doğrudan kullanılabilir mi?** Kısmen — hem de projenin tam kalbine: kas iğciği Ia/II afferent modelimiz r(t) için uygulanabilir bir şablon sunar. Taban model (Mileusnic 2006), Parziale 2020'nin Virtual Muscle'ında da kullanılan modeldir; literatürde ortak referans noktasıdır. Bu makale, o modeli spike üreten bir birime çevirmenin yollarını ve maliyetlerini gösterir.
- **Hangi büyüklüğümüz veya parametremizle eşleşir?** (1) İğcik modeli yapısı (bag1/bag2/chain, Ia/II birleşimi, occlusion) → bizim r(t) modelimizin iç yapısı kararı; (2) L̈ = 0 sadeleştirmesi + <%1 etki ölçümü → bizim OpenSim'den uzunluk/hız alırken ivmeyi dışarıda bırakma kararına doğrudan gerekçe; (3) fusimotor spike integrasyonu (r, τ değerleri) → NEURON'da gamma-MN spike'larını f aktivasyonuna çevirme katmanı; (4) uzatma protokolü + üç fusimotor koşulu → kendi iğcik implementasyonumuzun doğrulama senaryosu; (5) normalize uzunluk (L/L0) arayüz sözleşmesi → OpenSim–NEURON köprüsünde birim dönüşümü kuralı.
- **Bilinen sistematik fark:** parametreler kedi soleus'una optimize (sıçan değil; yazarlar anatomi bütün memelilerde aynı olduğundan parametre değişimiyle başka kaslara uyarlanabileceğini söyler, Bölüm 3); simülatör NEST/SpiNNaker (bizde NEURON — matematik taşınır, kod taşınmaz); gösterimlerin gömülü tarafı motor enkoderleridir, kas-iskelet simülasyonu değildir.
- **Nereye girdi olacak:** model yapısı kararı (iğcik modeli mimarisi ve sadeleştirmeleri) + doğrulama testi (uzatma senaryosu, niteliksel beklentiler) + parametre seçimi için yol göstericisi (asıl değerler için Mileusnic 2006 açılacak).

## 6 · Bizimle çelişen veya işimize gelmeyen bulgular
- **Parametrelerin türü yanlış:** kedi soleus optimizasyonu; sıçan arka bacak kasları için doğruluk iddiası yoktur. Sıçan iğcik parametreleri ya ayrı kaynaktan bulunmalı ya da tür farkı sistematik hata olarak kabullenilmelidir.
- **Spike integrasyonunun geçerlilik penceresi (30–150 spike/s) bizim gamma sürüş aralığımızı kısıtlayabilir:** CPG kaynaklı gamma aktivitesi bu pencerenin dışına çıkarsa fusimotor aktivasyon sistematik sapar (Bölüm 2.2 ve 4). Kendi implementasyonumuzda bu pencere test edilmelidir.
- **Rate→Poisson çıktı üretimi, spike zamanlamasındaki bilgiyi atar:** Ia sinapsımız kısa-dönem plastisite veya zamanlama duyarlı mekanizma içerirse, Poisson yaklaşıklığı yeterli olmayabilir. Makale bu soruyu tartışmaz.
- **Gösterimlerde kas modeli yoktur:** uzunluk sinyali motor enkoderinden geometrik denklemlerle üretilir; iğcik-kas dinamiği etkileşimi (ekstrafusal kuvvetin iğciğe etkisi) sınanmamıştır. Bizim kurulumda uzunluk OpenSim kas liflerinden gelecektir; bu fark doğrulamada akılda tutulmalıdır.
- **NEST durdur-başlat zorunluluğu, kapalı döngü performansını düşürür** (gerçek zaman faktörü 0.44); NEURON'da eşdeğer bir veri enjeksiyon dar boğazı oluşup oluşmayacağı ayrıca değerlendirilmelidir.

## 7 · Testlere girecek değerler (varsa)
Bu makaleden sayısal referans değeri çıkmıyor (afferent hız eğrileri yalnız şekillerde verilir; şekilden sayı okunmaz). Bunun yerine NİTELİKSEL bir doğrulama senaryosu çıkıyor ve iğcik implementasyonumuzun testi olarak kullanılabilir:

| Kimlik | Değer | Aralık [alt, üst] | Gerekçe |
|---|---|---|---|
| igcik_uzatma_senaryosu (girdi) | L: 0.95·L0 (1.1 s) → 0.11·L0/s (1.1 s) → 1.08·L0 (1.1 s); koşullar: fusimotor yok / gamma_dyn 70 / gamma_stat 70 spike/s | — | Bölüm 3.1 protokolü; sayısal çıktı bandı bu makaleden alınamaz, beklenti nitelikseldir |
| beklenen davranış 1 | fusimotor yokken kasılı kasta Ia ≈ II ≈ 0; uzatmada artış | niteliksel | Bölüm 3.1, Şekil 3 |
| beklenen davranış 2 | gamma_dyn altında Ia'nın uzama fazı yanıtı II'ye göre belirgin büyür | niteliksel | Bölüm 3.1, Şekil 3 |
| beklenen davranış 3 | gamma_stat altında hem Ia hem II taban aktivitesi yükselir; kasılı kasta aktivite sıfırdan büyük | niteliksel | Bölüm 3.1, Şekil 3 |

Sayısal bant istenirse Mileusnic 2006'nın kendi doğrulama verileri açılmalıdır; `referans_degerler.json`'a giriş bu niteliksel haliyle yapılmaz (kural: sayısal aralık yoksa test dosyasına girmez, senaryo doğrulama planında tutulur).

## 8 · Özete alınmayanlar
- Eş. 1–2 ve 5–9'un tam cebirsel biçimleri (özete sözel tanımları alındı); Eş. 13–20 geometrik çevrim denklemlerinin açık ifadeleri.
- Giriş bölümündeki çeviri yaklaşımları literatürü (Bouganis 2010, Casellato 2014, Sreenivasa 2016, Niu 2017, Lin & Crago 2002, Maltenfort & Burke 2003 karşılaştırmaları).
- Şekil 5, 7, 9'daki hız/raster eğrilerinin ayrıntıları; Neurorobotics Platform transfer fonksiyonu mimarisi.
- SpiNNaker API kısıtları (yalnız üstel sinaps desteği; alfa yanıtın neden seçilmediği).

## 9 · Açık sorular / doğrulanmayanlar
- Lif parametre değerleri (KSR, KPR, β0-2, Γ1-2, C, R, a, S, X, L0^SR, L0^PR...) bu makalede yoktur; modelleme öncesi Mileusnic 2006 Tablo 1 mutlaka açılmalıdır.
- Doğrulama "directly, albeit empirically, comparable" ifadesiyle Mileusnic sonuçlarına görsel karşılaştırmadır; sayısal hata metriği (RMSE vb.) verilmez — implementasyon doğruluğu nicel olarak raporlanmamıştır.
- "varsayım:" NEST doğrulama süresi 7.51 s'nin karşılık geldiği görev süresi, protokolden 3.3 s olarak hesaplanmıştır (1.1 s × 3); makale görev süresini o cümlede açıkça yazmaz.
- Occlusion ağırlığı S'nin değeri makalede verilmez (Mileusnic 2006'ya gönderme).
