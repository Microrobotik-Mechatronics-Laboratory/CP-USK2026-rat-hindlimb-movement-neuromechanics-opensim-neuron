# Literatür özeti — Moore ve ark. 2015 (Renshaw hücresi ↔ motonöron sinaptik bağlantısı)

> Bu dosya makalenin **seçici özetidir** — yerine geçmez. Amacı, makaleyi tekrar
> açmadan modelleme kararı verebilmektir.

## 1 · Künye ve sınıflandırma

- **Yazarlar / yıl:** Niall J. Moore, Gardave S. Bhumbra, Joshua D. Foster, Marco Beato — 2015 (Moore ve Bhumbra eşit katkılı)
- **Başlık:** Synaptic Connectivity between Renshaw Cells and Motoneurons in the Recurrent Inhibitory Circuit of the Spinal Cord
- **Dergi / cilt / sayfa:** The Journal of Neuroscience, 35(40), 13673–13686
- **DOI / PMC:** DOI 10.1523/JNEUROSCI.2541-15.2015 (Open Access)
- **PDF:** `pdf/Synaptic_Connectivity_between_Renshaw_Cells_and_Motoneurons_in_the_Recurrent_Inhibitory_Circuit_of_the_Spinal_Cord.pdf` (repoya girmez)
- **Özeti çıkaran / tarih:** Claude (Deniz'in isteğiyle) / 06.09.2026

- **Makale tipi:** deneysel (in vitro elektrofizyoloji + Bayesian quantal analysis)
- **Projemizin hangi tarafına bakıyor:** nöron (NEURON) — rekürren inhibisyon devresi: MN→RC eksitatör sinaps, RC→MN inhibitör sinaps, yakınsama (convergence) oranları
- **Bizim için değeri:** parametre kaynağı (sinaps quantal parametreleri, yakınsama, frekansa bağlı depresyon) · doğrulama referansı (RC ateşleme sadakati) — tür/yaş farkı şerhiyle

## 2 · Makalenin sorusu ve ana iddiası

Renshaw hücreleri motor çıkışın kollateralini alan tek merkezi nöron popülasyonudur; ama tek bir motonörondan ve yakınsayan motonöron havuzundan RC'ye gelen eksitatör sinapsın etkinliği bilinmiyordu. Yazarlar fare lumbar omurilik diliminde, kimliği doğrulanmış bağlantılı MN–RC çiftlerinden çift whole-cell kayıt almış. Ana iddiaları: tek motonöron girdisi bile RC'de büyük, neredeyse hiç başarısızlık göstermeyen eksitatör iletkenlik doğurur; bu güç, çok sayıda salım bölgesine (release site) yüksek salım olasılığıyla dayanır ve tek MN, RC'yi eşik üstüne çıkarıp ateşletebilir. Çiftlerin yaklaşık üçte biri karşılıklı (reciprocal) bağlıdır; hem eksitatör hem inhibitör yönde yakınsama geniştir. Sonuç: rekürren devrenin motor çıkış üzerindeki rolü sanılandan çok daha önemli olabilir.

---

## 3 · NEYİ NASIL YAPMIŞ (yöntem)

### 3a · Denek / malzeme / model

- Tür/soy: fare; GlyT2-EGFP transgenik hat (glisinerjik internöronlar EGFP ile işaretli; Zeilhofer ve ark. 2005).
- Yaş/cinsiyet: postnatal 8–14 gün; erkek veya dişi.
- Hazırlık: in vitro dilim. Üretan anestezisi (20–30 mg i.p.), buz soğuğu aCSF ile intrakardiyak perfüzyon, ventral laminektomi. Kaudal lumbar segment (L5), 400 µm kalınlık, transvers düzleme 35° eğik kesim (motor akson kollateralleri ve ventral kökler korunacak şekilde). 37 °C'de 45 dk inkübasyon, sonra oda sıcaklığında tutum; kayıtta 5–8 ml/dk süperfüzyon, %95/5 O2/CO2.
- aCSF (mM): 113 NaCl, 3 KCl, 25 NaHCO3, 1 NaH2PO4, 2 CaCl2, 2 MgCl2, 11 D-glukoz.
- Kayıt: RC'lerde voltage clamp (−60 mV tutma; Axopatch 200B), MN'lerde current clamp (ELC-03X). Filtre 5 kHz, örnekleme 50 kHz. Elektrotlar: RC için 3 MΩ, MN için 4 MΩ. Seri direnç 6–12 MΩ, %60–80 kompanzasyon; %20'den fazla artarsa kayıt terk edilmiş.
- Hücre kimliği: RC = EGFP(+) + lamina VIII'in en ventral bölgesi + ventral kök uyarımına ortodromik eksitasyon (işlevsel doğrulama). MN = lateral motor kolon konumu + soma çapı ≥ 20 µm veya ventral kök uyarımına antidromik spike.
- Salım olasılığı manipülasyonu: hücre dışı Ca²⁺ 1–4 mM aralığında değiştirilmiş (Ca yerine eşmolar Mg).
- Analiz: Bayesian quantal analysis (BQA; Bhumbra ve Beato 2013) — quantal size (q), maksimal yanıt (r = n·q) ve salım bölgesi sayısı (n) için posterior dağılımlar; medyanlar en iyi tahmin.

### 3b · Yöntem adımları

1. Yazarlar loose cell-attached konfigürasyonda aday presinaptik MN'leri uyarıp bağlantı aramış; bağlantı bulununca MN yeni elektrotla tekrar yamalanıp current clamp'te kaydedilmiş.
2. Çift kayıt: MN'de akım basamaklarıyla spike trenleri (her 9 s'de bir; darbe aralığı 33 ms), RC'de eş zamanlı EPSC kaydı. 30 bağlantılı çift toplanmış.
3. Ca²⁺ 1 / 2 / 4 mM'de yanıtlar ölçülmüş; PPR (paired-pulse ratio: 2. spike yanıtı / 1. spike yanıtı) hesaplanmış.
4. BQA yalnızca ilk spike yanıtlarına uygulanmış (sinaptik depresyonun analizi bozmaması için); 30 çiftin 15'i yeterli veri vermiş.
5. Karşılıklılık testi: 19 çiftte RC'de spike uyandırılıp MN'de (15 mV düzeyindeki tutmada; işaret için bkz. Bölüm 9) IPSC aranmış.
6. Çift current clamp: 10 çiftte tek MN girdisinin RC'yi ateşletip ateşletmediği ölçülmüş; ateşleme olasılığı, daha önce voltage clamp'te ölçülen EPSC boyutuyla karşılaştırılmış.
7. Popülasyon girdisi: supramaksimal ventral kök uyarımıyla bütün MN havuzu antidromik ateşletilmiş; RC'de bileşik EPSC kaydedilmiş (QX-315 Br 3 mM içeren pipetle) ve BQA ile toplam salım bölgesi sayısı çıkarılmış (22 hücre). Latans heterojenliği yüzünden yanıtlar genlik yerine yük (pC) olarak, tüm sinaptik olay süresi üzerinden ölçülmüş.
8. Depresyon: 20 darbelik ventral kök trenleri 3 / 10 / 33 / 50 / 100 Hz'de; EPSC_n / EPSC_1 oranları (13 hücre).
9. RC ateşleme sadakati: loose cell-attached (hücre içi diyalizsiz) kayıtla aynı trenlerde ateşleme olasılığı (12 hücre; ayrıca 1 vs 2 mM Ca karşılaştırması için 9 hücrelik ayrı set).
10. Rekürren IPSC: ventral kök uyarımıyla MN'lerde disinaptik IPSC (17 hücre). Cs-glukonat pipet, QX-315 Br; akımları küçültmek için doygunluk altı striknin (3–10 nM — makalede "nm" basılmış; bkz. Bölüm 9) veya gabazin (30 µM) ve yükseltilmiş hücre içi Cl⁻ (30–60 mM); MN'ler eksitatör akımların tersinme potansiyelinde tutulmuş (jonksiyon potansiyeli düzeltmesi 15,8 / 13,6 / 10,9 mV; 8 / 38 / 68 mM toplam CsCl için; işaret için bkz. Bölüm 9). Quantal parametre kestirimi yalnızca Ca ≤ 2 mM'de yapılmış (2 mM üstü multiveziküler salım yaptığı için; Bhumbra ve ark. 2014).

### 3c · Tanım ve birim uyarıları

- **n = "release site" (salım bölgesi) sayısıdır, anatomik temas sayısıyla aynı şey değildir**; yazarlar karşılaştırmayı tartışarak yapıyor (s. 13680–13681). Modele "sinaps sayısı" olarak aktarılacaksa bu ayrım korunmalı.
- **Birim farkı:** çift kayıtlarında quantal size pA (akım genliği); ventral kök deneylerinde pC (yük, alan integrali). İkisi doğrudan oranlanamaz; yakınsama hesabı n'ler üzerinden yapılıyor (30,3/7,1 ≈ 4), q'lar üzerinden değil.
- **PPR tanımı:** 2. uyarıya yanıt / 1. uyarıya yanıt; 33 ms aralıkta (≈30 Hz). PPR > 1 potansiyasyon, < 1 depresyon.
- **Bütün yakınsama sayıları alt sınırdır (lower bound):** dilim hazırlığı akson kollaterallerini kesmiş olabilir; kayıtlı hücreler yüzeyden ≤150 µm derinlikte.
- **Rekürren IPSC quantal değerleri farklı kayıt koşullarının havuzudur** (farklı Cl⁻, farklı blokerler); yazarlar bunların saçılımının arttığını ve önceki ölçümlerle doğrudan karşılaştırılamayacağını söylüyor (s. 13680).
- Potansiyeller mutlak mV cinsinden (RC tutma −60 mV); Cisi-Kohn'daki "dinlenim = 0" konvansiyonuyla karıştırılmamalı.

### 3d · Kullanılan parametreler ve değerleri

| Parametre | Değer | Birim | Nereden (tablo/şekil/sayfa) |
|---|---|---|---|
| Hayvan yaşı | P8–14 | gün | Materials and Methods, s. 13674 |
| Dilim kalınlığı / kesim açısı | 400 / 35 | µm / ° | s. 13674 |
| Hücre dışı Ca²⁺ koşulları | 1 / 2 / 4 (kontrol: 2) | mM | s. 13674–13675 |
| Spike treni: tekrar aralığı / darbe aralığı | 9 s / 33 ms | — | s. 13674 |
| Ventral kök tren frekansları | 3, 10, 33, 50, 100 | Hz | Şekil 8, s. 13682 |
| RC tutma potansiyeli | −60 | mV | s. 13675 |
| MN tutma (IPSC kayıtları) | 15 mV düzeyi, eksitatör tersinme potansiyeli (jonksiyon düzeltmesi 15,8/13,6/10,9; işaret: bkz. Bölüm 9) | mV | s. 13674 ve 13678 |
| Striknin / gabazin (doygunluk altı) | 3–10 nM (makalede "nm") / 30 µM | — | s. 13680 |

### 4a'ya girmeyen ara değer: RC whole-cell kapasitansı ~30 pF, kompanzasyon sonrası köşe frekansı 1–4 kHz (s. 13674).

---

## 4 · NE SONUÇ BULMUŞ

### 4a · Sayısal sonuçlar

| Büyüklük | Değer | Birim | Nereden | Saçılım (SD/SEM/aralık, n) |
|---|---|---|---|---|
| PPR, Ca 1 / 2 / 4 mM | 1,41 / 1,00 / 0,74 | — | Şekil 1E metni, s. 13675 | SEM ±0,12 / ±0,03 / ±0,07; Kruskal–Wallis χ²=17,6, p<0,001; n=7/30/10 kayıt |
| MN→RC quantal size (q), çift kayıt | 21 | pA | Şekil 3A metni, s. 13676 | SEM ±4; n=15 çift (BQA) |
| MN→RC maksimal yanıt (r) | 121 | pA | Şekil 3B metni, s. 13676 | SEM ±21; n=15 |
| MN→RC salım bölgesi sayısı (n) | 7,1 | adet | Şekil 3C metni, s. 13676 | SEM ±1,2; n=15 |
| Örnek çift: q̂ / r̂ / n̂ | 23,1 / 210,5 / 9 | pA / pA / adet | Şekil 2 metni, s. 13676 | tek çift |
| Salım olasılığı, çift kayıt, 2 mM Ca | 0,49 | — | Tartışma, s. 13681 | SEM ±0,07; aralık 0,11–0,85 |
| Karşılıklı bağlantı oranı | 7/19 (~%37) | — | Şekil 4 metni, s. 13677–13678 | — |
| IPSC–EPSC boyut korelasyonu (karşılıklı çiftler) | \|r\| = 0,537 (işaret: bkz. Bölüm 9) | — | Şekil 4C, s. 13677 | p = 0,245 (anlamsız) |
| Bağlantı gücü – hücre mesafesi korelasyonu | \|r\| = 0,322 (işaret: bkz. Bölüm 9) | — | Şekil 4F, s. 13677 | p = 0,082 (anlamsız) |
| İlk spike'ta RC ateşleme olasılığı ↔ EPSC boyutu | r = 0,639 | — | Şekil 5E, s. 13679 | p = 0,038; n=10 çift |
| VR→RC quantal size (q) | 0,20 | pC | Şekil 7A metni, s. 13680 | SEM ±0,03; n=22 hücre |
| VR→RC maksimal yanıt (r) | 5,56 | pC | Şekil 7B, s. 13680 | SEM ±0,97 |
| VR→RC salım bölgesi sayısı (n) | 30,3 | adet | Şekil 7C, s. 13680 | SEM ±3,0 |
| VR→RC salım olasılığı, 2 / 1 mM Ca | 0,622 / 0,125 | — | s. 13680 | SEM ±0,050 / ±0,025 |
| MN→RC yakınsaması (tahmin) | ~4 MN / RC | — | Tartışma, s. 13681 (30 site ÷ 7,1 site/MN) | alt sınır |
| VR tren depresyonu, 20. darbe | depresyon frekansla artıyor; 100 Hz'de azalma >%50 | — | Şekil 8 metni, s. 13679 ve 13682 | Spearman \|r\|=0,714, p<0,001; n=13 hücre (işaret: bkz. Bölüm 9) |
| 2. yanıtta frekans etkisi | yok | — | s. 13679 | \|r\|=0,014, p=0,931 |
| RC 2. darbede ateşleme (10/33/50/100 Hz) | 12/12; 11/12; 6/11; 7/10 | hücre | Şekil 9J metni, s. 13679–13683 | interpulse aralıkla zayıf korelasyon: \|r\|=0,361, p=0,016 (işaret: bkz. Bölüm 9) |
| Tren boyunca ateşleme olasılığı ↔ frekans | frekans arttıkça azalıyor | — | Şekil 9I, s. 13683 | Spearman \|r\|=0,528, p<0,001; 50 sweep (işaret: bkz. Bölüm 9) |
| Loose cell-attached: tek VR uyarımına spike | %100 (hem 1 hem 2 mM Ca) | — | s. 13680 | n=9 hücre |
| VR→MN rekürren IPSC: q | 10,1 | pA | Şekil 11A metni, s. 13680 | SEM ±0,9; n=17 hücre |
| VR→MN rekürren IPSC: r | 2.146,9 | pA | Şekil 11B, s. 13680 | SEM ±263,6 |
| VR→MN salım bölgesi sayısı (n) | 225 | adet | Şekil 11C, s. 13680 | SEM ±27 |
| VR→MN salım olasılığı, 2 mM Ca | 0,40 | — | Şekil 11D metni, s. 13681 | SEM ±0,05; akımla pozitif korelasyon r=0,663, p=0,003 |
| Örnek MN: q̂ / r̂ / n̂ | 15,5 / ~2.150 / ~139 | pA / pA / adet | Şekil 10 metni, s. 13680 | tek hücre |
| RC→MN yakınsaması (tahmin) | ~40 RC / MN | — | Tartışma, s. 13681 (225 ÷ 5,5 temas/RC; 5,5±0,5 Bhumbra ve ark. 2014'ten) | alt sınır |
| İnhibitör/eksitatör yakınsama oranı | ~10 kata kadar | — | Tartışma, s. 13681 | yazarların çıkarımı |

### 4b · Niteliksel bulgular

- Kontrol koşulunda (2 mM Ca) tek MN'nin RC'de doğurduğu EPSC'ler "tipik olarak büyük, az sayıda başarısızlıkla ya da hiç başarısızlık olmadan" (s. 13675).
- 1 mM Ca'da yanıtlar küçük, çok başarısızlıklı ve potansiyasyonlu; 4 mM'de maksimal, başarısızlıksız ve net depresyonlu (Şekil 1).
- Çift current clamp'te: küçük EPSC'li çiftte ilk spike hiç eşiğe ulaştırmıyor (ancak temporal toplama ile bazen 2.'de); büyük EPSC'li çiftte 1. ve 3. uyarıda düzenli spike, 2. ve 4.'te AHP nedeniyle başarısızlık (Şekil 5C–D, s. 13678–13679).
- Frekansa bağlı depresyona rağmen 100 Hz'e kadar süregelen yanıt var; RC ateşleme sadakati 50 Hz'e kadar korunuyor, 100 Hz'de bile sürebiliyor (s. 13683). Yazarlar bu sadakati talamustaki "relay" kavramına benzetiyor.
- MN konumları çoğunlukla gluteal ve hamstring kaslarını innerve eden havuz içinde; bütün RC'ler lamina VIII ventral bölümünün merkezinde, gri-beyaz madde arayüzünün 100 µm içinde (s. 13677).
- Bağlamsal bilgi: motonöronlar merkezi sinapslarda ACh + glutamat (belki aspartat) birlikte salar; MN→RC sinapsında AMPA + nikotinik + NMDA reseptörleri birlikte çalışır (Tartışma, s. 13681–13683, atıflarla).

### 4c · Yazarların kendi çıkardığı sonuç

MN→RC girdisi, çok sayıda salım bölgesinde yüksek salım olasılığıyla güçlüdür ve tek motonöron RC'yi ateşletebilir; bağlantıların önemli bölümü karşılıklıdır ve karşılıklılık kural bile olabilir (dilimde kesilen bağlantılar yüzünden %37 alt sınırdır). İnhibitör yöndeki yakınsama eksitatör yönden 10 kata kadar geniştir. Sınırlılıklar: dilim hazırlığı (kesilen kollateraller, kayıp inen/nöromodülatör girdiler), juvenil doku; MN–MN ve RC–RC iç bağlantıları ölçülmeden devrenin resmi eksiktir. Bulgular gelecekteki motor kontrol modelleri için temel parametre setidir (Significance Statement, s. 13673).

---

## 5 · Projemize ilgisi

- **Doğrudan kullanılabilir mi?** Kısmen. NEURON ağımızda Renshaw hücresi katmanı kurulacaksa MN→RC ve RC→MN sinapslarının quantal yapısı (q, n, salım olasılığı), yakınsama oranları (~4 MN/RC; ~40 RC/MN) ve frekansa bağlı depresyon profili bu makaleden parametrelenebilir — tür/yaş dönüşümü şerhiyle.
- **Hangi büyüklüğümüz veya parametremizle eşleşir?** (1) MN→RC sinaps ağırlığı ve salım bölgesi sayısı; (2) RC→MN inhibitör iletkenlik toplamı (havuz düzeyinde r ≈ 2,1 nA ölçeği); (3) motonöron ateşleme frekansı bandında (≤50–100 Hz) RC izleme sadakati — bizim CPG kaynaklı MN ateşleme desenlerinin RC katmanından nasıl geçeceğine dair doğrulama hedefi.
- **Bilinen sistematik fark:** tür (fare ↔ Sprague-Dawley sıçanı); yaş (P8–14 juvenil ↔ yetişkin hedef; sinaps olgunlaşması farklı olabilir); hazırlık (400 µm dilim, kesilmiş kollateraller → yakınsama alt sınır); sıcaklık (oda sıcaklığı; vücut sıcaklığında kinetikler hızlanır); inen ve nöromodülatör girdiler yok.
- **Nereye girdi olacak:** parametre seçimi (RC devresi kurulursa) + model yapısı kararı (karşılıklılık oranı, yakınsama mimarisi) + doğrulama testi adayı (aşağıda Bölüm 7).

## 6 · Bizimle çelişen veya işimize gelmeyen bulgular

- **Rekürren inhibisyonun gücü literatürde iki kutuplu.** Bu makale güçlü diyor; ama kendilerinin de andığı Lindsay ve Binder (1991) ile Maltenfort ve ark. (2004) dolaylı ölçümlerle "marjinal inhibitör etki" bulmuştu (s. 13674). Cisi-Kohn (2008) tarzı havuz modellerindeki zayıf RC ağırlıklarını mı, bu makaledeki güçlü sinapsları mı alacağımız bir karar noktasıdır; ikisi aynı modelde aynı anda doğru olamaz.
- **Alvarez ve ark. (1999) ekstrapolasyonu ~75 MN/RC'ye kadar çıkıyor; bu çalışma ~4 MN/RC buluyor** (s. 13680–13681). Yazarlar farkı üst sınır/alt sınır ve yöntem farklarıyla açıklıyor; yakınsamayı parametre yaparken aralık bu iki uç arasında belirsizdir.
- **Juvenil fare verisi:** bizim yetişkin sıçan modelimize ölçeklemenin doğrulanmış bir çarpanı yok. Quantal değerleri mutlak almak yerine göreli yapı (yüksek salım olasılığı, çoklu salım bölgesi, güçlü tek girdi) taşınmalı.
- **İşimize gelmeyen pratik nokta:** rekürren IPSC quantal değerleri karışık kayıt koşullarının havuzu (yazarların kendi uyarısı, s. 13680) — RC→MN iletkenliğini sayısal olarak buradan almak zayıf zemindir; tekil sinaps için Bhumbra ve ark. (2014) birincil kaynaktır.

## 7 · Testlere girecek değerler (varsa)

Aşağıdakiler adaydır; `referans_degerler.json`'a işlenmesi Deniz'in onayına ve tür-farkı gerekçesinin kabulüne bağlıdır (fare P8–14 → sıçan dönüşümü doğrulanmamış):

| Kimlik | Değer | Aralık [alt, üst] | Gerekçe (tür/koşul farkı, saçılım, model basitleştirmesi) |
|---|---|---|---|
| rc_mn2rc_release_sites | 7,1 | [4, 12] | SEM ±1,2 ve alt-sınır uyarısı; fare→sıçan farkı için aralık genişletildi (Şekil 3C, s. 13676) |
| rc_mn2rc_quantal_pA | 21 | [10, 40] | SEM ±4; oda sıcaklığı ve juvenil doku; mutlak değil ölçek testi olarak (Şekil 3A, s. 13676) |
| rc_ppr_30Hz_2mMCa | 1,00 | [0,7, 1,3] | SEM ±0,03 ama hücreler arası saçılım geniş (Şekil 1F); 33 ms aralık ≈ 30 Hz (s. 13675) |
| rc_firing_fidelity_33Hz | ≥ 0,9 (2. darbe) | [0,85, 1,0] | 11/12 hücre; model RC'si 33 Hz MN trenini izleyebilmeli (s. 13679–13683) |
| rc_convergence_mn_per_rc | 4 | [4, 75] | alt sınır bu makale, üst sınır Alvarez 1999 ekstrapolasyonu (s. 13680–13681) |

## 8 · Özete alınmayanlar

- BQA yönteminin matematiği (Bhumbra ve Beato 2013'e atıf; posterior dağılım şekilleri Şekil 2C–E, 6C–E, 10C–E).
- Şekil 8 ve 9'daki frekans×darbe bazlı tam grup verileri (yalnızca uç değerler özetlendi).
- Artefakt çıkarma prosedürü (uyarı artefaktının son bileşeninin üstel fitle çıkarılması) ve spontan olay kirliliğinde alan/genlik ölçekleme katsayısı.
- Tartışmadaki nöromüsküler kavşak salım olasılığı karşılaştırmaları (sıçan NMJ 0,06–0,16; kurbağa 0,32–0,65) — RC sinapsı için bağlam.
- Elektriksel kenetlenme (gap junction) ve RC–RC / MN–MN iç bağlantı literatürü (s. 13683'te "eksik resim" tartışması).

## 9 · Açık sorular / doğrulanmayanlar

- **Eksi işaretleri:** bu PDF'in metin katmanı eksi işaretlerini büyük ölçüde düşürüyor (korelasyon katsayıları ve tutma potansiyelleri işaretsiz görünüyor). İşareti yazarların düzyazısından doğrulanamayan her korelasyon bu özette mutlak değer (\|r\|) olarak verildi; yön, sözel ifadeden aktarıldı. MN tutma potansiyelinin ve jonksiyon düzeltme değerlerinin işareti de aynı sebeple bu oturumda doğrulanamadı. Sayısal işaret gerekiyorsa yayımcı sürümünden (JNeurosci HTML) bakılmalı.
- **QX-315 Br:** makale iki yerde "QX-315 Br" yazıyor; yaygın bilinen sodyum kanal blokeri QX-314 bromürdür. Varsayım: QX-314 kastediliyor; doğrulanmadı.
- **Striknin birimi:** metinde "3–10 nm" basılmış (s. 13680); varsayım: nM kastediliyor. Doğrulanmadı.
- **Kayıt sıcaklığı:** dilimler oda sıcaklığında tutulmuş; kayıt sırasındaki banyo sıcaklığı ayrıca yazılmamış. Varsayım: kayıtlar oda sıcaklığında.
- Yakınsama hesapları iki farklı deneyin n'lerinin oranıdır; hata yayılımı (belirsizlik aralığı) makalede verilmemiş.
- P8–14 penceresinde glisinerjik/GABAerjik sinaps olgunlaşması sürer; yetişkinde q ve n'nin nasıl değişeceği bu makaleden çıkarılamaz.
