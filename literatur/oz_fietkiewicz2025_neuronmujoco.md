# Literatür özeti — Fietkiewicz 2025 (NEURON + MuJoCo nöromekanik simülasyon)

> Bu dosya makalenin **kayıplı sıkıştırmasıdır** — yerine geçmez. Amacı, makaleyi tekrar
> açmadan modelleme kararı verebilmektir.

## 1 · Künye ve sınıflandırma

- **Yazarlar / yıl:** Chris Fietkiewicz, Linh Tran, Robert McDougal, Clayton Jackson, Roger D. Quinn, Hillel J. Chiel, Peter J. Thomas, 2025
- **Başlık:** Neuromechanical Simulation with NEURON and MuJoCo
- **Dergi / cilt / sayfa:** ACM biçimli metin; Vol. 1, No. 1, s. 1–7, yayın tarihi June 2025 (dergi adı/cilt bilgisi metinde tam verilmemiş — makalede belirtilmemiş)
- **DOI / PMC:** makalede belirtilmemiş
- **PDF:** `pdf/Neuromechanical_Simulation_with_NEURON_and_MuJoCo.pdf` (depoya girmez)
- **Özeti çıkaran / tarih:** Claude (özet taslağı) / 2026-09-05 — insan doğrulaması bekliyor

- **Makale tipi:** yöntem/araç (bilgisayar modeli gösterimi)
- **Projemizin hangi tarafına bakıyor:** köprü/kapalı döngü (NEURON ↔ fizik motoru)
- **Bizim için değeri:** yöntem örneği (eş-zamanlı adım senkronizasyonu, sıçan arka bacak iskeleti) · yalnız tartışma (MuJoCo tercihi)

## 2 · Makalenin sorusu ve ana iddiası

Soru: nöral simülasyon platformları fiziksel dünyayı modelleyemezken, NEURON ile MuJoCo fizik motoru tek bir Python denetim programında birleştirilebilir mi? İddia: iki simülatörü aynı entegrasyon adımıyla eşzamanlı ilerleten basit bir Python döngüsüyle, gerçekçi bir sıçan arka bacağı kas-iskelet modeli hem açık-döngü (iki tip diken üreten nöron) hem kapalı-döngü (kas boyu geri beslemeli CPG) olarak sürülebilir. Üç model de bacakta salınımlı hareket üretmiştir; hesap yükünün çoğunu MuJoCo taşımaktadır.

---

## 3 · NEYİ NASIL YAPMIŞ (yöntem)

### 3a · Denek / malzeme / model

- Genel mimari: Python denetim programı, NEURON ve MuJoCo'yu **aynı sayısal entegrasyon adımıyla (dt = 0.025 ms) eşzamanlı** ilerleten bir döngü. Her adım öncesi NEURON'da hesaplanan kas kuvvetleri MuJoCo aktüatörlerine yazılır; kapalı-döngüde MuJoCo'da hesaplanan kas boyları NEURON'a yazılır. Tüm iletişim her platformun standart API'siyle (s. 2).
- İskelet: halka açık bir OpenSim sıçan arka bacak modelinden (Johnson ve ark. 2008; kalça, femur, tibia, ayak) türetilmiş; geometriler STL, yerleşim XML olarak **MuJoCo v2.3.5**'e çevrilmiş. Fleksör-ekstansör tendonlar moment kolu analizine göre eklenmiş ve konumlandırılmış. **Tek eklem** femur tepesinde; tibia ve ayak femura göre sabit. Yüzey teması yok; bacak kalçadan dikey asılı (s. 2).
- Nöron/kas tarafı: **NEURON v8.2**. Tüm modellerde iki nöron; her biri protraksiyon veya retraksiyonu süren tek bir kası inerve ediyor. Kas modeli Fietkiewicz ve ark. 2023'ten (Kim ve Heckman'dan uyarlanmış fizyolojik kas modeli) (s. 2).
- Üç model: (1) açık-döngü, NEURON kütüphanesinden Hodgkin-Huxley nöronu; (2) açık-döngü, Purvis ve Butera 2005 tabanlı gerçekçi motonöron (HH'ye göre çok daha düşük diken hızı); (3) kapalı-döngü CPG — Yu ve Thomas 2021 modelinden, [13]'te NEURON'a uyarlanmış; iki iletkenlik-tabanlı nöron karşılıklı inhibisyon + kontralateral kasın gerilme reseptöründen inhibitör girdi alıyor (s. 2).

### 3b · Yöntem adımları

1. OpenSim iskelet bileşenleri MuJoCo biçimine çevrilir (STL + XML); tendonlar moment kolu analizine göre yerleştirilir.
2. Her MuJoCo tendonuna, uygulanan kuvvet parametresi Python'dan programatik olarak yazılan bir aktüatör bağlanır.
3. Simülasyon döngüsü: her 0.025 ms'lik adım öncesi NEURON kas kuvveti → MuJoCo aktüatör kuvveti; (kapalı-döngüde) MuJoCo kas boyu → NEURON gerilme reseptörü parametresi; sonra iki simülatör birer adım ilerletilir.
4. Açık-döngü modellerde her iki nörona çakışmayan, farklı başlangıç zamanlı uyarı darbeleri verilir (önce retraksiyon, sonra protraksiyon üretmek için) (s. 3).
5. Kapalı-döngü modelde dış uyarı yoktur; ritim iç dinamikten ve kas boyu geri beslemesinden doğar (s. 3).
6. Hesap süresi analizi: MuJoCo entegrasyonu ve parametre okuma/yazma seçici olarak devre dışı bırakılarak platform başına göreli süre ölçülür (s. 4).

### 3c · Tanım ve birim uyarıları

- "Kas" NEURON içinde yaşayan bir mekanizmadır; MuJoCo tarafındaki aktüatör **kas-tendon dinamiği içermez**, yalnız dışarıdan yazılan kuvveti uygular. Bizim OpenSim Hill kas-tendon birimimizle aynı adlandırma farklı içerik taşır.
- "Gerilme reseptörü", kas boyundan hesaplanan basit bir inhibitör geri beslemedir; fizyolojik iğcik (Ia/II) modeli değildir.
- "Kas boyu" MuJoCo tendon uzunluğundan türetilen bir parametredir; birim metinde verilmemiş.
- Bacak açısı rad cinsinden; kuvvet N cinsinden (Şekil 2, 3 eksenleri).

### 3d · Kullanılan parametreler ve değerleri

| Parametre | Değer | Birim | Nereden (tablo/şekil/sayfa) |
|---|---|---|---|
| Entegrasyon adımı (her iki simülatör) | 0.025 | ms | s. 2 |
| MuJoCo sürümü | v2.3.5 | — | s. 2 |
| NEURON sürümü | v8.2 | — | s. 2 |
| Model 1 (HH) uyarısı: genlik / darbe süresi / başlangıç ofseti | 10 / 70 / 200 | nA / ms / ms | s. 3 |
| Model 2 (motonöron) uyarısı: genlik / darbe süresi / başlangıç ofseti | 1 / 360 / 400 | nA / ms / ms | s. 3 |
| Nöron sayısı / kas sayısı | 2 / 2 | adet | s. 2 |
| Eklem sayısı (hareketli) | 1 (femur tepesi) | adet | s. 2 |

---

## 4 · NE SONUÇ BULMUŞ

### 4a · Sayısal sonuçlar

| Büyüklük | Değer | Birim | Nereden (tablo/şekil/sayfa) | Saçılım (SD/SEM/aralık, n) |
|---|---|---|---|---|
| Kapalı-döngü CPG tek çevrim süresi | ~3,570 | ms | Fig. 3(a); s. 3 | tek model, saçılım yok |
| Fig. 3(a) zaman ekseni başlangıcı (geçici rejimi atlamak için) | 640 | ms | s. 4 | — |
| 10,000 ms simülasyon için toplam hesap süresi | 12.7 (ortalama) | s | s. 4 | ortalama; n makalede belirtilmemiş |
| Göreli hesap payları: MuJoCo / Python / NEURON | %60 / %28 / %12 | — | Fig. 3(b); s. 4 | — |
| Donanım | MacBook Air M2, macOS 14.0 | — | s. 4 | — |
| MuJoCo'nun OpenSim'e göre hız iddiası | 600 ya da 900 kata kadar | — | s. 2 (atıfla: [17, 31]) | **alıntı iddia**, bu çalışmada ölçülmemiş |

### 4b · Niteliksel bulgular

- Açık-döngü modellerde diken salvosu kas kuvvetini kademeli yükseltir; nöron sustuktan sonra **kalsiyum dinamiği kuvveti bir süre taşır**, sonra kuvvet sıfıra döner; bacak açısı kuvvetle orantılı seyreder (s. 3).
- İki kuvvetin örtüştüğü dönemde karşıt kas kuvvetleri eşitlendiğinde bacak açısı sıfıra döner; iki açık-döngü modelin zaman ölçeği farkı yalnız nöron diken hızlarından kaynaklanır (s. 3).
- Kapalı-döngü model **dış uyarı olmadan** salınımı sürdürür; sonuçlar önceki sarkaç-tabanlı sürümlerle ([13], [33]) "çok benzer" (s. 3).
- Nöral-kas-iskelet bileşenlerinin çift yönlü bağlanması başlangıçta geçici (transient) davranış üretir (s. 4).

### 4c · Yazarların kendi çıkardığı sonuç

NEURON + MuJoCo birleşimi, açık ve kapalı döngü nöromekanik modelleri basit bir Python denetim programıyla çalıştırabilir. Hesap süresinin en büyük payı MuJoCo'ya, sonra Python denetimine aittir; gelecekte verimlilik için bellek erişimi, Python derleyicisi ve MuJoCo C++ API'si önerilir. Teknik, uzuv boyu ve lokomosyon çevrim periyodu farklı organizmalar arasında nicel karşılaştırmayı kolaylaştıracaktır (s. 4).

---

## 5 · Projemize ilgisi

- **Doğrudan kullanılabilir mi?** Kısmen. İskelet tabanı bizimkiyle **aynı kaynak** (Johnson ve ark. 2008 sıçan arka bacağı) ve nöron tarafı NEURON; eşzamanlı adım senkronizasyonu (kuvvet → fizik motoru, boy → NEURON) bizim OpenSim köprümüzün birebir şablonudur. Ancak fizik motoru MuJoCo'dur ve kas dinamiği NEURON içindedir; bizim ters dinamik + statik optimizasyon iş akışımız burada yok.
- **Hangi büyüklüğümüz veya parametremizle eşleşir?** (a) dt = 0.025 ms — Kim 2020 özetindeki NEURON adımıyla aynı; döngü senkronizasyonu için ortak adım seçimi örneği. (b) u(t) → aktüatör kuvveti ve X_m → r(t) veri akış yönleri. (c) Johnson 2008 iskelet geometrisi.
- **Bilinen sistematik fark:** MuJoCo aktüatörü kas-tendon dinamiği taşımaz (kuvvet dışarıdan yazılır); bizde Hill modeli OpenSim'de. Tek eklem, iki kas, yüzey teması yok — bizim çok-eklemli, temaslı lokomosyon hedefimizin çok altında. Gerilme reseptörü fizyolojik iğcik değil. Motonöron havuzu/PIC yok.
- **Nereye girdi olacak:** model yapısı kararı (senkron adım köprü mimarisi; performans bütçesi planlaması — darboğazın fizik motoru olabileceği bilgisi) · yalnız tartışma (MuJoCo'ya geçiş gerekirse hız verisi).

## 6 · Bizimle çelişen veya işimize gelmeyen bulgular

1. **Fizik motoru tercihi bize aykırı (s. 2):** Makale, MuJoCo'nun OpenSim'den 600 ya da 900 kata kadar hızlı olduğu atıflı iddiasını tekrarlar ve OpenSim yerine MuJoCo'yu seçer. Projemiz OpenSim üzerine kurulu; uzun simülasyonlarda hesap süresi sorun olursa bu bulgu bizim mimari tercihimize karşı bir argümandır. (Not: hız iddiası bu çalışmada ölçülmemiş, [17, 31]'den alıntıdır.)
2. **Kas, fizik motorunun dışında:** Bizim iş akışımız kas-tendon dinamiğini OpenSim'de tutar; bu makale tüm kas dinamiğini NEURON'a taşır ve mekanik tarafta yalnız çıplak kuvvet aktüatörü bırakır. İki mimari, moment kolu–kuvvet etkileşimini farklı yerde çözer; sonuçları doğrudan kıyaslanamaz.
3. **Duyusal geri besleme aşırı basitleştirilmiş:** Kontralateral inhibitör "gerilme reseptörü", bizim Ia/II iğcik modelimizin yerini tutmaz; bu makale kapalı-döngü afferent modellemesi için doğrulama kaynağı olamaz.
4. **Ölçek çelişkisi:** Tek serbestlik dereceli, temassız, dikey asılı bacak — yürüme benzeri görevlerdeki moment kolu ve yük dağılımı doğrulamalarımıza taban oluşturmaz.

## 7 · Testlere girecek değerler (varsa)

Bu makaleden doğrulama testi çıkmıyor: tüm sayısal sonuçlar (çevrim süresi ~3,570 ms, hesap payları) bu makaleye özgü basit CPG ve tek eklemli düzeneğin ürünüdür; bizim modelimiz için referans değer taşımaz.

## 8 · Sıkıştırmada ne düştü

- Şekil 2'nin panel-panel zaman serileri (voltaj, kuvvet, açı eğrilerinin ayrıntısı).
- Animasyon bağlantıları ([3], YouTube listesi) ve içerikleri — incelenmedi.
- Giriş bölümündeki platform taraması (Gazebo/NEST, MUSIC, NRP, EBRAINS, NEUROiD vb. atıf listesi).
- Yazar katkıları, teşekkür, hibe numaraları.
- Kaynak koda erişim bilgisi: metinde açık bir depo bağlantısı verilmemiş (2023 makalesindekinden farklı olarak) — sonradan gerekirse yazarlara/animasyon sayfasına bakılmalı.

## 9 · Açık sorular / doğrulanmayanlar

- Kas kuvvetinin MuJoCo aktüatörüne hangi ölçek/birim dönüşümüyle yazıldığı metinde yok.
- Gerilme reseptörünün fonksiyonel biçimi (eşik, kazanç, boydan iletkenliğe dönüşüm) bu makalede verilmemiş; [13] ve [33]'e bakılmalı.
- "Moment kolu analizine göre tendon yerleşimi"nin ayrıntısı (hangi açı aralığı, hangi hedef moment kolları) belirtilmemiş.
- Derginin künyesi (ACM hangi yayını) metinden çıkarılamıyor; **varsayım:** ön baskı/kabul aşaması biçimlendirmesi.
- Özeti çıkaran not: bu özet LLM tarafından üretildi; sayılar insan tarafından doğrulanmadan referans alınmamalı.
