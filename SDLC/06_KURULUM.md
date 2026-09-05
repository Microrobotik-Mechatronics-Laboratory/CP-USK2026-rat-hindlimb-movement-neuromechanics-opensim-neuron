# KURULUM — Projeyi Sıfırdan Ayağa Kaldırma

> Referans dosya. Depoyu ilk kez klonlayan **buradan** başlar. Kök `README.md` yalnızca kapıdır,
> kurulumun kanonik anlatımı bu dosyadadır (aynı bilgi iki yerde tutulmaz).
>
> **Bu belgedeki her komut 2026-09-05'te bu makinede (macOS/Darwin, arm64) denenmiştir.**
> Denenmemiş hiçbir adım buraya yazılmaz.

## Ön koşullar

- **uv** (paket/ortam yöneticisi) — denenen sürüm: `uv 0.11.26`.
- **Python 3.14** ana ortam için (`.python-version` dosyası bunu sabitler).
- **Python 3.13** ikincil OpenSim ortamı için (aşağıdaki gerekçeye bakınız). `uv` gerekli
  yorumlayıcıyı kendisi indirir, ayrıca kurmanız gerekmez.

---

## ÖNEMLİ: proje iki ayrı Python ortamı ister

`opensim` PyPI'da **Python 3.14 için tekerlek yayımlamıyor**; en güncel sürüm `opensim==4.6`
yalnızca `cp311`, `cp312`, `cp313` ABI etiketleriyle geliyor. Ana ortam ise NEURON nedeniyle
3.14'tür (`neuron==9.0.2` cp314/arm64 tekerleğine sahiptir). Dolayısıyla tek bir ortamda hem
OpenSim hem NEURON **kurulamaz**.

Bu, mimarideki mevcut ayrımla zaten örtüşür (`05_MIMARI_RISK.md`): `04_kapali_dongu/` çalışma
anında OpenSim kullanmaz, saf NumPy'dir.

| Ortam | Python | Ne çalıştırır | Paketler |
|---|---|---|---|
| **Ana** (`.venv`) | 3.14 | `04_kapali_dongu/`, `inline-supplementary-material-1/` (NEURON) | neuron, numpy, sympy, mpmath, matplotlib, cma |
| **OpenSim** (`.venv-osim`) | 3.13 | `03_kod/` (ID + Statik Optimizasyon, veri üretimi) | opensim 4.6, numpy, scipy |

---

## Adım 1 — Ana ortam (Python 3.14, NEURON)

```bash
uv sync
```

`.venv/` oluşur; `pyproject.toml`'daki `neuron==9.0.2`, `numpy`, `sympy`, `mpmath`,
`find-libpython`, `packaging`, `setuptools` kurulur.

`04_kapali_dongu/` betikleri ayrıca **`matplotlib`** (figür) ve **`cma`** (CMA-ES optimizasyon)
kullanır; bunlar henüz `pyproject.toml`'da **beyan edilmemiştir** (bilinen açık: İP-5, risk-1).
Beyan edilene kadar elle:

```bash
uv pip install matplotlib cma
```

## Adım 2 — OpenSim ortamı (Python 3.13, veri üretim hattı)

Yalnızca `03_kod/` altındaki OpenSim hattını (kod_01, kod_02, u_stance_pipeline,
cop_dienes_turetme) koşacaksanız gereklidir.

```bash
uv venv --python 3.13 .venv-osim
uv pip install --python .venv-osim opensim scipy numpy
```

İlk komut şu uyarıyı basar — **beklenen davranıştır, yok sayın**: *"The requested interpreter
resolved to Python 3.13.14, which is incompatible with the project's Python requirement: >=3.14"*.
`pyproject.toml` ana ortamı tarif eder; bu ikincil ortam kasıtlı olarak onun dışındadır.

Çalıştırırken **yorumlayıcıyı doğrudan çağırın**:

```bash
./.venv-osim/bin/python 03_kod/kod_02_swing_id_so.py
```

`uv run --python .venv-osim ...` bu projede **çalışmaz**: `uv run` projenin
`requires-python = ">=3.14"` kısıtını uygular ve 3.13'ü reddeder (denendi, hata verir).

## Adım 3 — NEURON mekanizmalarını derle (İP-4a)

`inline-supplementary-material-1/fig*/` klasörlerindeki `.o` dosyaları ve `nrnmech.dll`
**Windows 64-bit için derlenmiştir; bu makinede çalışmazlar.** Her figür klasöründeki `.mod`
dosyaları yeniden derlenmelidir. `nrnivmodl` ana ortamla birlikte gelir (`.venv/bin/nrnivmodl`):

```bash
source .venv/bin/activate
cd inline-supplementary-material-1/fig2_4_6 && nrnivmodl
```

Aynısı `fig3_5_7`, `fig8`, `fig9` için tekrarlanır (her klasörün `.mod` kümesi farklıdır:
`RampIClamp`, `syn_ramp`, `SawtoothIClamp`, `mStepIClamp`, `syn_Ia_sinewave` gibi figüre özel
mekanizmalar vardır). Derleme başarılıysa klasörde platforma özgü bir çıktı dizini
(`arm64/` veya `x86_64/`) oluşur.

Modelin nasıl koşturulacağı `inline-supplementary-material-1/README.txt`'te (Kim'in orijinal
5 adımlı yönergesi) anlatılır; `dpath`, `gcalbar`, `gmax_IaSyn` ve `xm` değerleri oradan
ayarlanır.

## Adım 4 — Depo bu haliyle tam değildir (kritik)

Aşağıdaki dosyalar depoda **yoktur**, başka bir bilgisayardadır (`teslim_cc/`, bkz. `OKU.txt`).
Bunlar olmadan ilgili hat **koşmaz**:

| Eksik | Etkisi |
|---|---|
| `cl_grid3d.npz` | kapalı-döngü bunsuz hiç koşmaz |
| Güncel `cl_emergent.py`, `cl_selfcheck.py`, `cl_optimize.py` (Tsim=6, ılık başlangıç) | depodakiler eski kopyalardır |
| `cl_best.json` | son optimizasyon sonucu |
| `03_kod/rig.py` | `kod_01_rat_walk_bone_uret.py` bunu `import rig` ile çağırır; **depoda yok**, betik çalışmaz |
| `01_model/Geometry/` mesh'leri | yalnız GUI görüntüleme; hesap için gerekmez |

## Adım 5 — Kurulum doğrulama

Ana ortam:

```bash
uv run python -c "import numpy, neuron; print('numpy', numpy.__version__); print('neuron', neuron.__version__)"
```

OpenSim ortamı:

```bash
./.venv-osim/bin/python -c "import opensim, scipy; print('opensim', opensim.__version__, '| scipy', scipy.__version__)"
```

**2026-09-05'te bu makinede ölçülen çıktı:**

```
numpy 2.4.6
neuron 9.0.2
opensim 4.6 | scipy 1.18.1
```

NEURON'un bastığı `Warning: no DISPLAY environment variable. --No graphics will be displayed.`
satırı zararsızdır; grafik arayüz olmadan (batch) koşulduğunu söyler.

Hata alırsanız kurulum tamamlanmamıştır, ilerlemeyin.
