# Özüt — Johnson 2008 (sıçan arka bacak geometrisi ve moment kolları)

> Bu dosya makalenin **kayıplı sıkıştırmasıdır** — yerine geçmez. Amacı, makaleyi tekrar
> açmadan modelleme kararı verebilmektir.

## 1 · Künye ve sınıflandırma

- **Yazarlar / yıl:** Will L. Johnson, Devin L. Jindrich, Roland R. Roy, V. Reggie Edgerton — 2008
- **Başlık:** A three-dimensional model of the rat hindlimb: musculoskeletal geometry and muscle moment arms
- **Dergi / cilt / sayfa:** Journal of Biomechanics, 41(3): 610–619
- **DOI / PMC:** makalenin bu (NIH yazar el yazması) sürümünde DOI yazılı değil; PMC'de Ocak 2009'dan itibaren erişilir deniyor
- **PDF:** `pdf/A_three-dimensional_model_of_the_rat_hindlimb_musculoskeletal_geometry_and_muscle_moment_arms.pdf` (depoya girmez)
- **Özütü çıkaran / tarih:** Claude / 05.09.2026

- **Makale tipi:** deneysel (kadavra ölçümü) + yarı-statik bilgisayar modeli
- **Projemizin hangi tarafına bakıyor:** mekanik (OpenSim) — modelimizin tabanı olan çalışma
- **Bizim için değeri:** parametre kaynağı (geometri, eklem merkezi, moment kolu) + doğrulama referansı

## 2 · Makalenin sorusu ve ana iddiası

Sıçan arka bacağının dinamik bir kas-iskelet modeline giden ilk adım olarak kas bağlantı noktalarını, eklem merkezlerini ve moment kollarını ölçmüşler. İki yöntem sorusu soruyorlar: eklem merkezleri eklem açısının basit fonksiyonlarıyla, kas bağlantı alanları düşük dereceli eğrilerle temsil edilebilir mi? Ana hipotezleri, tek başına postür değişiminin (özellikle dört ayaktan iki ayağa geçişin) seçilmiş bacak kaslarının işlevini değiştirmeye yettiğidir. İddiaları: birinci dereceden eklem merkezi fonksiyonları ve parabol bağlantı fitleri yeterlidir; moment kolları lokomosyon açı aralığında az değişir; postür değişimi bazı kasların içsel stabilizasyon özelliğini ortadan kaldırır.

## 3 · NEYİ NASIL YAPMIŞ (yöntem)

### 3a · Denek / malzeme / model

Yedi dişi Sprague-Dawley sıçanı (280 ± 16 g). İlk 3 hayvan kas bağlantı noktası sayısallaştırması, kalan 4 hayvan eklem merkezi belirleme için (Tablo 1). Hazırlık: diseksiyon sırasında anestezi (100 mg/kg ketamin + 5 mg/kg ksilazin, i.p.), krural ve ventromedial kalça kaslarına geçerken ötanazi (125 mg/kg sodyum pentobarbital, i.p.). Ölçüm aracı: iki dijital kamerayla stereofotogrametri (kameralar ~90° farklı bakış açısıyla), ticari yazılım SIMI Motion; tüm dönüşümler, fitler ve moment kolu hesapları MATLAB ile. Bipedal lokomosyon açıları için ayrıca 5 sıçan, 13 cm/s bantta, gövde askısıyla kısmi vücut ağırlığı desteğinde yürütülmüş; 4 kameralı hareket yakalama.

### 3b · Yöntem adımları

1. Kemik segmentlerine (omurga, kalça, femur, tibia, ayak) işaretleyici iğneler (20 gauge × 1 inç) yerleştirilmiş; her yönelimde 3 iğne görünür olacak şekilde.
2. Kaslar kemikten sırayla diseke edilmiş; her bağlantı alanı, 3 iğneyle birlikte çift fotoğraflanmış. Yön değiştiren kaslarda ara nokta "via point" olarak kaydedilmiş.
3. SIMI Motion ile her origin/insertion için kamera koordinat sisteminde (CCS1) 3B koordinat; alan büyüklüğüne göre fotoğraf başına 1–3 nokta, özellik başına 1–3 fotoğraf → bağlantı başına 3–27 nokta.
4. Kemikler soyulup yeniden fotoğraflanmış; iğne ve kemik nirengi noktaları ikinci kamera sisteminde bulunup doğrudan doğrusal dönüşümle kemik koordinat sistemine (BCS, Şekil 1 + Tablo 2) çevrilmiş. CCS1↔BCS rotasyonu, gürültü için en küçük kareler algoritmasıyla (Goryn ve Hein 1995) bulunmuş.
5. Eklem merkezleri: iğneli kemikler doğal aralıkta hareket ettirilirken fotoğraflanmış; anlık eklem eksenleri Woltring (1985) yöntemiyle; ortalama merkez, anlık eksenlerin kesişiminin en küçük kareler kestirimi; anlık merkez, ortalamanın anlık eksene izdüşümü.
6. Anlık merkez verisine 0., 1. ve 2. dereceden fonksiyonlar fit edilmiş (Denklem 1); hata, distal segment ucunun ölçülen ve hesaplanan konumları arasındaki ortalama mesafenin distal segment boyuna oranı (Tablo 4). Her eklem için 1. derece seçilmiş.
7. Kas bağlantı noktaları: tüm hayvanların noktaları 1. hayvanın segment boylarına normalize edilip birleştirilmiş; 2. dereceden (5'ten az nokta varsa 1. dereceden) eğri fit edilmiş; origin/insertion, bu fitin ağırlık merkezi alınmış (Şekil 2).
8. Moment kolu: kasın etki doğrultusundaki birim vektör ile insertion'ın eklem merkezinden yarıçap vektörünün dış çarpımı (Şekil 2).
9. Bipedal lokomosyon eklem açıları: iliak krista, büyük trokanter, lateral kondil, lateral malleol ve distal metatars işaretleyicilerinden, özel MATLAB rutinleriyle.

### 3c · Tanım ve birim uyarıları

- **Moment kolu tanımı geometrik:** birim etki vektörü × yarıçap vektörü dış çarpımı. Tendon gezinme yöntemi (−dL/dθ) DEĞİL. OpenSim moment kolu hesabıyla karşılaştırırken tanım farkı akılda tutulmalı.
- **Açı işaretleri:** addüksiyon, iç rotasyon, kalça fleksiyonu, diz ekstansiyonu ve ayak bileği dorsifleksiyonu pozitif (Tablo 2 başlığı). Bu yüzden diz fleksiyon açıları ve moment kolları negatif çıkar (Şekil 3 açıklaması); yaygın anatomik adlandırmayla matematiksel tanım burada ayrışıyor.
- **Sıfır açı:** proksimal ve distal segment eksenlerinin aynı yönelimde olduğu açı (Şekil 1).
- **Normalizasyon:** tüm ölçümler 1. hayvanın segment boylarına ölçeklenmiş; mutlak mm değerleri o hayvanın boyutuna göredir.
- **İçsel stabilizasyon ölçütü:** moment kolunun açıya göre negatif eğimle sıfırı kesmesi (Young ve ark. 1993'e atıfla).
- **Lokomosyon açı aralıkları (bu makalede kullanılan):** dört ayaklı — kalça −5°…50°, diz −110°…−60°, ayak bileği −20°…40° (Gruner 1980; Thota 2005'e atıfla). İki ayaklı — kalça −30°…−5°, diz −110°…−60°, ayak bileği −60°…−20° (kendi ölçümleri).

### 3d · Kullanılan parametreler ve değerleri

| Parametre | Değer | Birim | Nereden (tablo/şekil/sayfa) |
|---|---|---|---|
| Hayvan sayısı (bağlantı / eklem merkezi) | 3 / 4 | adet | Tablo 1 |
| Vücut ağırlığı (7 hayvan) | 280 ± 16 | g | Yöntemler, "Specimen variability" |
| Tibia boyu | 39–41 | mm | Tablo 1 |
| Femur boyu | 34–36 | mm | Tablo 1 |
| Anestezi | 100 ketamin + 5 ksilazin | mg/kg, i.p. | Yöntemler, s. 3 |
| Ötanazi | 125 pentobarbital | mg/kg, i.p. | Yöntemler, s. 3 |
| Bağlantı başına sayısallaştırılan nokta | 3–27 | adet | Yöntemler, s. 3 |
| Bipedal bant hızı | 13 | cm/s | Yöntemler, "Locomotion joint angle" |
| Bipedal ölçüm hayvan sayısı | 5 | adet | Yöntemler, "Locomotion joint angle" |
| Eklem merkezi fit derecesi (seçilen) | 1 | — | Sonuçlar, "Joint Centers" |
| 1. derece fit katsayıları (kalça/diz/bilek) | tam liste | mm, mm/rad | Tablo 5 (buraya alınmadı) |
| Kas bağlantı merkezleri ve genişlikleri (85 bölge) | tam liste | mm | Tablo 6 (buraya alınmadı) |

## 4 · NE SONUÇ BULMUŞ

### 4a · Sayısal sonuçlar

| Büyüklük | Değer | Birim | Nereden (tablo/şekil/sayfa) | Saçılım (SD/SEM/aralık, n) |
|---|---|---|---|---|
| Kalibrasyon bloğu RMS hatası | 0.22 | mm | Sonuçlar, s. 4 | 28 ölçüm |
| Tek nokta tekrar SD | 0.08 | mm | Sonuçlar, s. 4 | 20 tekrar |
| Kalça eklem merkezi bağıl hata (1. derece) | 6.6 | % | Tablo 4 | ortalama hata 1.79 mm |
| Diz eklem merkezi bağıl hata (1. derece) | 4.1 | % | Tablo 4 | ortalama hata 1.56 mm |
| Bilek eklem merkezi bağıl hata (1. derece) | 4.0 | % | Tablo 4 | ortalama hata 1.53 mm |
| BFA kalça moment kolu (tam fleksiyon → tam ekstansiyon) | ~0 → −15.3 | mm | Sonuçlar "Moment arms" + Şekil 3A | — |
| AM moment kolu aralığı: fizyolojik / dört ayaklı lokomosyon | 4.9 / 1.0 | mm | Sonuçlar "Moment arms" | — |
| Bipedal ile quadrupedal ortalama moment kolu farkı | 45 (ortalama); 5 kasta >100 | % | Sonuçlar "Moment arms" | 37 kas modeli |
| Pectineus + obturatorların fleksör→ekstansör geçişi | 21–40 | ° kalça fleksiyonu | Sonuçlar + Şekil 3B,C | — |
| Lokomosyon aralığının ≤15° yakınında tepe yapan kas | 27 / 37 | adet | Tartışma, "Low variability" | — |
| İçsel stabilizatör kas sayısı | 8 | adet | Tartışma, "Intrinsically stabilizing" | 3 kalça F/E + GI + 4 kuadriseps (diz add/abd) |
| Bağlantı elipsoid hacim aralığı | 0.03 – 626 | mm³ | Sonuçlar "Muscle attachments" | gastrocnemius insertion → GMa origin |
| Hacmi <100 mm³ olan bağlantı oranı | 95 | % | Sonuçlar "Muscle attachments" | — |
| Hayvanlar arası bağlantı merkezi SD (ortalama) | 2.20 | mm | Sonuçlar "Muscle attachments" | 85 bölge; 66'sında <3 mm |
| SD'si bağlantı genişliğinden küçük bölge oranı | 61 | % | Sonuçlar "Muscle attachments" | — |

### 4b · Niteliksel bulgular

- "Most muscles have moment arms with a large range across the physiological domain of joint angles, but their moment arms peak and vary little within the locomotion domain" (Özet). Modelleme sonucu: lokomosyon aralığında moment kolu ~sabit varsayımı savunulabilir.
- Eklem merkezi hareket tarifi: kalça ekstansiyonunda femur başı hafif rostral+ventral kayar; diz fleksiyonunda tibia kondilleri femurun ekstansör yüzüne kayar; bilek ekstansiyonunda ayak lateral öteleme + talokrural arayüzün plantarındaki bir nokta etrafında dönme.
- Bipedal aralıkta pectineus/obturator moment kolları sıfırı kesmez → içsel stabilizasyon kaybolur; kontrol yükü sinir sistemine kayar.
- Kedi (Burkholder ve Nichols 2004) ile fleksiyon/ekstansiyon moment kolları işaret ve eğilim olarak tutarlı; bilek add/abd'de TA ve EDL işaretleri türler arasında farklı (kedide stabilizatör, sıçanda TA addüktör, EDL abdüktör; ikisi de çok küçük). Yazarlar farkı digitigrad/plantigrad postürle açıklıyor.
- Model şimdilik statik; lokomosyona doğrudan uygulama için kas fizyolojisi ve eklem dinamiği gerekecek (Tartışma).

### 4c · Yazarların kendi çıkardığı sonuç

Eklem merkezleri eklem açısının 1. dereceden fonksiyonlarıyla doğru modellenebilir; bağlantılar doğrusal/karesel fit ağırlık merkezleriyle temsil edilebilir; kas işlevi büyük ölçüde moment kolunun açıyla değişimince belirlenir. Quadrupedal→bipedal postür geçişi bazı kasların stabilizasyon davranışını ortadan kaldırır, bazılarının moment kolunu ciddi değiştirir. Sınırlılık: model statiktir.

## 5 · Projemize ilgisi

- **Doğrudan kullanılabilir mi?** Evet — OpenSim modelimizin (Johnson tabanlı) kaynak geometrisi bu makalenin Tablo 5–6'sıdır.
- **Hangi büyüklüğümüzle eşleşir?** Kas origin/insertion/via koordinatları, eklem merkezi fonksiyonları, moment kolu–açı eğrileri; ters dinamik ve statik optimizasyonun geometrik tabanı.
- **Bilinen sistematik fark:** dişi SD ~280 g kadavra ölçümü; bizim simülasyon senaryolarımızın hayvan boyutuyla ölçek farkı olabilir. Moment kolu tanımı geometrik (dış çarpım), OpenSim tendon-gezinme türeviyle küçük farklar verebilir. Açı işaret kuralları OpenSim koordinatlarına eşlenmeli.
- **Nereye girdi olacak:** parametre seçimi (geometri) + doğrulama testi (moment kolu eğrileri) + model yapısı kararı (1. derece eklem merkezi yeterliliği).

## 6 · Bizimle çelişen veya işimize gelmeyen bulgular

- **Model statik:** kas kuvveti, PCSA, lif boyu, tendon özellikleri YOK. Hill parametrelerimiz buradan gelemez; başka kaynak şart.
- **Moment kolu eğrileri sayı olarak verilmemiş** (yalnız Şekil 3–4 grafikleri). Doğrulama testi kurarken şekilden okuma hatası kaçınılmaz; bant geniş tutulmalı.
- **Postüre bağlı işlev değişimi bize ek yük:** bipedal senaryo simüle edersek quadrupedal aralık için doğrulanmış varsayımlar (moment kolu ~sabit, içsel stabilizasyon) geçersizleşiyor. Tek "lokomosyon moment kolu" sabiti kullanan basitleştirme bipedal tarafta ortalama %45 hata taşır.
- **Diz için 0. ve 1. derece fit hatası eşit** (Tablo 4: %4.1 – %4.1); 1. derece seçimi hataya değil insan dizi literatürüne dayandırılmış. Dizde sabit merkez varsayımı da aynı doğrulukta savunulabilirdi.

## 7 · Testlere girecek değerler (varsa)

| Kimlik | Değer | Bant [alt, üst] | Gerekçe (tür/koşul farkı, saçılım, model basitleştirmesi) |
|---|---|---|---|
| momentkolu_BFA_kalca_tamekstansiyon | −15.3 mm | [−18, −12] | Şekilden/metinden tek değer; hayvanlar arası SD 2.20 mm ve tanım farkı payı |
| eklemmerkezi_bagil_hata_ust | ≤7 % | [0, 7] | Tablo 4 üst sınırı; OpenSim iskeletimizin uç nokta hatası bu bandı aşmamalı |
| pectineus_sifir_kesme_kalca | 21–40 ° | [15, 45] | Şekil 3B'den; şekil okuma ve birey farkı payı |

## 8 · Sıkıştırmada ne düştü

- Tablo 5'in tam katsayı seti (kalça/diz/bilek, pelvis-femur-tibia-ayak referanslı x/y/z, a·b·c katsayıları) — modele girerken doğrudan tablodan alınmalı.
- Tablo 6'nın 85 satırlık tam bağlantı koordinatları ve genişlikleri (A–D blokları).
- Tablo 2 (BCS eksen tanımları) ve Tablo 3 (anatomik kısaltmalar).
- Şekil 3–4'teki tüm kasların moment kolu eğrileri (yalnız örnek değerler alındı).
- Giriş bölümünün SCI literatür taraması.

## 9 · Açık sorular / doğrulanmayanlar

- Moment kolu eğrilerinin sayısal verisi yayında yok; **varsayım:** doğrulama bantlarını şekillerden okuyacağız.
- Tablo 5 katsayılarının açı birimi makalede açıkça yazılmamış (Denklem 1'de θ, φ, ψ rotasyon açıları); **varsayım:** radyan. Modele girmeden birim, uç nokta hatasını yeniden üreterek test edilmeli.
- MTL, kas kuvvet parametreleri, sarkomer verisi bu makalede belirtilmemiş.
- DOI bu el yazması sürümünde yok; künye depoya işlenirken yayıncı sayfasından tamamlanmalı.
