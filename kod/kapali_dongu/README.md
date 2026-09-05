# kod/kapali_dongu — emergent kapalı-döngü denetleyici

**Ortam:** ana ortam (Python 3.14, `~/.venvs/usk26`). **Saf NumPy — çalışma anında OpenSim
gerekmez;** kas-iskelet geometrisi önceden `veri/kapali_dongu/cl_grid3d.npz` ızgarasına
tablolanmıştır. Ek bağımlılık: `matplotlib` (figür), `cma` (optimizasyon).

```bash
$HOME/.venvs/usk26/bin/python kod/kapali_dongu/cl_teslim_9of9.py
```

## Modüller

| Dosya | Ne |
|---|---|
| `cl_emergent.py` | Emergent çekirdek: FSM-CPG + anatomik sinerji + gerçek ayak-yer teması + yapısal refleks (yük + fazik Ia/II). Referans servo yok, ölçülmüş GRF izi yok. `run()` dışa verir. |
| `cl_selfcheck.py` | `verify(P)` gate'leri G1–G9 (kabul ölçütleri) ve CMA-ES için `fitness(P)`. G9 yapısal testtir: geri beslemeyi faz-ortalaması sabitle (`meanff`) değiştirir. |
| `cl_optimize.py` | CMA-ES (paralel); `veri/kapali_dongu/cl_best.json`'ı önceki en iyi çözümden başlatma (warm start) için okur ve oraya yazar. |
| `cl_teslim_9of9.py` | 9/9 gateyı geçen parametre setiyle sonuç koşusu. Çıktı: `sekiller/cl_teslim_9of9.png` + `veri/kapali_dongu/cl_teslim_9of9.npz`. |

## Bilinmesi gerekenler

- **`cl_emergent.py` ızgarayı import anında yükler.** `veri/kapali_dongu/cl_grid3d.npz` yerinde
  değilse modül import bile edilemez ve zincirin tamamı düşer. Bu dosyanın üreteci
  (`stage0_grid.py`) hiçbir zaman repoya girmedi — **yeniden üretilemez birincil varlıktır.**
- **`dt=2e-5` zorunludur.** Bilek DOF eylemsizliği çok küçük (kalçanın ~1/120'si); açık Euler
  `dt=1e-4`'te bu stiff DOF kararsız ve bilek ızgara limitine çakılıyor. Bu bir kontrol hatası
  değil, entegrasyon artefaktıdır (`DOGRULAMA.md` §K.2).
- Aşılmış sürümler (`cl_sim2`, `cl_teslim`, `cl_emergent_teslim` ve 7b/7c öncesi kopyalar)
  `arsiv/kod/` altındadır.
