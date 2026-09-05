# DOĞRULAMA KAYDI

> **Konum notu (05.09.2026):** bu dosya `04_kapali_dongu/02_DOGRULAMA_KAYDI.md` iken depo köküne
> `DOGRULAMA.md` olarak alındı. Aşağıdaki kayıtlar **tarihli ölçüm tutanaklarıdır ve
> düzenlenmezler**; içlerinde geçen dosya adları yazıldıkları günün düzenine göredir. Bugünkü
> karşılıkları: `kod/opensim/`, `kod/kapali_dongu/`, `veri/kapali_dongu/`, `sekiller/`,
> `arsiv/` (aşılmış sürümler). Güncel klasör haritası: `README.md`.

**Ölçüm tarihi:** 27.07.2026
**Nasıl ölçüldü:** `pip install opensim --break-system-packages` ile OpenSim **4.6** kuruldu. Depodaki scriptler (`build_osim.py`, `ma_validate.py`, `clean_ma.py`, `peak_ma.py`) çalıştırıldı. `rat_hindlimb_0.2.osim` dosyası XML olarak ayrıştırıldı. Johnson ve ark. 2008 tam metni PMC2322854'ten okundu.

Aşağıdaki her satır bu oturumda ölçülmüştür. Devir dosyalarından taşınan hiçbir sayı doğrulanmış sayılmamıştır.

---

# A · Doğrulanan sayılar

| İddia | Ölçülen | Üreten |
|---|---|---|
| Quad diz moment kolu ≈ +3,7 mm | RF +3,70 · VL +3,73 · VI +3,72 · VM +3,70 | `ma_validate.py` |
| Aynı sayı, ikinci yöntemle | RF +3,70 · VL +3,74 · VI +3,72 · VM +3,71 | `clean_ma.py` |
| Semimembranosus ≈ −3,9 mm | −3,87 | her iki script |
| Quad tepe değeri | 3,75 mm @ −117° | `peak_ma.py` |
| Trot diz aralığı | −123,1° … −54,5° | `rat_trot.mot` |
| Trot aralığında değişim | 0,47 mm (3,28 … 3,75) | `peak_ma.py` |
| Koordinat sayısı | 14 (7'si bacak ekseni) | `.osim` |
| Kas sayısı | 38, hepsi `Thelen2003Muscle` | `.osim` |
| Her kasın nokta sayısı | hepsinde tam 2 (via point yok) | `.osim` |
| `tendon_slack_length` | 38 kasın hepsinde 0 | `.osim` |
| F_max | dosyada gerçek değerler 0,2–18,8 N; `build_osim.py` 10 N yer tutucu koyuyor | `.osim` + `build_osim.py` |
| Sarma nesnesi sayısı | 13 = 9 silindir + 2 torus + 2 küre | `.osim` |
| `knee_flx` varsayılan / aralık | −120° / −150° … −20° | `.osim` |
| İki ileri kinematik uyumu | femur, tibia, foot origin'leri örtüşüyor | `build_osim.py` |
| "Diz büküldükçe ekstansör uzar, fleksör kısalır" | RF: −20°'de 33,42 mm → −150°'de 41,18 mm (uzuyor). SM: 46,45 → 38,46 mm (kısalıyor) | ölçüldü |
| Sıçan soyu Sprague-Dawley | Johnson Methods: yedi dişi Sprague-Dawley, 280 ± 16 g | Johnson 2008 |
| Johnson'ın ana bulgusu | "moment kolları lokomosyon bölgesinde tepe yapıp az değişir"; 37 kasın 27'si lokomosyon bölgesinin 15° içinde tepe yapıyor | Johnson 2008 |

**Diz moment kolu tam listesi (varsayılan diz açısı −120°, mm):**

| kas | r | kas | r |
|---|---|---|---|
| STa | −15,46 | RF | +3,70 |
| STp | −14,97 | VL | +3,73 |
| BFp | −13,77 | VI | +3,72 |
| GP | −12,33 | VM | +3,70 |
| GA | −9,39 | MG | −3,44 |
| Pla | −4,11 | LG | −3,23 |
| SM | −3,87 | Pop | −1,66 |

---

# B · Bulunan hatalar

## H1 — "Quad'da sarma atıldır" — YANLIŞ (en kritik)

Devir belgesi Bölüm 5.1 ve `ACIKLAMA_yontem_farklar_dogrulama.docx` şunu yazıyor: *"sarma quad'da atıldır, kas yolu ~0,03 mm değişir"*, ve buna dayanarak *"yöntem Johnson'ın düz çizgisine indirgenir, bu yüzden sonuç güvenlidir"* diyor.

**Kapat-ve-bak testi (quad diz moment kolu, −120°, mm):**

| quad'ın sarmaları | RF | VL | VI | VM |
|---|---|---|---|---|
| hepsi açık | +3,70 | +3,73 | +3,72 | +3,70 |
| hepsi kapalı | −0,65 | −1,18 | −0,61 | −0,97 |
| yalnız `femur_dist` torus | +3,71 | +3,72 | +3,72 | +3,71 |
| yalnız `femur_shaft_small` silindir | −0,68 | −1,18 | −0,61 | −0,99 |

**Sonuç:** +3,7 mm'yi tek başına `femur_dist` WrapTorus üretiyor. Sarma olmadan quadriceps modelde **fleksör** oluyor (negatif işaret) ve moment kolu ~1 mm'ye düşüyor. Silindir diz moment koluna hiç karışmıyor.

**Yarıçap taraması** — moment kolu torusun `inner_radius` alanına bağlı:

| `inner_radius` | quad ortalama r |
|---|---|
| 2 mm | 2,94 mm |
| 3 mm | 3,35 mm |
| **4 mm (modeldeki)** | **3,71 mm** |
| 5 mm | 4,02 mm |

**0,03 mm nereden geldi:** `wrap.py` torus hesabı yapamıyor; torusun yerine merkezine 6 mm yarıçaplı bir küre koyuyor (yarıçapı `outer_radius` alanından alıyor). Quad çizgisi o merkezden 10,3 mm uzaktan geçiyor, yani küreye 4,3 mm boşlukla değmiyor. Temas bulunmayınca yol düz kalıyor ve iki uzunluk hesabı arasındaki fark 0,03 mm çıkıyor. **Bu sayı modelin değil, `wrap.py`'nin kendi ikamesinin ölçüsüdür.**

## H2 — "6 kemik" — YANLIŞ, doğrusu 5

`.osim` dosyasında 6 `Body` var ama biri `ground` (kemik değil, sabit referans çerçevesi). Gerçek segmentler: spine, pelvis, femur, tibia, foot.
Johnson da beş sayıyor: iğneler spine, hip, femur, tibia ve foot segmentlerine yerleştirilmiş.

## H3 — "38 kas (Johnson ve ark., 2008)" — atıf yanlış

Johnson makalesi **37 kas** modellendiğini yazıyor. Fark semitendinosus'tan: Johnson iki origin (accessory, primary) ama tek insertion veriyor; port bunu STa ve STp diye iki kas yapmış. 38, portun sayısıdır.

## H4 — "38 kasın tümü doğru anatomik bağlantılarla üretilmiştir" — kas yolu için savunulamaz

Portta 38 kasın hepsi tam iki noktalı. Johnson ise Tablo 6'da quadriceps'in dört başı, TA, EDL, TP, FDL, FHL ve Peronei için birer **via point** kaydetmiş. Port, makalenin kas yolu topolojisini yeniden üretmiyor.

Ek olarak koordinatlar birebir değil: portun quad insertion'ı tibia çerçevesinde (2,6 · 37,5 · 0,5) mm, Johnson'ınki (2,03 · 40,99 · 1,68) mm.

## H5 — "İki bağımsız yöntem" — bağımsız değil

`ma_validate.py` OpenSim'in `computeMomentArm` fonksiyonunu çağırıyor, `clean_ma.py` kas boyunu `getLength` ile alıp merkezi farkla türev alıyor. **İkisi de aynı kas yolunu ve aynı sarma motorunu kullanıyor.** Uyuşma türevin doğruluğunu gösterir, geometrinin doğruluğunu göstermez.

## H6 — Johnson'ın moment kolu tanımı farklı

Özet `r = −dL/dθ` yazıyor. Johnson moment kolunu, kas etki doğrultusundaki birim vektör ile insertion'ın eklem merkezine göre yarıçap vektörünün dış çarpımı olarak tanımlıyor. Bu modelin dizinde eklem merkezi açıyla kaydığı için iki tanım aynı sayıyı vermek zorunda değil.

## H7 — Lokomosyon penceresi Johnson'ınkiyle aynı değil

Johnson'ın dörtayak lokomosyon diz aralığı **−110° … −60°**. Bu çalışmanın trot aralığı **−123° … −54°**, iki uçta da daha geniş. "Johnson'ın aralığında" denemez.

## H8 — `ma_validate.py` çıktısındaki eklem aralığı sahte

Çıktı `knee_flx` aralığını ±572,96° gösteriyor. Sebep: `build_osim.py` koordinat aralıklarını `.osim`'den kopyalamıyor, yeniden kurulan modelde eklem limiti yok. Moment kolu hesabını bozmuyor ama yanıltıcı.

## H9 — "Sarma hamstringde moment kollarını güvenilmez kılıyor" — abartılı

Kapat-ve-bak testi (−120°, mm):

| kas | sarma açık | sarma kapalı | fark |
|---|---|---|---|
| SM | −3,87 | −3,87 | 0,00 |
| BFp | −13,77 | −14,16 | +0,40 |
| STa | −15,46 | −15,39 | −0,07 |
| STp | −14,97 | −14,79 | −0,18 |
| GP | −12,33 | −12,33 | 0,00 |
| GA | −9,39 | −9,37 | −0,02 |

STp'nin **yol uzunluğu** sarmayla 45,9 → 72,5 mm şişiyor (26,6 mm), ama **diz moment kolu** yalnız 0,18 mm oynuyor. Yol uzunluğu ile moment kolu ayrı büyüklüklerdir. Yol uzunluğu şişmesi Faz-2'de lif boyu ve Hill kuvveti için sorun yaratır; diz moment kolu için yaratmaz.

**Bunun poster açısından değeri:** semimembranosus'un −3,87'si sarmadan tamamen bağımsızdır. Posterdeki en savunulabilir sayı budur.

---

# C · Johnson'ın via point'i ile karşılaştırma

Johnson Tablo 6'daki via point'ler bu modelin çerçevesine taşınıp sarma kapatılarak ölçüldü (port ile Johnson arasındaki insertion farkı kadar rijit kaydırma uygulandı).

| | RF | VL | VI | VM |
|---|---|---|---|---|
| torus sarma (mevcut model) | +3,70 | +3,73 | +3,72 | +3,70 |
| Johnson via point, sarma yok | +1,30 | +1,01 | +1,51 | +1,02 |
| ikisi de yok | −0,65 | −1,18 | −0,61 | −0,97 |

**Okunuşu:** Johnson'ın via point'i **işareti** düzeltiyor (dördü de pozitif, quadriceps ekstansör oluyor) ama büyüklüğü 1,0–1,5 mm'de bırakıyor ve **kümelenme kayboluyor** (1,01 ile 1,51 arası yayılıyor).

**Sonuç:** dört başın 0,03 mm içinde kümelenmesi torusun imzasıdır, anatominin bulgusu değildir. Dördü de aynı çemberin üstünden geçtiği için aynı yarıçapı alıyor.

**Uyarı:** bu taşıma kabadır. Yön göstergesi olarak güvenilir, kesin sayı olarak değil.

---

# D · Doğrulanmayanlar

| Konu | Durum |
|---|---|
| Johnson Şekil 3'teki quad eğrisiyle karşılaştırma | **Yapılmadı.** Tek eksik geometri doğrulaması budur. |
| OpenSim'in `WrapTorus` iç algoritması | Yeniden yazılmadı. Sonucun `inner_radius`'a bağlı olduğu ölçüldü, temas geometrisi çözülmedi. |
| Fietkiewicz ve ark. 2023, 2025 atfı | **Bu oturumda doğrulanmadı.** Devir dosyasına göre 2025 bir bioRxiv ön baskısı ve gövdesi tek eklemli iki tendonlu bir MuJoCo modeli — yani buradaki yöntem değil. Sunumdan önce PDF açılıp kontrol edilecek. |
| Johnson'ın 7 sıçanının hangi kısmının bu porta girdiği | Bilinmiyor. Portu yapan kişi belli değil. |

---

# E · Muhtemel hakem soruları ve hazır cevaplar

**"+3,7 mm nereden geliyor?"**
Modelde quadriceps'in yolu iki noktalıdır. O yolu femurun distal ucundaki sarma yüzeyi öne iter ve moment kolu o yüzeyin yarıçapına oturur. Johnson aynı işi bir via point ile çözer; OpenSim portunda via point yoktur.

**"Johnson'ın eğrisiyle karşılaştırdınız mı?"**
Hayır. Yapılacak işler listesinde ilk sıradadır.

**"İki bağımsız yöntemle doğruladık diyorsunuz, ne bağımsız?"**
Türev alma yöntemleri bağımsızdır, kas yolu ve sarma motoru ortaktır. Uyuşma türevi doğrular, geometriyi doğrulamaz.

**"NEURON çıktısı nerede?"**
Nöron modeli henüz yazılmadı. Özet metnindeki ifade kapsamı aşmaktadır.

**"Ön uzuv nerede?"**
Johnson ve ark. 2008 bir arka bacak modelidir. Sunum kapsamı arka bacakla sınırlıdır.

**"Tırıs verisi nereden?"**
Ayak yörüngesinden ters kinematikle üretilmiş belirlenmiş bir rekonstrüksiyondur. Ölçülmüş hayvan verisi değildir.

**"Tek bacakla tırıs gösterilebilir mi?"**
Hayır. Tırıs bacaklar arası eşgüdüm gerektirir. Halka açık model tek arka bacaktır; kapsam buna göre daraltılmıştır.

---

# F · Oturum 6 eki (1 Eylül 2026) — r_tamdongu_v3 II sütunu: belge-uygulama tutarsızlığı

**Doğrusu ne olmalıydı:** 46_ §5b, II formülünü `f = 14,43·d + 21,25·sign(v)·|v|^0,358`
diye belgeler. sign(v) fizyolojik olarak da doğru yöndür: iğcik, kas kısalırken ateşlemeyi
AZALTIR; hız terimi kısalmada eksi katkı vermelidir.

**Ölçülen:** r_tamdongu_v3.csv'nin II sütunu `f = 14,43·d + 21,25·|v|^0,358` (mutlak hız)
ile üretilmiş — kısalma hızı da ateşlemeyi ARTIRIYOR. Kimlikleme: vincent_bicim_testi.py
üç adayı (sign'lı ham / 0-kırpılmış / |v|) CSV'nin 10 bilinen değerine karşı koştu;
yalnız |v| adayı tuttu (maks fark 0,0005; sign adayları 126,3 / 76,1). Ia sütunu belgeyle
tutarlı (maks fark 0,0005).

**Etki ölçümü (bileşeni değiştirip sayıyı yeniden alma):** Vincent biçim sınamasında
Ia/II derinlik oranı medyanı |v| biçimiyle 2,431, sign biçimiyle 2,148 (hedef 2,544) —
sınama iki biçimde de geçer, bulgu Oturum 6 sonucunu devirmez. Ama v3'ün II eğrilerinin
salınım-kısalma fazındaki yüksek değerleri bu tutarsızlığın ürünüdür; Faz 3'te II'yi devre
girdisi yapmadan önce karar gerekir (belgeyi mi uygulamaya, uygulamayı mı belgeye uydurmalı —
karar Deniz'in; çekirdek-dokunulmazlık kuralı gereği CSV kendiliğinden değiştirilmedi).
**Oturum 7 kapanışı:** r_tamdongu_v3.1 [r31_uret.py] belgeyle uyumlu sign(v) biçimini resmîleştirdi;
bu oturumda pipeline canlı kurulup r_tamdongu_v3.1 Deniz'in yüklediği CSV ile 0 farkla yeniden üretildi;
biçim sınaması medyan 2,148, 35/35 bandda. Karar KAPANDI.

---

# G · Oturum 7 eki (1 Eylül 2026) — Varejão gerilimi yeniden değerlendirmesi + pipeline canlı doğrulama

**Bu oturumda ortam:** OpenSim 4.6 bu container'a kuruldu; çekirdek (faz1a.osim, smooth.mot, u_swing_v2)
+ JSON'lar projeden indirildi; rt_ara sahneden yeniden üretildi. 49_ zorunlu salınım kapısı:
`u_stance_pipeline` u_swing_v2'yi **medyan 0,0174** farkla yeniden üretti (49_/50_ hedefiyle birebir;
maks 0,0401 @ %87,5 FDL). Sonra u_stance_v5, r_tamdongu_v3.1, ib_drive_v3 canlı koşuldu ve Deniz'in
yüklediği CSV'lerle **maks fark 0** (byte düzeyinde aynı). Yani aşağıdaki geometri canlı, doğrulanmış sahneden.
Üreten: `geo_varejao.py` (+ cop_direct_v1.json, cop_dienes.json).

**Terim:** s = CoP'nin ayak ekseni üzerindeki kesirli konumu; s=0 topuk istasyonu (V_CAL, calcaneus),
s=1 parmak istasyonu (V_TOE). Bu eksende — geo_varejao.py'nin x-izdüşümüyle doğrulandı — MTP eklemi
s=0,674, yük yastığı (digital pad) s≈0,64–0,69 (Greene B19).

**Doğrusu ne olmalıydı:** Sıçan digitigrad yürür; yükü ayağın ön ucundaki metatars/parmak yastığı taşır.
O zaman stance boyunca CoP ayak ekseninde ileride, yastık/MTP dolayında (s≈0,66+) olmalı. Varejão ilk
temasın parmakla olduğunu bildiriyorsa, temas anında CoP distal (yüksek s) beklenir.

**Ölçülen (doğrudan CoP, cop_direct_v1.json + geo_varejao.py):**
- İlk temas (%0): CoP s = **0,376** (marker±2mm/ölçek bandı 0,341–0,428). Bilek ayak ekseninde s=0,173'te;
  CoP bileğin 6,0 mm önünde. Yastık s=0,665; CoP yastığın **0,289 gerisinde** (orta-metatars). Üst-bant
  (en distal tahmin) s=0,428 bile yastığın 0,212 gerisinde → okuma "yastık değil" sonucuna dayanıklı.
- Erken/orta stance: s %0→33 arası 0,38→0,55 (orta-ayak); yastığa (s≈0,66) ancak %36'da ulaşıyor.
- %39 sonrası s KARARSIZ (0,93 → 2,43 → negatif): ayak dikleşiyor (topuk→parmak eğimi %0 −28° → %42 −87°),
  yatay açıklık xt−xh 30 mm → %36'da 9 mm → %42'de 1,7 mm → payda sıfıra gidiyor. Bu, cop_dienes'in
  "%62 sonrası güvenilmez" bayrağıyla AYNI sebep (payda→0). Erken stance (%0–33) bu rejimin dışında, s sağlam.
- Türetilmiş CoP (cop_dienes.json) karşılaştırma: erken/orta stance s=0,49–0,58 (orta-ayak); ilk %5 NaN
  (hesaplanamıyordu — B23'ün "doğrudan çelişki kanıtlanamaz" kaydının sebebi).

**Bulgu:** faz_is_plani_v4 karnesindeki Varejão kartı "doğrudan CoP %0'da parmak bölgesini gösteriyor →
gerilim büyük olasılıkla türetmenin erken-stance zayıflığından" diyor. Bu cümle **verisiyle tutmuyor**:
doğrudan CoP %0'da parmak/yastık değil, orta-metatarsta (s=0,376); türetilmiş CoP'nin orta-ayak konumunu
tekrarlıyor, parmağa taşımıyor. Kartın kendisi zaten "henüz YAPILMADI" diyordu — o cümle koşulmadan yazılmış
bir beklentiydi. Gerilim ÇÖZÜLMEDİ.

**Ne yeni doğrulandı (türetmenin yapamadığı):** doğrudan CoP ilk kez %0'ı verdiği için (türetmede NaN'dı),
ilk temasta yükün bileğin önünde ve topuğun yüksüz olduğu artık %0'da gösterilebiliyor — İYİ kartının
"digitigrad duruş kendiliğinden" cümlesi GÜÇLENDİ (%0'a genişledi). Bu, Varejão'dan ayrı bir iddiadır ve sağlamdır.

**Derinlik (gerilim kısmen kategori karışıklığı):** Varejão KİNEMATİK bir temas olayını ölçer (hangi parça
önce yere değiyor). Model CoP KİNETİK bir büyüklüktür (yük binince bileşke kuvvet nerede). Parmaklar önce
değip neredeyse sıfır yük taşırken, yük metatarsa binerken CoP metatars altında olabilir — ikisi zorunlu
çelişki değil. Kalan gerçek soru dar: CoP digitigrad bir sıçana göre fazla mı proksimal (yastığın 0,29 gerisi)?
Bu proksimal sapmanın baş şüphelisi z_a/ρ ölçek varsayımları (B23) + Fig 4'ün tek-tipik-adım olması (24 hayvan
ortalaması değil), gerilimin "çözülmesi" değil.

**Doğrulanmadı (bu oturumda):** Varejão'nun kendi ölçümü birincil kaynaktan görülmedi — makale proje
dosya listesinde o adla yok; "parmak-önce temas" oturum kaydından (47_ B16/B23) alınan nitel ifadedir.
Varejão'nun temas kinematiğini sayıyla sabitlemek makaleyi ister.

**Karne önerisi (Deniz onayına):** Varejão satırı KARIŞIK kalır; "parmak bölgesini gösteriyor → çözüldü"
cümlesi çıkar; yerine: *"Doğrudan CoP ilk temasta bileğin 6 mm önünde ama yük yastığının proksimalinde
(s≈0,38; bant 0,34–0,43). Digitigrad/topuk-yüksüz duruş doğrulanır (İYİ). Parmak-önce temas ile orta-ayak
CoP kısmen kinematik–kinetik ayrımıdır; kalan proksimal sapma z/ρ ölçek bandına bağlı açık sınır. Geç-stance
s'i ayak dikleşmesiyle (%39+) tanımsız."*

---

# H · Oturum 7 eki (1 Eylül 2026) — Arka bacak KAPALI DÖNGÜ yürüyüş

**Ortam:** §G ile aynı canlı, doğrulanmış sahne (pipeline u_swing_v2'yi medyan 0,0174 farkla; v5 / r_tamdongu_v3.1 / ib_drive_v3'ü Deniz'in CSV'leriyle 0 farkla yeniden üretti). Kapalı döngü bu sahnenin üstüne kuruldu.

**Soru:** Arka bacağın tamamı (yalnız bilek değil), farklı hızlarda, u(t) ve r(t) canlıyken yürüyen bir KAPALI döngü üretilebilir mi?

**Zincir (tek doğrusal hat):** CPG faz φ̇=ω → ileri-besleme u_ff(φ) [SO v5 + swing v2, resmî deliverable] her kasa dağılır → aktivasyon dinamiği a(t) → Hill kuvveti F = a·Fmax·fL·fV·cosα → moment kolu r(q) ile eklem torku → çok-cisim ileri dinamiği (kalça+diz+bilek fleksiyonu) → hareket → kas boyu/hızı → iğcik r(t) [Ia/II] → refleks servo Δu = G·(r − r_ref(φ)) → u'ya geri. Döngü kapanır. Hız ω çevrilince aynı örüntü hızlanır, refleks farkı kapatır.

**Dört doğrulama kapısı (her sayının yanında üreten dosya):**

**Gate 1 — çok-cisim dinamiği** [`gate1_dyn.py`]: OpenSim M(q) (`calcM`) + bias b = `IDSolver.solve(·, u̇=0)` çıkarıldı; L=[hip_flx, knee_flx, ankle_flx] alt-sistemi partition edildi (q̈_L = M_LL⁻¹(τ_L − b_L − M_LP·q̈_P)). Kimlik M·q̈+b=τ_full artığı **2,2e-16** (5 fazda); partition q̈_L yeniden-üretim hatası **≤4,1e-13 rad/s²**. Referans ROM: kalça 56,4° · diz 32,1° · bilek 33,5° (gerçek yürüyüş genlikleri).

**Gate 2 — kas modeli tutarlılığı** [`gate2_ref.py` → `cl_ref.npz`]: (a) OpenSim lm0 == rt_ara lm **5,2e-15 m**; (b) lif hızı kimliği vlm = −Σ_k r_k·(lmt−tsl)/lm·q̇_k (OpenSim sonlu-farkıyla ~1e-12; rt_ara ile medyan **2,2e-6 m/s**, tek sapma CF %72'de wrapping artefaktı); (c) τ_ID(pipeline TAU) == τ_full(IDSolver) bacak DOF **1,0e-3 N·m**.

**BULGU (d) — 38 kaslık küme gereken torkun son ~%10-12'sini karşılamıyor:** ileri-besleme u_ff'nin (referans boy/hızda) ürettiği kas torku, gereken torktan (τ_ID − Q) tepede sapıyor: hip **%12,4** (maks 2,86e-3), knee **%11,2** (4,07e-3), ankle **%10,1** (9,22e-4 N·m); rms ~6e-4. Doğrusu: bu sapma SO'nun reserve payıdır — çözüm min Σa² + W·Σrezerv² (W=1e6) torkun son ~%10'unu 38 kasla kapatamayıp reserve aktüatöre bırakır. İki yol sınandı: reserve'i "trim" olarak feedforward torka eklemek, ya da refleksin kapatması — ikisi de yürüyor (Gate 3).

**Gate 3 — refleks kapanışı işlevsel** [`cl_sim2.py`, `gate3_test.py`]: kazanç taraması GIa=0,004 GII=0,005 (GIb=0) kararlı izleme verdi: kalça **0,8°** · diz **1,5°** · bilek **3,3°** RMS sapma. YÜKSEK kazanç TERSİNE kararsızlaştırır (GIa=0,01 → 9-30° sapma, bilek klempe çarpar) — fizyolojik düşük-kazanç bandı.
- **Refleks GEREKLİ (kapat-ve-bak):** kapalı → 26/24/34° ıraksar; açık → 0,8/1,5/3,3° izler.
- **Reserve trim OLMADAN da izler:** 1,3/1,4/3,8° — geri besleme %10 reserve'i kapatır.
- **Limit-çevrim:** her eklem ~11° kaydırılmış bozuk başlangıç TEK çevrimde 0,8/1,5/3,3°'ye yakınsar (çekim havzası var → gerçek limit-çevrim).
- **Bozucu reddi:** bileğe 30 ms +0,004 N·m tork; refleks açık bozucu-sonrası çevrimde 3,0°'ye toparlar, kapalı 34°'de kalır.

**Gate 4 — değişken hız** [`cl_teslim.py` → `cl_kapali_dongu.npz` / `.png`]: aynı merkezî örüntü ω-ölçekli, periyot **0,553 / 0,387 / 0,276 s** (0,7× / 1,0× / 1,4×). Bilek ROM hızla değişiyor (yavaş −14…33°, nominal −6…29°, hızlı −2…22°) — aynı merkezî sürüş yüksek hızda farklı kinematik verir, geri besleme düzenler. **Tırıs YOK**, hepsi walk. u(t) 0-0,9 (aktivasyon 0-0,65, excitation doygunluğu %0); r(t) Ia_Sol 30-223 pps, II_Sol 0-135 pps (Vincent/Blum bandı).

**Dürüst indirgemeler (kapsam sınırı):**
1. Gövde-yer teması ve denge YOK. Leğen (sacrum 6-DOF) + küçük frontal/rotasyon DOF'ları (hip_add, hip_int, ankle_add, ankle_int, sacroiliac_flx) ölçülmüş referansı izler. İleri-dinamik olan, yürüyüşü yapan sagittal kalça+diz+bilek zinciridir.
2. Stance yükü ölçülmüş Lewis GRF'sinden prescribe edilir (Q_GRF, faz-indeksli, swing'de sıfır) — döngüden ÇIKMAZ, dışarıdan verilir. Tek prescribe edilen dış terim.
3. CPG sabit-hızlı faz osilatörüdür (φ̇=ω); ritim henüz duyusal modüle edilmez (stance→swing yük/Ib-kapılı değil). Döngü UZUV hareketinde kapalı, RİTİMDE değil.
4. Mimari ileri-besleme + geri besleme (servo): merkezî sürüş = SO u(t); refleks = Ia/II sapma servosu. Otonom CPG (örüntüyü sıfırdan üreten) değil.
5. Bacak geometrisi referans-faza tablolu: r0(φ) sabit alınır (Δq_leg ile değişimi ihmal); lm bacak sapmasıyla momentkolu kimliğinden güncellenir. Küçük-sapma birinci-mertebe yaklaşımı; sapma qref±0,6 rad'da klemplenir.

**Ne KANITLANDI:** r(t), kararlı bütün-bacak yürüyüşü için GEREKLİ (kapatınca ıraksar) ve dış bozucuyu reddediyor; u(t) ve r(t) döngüde canlı; hız ω ile değişiyor, tırıs gerekmez. Bu, "bir şekilde yürüyen kapalı döngü"nün UZUV-DÜZEYİ kanıtıdır.

**Kalan iş:** (1) duyusal ritim — Ib/yük ile stance→swing kapısı, ritmi de kapat; (2) gövde ilerlemesi / yer teması modeli (gerçek lokomosyon, tek prescribe terimi kaldır); (3) otonom CPG — örüntüyü feedback'ten üret, u_ff bağımlılığını azalt.

---

# I · Oturum 7 eki (1 Eylül 2026) — EMERGENT (referanssız) kapalı döngü yürüyüş

**Soru (Deniz):** Ölçülmüş referansı izleyen değil, sürüşü anatomiden, ritmi duyudan, yükü gerçek yer temasından gelen, kendi kendine yürüyen bir kapalı döngü. "Yüzde yüz olmayacağını biliyorum (OpenSim, sabit ayak, iğcik-verisi yetersizliği, kaslar) — yapabildiğimizin en iyisi olsun."

**Yaklaşım (§H'den fark):** §H'de üç şey ölçümden geliyordu (sürüş=SO u(t), ritim=sabit saat, hedef=referans q). Üçü de söküldü. Sürüş = **anatomik sinerji** (stance: kalça ekstansör + quad; swing: kalça fleksör), gruplar moment kolu işaretinden [stage1_analiz.py]. Ritim = **kalça-açısı sonlu-durum denetleyici** (stance→swing kalça ekstansiyon eşiğinde; kedi/rat lokomosyonunda faz değişkeni kalçadır). Yük = **gerçek ayak-yer teması** (parmak istasyonu yer düzlemine inince yay-sönüm, Q=F·∂p/∂q ile eklem torkuna). Referans servo YOK.

**Altyapı:** bacak artık ölçülmüş yol etrafında kalmadığı için geometri/dinamik referans-fazına göre değil, **kalça×diz×bilek 3B ızgarasında** tablolandı [stage0_grid.py → cl_grid3d.npz, 13³=2197 nokta, 36 s]: her nokta için moment kolu R[3][38], lif boyu, M_leg[3][3], yerçekimi bias, ayak istasyonu dünya konumu. Canlı trilineer interpolasyon.

**Ne EMERGENT çıktı (kilitli config, cl_emergent.py; cl_emergent.npz/.png):**
- Kalça kendiliğinden salınıyor: **21°..58°** (genlik 37°), temiz ve tekrarlı.
- Diz referans bandında eşlik ediyor: **−123°..−107°** (quad iki fazda tutar; ~15° salınım), limitten uzak, kararlı.
- **Kapalı kalça-diz limit-çevrimi** (faz-portresi kapalı halka → gerçek çekici).
- Ritim duyusaldan doğuyor: kadans **3,3 Hz** (periyot 0,30 s), stance oranı **0,64** (walk).
- Gerçek ayak teması: kuvvet **0,44–1,18 N**, stance boyunca modüle.
- u(t) canlı, fazlı sinerji örüntüsü; r(t) canlı — hareketli kasların (kalça-ekst SM, diz-ekst VL) Ia/II'si çevrim boyunca modüle oluyor.
- **Değişken hız SÜRÜŞ YOĞUNLUĞUNDAN** doğuyor (saat değil): kalça sürüşü ×0,85 / ×1,0 / ×1,15 → **3,0 / 3,3 / 3,6 Hz**. Hayvan gibi: daha çok itki → daha hızlı adım.

**Ne TUTULUYOR / sınır (dürüst):**
1. **Ayak −35°'de (plantarfleksiyon grid limiti) çakılı, dinamik değil.** İndirgenmiş model bu hafif, iğcik-verisi zayıf eklemi kaslardan kararlı süremiyor: açık-döngü ko-kontraksiyon bir limite kayıyor, pozitif uzunluk (II) refleksi yüksek kazançta kararsızlaştırıyor, PD temas torkuyla eziliyor. Ayak plantarfleksiyonda (digitigrad, toe-down) tutulur — temas sağlar ama havada-swing (aerial clearance) yoktur; ayak çevrimin çoğunda yüklü (yürüyüş değil, "yerinde adım / koşu bandı sürtme" kinematiği).
2. **Biçim-topolojisi bulgusu:** modelde TEMIZ diz fleksörü yok — diz fleksörleri (STa/STp/BFp/GP) aynı zamanda kalça ekstansörü. Swing'de aktif diz fleksiyonu kalça fleksiyonunu baltalar; bu yüzden diz aktif bükülemedi, quad'la TUTULDU. Bu Johnson portunun via-point'siz iki-noktalı yollarının (H4) dinamik sonucudur.
3. **Afferent büyüklükleri model ekstrapolasyonu:** SM Ia tepe ~600 pps çıkıyor (kalça çok gerildiği için); Blum/Vincent fit aralığının (≤~250 pps) ötesi. Yön doğru, mutlak değer güvenilmez.
4. **Distal limit-çevrim yalnız marjinal kararlı:** kilitli config 6 s boyunca kararlı, ama küçük parametre değişimi çöküşe (hip/knee/ankle köşe limitlerine) atlatıyor. Tam kararlı bir distal çekici bu indirgenmiş modelde (gerçek temas mekaniği yok, sabit ayak, hafif segmentler) YOK. Bu bir bulgu, gizlenen bir başarısızlık değil.

**Karşılaştırma:** §H'nin referans-tabanlı döngüsü fizyolojik olarak sadık ve sağlam kararlı tam-bacak kapalı döngüdür (kalça+diz+bilek izler, refleks gerekli, bozucu reddi). §I emergent döngü referans-sadakatini özerklikle değiştirir ve indirgenmiş modelin sınırına dayanır: kalça+diz+ritim+yük emergent, ayak tutulu. İkisi projenin iki ucudur — biri sadık, biri özerk.

**Kalan iş (özerkliği ilerletmek):** gerçek çok-cisim temas + gövde ağırlığı desteği (sabit-ayak/hafif-eklem sorununu kaldırır); modele temiz diz fleksörü (kısa-baş biceps) + via-point eklemek (aktif swing diz fleksiyonu); iğcik fitini fizyolojik aralıkta doyurmak (SM Ia patlamasını önler); optimizasyon-tabanlı kazanç ayarı (elle ayarın kırılganlığını aşar).

**Dosyalar:** `stage0_grid.py` (3B ızgara), `stage1_analiz.py` (sinerji/rol çıkarımı), `cl_emergent.py` (emergent çekirdek: FSM+sinerji+temas+refleks), `cl_emergent_teslim.py` (teslim koşusu+şekil), `cl_emergent.png/.npz`.

---

# J · Oturum 7 eki (1 Eylül 2026) — Ayak/diz model doğrulaması (PCSA + fleksör anatomisi)

**Bağlam:** Emergent döngüde ayak plantarfleksiyon limitine çakılıyordu; "model hatası mı, kontrol hatası mı" sorusunu Deniz'in yüklediği birincil kaynağa (Scaling of muscle architecture and fiber types in the rat hindlimb, Tablo 1–2) karşı sınadım.

**Check 1 — kas kuvvetleri (Fmax) DOĞRU, birincil kaynakla tutarlı.** Model Fmax'ini Tablo 1 PCSA'sına böldüm; özgül gerilim σ=Fmax/PCSA **19 kasta medyan 20,8 N/cm² (std 3,5)** — neredeyse sabit. Yani faz1a.osim'in Fmax'i tam olarak bu tablodan σ≈20,8 ile türetilmiş. (Tek görünür sapma Per σ=36; sebebi modeldeki Per'in PerL+PerB birleşimi olması, 0,19+0,14=0,33 alınınca σ=20,7.) Üreten: `kas_par`/`cl_grid3d` Fmax vs Tablo 1.
- Bu §A'daki "build_osim.py 10 N yer tutucu koyuyor" endişesini KAPATIR: çalıştığım faz1a.osim yer tutucu değil, gerçek PCSA-türevi Fmax kullanıyor, doğrulandı.
- Ayak: Sol Fmax **1,34 N DOĞRU** (PCSA 0,07 = en küçük plantarfleksör; Tablo 2: %80 tip I, yavaş postural kas). Plantarfleksör/dorsifleksör baskınlığı: oran kas kümesine bağlı — PCSA {Sol,MG,LG,Pla}/{TA,EDL,PerL,PerB}=**1,80**; kod-alt-kümesi {Sol,MG,LG}/{TA,EDL}=**2,48**; tam anatomi Fmax≈**2,61**; tork-kapasite (Fmax×momentkolu)≈**2,78**. [ERRATUM: bu satır ilk yazımda "2,18" diyordu — tutarsız bir alt-kümeydi; denetim (Oturum 7b, §K) düzeltti. Yön aynı, ama baskınlık ~2,5-2,8, yani bilek problemi buradaki çerçevelemeden BİRAZ DAHA ZOR.]
- **Sonuç:** emergent döngüde ayağın plantarfleksiyona çökmesi MODEL HATASI DEĞİL. Denetleyicim dorsifleksöre, 2,2× güçlü plantarfleksörü dengeleyecek orantılı sürüş vermedi (kontrol-tarafı hata). Kazanç optimizasyonuyla düzelir; modele dokunmaya gerek yok.

**Check 2 — temiz (monoartiküler) diz fleksörü: modelde yok, ve sıçanda da muhtemelen yok.** Modelin bütün diz fleksörleri biartiküler (BFp hip−10,7/knee−13,8; STa −12,8/−15,6; STp −7,6/−15,2; GP −14,9/−12,4 mm); BFa üç eklemde de momentkolu ~0 (işlevsiz); Pop knee −1,6 (küçük). Tablo 1 biceps femoris'i **tek** kas olarak listeliyor (biartiküler hamstring, 2670 mg, en büyük); ayrı bir monoartiküler diz fleksörü yok. "Knee flexors" grubu biartiküler hamstring+gastroc.
- **Sonuç:** modelin temiz diz fleksöründen yoksun olması anatomiye SADIK görünüyor (kesin model-kaynağı için Johnson 2008 açılmalı). Modele monoartiküler diz fleksörü eklemek anatomi uydurmak olur. Sıçanda swing diz fleksiyonu biartiküler eşgüdüm + pasif dinamiktir; denetleyici bunu üretmeli, model bir kas eklemeyle "düzeltilmemeli". Güven: Tablo 1'den güçlü çıkarım; birincil-kaynak nitel (rat myoloji atlası ile pekişir).

**Check 3 — katı vs elastik tendon:** literatür sorusu değil, model-ayarı testi (Aşil esnekliği ankle'da fark yaratır mı). Ertelendi, düşük öncelik.

**Karar:** çekirdek .osim'e DOKUNMA — hem ayak kuvvetleri hem diz-fleksör tamamlayıcısı anatomik sadık. Emergent döngünün sınırları kontrol-tarafı (ayak sürüş dengesi) + gerçek biartiküler/pasif diz fleksiyonu + yapısal katı-ayak/MTP eksikliği (§G/§I). Poster açısından yan ürün: **PCSA doğrulaması (σ=20,8) modelin kuvvetlerini birincil kaynağa karşı doğrular** — sunulabilir bir doğrulama.

---

# K · Oturum 7b eki (1 Eylül 2026) — Emergent döngü DENETİMİ (Deniz) + düzeltmeler

Deniz emergent kodu belge-denetimi protokolüyle inceledi; bulgular büyük ölçüde doğru çıktı ve kod/kayıt buna göre düzeltildi. Bulgular ve yanıtlar:

**B1 — r(t) [Ia/II] döngüyü TAŞIMIYORDU (en kritik, kabul edildi).** Denetim ölçümü: `GIa=0` ritmi bozmuyordu (Ia atıl); `II` hesaplanıp loglanıyor ama excitation'a hiç beslenmiyordu (ölü, `grep` ile doğrulandı — yalnız `e+=GIa*Ia*0.001`); hız terimi `clip(vlm,-20,20)` tipik lif hızında (~34 mm/s) sürekli satüreydi. Döngüyü taşıyan tek geri besleme `load=Fy/Fref` (üstelik GRF proxy'si, gerçek Golgi/Ib değil). Yani posterin/brief'in "iğcik afferenti r(t) [Ia/II] döngüyü taşıyor" ifadesi o kodla YANLIŞTI.
- **Düzeltme [cl_emergent.py]:** II excitation'a bağlandı; Ia+II artık FAZIK (kendi EMA-ortalamalarından sapma, τ_ema=0,12 s) → ortalaması ~0, yani **yapısal** geri besleme (sabit sürüş seviyesiyle taklit edilemez); hız doyumu VCAP 20→45 mm/s. GIa/GII gerçek, tunable kazançlar (PARSPEC'te 0–3).

**B2 — G9 kapısı yapıyı değil büyüklüğü test ediyordu (kabul edildi).** Eski G9 `GIa=GIb=0` yapıyordu; ama `GIb*load` stance'te taban sürüşe %66 ekliyor (load≈0,35, GIb×load≈0,106 > Ahe=0,16'nın yarısından çok), yani sıfırlamak geri beslemeyle birlikte ekstansör sürüşünün çoğunu da kaldırıyordu. Çöküş "yapı zorunlu"yu değil "ekstansör bu sürüşsüz zayıf"ı gösteriyordu.
- **Düzeltme [cl_selfcheck.py]:** G9 artık YAPISAL test — geri beslemeyi faz-ortalaması SABİT ileri-beslemeyle değiştir (`fb='meanff'`); yürüyüş sabitle de ayakta kalıyorsa geri besleme yapısal değildi.
- **İLK ÖLÇÜM (kilitli config, düzeltme sonrası): G9 KALIYOR.** live 7 geçiş / meanff 16 geçiş, ikisi de nearlim 1,0 — sabit-ortalama geri besleme yürüyüşü bozmuyor (hatta iyileştiriyor). Yani **mevcut config'te gerçek yapısal kapalı döngü YOK**; FSM (kalça proprioseptif kapısı) + feedforward + sürüş seviyesi taşıyor. Bunu optimizasyonun G9'u geçirerek çözmesi gerekiyor; geçemezse "bu indirgenmiş modelde r(t) yapısal döngüyü taşıyamıyor" dürüst sonucu.
- Not: FSM'nin STANCE→SWING kapısı kalçanın eşiğe inmesini gerektiriyor ve kalçayı indiren yük geri beslemesi — yani bir tür kapanış var, ama G9'un test ettiği "iğcik r(t) yapısal katkısı" ölçütünü mevcut config geçmiyor.

**B3 — §J PF/DF oranı gevşekti (düzeltildi).** §J "2,18" diyordu; tutarsız alt-küme. Doğrusu kümeye bağlı: PCSA tam 1,80; kod-alt-kümesi 2,48; Fmax 2,61; tork-kapasite 2,78. Baskınlık ~2,5-2,8 → bilek nötrü için gereken cdf/cpf~3,0; PARSPEC cdf tavanı 0,15→**0,25** genişletildi (marj için). §J satırı düzeltildi.

**B4 — GMi ters işaretli (düzeltildi).** `HIP_FLX` içinde GMi'nin hip momentkolu çalışma bandında ters (−0,5..−0,16 mm) → gruba karşı çalışıyordu. GMi HIP_FLX'ten çıkarıldı.

**B5 — ölü/yanıltıcı kod (temizlendi).** `DISTAL`, `STANCE_SYN`, `KNE_FLX` (yalnız DISTAL'ı besliyordu), `Foff` atıldı; "monoartiküler" yorumu (BFp/STp aslında biartiküler — §J ile çelişiyordu) kaldırıldı. Artık kod, döngüde olmayan bir bileşen varmış izlenimi vermiyor.

**Denetimin doğrulayamadıkları (dürüstlük):** afferent katsayıları (10,43; 26,59; 27,08; 14,43; 21,25 ve üsteller) bu denetim oturumunda birincil kaynaktan görülmedi — ama 46_/02 (Oturum 6) kayıtlarında Blum 2020 (Ia) ve Vincent 2017 (II) birincil kaynaklarına karşı doğrulanmıştı; kod yorumuna bu referans eklendi.

**Net durum:** kod ve kapılar artık dürüst. "u(t)/r(t) kapalı döngü" iddiası mevcut config'te G9'dan KALIYOR (yapısal değil) — bu, optimizasyonun geçirmesi gereken hedef; poster iddiası ancak G9 geçtikten sonra edilebilir.

---

# K.2 · Oturum 7c eki (2 Eylül 2026) — Denetimin 2. turu (Deniz): bilek çakılması bir SAYISAL artefakt

Deniz 7b düzeltmelerini içeren paketi yeniden denetletti. Düzeltmeler doğrulandı (II besleniyor, Ia/II fazik, VCAP=45, GMi çıkmış, ölü kod atılmış, G9 meanff-yapısal, §J erratum). En kritik YENİ bulgu: emergent döngüde bileğin -35°'ye çakılması bir kontrol dengesi hatası DEĞİL, açık-Euler entegrasyonunun bilek DOF'unda yakınsamamasıdır. Brief, §J, §K/7b ve ilk denetimin turn-1 statik tork hesabı bunu kontrol hatası sanıyordu — hepsi yanlıştı; hiçbiri dt duyarlılığına bakmamıştı.

**Kanıt (üreten: cl_emergent.run, dt taraması, aynı oturum):**
- Bilek eylemsizliği çok küçük: M[ankle,ankle]=1,1e-7, M[hip,hip]=1,4e-5 → ~120×. Bilek ivmesi 1e4-1e5 rad/s²; dt=1e-4'te açık Euler bu stiff DOF'ta kararsız (salınıp grid limitine çakılıyor, `wa=0` ile kilitleniyor).
- dt duyarlılığı: dt=1e-4 → bilek -35..-35; dt=5e-5 → +55 (öteki limite çakılı); dt=3e-5 → knee -155'e çakılı; dt=2e-5 → bilek 15..24 (canlı); dt=1e-5 → 15..24 (2e-5 ile BİREBİR aynı = yakınsak). En büyük yakınsak dt = 2e-5.
- Artefakt kontrolü kilitliyordu: dt=1e-4'te bilek cdf'den bağımsız (cdf=0,06..0,25 → hep -35). dt=2e-5'te bilek cdf'ye monoton yanıt verir: cdf=0,06→-35..-15; 0,10→-9..7; 0,135→23..42; 0,18→38..55. Yani sayısal düzeltme brief'in "cdf ile ayağı dengele" planını ARTIK uygulanabilir kılar. Fizyolojik nötr için cdf≈0,10 (cdf/cpf≈2,2 — turn-1'in ~3,0 statik tahmininden düşük; statik hesap dinamiği ve yerçekimi katkısını atlamıştı).

**Düzeltme [cl_emergent.py, cl_selfcheck.py]:** varsayılan dt 1e-4 → 2e-5 (`run` ve `_run`). Bu bir çekirdek-sim (entegratör) düzeltmesidir, kontrol değişikliği değil; brief'in "yalnız parametre" kapsamı korunur. Maliyet: sim ~5× yavaş; CMA-ES çok çekirdekli makinede hâlâ pratik.

**Yeni dürüst baseline (üreten: cl_selfcheck.verify, dt=2e-5):**
- Kilitli config (cdf=0,06): G3 hâlâ kalıyor (ankle -35), ama artık GERÇEK kontrol nedeniyle (zayıf DF sürüşü), artefakt değil.
- Elle dengeli config (cdf=0,10 Adf=0,10): G1,G2,G3,G4,G5,G7,G8 GEÇER (ankle -17..4, hip 21..56, knee -139..-124, stance 0,55, kadans 2,0Hz) — 9 kapının 7'si. G6 (temas modülasyonu) ve G9 (yapısal döngü) KALIR. PASS_kritik yalnız G9'dan kalıyor.
- Sonuç: ayak-limit sorunu (§J/§K/7b'nin baş konusu) çözüldü; kalan iki kapı gerçek bilim (temas modülasyonu + r(t)'nin yapısal katkısı), sayısal değil. CMA-ES artık DOĞRU dinamiğe karşı optimize eder.

**Küçük düzeltmeler:** (1) fazik gerekçe düzeltildi — 7b'deki kod yorumu ve §K "fazik → ~0 ortalama → sabitle taklit edilemez" diyordu; ama FAZ-BAZLI ortalama ~0 değil (üreten: refl_stance/swing_mean; VL swing 0,10, Sol swing -0,058, TA swing 0,048). meanff testi yine geçerli — faz-ortalamalarını GERÇEK değeriyle sabitler, geriye faz-içi zamanlamayı test eder; gerekçe buna göre düzeltildi. (2) ölü değişken `SPINDLE` atıldı (7b'nin ölü-kod temizliğinin kendisi bir ölü değişken bırakmıştı). (3) G9 ölü-yürüyüşte (live<6 geçiş) True dönebiliyor; G1 ve fitness'ın n_transition<6 erken-dönüşü bunu PASS_kritik'e taşımıyor — bilinen, korumalı.

**Doğrulanamayanlar:** dt=5e-6 ile 2e-5'in ötesinde yakınsama teyidi koşu-süre limitini aştı; iddia "2e-5 yakınsak (1e-5 ile birebir)", "daha küçük dt farklı verir" değil. Tam CMA-ES koşulmadı (oturum tek çekirdekli, cma yok); PASS_kritik'in erişilebilirliği elle bir config ile 7/9'a (G3 dahil) kadar gösterildi, G9 açık kaldı. Bağımsız okuyucu-göz turu yapılmadı (o araç bu arayüzde yok); uygulayıcı-göz turu (kodu bizzat işletmek) yapıldı ve dt bulgusu ondan çıktı.

---

# K.3 · Oturum 7c eki (2 Eylül 2026) — 7c denetiminin BAĞIMSIZ doğrulaması (bulut oturumu)

Deniz 7c paketini (`rat_emergent_cc_7c`) + `55_CC_DEVIR.md`'yi bu oturuma getirdi; §K.2'nin dt-artefakt bulgusunu bağımsız koşuyla sınadım. **Doğrulandı, her noktada.**

**Ölçtüğüm (üreten: cl_emergent.run, cl_selfcheck.verify, 7c paketi):**
- Bilek eylemsizliği: M[ankle,ankle]=1,13e-7, M[hip,hip]=1,17e-5 → **oran 104×** (§K.2 "~120×" ile aynı mertebe; küçük fark hangi config/ortalama). Bilek gerçekten hip'in ~1/100'ü.
- dt yakınsaması (cdf=0,10): dt=1e-4 → bilek -35..54, son-yarı ort **-35 (çakılı)**; dt=2e-5 → **4..10**; dt=1e-5 → **5..10** (2e-5 ile birebir). Yani **2e-5 yakınsak, 1e-4 sahte artefakt** — §K.2 doğru.
- Kapı okuması (cdf=0,10 Adf=0,10, dt=2e-5, verify): **G3 GEÇER** (bilek -9..7, kalça 21..56, diz -139..-125, stance 0,57, kadans 2,0Hz); G6 (temas 0,18 vs 0,14N, oran ~1,3) ve **G9 (yapısal: live 5 geçiş vs meanff 10 — meanff bozmuyor)** KALIR. §K.2'nin "7/9, G6+G9 kalır" tablosuyla birebir. (G1 bende Tsim=2,5 kısa olduğu için düştü — sanal, uzun koşuda geçer.)

**Değerlendirme:** 7c denetimi doğru ve titiz; dt-artefakt bulgusu benim §J/§K çerçevememi **düzeltiyor** — bileği "kontrol dengesi" sanıp dt=1e-4'te optimize etmeye çalışmışım (o arama artefaktla dövüşüyormuş, boşa gitmiş). Ne ben ne turn-1 statik-tork denetimi dt duyarlılığına bakmıştık; 7c baktı. `run`/`_run` varsayılan dt=2e-5 doğru düzeltmedir, korunmalı.

**Kalan iki kapı gerçek bilim, sayısal değil:** G6 (swing'de ayak yerden kalkmıyor → temas modüle olmuyor; muhtemelen katı-ayak/MTP yapısal sınırı), G9 (r(t) yapısal döngüyü taşımıyor — meanff sabitiyle yürüyüş bozulmuyor). Poster "u(t)/r(t) kapalı döngü" iddiası ancak G9 dürüstçe geçerse edilebilir. `55_CC_DEVIR.md`'nin üç sınır-uyarısı (G9'u zorlama, G6 yapısal olabilir birkaç turdan sonra bırak, çekirdeğe/dt'ye dokunma) doğru; onaylıyorum. CMA-ES artık DOĞRU dinamiğe (dt=2e-5) karşı koşulmalı.

---

# L · Oturum 7d eki (3 Eylül 2026) — CMA-ES optimizasyonu: 9/9 kapı geçti (yerel koşu, 32 çekirdek)

**Görev:** 54/55 brief'i uyarınca `cl_emergent.py` denetleyicisinin 13 parametresini (PARSPEC) CMA-ES ile optimize etmek; dt=2e-5, çekirdek dosyalar ve denetleyici yapısı dokunulmadan. Kapılar ve fitness `cl_selfcheck.py`'den, DEĞİŞTİRİLMEDİ.

**Koşum zinciri (log dosyalarıyla):**
1. Baseline selfcheck (kilitli config, dt=2e-5) [log1_baseline_selfcheck.txt]: G3/G5/G6 kalır (ankle -35..-35 çakılı); selfcheck'in kendi default'u cdf=0,06'dır — §K.2'nin "7/9 geçer" dediği elle-config (cdf=0,10) değil.
2. CMA-ES koşum 1 (Tsim=3 arama, popsize=32, workers=32) [log2]: maliyet 234→1,79 (jen 33); worker spawn hatasıyla (WinError 87) düştü, en iyi `cl_best.json`'a kayıtlıydı.
3. Koşum 2 (ılık başlangıç, 150 jen, Tsim=3) [log3]: maliyet 1,79→0,056. **Tsim=6 doğrulamada G3 KALDI** (ankle -35..-4, nearlim 0,48): kısa-ufuk optimumu 3 s'den sonra bileği yavaşça limite sürüklüyor, arama penceresi bunu görmüyordu.
4. Koşum 3 (ders uygulandı: **arama ufku Tsim=6'ya eşitlendi** — kapılar/fitness aynı, yalnız değerlendirme penceresi doğrulamayla eşit; sıkılaştırma, deformasyon değil) [log4]: maliyet 2,73→0,097 (son iyileşme jen 46; sonrası iyileşmesiz). **verify(P, Tsim=6): 9/9 kapı GEÇER, PASS_kritik=True, PASS=True.**

**Optimizasyon tarafında yapılan değişiklikler (yalnız `cl_optimize.py`, koşum konfigürasyonu):** workers 8→32, popsize 16→32; `cl_best.json` varsa ılık başlangıç (sigma=0,10); arama Tsim 3→6. Çekirdek (.osim/.mot/kas_par/grid), dt=2e-5, `cl_emergent.py` ve `cl_selfcheck.py` dokunulmadı.

**Kapı okuması (üreten: cl_optimize.py nihai verify [log4]; aynı P ile deterministik yeniden-koşu cl_teslim_9of9.py birebir aynı sayıları verdi):** kadans 2,9 Hz; stance 0,58; hip 26..52° (ROM 26°); knee -141..-129°; ankle 18..19°; live nearlim 0,00; Fc stance 0,167 N / swing 0,112 N; refl_HE std 0,101. En iyi P [cl_best_9of9.json]: Ahe=0,276 Ake=0,297 cpf=0,002 cdf=0,040 Apf_st≈0,0003 Ahf=0,598 Adf=0,023 **GIb=0,015 GIa=0,091 GII=0,059** kc=137 hip_ext=26,3° hip_flx=50,7°.

**G9 yapısal kanıt (asıl hedef; üreten: log4 + cl_teslim_9of9.png son panel):** canlı geri beslemeyle bilek 6 s boyunca 18..19°'de, limitten uzak (nearlim 0,00); geri besleme faz-ortalaması SABİTle değiştirilince (`meanff`) bilek ~3. saniyede +55° dorsifleksiyon limitine tırmanıp çakılıyor (nearlim 1,00, son yarı 51..55°). G9, nearlim ölçütünden geçer (1,00 > 0,00+0,05). Yani iğcik r(t)'nin FAZ-İÇİ zamanlaması bileği limitten uzak tutan şeydir — sabit sürüş seviyesiyle taklit edilemez; **yapısal kapalı döngü bu modelde İLK KEZ nesnel olarak gösterildi** (§K/K.2'de açık kalan kapı). Dip not (dürüstlük): verify çıktısındaki "live geçiş 17 vs meanff 39" iki farklı metriği karıştırır — live_tr yalnız SWING→STANCE basışlarını, meanff_tr TÜM geçişleri sayar; elmalı-elmalı karşılaştırma 34 vs 39'dur (üreten: cl_teslim_9of9.py). Bu, G9'un geçiş-sayısı ölçütünü yalnız TUTUCU yönde saptırır (meanff_tr şişkin → ölçüt 1 zor ateşlenir); G9 zaten nearlim ölçütünden geçti, sonuç etkilenmez. Ayrıca fitness'taki yapısal-ödül terimi de aynı karışık metriği kullanır (struct_gap'ın geçiş terimi); nearlim bileşeni baskın olduğundan sonuç değişmez ama gelecek oturum isterse düzeltebilir.

**Dürüst çekinceler (formal 9/9'a rağmen):**
1. **Bilek +18..19°'de dorsiflekste park etmiş (ROM ~1°).** Brief'in hedefi ayağı toe-down ~-25..0° bandına oturtmaktı ve "ayağı dorsifleksiyonda cycle ettirme" uyarısı vardı; G4'ün formal bandı (-40..35) geçiyor ama optimizasyon G3'ü, ayağı toe-down band içinde SÜREREK değil, dorsiflekste sabit tutup yükü küçülterek çözdü.
2. **Yük taşıma minimal:** Fc stance ortalaması 0,167 N (baseline 1,30 N'du); G6 eşiği (0,167 > 0,112×1,3=0,146) kıl payı. Çevrim İÇİ modülasyon gerçek ve net (0→0,33 N her adımda; şekil panel 2) ama FSM stance'iyle kısmen faz-kaymalı — stance/swing ORTALAMA farkını küçülten bu kayma. GIb'nin 0,015'e çökmesi tutarlı: yük refleksi fiilen kapalı, döngüyü iğcik (GIa/GII) taşıyor.
3. **Diz ROM'u 12°** (-141..-129); minimum G4 alt sınırına (-150) 9° mesafede.
4. Ia SM ~300-560 pps — Blum fit aralığının (≲250) üstü; §I madde 3'ün ekstrapolasyon çekincesi bu config'te de geçerli.

**Yorum:** kapılar dürüstçe, deformasyonsuz geçildi ve G9 kanıtı güçlü — iğcik geri beslemesinin yapısal gerekliliği artık nesnel. Ama rejim "yük taşıyan toe-down yürüyüş"ten çok "minimal-yük ritim"dir: optimizasyon, katı-ayak/MTP'siz modelde yük ile limit-uzaklığını aynı anda bulamayıp yükü küçülten çözüme gitti. Bu, 54'ün "gerçek stance yuvarlanması ancak MTP ile gelir" yapısal sınırıyla tutarlı. Poster iddiası "u(t)/r(t) yapısal kapalı döngü (G9 nesnel)" olarak edilebilir; "yük taşıyan digitigrad yürüyüş" iddiası bu config ile EDİLMEMELİ. Toe-down + daha yüksek yük istenirse iki yol: (a) mevcut kapılar içinde farklı başlangıçlarla yeni arama (G9'u bozma riski var), (b) MTP eklemi (Deniz onaylı ayrı iş).

**Dosyalar:** `cl_best_9of9.json` (en iyi P), `cl_optimize.py` (ılık başlangıç + Tsim=6 arama), `cl_teslim_9of9.py` → `cl_teslim_9of9.png/.npz` (zaman serileri + faz portresi + G9 live-vs-meanff), `log1..log4` (koşum kayıtları). Kopyalar: `tum/04_kapali_dongu_ESKI/`.
