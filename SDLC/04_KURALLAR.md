# KURALLAR — Çalışma Kuralları

> Referans dosya. Git, dokümantasyon, yorum, test ve raporlama kuralları tek yerde.

## Git commit
- **Biçim:** `tip: açıklama` — Türkçe, buyruk kipi. Depo geçmişindeki tipler: `src:`, `doc:`, `init:`.
  Öneri seti: `src:` (kaynak kod), `doc:` (dokümantasyon), `veri:` (veri/çıktı), `model:` (osim/mod),
  `fix:` (düzeltme), `init:` (kuruluş).
- **Sıklık:** Her **anlamlı VE küçük** değişiklikte commit at. Kısa ama açıklayıcı mesaj yaz.
  Commit atmak için dosyaların birikmesini **bekleme** — amaç ilerlemenin izini tutmak.
- **Yazarlık:** Commit mesajında Claude/agent/otomatik üretimden **kesinlikle bahsetme**;
  `Co-Authored-By` veya benzeri iz **eklenmez**.
- **Emoji:** Commit mesajlarında ve projenin **hiçbir yerinde** emoji kullanılmaz.
- **Push/PR:** Değişiklikler otomatik commit'lenir; **push kullanıcı onayı ile**. Bir PR'a
  yetecek anlamlı değişiklik birikince push + pull request aç, uygunsa merge et.
- **Hijyen:** `.DS_Store` git-ignore'da; commit'e girmemeli. Makale PDF'leri
  (`07_literatur/pdf/`) telif nedeniyle commit edilmez.
- Ana dal `main`, `origin`'i takip eder (herkese açık lab reposu).

## Bağımlılık
- Yeni bir çalışma-zamanı bağımlılığı kullanan kod, **aynı commit'te** beyanını da ekler
  (ana ortam için `pyproject.toml`). Beyansız `import` bırakılmaz — risk-2 tekrarını önler.
- Bağımlılık hangi ortama ait olduğu belirtilerek eklenir: proje **iki ortamlıdır**
  (3.14 NEURON / 3.13 OpenSim). Ayrıntı: `06_KURULUM.md`.

## Dokümantasyon
- Her `.py` betiği başında **Türkçe sağlayıcı/provenance başlığı**: ne ürettiği, girdisi/çıktısı,
  hangi kaynaktan/önceki adımdan türediği (mevcut `03_kod` deseni). Betik hangi ortamda
  koşuyorsa (3.14 / 3.13) başlıkta belirtilir.
- Bilimsel iddialar **bağımsız yeniden ölçülür**; `02_DOGRULAMA_KAYDI.md` tarzı doğrulama defteri
  tutulur. Devir belgelerinden taşınan sayı, yeniden ölçülene kadar "doğrulanmamış" sayılır.
- Proje durumu/tarihçe her zaman `SDLC/`'ye yazılır.

## Satır-içi yorumlar
- Dil **Türkçe**. Yorumlar "**neden**"i açıklar, "ne"yi değil.
- Çevredeki kodun stiline uy: yoğunluk, adlandırma, deyim (idiom). Yeni desen icat etme.
- Kritik/kaygan yerleri işaretle (ör. entegrasyon adımı, saturasyon sabiti, birim dönüşümü).
- **Emoji yok** — kod, yorum, dokümantasyon ve commit dahil projenin hiçbir yerinde.

## Test / doğrulama

### Altyapı
Ayrı test çerçevesi (pytest) **yok**; doğrulama kod içinde yapılır:
- `assert`'ler (ör. `r31_uret.py` bilinen referans değerlere karşı).
- Reprodüksiyon self-check (`u_stance_pipeline.py` swing u(t)'yi yeniden üretip doğrular).
- `verify()` / `fitness()` geçit fonksiyonları + G9 yapısal testi (`cl_selfcheck.py`).

### Literatüre yakınlık: birebir değil, bant
Referans makalelerden gelen değerlerle karşılaştırma yapılırken **birebir eşleşme aranmaz.**
Aranan, sonucun makul bir aralıkta kalması ve farkın gerekçelendirilebilir olmasıdır.

1. **Bant önce ilan edilir.** Her karşılaştırma için `[alt, üst]` bandı, testi yazmadan **önce**
   `07_literatur/referans_degerler.json`'a gerekçesiyle işlenir. Gerekçe, farkın kaynağını
   söyler: tür/koşul farkı (ör. kedi motonöron verisinin sıçana uygulanması), ölçüm saçılımı
   (yayımlanmış SD/aralık), model basitleştirmesi.
2. **Post-hoc bant genişletme yasaktır.** Ölçüm banda düşmüyorsa önce bant değil, **model ve
   varsayımlar** sorgulanır. Bant yine de değişecekse, eski bant/yeni bant ve gerekçesi
   `02_DOGRULAMA_KAYDI.md`'ye yazılır — sessizce genişletilmez.
3. **Her bant bir kaynağa bağlıdır.** Test, bandı `referans_degerler.json`'dan `kimlik` ile
   okur; sayı koda gömülmez. Kaynağı olmayan bant test edilmez.
4. **Assert mesajı dört şeyi basar:** ölçülen · beklenen · bant · kaynak künye. Bir test
   düştüğünde, neyin neye göre düştüğü mesajdan anlaşılmalıdır.
5. **Sonuç deftere işlenir.** Hangi büyüklüğün hangi bantta geçtiği/kaldığı
   `02_DOGRULAMA_KAYDI.md`'ye yazılır.

Yeni bilimsel çıktı → mümkünse bağımsız ikinci yöntemle çapraz kontrol; sonucu DOGRULAMA'ya işle.

## Raporlama

### Figür
- `matplotlib` **Agg** backend ile üretilir.
- Çıktı **daima** `06_sekiller/` altına yazılır — betiğin çalışma dizinine değil. (Mevcut
  `cl_teslim_9of9.py` ve `cl_emergent_teslim.py` bu kurala henüz uymuyor; İP-9'da düzeltilecek.)
- PNG, **300 dpi**.
- **Her figürün yanında onu üreten sayısal veri CSV olarak** aynı tabanla kaydedilir:
  `06_sekiller/<ad>.png` + `06_sekiller/<ad>.csv`. Amaç, figürün kaynak koda dönmeden
  yeniden üretilebilir ve denetlenebilir olmasıdır.

### Rapor
- Sonuç raporu **Markdown**: açıklayıcı metin + gömülü figür + sayısal tablo + hangi testin
  hangi bantta geçtiği.
- Sayısal sonuç/karar özetleri `.md` olarak (DOGRULAMA geleneği); oturum ilerlemesi
  `SDLC/03_GUNLUK.md`'ye.

## Proje yapısı
Numaralı Türkçe klasörler (paket değil). Tam manifesto: `../OKU.txt`. Akış/risk: `05_MIMARI_RISK.md`.
Kurulum: `06_KURULUM.md`.
