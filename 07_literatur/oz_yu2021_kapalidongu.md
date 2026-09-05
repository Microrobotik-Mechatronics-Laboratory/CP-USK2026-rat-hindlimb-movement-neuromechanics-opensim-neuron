# Özüt — Yu 2021 (yarım-merkez osilatörde duyusal geri beslemenin dinamik sonuçları)

> Bu dosya makalenin **kayıplı sıkıştırmasıdır** — yerine geçmez. Amacı, makaleyi tekrar
> açmadan modelleme kararı verebilmektir.

## 1 · Künye ve sınıflandırma

- **Yazarlar / yıl:** Zhuojun Yu, Peter J. Thomas — 2021
- **Başlık:** Dynamical consequences of sensory feedback in a half-center oscillator coupled to a simple motor system
- **Dergi / cilt / sayfa:** Biological Cybernetics, 115: 135–160
- **DOI / PMC:** https://doi.org/10.1007/s00422-021-00864-y
- **PDF:** `pdf/Dynamical_consequences_of_sensory_feedback_in_a_half-center_oscillator_coupled_to_a_simple_motor_system.pdf` (depoya girmez)
- **Özütü çıkaran / tarih:** Claude / 05.09.2026

- **Makale tipi:** bilgisayar modeli (dinamik sistemler / çatallanma analizi)
- **Projemizin hangi tarafına bakıyor:** köprü/kapalı döngü (CPG ↔ kas ↔ duyusal geri besleme)
- **Bizim için değeri:** yöntem örneği (kapalı döngü kurma, gCPG–gFB dengesi, gürbüzlük ölçümü); parametre kaynağı DEĞİL (Aplysia kası, Morris–Lecar nöronu)

## 2 · Makalenin sorusu ve ana iddiası

Kuo'nun (2002) ayrık-zamanlı ileri besleme/geri besleme karşılaştırmasını, sürekli zamanlı ve biyomekanikli bir modele taşıyorlar: Morris–Lecar tabanlı yarım-merkez osilatör (HCO) bir itme–çekme kas–sarkaç sistemini sürüyor, kas boyu da CPG'ye sinaptik geri besleme veriyor. Soru: ritim üretimini CPG iletkenliği (g_syn^CPG) ile geri besleme iletkenliği (g_syn^FB) arasında paylaştırmak dinamiği nasıl değiştirir? Ana iddialar: FB'yi artırmak sistemi dış pertürbasyona karşı gürbüz, iç (duyusal) gürültüye karşı hassas yapar (CPG'yi artırmak tersini); kapalı döngü, salt CPG'li sisteme göre daha zengin davranış dağarcığı (asimetrik limit çevrimleri) üretir; salt geri beslemeli "zincir refleks" ritmi yalnız inhibitör FB ile mümkündür; iç gürültü varken escape/release ayrımı silikleşir. Sonuç anti-redüksiyonist: gürbüz motor kontrol, izole CPG ile değil bütün kapalı döngüyle anlaşılır.

## 3 · NEYİ NASIL YAPMIŞ (yöntem)

### 3a · Denek / malzeme / model

Tamamen hesaplamalı çalışma; deney hayvanı yok. Model 7 değişkenli ODE sistemi: (V1, V2, N1, N2, A1, A2, x). Nöronlar: 2 adet Morris–Lecar hücresi, karşılıklı inhibitör sinapslarla HCO (Skinner 1994; Zhang-Lewis 2013 parametre hattı). Kas: Aplysia californica I2 kasından ölçülmüş Hill tabanlı kinetik model (Yu ve ark. 1999); F = F0·a·FV·LT, FV ≡ 1 sadeleştirmesiyle. Gövde: iki kas arasına asılı sönümlü sarkaç (Kuo geometrisi), 1B hareket. Yazılım: MATLAB (simülasyon) + MatCont (çatallanma, Floquet çarpanları). Kodlar github.com/zhuojunyu-appliedmath/CPG-FB.

### 3b · Yöntem adımları

1. HCO kurulmuş: izole Morris–Lecar hücresi global çekici sabit noktada (V ≈ 13.3 mV, N ≈ 0.85, depolarizasyon bloğu); osilasyon ancak sinaptik etkileşimle doğuyor.
2. Kas aktivasyonu birinci dereceden alçak geçiren filtreyle (Denk. 12–14); nöral girdi u = V/2; kas boyları sarkaç konumuna doğrusal bağlı: L1 = (50 + 0.8x)ℓ, L2 = (50 − 0.8x)ℓ; dx/dt = (F2 − F1)/b.
3. Geri besleme: kas boyunun anlık sigmoid fonksiyonuyla sinaptik iletkenlik (Denk. 17); kontralateral/ipsilateral, aktive edici/inaktive edici, inhibitör/eksitatör seçenekleri.
4. 16 olası mimari, simetriler ve deneme sonuçlarıyla 4 işlevsel sınıfa indirgenmiş: inhibition-release (IR), inhibition-escape (IE), excitation-release (ER), excitation-escape (EE).
5. Her sınıf için (gCPG, gFB) düzleminde: osilasyon bölgesi, periyot, 2. Floquet çarpanı haritalanmış; çatallanmalar (pitchfork, fold, Hopf, torus) MatCont ile bulunup Poincaré haritası Jacobian'ıyla (B matrisi, Bv = ±v testi) doğrulanmış.
6. Dış pertürbasyon testi: sarkaç maksimum konumundan %10 yer değiştirme; hata = pertürbe/pertürbesiz minimum hız farkının mutlak yüzdesi.
7. İç gürültü testi: FB iletkenliği binom kanal gürültülü stokastik terimle değiştirilmiş (Denk. 19); 100 periyot boyunca sağ ekstremumdaki (z=0) maksimum konumun SD'si.

### 3c · Tanım ve birim uyarıları

- **Release / escape:** geçişi aktif hücrenin sönmesi tetikliyorsa release; baskılanan hücrenin kendiliğinden toparlanması tetikliyorsa escape. Ethresh ile ayarlanıyor (0 veya 30 mV).
- **Simetrik / asimetrik çevrim:** R_κ γ(t) = γ(t + T/2) sağlanıyorsa simetrik (Tanım 1); sağlanmıyorsa asimetrik (Tanım 2). Asimetri = iki hücrenin aktif faz süreleri eşit değil.
- **İletkenlik birimi µS/cm²** (Tablo 2) — dikkat: literatürde sinaptik iletkenlik çoğu kez mS/cm²; bizim NEURON modellerimize taşınırken birim ailesi karışmamalı (zaten taşınmayacak, model soyut).
- Kas boyu birimsizleştirilmiş (ℓ = 1 mm ölçek); zaman birimi açık yazılmamış (ms uyumlu görünmekte); periyotlar T ≈ 2254 gibi model-zaman birimleriyle.
- mV → Hz çevrim katsayısı örtük bırakılmış (dipnot 2).

### 3d · Kullanılan parametreler ve değerleri

Tam liste makalede Tablo 2; buraya çekirdek alt küme alındı.

| Parametre | Değer | Birim | Nereden (tablo/şekil/sayfa) |
|---|---|---|---|
| C | 1 | µF/cm² | Tablo 2 |
| Iext | 0.8 | µA/cm² | Tablo 2 |
| gL / gCa / gK | 0.005 / 0.015 / 0.02 | µS/cm² | Tablo 2 |
| EL / ECa / EK | −50 / 100 / −80 | mV | Tablo 2 |
| E_syn^CPG / E_syn^FB | −80 / ±80 | mV | Tablo 2 |
| E1, E3 / E2, E4 | 0 / 15 | mV | Tablo 2 |
| Ethresh / Eslope | 0 veya 30 / 2 | mV | Tablo 2 |
| φN | 0.0005 | ms⁻¹ | Tablo 2 |
| Kas: τ / β / F0 / g / a0 | 2.45 s / 0.703 / 150 mN / 2 / 0.165 | — | Tablo 2 |
| Sürtünme b | 4×10³ | — | Tablo 2 |
| LT(L) katsayıları | −5.27×10⁻⁴, +0.1054, −4.27 | — | Denk. 11 |
| Taranan gCPG, gFB aralığı | ~0–0.014, ~0–0.012 | µS/cm² | Şekil 6, 12, 18, 21 |

## 4 · NE SONUÇ BULMUŞ

### 4a · Sayısal sonuçlar

| Büyüklük | Değer | Birim | Nereden (tablo/şekil/sayfa) | Saçılım (SD/SEM/aralık, n) |
|---|---|---|---|---|
| IR: osilasyonun kesildiği FB üst sınırı | gFB ≳ 0.012 | µS/cm² | Bölüm 3.3 | — |
| IR: osilasyonun sürdüğü CPG aralığı | 1'e kadar | µS/cm² | Bölüm 3.3 | — |
| IR süperkritik pitchfork | gCPG=0.008, gFB≈7.06×10⁻³ | µS/cm² | Şekil 7 + Tablo 1 | pitchfork tanısı: ‖Bv+v‖=0.0066 ≈ 0 |
| IR subkritik pitchfork | gCPG=0.0016, gFB=2.64×10⁻³ | µS/cm² | Şekil 8 + Tablo 1 | — |
| IE: salt CPG'de escape'in kilitlendiği eşik | gCPG > 0.0108 | µS/cm² | Şekil 13 | nullcline analizi |
| IE süperkritik pitchfork | gCPG=0.0004, gFB≈0.0035 | µS/cm² | Şekil 15 + Tablo 1 | — |
| ER fold-of-cycles | gCPG=0.008, gFB≈5.58×10⁻³ | µS/cm² | Şekil 19 + Tablo 1 | fold tanısı: ‖Bv−v‖=0.0191 ≈ 0 |
| ER: osilasyonun kesildiği FB üst sınırı | gFB ≳ 0.012 | µS/cm² | Bölüm 3.5 | — |
| EE: FB'siz osilasyon CPG aralığı | 0.0023 ≲ gCPG ≲ 0.01 | µS/cm² | Bölüm 3.6 | — |
| EE torus çatallanması | gCPG=0.008, gFB≈7.8×10⁻³ | µS/cm² | Şekil 22 | — |
| Örnek periyotlar (IR simetrik/asimetrik) | T ≈ 2254 / 2361 | model zamanı | Şekil 3, 4 | — |
| MATLAB–MatCont çatallanma noktası uyumu | ≤1.4×10⁻⁴ | µS/cm² | Bölüm 4.2 | — |

### 4b · Niteliksel bulgular

- Her dört mimaride, her sabit gCPG için: gFB arttıkça dış pertürbasyon hatası düşer, iç gürültü sapması artar (Şekil 10, 17, 20, 24). Kuo'nun ana sonucu sürekli zamanda da doğrulanıyor.
- Salt ileri beslemeli sistem (gFB=0) yalnız simetrik çevrim üretir; FB eklenince süperkritik pitchfork'la asimetrik çevrim çiftleri doğar — neredeyse eş-fazlıdan neredeyse zıt-fazlıya bir süreklilik (Şekil 25). Yazarlar bunu otopoietik yönlenme (kaçış/yem arama) için olası kaynak diye yorumluyor.
- Salt geri beslemeli ritim (gCPG=0, zincir refleks) yalnız inhibitör FB'de mümkün; eksitatör FB'de faz inhibisyonu şart, dahası eksitatör FB büyüdükçe telafi için daha güçlü inhibitör CPG gerekiyor.
- İç gürültü varken inhibitör sistemlerde release ve escape'in iç/dış gürültü ödünleşim eğrileri üst üste biniyor (Şekil 26); ayrım pratikte siliniyor. Küçük gCPG'de escape≈release, küçük gFB'de inhibisyon≈eksitasyon (Şekil 27; fark ≤%2).
- Periyodun iletkenliklere bağlılığı mimariye göre değişiyor: EE'de gFB arttıkça periyot kısalıyor (frekans artıyor; Spardy 2011 ile uyumlu), inhibitör mimarilerde tekdüze değil.

### 4c · Yazarların kendi çıkardığı sonuç

Kuo'nun ödünleşimi (FB↑ → dış gürbüzlük↑, iç gürültü hassasiyeti↑) biyomekanikli sürekli modelde doğrulandı. Kapalı döngü, izole CPG'de olmayan davranışlar (asimetrik çevrimler, zincir-refleks ritmi) üretir; escape/release ayrımı gürültüyle silikleşir. Ana mesaj: motor kontrol mekanizması izole CPG'den değil, bozulmamış kapalı döngüden çalışılmalı. Sınırlılıklar (yazarların kendisinden): gürbüzlük ölçüsü tek bir tanım; sinaptik gürültü sonsuz kısa korelasyonlu; dış yük yok (Λ ≡ 0); biyomekanik Aplysia'ya özgü ve ayrıntılı model olma iddiası yok.

## 5 · Projemize ilgisi

- **Doğrudan kullanılabilir mi?** Hayır (parametre olarak); evet (yöntem şablonu olarak). Bizim döngümüz aynı çerçevede: da/dt = f(a) + g(a,x); dx/dt = h(a,x) — a = NEURON değişkenleri, x = OpenSim durumu, g = iğcik Ia geri beslemesi.
- **Hangi büyüklüğümüzle eşleşir?** gFB ↔ Ia sinaps ağırlığımız; gCPG ↔ CPG içi karşılıklı inhibisyon ağırlığımız. Gürbüzlük test protokolleri (%10 pertürbasyon; kanal gürültüsü SD'si) bizim doğrulama koşumlarımıza şablon olur.
- **Bilinen sistematik fark:** tür ve ölçek tamamen farklı (Aplysia I2 düz kası, FV≡1; Morris–Lecar 1-bölmeli soyut hücre; sarkaç gövde). Sayılar taşınmaz; yalnız nitel sonuçlar ve analiz yöntemi taşınır.
- **Nereye girdi olacak:** model yapısı kararı (kapalı döngü zorunluluğu, gFB/gCPG dengesinin taranması) + yalnız tartışma/atıf.

## 6 · Bizimle çelişen veya işimize gelmeyen bulgular

- **FB güçlendirmenin bedeli:** iğcik geri beslemesini güçlü yaparsak duyusal gürültüye hassasiyet artacak. "Geri besleme her zaman iyidir" beklentisiyle çelişir; gFB seçimimizde ödünleşim raporlanmalı.
- **Kapalı döngü asimetri üretebilir:** simetrik kurduğumuz sol-sağ (veya fleksör-ekstansör) CPG'de, iğcik geri beslemesi eklenince istemediğimiz asimetrik yürüyüş çözümleri (pitchfork) çıkabilir; bu, hata değil model davranışı olabilir — ayırt etmek bize düşer.
- **Escape/release ayrımına yatırım:** CPG mekanizma tipini gürültüsüz izole testlerle sınıflandırma planımız varsa, bu makale gürültülü kapalı döngüde ayrımın silindiğini söylüyor; izole sınıflandırmanın kapalı döngü davranışını öngörmeyebileceğini kabul etmeliyiz.
- **Aktarılamazlık:** kas modeli FV≡1 varsayıyor; bizim Hill modelimizde kuvvet–hız ilişkisi merkezî. Buradaki nicel sonuçlar (çatallanma konumları, periyotlar) bizim sistemimiz için öngörü değildir.

## 7 · Testlere girecek değerler (varsa)

Bu makaleden test çıkmıyor: sayılar Aplysia-Morris–Lecar modeline özgü, sıçan büyüklükleriyle eşleşmiyor. Test yerine iki **protokol** ödünç alınabilir: (1) %10 konum pertürbasyonu sonrası minimum hız hatası; (2) FB kanalına binom gürültüsüyle 100 periyotluk tepe-konum SD'si.

## 8 · Sıkıştırmada ne düştü

- Denk. 2–19'un tam matematiği (özellikle aktivasyon filtresi 12–14 ve stokastik terim 19'un katsayıları).
- Tablo 2'nin tamamı (yukarıya alt küme alındı) ve Ek C'deki akış-değişmez küme türetimi (Vmin ≈ −76.63 mV, Vmax = 110 mV, Amax ≈ 1.021, xmax ≈ 8.05).
- Şekil 6/12/18/21 periyot ve Floquet haritalarının tam görünümü; Şekil 5 mimari sınıflandırma şeması.
- Poincaré/Floquet hesap ayrıntıları (Bölüm 4) ve tartışmadaki robotik/solunum literatür bağlantıları.

## 9 · Açık sorular / doğrulanmayanlar

- Bölüm 3.4 metni, salt CPG'li IE sisteminin "gCPG ≳ 1.0" için osilasyon üretemediğini yazıyor; Şekil 13 analizi ise eşiği gCPG = 0.0108 gösteriyor. İki değer 100 kat farklı; muhtemel dizgi sorunu. Özüte mekanizmalı olan (0.0108) alındı; alıntılarken dikkat.
- Zaman birimi makalede açık tanımlanmamış; **varsayım:** ms ölçeği (C=1 µF/cm², iletkenlik µS/cm² ailesiyle uyumlu). Periyot değerleri bu belirsizlikle okunmalı.
- mV→Hz çevrimi örtük (dipnot 2); u = V/2 ifadesinin birimi tanımsız.
