# PROJE — Tanım ve Kapsam

> Referans dosya. Yalnızca projenin amacı/kapsamı/kaynakları değişince güncellenir.

## Amaç
Sıçan arka bacağı yürüyüşünün **nöromekanik modellenmesi**: OpenSim kas-iskelet modeli +
NEURON motonöron / kas iğciği / refleks modeli. Swing (salınım) ve stance (basma) fazları,
kapalı-döngü "emergent" yürüyüşün üretilmesi ve optimizasyonu.

Proje kimliği: **USK26** — "Sıçan arka bacak hareketinin OpenSim ve NEURON ile nöromekanik
modellenmesi".

## Başarı ölçütleri
- Ölçülmüş kinematikle uyumlu, moment kolları doğrulanmış bir OpenSim modeli. *(sağlandı — bkz. DOGRULAMA)*
- Swing + stance kas komutu (u) ve duyu (r) sinyal hattı. *(sağlandı)*
- Referans servo/ölçülmüş GRF kullanmadan, refleks+CPG ile ortaya çıkan (emergent) kapalı-döngü
  yürüyüş. *(teslim: 9of9)*
- NEURON motonöron modelinin bu makinede çalışır hale getirilmesi ve entegrasyonu. *(sürüyor — İP-4)*

## Klasör yapısı (özet)
Tam manifesto: **`../OKU.txt`** (kopyalanmaz, oraya bakılır).
- `01_model/` — OpenSim `.osim` modelleri + `Geometry/` kemik mesh'leri
- `02_veri/` — girdi/çıktı verileri (`.mot`, `.csv`, `.json`)
- `03_kod/` — OpenSim veri-üretim hattı (Python: opensim+numpy+scipy)
- `04_kapali_dongu/` — kapalı-döngü kontrolcü + CMA-ES optimizasyon (saf NumPy)
- `06_sekiller/` — figürler
- `inline-supplementary-material-1/` — Hojeong Kim NEURON motonöron modeli (HOC + `.mod`, 4 figür klasörü)
- `SDLC/` — bu klasör (kurumsal hafıza)

## Dış kaynaklar ve literatür
- **Johnson ve ark. 2008** (PMC2322854) — sıçan arka bacak kas mimarisi / moment kolları.
- **Blum 2020** — kas iğciği (spindle) verisi (Ia/II ateşleme modelleri).
- **Dienes 2022** — bilek momenti / CoP türetimi.
- **Lewis GRF** — zemin tepki kuvveti girdisi.
- **Hojeong Kim motonöron modeli** — PIC (Cav1.3), Ia afferent; `inline-supplementary-material-1/`.
- **SimTK taban modeli** `rat_hindlimb_0_2.osim` — köken kaydı; yayından önce **SimTK lisansı** kontrol edilmeli.

## Ortam
Python 3.14, `uv` ile yönetiliyor. Bildirilen: `neuron==9.0.2`, `numpy`, `sympy`, `mpmath`.
Kodda kullanılan ama **bildirilmeyen**: `opensim` (4.6, ayrı kuruldu), `scipy`, `matplotlib`, `cma`.
Detay/risk: `05_MIMARI_RISK.md`.
