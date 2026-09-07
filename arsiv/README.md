# arsiv — aşılmış kuşaklar, ara ürünler ve kullanımdan kalkmış hatlar

Buradaki hiçbir dosya **canlı hesapta** (NEURON-OpenSim köprüsü, `../kod/kopru/`) kullanılmaz.
Silinmediler çünkü ya bir doğrulama kaydının dayanağıdırlar (`../DOGRULAMA.md`), ya
**yeniden üretilemezler** (üreteçleri hiçbir zaman depoya girmedi), ya da hâlâ yayımlanmış
bir veri ürününün üreteci durumundadırlar.

Silme kuralı: buradaki bir dosyayı silmeden önce `../DOGRULAMA.md` içinde adının geçip
geçmediğine bakın. Geçiyorsa silinmez.

## Versiyon kontrolü durumu (07.09.2026)

`arsiv/` kural olarak `.gitignore`'dadır. **İstisnalar izlenmeye devam eder:** `kod/opensim/`,
`kod/kapali_dongu/`, `veri/cl_ref.npz` ve 07.09.2026 taşımasıyla gelen dört dosya
(`model/rat_hindlimb_KASLI_x10.osim`, `sekiller/cl_teslim_9of9.png`,
`veri/kosum_ayakbilegi.npz`, `veri/goruntuleme/rat_walk_bone_zemin_x10_Bauman.mot`).
Gerekçe: **arşivleme kullanımdan kalkmadır, izlemeden düşme değil** — bu dosyalar taşınmadan
önce versiyon kontrolündeydi ve yayımlanmış sonuçların dayanağıdır. Kuralın kendisi
`../.gitignore` içinde yorumuyla birlikte durur.

## `kod/opensim/` ve `kod/kapali_dongu/` — 07.09.2026'da `kod/` altından taşındı

| Klasör | Ne | Neden arşivde |
|---|---|---|
| `kod/opensim/` | ID + Statik Optimizasyon veri-üretim hattı (8 betik, Python 3.13 + OpenSim 4.6) | Köprü bu hattan hiçbir şey import etmez; kinematik artık reçete değil, kuvvetten doğuyor. **Ama `kod_02_swing_id_so.py` hâlâ `../veri/u_swing_v2.csv`'nin üreticisidir** ve PREPRINT ona atıf yapar. Sekiz betiğin yalnız bu biri koşuyor; kalanının girdileri eksik (`kod/opensim/README.md` tablosu). |
| `kod/kapali_dongu/` | Emergent (referanssız) kapalı döngü + CMA-ES (4 betik, Python 3.14, saf NumPy) | Refleksi **fenomenolojik kazançlarla** temsil ediyordu; yerini gerçek nöron simülasyonuyla çalışan köprü aldı (PREPRINT bölüm 2). Sonuç koşusu (9/9) ve verisi kayıtlı kalır: `../veri/kapali_dongu/`. |

Köprünün import zinciri taşımadan **sonra** doğrulandı: `kod/kopru/` ile `kod/yollar.py` bu iki
klasörden hiçbir şey import etmiyor, yalnız yorumlarda atıf veriyor.

`arsiv/kod/` kökündeki beş dosya (`cl_sim2.py`, `cl_teslim.py`, `cl_emergent_teslim.py`,
`eski_cl_*.py`) daha eski kuşaklardır; tabloları aşağıdadır.

## `kod/` kökü — aşılmış kapalı-döngü sürümleri

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
| `kosum_ayakbilegi.npz` | 07.09.2026'da `veri/kopru/`'den taşındı. Köprünün **ilk** ayak bileği koşusunun (10 havuz, 1 DOF) çıktısı; adı da eskidir — güncel betik `kosu_ayakbilegi.npz` yazar. §P bu koşuya dayanır. |
| `goruntuleme/rat_walk_bone_zemin_x10_Bauman.mot` | 07.09.2026'da `veri/goruntuleme/`'den taşındı. Ölçülmüş yürüyüşün GUI animasyonu (zemine oturtulmuş, 10x); hesapta kullanılmaz. |

## `model/`

`rat_hindlimb_KASLI_x10.osim` — 07.09.2026'da `model/`'den taşındı. Yalnız **GUI görüntüleme**
içindir (10x büyütülmüş); hiçbir hesap bunu kullanmaz, hesap modeli `../model/rat_hindlimb_faz1a.osim`
olarak yerinde kaldı.

`rat_hindlimb_0_2.osim` — SimTK taban modeli (OpenSimDocument **1.06**, 39 kas, 6 gövde).
Hesapta kullanılmaz; köken kaydı olarak tutulur. `DOGRULAMA.md` H2 bulgusu ("6 kemik yanlış,
doğrusu 5") tam olarak bu modelden gelir. **Yayından/paylaşımdan önce SimTK lisansı kontrol
edilmelidir** (İP-6).

## `sekiller/`

`cl_teslim_9of9.png` — 07.09.2026'da `sekiller/`'den taşındı. Arşivlenen emergent kapalı
döngünün 9/9 sonuç figürü; üreteci `kod/kapali_dongu/cl_teslim_9of9.py` ile birlikte buraya
alındı. Verisi `../veri/kapali_dongu/cl_teslim_9of9.npz` olarak yerinde kaldı.

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
