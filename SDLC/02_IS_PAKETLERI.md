# İŞ PAKETLERİ (WBS)

> Durum etiketleri: `todo` · `sürüyor` · `bitti` · `bloke`. İlerleme oldukça güncellenir.

## İP-1 · OpenSim iskelet-kas modeli & moment kolu doğrulaması — **bitti**
- **Hedef:** Ölçülmüş kinematikle uyumlu, moment kolları bağımsız doğrulanmış model.
- **Çıktı:** `model/rat_hindlimb_faz1a.osim` (hesap), `model/rat_hindlimb_KASLI_x10.osim` (GUI).
- **Not:** Bağımsız doğrulama `../DOGRULAMA.md`'de (H1–H9 hataları dahil).

## İP-2 · Veri üretim hattı — **bitti**
- **Hedef:** Swing/stance kas komutları (u) ve tam-çevrim duyu sinyalleri (r).
- **Çıktı:** `veri/u_swing_v2.csv` (güncel). Aşılmış kuşaklar arşivde: `arsiv/veri/u_stance_v4.csv`
  (v5 ile), `arsiv/veri/r_tamdongu_v3.csv` (v3.1 ile), `arsiv/veri/ib_drive_v2.csv` (v3 ile) —
  gerekçeler `arsiv/README.md`'de.
- **Üreten kod:** `kod/opensim/` (`kod_01`, `kod_02`, `u_stance_pipeline`, `cop_dienes_turetme`, `spindle_*`, `rt_ara_uret`, `r31_uret`).

## İP-3 · Kapalı-döngü nöromekanik kontrolcü — **bitti (teslim: 9of9)**
- **Hedef:** Refleks + CPG ile emergent yürüyüş; referans servo/ölçülmüş GRF yok.
- **Çıktı:** `kod/kapali_dongu/cl_teslim_9of9.py` → `veri/kapali_dongu/cl_teslim_9of9.npz` +
  `sekiller/cl_teslim_9of9.png`; parametre `veri/kapali_dongu/cl_best_9of9.json`.
- **Not (2026-09-05 düzeltmesi):** "güncel sürümler depo dışında" kaydı **yanlıştı**; güncel
  `cl_*.py` ve `cl_grid3d.npz` depodadır. Teslim koşusu bu makinede yeniden koşuldu ve 24 çıktı
  dizisinin tamamı birebir aynı çıktı. 7b/7c öncesi kopyalar `arsiv/kod/` altındadır.

## İP-4a · NEURON motonöron modeli: derleme + tek nöron doğrulaması — **sürüyor**
- **Hedef:** Kim modelini bu makinede (Darwin/arm64) koşturmak ve yayımlanmış davranışını
  yeniden üretmek.
- **Adımlar:**
  1. ~~Derleme yolunu kur~~ **çözüldü (2026-09-05):** `nrnivmodl` boşluklu proje yolunda kurulu
     NEURON ile çalışmıyordu; NEURON `~/.venvs/usk26` altına (boşluksuz yola) alınınca derleme
     proje içinde sorunsuz koşuyor. Yordam: `06_KURULUM.md` Adım 1 ve 3.
  2. **`module1_2.mod` NEURON 9 ile derlenmiyor — açık engel.** `fig2_4_6`'daki 12 `.mod`
     dosyasının 11'i derleniyor (`Successfully created arm64/special` alındı), yalnız bu düşüyor:
     `Error: U used as both variable and function`. `U` hem `RANGE` değişkeni (satır 10) hem
     `FUNCTION U (x)` (satır 133) olarak tanımlı; eski NEURON izin veriyordu, 9'un `nocmodl`'ü
     vermiyor. `U` sarkoplazmik retikulum kalsiyum pompası akısıdır, `module1_2.mod` kas kasılma
     modülüdür — atlanamaz. İlk denenecek düzeltme: `RANGE` listesinden `U`'yu çıkarmak; önce
     HOC tarafının `U`'ya erişip erişmediği kontrol edilmeli.
  3. Kalan üç klasörü (`fig3_5_7`, `fig8`, `fig9`) derle; figüre özel mekanizmalarda
     (`syn_ramp`, `SawtoothIClamp`, `mStepIClamp`, `syn_Ia_sinewave`) benzer NEURON 9
     uyumsuzluğu olup olmadığını gör.
  4. `motor_unit.hoc` hattını Python'dan (veya HOC'tan) koştur; GUI'siz (batch) koşum yolu kur.
  5. Fig 2-9 davranışını yeniden üret: PIC'in `dpath` / `gcalbar` bağımlılığı, Ia girdisi
     (`gmax_IaSyn`), `xm` kas boyu koşulları.
  6. Yeniden üretimi **tolerans bantlı** doğrula (İP-8 altyapısıyla); sonucu DOGRULAMA'ya işle.
- **Çıktı:** derlenmiş mekanizmalar, batch koşum betiği, doğrulama kaydı.
- **Sıradaki somut adım:** `module1_2.mod`'daki `U` çakışmasını çöz.

## İP-4b · Motonöron havuzu ile kas arasında köprü — **todo**
- **Hedef:** `01_PROJE.md`'de tanımlanan Aşama 2 arayüzünü kurmak.
- **Kapsam:**
  - **NEURON → kas:** havuz ateşlemesinden kas aktivasyon komutu **u(t)** türet (bugünkü
    `veri/u_swing_v2.csv` sinyalinin yerini alır; basma fazı kapsam dışı).
  - **Kas → NEURON:** iğcik duyu sinyali **r(t)** (Ia/II) motonörona Ia sinapsı olarak girsin
    (`neuron/fig2_4_6/group_Ia.hoc` / `syn_Ia.mod`).
  - Zaman adımı, birim ve ölçek sözleşmesini yazılı hale getir (NEURON ms/mV/uS ile
    kapalı-döngünün s/mm/N birimleri arasındaki dönüşüm kritik noktadır).
- **Bağımlılık:** İP-4a bitmeden başlamaz.

## İP-5 · Reprodüksiyon & bağımlılık bütünlüğü — **sürüyor**
- **Hedef:** Depoyu klonlayan birinin projeyi çalıştırabilmesi.
- **Bitti (2026-09-05):**
  - ~~`matplotlib`, `cma` ana ortama; `opensim`, `scipy` OpenSim ortamına beyan edilsin~~ →
    `pyproject.toml` + `uv.lock` ve `requirements-opensim.txt`.
  - ~~`requiremnts.txt` yazım hatası~~ → dosya kaldırıldı (pyproject ile birebir aynıydı).
  - ~~Depo-dışı kritik dosyaların durumu çözülsün~~ → yeniden ölçüldü: `cl_grid3d.npz`, güncel
    `cl_*.py` ve `cl_best_9of9.json` **depodadır**; kayıt yanlıştı. Kapalı döngü koşuyor.
  - Betiklerin çalışma dizinine bağlılığı kaldırıldı (`kod/yollar.py`); OpenSim hattı
    `u_swing_v2.csv`'yi sıfır farkla yeniden üretti.
- **Kalan:**
  - `kod/opensim/rig.py` getirilsin — **git geçmişinde duruyor:** `git show e0192ec^:kod/rig.py`.
    Getirildikten sonra `kod_01_rat_walk_bone_uret.py` gerçekten koşuyor mu denenmeli
    (iki `bauman_fig4_*.csv` girdisi de eksik).
  - Kalan eksik girdiler ve biçim uyuşmazlıkları: `kod/opensim/README.md` tablosu.
  - `veri/kapali_dongu/cl_grid3d.npz` ve `arsiv/veri/cl_ref.npz` yeniden üretilemez (üreteçleri `stage0_grid.py`,
    `gate2_ref.py` hiç depoya girmedi) — bunlar getirilsin ya da durum kabul edilip yazılsın.

## İP-6 · Raporlama & yayın figürleri — **todo**
- **Hedef:** `sekiller/` figürlerinin yayına hazır hale getirilmesi; SimTK lisans kontrolü.
- **Bağımlılık:** İP-9 altyapısı kurulduktan sonra figürler o altyapıyla yeniden üretilir.

## İP-7 · Literatür özeti defteri — **todo**
- **Hedef:** Referans makalelerin materyal-metot ve sonuçlarını çıkarıp testlere kaynak yapmak.
- **Kapsam:**
  - Her makale için `literatur/oz_<kisa_ad>.md`: künye/DOI, tür ve deney koşulları,
    materyal-metot özeti, çıkarılan sayısal sonuçlar (değer, birim, tablo/şekil numarası),
    bizim modele uygulanabilirliği.
  - Çıkarılan her değer `literatur/referans_degerler.json`'a **tolerans bandı ve gerekçesiyle**
    işlenir.
- **Kaynak sırası:** Kim (motonöron/PIC/Ia) → Johnson 2008 (moment kolu/mimari) → Blum 2020
  (iğcik) → Dienes 2022 (bilek momenti/CoP) → Lewis (GRF).

## İP-8 · Literatüre-yakınlık doğrulama testleri — **todo**
- **Hedef:** Sonuçların literatür bandında kaldığını kod içinde denetlemek.
- **Kapsam:** `referans_degerler.json`'u okuyup ölçülen değeri banda karşı sınayan ortak yardımcı;
  mevcut kod-içi `assert` deseninin genişletilmiş hali (ayrı test çerçevesi kullanılmaz).
  Assert mesajı ölçülen · beklenen · bant · kaynak künyeyi basar. Kural: `04_KURALLAR.md`.
- **Bağımlılık:** İP-7 ile birlikte yürür (band olmadan test yazılmaz).

## İP-9 · Rapor ve figür dışa aktarma altyapısı — **todo**
- **Hedef:** Sonuçları tek komutla dışarı aktarabilmek.
- **Kapsam:**
  - Ortak figür yardımcısı: `Agg` backend, çıktı **daima** `sekiller/`, PNG 300 dpi.
  - Her figürün yanında onu üreten sayısal veri aynı tabanla CSV olarak kaydedilir
    (`<ad>.png` + `<ad>.csv`).
  - Metin + gömülü figür **Markdown rapor**: sayısal tablo, hangi testin hangi bantta geçtiği.
- **Not:** ~~Mevcut betikler figürü çalışma dizinine yazıyor~~ — `cl_teslim_9of9.py` artık
  `sekiller/` altına yazıyor (2026-09-05). Kalan: 300 dpi ve figür yanında kaynak CSV.
  `arsiv/kod/cl_emergent_teslim.py` arşive alındı, bu paketin kapsamında değil.
