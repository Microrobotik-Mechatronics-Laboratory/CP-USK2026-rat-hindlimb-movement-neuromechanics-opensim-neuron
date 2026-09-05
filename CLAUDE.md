# CLAUDE.md

Bu, sıçan arka bacak nöromekanik modelleme projesidir (OpenSim + NEURON).

## Oturuma başlarken (ZORUNLU)

Bu projede herhangi bir işe başlamadan **önce şu sırayla oku**:

1. `SDLC/00_DURUM.md` — projenin anlık durumu, sıradaki adım.
2. `SDLC/03_GUNLUK.md` — **son kayıt** (geçen oturumda ne yapıldı).
3. `PREPRINT.md` — **projenin bilimsel tek doğruluk kaynağı**: ne yapmaya çalıştığımız, model
   yapısı (kas-iskelet + omurilik devresi), doğrulanmış sayılar ve açık sorular. "Projemiz ne?"
   sorusunun cevabı burasıdır; `SDLC/` ise sürecin (durum, iş paketi, kural) kaynağıdır.
4. Sonra `SDLC/README.md`'deki **Oturum-Başı ve Oturum-Kapanış protokollerini** izle.

İki doğruluk kaynağı vardır ve karıştırılmaz:
- **`PREPRINT.md` — bilimsel içerik:** amaç, model yapısı, yöntem, sayılar, iddialar, farklar.
  Bir bilimsel iddia değişecekse **önce burada** değişir. Kullanıcı burayı elle düzeltir.
- **`SDLC/` — süreç:** durum, iş paketleri, kurallar (git/dokümantasyon/yorum/test/raporlama),
  mimari ve riskler.

Okuduktan sonra kullanıcıya 2-3 satır durum özeti ver ve çalışmaya hazır ol — ekstra soru sorma.

## Oturumu kapatırken

`SDLC/README.md`'deki **Oturum-Kapanış Protokolü**'nü uygula: `00_DURUM.md` ve `03_GUNLUK.md`'yi
güncelle, gerekirse `02_IS_PAKETLERI.md`'yi güncelle, sonra otomatik commit (push için onay sor).
Bu adımları `logger` alt-ajanı da yürütebilir.

## Kurallar
Git commit biçimi, kod/yorum/test/raporlama kuralları: `SDLC/04_KURALLAR.md`. Bunlara uy.
