# USK26 — Sıçan Arka Bacak Nöromekanik Modellemesi

Sıçan arka bacağı yürüyüşünün OpenSim (kas-iskelet) + NEURON (motonöron, kas iğciği, refleks)
ile nöromekanik modellenmesi. Hedef: omurilikten kasa uzanan kapalı döngüyü bilgisayarda kurmak
— motonöron havuzu kası sürer, hareket iğcikte duyu doğurur, Ia/II afferenti komutu yeniler.

## Nereden başlamalı

| İhtiyaç | Dosya |
|---|---|
| **Projemiz ne? Yöntem, sayılar, iddialar** | `PREPRINT.md` (bilimsel tek doğruluk kaynağı) |
| Kurulum (uv, iki ortam, NEURON derlemesi) | `SDLC/06_KURULUM.md` |
| Projenin anlık durumu, sıradaki adım | `SDLC/00_DURUM.md` |
| Amaç, kapsam, başarı ölçütleri | `SDLC/01_PROJE.md` |
| Çalışma kuralları (git, test, raporlama) | `SDLC/04_KURALLAR.md` |
| Doğrulama kaydı (ne doğrulandı, ne doğrulanmadı) | `DOGRULAMA.md` |

İki doğruluk kaynağı vardır ve karıştırılmaz: **`PREPRINT.md`** bilimsel içeriğin,
**`SDLC/`** sürecin kaynağıdır. Bu README yalnızca giriş belgesidir; bilgi burada tekrarlanmaz.

## Klasör haritası

```
PREPRINT.md      bilimsel tek doğruluk kaynağı
DOGRULAMA.md     doğrulama kaydı (A-L bölümleri, tarihli)
SDLC/            süreç: durum, günlük, iş paketleri, kurallar, mimari-risk, kurulum

model/           OpenSim modelleri
  rat_hindlimb_faz1a.osim       GÜNCEL hesap modeli - her hesap bununla
  rat_hindlimb_KASLI_x10.osim   yalnız GUI görüntüleme (10x büyütülmüş)
  Geometry/                     kemik mesh'leri (.vtp); yalnız görüntüleme

veri/            girdi ve üretilen seriler
  rat_walk_bone_smooth.mot      ölçülmüş kemik-çerçeve yürüyüş açıları (çekirdek kinematik)
  u_swing_v2.csv                salınım fazı kas komutları, 38 kas x 71 örnek
  r_katsayilari_v3.json         Ia/II çevirici katsayıları (Blum fiti)
  kas_par.json  lewis_grf.json  id_tau.json                    hesap girdileri
  dienes_bilek_momenti.json  cop_dienes.json
  goruntuleme/                  GUI animasyonu için .mot'lar (hesapta kullanılmaz)
  kapali_dongu/                 cl_grid3d.npz (3B ızgara), cl_best_9of9.json, cl_teslim_9of9.npz

kod/             tüm Python
  yollar.py                     repo-içi yolların tek kaynağı; betikler bunu kullanır
  opensim/                      ID + Statik Optimizasyon hattı (Python 3.13, .venv-osim)
  kapali_dongu/                 emergent kapalı-döngü + CMA-ES (Python 3.14, saf NumPy)

neuron/          NEURON kaynak ağacı: Kim 2020 motonöron modeli (.hoc + .mod)
  fig2_4_6/  fig3_5_7/  fig8/  fig9/     figüre özel mekanizma kümeleri

sekiller/        yayın figürleri (04_KURALLAR: figür DAİMA buraya yazılır)
literatur/       literatür özetleri (oz_*.md), tolerans bantları (referans_degerler.json),
                 diyagramlar/ (D1-D8 Mermaid; PREPRINT'teki diyagramların kaynağı)
arsiv/           aşılmış kuşaklar ve ara ürünler; hesapta kullanılmaz (arsiv/README.md)
```

Her alt klasörün kendi `README.md`'si vardır (`kod/opensim/`, `kod/kapali_dongu/`, `literatur/`,
`literatur/diyagramlar/`, `arsiv/`, `SDLC/`); ayrıntı oradadır.

## Repo bugün ne kadar koşuyor

| Hat | Durum |
|---|---|
| **Kapalı döngü** (`kod/kapali_dongu/`) | **Koşar.** Sonuç koşusu bu makinede yeniden üretildi. |
| **OpenSim ID + SO** (`kod/opensim/kod_02_swing_id_so.py`) | **Koşar.** `u_swing_v2.csv`'yi sıfır farkla yeniden üretti. |
| OpenSim hattının kalanı | Girdileri eksik — tablo: `kod/opensim/README.md`. |
| **NEURON** (`neuron/`) | Derleme sürüyor: `module1_2.mod` NEURON 9 ile düşüyor (İP-4a). |

Repo tam self-contained değildir; eksiklerin tam listesi ve nereden geleceği
`SDLC/05_MIMARI_RISK.md` risk-6'dadır.
