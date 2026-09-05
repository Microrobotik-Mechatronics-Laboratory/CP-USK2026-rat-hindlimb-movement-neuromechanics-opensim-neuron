# MİMARİ & RİSK

> Referans dosya. Teknik veri-akışı ve bilinen riskler.

## Veri-akış haritası

```
03_kod/ (ORTAM: Python 3.13 + OpenSim 4.6 — ID + Statik Optimizasyon, numpy/scipy)
   kod_01 → rat_walk_bone_smooth.mot        [rig.py gerektirir — DEPODA YOK]
   kod_02 (ID+SO) → u_swing_v2.csv
   u_stance_pipeline → u_stance_v4.csv
   cop_dienes_turetme → cop_dienes.json
   spindle_onisle/fit, rt_ara_uret, r31_uret → r_tamdongu_v3.csv, r_katsayilari_v3.json
        │
        ▼
02_veri/  (u/r sinyalleri, .json girdiler, önceden pişmiş .npz ızgaralar)
        │
        ▼
04_kapali_dongu/ (ORTAM: Python 3.14 — SAF NumPy, çalışma anında OpenSim YOK)
   cl_sim2 (vektörize çekirdek) + cl_selfcheck (verify/fitness/G9)
   cl_optimize (CMA-ES) → cl_best*.json
   cl_teslim_9of9 → çıktı u/r/açı + figür
        │
        ▼
06_sekiller/ (yayın figürleri + her figürün kaynak CSV'si) → Markdown rapor

inline-supplementary-material-1/ (ORTAM: Python 3.14 + NEURON 9.0.2)
   HOC + .mod (fig2_4_6, fig3_5_7, fig8, fig9); PIC (Cav1.3), Ia afferent.
```

### Kurulacak köprü (İP-4b, `01_PROJE.md` Aşama 2)

```
   r_tamdongu_v3.csv (Ia/II)  ──►  NEURON: group_Ia.hoc / syn_Ia.mod
                                        │  motonöron havuzu (PIC, Cav1.3)
                                        ▼
   04_kapali_dongu kas aktivasyonu u(t)  ◄──  havuz ateşleme çıktısı
```

Bugün iki taraf ayrıktır: **Python/OpenSim** (03_kod, 04_kapali_dongu) ile **NEURON HOC/.mod**
(inline-supplementary-material-1) arasında veri alışverişi yoktur. Bir değişiklik hangi tarafa
dokunuyorsa netleştir. Köprü kurulurken **birim ve zaman-adımı dönüşümü** kritik noktadır:
NEURON ms/mV/uS ile çalışır, kapalı-döngü s/mm/N ile.

### Doğrulama akışı

```
07_literatur/oz_*.md (makale özütleri)
        │  değer + [alt, üst] bandı + gerekçe
        ▼
07_literatur/referans_degerler.json  ──►  kod-içi assert'ler (İP-8)
                                              │
                                              ▼
                                    02_DOGRULAMA_KAYDI.md + Markdown rapor
```

## Bilinen riskler

1. **İki ortam zorunluluğu.** `opensim` Python 3.14 için tekerlek yayımlamıyor (yalnız
   cp311/cp312/cp313); NEURON ana ortamı ise 3.14. Tek ortamda ikisi birden **kurulamaz**.
   Proje 3.14 (NEURON + kapalı döngü) ve 3.13 (OpenSim + 03_kod) ortamlarıyla çalışır.
   Bu ayrım İP-4b köprüsünü doğrudan etkiler: köprü, iki ortamı aynı süreçte buluşturamaz;
   ya dosya/soket üzerinden ayrık koşum, ya da OpenSim'siz bir kas modeli gerekir. → `06_KURULUM.md`.
2. **Bildirilmeyen çalışma-zamanı bağımlılıkları.** `opensim` (4.6), `scipy`, `matplotlib`, `cma`
   kodda kullanılıyor ama `pyproject.toml`/`uv.lock`/`requiremnts.txt`'te yok. → İP-5.
3. **Windows-derlenmiş NEURON ikilileri.** `.o`/`.c`/`nrnmech.dll` Windows 64-bit için derlenmiş;
   bu makinede (Darwin/arm64) `.mod`'lar `nrnivmodl` ile **yeniden derlenmeli**. → İP-4a.
4. **Boşluklu depo yolu NEURON derlemesini kırıyor.** Depo yolu boşluk ve Türkçe karakter içerir
   (`.../USK26 - Sıçan arka bacak .../Uygulama`). `nrnivmodl`, NEURON'un kurulu olduğu dizinin
   yolunu derleyiciye tırnaklamadan geçirdiği için, NEURON proje içindeki `.venv`'e kuruluysa
   derleme `clang++: no such file or directory: 'Sıçan'` ile düşer. **Çözüm uygulandı:** ana ortam
   `~/.venvs/usk26` (boşluksuz) altına alınır — `06_KURULUM.md` Adım 1. Derlemenin proje içinde
   yapılması sorun değildir; kısıt yalnız NEURON'un kendi kurulum yolundadır.
5. **NEURON 9 ile eski `.mod` uyumsuzluğu.** `module1_2.mod` (kas kasılma modülü) `U` adını hem
   `RANGE` değişkeni hem `FUNCTION` olarak kullanıyor; NEURON 9'un `nocmodl` çeviricisi bunu
   reddediyor (eski NEURON kabul ediyordu). Aynı klasördeki diğer 11 mekanizma derleniyor.
   Model dosyalarına dokunmayı gerektiren tek bilinen engel budur. → İP-4a.
6. **Depo-dışı kritik dosyalar.** Güncel `cl_*.py` (Tsim=6, ılık başlangıç), `cl_grid3d.npz`
   (kapalı döngü bunsuz koşmaz), `cl_best.json`, `Geometry/` mesh'leri başka bilgisayarda
   (`teslim_cc/`). Ayrıca **`03_kod/rig.py` depoda yok** — `kod_01_rat_walk_bone_uret.py` onu
   `import rig` ile çağırıyor, yani veri hattının ilk halkası bu haliyle koşmuyor.
   Repo tam self-contained değil. → İP-5.
7. **Literatür değerlerinin tür/koşul uyumsuzluğu.** Referans değerler farklı tür, farklı deney
   koşulu veya farklı ölçüm yönteminden gelebilir (Kim motonöron modelinin kökeni ile sıçan
   arka bacağı; Johnson/Blum/Dienes'in kendi koşulları). Bu yüzden karşılaştırma birebir değil
   **banttır** ve her bandın gerekçesi tür/koşul farkını açıkça söylemelidir. → `04_KURALLAR.md`.
8. **Telif.** Makale PDF'leri repoya konulamaz; `07_literatur/pdf/` git-ignore'dadır. Depoya
   yalnız künye, çıkarılan sayısal değer ve özüt girer.
9. **Lisans.** `rat_hindlimb_0_2.osim` SimTK taban modeli — yayından/paylaşımdan önce SimTK
   lisansı kontrol edilmeli. Hesapta kullanılmıyor (yalnız köken kaydı).
10. **Küçük hijyen.** `requiremnts.txt` dosya adı yazım hatalı (eksik "e"); `.DS_Store` izleniyordu
   (artık git-ignore'da).
