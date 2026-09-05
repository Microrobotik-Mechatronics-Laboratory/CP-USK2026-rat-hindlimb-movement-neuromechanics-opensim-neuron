# GÜNLÜK — Oturum Kayıtları

> SICAK / Append-only. Her oturum en **üste** yeni bir tarihli blok eklenir. Eski kayıtlar ASLA
> düzenlenmez. Format aşağıdaki gibidir.

---

## 2026-09-05 (4. oturum) — dizin hiyerarşisi yeniden düzenlendi

**Ne yapıldı:**
- **Klasörler numarasız anlamlı adlara alındı** (kullanıcı kararı): `01_model`→`model`,
  `02_veri`→`veri`, `03_kod`→`kod/opensim`, `04_kapali_dongu`→`kod/kapali_dongu` (+ verisi
  `veri/kapali_dongu`), `06_sekiller`→`sekiller`, `07_literatur`→`literatur`,
  `inline-supplementary-material-1`→`neuron`. Tümü `git mv` ile (geçmiş korundu).
- **Kim 2020 hoc/mod ağacı dış kaynak değil, kaynak kodumuz sayıldı** (kullanıcı kararı):
  `neuron/` altında kendi ağacı oldu; nöron modelimiz bunun üzerine kurulacak.
- **`arsiv/` açıldı** (kullanıcı kararı: silme, arşivle): aşılmış kapalı-döngü hattı
  (`cl_sim2`, `cl_teslim`, `cl_emergent_teslim`, 7b/7c öncesi kopyalar), aşılmış veri kuşakları
  (`u_stance_v4`, `r_tamdongu_v3`, `ib_drive_v2`), görüntüleme `.mot`'ları, koşum logları,
  SimTK taban modeli ve Windows derlenmiş NEURON ikilileri. Her grubun gerekçesi
  `arsiv/README.md`'de.
- **İki birebir duplike düşürüldü:** `eski/cl_optimize.py` (üsttekiyle byte düzeyinde aynı) ve
  `04_kapali_dongu/cl_teslim_9of9.png` (`06_sekiller/`dekiyle aynı, md5 eşleşiyor).
- **`kod/yollar.py` eklendi:** depo-içi yolların tek kaynağı. Betikler artık çalışma dizinine
  bağlı değil; yabancı mutlak yollar (`/home/claude/oturum5/`, `/mnt/user-data/uploads/`) ve
  var olmayan `OTURUM5_YUKLE/` klasörü temizlendi. Kural `04_KURALLAR.md`'ye yazıldı.
- **Doğrulama defteri köke alındı:** `04_kapali_dongu/02_DOGRULAMA_KAYDI.md` → `DOGRULAMA.md`.
  İçeriği düzenlenmedi (tarihli tutanak); başına konum notu eklendi.
- **`OKU.txt` kaldırıldı**, içeriği `README.md`'nin klasör haritasına katlandı. İki manifesto
  drift üretiyordu ve OKU.txt zaten var olmayan dosya adları sayıyordu.
- **Bağımlılıklar beyan edildi:** `matplotlib`+`cma` → `pyproject.toml`/`uv.lock`;
  `opensim`+`scipy` → yeni `requirements-opensim.txt`. `requiremnts.txt` kaldırıldı.
- **Yol referansları projenin her yerinde güncellendi:** `SDLC/*`, `README.md`,
  `.claude/agents/*` (5 ajan tanımı klasör yapısını listeliyordu), `.gitignore`.
  `SDLC/03_GUNLUK.md` ve `DOGRULAMA.md` **tarihli kayıt oldukları için düzenlenmedi**.
  `PREPRINT.md` ve `literatur/*` paralel bir oturum tarafından güncellendi (commit `559d315`).

**Ölçülen bulgular (hepsi koşularak):**
- `cl_teslim_9of9.py` taşımadan sonra yeniden koşuldu: 24 çıktı dizisinin tamamı taşıma
  öncesiyle **birebir aynı**, PNG bayt bayt aynı. Figür artık `sekiller/` altına yazılıyor.
- `kod_02_swing_id_so.py` `.venv-osim` ile koşuldu ve `u_swing_v2.csv`'yi **sıfır sayısal
  farkla** yeniden üretti (yalnız dosyanın yorum başlığı elle zenginleştirilmiş).
- `neuron/fig2_4_6`'da `nrnivmodl` taşımadan önceki **aynı** hatayı veriyor:
  `Error: U used as both variable and function in file module1_2.mod`. Taşıma bu engeli ne
  yarattı ne çözdü — İP-4a aynen duruyor.
- Doküman yol denetimi: tüm `.md`/`.txt`/`.toml` içindeki yol benzeri token'lar diskle
  karşılaştırıldı; bilinmeyen kırık yol kalmadı (kasten var olmayanlar
  `kod/opensim/README.md` ve risk-6'da listeli).

**Düzeltilen yanlış kayıtlar (yeniden ölçülerek):**
- "`cl_grid3d.npz` ve güncel `cl_*.py` depo dışında" — **yanlış**; ikisi de depoda, kapalı
  döngü bu makinede koşuyor. `cl_best.json`'un karşılığı `cl_best_9of9.json`.
- "`rig.py` depoda yok" — kayıp değil: `git show e0192ec^:kod/rig.py` (79 satır; `e0192ec`
  "remove old folders" commit'inde eski `kod/` klasörüyle silinmiş).
- risk-2 (bildirilmeyen bağımlılıklar) ve risk-10 (`requiremnts.txt`) **kapandı**.
- `veri/kapali_dongu/cl_grid3d.npz` ve `arsiv/veri/cl_ref.npz` **yeniden üretilemez** —
  üreteçleri (`stage0_grid.py`, `gate2_ref.py`) hiç depoya girmedi; bu artık yazılı.

**Kararlar (kullanıcı):** numarasız anlamlı Türkçe klasör adları; ara ürün/eski sürüm/log
arşive taşınır, silinmez; Kim 2020 hoc/mod kaynak kodun içine alınır; bağımlılıklar beyan
edilir ve dizin değişikliği projenin her yerine işlenir.

**Sonuç/artefakt:** yeni ağaç (`model/ veri/ kod/ neuron/ sekiller/ literatur/ arsiv/ SDLC/`),
`kod/yollar.py`, `DOGRULAMA.md`, `README.md` (yeniden yazıldı), `arsiv/README.md`,
`kod/opensim/README.md`, `kod/kapali_dongu/README.md`, `requirements-opensim.txt`,
güncellenen `SDLC/{00_DURUM,01_PROJE,02_IS_PAKETLERI,04_KURALLAR,05_MIMARI_RISK,06_KURULUM,
README}.md`, `.claude/agents/*`, `.gitignore`, `pyproject.toml`, `uv.lock`.

**Değişen dosyalar:** yukarıdakiler. Bilimsel içerik (`PREPRINT.md`, `literatur/`) bu oturumda
değiştirilmedi.

**Commit:** `dce7d25` (hiyerarşi + arşiv), `fe77f26` (kapalı döngü yolları), `a706525`
(veri hattı yolları + bağımlılık), `391ed5e` (doküman yol sweep'i + yanlış kayıt düzeltmeleri),
bu günlük kaydı. Push onay bekliyor.

---

## 2026-09-05 (3. oturum) — PREPRINT yeniden kuruldu; nöron-kas mimarisi ve diyagramlar

**Ne yapıldı:**
- **`PREPRINT.md` sıfırdan yazıldı** (1056 satır, 15 bölüm) ve projenin **bilimsel tek doğruluk
  kaynağı** ilan edildi. `CLAUDE.md` buna göre güncellendi: PREPRINT bilimsel içeriğin, SDLC
  sürecin kaynağı.
- **Omurilik devresi tasarımı yazıldı:** supraspinal sürüş → CPG yarım-merkezleri → eklem başına
  örüntü katmanı → 38 motonöron havuzu → u(t) → OpenSim Hill kası → iğcik → Ia/II → geri.
  Her kutu kaynağı ve durum etiketiyle (`[ölçüldü]` / `[literatürden]` / `[tasarım]` /
  `[varsayım]`) işaretlendi.
- **`07_literatur/diyagramlar/` kuruldu:** D1 sistem, D2 omurilik devresi, D3 motonöron hücresi,
  D4 iğcik/afferent, D5 kas-iskelet, D6 havuz-kas eşleşmesi, D7 yürüyüş zamanlaması,
  D8 hat + doğrulama haritası; README'de drift kuralı (kaynak burası, PREPRINT'e kopyalanır).
- Diyagramlar PREPRINT'e gömüldü (11 blok) — Markdown editöründe okunabilir.

**Ölçülen bulgular (bu oturumda, depo verisinden):**
- 38 kasın üç eklem için moment kolları ve **işaret kararlılığı** (`cl_grid3d.npz`, referans poz
  kalça +21,7° / diz −120° / bilek 0°). Diz değerleri `02_DOGRULAMA_KAYDI.md` A bölümüyle
  tutarlı (RF +3,69 vs +3,70; VL +3,72 vs +3,73; SM −3,95 vs −3,87 — fark pozdan).
- **`GMa` modelde kalça fleksörü çıkıyor** (+5,39 mm, ızgaranın tamamında aynı işaret) —
  anatomiyle çelişki, açık soru olarak kaydedildi.
- `Pir`, `GMi`, `OE`, `Pec`, `BFa` moment kolu işaretleri kararsız (≤0,77) — işlevsel gruplara
  atanmadılar.
- Salınım fazı grup zamanlamaları (`u_swing_v2.csv`): kalça fleksör tepe %68,5 · diz ekstansör
  %66,5 · diz fleksör %76,0 · dorsifleksör %85,5 · plantar fleksör %87,0; kalça ekstansör grubu
  toplam aktivasyonu yalnız 0,883 (kalça fleksörlerinde 7,851).
- Kinematik girdi yalnız **üç eklemi** sürüyor (hip_flx, knee_flx, ankle_flx + sacrum_pitch);
  add/rot eksenleri sabit.

**Kararlar (kullanıcı):**
- NEURON tarafı preprintte **tasarım + parametre tablosu** olarak ve **hedef kapalı döngü**
  olarak yazılır; hiçbir NEURON sonucu iddia edilmez.
- **Kas başına bir motonöron havuzu** (38 kas → 38 havuz).
- Eski basma fazı / fenomenolojik emergent kapalı-döngü anlatısı **preprintten tamamen çıkarıldı**
  (dosyalar depoda duruyor, silinmedi).
- Semimembranosus için **ölçülen −3,87 mm** esas; bildirideki −4,1 mm fark olarak kayıtlı.

**Doğrulama:** 22 Mermaid bloğunun tamamı `@mermaid-js/mermaid-cli` ile derlendi (hepsi çizildi);
bildiri özeti metni git'teki önceki sürümle **birebir aynı** olduğu diff ile doğrulandı; preprintte
kapsam dışı bırakılan terimler (`stance`, `emergent`, `CMA-ES`, `9/9`) grep ile arandı, bulunmadı.

**Sonuç/artefakt:** `PREPRINT.md` (yeniden yazıldı), `07_literatur/diyagramlar/` (9 yeni dosya),
`07_literatur/README.md`, `CLAUDE.md`, `SDLC/00_DURUM.md`, bu günlük.

**Değişen dosyalar:** yukarıdakiler. Kod ve veri dosyalarına dokunulmadı.

**Commit:** bu oturumun sonunda atıldı; push onay bekliyor.

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
