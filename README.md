# USK26 — Sıçan Arka Bacak Nöromekanik Modellemesi

Sıçan arka bacağı yürüyüşünün OpenSim (kas-iskelet) + NEURON (motonöron, kas iğciği, refleks)
ile nöromekanik modellenmesi. Hedef: referans servo veya ölçülmüş yer tepki kuvveti kullanmadan,
refleks ve CPG etkileşiminden **ortaya çıkan (emergent)** kapalı-döngü yürüyüş.

## Nereden başlamalı

| İhtiyaç | Dosya |
|---|---|
| Kurulum (uv, iki ortam, NEURON derlemesi) | `SDLC/06_KURULUM.md` |
| Projenin anlık durumu, sıradaki adım | `SDLC/00_DURUM.md` |
| Amaç, kapsam, başarı ölçütleri | `SDLC/01_PROJE.md` |
| Çalışma kuralları (git, test, raporlama) | `SDLC/04_KURALLAR.md` |
| Dosya-dosya manifesto | `OKU.txt` |

`SDLC/` klasörü projenin tek doğruluk kaynağıdır. Bu README yalnızca kapıdır; bilgi burada
tekrarlanmaz, ilgili dosyaya yönlendirilir.

## Klasör haritası

```
01_model/    OpenSim .osim modelleri (+ Geometry/ mesh)
02_veri/     girdi/çıktı verileri (.mot, .csv, .json)
03_kod/      OpenSim veri-üretim hattı (ID + Statik Optimizasyon)
04_kapali_dongu/  kapalı-döngü kontrolcü + CMA-ES (saf NumPy)
06_sekiller/ yayın figürleri (+ figürü üreten kaynak CSV)
07_literatur/     referans makale özütleri + tolerans bantları
inline-supplementary-material-1/   Kim NEURON motonöron modeli (HOC + .mod)
SDLC/        proje hafızası: durum, günlük, iş paketleri, kurallar, mimari-risk
```

## Uyarı

Depo şu an **self-contained değildir**: kapalı-döngünün koşması için gereken `cl_grid3d.npz`,
güncel `cl_*.py` sürümleri ve `03_kod/rig.py` başka bir bilgisayardadır. Ayrıntı:
`SDLC/06_KURULUM.md` Adım 4.
