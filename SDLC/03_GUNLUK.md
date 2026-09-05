# GÜNLÜK — Oturum Kayıtları

> SICAK / Append-only. Her oturum en **üste** yeni bir tarihli blok eklenir. Eski kayıtlar ASLA
> düzenlenmez. Format aşağıdaki gibidir.

---

## 2026-09-05 — SDLC kurumsal-hafıza sistemi kuruldu

**Ne yapıldı:**
- Boş `SDLC/` klasörü 7 dosyalık context sistemine dönüştürüldü: `README`, `00_DURUM`,
  `01_PROJE`, `02_IS_PAKETLERI`, `03_GUNLUK`, `04_KURALLAR`, `05_MIMARI_RISK`.
- Kök dizine `CLAUDE.md` eklendi (oturum başında `00_DURUM.md`'yi otomatik okutur).
- `logger` adında bir Claude alt-ajanı oluşturuldu (oturum-başı/kapanış protokolünü yürütür).
- `.gitignore`'a `.DS_Store` eklendi.
- Ayrıca: Claude Code status line (model · dizin · git · bağlam% · 5s/7g limit) `~/.claude` altında kuruldu.

**Kararlar:**
- Tek doğruluk kaynağı SDLC. Her oturum sadece 2 "sıcak" dosya değişir (`00_DURUM` + `03_GUNLUK`).
- `OKU.txt` ve `02_DOGRULAMA_KAYDI.md` kopyalanmadı, referans verildi (drift önlemi).
- Commit: otomatik; push: onay ile.

**Sonuç/artefakt:** `SDLC/*`, kök `CLAUDE.md`, `.claude/agents/logger.md`, `.gitignore`.

**Değişen dosyalar:** yukarıdaki yeni dosyalar + `.gitignore` + proje yapılandırması izlemeye alındı.

**Commit:** `b9dbdf5` (git hijyeni), `761d200` (proje yapılandırması), `5bedf79` (alt-ajanlar),
`1ea812d` (SDLC), `79f3565` (CLAUDE.md). Push henüz yapılmadı (onay bekliyor).

---

<!-- YENİ KAYIT ŞABLONU (kopyala, en üste yapıştır):
## YYYY-AA-GG — <kısa başlık>
**Ne yapıldı:**
- ...
**Kararlar:** ...
**Sonuç/artefakt:** ...
**Değişen dosyalar:** ...
**Commit:** <hash>
-->
