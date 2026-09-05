# MİMARİ & RİSK

> Referans dosya. Teknik veri-akışı ve bilinen riskler.

## Veri-akış haritası

```
kod/opensim/ (ORTAM: Python 3.13 + OpenSim 4.6 — ID + Statik Optimizasyon, numpy/scipy)
   kod_01 → rat_walk_bone_smooth.mot        [rig.py gerektirir — REPODA YOK]
   kod_02 (ID+SO) → u_swing_v2.csv
   u_stance_pipeline → u_stance_v4.csv
   cop_dienes_turetme → cop_dienes.json
   spindle_onisle/fit, rt_ara_uret, r31_uret → r_tamdongu_v3.csv, r_katsayilari_v3.json
        │
        ▼
veri/  (u/r sinyalleri, .json girdiler, önceden pişmiş .npz ızgaralar)
        │
        ▼
kod/kapali_dongu/ (ORTAM: Python 3.14 — SAF NumPy, çalışma anında OpenSim YOK)
   cl_emergent (emergent çekirdek) + cl_selfcheck (verify/fitness/G9)
   cl_optimize (CMA-ES) → veri/kapali_dongu/cl_best.json
   cl_teslim_9of9 → veri/kapali_dongu/cl_teslim_9of9.npz + sekiller/cl_teslim_9of9.png
        ▲ izgara: veri/kapali_dongu/cl_grid3d.npz (import anında yüklenir)
        │
        ▼
sekiller/ (yayın figürleri + her figürün kaynak CSV'si) → Markdown rapor

neuron/ (ORTAM: Python 3.14 + NEURON 9.0.2)
   HOC + .mod (fig2_4_6, fig3_5_7, fig8, fig9); PIC (Cav1.3), Ia afferent.
```

### Kurulacak köprü (İP-4b, `01_PROJE.md` Aşama 2)

```
   r_tamdongu_v3.csv (Ia/II)  ──►  NEURON: group_Ia.hoc / syn_Ia.mod
                                        │  motonöron havuzu (PIC, Cav1.3)
                                        ▼
   kod/kapali_dongu kas aktivasyonu u(t)  ◄──  havuz ateşleme çıktısı
```

Bugün iki taraf ayrıktır: **Python/OpenSim** (kod/opensim, kod/kapali_dongu) ile **NEURON HOC/.mod**
(neuron) arasında veri alışverişi yoktur. Bir değişiklik hangi tarafa
dokunuyorsa netleştir. Köprü kurulurken **birim ve zaman-adımı dönüşümü** kritik noktadır:
NEURON ms/mV/uS ile çalışır, kapalı-döngü s/mm/N ile.

**Yol kuralı:** hiçbir betik çıplak dosya adı veya mutlak yol yazmaz; tüm repo-içi yollar
`kod/yollar.py` üzerinden çözülür (kök, dosyanın kendi konumundan bulunur). Aşılmış sürümler
ve ara ürünler `arsiv/` altındadır ve hesapta kullanılmazlar (`arsiv/README.md`).

### Doğrulama akışı

```
literatur/oz_*.md (literatür özetleri)
        │  değer + [alt, üst] bandı + gerekçe
        ▼
literatur/referans_degerler.json  ──►  kod-içi assert'ler (İP-8)
                                              │
                                              ▼
                                    DOGRULAMA.md + Markdown rapor
```

## Bilinen riskler

1. **İki ortam zorunluluğu.** `opensim` Python 3.14 için tekerlek yayımlamıyor (yalnız
   cp311/cp312/cp313); NEURON ana ortamı ise 3.14. Tek ortamda ikisi birden **kurulamaz**.
   Proje 3.14 (NEURON + kapalı döngü) ve 3.13 (OpenSim + kod/opensim) ortamlarıyla çalışır.
   Bu ayrım İP-4b köprüsünü doğrudan etkiler: köprü, iki ortamı aynı süreçte buluşturamaz;
   ya dosya/soket üzerinden ayrık koşu, ya da OpenSim'siz bir kas modeli gerekir. → `06_KURULUM.md`.
2. ~~**Bildirilmeyen çalışma-zamanı bağımlılıkları.**~~ **Kapandı (2026-09-05):** `matplotlib` ve
   `cma` ana ortama (`pyproject.toml` + `uv.lock`) beyan edildi; `opensim` ve `scipy` ikincil
   ortam için `requirements-opensim.txt`'e yazıldı. Yazım hatalı `requiremnts.txt` kaldırıldı.
3. **Windows-derlenmiş NEURON ikilileri.** `.o`/`mod_func.c`/`nrnmech.dll` Windows 64-bit için
   derlenmiş; bu makinede (Darwin/arm64) çalışmazlar. 2026-09-05'te `neuron/` ağacından
   `arsiv/neuron_ikili/` altına alındılar; `.mod` dosyaları `nrnivmodl` ile **yeniden
   derlenmeli**. → İP-4a.
4. **Boşluklu repo yolu NEURON derlemesini kırıyor.** Repo yolu boşluk ve Türkçe karakter içerir
   (`.../USK26 - Sıçan arka bacak .../Uygulama`). `nrnivmodl`, NEURON'un kurulu olduğu dizinin
   yolunu derleyiciye tırnaklamadan geçirdiği için, NEURON proje içindeki `.venv`'e kuruluysa
   derleme `clang++: no such file or directory: 'Sıçan'` ile düşer. **Çözüm uygulandı:** ana ortam
   `~/.venvs/usk26` (boşluksuz) altına alınır — `06_KURULUM.md` Adım 1. Derlemenin proje içinde
   yapılması sorun değildir; kısıt yalnız NEURON'un kendi kurulum yolundadır.
5. **NEURON 9 ile eski `.mod` uyumsuzluğu.** `module1_2.mod` (kas kasılma modülü) `U` adını hem
   `RANGE` değişkeni hem `FUNCTION` olarak kullanıyor; NEURON 9'un `nocmodl` çeviricisi bunu
   reddediyor (eski NEURON kabul ediyordu). Aynı klasördeki diğer 11 mekanizma derleniyor.
   Model dosyalarına dokunmayı gerektiren tek bilinen engel budur. → İP-4a.
6. **Repo eksikleri (2026-09-05'te yeniden ölçüldü).** Eski kayıtta "repo dışında" denen üç
   dosya **aslında repodadır**: `veri/kapali_dongu/cl_grid3d.npz`, güncel `cl_emergent.py` ve
   `cl_selfcheck.py` (7b/7c düzeltmeli sürümler; eski kopyalar `arsiv/kod/` altında).
   `cl_best.json`'un karşılığı `veri/kapali_dongu/cl_best_9of9.json`. `model/Geometry/` mesh'leri
   de repodadır. Gerçekten eksik olanlar:
   - **`kod/opensim/rig.py`** — kayıp değil, **git geçmişinde duruyor**:
     `git show e0192ec^:kod/rig.py` (79 satır). Geri getirmek İP-5'in işi.
   - `veri/bauman_fig4_*.csv`, `veri/rt_ara.npz`, `veri/spindle_ham/` ve `.npz` beklenip `.json`
     duran iki girdi. Tam tablo: `kod/opensim/README.md`.
   - `veri/kapali_dongu/cl_grid3d.npz` ve `arsiv/veri/cl_ref.npz` **yeniden üretilemez** —
     üreteçleri (`stage0_grid.py`, `gate2_ref.py`) hiç repoya girmedi. → İP-5.
7. **Literatür değerlerinin tür/koşul uyumsuzluğu.** Referans değerler farklı tür, farklı deney
   koşulu veya farklı ölçüm yönteminden gelebilir (Kim motonöron modelinin kökeni ile sıçan
   arka bacağı; Johnson/Blum/Dienes'in kendi koşulları). Bu yüzden karşılaştırma birebir değil
   **banttır** ve her bandın gerekçesi tür/koşul farkını açıkça söylemelidir. → `04_KURALLAR.md`.
8. **Telif.** Makale PDF'leri repoya konulamaz; `literatur/pdf/` git-ignore'dadır. Repoya
   yalnız künye, çıkarılan sayısal değer ve literatür özeti girer.
9. **Lisans.** `arsiv/model/rat_hindlimb_0_2.osim` SimTK taban modeli — yayından/paylaşımdan önce
   SimTK lisansı kontrol edilmeli. Hesapta kullanılmıyor (yalnız köken kaydı).
10. ~~**Küçük düzen sorunu.**~~ **Kapandı:** yazım hatalı `requiremnts.txt` kaldırıldı;
   `.DS_Store`, `opensim.log` ve `veri/id_bone.sto` git-ignore'dadır.
