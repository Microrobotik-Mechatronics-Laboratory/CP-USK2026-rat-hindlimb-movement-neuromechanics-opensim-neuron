# D8 — İşlem hattı ve doğrulama haritası

## İşlem hattı

```mermaid
flowchart TD
    OSIM["rat_hindlimb_faz1a.osim<br/>5 segment - 38 Thelen kas<br/>[var]"]
    MOT["rat_walk_bone_smooth.mot<br/>olculmus kemik eklem acilari<br/>T = 0.387 s - 201 ornek<br/>[var]"]
    ID["Ters dinamik<br/>kas kuvvetleri haric - 15 Hz alcak gecirgen<br/>kod_02_swing_id_so.py<br/>[var]"]
    RMAT["Moment kolu matrisi R q<br/>7 DOF x 38 kas<br/>computeMomentArm<br/>[var]"]
    SO["Statik optimizasyon<br/>min toplam a^2 + rezerv<br/>rijit tendon - Thelen fV<br/>[var]"]
    USW["u_swing_v2.csv<br/>38 kas x 71 ornek<br/>gait %65-100<br/>[var]"]

    MODC["nrnivmodl derleme<br/>fig2_4_6 - 12 mekanizmadan 11 derlendi<br/>module1_2.mod ENGEL"]
    MN1["Asama 1: tek motonoron dogrulamasi<br/>Kim Fig 2-9 yeniden uretimi<br/>[YAPILACAK]"]
    POOL["38 motonoron havuzu + CPG + internoronlar<br/>[YAPILACAK]"]
    BR["Kopru: u t cikisi - r t girisi<br/>ayni zaman adimi dt = 0.025 ms<br/>[YAPILACAK]"]
    CL["Kapali dongu kosusu<br/>[HEDEF]"]

    OSIM --> ID
    MOT --> ID
    ID --> SO
    OSIM --> RMAT
    RMAT --> SO
    SO --> USW
    USW -->|"referans u t - karsilastirma hedefi"| BR

    MODC --> MN1
    MN1 --> POOL
    POOL --> BR
    OSIM --> BR
    BR --> CL
```

## Doğrulama haritası

Her ok bir iddiayı bir kaynağa bağlar. `literatur` kayıtları dış yayına, `ic_olcum` kayıtları
kendi ölçümümüze aittir; ikisi karıştırılmaz (`../README.md`).

```mermaid
flowchart LR
    subgraph OLC["Modelin urettigi buyukluk"]
        M1["Quad diz moment kolu"]
        M2["SM diz moment kolu"]
        M3["Salinim aktivasyon sirasi"]
        M4["Ia atesleme orani"]
        M5["Motonoron atesleme frekansi"]
        M6["PIC konum davranisi"]
    end
    subgraph KAY["Kaynak ve aralık"]
        K1["Johnson 2008 Sekil 3<br/>aralık YOK - karsilastirma yapilmadi"]
        K2["ic_olcum -3.87 mm<br/>aralık -3.92 .. -3.82"]
        K3["Bildiri cumlesi<br/>aralık tanimlanmadi"]
        K4["Vincent 2017 Tablo 4<br/>Ia Dyn pfr 176.4 - aralık 123..230"]
        K5["Gorassini 2000 Tablo 1<br/>TA 97 Hz - aralık 80..110"]
        K6["Kim 2020 Tablo 1 ve Fig 4-7<br/>nitel: Tip I / IV / III"]
    end
    M1 --> K1
    M2 --> K2
    M3 --> K3
    M4 --> K4
    M5 --> K5
    M6 --> K6
```

## Aralık durumu

| Kimlik | Değer | Aralık | Tür | Durum |
|---|---|---|---|---|
| `ic.quad_diz_moment_kolu` | 3,70 · 3,73 · 3,72 · 3,70 mm | [3,65 · 3,78] | `ic_olcum` | JSON'da **var** — regresyon aralığı |
| `ic.sm_diz_moment_kolu` | −3,87 mm | [−3,92 · −3,82] | `ic_olcum` | JSON'da **var** — regresyon aralığı |
| `johnson2008.kas_sayisi` | 37 | — | `literatur` | JSON'da var |
| `johnson2008.lokomosyon_diz_araligi` | [−110 · −60]° | — | `literatur` | JSON'da var |
| `johnson2008.quad_diz_moment_kolu_egrisi` | — | — | `literatur` | **boş** — Şekil 3 karşılaştırması yapılmadı |
| `Ia_Dyn_pfr_hizli` | 176,4 pps | [123 · 230] | `literatur` | literatür özetinde hazır (`oz_vincent2017` §7), **JSON'a girmedi** |
| `Ia_DI_hizli` | 137,9 pps | [90 · 186] | `literatur` | aynı |
| `II_Dyn_pfr_hizli` | 105,4 pps | [57 · 154] | `literatur` | aynı |
| `Ia_ThrL` / `II_ThrL` | 0,2 / 0,6 mm | [0 · 0,4] / [0 · 1,2] | `literatur` | aynı |
| `mn_frekans_TA_swing` | 97 Hz | [80 · 110] | `literatur` | literatür özetinde hazır (`oz_gorassini2000` §7), **JSON'a girmedi** |
| `dublet_orani_hizli_uniteler` | ≥ %80 adım | [%50 · %100] | `literatur` | aynı |
| `MN_esik_boy_dususu` | ~4 kat | [2 · 6] | `literatur` | literatür özetinde hazır (`oz_kim2020` §7), **JSON'a girmedi** |
| `momentkolu_BFA_kalca_tamekstansiyon` | −15,3 mm | [−18 · −12] | `literatur` | literatür özetinde hazır (`oz_johnson2008` §7), **JSON'a girmedi** |

**Kural** (`SDLC/04_KURALLAR.md`): aralık testten **önce** gerekçesiyle ilan edilir; ölçüm banda
düşmezse önce model ve varsayımlar sorgulanır, aralık sessizce genişletilmez.

## Yöntem borçları (kaynağı belli, uygulanmadı)

| Yöntem | Kaynak | Ne için |
|---|---|---|
| Adım-yarılama yakınsama testi | `oz_fietkiewicz2023_neuronpointer.md` §5 | Köprü sayısal kararlılığı; iki simülatör dıştan kuplajlandığı için Jacobian kurulamıyor, bu test zorunlu |
| Eş adımlı ilerletme döngüsü (dt = 0,025 ms) | `oz_fietkiewicz2025_neuronmujoco.md` §3b | Köprü mimarisi |
| `gFB` / `gCPG` taraması + gürbüzlük ölçümü | `oz_yu2021_kapalidongu.md` §7 | Geri besleme ağırlığının seçimi ve ödünleşimin raporlanması |
| PIC konumu taraması `D_path` 100–1000 µm | `oz_kim2020_piclokasyonu.md` Tablo 1 | Motonöron girdi-çıktı tipinin belirlenmesi |
