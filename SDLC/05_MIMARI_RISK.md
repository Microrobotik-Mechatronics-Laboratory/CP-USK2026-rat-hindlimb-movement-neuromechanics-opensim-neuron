# MİMARİ & RİSK

> Referans dosya. Teknik veri-akışı ve bilinen riskler.

## Veri-akış haritası

```
03_kod/ (OpenSim: ID + Static Optimization, numpy/scipy)
   kod_01 → rat_walk_bone_smooth.mot
   kod_02 (ID+SO) → u_swing_v2.csv
   u_stance_pipeline → u_stance_v4.csv
   cop_dienes_turetme → cop_dienes.json
   spindle_onisle/fit, rt_ara_uret, r31_uret → r_tamdongu_v3.csv, r_katsayilari_v3.json
        │
        ▼
02_veri/  (u/r sinyalleri, .json girdiler, önceden pişmiş .npz ızgaralar)
        │
        ▼
04_kapali_dongu/ (SAF NumPy — çalışma anında OpenSim YOK)
   cl_sim2 (vektörize çekirdek) + cl_selfcheck (verify/fitness/G9)
   cl_optimize (CMA-ES) → cl_best*.json
   cl_teslim_9of9 → çıktı u/r/açı + figür
        │
        ▼
06_sekiller/ (yayın figürleri)

inline-supplementary-material-1/ (NEURON motonöron modeli — AYRI ada)
   HOC + .mod (fig2_4_6, fig3_5_7, fig8, fig9); PIC (Cav1.3), Ia afferent.
   → İP-4'te kapalı-döngüye bağlanacak.
```

İki taraf ayrıktır: **Python/OpenSim** (03_kod, 04_kapali_dongu) ↔ **NEURON HOC/.mod**
(inline-supplementary-material-1). Bir değişiklik hangi tarafa dokunuyorsa netleştir.

## Bilinen riskler

1. **Bildirilmeyen çalışma-zamanı bağımlılıkları.** `opensim` (4.6, ayrı kuruldu),
   `scipy`, `matplotlib`, `cma` kodda kullanılıyor ama `pyproject.toml`/`uv.lock`/`requiremnts.txt`'te
   yok. Temiz makinede reprodüksiyon kırılır. → İP-5.
2. **Windows-derlenmiş NEURON ikilileri.** `.o`/`.c`/`nrnmech.dll` Windows 64-bit için derlenmiş;
   bu makinede (Darwin) `.mod`'lar `nrnivmodl` ile **yeniden derlenmeli**. → İP-4.
3. **Depo-dışı kritik dosyalar.** `OKU.txt`'ye göre güncel `cl_*.py` (Tsim=6, ılık başlangıç),
   `cl_grid3d.npz` (kapalı döngü bunsuz koşmaz), `cl_best.json`, `Geometry/` mesh'leri başka
   bilgisayarda (`teslim_cc/`). Repo tam self-contained değil.
4. **Lisans.** `rat_hindlimb_0_2.osim` SimTK taban modeli — yayından/paylaşımdan önce SimTK
   lisansı kontrol edilmeli. Hesapta kullanılmıyor (yalnız köken kaydı).
5. **Küçük hijyen.** `requiremnts.txt` dosya adı yazım hatalı (eksik "e"); `.DS_Store` izleniyordu
   (artık git-ignore'da).
