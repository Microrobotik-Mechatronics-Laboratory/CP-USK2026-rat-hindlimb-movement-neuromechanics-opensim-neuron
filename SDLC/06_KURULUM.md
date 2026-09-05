# KURULUM — Projeyi Sıfırdan Ayağa Kaldırma

> Referans dosya. Depoyu ilk kez klonlayan **buradan** başlar. Kök `README.md` yalnızca kapıdır,
> kurulumun kanonik anlatımı bu dosyadadır (aynı bilgi iki yerde tutulmaz).
>
> **Bu belgedeki her komut 2026-09-05'te bu makinede (macOS/Darwin, arm64) denenmiştir.**
> Denenmemiş hiçbir adım buraya yazılmaz; denenip **çalışmayan** yollar da "çalışmıyor" diye
> yazılmıştır.

## Ön koşullar

- **uv** (paket/ortam yöneticisi) — denenen sürüm: `uv 0.11.26`.
- **Python 3.14** ana ortam için (`.python-version` dosyası bunu sabitler).
- **Python 3.13** ikincil OpenSim ortamı için. `uv` gerekli yorumlayıcıyı kendisi indirir.
- Xcode Command Line Tools (`clang++`) — NEURON mekanizmalarını derlemek için.

---

## Bu proje iki ayrı Python ortamı ister

`opensim` PyPI'da **Python 3.14 için tekerlek yayımlamıyor**; en güncel sürüm `opensim==4.6`
yalnızca `cp311`, `cp312`, `cp313` ABI etiketleriyle geliyor. Ana ortam ise NEURON nedeniyle
3.14'tür (`neuron==9.0.2` cp314/arm64 tekerleğine sahiptir). Dolayısıyla tek bir ortamda hem
OpenSim hem NEURON **kurulamaz**.

Bu, mimarideki mevcut ayrımla zaten örtüşür (`05_MIMARI_RISK.md`): `04_kapali_dongu/` çalışma
anında OpenSim kullanmaz, saf NumPy'dir.

| Ortam | Python | Nerede | Ne çalıştırır | Paketler |
|---|---|---|---|---|
| **Ana** | 3.14 | `~/.venvs/usk26` (**proje dışı, zorunlu**) | `04_kapali_dongu/`, NEURON | neuron, numpy, sympy, mpmath, matplotlib, cma |
| **OpenSim** | 3.13 | `.venv-osim` (proje içi) | `03_kod/` (ID + SO) | opensim 4.6, numpy, scipy |

### Ana ortam neden proje klasörünün DIŞINDA olmak zorunda?

Bu deponun yolu boşluk ve Türkçe karakter içeriyor
(`.../USK26 - Sıçan arka bacak hareketinin .../Uygulama`). NEURON'un `nrnivmodl` derleyicisi,
kendi kurulu olduğu dizinin yolunu derleyiciye **tırnaklamadan** geçirir; boşluklu yolda
derleme şu hatayla düşer:

```
clang++: error: no such file or directory: 'Sıçan'
clang++: error: cannot specify -o when generating multiple output files
```

Bu yüzden NEURON **boşluksuz bir yola** kurulmalıdır. Ölçülen sonuç: NEURON boşluksuz yolda
kuruluysa, derlemenin **proje klasörü içinde** (boşluklu yolda) yapılması sorun değildir —
kısıt yalnızca NEURON'un kendi kurulum yolundadır.

---

## Adım 1 — Ana ortam (Python 3.14, NEURON)

```bash
export UV_PROJECT_ENVIRONMENT="$HOME/.venvs/usk26"
uv sync
```

`export` satırını kabuk profilinize (`~/.zshrc`) koymanız önerilir; aksi halde her yeni
terminalde tekrarlanmalıdır. Ayarlanmadığında `uv sync` ortamı proje içindeki `.venv`'e kurar
ve **NEURON derlemesi çalışmaz** (yukarıdaki gerekçe).

`04_kapali_dongu/` betikleri ayrıca **`matplotlib`** (figür) ve **`cma`** (CMA-ES) kullanır;
bunlar henüz `pyproject.toml`'da **beyan edilmemiştir** (bilinen açık: İP-5, risk-2). Beyan
edilene kadar elle:

```bash
uv pip install matplotlib cma
```

## Adım 2 — OpenSim ortamı (Python 3.13, veri üretim hattı)

Yalnızca `03_kod/` altındaki OpenSim hattını koşacaksanız gereklidir.

```bash
uv venv --python 3.13 .venv-osim
uv pip install --python .venv-osim opensim scipy numpy
```

İlk komut şu uyarıyı basar — **beklenen davranıştır, yok sayın**: *"The requested interpreter
resolved to Python 3.13.14, which is incompatible with the project's Python requirement:
>=3.14"*. `pyproject.toml` ana ortamı tarif eder; bu ikincil ortam kasıtlı olarak onun dışındadır.

Çalıştırırken **yorumlayıcıyı doğrudan çağırın**:

```bash
./.venv-osim/bin/python 03_kod/kod_02_swing_id_so.py
```

`uv run --python .venv-osim ...` bu projede **çalışmaz**: `uv run` projenin
`requires-python = ">=3.14"` kısıtını uygular ve 3.13'ü reddeder (denendi, hata verir).

## Adım 3 — NEURON mekanizmalarını derle (İP-4a)

`inline-supplementary-material-1/fig*/` klasörlerindeki `.o` dosyaları ve `nrnmech.dll`
**Windows 64-bit için derlenmiştir; bu makinede çalışmazlar.** Her figür klasöründeki `.mod`
dosyaları yeniden derlenmelidir:

```bash
export PATH="$HOME/.venvs/usk26/bin:$PATH"
cd inline-supplementary-material-1/fig2_4_6 && nrnivmodl
```

Başarılıysa klasörde `arm64/` dizini ve `arm64/special` yürütülebiliri oluşur. Aynısı
`fig3_5_7`, `fig8`, `fig9` için tekrarlanır (her klasörün `.mod` kümesi farklıdır:
`RampIClamp`, `syn_ramp`, `SawtoothIClamp`, `mStepIClamp`, `syn_Ia_sinewave` gibi figüre özel
mekanizmalar vardır).

### Bilinen engel: `module1_2.mod` NEURON 9 ile derlenmiyor

`fig2_4_6` klasöründeki 12 `.mod` dosyasından **11'i sorunsuz derleniyor**; yalnız
`module1_2.mod` düşüyor:

```
Error: U used as both variable and function in file module1_2.mod
```

Sebep: dosya `U` adını hem `RANGE` değişkeni olarak ilan ediyor (satır 10) hem de
`FUNCTION U (x)` olarak tanımlıyor (satır 133). Eski NEURON (modelin yazıldığı 7.x) buna izin
veriyordu, **NEURON 9'un `nocmodl` çevirici**si vermiyor. `U`, sarkoplazmik retikulum kalsiyum
pompası akısını hesaplar; `module1_2.mod` kas kasılma modülüdür, yani atlanabilir değildir.

**Durum:** açık. Düzeltme İP-4a kapsamındadır (`RANGE` listesinden `U`'yu çıkarmak ilk
denenecek yoldur, ancak HOC tarafının `U`'ya erişip erişmediği kontrol edilmelidir).
Doğrulama: `module1_2.mod` geçici olarak dışarı alındığında kalan 11 dosya derlenip
`Successfully created arm64/special` çıktısı alınmıştır.

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

```bash
$HOME/.venvs/usk26/bin/python -c "import numpy, neuron; print('numpy', numpy.__version__); print('neuron', neuron.__version__)"
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
