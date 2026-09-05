# GÜNLÜK — Oturum Kayıtları

> SICAK / Append-only. Her oturum en **üste** yeni bir tarihli blok eklenir. Eski kayıtlar ASLA
> düzenlenmez. Format aşağıdaki gibidir.

---

## 2026-09-05 (2. oturum) — SDLC genişletildi; NEURON derleme yolu çözüldü

**Ne yapıldı:**
- **Kapsam:** `01_PROJE.md`'ye "Kas ile NEURON arasındaki bağ" bölümü eklendi — iki aşamalı
  köprü: Aşama 1 tek motonöron doğrulaması (Kim Fig 2-9), Aşama 2 havuz ile kas arasında
  iki yönlü arayüz (NEURON çıkışı -> u(t); iğcik r(t) -> Ia sinapsı).
- **İş paketleri:** İP-4 ikiye bölündü (4a derleme+doğrulama, 4b köprü); İP-7 (literatür özüt
  defteri), İP-8 (tolerans bantlı testler), İP-9 (rapor/figür dışa aktarma) açıldı; İP-5
  genişletildi.
- **Kurallar:** literatüre-yakınlık kuralı yazıldı (bant testten önce ilan edilir, post-hoc
  genişletme yasak, assert mesajı ölçülen/beklenen/bant/künye basar); figür standardı
  (`06_sekiller/`, 300 dpi, yanında kaynak CSV) ve Markdown rapor kuralı; bağımlılık beyan kuralı.
- **Kurulum:** `SDLC/06_KURULUM.md` yazıldı ve **her adımı bu makinede denendi**. Kök `README.md`
  (0 byte'tı) kapı belgesi olarak dolduruldu.
- **Literatür:** `07_literatur/` iskeleti kuruldu (README, `oz_SABLON.md`,
  `referans_degerler.json` — 6 tohum kayıt; JSON ayrıştırma doğrulandı). PDF klasörü git-ignore'a.

**Ölçülen bulgular (hepsi denenerek):**
- `opensim` Python 3.14 için tekerlek yayımlamıyor (cp311/312/313). NEURON 3.14 gerektirdiği için
  proje **iki ortamlı** olmak zorunda: ana 3.14 (NEURON) + `.venv-osim` 3.13 (OpenSim 4.6).
  Her iki ortam da kurulup import doğrulaması yapıldı: numpy 2.4.6, neuron 9.0.2, opensim 4.6,
  scipy 1.18.1.
- `uv run --python .venv-osim ...` **çalışmıyor** (proje `requires-python >=3.14` kısıtı 3.13'ü
  reddediyor); doğrudan `./.venv-osim/bin/python` çağrılmalı.
- **Boşluklu depo yolu `nrnivmodl`'ü kırıyor:** NEURON proje içi `.venv`'e kuruluyken derleme
  `clang++: no such file or directory: 'Sıçan'` ile düşüyor. NEURON `~/.venvs/usk26`'ya
  (`UV_PROJECT_ENVIRONMENT`) alınınca **derleme proje içinde sorunsuz koşuyor** — kısıt yalnız
  NEURON'un kendi kurulum yolunda.
- `fig2_4_6`'daki 12 `.mod` dosyasının **11'i derlendi** (`Successfully created arm64/special`);
  yalnız `module1_2.mod` düşüyor: `U used as both variable and function` (satır 10 `RANGE U`,
  satır 133 `FUNCTION U (x)`). NEURON 9 `nocmodl` eski kullanımı reddediyor.
- `03_kod/rig.py` **depoda yok**; `kod_01_rat_walk_bone_uret.py` onu `import rig` ile çağırıyor,
  yani veri hattının ilk halkası bu haliyle koşmuyor (daha önce kayıtlı olmayan bulgu).

**Kararlar:**
- Testlerde ayrı çerçeve (pytest) kullanılmayacak; kod-içi assert deseni tolerans bandıyla
  genişletilecek. Bantlar `07_literatur/referans_degerler.json`'da, koda gömülmez.
- Literatür karşılaştırması birebir değil bant; bant testten **önce** gerekçesiyle ilan edilir.
- Kurulum bilgisi tek yerde (`SDLC/06_KURULUM.md`); kök README yalnız yönlendirir (drift önlemi).
- `referans_degerler.json`'da `literatur` ve `ic_olcum` kayıtları ayrı tutulur; iç ölçüm bandı
  regresyon bandıdır, literatür doğrulaması sayılmaz.

**Sonuç/artefakt:** `SDLC/06_KURULUM.md` (yeni), güncellenen `SDLC/{00_DURUM, 01_PROJE,
02_IS_PAKETLERI, 04_KURALLAR, 05_MIMARI_RISK, README}.md`, kök `README.md`,
`07_literatur/{README.md, oz_SABLON.md, referans_degerler.json}`, `.gitignore`.

**Değişen dosyalar:** yukarıdakiler. Depo dışı yan etki: `~/.venvs/usk26` (ana ortam) ve
proje içinde `.venv-osim/` (git-ignore'da) kuruldu.

**Commit:** `e89c16b` (kurulum+README), `b7a6605` (kapsam+İP), `ebadec1` (kurallar+risk),
`08d8225` (07_literatur), `e933ed1` (SDLC README), `0723706` (kurulum düzeltmesi),
`9a1a311` (NEURON derleme bulguları). Push henüz yapılmadı (onay bekliyor).

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
