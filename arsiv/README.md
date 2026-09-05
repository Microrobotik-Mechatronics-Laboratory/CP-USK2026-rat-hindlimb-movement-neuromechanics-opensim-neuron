# arsiv — aşılmış kuşaklar ve ara ürünler

Bu klasördeki hiçbir dosya güncel hesapta kullanılmaz. Silinmediler çünkü ya bir doğrulama
kaydının dayanağıdırlar (`../DOGRULAMA.md`), ya da **yeniden üretilemezler** — onları üreten
betikler hiçbir zaman depoya girmedi.

Silme kuralı: buradaki bir dosyayı silmeden önce `../DOGRULAMA.md` içinde adının geçip
geçmediğine bakın. Geçiyorsa silinmez.

## `kod/` — aşılmış kapalı-döngü sürümleri

| Dosya | Ne | Neden arşivde |
|---|---|---|
| `cl_sim2.py` | Faz ızgaralı, **referans-servolu** kapalı döngü çekirdeği | §H hattı. Emergent (referanssız) hat tarafından aşıldı; bildirinin taahhüdü referans servo kullanmamaktır. Import anında `../veri/cl_ref.npz` yükler. |
| `cl_teslim.py` | `cl_sim2` ile 3 hızda teslim koşusu + bozucu on/off | Aynı §H hattı. Çıktıları (`cl_kapali_dongu.npz/.png`) depoya hiç girmedi. |
| `cl_emergent_teslim.py` | Optimizasyon **öncesi** emergent teslim, P elle gömülü | `dt=1e-4` kullanıyor; §K.2 bu adımın bilek DOF'unda **sayısal artefakt** ürettiğini gösterdi (kontrol hatası değil, entegrasyon hatası). Yakınsak adım `dt=2e-5`. |
| `eski_cl_emergent.py` | 7b denetimi **öncesi** emergent çekirdek | GMi hâlâ HIP_FLX'te (ters işaretli moment kolu), ölü kod (DISTAL/STANCE_SYN/KNE_FLX/Foff/SPINDLE) duruyor, II excitation'a beslenmiyor, VCAP=20. |
| `eski_cl_selfcheck.py` | 7c denetimi **öncesi** kapı kümesi | Eski G9 "refleksi tamamen kapat" testiydi; güncel G9 geri beslemeyi faz-ortalaması sabitle değiştiren **yapısal** testtir. Varsayılan `dt=1e-4`. |

Bu iki `eski_*` dosya 3 Eylül 2026'da, güncel sürümler başka bir makineden (`teslim_cc/`)
kopyalanırken kenara alınmıştı. `eski/cl_optimize.py` güncel sürümle **byte düzeyinde aynı**
olduğu için hiç taşınmadı, düşürüldü (git geçmişinde durur).

## `veri/` — aşılmış kuşaklar ve görüntüleme dosyaları

| Dosya | Neden arşivde |
|---|---|
| `cl_ref.npz` | §H Gate 2 çıktısı. **Yeniden üretilemez** — üreteci `gate2_ref.py` depoda yok. |
| `u_stance_v4.csv` | Başlığında "resmî teslim" yazar ama §G'de **v5** resmîleşti. Ayrıca basma fazı anlatısı PREPRINT'ten tamamen çıkarıldı. |
| `r_tamdongu_v3.csv` | §F: v3'ün II sütunu `\|v\|` kullanıyordu (kısalma ateşlemeyi artırıyordu); `r31_uret.py` ile **v3.1** `sign(v)` biçimini resmîleştirdi. |
| `ib_drive_v2.csv` | §G'de **v3** ile değiştirildi; girdisi zaten `u_stance_v4`. |
| `rat_emergent_best.mot` | §I dönemi emergent koşusunun eklem açı çıktısı; `cl_teslim_9of9` tarafından aşıldı. |
| `rat_emergent_best_zemin_x10.mot` | Yukarıdakinin GUI ikizi (yalnız `sacrum_y` farklı: zemine oturtma). |
| `rat_kapali_dongu_referansli_zemin_x10.mot` + `_YAVAS4x` | §H referans-servolu koşunun GUI animasyonu; `_YAVAS4x` aynı verinin 4x yavaş oynatma sürümüdür (yalnız zaman adımı 2e-4 → 8e-4). |
| `bozucu_refleks_ACIK_x10_YAVAS4x.mot` + `_KAPALI_...` | §H bozucu deneyinin refleks açık/kapalı GUI animasyonları. |

## `model/`

`rat_hindlimb_0_2.osim` — SimTK taban modeli (OpenSimDocument **1.06**, 39 kas, 6 gövde).
Hesapta kullanılmaz; köken kaydı olarak tutulur. `DOGRULAMA.md` H2 bulgusu ("6 kemik yanlış,
doğrusu 5") tam olarak bu modelden gelir. **Yayından/paylaşımdan önce SimTK lisansı kontrol
edilmelidir** (İP-6).

## `sekiller/`

`bozucu_deneyi.png` ve `referansli_kol_sonuc.png` — ikisi de §H referans-servolu hattın
figürleri. Üreten betikler depoda yok, yani **yeniden üretilemezler**. PREPRINT'te atıf
almazlar (referanslı anlatı preprintten çıkarıldı).

## `loglar/`

`log1..log4` — CMA-ES koşum kayıtları. `DOGRULAMA.md` §L bu loglardan sayı sayı alıntı yapar;
`log4` (Tsim=6) nihai 9/9 doğrulamasının kaydıdır.

## `neuron_ikili/`

Kim 2020 ek materyalinin **Windows x64 için derlenmiş** çıktıları: 52 `.o`, 4 `nrnmech.dll`,
4 `mod_func.c` (nocmodl üreticisi). Bu makinede (Darwin/arm64) çalışmazlar ve `nrnivmodl`
tarafından yeniden üretilirler. Kaynak `.mod`/`.hoc` dosyaları `../neuron/` altındadır.
