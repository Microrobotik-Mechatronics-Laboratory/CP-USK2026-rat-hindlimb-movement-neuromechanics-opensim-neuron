# kod/opensim — OpenSim veri üretim hattı

**Ortam:** Python 3.13 + OpenSim 4.6 (`.venv-osim`). Ana 3.14 ortamıyla koşmaz.
Çağrı biçimi (`uv run` bu ortamda **çalışmaz**, bkz. `../../SDLC/06_KURULUM.md`):

```bash
./.venv-osim/bin/python kod/opensim/kod_02_swing_id_so.py
```

Tüm yollar `../yollar.py` üzerinden çözülür; betikler nereden çağrılırsa çağrılsın aynı
dosyayı bulur. Çıplak dosya adı veya mutlak yol yazılmaz.

## Hat

```
kod_01_rat_walk_bone_uret.py   bauman CSV     -> veri/rat_walk_bone.mot (+_smooth)
kod_02_swing_id_so.py          osim + smooth  -> veri/u_swing_v2.csv        [ID + SO]
rt_ara_uret.py                 osim + smooth  -> veri/rt_ara.npz            [kas boy/hiz tablosu]
r31_uret.py                    rt_ara.npz     -> veri/r_tamdongu_v3_1.csv   [Ia/II serileri]
u_stance_pipeline.py           (Makine sinifi) -> stdout                    [basma fazi SO]
cop_dienes_turetme.py          Dienes + Lewis -> veri/cop_dienes.npz        [Makine'yi import eder]
spindle_onisle.py              Blum ham .mat  -> veri/spindle_cache.pkl
spindle_fit.py                 spindle_cache  -> veri/spindle_fit_sonuc.json
```

## Ne koşar, ne koşmaz

| Betik | Durum |
|---|---|
| `kod_02_swing_id_so.py` | **Koşar.** 2026-09-05'te bu makinede koşuldu; `u_swing_v2.csv`'yi sayısal olarak birebir (fark 0,0) yeniden üretti; yalnız dosyanın yorum başlığı elle zenginleştirilmiş olduğu için metin farkı var. Yan çıktı `veri/id_bone.sto` (ID ara dosyası, git-ignore). |
| `rt_ara_uret.py` | Girdileri depoda (model + smooth.mot + kas_par.json); koşması beklenir, **denenmedi**. |
| `kod_01_rat_walk_bone_uret.py` | **Koşmaz.** `import rig` — `rig.py` depoda yok (aşağıya bak). Ayrıca iki `bauman_fig4_*.csv` girdisi de yok. |
| `r31_uret.py` | `veri/rt_ara.npz` gerektirir; önce `rt_ara_uret.py` koşmalı. |
| `u_stance_pipeline.py`, `cop_dienes_turetme.py` | **Koşmaz.** `rt_ara.npz` yok; ayrıca `id_tau.npz` ve `dienes_bilek_momenti.npz` bekliyorlar, depoda **`.json`** karşılıkları var (biçim dönüşümü yapılmadı). |
| `spindle_onisle.py`, `spindle_fit.py` | **Koşmaz.** Blum 2020 eLife ham `.mat` kümesi depoda yok (`veri/spindle_ham/`). |

## Eksik girdiler

| Eksik | Nereden gelir |
|---|---|
| `rig.py` | **Git geçmişinde duruyor:** `git show e0192ec^:kod/rig.py` (79 satır; `.osim` XML'inden gövde/eklem zincirini okuyup ileri kinematik yapar). `e0192ec` "remove old folders" commit'inde eski `kod/` klasörüyle birlikte silinmiş. Geri getirmek İP-5'in işi. |
| `veri/bauman_fig4_v3_hipknee.csv`, `veri/bauman_fig4_v2_kapali_devre.csv` | Bauman Fig 4 sayısallaştırması; depoda yok. |
| `veri/rt_ara.npz` | `rt_ara_uret.py` üretir. |
| `veri/id_tau.npz`, `veri/dienes_bilek_momenti.npz` | Depoda `.json` biçiminde var; dönüştürülmedi. |
| `veri/spindle_ham/aff*_proc.mat` | Blum 2020 eLife veri kümesi (boyut/telif nedeniyle depoya girmez). |
