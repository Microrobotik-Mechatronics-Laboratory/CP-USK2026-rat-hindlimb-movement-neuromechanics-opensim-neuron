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
- **Hijyen:** `.DS_Store` git-ignore'da; commit'e girmemeli.
- Ana dal `main`, `origin`'i takip eder (herkese açık lab reposu).

## Dokümantasyon
- Her `.py` betiği başında **Türkçe sağlayıcı/provenance başlığı**: ne ürettiği, girdisi/çıktısı,
  hangi kaynaktan/önceki adımdan türediği (mevcut `03_kod` deseni).
- Bilimsel iddialar **bağımsız yeniden ölçülür**; `02_DOGRULAMA_KAYDI.md` tarzı doğrulama defteri
  tutulur. Devir belgelerinden taşınan sayı, yeniden ölçülene kadar "doğrulanmamış" sayılır.
- Proje durumu/tarihçe her zaman `SDLC/`'ye yazılır.

## Satır-içi yorumlar
- Dil **Türkçe**. Yorumlar "**neden**"i açıklar, "ne"yi değil.
- Çevredeki kodun stiline uy: yoğunluk, adlandırma, deyim (idiom). Yeni desen icat etme.
- Kritik/kaygan yerleri işaretle (ör. entegrasyon adımı, saturasyon sabiti, birim dönüşümü).
- **Emoji yok** — kod, yorum, dokümantasyon ve commit dahil projenin hiçbir yerinde.

## Test / doğrulama
- Ayrı test çerçevesi (pytest) **yok**; doğrulama kod içinde:
  - `assert`'ler (ör. `r31_uret.py` bilinen referans değerlere karşı).
  - Reprodüksiyon self-check (`u_stance_pipeline.py` swing u(t)'yi yeniden üretip doğrular).
  - `verify()` / `fitness()` geçit fonksiyonları + G9 yapısal testi (`cl_selfcheck.py`).
- Yeni bilimsel çıktı → mümkünse bağımsız ikinci yöntemle çapraz kontrol; sonucu DOGRULAMA'ya işle.

## Raporlama
- Figürler `matplotlib` **Agg** backend ile üretilir, `06_sekiller/`'e kaydedilir.
- Sayısal sonuç/karar özetleri `.md` olarak (DOGRULAMA geleneği); oturum ilerlemesi `SDLC/03_GUNLUK.md`'ye.

## Proje yapısı
Numaralı Türkçe klasörler (paket değil). Tam manifesto: `../OKU.txt`. Akış/risk: `05_MIMARI_RISK.md`.
