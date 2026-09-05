# İŞ PAKETLERİ (WBS)

> Durum etiketleri: `todo` · `sürüyor` · `bitti` · `bloke`. İlerleme oldukça güncellenir.

## İP-1 · OpenSim iskelet-kas modeli & moment kolu doğrulaması — **bitti**
- **Hedef:** Ölçülmüş kinematikle uyumlu, moment kolları bağımsız doğrulanmış model.
- **Çıktı:** `01_model/rat_hindlimb_faz1a.osim` (hesap), `..._KASLI_x10.osim` (GUI).
- **Not:** Bağımsız doğrulama `../04_kapali_dongu/02_DOGRULAMA_KAYDI.md`'de (H1–H9 hataları dahil).

## İP-2 · Veri üretim hattı — **bitti**
- **Hedef:** Swing/stance kas komutları (u) ve tam-çevrim duyu sinyalleri (r).
- **Çıktı:** `02_veri/` içindeki `u_swing_v2.csv`, `u_stance_v4.csv`, `r_tamdongu_v3.csv`, `ib_drive_v2.csv` vb.
- **Üreten kod:** `03_kod/` (`kod_01`, `kod_02`, `u_stance_pipeline`, `cop_dienes_turetme`, `spindle_*`, `rt_ara_uret`, `r31_uret`).

## İP-3 · Kapalı-döngü nöromekanik kontrolcü — **bitti (teslim: 9of9)**
- **Hedef:** Refleks + CPG ile emergent yürüyüş; referans servo/ölçülmüş GRF yok.
- **Çıktı:** `04_kapali_dongu/cl_teslim_9of9.py`, `cl_teslim_9of9.npz`, `cl_best_9of9.json`, `cl_teslim_9of9.png`.
- **Not:** Güncel çalışan sürümler (Tsim=6, ılık başlangıç) + `cl_grid3d.npz` depo dışında (bkz. risk).

## İP-4a · NEURON motonöron modeli: derleme + tek nöron doğrulaması — **sürüyor**
- **Hedef:** Kim modelini bu makinede (Darwin/arm64) koşturmak ve yayımlanmış davranışını
  yeniden üretmek.
- **Adımlar:**
  1. `inline-supplementary-material-1/fig*/` klasörlerinde `.mod` dosyalarını `nrnivmodl` ile
     derle (mevcut `.o` / `nrnmech.dll` Windows-derlenmiş, çalışmaz). Yordam: `06_KURULUM.md` Adım 3.
  2. `motor_unit.hoc` hattını Python'dan (veya HOC'tan) koştur; GUI'siz (batch) koşum yolu kur.
  3. Fig 2-9 davranışını yeniden üret: PIC'in `dpath` / `gcalbar` bağımlılığı, Ia girdisi
     (`gmax_IaSyn`), `xm` kas boyu koşulları.
  4. Yeniden üretimi **tolerans bantlı** doğrula (İP-8 altyapısıyla); sonucu DOGRULAMA'ya işle.
- **Çıktı:** derlenmiş mekanizmalar, batch koşum betiği, doğrulama kaydı.

## İP-4b · Motonöron havuzu ile kas arasında köprü — **todo**
- **Hedef:** `01_PROJE.md`'de tanımlanan Aşama 2 arayüzünü kurmak.
- **Kapsam:**
  - **NEURON → kas:** havuz ateşlemesinden kas aktivasyon komutu **u(t)** türet (bugünkü
    `u_swing_v2.csv` / `u_stance_v4.csv` sinyalinin yerini alır).
  - **Kas → NEURON:** iğcik duyu sinyali **r(t)** (Ia/II) motonörona Ia sinapsı olarak girsin
    (`group_Ia.hoc` / `syn_Ia.mod`).
  - Zaman adımı, birim ve ölçek sözleşmesini yazılı hale getir (NEURON ms/mV/uS ile
    kapalı-döngünün s/mm/N birimleri arasındaki dönüşüm kritik noktadır).
- **Bağımlılık:** İP-4a bitmeden başlamaz.

## İP-5 · Reprodüksiyon & bağımlılık bütünlüğü — **todo**
- **Hedef:** Depoyu klonlayan birinin projeyi çalıştırabilmesi.
- **Kapsam:**
  - `matplotlib`, `cma` ana ortama; `opensim`, `scipy` OpenSim ortamına **beyan edilsin**
    (bugün hiçbiri `pyproject.toml`'da yok).
  - `03_kod/rig.py` **depoda yok** — `kod_01_rat_walk_bone_uret.py` bunsuz çalışmıyor; getirilsin.
  - Depo-dışı kritik dosyaların (`cl_grid3d.npz`, güncel `cl_*.py`, `cl_best.json`) durumu çözülsün.
  - `requiremnts.txt` yazım hatası düzeltilsin (eksik "e") veya dosya kaldırılsın.
- **Not:** Kurulum belgesi (`06_KURULUM.md`) yazıldı; bu paket belgeyi gereksiz kılacak
  düzeltmeleri yapar.

## İP-6 · Raporlama & yayın figürleri — **todo**
- **Hedef:** `06_sekiller/` figürlerinin yayına hazır hale getirilmesi; SimTK lisans kontrolü.
- **Bağımlılık:** İP-9 altyapısı kurulduktan sonra figürler o altyapıyla yeniden üretilir.

## İP-7 · Literatür özüt defteri — **todo**
- **Hedef:** Referans makalelerin materyal-metot ve sonuçlarını çıkarıp testlere kaynak yapmak.
- **Kapsam:**
  - Her makale için `07_literatur/oz_<kisa_ad>.md`: künye/DOI, tür ve deney koşulları,
    materyal-metot özeti, çıkarılan sayısal sonuçlar (değer, birim, tablo/şekil numarası),
    bizim modele uygulanabilirliği.
  - Çıkarılan her değer `07_literatur/referans_degerler.json`'a **tolerans bandı ve gerekçesiyle**
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
  - Ortak figür yardımcısı: `Agg` backend, çıktı **daima** `06_sekiller/`, PNG 300 dpi.
  - Her figürün yanında onu üreten sayısal veri aynı tabanla CSV olarak kaydedilir
    (`<ad>.png` + `<ad>.csv`).
  - Metin + gömülü figür **Markdown rapor**: sayısal tablo, hangi testin hangi bantta geçtiği.
- **Not:** Mevcut betikler figürü çalışma dizinine yazıyor (`cl_teslim_9of9.py`,
  `cl_emergent_teslim.py`); bu paket kapsamında `06_sekiller/`'e yönlendirilecek.
