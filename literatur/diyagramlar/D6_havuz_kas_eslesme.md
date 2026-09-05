# D6 — 38 motonöron havuzu ile 38 kasın eşleşmesi

**Kural:** OpenSim modelindeki her kasın **bir motonöron havuzu** vardır (38 kas → 38 havuz).
Havuzlar CPG'ye doğrudan değil, eklem başına bir **örüntü oluşturma katmanı**
(pattern formation, PF) üzerinden bağlanır.

```mermaid
flowchart TD
    RGF["RG-F<br/>ritim uretici fleksor"]
    RGE["RG-E<br/>ritim uretici ekstansor"]

    PHF["PF kalca fleksor"]
    PHE["PF kalca ekstansor"]
    PKF["PF diz fleksor"]
    PKE["PF diz ekstansor"]
    PAD["PF bilek dorsifleksor"]
    PAP["PF bilek plantarfleksor"]

    RGF --> PHF
    RGF --> PKF
    RGF --> PAD
    RGE --> PHE
    RGE --> PKE
    RGE --> PAP

    PHF --- MHF
    PHE --- MHE
    PKF --- MKF
    PKE --- MKE
    PAD --- MAD
    PAP --- MAP

    subgraph MHF["Kalca fleksor havuzlari"]
        IP["IP r=+5.41"]
        TFL["TFL r=+8.47"]
        RF1["RF r=+4.17 - iki eklemli"]
        GMe["GMe r=+2.15"]
        GMa["GMa r=+5.39 - CELISKILI"]
    end

    subgraph MHE["Kalca ekstansor havuzlari"]
        SM["SM r=-12.39"]
        BFp["BFp r=-11.95 - iki eklemli"]
        STa["STa r=-14.04 - iki eklemli"]
        STp["STp r=-9.94 - iki eklemli"]
        GP["GP r=-15.23 - iki eklemli"]
        GA["GA r=-7.06 - iki eklemli"]
        AB["AB r=-8.51"]
        AM["AM r=-7.76"]
        AL["AL r=-5.57"]
        QF["QF r=-4.59"]
        CF["CF r=-3.95"]
        GI["GI r=-2.49"]
        GS["GS r=-1.00"]
    end

    subgraph MKE["Diz ekstansor havuzlari"]
        VL["VL r=+3.72"]
        VI["VI r=+3.71"]
        VM["VM r=+3.69"]
        RF2["RF ayni havuz"]
    end

    subgraph MKF["Diz fleksor havuzlari"]
        Pop["Pop r=-1.58"]
        MG1["MG r=-3.43 - iki eklemli"]
        LG1["LG r=-3.08 - iki eklemli"]
        Pla1["Pla r=-4.13 - iki eklemli"]
    end

    subgraph MAD["Bilek dorsifleksor havuzlari"]
        TA["TA r=+3.43"]
        EDL["EDL r=+2.48"]
        Per["Per r=+2.46"]
    end

    subgraph MAP["Bilek plantarfleksor havuzlari"]
        Sol["Sol r=-4.00"]
        MG2["MG ayni havuz"]
        LG2["LG ayni havuz"]
        Pla2["Pla ayni havuz"]
        TP["TP r=-1.88"]
        FDL["FDL r=-2.25"]
        FHL["FHL r=-2.26"]
    end

    subgraph MX["Gruplanmayan havuzlar - moment kolu kararsiz"]
        Pir["Pir"]
        GMi["GMi"]
        OE["OE"]
        OI["OI"]
        Pec["Pec"]
        BFa["BFa"]
    end

    MHF <-->|"resiprokal inhibisyon"| MHE
    MKF <-->|"resiprokal inhibisyon"| MKE
    MAD <-->|"resiprokal inhibisyon"| MAP
```

## Neden eklem başına bir örüntü oluşturma katmanı var

Tek bir yarım-merkez çifti (RG) yalnız iki faz üretir: fleksör ve ekstansör. Ama bu çalışmanın
salınım fazı ölçümü (`D7`) üç eklemin **farklı zamanlarda** tepe yaptığını gösteriyor: kalça
fleksörleri %68,5, diz fleksörleri %76,0, ayak bileği dorsifleksörü %85,5. Tek fazlı bir
girdi bu gecikmeleri veremez. Bu yüzden RG ile motonöron havuzları arasına eklem başına bir
örüntü oluşturma katmanı (PF) konur. `[tasarım]` — literatür özetlerinde doğrudan kaynağı yoktur;
gerekçesi kendi ölçümümüzdür.

## Havuz iç yapısı

| Karar | Seçim | Durum |
|---|---|---|
| Havuz sayısı | 38 (kas başına bir) | `[tasarım]` — kullanıcı kararı |
| Havuzdaki motonöron sayısı `N` | ilk sürümde 1 (temsilî motonöron), sonra artırılacak | `[tasarım]` |
| Motonöron modeli | Kim 2020 hücresi (`D3`) | `[literatürden]` |
| Devreye alma (recruitment) | `F_max` sırasına göre Henneman büyüklük ilkesi (size principle) | `[tasarım]` |
| İki eklemli (biartiküler) kaslar | **tek havuz**, iki örüntü oluşturma katmanından da girdi alır (RF, BFp, STa, STp, GP, GA, MG, LG, Pla, EDL) | `[tasarım]` |
| Antagonist eşleşme | eklem başına fleksör ⇄ ekstansör grupları | moment kolu işaretinden `[ölçüldü]` |
| Gruplanmayanlar | Pir, GMi, OE, OI, Pec, BFa — moment kolu işareti ızgarada kararsız | `[ölçüldü]` gerekçe |

## Ateşleme hedefleri (havuz çıkışının doğrulanacağı aralıklar)

Kaynak: `oz_gorassini2000_motorunite.md` §7 — bilinçli, serbest yürüyen sıçanda tek motor ünite
kayıtları. Bunlar havuz **çıkışının** doğrulama hedefleridir; parametre değil.

| Kimlik | Değer | Aralık | Not |
|---|---|---|---|
| `mn_frekans_TA_swing` | 97 Hz | [80, 110] | salınım fazı dorsifleksör |
| `mn_frekans_MGLG_ortagec` | 62–72 Hz | [50, 90] | basma fazı; bizim kapsam dışı ama havuz sınırı |
| `mn_frekans_SOL_yuruyus` | 28 Hz | [20, 35] | yavaş ünite |
| `dublet_orani_hizli_uniteler` | ≥ %80 adım | [%50, %100] | başlangıç dubleti, ISI ≤ 10 ms |
| `dublet_orani_yavas_SOL` | ~%18 adım | [%0, %30] | gevşetilmiş dublet tanımıyla |

**Uyarı** (`oz_gorassini2000_motorunite.md` §6): MG/LG'de tek ünite aktivitesi gros-EMG zarfından
kopuktur (r² = 0,0015–0,010). Havuzu tek ortak sürücüyle modellemek soleus için savunulabilir,
MG/LG için sorgulanır. Ayrıca yavaş ünitelerde dublet yoktur; PIC'i tüm havuzlara aynı güçle
koyarsak yavaş motonöronlarda fazla dublet üretiriz.
