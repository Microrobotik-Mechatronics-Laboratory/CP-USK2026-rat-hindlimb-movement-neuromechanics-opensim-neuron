# Rat Hindlimb Neuromechanics — OpenSim + NEURON

Closed-loop neuromechanical model of rat hindlimb locomotion.

[English](#english) · [Türkçe](#türkçe)

---

## English

### What this is

This repository builds, *in silico*, the closed loop that runs from the spinal cord to the muscle
and back in the hindlimb of a Sprague-Dawley rat. **OpenSim** carries the mechanics — a
musculoskeletal model of the limb. **NEURON** carries the neural command — motoneurons and the
spinal circuitry above them. The loop closes on itself: motoneuron pools drive the muscles, the
resulting movement stretches the muscle spindles, and the Ia/II afferent signal renews the command.
The longer-term motivation is a substrate for developing neuroprostheses after spinal cord injury.

Where the work stands today: the musculoskeletal half is built and swing-phase muscle activations
have been solved; the motoneuron cell is built in Python and matches the reference HOC
implementation bit-for-bit; NEURON and OpenSim have been shown to run inside one Python process.
Wiring the full 38-pool spinal circuit is the step in progress.

`PREPRINT.md` is the scientific source of truth (method, numbers, claims, open questions).
`DOGRULAMA.md` is the measurement log — what was verified, when, and what was not.

### Requirements

- **macOS / Darwin arm64** — the platform every command below was actually run on
- **uv** >= 0.11.26
- **Xcode Command Line Tools** (`clang++`) — needed by `nrnivmodl`
- Python **3.14** and **3.13** — uv downloads both itself

### Installation

**Three environments are needed, not one.** `opensim==4.6` publishes no Python 3.14 wheel
(cp311/cp312/cp313 only), while the main environment must be 3.14 for `neuron==9.0.2`. The two
cannot share one environment. The *bridge* environment is their common denominator, Python 3.13,
where NEURON and OpenSim are importable in the same process.

| Environment | Python | Location | Runs |
|---|---|---|---|
| Main | 3.14 | `~/.venvs/usk26` (outside the project) | `kod/kapali_dongu/` |
| OpenSim | 3.13 | `.venv-osim` (inside the project) | `kod/opensim/` |
| Bridge | 3.13 | `~/.venvs/usk26-kopru` (outside the project) | `kod/kopru/`, `nrnivmodl`, NEURON |

**Two path constraints** follow from this repository's own directory name containing spaces and
Turkish characters:

1. **NEURON must be installed under a space-free path.** `nrnivmodl` passes the install directory
   to the compiler *unquoted*, so a space breaks the build. This is why the main and bridge
   environments live in `~/.venvs`. Compiling *inside* the project is fine — the constraint is only
   on NEURON's own install path.
2. **Every path handed to NEURON must be relative and ASCII.** The HOC string interface rejects
   non-ASCII characters (`python string arg cannot decode into c_str`). The Python side positions
   itself with `os.chdir()` and passes bare relative names to `load_file` / `xopen`.

```bash
# 1) Main environment (Python 3.14, NEURON + closed loop)
export UV_PROJECT_ENVIRONMENT="$HOME/.venvs/usk26"     # add this line to ~/.zshrc as well
uv sync

# 2) OpenSim environment (Python 3.13)
uv venv --python 3.13 .venv-osim
uv pip install --python .venv-osim -r requirements-opensim.txt

# 3) Bridge environment (Python 3.13, NEURON + OpenSim in one process)
uv venv --python 3.13 "$HOME/.venvs/usk26-kopru"
uv pip install --python "$HOME/.venvs/usk26-kopru" -r requirements-kopru.txt

# 4) Compile the NEURON mechanisms (each figure folder has its own .mod set)
export PATH="$HOME/.venvs/usk26-kopru/bin:$PATH"
for d in fig2_4_6 fig3_5_7 fig8 fig9; do (cd "neuron/$d" && nrnivmodl); done

# 5) Verify the installation
$HOME/.venvs/usk26/bin/python -c "import numpy, neuron; print(numpy.__version__, neuron.__version__)"
./.venv-osim/bin/python -c "import opensim, scipy; print(opensim.__version__, scipy.__version__)"
$HOME/.venvs/usk26-kopru/bin/python -c "import neuron, opensim; print('bridge ok')"
```

Expected output of step 5 on the reference machine: `2.4.6 9.0.2` · `4.6 1.18.1` · `bridge ok`.
Each `nrnivmodl` should end with `Successfully created arm64/special`; all four folders compile
(12 mechanisms in total). Two harmless messages: `uv venv --python 3.13` warns that 3.13 is
incompatible with `requires-python = ">=3.14"`, and NEURON warns about a missing `DISPLAY`.

Note: `uv run --python .venv-osim ...` does **not** work here — the project's `requires-python`
constraint rejects 3.13. Call the interpreter directly, as shown below.

### Running

```bash
# Inverse dynamics + static optimization -> veri/u_swing_v2.csv
./.venv-osim/bin/python kod/opensim/kod_02_swing_id_so.py

# Closed-loop delivery run -> sekiller/ + veri/kapali_dongu/
$HOME/.venvs/usk26/bin/python kod/kapali_dongu/cl_teslim_9of9.py

# Motoneuron cross-check: Python build vs HOC build, same process, same stimulus
$HOME/.venvs/usk26-kopru/bin/python kod/kopru/capraz_kontrol.py
```

`kod/kapali_dongu/cl_optimize.py` runs the CMA-ES parameter search (~6-7 hours). The closed-loop
integrator **requires `dt = 2e-5`**: the ankle DOF inertia is about 1/120 of the hip's, and explicit
Euler at `dt = 1e-4` is unstable for that stiff DOF — the artefact is numerical, not a control
failure (`DOGRULAMA.md` §K.2).

### What the model does

**Musculoskeletal side (OpenSim).** Geometry from Johnson et al. 2008. Five segments (spine,
pelvis, femur, tibia, foot), 14 coordinates of which 7 are the leg axes, and 38 muscles, all
`Thelen2003Muscle` with a rigid tendon. The input kinematics `veri/rat_walk_bone_smooth.mot` is a
measured bone-frame gait cycle: 201 samples, T = 0.387 s. We solve the **swing phase**, deliberately:
the foot is off the ground, so no ground reaction force is required. The chain is inverse dynamics
(muscle forces excluded, 15 Hz low-pass) → the moment-arm matrix `R(q)`, 7 DOF × 38 muscles →
static optimization `min Σa² + 1e6·Σr²` subject to `R·F(a) + R·F_passive + r = τ_ID` → the muscle
commands `veri/u_swing_v2.csv`, 38 muscles × 71 samples over 65-100 % of the gait cycle.

**Spinal side (NEURON).** The cell is the Kim 2020 motoneuron: 311 dendritic compartments, soma
channels Naf/KDr/CaN/KCa/Nap, an axon hillock and initial segment where the action potential is
born, and a Cav1.3 persistent-inward-current hot-spot at `D_path = 600 µm` with
`gcalbar = 1.37 mS/cm²`. Ia synapses sit on the soma and on dendrites with `D_path < 1400 µm`.
Above the cell sits the planned circuit: tonic supraspinal drive → a CPG half-centre pair
(Yu & Thomas 2021 architecture) → a pattern-formation layer per joint → **38 motoneuron pools, one
per muscle**, with reciprocal (IaIN) and recurrent (Renshaw) interneurons. Pools are assigned to
flexor/extensor groups from the sign of the moment arm.

**The closed loop.** Both simulators are advanced in a single Python control loop, in one process,
with the same time step (dt = 0.025 ms):

```
1. advance NEURON one step
2. read motoneuron pool spikes            -> u(t)     dimensionless 0-1
3. write u(t) into OpenSim muscle activations
4. advance OpenSim one step
5. read muscle-tendon lengths and velocities -> l_mt, v_mt   (mm, mm/s)
6. compute spindle firing r(t) and apply the afferent delay  (Ia 1.5 ms, II 1.8 ms)
7. write r(t) into the Ia synaptic conductance -> gmax_IaSyn
```

The spindle transfer is fitted from Blum 2020:
`Ia = max(0, 10.43 + 26.59·d + 27.08·max(v,0)^0.532)`.
One architectural rule is absolute: **muscle dynamics live in OpenSim.** Kim's own `muscle_unit`
compartment is used only for stage-1 replication and is disabled in the closed loop, otherwise
force would be generated twice.

### Verified numbers

| Result | Value |
|---|---|
| Quadriceps knee moment arm (knee −120°) | RF +3.70 · VL +3.73 · VI +3.72 · VM +3.70 mm |
| Semimembranosus knee moment arm | −3.87 mm |
| Sign convention | extensor positive, flexor negative — confirmed by two independent methods |
| Swing activation peaks | hip flexors 68.5 % · knee flexors 76.0 % · ankle dorsiflexors 85.5 % of the cycle |
| `kod_02_swing_id_so.py` re-run | reproduces `u_swing_v2.csv` with **zero** difference |
| `cl_teslim_9of9.py` re-run | 24 output series **identical** |
| Motoneuron cross-check (Python vs HOC) | 315/315 sections, 2655/2655 segments, 28/28 spikes, **spike-time difference 0.000000 ms, voltage difference 0.000000 mV** |

Honesty note: the quadriceps `+3.7 mm` is produced by the `femur_dist` WrapTorus, not by the
underlying anatomy — with wrapping disabled the quadriceps become flexors. The comparison against
Johnson's Figure 3 has **not** been made, so these values do not yet carry an experimental
validation claim. Full detail, including the GMa sign contradiction, is in `PREPRINT.md` §10.

### What runs today

| Pipeline | State |
|---|---|
| Closed loop (`kod/kapali_dongu/`) | **Runs.** Delivery run reproduced on this machine. |
| OpenSim ID + SO (`kod/opensim/kod_02_swing_id_so.py`) | **Runs.** Reproduces `u_swing_v2.csv` exactly. |
| NEURON mechanisms (`neuron/`) | **Compile.** 12/12 across all four figure folders. |
| NEURON-OpenSim bridge (`kod/kopru/`) | **Runs.** Single process; motoneuron verified against HOC. |
| Rest of the OpenSim pipeline | Missing inputs — see the table in `kod/opensim/README.md`. |
| Full 38-pool spinal circuit | Designed, not yet wired. |

The repository is not fully self-contained: `kod/opensim/rig.py` and a few raw datasets
(Bauman CSVs, Blum `.mat` files) are not here, so the scripts depending on them do not run.

### Repository layout

```
PREPRINT.md      scientific source of truth
DOGRULAMA.md     measurement log (sections A-O, dated)

model/           OpenSim models
  rat_hindlimb_faz1a.osim       the computational model - every result uses this one
  rat_hindlimb_KASLI_x10.osim   GUI viewing only (10x scaled)
  Geometry/                     bone meshes (.vtp); viewing only

veri/            inputs and generated series
  rat_walk_bone_smooth.mot      measured bone-frame gait angles (the core kinematics)
  u_swing_v2.csv                swing-phase muscle commands, 38 muscles x 71 samples
  r_katsayilari_v3.json         Ia/II transfer coefficients (Blum fit)
  kas_par.json  lewis_grf.json  id_tau.json                    computation inputs
  dienes_bilek_momenti.json  cop_dienes.json
  goruntuleme/                  .mot files for GUI animation (not used in computation)
  kapali_dongu/                 cl_grid3d.npz (3D grid), cl_best_9of9.json, cl_teslim_9of9.npz
  kopru/                        moto_morfoloji.npz (motoneuron morphology dump)

kod/             all Python
  yollar.py                     single source of in-repo paths; every script uses it
  opensim/                      ID + static optimization pipeline (Python 3.13, .venv-osim)
  kapali_dongu/                 emergent closed loop + CMA-ES (Python 3.14, pure NumPy)
  kopru/                        NEURON-OpenSim bridge, motoneuron in Python (Python 3.13)

neuron/          NEURON source tree: the Kim 2020 motoneuron model (.hoc + .mod)
  fig2_4_6/  fig3_5_7/  fig8/  fig9/     per-figure mechanism sets
  kopru/                                 GUI-free entry point (motor_unit_batch.hoc)

sekiller/        publication figures
literatur/       literature summaries (oz_*.md), tolerance bands (referans_degerler.json),
                 diyagramlar/ (D1-D8 Mermaid sources of the diagrams in PREPRINT.md)
```

`kod/opensim/`, `kod/kapali_dongu/` and `literatur/` each have their own `README.md` with the
details; NEURON's own run instructions are in `neuron/README.txt`.

### References

| Source | Role |
|---|---|
| Johnson et al. 2008, *J Biomech* 41(3):610-619 | Musculoskeletal geometry; moment-arm reference |
| Kim 2020, *eNeuro* 7(2) | Motoneuron cell, Cav1.3 PIC location, Ia synapse distribution, closed-loop motor unit architecture (cat-derived) |
| Vincent et al. 2017, *J Neurophysiol* 118:2687-2701 | Rat Ia/II afferent validation bands; Ia to lamina IX connectivity |
| Gorassini et al. 2000, *J Neurophysiol* 83:2002-2011 | Pool output validation targets (TA swing 97 Hz, Sol 28 Hz, MG/LG 62-72 Hz) |
| Yu & Thomas 2021, *Biol Cybern* 115:135-160 | CPG architecture (half-centre, Morris-Lecar) |
| Fietkiewicz 2023, *Front Comput Neurosci* 17:1143323 | In-NEURON module coupling (POINTER, NetCon), time-step halving test |
| Fietkiewicz 2025 (NEURON + MuJoCo) | Template for advancing two simulators on a shared time step |
| Blum 2020 | Source of the Ia spindle fit coefficients |

---

## Türkçe

### Bu ne?

Bu depo, Sprague-Dawley sıçanının arka bacağında **omurilikten kasa uzanan kapalı döngüyü**
bilgisayarda kuruyor. Mekaniği **OpenSim** taşıyor — bacağın kas-iskelet modeli. Sinirsel komutu
**NEURON** taşıyor — motonöronlar ve üstlerindeki omurilik devresi. Döngü kendi üstüne kapanıyor:
motonöron havuzları kasları sürer, doğan hareket kas iğciklerini gerer, Ia/II afferent sinyali
komutu yeniler. Uzun vadeli gerekçe, omurilik yaralanmasında nöroprotez geliştirmek için bir zemin
kurmak.

Bugünkü nokta: kas-iskelet yarısı kurulu ve salınım fazı kas aktivasyonları çözüldü; motonöron
hücresi Python'da kuruldu ve referans HOC uygulamasıyla birebir doğrulandı; NEURON ile OpenSim'in
tek bir Python sürecinde birlikte koştuğu gösterildi. Sıradaki adım 38 havuzluk omurilik devresini
bağlamak.

`PREPRINT.md` bilimsel tek doğruluk kaynağıdır (yöntem, sayılar, iddialar, açık sorular).
`DOGRULAMA.md` ölçüm defteridir — ne, ne zaman doğrulandı ve ne doğrulanmadı.

### Gereksinimler

- **macOS / Darwin arm64** — aşağıdaki her komutun fiilen denendiği platform
- **uv** >= 0.11.26
- **Xcode Command Line Tools** (`clang++`) — `nrnivmodl` bunu ister
- Python **3.14** ve **3.13** — ikisini de uv kendisi indirir

### Kurulum

**Bir değil, üç ortam gerekiyor.** `opensim==4.6` Python 3.14 tekerleği yayımlamıyor (yalnız
cp311/cp312/cp313), ana ortam ise `neuron==9.0.2` nedeniyle 3.14 olmak zorunda. İkisi tek ortamda
buluşamıyor. *Köprü* ortamı bunların ortak paydasıdır (Python 3.13); NEURON ile OpenSim aynı süreçte
oraya import edilebilir.

| Ortam | Python | Yer | Ne koşar |
|---|---|---|---|
| Ana | 3.14 | `~/.venvs/usk26` (proje dışı) | `kod/kapali_dongu/` |
| OpenSim | 3.13 | `.venv-osim` (proje içi) | `kod/opensim/` |
| Köprü | 3.13 | `~/.venvs/usk26-kopru` (proje dışı) | `kod/kopru/`, `nrnivmodl`, NEURON |

Bu deponun kendi dizin adı boşluk ve Türkçe karakter içerdiği için **iki yol kısıtı** doğuyor:

1. **NEURON boşluksuz bir yola kurulmalı.** `nrnivmodl`, kurulum dizinini derleyiciye *tırnaklamadan*
   geçirir; boşluk derlemeyi düşürür. Ana ve köprü ortamlarının `~/.venvs` altında olmasının nedeni
   budur. Derlemenin proje *içinde* yapılması sorun değildir — kısıt yalnız NEURON'un kendi kurulum
   yolundadır.
2. **NEURON'a verilen her yol göreli ve ASCII olmalı.** HOC dizgi arayüzü ASCII dışı karakter kabul
   etmiyor (`python string arg cannot decode into c_str`). Python tarafı `os.chdir()` ile konumlanır
   ve `load_file` / `xopen`'a yalnız göreli ad verir.

```bash
# 1) Ana ortam (Python 3.14, NEURON + kapali dongu)
export UV_PROJECT_ENVIRONMENT="$HOME/.venvs/usk26"     # bu satiri ~/.zshrc'ye de ekle
uv sync

# 2) OpenSim ortami (Python 3.13)
uv venv --python 3.13 .venv-osim
uv pip install --python .venv-osim -r requirements-opensim.txt

# 3) Kopru ortami (Python 3.13, NEURON + OpenSim ayni surecte)
uv venv --python 3.13 "$HOME/.venvs/usk26-kopru"
uv pip install --python "$HOME/.venvs/usk26-kopru" -r requirements-kopru.txt

# 4) NEURON mekanizmalarini derle (her figur klasorunun kendi .mod kumesi var)
export PATH="$HOME/.venvs/usk26-kopru/bin:$PATH"
for d in fig2_4_6 fig3_5_7 fig8 fig9; do (cd "neuron/$d" && nrnivmodl); done

# 5) Kurulumu dogrula
$HOME/.venvs/usk26/bin/python -c "import numpy, neuron; print(numpy.__version__, neuron.__version__)"
./.venv-osim/bin/python -c "import opensim, scipy; print(opensim.__version__, scipy.__version__)"
$HOME/.venvs/usk26-kopru/bin/python -c "import neuron, opensim; print('kopru ok')"
```

5. adımın referans makinedeki çıktısı: `2.4.6 9.0.2` · `4.6 1.18.1` · `kopru ok`. Her `nrnivmodl`
`Successfully created arm64/special` ile bitmeli; dört klasörün dördü de derleniyor (toplam 12
mekanizma). İki zararsız uyarı: `uv venv --python 3.13`, 3.13'ün `requires-python = ">=3.14"` ile
uyumsuz olduğunu söyler; NEURON da eksik `DISPLAY` uyarısı basar.

Not: `uv run --python .venv-osim ...` bu projede **çalışmaz** — `requires-python` kısıtı 3.13'ü
reddeder. Yorumlayıcı aşağıdaki gibi doğrudan çağrılır.

### Nasıl koşturulur

```bash
# Ters dinamik + statik optimizasyon -> veri/u_swing_v2.csv
./.venv-osim/bin/python kod/opensim/kod_02_swing_id_so.py

# Kapali dongu teslim kosusu -> sekiller/ + veri/kapali_dongu/
$HOME/.venvs/usk26/bin/python kod/kapali_dongu/cl_teslim_9of9.py

# Motonoron capraz kontrolu: Python kurulumu vs HOC kurulumu, ayni surec, ayni uyaran
$HOME/.venvs/usk26-kopru/bin/python kod/kopru/capraz_kontrol.py
```

`kod/kapali_dongu/cl_optimize.py` CMA-ES parametre aramasını koşar (~6-7 saat). Kapalı döngü
integratörü **`dt = 2e-5` zorunlu kılar**: bilek DOF eylemsizliği kalçanınkinin yaklaşık 1/120'sidir
ve açık Euler `dt = 1e-4`'te bu stiff DOF için kararsızdır — artefakt sayısaldır, kontrol hatası
değildir (`DOGRULAMA.md` §K.2).

### Model ne yapıyor

**Kas-iskelet tarafı (OpenSim).** Geometri Johnson ve ark. 2008'den. Beş segment (spine, pelvis,
femur, tibia, foot), 14 koordinat — 7'si bacak ekseni — ve 38 kas; hepsi rijit tendonlu
`Thelen2003Muscle`. Girdi kinematiği `veri/rat_walk_bone_smooth.mot` ölçülmüş kemik-çerçeve yürüyüş
çevrimidir: 201 örnek, T = 0,387 s. **Salınım fazını** bilerek çözüyoruz: ayak yerden kesiktir,
dolayısıyla yer tepki kuvveti gerekmez. Zincir şudur — ters dinamik (kas kuvvetleri hariç, 15 Hz
alçak geçirgen) → moment kolu matrisi `R(q)`, 7 DOF × 38 kas → statik optimizasyon
`min Σa² + 1e6·Σr²`, kısıt `R·F(a) + R·F_pasif + r = τ_ID` → kas komutları `veri/u_swing_v2.csv`,
yürüyüş çevriminin %65-100 aralığında 38 kas × 71 örnek.

**Omurilik tarafı (NEURON).** Hücre Kim 2020 motonöronudur: 311 dendrit bölmesi, somada
Naf/KDr/CaN/KCa/Nap kanalları, aksiyon potansiyelinin doğduğu akson tepeciği ve başlangıç segmenti,
ve `D_path = 600 µm`'de `gcalbar = 1,37 mS/cm²` değerinde bir Cav1.3 kalıcı-içeri-akım (PIC)
odağı. Ia sinapsları somada ve `D_path < 1400 µm` olan dendritlerdedir. Hücrenin üstünde tasarlanan
devre şudur: supraspinal tonik girdi → CPG yarım-merkez çifti (Yu ve Thomas 2021 mimarisi) → eklem
başına örüntü oluşturma katmanı → **kas başına bir olmak üzere 38 motonöron havuzu**, yanlarında
resiprokal (IaIN) ve rekürren (Renshaw) internöronlar. Havuzların fleksör/ekstansör gruplara
atanması moment kolunun işaretinden çıkar.

**Kapalı döngü.** İki simülatör tek bir Python denetim döngüsünde, tek süreçte ve aynı zaman adımıyla
(dt = 0,025 ms) ilerletilir:

```
1. NEURON'u bir adim ilerlet
2. motonoron havuzlarinin dikenlerini oku      -> u(t)   birimsiz 0-1
3. u(t)'yi OpenSim kas aktivasyonlarina yaz
4. OpenSim'i bir adim ilerlet
5. kas-tendon boylarini ve hizlarini oku       -> l_mt, v_mt   (mm, mm/s)
6. igcik atesleme hizi r(t)'yi hesapla, afferent gecikmeyi uygula  (Ia 1,5 ms, II 1,8 ms)
7. r(t)'yi Ia sinaps iletkenligine yaz         -> gmax_IaSyn
```

İğcik çevirici Blum 2020'den fit edilmiştir:
`Ia = max(0; 10,43 + 26,59·d + 27,08·max(v,0)^0,532)`.
Mimarinin bir kuralı kesindir: **kas dinamiği OpenSim'dedir.** Kim modelinin kendi `muscle_unit`
bölmesi yalnız Aşama 1 doğrulamasında kullanılır ve kapalı döngüde devre dışıdır; aksi hâlde kuvvet
iki kez üretilirdi.

### Doğrulanmış sayılar

| Sonuç | Değer |
|---|---|
| Quadriceps diz moment kolu (diz −120°) | RF +3,70 · VL +3,73 · VI +3,72 · VM +3,70 mm |
| Semimembranosus diz moment kolu | −3,87 mm |
| İşaret kuralı | ekstansör pozitif, fleksör negatif — iki bağımsız yöntemle doğrulandı |
| Salınım aktivasyon tepeleri | kalça fleksörleri %68,5 · diz fleksörleri %76,0 · bilek dorsifleksörleri %85,5 |
| `kod_02_swing_id_so.py` yeniden koşusu | `u_swing_v2.csv`'yi **sıfır** farkla üretiyor |
| `cl_teslim_9of9.py` yeniden koşusu | 24 çıktı dizisi **birebir aynı** |
| Motonöron çapraz kontrolü (Python vs HOC) | 315/315 section, 2655/2655 segment, 28/28 diken, **diken zamanı farkı 0,000000 ms, voltaj farkı 0,000000 mV** |

Dürüstlük notu: quadriceps'in `+3,7 mm`'sini anatominin kendisi değil `femur_dist` WrapTorus'u
üretiyor — sarma kapatıldığında quadriceps fleksör oluyor. Johnson'ın Şekil 3'üyle karşılaştırma
**yapılmadı**, dolayısıyla bu değerler henüz bir deneysel doğrulama iddiası taşımıyor. Ayrıntı ve
GMa işaret çelişkisi `PREPRINT.md` bölüm 10'dadır.

### Depo bugün ne kadar koşuyor

| Hat | Durum |
|---|---|
| Kapalı döngü (`kod/kapali_dongu/`) | **Koşar.** Teslim koşusu bu makinede yeniden üretildi. |
| OpenSim ID + SO (`kod/opensim/kod_02_swing_id_so.py`) | **Koşar.** `u_swing_v2.csv`'yi sıfır farkla üretti. |
| NEURON mekanizmaları (`neuron/`) | **Derleniyor.** Dört figür klasöründe 12/12. |
| NEURON-OpenSim köprüsü (`kod/kopru/`) | **Koşar.** Tek süreç; motonöron HOC'a karşı doğrulandı. |
| OpenSim hattının kalanı | Girdileri eksik — tablo: `kod/opensim/README.md`. |
| 38 havuzluk tam omurilik devresi | Tasarlandı, henüz bağlanmadı. |

Depo tam self-contained değildir: `kod/opensim/rig.py` ve bazı ham veri kümeleri (Bauman CSV'leri,
Blum `.mat` dosyaları) burada yoktur; bunlara bağlı betikler koşmaz.

### Klasör haritası

```
PREPRINT.md      bilimsel tek dogruluk kaynagi
DOGRULAMA.md     olcum/dogrulama defteri (A-O bolumleri, tarihli)

model/           OpenSim modelleri
  rat_hindlimb_faz1a.osim       GUNCEL hesap modeli - her hesap bununla
  rat_hindlimb_KASLI_x10.osim   yalniz GUI goruntuleme (10x buyutulmus)
  Geometry/                     kemik mesh'leri (.vtp); yalniz goruntuleme

veri/            girdi ve uretilen seriler
  rat_walk_bone_smooth.mot      olculmus kemik-cerceve yuruyus acilari (cekirdek kinematik)
  u_swing_v2.csv                salinim fazi kas komutlari, 38 kas x 71 ornek
  r_katsayilari_v3.json         Ia/II cevirici katsayilari (Blum fiti)
  kas_par.json  lewis_grf.json  id_tau.json                    hesap girdileri
  dienes_bilek_momenti.json  cop_dienes.json
  goruntuleme/                  GUI animasyonu icin .mot'lar (hesapta kullanilmaz)
  kapali_dongu/                 cl_grid3d.npz (3B izgara), cl_best_9of9.json, cl_teslim_9of9.npz
  kopru/                        moto_morfoloji.npz (motonoron morfoloji dokumu)

kod/             tum Python
  yollar.py                     depo-ici yollarin tek kaynagi; betikler bunu kullanir
  opensim/                      ID + Statik Optimizasyon hatti (Python 3.13, .venv-osim)
  kapali_dongu/                 emergent kapali-dongu + CMA-ES (Python 3.14, saf NumPy)
  kopru/                        NEURON-OpenSim koprusu, Python'da motonoron (Python 3.13)

neuron/          NEURON kaynak agaci: Kim 2020 motonoron modeli (.hoc + .mod)
  fig2_4_6/  fig3_5_7/  fig8/  fig9/     figure ozel mekanizma kumeleri
  kopru/                                 GUI'siz giris noktasi (motor_unit_batch.hoc)

sekiller/        yayin figurleri
literatur/       literatur ozetleri (oz_*.md), tolerans bantlari (referans_degerler.json),
                 diyagramlar/ (D1-D8 Mermaid; PREPRINT'teki diyagramlarin kaynagi)
```

`kod/opensim/`, `kod/kapali_dongu/` ve `literatur/` klasörlerinin kendi `README.md`'leri vardır;
ayrıntı oradadır. NEURON'un kendi çalıştırma yönergesi `neuron/README.txt`'tedir.

### Kaynaklar

| Kaynak | Rolü |
|---|---|
| Johnson ve ark. 2008, *J Biomech* 41(3):610-619 | Kas-iskelet geometri tabanı; moment kolu referansı |
| Kim 2020, *eNeuro* 7(2) | Motonöron hücresi, Cav1.3 PIC yerleşimi, Ia sinaps dağılımı, kapalı-döngü motor ünite mimarisi (kedi kaynaklı) |
| Vincent ve ark. 2017, *J Neurophysiol* 118:2687-2701 | Sıçan Ia/II afferent doğrulama bantları; Ia → lamina IX bağlantısı |
| Gorassini ve ark. 2000, *J Neurophysiol* 83:2002-2011 | Havuz çıkışı doğrulama hedefleri (TA swing 97 Hz, Sol 28 Hz, MG/LG 62-72 Hz) |
| Yu ve Thomas 2021, *Biol Cybern* 115:135-160 | CPG mimarisi (yarım-merkez, Morris-Lecar) |
| Fietkiewicz 2023, *Front Comput Neurosci* 17:1143323 | NEURON içi modül bağlama (POINTER, NetCon), zaman adımı yarılama testi |
| Fietkiewicz 2025 (NEURON + MuJoCo) | İki simülatörü ortak zaman adımıyla ilerletme şablonu |
| Blum 2020 | Ia iğcik fit katsayılarının kaynağı |
