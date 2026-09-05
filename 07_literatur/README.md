# 07_literatur — Referans Makale Özütleri ve Tolerans Bantları

Bu klasör, projenin bilimsel iddialarının **dayandığı dış kaynakları** ve bu kaynaklardan
çıkarılan **sayısal referans değerleri** tutar. Testler (İP-8) sayıyı koda gömmez; buradan okur.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `oz_SABLON.md` | Makale özütü şablonu — yeni bir makale eklerken kopyalanır |
| `oz_<kisa_ad>.md` | Bir makalenin materyal-metot ve sonuç özütü (insan okur) |
| `referans_degerler.json` | Çıkarılan sayısal değerler + tolerans bantları (kod okur) |
| `pdf/` | Makale PDF'leri — **git-ignore'dadır, commit edilmez** (telif) |

## Yordam: bir makale nasıl eklenir

1. PDF'i `07_literatur/pdf/` altına koy (depoya girmez).
2. `oz_SABLON.md`'yi `oz_<kisa_ad>.md` olarak kopyala ve doldur. Materyal-metot bölümünde
   **tür, deney koşulu ve ölçüm yöntemi** mutlaka yazılsın — tolerans bandının gerekçesi
   buradan gelir.
3. Kullanılacak her sayıyı `referans_degerler.json`'a bir kayıt olarak ekle: değer, birim,
   nereden alındığı (tablo/şekil numarası), **tolerans bandı ve gerekçesi**.
4. Testi ancak bundan sonra yaz (`04_KURALLAR.md`: bant önce ilan edilir).

## Bant ilkesi (özet)

Literatürle karşılaştırma **birebir eşleşme değildir.** Sonucun makul bir aralıkta kalması ve
farkın gerekçelendirilebilir olması aranır. Bant **testten önce** ilan edilir; ölçüm banda
düşmezse önce model ve varsayımlar sorgulanır, bant sessizce genişletilmez. Tam kural:
`../SDLC/04_KURALLAR.md` "Literatüre yakınlık" bölümü.

## Kayıt türleri

`referans_degerler.json`'daki her kaydın bir `kaynak_tipi` alanı vardır:

- **`literatur`** — dış bir yayından çıkarılmış değer. Bandın gerekçesi tür/koşul farkını
  ve yayımlanmış saçılımı söyler.
- **`ic_olcum`** — bu projede bağımsız olarak ölçülmüş ve `02_DOGRULAMA_KAYDI.md`'ye işlenmiş
  değer. Bandı bir **regresyon** bandıdır (sayı değişirse haberimiz olsun), literatür bandı
  değildir. İkisi karıştırılmaz.
