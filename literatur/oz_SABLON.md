# Özüt — <Makale kısa adı>

<!-- ==========================================================================
DOLDURAN İÇİN TALİMAT (özüt tamamlanınca bu blok silinebilir)

Bu şablonu bir makale PDF'i ile birlikte aldıysan: makaleyi bu şablona göre özütle.

ODAK — sadece iki şey önemli:
  (1) NEYİ NASIL YAPMIŞ  -> bölüm 3
  (2) NE SONUÇ BULMUŞ    -> bölüm 4
Diğer bölümler bu ikisini kullanılabilir kılmak içindir. Makalenin tamamını
aktarma; giriş/literatür taraması/teşekkür/uzun tartışma özüte GİRMEZ.

KURALLAR:
- Şablonun bölüm sırasını ve başlıklarını aynen koru.
- Makalede olmayan hiçbir şeyi ekleme. Bilmiyorsan alanı boş bırak veya
  "makalede belirtilmemiş" yaz. Tahminle doldurma.
- Her sayının yanına birimini ve NEREDEN alındığını yaz (tablo/şekil/sayfa).
  Kaynağı yazılamayan sayıyı hiç yazma.
- Yuvarlama yapma; makaledeki basamak sayısını koru. Birim dönüştürdüysen
  hem orijinali hem dönüştürülmüşü yaz.
- Makalenin dediği ile senin çıkarımını karıştırma. Çıkarımı "yorum:" veya
  "varsayım:" diye işaretle.
- Bölüm 6 (çelişen bulgular) ZORUNLUDUR; boş bırakılamaz.
- Uymayan bölümlere "bu makale için geçerli değil" yaz, silme.

PROJE BAĞLAMI (bölüm 5'i buna göre doldur):
Sprague-Dawley sıçanı arka bacağının nöromekanik kapalı-döngü modeli.
Mekanik taraf: OpenSim, Hill tipi kas-iskelet modeli (Johnson ve ark. 2008 tabanlı),
ters dinamik + statik optimizasyon. Nöron tarafı: NEURON — merkezi örüntü üreteci
(CPG), internöronlar, motonöron havuzu (PIC/Cav1.3), kas iğciği Ia/II afferenti.
Hedef: motonöron çıkışı -> kas aktivasyonu u(t), iğcik geri beslemesi r(t) -> Ia
sinapsı olacak şekilde döngüyü kapatmak. Ayrıntı: ../PREPRINT.md
========================================================================== -->

> Bu dosya makalenin **kayıplı sıkıştırmasıdır** — yerine geçmez. Amacı, makaleyi tekrar
> açmadan modelleme kararı verebilmektir.
>
> Kullanım: `cp oz_SABLON.md oz_<yazar><yil>_<konu>.md` (ör. `oz_johnson2008_momentkolu.md`).

## 1 · Künye ve sınıflandırma

- **Yazarlar / yıl:**
- **Başlık:**
- **Dergi / cilt / sayfa:**
- **DOI / PMC:**
- **PDF:** `pdf/<dosya>.pdf` (depoya girmez)
- **Özütü çıkaran / tarih:**

- **Makale tipi:** deneysel · bilgisayar modeli · derleme · yöntem/araç · karma
- **Projemizin hangi tarafına bakıyor:** nöron (NEURON) · mekanik (OpenSim) · köprü/kapalı döngü · genel
- **Bizim için değeri:** parametre kaynağı · doğrulama referansı · yöntem örneği · yalnız tartışma/atıf

## 2 · Makalenin sorusu ve ana iddiası
> 3-5 cümle. Ne sormuşlar, ne bulduklarını iddia ediyorlar. Bizim projemizle ilgisi burada
> kurulmaz (o bölüm 5'tir) — burası makalenin kendi anlatımıdır.

---

## 3 · NEYİ NASIL YAPMIŞ (yöntem)

> **Ana bölüm.** Yöntemi, biri aynı işi tekrar yapabilecek kadar açık yaz — ama makalenin
> metnini kopyalama, adımlara indir.

### 3a · Denek / malzeme / model
> Deneysel çalışmada: tür, soy, cinsiyet, ağırlık, n, hazırlık (in vivo / in vitro / ex vivo),
> anestezi, sıcaklık, yükleme veya uyarım koşulu.
> Bilgisayar modeli çalışmasında: model tipi, kaç bölme/hücre, hangi yazılım ve sürümü,
> hangi önceki modelden türetilmiş, entegrasyon adımı.
> Derlemede: hangi çalışmalar taranmış, dahil etme ölçütü.

### 3b · Yöntem adımları
> Numaralı liste. Ölçüm/hesap sırası, hangi aşamada neyin sabit tutulduğu.

### 3c · Tanım ve birim uyarıları
> **Kritik.** Aynı adı taşıyan büyüklük farklı tanımlanmış olabilir (ör. moment kolunu
> `-dL/dθ` ile mi, yarıçap vektörü çapraz çarpımıyla mı tanımlamış; iletkenliği hücre başına
> mı, birim alana mı vermiş). Bizimkinden farklı olan her tanımı burada yaz.

### 3d · Kullanılan parametreler ve değerleri
> Modelin/deneyin girdileri. Bizim modelimize doğrudan aktarılabilecek sayılar çoğunlukla
> buradadır.

| Parametre | Değer | Birim | Nereden (tablo/şekil/sayfa) |
|---|---|---|---|
| | | | |

---

## 4 · NE SONUÇ BULMUŞ

> **Ana bölüm.** Yazarların sonuçları — yorum katmadan.

### 4a · Sayısal sonuçlar

> Her satırın **nereden** geldiği yazılmadan kayıt tamam sayılmaz; sonradan PDF'e dönebilmenin
> tek yolu budur.

| Büyüklük | Değer | Birim | Nereden (tablo/şekil/sayfa) | Saçılım (SD/SEM/aralık, n) |
|---|---|---|---|---|
| | | | | |

### 4b · Niteliksel bulgular
> Sayıya dökülmeyen ama modelleme kararını etkileyen ifadeler (ör. "moment kolları lokomosyon
> bölgesinde tepe yapıp az değişir"). Mümkünse alıntı biçiminde, kendi yorumun karıştırılmadan.

### 4c · Yazarların kendi çıkardığı sonuç
> Makalenin sonuç bölümünün 2-4 cümlelik özeti. Yazarların koyduğu sınırlılıklar varsa ekle.

---

## 5 · Projemize ilgisi
- **Doğrudan kullanılabilir mi?** (evet / kısmen / hayır — neden)
- **Hangi büyüklüğümüz veya parametremizle eşleşir?**
- **Bilinen sistematik fark:** (tür, ölçek, tanım, koşul, sıcaklık, hazırlık)
- **Nereye girdi olacak:** parametre seçimi · doğrulama testi · model yapısı kararı · yalnız tartışma

## 6 · Bizimle çelişen veya işimize gelmeyen bulgular
> **Boş bırakılamaz.** Çelişki bulamadıysan ne aradığını yazarak "çelişki bulunamadı" de.
> Özütlemede en kolay kaybolan şey, modelimizi desteklemeyen bulgudur.

## 7 · Testlere girecek değerler (varsa)
> Yalnız bu makaleden bir **doğrulama testi** çıkacaksa doldurulur; çoğu makaleden çıkmaz —
> o durumda "bu makaleden test çıkmıyor" yaz. Doldurulursa bu satırlar
> `referans_degerler.json`'a da işlenir (kural: `../SDLC/04_KURALLAR.md`).

| Kimlik | Değer | Bant [alt, üst] | Gerekçe (tür/koşul farkı, saçılım, model basitleştirmesi) |
|---|---|---|---|
| | | | |

## 8 · Sıkıştırmada ne düştü
> Özüte almadığın ama makalede olan, sonradan gerekebilecek şeyler: ham veri tabloları, ek
> dosyalar (supplementary), okunmayan bölümler, atlanan şekiller. Bir sayı tartışmalı hale
> gelirse **önce buraya** bakılır, sonra PDF açılır.

## 9 · Açık sorular / doğrulanmayanlar
> Makalede net olmayan, varsayımla doldurduğun noktalar. Varsayımları "varsayım:" diye işaretle.
