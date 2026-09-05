# Özüt — <Makale kısa adı>

> **Ne olduğu:** Bu dosya bir makalenin **kayıplı sıkıştırmasıdır** — makalenin yerine geçmez.
> Amacı, makaleyi tekrar açmadan modelleme kararı verebilmek ve testlere sayı sağlamaktır.
> Doldurulan her sayı `referans_degerler.json`'a da işlenmelidir; yalnız burada kalan sayı
> teste giremez.
>
> Şablon kopyalanır: `cp oz_SABLON.md oz_<kisa_ad>.md`. Boş bırakılan alan **"bilinmiyor"**
> demektir; tahminle doldurulmaz.

## 1 · Künye
- **Yazarlar / yıl:**
- **Başlık:**
- **Dergi / cilt / sayfa:**
- **DOI / PMC:**
- **PDF:** `pdf/<dosya>.pdf` (depoya girmez)
- **Özütü çıkaran / tarih:**

## 2 · Ne yaptılar (açıklama)
> 3-6 cümle. Makalenin sorusu, yaklaşımı ve ana iddiası. Bizim projemizle ilgisi burada değil,
> bölüm 5'te kurulur — burası makalenin kendi anlatımıdır.

## 3 · Materyal ve metot

### 3a · Tür ve deney koşulları
> Tolerans bandının gerekçesi buradan çıkar. Koşullar bizimkinden ne kadar farklıysa, bant
> o kadar geniş olmalı ve gerekçesi o kadar açık yazılmalı.

- **Tür / soy / cinsiyet / ağırlık:**
- **Hazırlık (in vivo / in vitro / ex vivo / bilgisayar modeli):**
- **Sıcaklık, anestezi, yükleme/uyarım koşulu:**
- **Örneklem sayısı (n) ve saçılım (SD / SEM / aralık):**

### 3b · Ölçüm nasıl yapıldı
> Yöntemin kendisi. **Tanım farkına dikkat:** aynı adı taşıyan büyüklük farklı tanımlanmış
> olabilir (ör. moment kolu `-dL/dθ` ile mi, yarıçap vektörü çapraz çarpımıyla mı tanımlanmış).
> Bizim yöntemimizden farklıysa açıkça yaz — sayılar aynı adı taşısa da aynı şeyi ölçmüyor olabilir.

## 4 · Çıkarılan sayısal sonuçlar

> Her satırın **nereden** geldiği (tablo/şekil/sayfa) yazılmadan kayıt tamam sayılmaz —
> sonradan PDF'e dönebilmenin tek yolu budur.

| Büyüklük | Değer | Birim | Nereden (tablo/şekil/sayfa) | Saçılım |
|---|---|---|---|---|
| | | | | |

### 4a · Metinden okunan niteliksel bulgular
> Sayıya dökülmeyen ama modelleme kararını etkileyen ifadeler (ör. "moment kolları lokomosyon
> bölgesinde tepe yapıp az değişir"). Alıntı biçiminde, kendi yorumun karıştırılmadan.

## 5 · Bizim modele uygulanabilirliği
- **Doğrudan karşılaştırılabilir mi?** (evet / kısmen / hayır — neden)
- **Hangi büyüklüğümüzle eşleşir?** (`referans_degerler.json` kimliği)
- **Bilinen sistematik fark:** (ölçek, tanım, tür, koşul)
- **Hangi karara girdi olacak:** (parametre seçimi / doğrulama testi / yalnız tartışma)

## 6 · Bizimle çelişen veya işimize gelmeyen bulgular
> **Bu bölüm boş bırakılamaz.** Boşsa "çelişki bulunamadı" yazılır ve ne arandığı belirtilir.
> Özütleme sırasında en kolay kaybolan şey, modelimizi desteklemeyen bulgudur; bu yüzden
> ayrı ve zorunlu bir bölümdür.

## 7 · Önerilen tolerans bandı

| Kimlik | Bant [alt, üst] | Gerekçe (tür/koşul farkı, saçılım, model basitleştirmesi) |
|---|---|---|
| | | |

## 8 · Sıkıştırmada ne düştü
> Özüte girmeyen ama makalede olan, sonradan gerekebilecek şeyler: ham veri tabloları, ek
> dosyalar (supplementary), okunmayan bölümler, atlanmış şekiller. Bir sayı teste girip
> tartışmalı hale gelirse **önce buraya bakılır**, sonra PDF açılır.

## 9 · Açık sorular / doğrulanmayanlar
> Makalede net olmayan, bizim varsayımla doldurduğumuz noktalar. Varsayım yaptıysan
> "varsayım:" diye işaretle.
