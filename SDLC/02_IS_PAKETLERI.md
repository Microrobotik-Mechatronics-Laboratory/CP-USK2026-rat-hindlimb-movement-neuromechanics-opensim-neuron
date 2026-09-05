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

## İP-4 · NEURON motonöron modeli derleme & entegrasyon — **sürüyor**
- **Hedef:** `inline-supplementary-material-1/` modelini Darwin'de derleyip Python hattına bağlamak.
- **Sıradaki adım:** `.mod` dosyalarını `nrnivmodl` ile yeniden derle (Windows `.o`/`.dll` çalışmaz).
- **Açık soru:** Motonöron havuzu mu bağlanacak, yoksa yalnızca PIC/refleks parametreleri mi?

## İP-5 · Reprodüksiyon & bağımlılık bütünlüğü — **todo**
- **Hedef:** `opensim`/`scipy`/`matplotlib`/`cma` bağımlılıklarını beyan et; depo-dışı kritik
  dosyaların (grid, best.json, güncel cl_*) durumunu çöz; `requiremnts.txt` yazımını düzelt.

## İP-6 · Raporlama & yayın figürleri — **todo**
- **Hedef:** `06_sekiller/` figürlerinin yayına hazır hale getirilmesi; SimTK lisans kontrolü.
