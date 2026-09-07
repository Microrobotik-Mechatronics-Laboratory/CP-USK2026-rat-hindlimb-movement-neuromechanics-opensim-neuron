# Literatür özeti — Sartori 2019 (çok ölçekli nöromusküler model + egzoiskelet)

> Bu dosya makalenin **seçici özetidir** — yerine geçmez. Amacı, makaleyi tekrar
> açmadan modelleme kararı verebilmektir.

## 1 · Künye ve sınıflandırma

- **Yazarlar / yıl:** Massimo Sartori, Guillaume Durandau, Herman van der Kooij, Dario Farina / 2019
- **Başlık:** Multi-scale Modelling of the Human Neuromuscular System for Symbiotic Human-Machine Motor Interaction
- **Dergi / cilt / sayfa:** ICNR 2018 bildirisi; L. Masia et al. (Eds.), BIOSYSROB 21, s. 167–170 (Springer)
- **DOI / PMC:** 10.1007/978-3-030-01845-0_33
- **PDF:** `pdf/Multi-scale_Modelling_of_the_Human_Neuromuscular_System_for_Symbiotic_Human-_Machine_Motor_Interaction.pdf` (repoya girmez)
- **Özeti çıkaran / tarih:** Claude / 2026-09-06

- **Makale tipi:** derleme/perspektif + kısa deneysel gösterim (4 sayfalık konferans bildirisi; kendi ifadesiyle "perspective paper", Bölüm 1)
- **Projemizin hangi tarafına bakıyor:** köprü (MN dekodlama → kas-iskelet modeli) + uygulama (egzoiskelet, Faz 3'ümüzün konusu)
- **Bizim için değeri:** yalnız tartışma/atıf + Faz 3 (egzoiskelet) için yöntem işaretçisi. MN→model kısmı Sartori 2017'nin (Sci Rep 7:13465) özetidir; oradaki özet esas alınır.

## 2 · Makalenin sorusu ve ana iddiası
Bildiri, omurilik motoneuron havuzlarının aktivitesini okuma ve bunu kas-iskelet mekanik fonksiyonuna çevirme tekniklerini derler; sonra bu çerçeveyi robotik egzoiskelet bağlamına taşır. İddia: nöral aktivasyon, fiber kısalma-uzama döngüsü, tendon gerinimi gibi nöromusküler iç durumlara pencere açan insan-makine arayüzleri kurulabilir ve bu, kullanıcıyla "simbiyotik" çalışan egzoiskeletlere doğru bir adımdır (Abstract; Bölüm 1).

---

## 3 · NEYİ NASIL YAPMIŞ (yöntem)

### 3a · Denek / malzeme / model
- **Derleme tarafı:** kendi grubunun önceki çalışmaları derlenir — MN dekodlama + nöral veri sürüşlü modelleme [1 = Sartori 2017 Sci Rep] ve gerçek zamanlı EMG sürüşlü modelleme [3 = Durandau 2018].
- **Deneysel taraf:** 4 sağlıklı erkek (yaş 30 ± 1.9 yıl, kütle 68.3 ± 1.3 kg, boy 184 ± 2.1 cm). Etik: MN dekodlama için Göttingen; insan-egzoiskelet etkileşimi için University of Twente etik kurulu (Bölüm 2.1).
- **Egzoiskelet:** Achilles — plantar fleksiyonu destekleyen, seri-elastik eyleyicili iki taraflı ayak bileği ortezi (Bölüm 2.4).

### 3b · Yöntem adımları
1. HD-EMG 2048 Hz'de örneklenir, 10–500 Hz bant geçiren filtrelenir; deconvolution tabanlı blind source separation ile MN deşarjları çıkarılır (Bölüm 2.2).
2. Dekode spike train'ler, OpenSim ile deneğe ölçeklenmiş modeli (5 DOF; 7 MTU: soleus, gastrocnemius med./lat., peroneus longus/brevis/tertius, tibialis anterior) ileri dinamik formülasyonda sürer; kör tahmin yapılır (Bölüm 2.2–2.3).
3. Hesaplama çerçevesi Achilles egzoiskelete EtherCAT protokolüyle gerçek zamanlı bağlanır; bu gerçek zamanlı nöromekanik model 5 bilek kasından alınan bipolar EMG ile sürülür (Bölüm 2.4).
4. Calf rise (parmak ucu yükselme) sırasında soleus kasının kuvvet-uzunluk work loop'u iki asistans düzeyinde karşılaştırılır (Bölüm 3; Şekil 1).

### 3c · Tanım ve birim uyarıları
- **Work loop eksenleri normalizedir:** Y ekseni yüzde kas kuvveti, X ekseni normalize fiber uzunluğu (fiber uzunluğu / optimal fiber uzunluğu) (Şekil 1 açıklaması). Mutlak N veya mm değildir.
- **İki farklı EMG kipi aynı bildiride geçer:** MN dekodlama çok kanallı HD-EMG ([1]) ile; egzoiskelet kontrolü bipolar EMG (5 kanal) ile yapılır (Bölüm 2.4). "EMG sürüşlü" ifadesi geçtiğinde hangi kip kastediliyor, ayırt edilmelidir.
- **"Minimal impedance" asistans kipinin tanımı bildiride açılmaz;** karşıt kip metinde "without minimal impedance" diye anılır (Bölüm 3). Kip tanımları için [3, 4] açılmalıdır.

### 3d · Kullanılan parametreler ve değerleri

| Parametre | Değer | Birim | Nereden |
|---|---|---|---|
| HD-EMG örnekleme / bant | 2048 / 10–500 | Hz | Bölüm 2.2 |
| Geometri modeli | 5 DOF, 7 MTU | — | Bölüm 2.3 |
| Egzoiskelet iletişimi | EtherCAT | — | Bölüm 2.4 |
| Egzoiskelet kontrol EMG'si | 5 bilek kası, bipolar | — | Bölüm 2.4 |

---

## 4 · NE SONUÇ BULMUŞ

### 4a · Sayısal sonuçlar

| Büyüklük | Değer | Birim | Nereden | Saçılım (SD/SEM/aralık, n) |
|---|---|---|---|---|
| Dekode MN sayısı (bütün kaslar) | 56.7 | adet | Bölüm 3 | ±10.2 |
| Doğrulama denemesi | 207 | deneme | Bölüm 3 | denek başına 51.7 ± 5.6 |
| Kör moment tahmini NRMSE | 0.13 – 0.58 | — | Bölüm 3 | aralık |
| Kör moment tahmini R² | 0.82 – 0.99 | — | Bölüm 3 | aralık |
| Soleus min. normalize kuvvet (minimal impedance / onsuz) | 0.04 / 0.08 | — | Bölüm 3 | — |
| Soleus maks. normalize kuvvet (minimal impedance / onsuz) | 0.29 / 0.65 | — | Bölüm 3 | — |
| Soleus min. normalize fiber uzunluğu (minimal impedance / onsuz) | 0.89 / 0.88 | — | Bölüm 3 | — |
| Soleus maks. normalize fiber uzunluğu (minimal impedance / onsuz) | 1.05 / 1.04 | — | Bölüm 3 | — |

### 4b · Niteliksel bulgular
- Egzoiskelet asistans kipleri, soleus work loop'unu belirgin biçimde ve özellikle KUVVET ekseninde modüle eder; kasın çalıştığı UZUNLUK aralığı kipler arasında değişmez ve kısalma-uzama döngüleri kuvvet-uzunluk ilişkisinin platosu etrafında merkezli kalır (Bölüm 3; Şekil 1).
- Sonuç, insan-egzoiskelet etkileşiminin KAS MEKANİĞİ düzeyinde (eklem değil, tek kas düzeyinde) yakalanabildiğinin kavram kanıtıdır (Bölüm 4).

### 4c · Yazarların kendi çıkardığı sonuç
Gerçek zamanlı veri-model çerçevesi, iki taraflı bilek egzoiskeletiyle doğrudan arayüzlenmiştir; asistans kiplerinin kas mekaniğini nasıl değiştirdiği gözlenebilmiştir. Gelecek işler: HD-EMG-model bağlaşımının egzoiskeletlerle birleştirilmesi ve operatörün kasıyla simbiyoz içinde çalışan çok ölçekli kontrolörler (Bölüm 4).

---

## 5 · Projemize ilgisi
- **Doğrudan kullanılabilir mi?** Hayır — 4 sayfalık perspektif bildirisidir; yöntem ayrıntısı ve yeni parametre taşımaz. Değeri yön göstermektir.
- **Hangi büyüklüğümüz veya parametremizle eşleşir?** Faz 3 (egzoiskelet tasarımı ve kontrolü) hedefimizle kavramsal eşleşme: nöromekanik modelin gerçek zamanlı, donanıma bağlı çalıştırılabildiğinin ve asistansın kas düzeyinde değerlendirilebildiğinin kanıtı. "Model iç durumlarını (fiber uzunluğu, tendon gerinimi) kontrolör girdisi yapma" fikri, bizim uzun vadeli mimari tartışmamıza girer.
- **Bilinen sistematik fark:** insan bileği, calf rise görevi, EMG sürüşü (bizde simüle MN sürüşü), n=4.
- **Nereye girdi olacak:** yalnız tartışma/atıf (Faz 3 gerekçelendirmesi; gerçek zamanlılık için asıl kaynak Durandau 2018'dir).

## 6 · Bizimle çelişen veya işimize gelmeyen bulgular
- Doğrudan çelişki bulunamadı. Ne arandı: (1) kapalı döngü geri beslemenin gereksizliğine dair iddia (Sartori 2017 özetindeki açık döngü gerilimi burada da geçerlidir ama bildiri yeni kanıt eklemez); (2) work loop bulgusunun sıçan lokomosyonuyla çelişip çelişmediği (izometrik değil ama insan calf rise'ına özgüdür, aktarım iddiası yok). İşimize gelmeyen yön: bildiri, [1] ve [3]'ün sonuçlarını yeni veri eklemeden tekrarlar; atıf verirken birincil kaynak olarak Sartori 2017 ve Durandau 2018 gösterilmelidir, bu bildiri değil.

## 7 · Testlere girecek değerler (varsa)
Bu makaleden test çıkmıyor.

## 8 · Özete alınmayanlar
- Şekil 1'in sol paneli (dekodlama→model→kontrolör akış şeması) ayrıntıları.
- 6 maddelik kaynakça; [3] Durandau 2018 (gerçek zamanlı EMG sürüşlü modelleme) ve [4] Van Dijk 2017 (Achilles değerlendirmesi) gerektiğinde açılacak birincil kaynaklardır.

## 9 · Açık sorular / doğrulanmayanlar
- Asistans kiplerinin ("minimal impedance" vs "without") teknik tanımı ve denetleyici parametreleri bildiride yoktur; [3, 4]'e bakılmalıdır.
- Work loop sayılarının kaç denemeden geldiği (n) bildirilmez; tek temsilî deneme olabilir — "varsayım:" saçılım verilmediği için tek ölçüm kabul edilmiştir, doğrulanmadı.
