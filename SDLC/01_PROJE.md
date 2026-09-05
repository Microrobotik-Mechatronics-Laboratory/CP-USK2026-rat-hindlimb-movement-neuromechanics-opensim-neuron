# PROJE — Tanım ve Kapsam

> Referans dosya. Yalnızca projenin amacı/kapsamı/kaynakları değişince güncellenir.

## Amaç
Sıçan arka bacağı yürüyüşünün **nöromekanik modellenmesi**: OpenSim kas-iskelet modeli +
NEURON motonöron / kas iğciği / refleks modeli. Swing (salınım) ve stance (basma) fazları,
kapalı-döngü "emergent" yürüyüşün üretilmesi ve optimizasyonu.

Proje kimliği: **USK26** — "Sıçan arka bacak hareketinin OpenSim ve NEURON ile nöromekanik
modellenmesi".

## Kas ile NEURON arasındaki bağ (projenin çekirdeği)

Bugün iki taraf **ayrıktır**: Python/OpenSim tarafı (`kod/opensim`, `kod/kapali_dongu`) refleksi
fenomenolojik kazançlarla temsil eder; NEURON tarafı (`neuron`) ise
biyofiziksel motonöronu ayrı bir ada olarak barındırır. Projenin asıl hedefi bu sınırı
kapatmaktır. Bağlantı **iki aşamada** kurulur:

**Aşama 1 — NEURON tarafı tek başına doğrulanır (İP-4a).**
`.mod` mekanizmaları bu makinede derlenir; Kim modelinin yayımlanmış davranışı (Fig 2-9)
yeniden üretilir: Cav1.3 aracılı PIC'in `dpath` (kanal yerleşimi) ve `gcalbar` (tepe iletkenlik)
bağımlılığı, Ia sinaptik girdinin (`gmax_IaSyn`) etkisi, `xm` ile temsil edilen kas boyu
durumları. Yeniden üretim başarısı **tolerans bandıyla** ölçülür (bkz. `04_KURALLAR.md`).

**Aşama 2 — Motonöron havuzu ile kas arasında köprü (İP-4b).**
İki yönlü arayüz:
- **NEURON → kas:** motonöron havuzunun ateşleme çıktısı, OpenSim/kapalı-döngü kasının
  aktivasyon komutu **u(t)** olarak kullanılır (bugün `veri/u_swing_v2.csv` ile temsil edilen
  sinyalin yerini alır; basma fazı kapsam dışıdır, `arsiv/veri/u_stance_v4.csv`).
- **Kas → NEURON:** kas iğciğinden türetilen duyu sinyali **r(t)** (Ia/II ateşleme oranları,
  `arsiv/veri/r_tamdongu_v3.csv`; resmî biçim v3.1'dir, `kod/opensim/r31_uret.py` üretir)
  motonörona Ia sinapsı olarak girer (`neuron/fig2_4_6/group_Ia.hoc` / `syn_Ia.mod` arayüzü).

Böylece refleks döngüsü fenomenolojik kazanç yerine biyofiziksel motonöron dinamiği üzerinden
kapanır.

## Başarı ölçütleri
- Ölçülmüş kinematikle uyumlu, moment kolları doğrulanmış bir OpenSim modeli. *(sağlandı — bkz. DOGRULAMA)*
- Swing + stance kas komutu (u) ve duyu (r) sinyal hattı. *(sağlandı)*
- Referans servo/ölçülmüş GRF kullanmadan, refleks+CPG ile ortaya çıkan (emergent) kapalı-döngü
  yürüyüş. *(teslim: 9of9)*
- **Aşama 1:** NEURON motonöron modeli bu makinede koşar ve Kim Fig 2-9 davranışını tolerans
  bandı içinde yeniden üretir. *(sürüyor — İP-4a)*
- **Aşama 2:** motonöron havuzu ile kas arasında iki yönlü köprü (u çıkışı, r girişi) kurulur.
  *(İP-4b)*
- **Literatüre yakınlık:** üretilen sayısal sonuçlar, referans makalelerden çıkarılan değerlerin
  **önceden ilan edilmiş tolerans bandında** kalır. Birebir örtüşme aranmaz; aranan, farkın
  gerekçelendirilebilir olmasıdır. Kural: `04_KURALLAR.md`; değerler:
  `literatur/referans_degerler.json`.

## Klasör yapısı (özet)
Tam manifesto: **`../README.md`** klasör haritası (kopyalanmaz, oraya bakılır).
- `model/` — OpenSim `.osim` modelleri + `Geometry/` kemik mesh'leri
- `veri/` — girdi/çıktı verileri (`.mot`, `.csv`, `.json`)
- `kod/opensim/` — OpenSim veri-üretim hattı (Python: opensim+numpy+scipy)
- `kod/kapali_dongu/` — kapalı-döngü kontrolcü + CMA-ES optimizasyon (saf NumPy)
- `sekiller/` — yayın figürleri; her figürün yanında onu üreten kaynak CSV
- `literatur/` — referans makale özütleri + testlerin okuduğu `referans_degerler.json`
- `neuron/` — Hojeong Kim NEURON motonöron modeli (HOC + `.mod`, 4 figür klasörü)
- `SDLC/` — bu klasör (kurumsal hafıza)

## Dış kaynaklar ve literatür
Künyeler ve bunlardan çıkarılan **sayısal referans değerler + tolerans bantları** makine-okunur
biçimde `literatur/referans_degerler.json`'da tutulur; makale başına materyal-metot/sonuç
özütü `literatur/oz_*.md` dosyalarındadır. Aşağıdaki liste yalnızca kaynakların rolünü
gösterir:

- **Johnson ve ark. 2008** (PMC2322854) — sıçan arka bacak kas mimarisi / moment kolları.
- **Blum 2020** — kas iğciği (spindle) verisi (Ia/II ateşleme modelleri).
- **Dienes 2022** — bilek momenti / CoP türetimi.
- **Lewis GRF** — zemin tepki kuvveti girdisi.
- **Hojeong Kim motonöron modeli** — PIC (Cav1.3), Ia afferent; `neuron/`.
- **SimTK taban modeli** `arsiv/model/rat_hindlimb_0_2.osim` — köken kaydı (hesapta kullanılmaz);
  yayından önce **SimTK lisansı** kontrol edilmeli.

## Ortam
**Proje iki ayrı Python ortamı gerektirir**: `opensim` Python 3.14 için tekerlek yayımlamadığından
(yalnız cp311/312/313), NEURON'un 3.14 ana ortamıyla aynı yere kurulamaz. Ana ortam (3.14):
NEURON + NumPy + matplotlib + cma. İkincil ortam (3.13): OpenSim + SciPy, yalnız `kod/opensim/` için.
Kurulumun tamamı: **`06_KURULUM.md`**.

Bildirilen (pyproject): `neuron==9.0.2`, `numpy`, `sympy`, `mpmath`.
Kodda kullanılan ama **bildirilmeyen**: `opensim` (4.6), `scipy`, `matplotlib`, `cma` — İP-5.
Detay/risk: `05_MIMARI_RISK.md`.
