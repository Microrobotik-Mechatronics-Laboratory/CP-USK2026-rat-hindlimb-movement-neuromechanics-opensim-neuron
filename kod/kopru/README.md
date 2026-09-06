# `kod/kopru/` — NEURON ile OpenSim arasındaki köprü

Bu klasör, `PREPRINT.md` bölüm 8'de tarif edilen **iki yönlü köprüyü** uygular: motonöron
havuzunun ateşlemesi kası sürer (`u(t)`), hareket kas iğciğinde duyu doğurur, Ia/II afferenti
komutu yeniler (`r(t)`). İş paketi: **İP-4b**.

## Ortam

**Bu klasör `~/.venvs/usk26-kopru` (Python 3.13) ile koşar** — NEURON ve OpenSim'in *aynı
süreçte* bulunduğu tek ortam budur. Kurulum ve gerekçe: `SDLC/06_KURULUM.md`.

```bash
~/.venvs/usk26-kopru/bin/python kod/kopru/kos_ayakbilegi.py 3.0
```

## NEURON tarafının iki kırılgan kuralı

Her ikisi de `nrn_ortam.py`'de tek yerde tutulur; doğrudan `from neuron import h` yazmayın.

1. **Yollar göreli olmalıdır.** NEURON'un HOC dizgi arayüzü ASCII dışı karakter kabul etmiyor
   ve bu reponun yolu Türkçe karakter içeriyor. Mutlak yol verilirse
   `python string arg cannot decode into c_str` hatası alınır. (`DOGRULAMA.md` N, ölçüm 4)
2. **Mekanizmalar kendiliğinden yüklenir.** NEURON, import anında çalışma dizinindeki
   `arm64/libnrnmech.dylib`'i yükler. Bu yüzden `os.chdir` **import'tan önce** olmalı ve
   `nrn_load_dll` çağrılmamalıdır (çağrılırsa `user defined name already exists: CaL`).

Üçüncü tuzak, NEURON'a özgü değil ama aynı derecede sessiz: **NEURON nesneleri Python tarafında
referans tutulmazsa çöp toplayıcı siler ve sinaps sessizce yok olur.** Bu, kurulum sırasında
CPG → PF sürüşünü tamamen kaybettirdi (bütün motonöronlar sustu, sebep hiçbir yerde hata
vermedi). `kopru.py` her `NetCon`, `Exp2Syn` ve `GradeSyn`'i `self._nc` / `self._gsyn`'de tutar.

## Dosyalar

| Dosya | Ne yapar |
|---|---|
| `nrn_ortam.py` | NEURON'u doğru dizinde ve doğru sırayla ayağa kaldırır (yukarıdaki iki kural) |
| `morfoloji_cikar.py` | Kim'in morfolojisini bir kez HOC'tan okuyup `veri/kopru/moto_morfoloji.npz`'ye döker |
| `nrn_hucre.py` | Kim 2020 motonöronunu Python'da kurar (çok örnekli; havuz için) |
| `capraz_kontrol.py` | Python kurulumunun HOC kurulumuyla aynı olduğunu aksiyon potansiyeli zamanlarından doğrular |
| `nrn_devre.py` | CPG yarım-merkezleri (Morris-Lecar), PF, IaIN, Renshaw, II aktarım |
| `igcik.py` | Kas-tendon boyu/hızı → Ia ve II ateşleme oranı (Blum fiti) |
| `osim_mekanik.py` | OpenSim ileri dinamiği: kilitleme, uyarım yazma, adım |
| `kopru.py` | İki simülatörü aynı zaman adımıyla ilerleten döngü + birim sözleşmesi |
| `devre_par.json` | Sinaptik ağırlıklar ve kalibrasyon değerleri (koda gömülmez) |
| `kos_ayakbilegi.py` | Aşama 3: ayak bileğinde tam kapalı döngü (1 DOF, 10 havuz) |
| `adim_yarilama.py` | Zaman adımı yarılama testi — **zorunlu** (PREPRINT 8) |

## Birim ve zaman sözleşmesi

`05_MIMARI_RISK.md` bunu köprünün kritik noktası olarak işaretler. Tek yerde,
`kopru.py` başlığında yazılıdır:

| Büyüklük | NEURON | OpenSim | İğcik fiti |
|---|---|---|---|
| zaman | ms | s | — |
| uzunluk | µm (morfoloji) | m | mm |
| iletkenlik | S/cm² | — | — |
| oran | — | — | pps |

**Köprü adımı `dt_k` = 0,3 ms.** Gerekçe: NEURON adımının (0,025 ms) tam katı (12 adım),
Ia gecikmesinin (1,5 ms → 5 adım) ve II gecikmesinin (1,8 ms → 6 adım) tam böleni. Gecikme
yuvarlama hatası sıfırdır.

## Kaynaksız bileşenler (dürüstlük notu)

`IaIN` (resiprokal inhibisyon) ve `Renshaw` (rekürren inhibisyon) bu projenin literatür setinde
**kaynağı olmayan** iki bileşendir (PREPRINT 6.1). Kullanıcı kararıyla ilk sürümde devrededirler
ama **hiçbir sonuç bunlara dayandırılarak iddia edilmez**. `devre_par.json` içindeki
`iain_renshaw.iain_etkin` / `renshaw_etkin` bilinen sapma etiketleriyle kapatılabilirler.

Aynı şekilde `II` katsayıları izlenebilir bir kaynağa dayanmıyor
(`veri/r_katsayilari_v3.json`: "II bu pakette YOK") ve `[varsayım]` etiketlidir.
