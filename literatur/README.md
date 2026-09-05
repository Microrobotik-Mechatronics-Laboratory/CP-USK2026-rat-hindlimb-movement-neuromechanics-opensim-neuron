# literatur — Literatür Özetleri ve Tolerans Bantları

Bu klasör, projenin bilimsel iddialarının **dayandığı dış kaynakları** ve bu kaynaklardan
çıkarılan **sayısal referans değerleri** tutar. Testler (İP-8) sayıyı koda gömmez; buradan okur.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `oz_SABLON.md` | Literatür özeti şablonu — yeni bir makale eklerken kopyalanır |
| `oz_<kisa_ad>.md` | Bir makalenin materyal-metot ve sonuç özeti (insan okur) |
| `referans_degerler.json` | Çıkarılan sayısal değerler + tolerans bantları (kod okur) |
| `diyagramlar/` | Modelin nöron-kas yapısını gösteren Mermaid diyagramları (D1–D8) — **diyagramların kaynağı burasıdır**, `PREPRINT.md`'ye kopyalanır |
| `pdf/` | Makale PDF'leri — **git-ignore'dadır, commit edilmez** (telif) |

## Adımlar: bir makale nasıl eklenir

1. PDF'i `literatur/pdf/` altına koy (repoya girmez).
2. Makalenin özetini çıkar — `oz_SABLON.md`'yi `oz_<kisa_ad>.md` olarak kopyala ve doldur.
   Aşağıdaki istem bu iş için hazırdır.
3. Kullanılacak her sayıyı `referans_degerler.json`'a bir kayıt olarak ekle: değer, birim,
   nereden alındığı (tablo/şekil numarası), **tolerans bandı ve gerekçesi**.
4. Testi ancak bundan sonra yaz (`04_KURALLAR.md`: bant önce ilan edilir).

## Özet çıkarma yönergesi (makaleyi Claude'a verirken kullan)

> Aşağıdaki metni makale PDF'i ile birlikte ver. Amaç, makaleyi **bozmadan sıkıştırmak**;
> yorum katmak değil.

```
Bu makaleyi literatur/oz_SABLON.md şablonuna göre özetle.

Kurallar:
- Şablonun bölüm sırasını ve başlıklarını aynen koru.
- Her sayısal değerin yanına birimini ve NEREDEN alındığını (tablo/şekil/sayfa) yaz.
  Kaynağı yazılamayan sayıyı hiç yazma.
- Makalede olmayan hicbir şeyi ekleme, boşluğu tahminle doldurma. Bilmiyorsan alanı boş
  bırak veya "makalede belirtilmemiş" yaz.
- Yuvarlama yapma; makaledeki basamak sayısını koru. Birim dönüşümü yaptıysan hem
  orijinali hem dönüştürülmüşü yaz.
- Bölüm 6 (bizimle çelişen bulgular) ZORUNLUDUR. Bu makalede aşağıdaki projeyle çelişen
  veya onu desteklemeyen ne varsa oraya yaz; hiçbir şey bulamadıysan ne aradığını yazarak
  "çelişki bulunamadı" de.
- Bölüm 8'e (özete alınmayanlar) özete almadığın bölümleri, ek dosyaları ve atladığın
  şekilleri listele.
- Yorum ile bulguyu karıştırma: makalenin dediği ile senin çıkarımın ayrı yazılsın
  (çıkarımı "varsayım:" veya "yorum:" diye işaretle).

Projemizin bağlamı (uygulanabilirlik bölümünü buna göre doldur):
Sprague-Dawley sıçanı arka bacağının nöromekanik kapalı-döngü modeli. OpenSim'de Hill tipi
kas-iskelet modeli (Johnson ve ark. 2008 tabanlı), NEURON'da omurilik devresi (CPG,
internöronlar, motonöron havuzu, Ia afferent). Ayrıntı: ../PREPRINT.md
```

## Bant ilkesi (özet)

Literatürle karşılaştırma **birebir eşleşme değildir.** Sonucun makul bir aralıkta kalması ve
farkın gerekçelendirilebilir olması aranır. Bant **testten önce** ilan edilir; ölçüm banda
düşmezse önce model ve varsayımlar sorgulanır, bant sessizce genişletilmez. Tam kural:
`../SDLC/04_KURALLAR.md` "Literatüre yakınlık" bölümü.

## Kayıt türleri

`referans_degerler.json`'daki her kaydın bir `kaynak_tipi` alanı vardır:

- **`literatur`** — dış bir yayından çıkarılmış değer. Bandın gerekçesi tür/koşul farkını
  ve yayımlanmış saçılımı söyler.
- **`ic_olcum`** — bu projede bağımsız olarak ölçülmüş ve `DOGRULAMA.md`'ye işlenmiş
  değer. Bandı bir **regresyon** bandıdır (sayı değişirse haberimiz olsun), literatür bandı
  değildir. İkisi karıştırılmaz.
