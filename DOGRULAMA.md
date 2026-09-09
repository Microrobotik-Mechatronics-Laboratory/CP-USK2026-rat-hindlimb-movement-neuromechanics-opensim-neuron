# DOĞRULAMA KAYDI

Bu dosya, projede kullanılan her sayının **bağımsız olarak nasıl ölçüldüğünü** kaydeder.
Her bölüm bir ölçüm oturumudur ve tarihlidir. Bölümlerin düzeni: *ne ölçüldü · nasıl ölçüldü ·
sonuç · üreten dosya*.

Kurallar:

- Kayıtlar **tarihli tutanaklardır ve sonradan içerik olarak düzenlenmezler**; yalnız terim ve
  dil düzeltmesi yapılır (05.09.2026 terim denetimi).
- Konum: bu dosya `04_kapali_dongu/02_DOGRULAMA_KAYDI.md` iken 05.09.2026'da repo köküne
  `DOGRULAMA.md` olarak alındı.
- İçlerinde geçen dosya adları yazıldıkları günün klasör düzenine göredir. Bugünkü karşılıkları:
  `kod/kopru/` (canlı hat), `arsiv/kod/opensim/` ve `arsiv/kod/kapali_dongu/` (07.09.2026'da
  arşivlendi, versiyon kontrolünde), `veri/kapali_dongu/`, `sekiller/`, `arsiv/` (aşılmış
  sürümler). Güncel klasör haritası: `README.md`.
- Bilimsel iddiaların kendisi `PREPRINT.md`'dedir; bu dosya onların kanıt tabanıdır.

---

# A · Doğrulanan sayılar

**Ölçüm tarihi:** 27.07.2026

**Yöntem:** OpenSim **4.6** kuruldu (`pip install opensim --break-system-packages`). Repodaki
betikler (`build_osim.py`, `ma_validate.py`, `clean_ma.py`, `peak_ma.py`) çalıştırıldı.
`rat_hindlimb_0.2.osim` dosyası XML olarak ayrıştırıldı. Johnson ve ark. 2008 tam metni
PMC2322854'ten okundu.

Aşağıdaki her satır bu oturumda ölçülmüştür. Önceki oturumlardan gelen belgelerdeki hiçbir sayı
doğrulanmış sayılmamıştır.

| İddia | Ölçülen | Üreten |
|---|---|---|
| Quad diz moment kolu ≈ +3,7 mm | RF +3,70 · VL +3,73 · VI +3,72 · VM +3,70 | `ma_validate.py` |
| Aynı sayı, ikinci yöntemle | RF +3,70 · VL +3,74 · VI +3,72 · VM +3,71 | `clean_ma.py` |
| Semimembranosus ≈ −3,9 mm | −3,87 | her iki betik |
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

## H1 — "Quadriceps'te sarmanın etkisi yok" iddiası yanlış (en kritik)

Önceki oturumdan gelen belgenin bölüm 5.1'i ve `ACIKLAMA_yontem_farklar_dogrulama.docx` şunu
yazıyor (alıntı): *"sarma quad'da atıldır, kas yolu ~0,03 mm değişir"*; buna dayanarak
*"yöntem Johnson'ın düz çizgisine indirgenir, bu yüzden sonuç güvenlidir"* sonucuna varıyor.

**Sarma kapatılarak yapılan karşılaştırma** (quad diz moment kolu, −120°, mm):

| quad'ın sarmaları | RF | VL | VI | VM |
|---|---|---|---|---|
| hepsi açık | +3,70 | +3,73 | +3,72 | +3,70 |
| hepsi kapalı | −0,65 | −1,18 | −0,61 | −0,97 |
| yalnız `femur_dist` torus | +3,71 | +3,72 | +3,72 | +3,71 |
| yalnız `femur_shaft_small` silindir | −0,68 | −1,18 | −0,61 | −0,99 |

**Sonuç:** +3,7 mm'yi tek başına `femur_dist` WrapTorus üretiyor. Sarma olmadan quadriceps
modelde **fleksör** oluyor (negatif işaret) ve moment kolu ~1 mm'ye düşüyor. Silindirin diz
moment koluna katkısı yok.

**Yarıçap taraması** — moment kolu torusun `inner_radius` alanına bağlı:

| `inner_radius` | quad ortalama r |
|---|---|
| 2 mm | 2,94 mm |
| 3 mm | 3,35 mm |
| **4 mm (modeldeki)** | **3,71 mm** |
| 5 mm | 4,02 mm |

**0,03 mm nereden geliyor:** `wrap.py` torus hesabı yapamıyor; torusun yerine merkezine 6 mm
yarıçaplı bir küre koyuyor (yarıçapı `outer_radius` alanından alıyor). Quad çizgisi o merkezden
10,3 mm uzaktan geçiyor, yani küreye 4,3 mm boşlukla değmiyor. Temas bulunmayınca yol düz kalıyor
ve iki uzunluk hesabı arasındaki fark 0,03 mm çıkıyor. **Bu sayı modelin değil, `wrap.py`'nin
kendi ikamesinin ölçüsüdür.**

## H2 — "6 kemik" yanlış; doğrusu 5

`.osim` dosyasında 6 `Body` var ama biri `ground` (kemik değil, sabit referans çerçevesi).
Gerçek segmentler: spine, pelvis, femur, tibia, foot. Johnson da beş sayıyor: işaretleyici
iğneler spine, hip, femur, tibia ve foot segmentlerine yerleştirilmiş.

## H3 — "38 kas (Johnson ve ark., 2008)" atfı yanlış

Johnson makalesi **37 kas** modellendiğini yazıyor. Fark semitendinosus'tan geliyor: Johnson iki
origin (accessory, primary) ama tek insertion veriyor; OpenSim aktarımı bunu STa ve STp diye iki
kas yapmış. 38, aktarımın sayısıdır.

## H4 — "38 kasın tümü doğru anatomik bağlantılarla üretilmiştir" — kas yolu için savunulamaz

Aktarılan modelde 38 kasın hepsi tam iki noktalıdır. Johnson ise Tablo 6'da quadriceps'in dört
başı, TA, EDL, TP, FDL, FHL ve Peronei için birer **via point** kaydetmiştir. Aktarım, makalenin
kas yolu topolojisini yeniden üretmiyor.

Koordinatlar da birebir değil: aktarımın quad insertion'ı tibia çerçevesinde (2,6 · 37,5 · 0,5) mm,
Johnson'ınki (2,03 · 40,99 · 1,68) mm.

## H5 — "İki bağımsız yöntem" iddiası — yöntemler bağımsız değil

`ma_validate.py` OpenSim'in `computeMomentArm` fonksiyonunu çağırıyor; `clean_ma.py` kas boyunu
`getLength` ile alıp merkezi farkla türev alıyor. **İkisi de aynı kas yolunu ve aynı sarma
motorunu kullanıyor.** Uyuşma türevin doğruluğunu gösterir, geometrinin doğruluğunu göstermez.

## H6 — Johnson'ın moment kolu tanımı farklı

Özet metni `r = −dL/dθ` yazıyor. Johnson moment kolunu, kas etki doğrultusundaki birim vektör ile
insertion'ın eklem merkezine göre yarıçap vektörünün dış çarpımı olarak tanımlıyor. Bu modelin
dizinde eklem merkezi açıyla kaydığı için iki tanımın aynı sayıyı vermesi zorunlu değildir.

## H7 — Lokomosyon penceresi Johnson'ınkiyle aynı değil

Johnson'ın dörtayak lokomosyon diz aralığı **−110° … −60°**. Bu çalışmanın trot aralığı
**−123° … −54°**, iki uçta da daha geniş. "Johnson'ın aralığında" denemez.

## H8 — `ma_validate.py` çıktısındaki eklem aralığı geçersiz

Çıktı `knee_flx` aralığını ±572,96° gösteriyor. Sebep: `build_osim.py` koordinat aralıklarını
`.osim`'den kopyalamıyor, yeniden kurulan modelde eklem sınırı yok. Moment kolu hesabını
bozmuyor ama yanıltıcı.

## H9 — "Sarma hamstringde moment kollarını güvenilmez kılıyor" iddiası abartılı

Sarma kapatılarak yapılan karşılaştırma (−120°, mm):

| kas | sarma açık | sarma kapalı | fark |
|---|---|---|---|
| SM | −3,87 | −3,87 | 0,00 |
| BFp | −13,77 | −14,16 | +0,40 |
| STa | −15,46 | −15,39 | −0,07 |
| STp | −14,97 | −14,79 | −0,18 |
| GP | −12,33 | −12,33 | 0,00 |
| GA | −9,39 | −9,37 | −0,02 |

STp'nin **yol uzunluğu** sarmayla 45,9 → 72,5 mm artıyor (26,6 mm), ama **diz moment kolu**
yalnız 0,18 mm değişiyor. Yol uzunluğu ile moment kolu ayrı büyüklüklerdir. Yol uzunluğundaki
artış Faz-2'de lif boyu ve Hill kuvveti için sorun yaratır; diz moment kolu için yaratmaz.

**Bunun poster açısından değeri:** semimembranosus'un −3,87 mm'si sarmadan tamamen bağımsızdır.
Posterdeki en savunulabilir sayı budur.

---

# C · Johnson'ın via point'i ile karşılaştırma

Johnson Tablo 6'daki via point'ler bu modelin çerçevesine taşınıp sarma kapatılarak ölçüldü
(aktarım ile Johnson arasındaki insertion farkı kadar rijit kaydırma uygulandı).

| | RF | VL | VI | VM |
|---|---|---|---|---|
| torus sarma (mevcut model) | +3,70 | +3,73 | +3,72 | +3,70 |
| Johnson via point, sarma yok | +1,30 | +1,01 | +1,51 | +1,02 |
| ikisi de yok | −0,65 | −1,18 | −0,61 | −0,97 |

**Okunuşu:** Johnson'ın via point'i **işareti** düzeltiyor (dördü de pozitif, quadriceps ekstansör
oluyor) ama büyüklüğü 1,0–1,5 mm'de bırakıyor ve **kümelenme kayboluyor** (1,01 ile 1,51 arası
yayılıyor).

**Sonuç:** dört başın 0,03 mm içinde kümelenmesi torusun ürettiği yapay bir sonuçtur, anatomik
bir bulgu değildir. Dördü de aynı çemberin üstünden geçtiği için aynı yarıçapı alıyor.

**Uyarı:** bu taşıma kabadır. Yön göstergesi olarak güvenilir, kesin sayı olarak değil.

---

# D · Doğrulanmayanlar

| Konu | Durum |
|---|---|
| Johnson Şekil 3'teki quad eğrisiyle karşılaştırma | **Yapılmadı.** Tek eksik geometri doğrulaması budur. |
| OpenSim'in `WrapTorus` iç algoritması | Yeniden yazılmadı. Sonucun `inner_radius`'a bağlı olduğu ölçüldü, temas geometrisi çözülmedi. |
| Fietkiewicz ve ark. 2023, 2025 atfı | **Bu oturumda doğrulanmadı.** Önceki oturumdan gelen belgeye göre 2025 bir bioRxiv ön baskısıdır ve gövdesi tek eklemli iki tendonlu bir MuJoCo modelidir — yani buradaki yöntem değildir. Sunumdan önce PDF açılıp kontrol edilecek. |
| Johnson'ın 7 sıçanının hangi kısmının bu aktarıma girdiği | Bilinmiyor. Aktarımı yapan kişi belli değil. |

---

# E · Sorulabilecek sorular ve hazır cevaplar

**"+3,7 mm nereden geliyor?"**
Modelde quadriceps'in yolu iki noktalıdır. O yolu femurun distal ucundaki sarma yüzeyi öne iter
ve moment kolu o yüzeyin yarıçapına oturur. Johnson aynı işi bir via point ile çözer; OpenSim
aktarımında via point yoktur.

**"Johnson'ın eğrisiyle karşılaştırdınız mı?"**
Hayır. Yapılacak işler listesinde ilk sıradadır.

**"İki bağımsız yöntemle doğruladık diyorsunuz, ne bağımsız?"**
Türev alma yöntemleri bağımsızdır; kas yolu ve sarma motoru ortaktır. Uyuşma türevi doğrular,
geometriyi doğrulamaz.

**"NEURON çıktısı nerede?"**
27.07.2026 itibarıyla nöron modeli henüz yazılmamıştı; özet metnindeki ifade o tarihte kapsamı
aşıyordu. Bugünkü durum için bkz. bölüm N ve O.

**"Ön uzuv nerede?"**
Johnson ve ark. 2008 bir arka bacak modelidir. Sunum kapsamı arka bacakla sınırlıdır.

**"Tırıs verisi nereden?"**
Ayak yörüngesinden ters kinematikle üretilmiş belirlenmiş bir rekonstrüksiyondur. Ölçülmüş
hayvan verisi değildir.

**"Tek bacakla tırıs gösterilebilir mi?"**
Hayır. Tırıs bacaklar arası eşgüdüm gerektirir. Halka açık model tek arka bacaktır; kapsam buna
göre daraltılmıştır.

---

# F · 01.09.2026 — `r_tamdongu_v3` II sütunu: belge ile uygulama arasında tutarsızlık

**Ne olması gerekiyordu:** 46_ §5b, II formülünü `f = 14,43·d + 21,25·sign(v)·|v|^0,358` diye
belgeliyor. `sign(v)` fizyolojik olarak da doğru yöndür: iğcik, kas kısalırken ateşlemeyi
azaltır; hız terimi kısalmada eksi katkı vermelidir.

**Ölçülen:** `r_tamdongu_v3.csv`'nin II sütunu `f = 14,43·d + 21,25·|v|^0,358` (mutlak hız) ile
üretilmiş — yani kısalma hızı da ateşlemeyi artırıyor. Belirleme yöntemi: `vincent_bicim_testi.py`
üç adayı (sign'lı ham / 0-kırpılmış / |v|) CSV'nin 10 bilinen değerine karşı koşturdu; yalnız |v|
adayı tuttu (maksimum fark 0,0005; sign adaylarında 126,3 ve 76,1). Ia sütunu belgeyle tutarlıdır
(maksimum fark 0,0005).

**Etki ölçümü (bileşen değiştirilip sayı yeniden alındı):** Vincent biçim sınamasında Ia/II
derinlik oranı medyanı |v| biçimiyle 2,431, sign biçimiyle 2,148 (hedef 2,544) — sınama iki
biçimde de geçiyor, bulgu Oturum 6 sonucunu geçersizleştirmiyor. Ancak v3'ün II eğrilerinin
salınım-kısalma fazındaki yüksek değerleri bu tutarsızlığın ürünüdür; Faz 3'te II devre girdisi
yapılmadan önce karar gerekir (belge mi uygulamaya, uygulama mı belgeye uydurulacak). Çekirdek
dosyaya dokunulmazlık kuralı gereği CSV kendiliğinden değiştirilmedi.

**Kapanış (Oturum 7):** `r_tamdongu_v3.1` [`r31_uret.py`] belgeyle uyumlu `sign(v)` biçimini
resmîleştirdi. Aynı oturumda işlem hattı canlı kurulup `r_tamdongu_v3.1` yüklenen CSV ile 0 farkla
yeniden üretildi; biçim sınaması medyan 2,148, 35/35 bandda. Karar kapandı.

---

# G · 01.09.2026 — Varejão gerilimi ve işlem hattının canlı doğrulaması

**Çalışma ortamı:** OpenSim 4.6 bu ortama kuruldu; çekirdek dosyalar (`faz1a.osim`, `smooth.mot`,
`u_swing_v2`) ve JSON girdileri projeden indirildi; `rt_ara` yeniden üretildi.

**Zorunlu salınım kontrolü (49_):** `u_stance_pipeline` `u_swing_v2`'yi **medyan 0,0174** farkla
yeniden üretti (49_/50_ hedefiyle birebir; maksimum 0,0401 @ %87,5 FDL). Ardından `u_stance_v5`,
`r_tamdongu_v3.1` ve `ib_drive_v3` canlı koşuldu ve yüklenen CSV'lerle **maksimum fark 0**
(bayt düzeyinde aynı). Aşağıdaki geometri bu doğrulanmış ortamdan gelmektedir.
Üreten: `geo_varejao.py` (+ `cop_direct_v1.json`, `cop_dienes.json`).

**Tanım:** s = basınç merkezinin (CoP) ayak ekseni üzerindeki kesirli konumu; s = 0 topuk
istasyonu (V_CAL, calcaneus), s = 1 parmak istasyonu (V_TOE). Bu eksende — `geo_varejao.py`'nin
x-izdüşümüyle doğrulandı — MTP eklemi s = 0,674, yük yastığı (digital pad) s ≈ 0,64–0,69
(Greene B19).

**Beklenti:** sıçan digitigrad yürür; yükü ayağın ön ucundaki metatars/parmak yastığı taşır. Buna
göre stance boyunca CoP ayak ekseninde ileride, yastık/MTP dolayında (s ≈ 0,66+) olmalıdır.
Varejão ilk temasın parmakla olduğunu bildiriyorsa, temas anında CoP distal (yüksek s) beklenir.

**Ölçülen (doğrudan CoP; `cop_direct_v1.json` + `geo_varejao.py`):**

- İlk temas (%0): CoP s = **0,376** (marker ±2 mm / ölçek aralığı 0,341–0,428). Bilek ayak
  ekseninde s = 0,173'te; CoP bileğin 6,0 mm önünde. Yastık s = 0,665; CoP yastığın **0,289
  gerisinde** (orta-metatars). Üst aralık (en distal tahmin) s = 0,428 bile yastığın 0,212
  gerisindedir; okuma "yastık değil" sonucuna dayanıklıdır.
- Erken/orta stance: s, %0→33 arasında 0,38→0,55 (orta-ayak); yastığa (s ≈ 0,66) ancak %36'da
  ulaşıyor.
- %39 sonrası s kararsız (0,93 → 2,43 → negatif): ayak dikleşiyor (topuk→parmak eğimi %0'da
  −28°, %42'de −87°), yatay açıklık x_t − x_h 30 mm → %36'da 9 mm → %42'de 1,7 mm; payda sıfıra
  gidiyor. Bu, `cop_dienes`'in "%62 sonrası güvenilmez" uyarısıyla aynı sebeptir. Erken stance
  (%0–33) bu rejimin dışındadır ve s sağlamdır.
- Türetilmiş CoP (`cop_dienes.json`) ile karşılaştırma: erken/orta stance s = 0,49–0,58
  (orta-ayak); ilk %5 NaN (hesaplanamıyordu — B23'ün "doğrudan çelişki kanıtlanamaz" kaydının
  sebebi budur).

**Bulgu:** `faz_is_plani_v4` değerlendirme tablosundaki Varejão satırı, "doğrudan CoP %0'da parmak
bölgesini gösteriyor → gerilim büyük olasılıkla türetmenin erken-stance zayıflığından" diyordu.
Bu ifade **veriyle tutmuyor**: doğrudan CoP %0'da parmak/yastıkta değil, orta-metatarsta
(s = 0,376); türetilmiş CoP'nin orta-ayak konumunu tekrarlıyor, parmağa taşımıyor. Satırın kendisi
zaten "henüz yapılmadı" diyordu; o cümle ölçüm yapılmadan yazılmış bir beklentiydi. Gerilim
çözülmedi.

**Yeni doğrulanan (türetmenin veremediği):** doğrudan CoP ilk kez %0'ı verdiği için (türetmede
NaN'dı), ilk temasta yükün bileğin önünde ve topuğun yüksüz olduğu artık %0'da gösterilebiliyor.
"Digitigrad duruş kendiliğinden ortaya çıkıyor" iddiası %0'a genişledi. Bu, Varejão'dan ayrı bir
iddiadır ve sağlamdır.

**Değerlendirme (gerilim kısmen kategori farkından):** Varejão **kinematik** bir temas olayını
ölçer (hangi parça önce yere değiyor). Model CoP'si **kinetik** bir büyüklüktür (yük binince
bileşke kuvvet nerede). Parmaklar önce değip neredeyse sıfır yük taşırken yük metatarsa binerse
CoP metatars altında olabilir; ikisi zorunlu olarak çelişmez. Kalan gerçek soru dardır: CoP,
digitigrad bir sıçana göre fazla mı proksimal (yastığın 0,29 gerisi)? Bu proksimal sapmanın baş
nedeni z_a/ρ ölçek varsayımları (B23) ve Şekil 4'ün tek tipik adım olmasıdır (24 hayvan ortalaması
değil). Bu, gerilimin çözülmesi anlamına gelmez.

**Doğrulanmadı:** Varejão'nun kendi ölçümü birincil kaynaktan görülmedi — makale proje dosya
listesinde o adla yok; "parmak-önce temas" ifadesi oturum kaydından (47_ B16/B23) alınan nitel
bir aktarımdır. Temas kinematiğini sayıyla sabitlemek makaleyi gerektirir.

**Değerlendirme tablosu için öneri:** Varejão satırı karışık kalır; "parmak bölgesini gösteriyor →
çözüldü" ifadesi çıkarılır; yerine: *"Doğrudan CoP ilk temasta bileğin 6 mm önünde ama yük
yastığının proksimalinde (s ≈ 0,38; aralık 0,34–0,43). Digitigrad ve topuk-yüksüz duruş doğrulanır.
Parmak-önce temas ile orta-ayak CoP arasındaki fark kısmen kinematik–kinetik ayrımıdır; kalan
proksimal sapma z/ρ ölçek aralığına bağlı açık bir sınırdır. Geç stance'te s, ayak dikleşmesiyle
(%39+) tanımsızdır."*

---

# H · 01.09.2026 — Arka bacağın referans izleyen kapalı-döngü yürüyüşü

**Çalışma ortamı:** §G ile aynı canlı ve doğrulanmış ortam (işlem hattı `u_swing_v2`'yi medyan
0,0174 farkla; `v5` / `r_tamdongu_v3.1` / `ib_drive_v3`'ü yüklenen CSV'lerle 0 farkla yeniden
üretti). Kapalı döngü bunun üstüne kuruldu.

**Soru:** arka bacağın tamamı (yalnız bilek değil), farklı hızlarda, u(t) ve r(t) canlıyken yürüyen
bir kapalı döngü üretilebilir mi?

**Zincir:** CPG fazı φ̇ = ω → ileri besleme u_ff(φ) (SO v5 + swing v2) her kasa dağılır →
aktivasyon dinamiği a(t) → Hill kuvveti F = a·F_max·f_L·f_V·cos α → moment kolu r(q) ile eklem
momenti → çok cisimli ileri dinamik (kalça + diz + bilek fleksiyonu) → hareket → kas boyu/hızı →
iğcik r(t) [Ia/II] → refleks servosu Δu = G·(r − r_ref(φ)) → u'ya geri. Hız ω değiştirilince aynı
örüntü hızlanır, refleks farkı kapatır.

**Dört kabul ölçütü (gate); her sayının yanında üreten dosya:**

**Gate 1 — çok cisimli dinamik** [`gate1_dyn.py`]: OpenSim M(q) (`calcM`) ve bias terimi
b = `IDSolver.solve(·, u̇=0)` çıkarıldı; L = [hip_flx, knee_flx, ankle_flx] alt sistemi ayrıldı
(q̈_L = M_LL⁻¹(τ_L − b_L − M_LP·q̈_P)). M·q̈ + b = τ_full özdeşliğinin artığı **2,2e-16** (5 fazda);
ayrıştırmadan gelen q̈_L yeniden üretim hatası **≤ 4,1e-13 rad/s²**. Referans hareket açıklığı:
kalça 56,4° · diz 32,1° · bilek 33,5°.

**Gate 2 — kas modeli tutarlılığı** [`gate2_ref.py` → `cl_ref.npz`]: (a) OpenSim lm0 == `rt_ara`
lm farkı **5,2e-15 m**; (b) lif hızı özdeşliği v_lm = −Σ_k r_k·(lmt − tsl)/lm·q̇_k (OpenSim sonlu
farkıyla ~1e-12; `rt_ara` ile medyan **2,2e-6 m/s**, tek sapma CF'de %72'de sarma kaynaklı);
(c) τ_ID (işlem hattı TAU) == τ_full (IDSolver) bacak serbestlik derecelerinde **1,0e-3 N·m**.

**Bulgu (d) — 38 kaslık küme gereken momentin son ~%10–12'sini karşılamıyor:** ileri besleme
u_ff'nin (referans boy ve hızda) ürettiği kas momenti, gereken momentten (τ_ID − Q) tepede
sapıyor: kalça **%12,4** (maksimum 2,86e-3), diz **%11,2** (4,07e-3), bilek **%10,1**
(9,22e-4 N·m); rms ~6e-4. Bunun nedeni statik optimizasyonun rezerv payıdır: çözüm
min Σa² + W·Σrezerv² (W = 1e6) momentin son ~%10'unu 38 kasla kapatamayıp rezerv aktüatöre
bırakır. İki yol sınandı — rezervi düzeltme terimi olarak ileri besleme momentine eklemek ya da
refleksin kapatması; ikisi de çalışıyor (Gate 3).

**Gate 3 — refleks kapanışı işlevsel** [`cl_sim2.py`, `gate3_test.py`]: kazanç taramasında
GIa = 0,004, GII = 0,005 (GIb = 0) kararlı izleme verdi: kalça **0,8°** · diz **1,5°** · bilek
**3,3°** rms sapma. Yüksek kazanç tersine kararsızlaştırıyor (GIa = 0,01 → 9–30° sapma, bilek
sınıra çarpıyor); yani fizyolojik düşük kazanç aralığı geçerli.

- **Refleks gerekli (kapatıp bakma):** kapalıyken 26/24/34° ıraksıyor; açıkken 0,8/1,5/3,3° izliyor.
- **Rezerv düzeltmesi olmadan da izliyor:** 1,3/1,4/3,8° — geri besleme %10'luk rezervi kapatıyor.
- **Limit çevrimi:** her eklemde ~11° kaydırılmış bozuk başlangıç tek çevrimde 0,8/1,5/3,3°'ye
  yakınsıyor (çekim havzası var → gerçek limit çevrimi).
- **Bozucu reddi:** bileğe 30 ms boyunca +0,004 N·m moment uygulandığında refleks açıkken
  bozucu sonrası çevrimde 3,0°'ye toparlanıyor, kapalıyken 34°'de kalıyor.

**Gate 4 — değişken hız** [`cl_teslim.py` → `cl_kapali_dongu.npz` / `.png`]: aynı merkezî örüntü
ω ile ölçeklendiğinde periyot **0,553 / 0,387 / 0,276 s** (0,7× / 1,0× / 1,4×). Bilek hareket
açıklığı hızla değişiyor (yavaş −14…33°, nominal −6…29°, hızlı −2…22°): aynı merkezî sürüş yüksek
hızda farklı kinematik veriyor, geri besleme düzenliyor. Tırıs yok, hepsi walk. u(t) 0–0,9
(aktivasyon 0–0,65, excitation doygunluğu %0); r(t) Ia_Sol 30–223 pps, II_Sol 0–135 pps
(Vincent/Blum aralığı).

**Bilinçli indirgemeler (kapsam sınırı):**

1. Gövde-yer teması ve denge yok. Pelvis (sacrum 6 serbestlik derecesi) ve küçük frontal/rotasyon
   eksenleri (hip_add, hip_int, ankle_add, ankle_int, sacroiliac_flx) ölçülmüş referansı izliyor.
   İleri dinamik olan, yürüyüşü üreten sagittal kalça + diz + bilek zinciridir.
2. Stance yükü ölçülmüş Lewis GRF'sinden verilir (Q_GRF, faz indeksli, swing'de sıfır) — döngüden
   çıkmaz, dışarıdan verilir. Dışarıdan verilen tek terim budur.
3. CPG sabit hızlı bir faz osilatörüdür (φ̇ = ω); ritim henüz duyusal olarak modüle edilmiyor.
   Döngü uzuv hareketinde kapalı, ritimde değildir.
4. Mimari ileri besleme + geri besleme (servo) biçimindedir: merkezî sürüş = SO u(t); refleks =
   Ia/II sapma servosu. Örüntüyü sıfırdan üreten özerk bir CPG değildir.
5. Bacak geometrisi referans faza göre tablolanmıştır: r0(φ) sabit alınır (Δq_leg ile değişimi
   ihmal edilir); lm, bacak sapmasıyla moment kolu özdeşliğinden güncellenir. Küçük sapma birinci
   mertebe yaklaşımıdır; sapma q_ref ± 0,6 rad'da sınırlanır.

**Gösterilen:** r(t), kararlı bütün bacak yürüyüşü için gereklidir (kapatılınca ıraksıyor) ve dış
bozucuyu reddediyor; u(t) ve r(t) döngüde canlıdır; hız ω ile değişiyor, tırıs gerekmiyor. Bu,
kapalı döngünün uzuv düzeyindeki kanıtıdır.

**Kalan iş:** (1) duyusal ritim — Ib/yük ile stance→swing geçişi, ritmi de kapatmak; (2) gövde
ilerlemesi ve yer teması modeli (dışarıdan verilen tek terimi kaldırmak); (3) özerk CPG — örüntüyü
geri beslemeden üretip u_ff bağımlılığını azaltmak.

---

# I · 01.09.2026 — Referanssız (emergent) kapalı-döngü yürüyüş

**Soru:** ölçülmüş referansı izleyen değil; sürüşü anatomiden, ritmi duyudan, yükü gerçek yer
temasından gelen, kendi kendine yürüyen bir kapalı döngü kurulabilir mi? Beklenti baştan
sınırlıdır (OpenSim, sabit ayak, iğcik verisinin yetersizliği, kas kümesi).

**§H'den farkı:** §H'de üç şey ölçümden geliyordu — sürüş (SO u(t)), ritim (sabit saat) ve hedef
(referans q). Üçü de kaldırıldı. Sürüş = **anatomik sinerji** (stance: kalça ekstansör + quad;
swing: kalça fleksör), gruplar moment kolu işaretinden [`stage1_analiz.py`]. Ritim = **kalça
açısına dayalı sonlu durum denetleyicisi** (stance→swing geçişi kalça ekstansiyon eşiğinde; kedi
ve sıçan lokomosyonunda faz değişkeni kalçadır). Yük = **gerçek ayak-yer teması** (parmak
istasyonu yer düzlemine inince yay-sönüm, Q = F·∂p/∂q ile eklem momentine). Referans servosu yok.

**Altyapı:** bacak artık ölçülmüş yörünge çevresinde kalmadığı için geometri ve dinamik, referans
fazına göre değil **kalça × diz × bilek üç boyutlu ızgarasında** tablolandı [`stage0_grid.py` →
`cl_grid3d.npz`; 13³ = 2197 nokta, 36 s]: her nokta için moment kolu R[3][38], lif boyu,
M_leg[3][3], yerçekimi bias terimi, ayak istasyonunun dünya konumu. Koşu sırasında trilineer
interpolasyon.

**Emergent çıkan davranış (kilitli config, `cl_emergent.py`; `cl_emergent.npz`/`.png`):**

- Kalça kendiliğinden salınıyor: **21°…58°** (genlik 37°), tekrarlı.
- Diz referans aralığında eşlik ediyor: **−123°…−107°** (quadriceps iki fazda tutuyor; ~15°
  salınım), sınırdan uzak ve kararlı.
- **Kapalı kalça-diz limit çevrimi** (faz portresinde kapalı halka → gerçek çekici).
- Ritim duyusaldan doğuyor: adım sıklığı **3,3 Hz** (periyot 0,30 s), stance oranı **0,64** (walk).
- Gerçek ayak teması: kuvvet **0,44–1,18 N**, stance boyunca modüle oluyor.
- u(t) canlı ve fazlı sinerji örüntüsünde; r(t) canlı — hareketli kasların (kalça ekstansörü SM,
  diz ekstansörü VL) Ia/II'si çevrim boyunca modüle oluyor.
- **Hız, sürüş yoğunluğundan** doğuyor (saatten değil): kalça sürüşü ×0,85 / ×1,0 / ×1,15 →
  **3,0 / 3,3 / 3,6 Hz**. Daha çok itki, daha hızlı adım.

**Sınırlar:**

1. **Ayak −35°'de (plantar fleksiyon ızgara sınırı) tutuluyor, dinamik değil.** İndirgenmiş model
   bu hafif ve iğcik verisi zayıf eklemi kaslardan kararlı süremiyor: açık döngü ko-kontraksiyon
   bir sınıra kayıyor, pozitif uzunluk (II) refleksi yüksek kazançta kararsızlaştırıyor, PD temas
   momenti baskın geliyor. Ayak plantar fleksiyonda (digitigrad, toe-down) tutuluyor — temas
   sağlıyor ama havada salınım (aerial clearance) yok; ayak çevrimin çoğunda yüklü. Bu, yürüyüşten
   çok "yerinde adım" kinematiğidir.
2. **Kas topolojisi bulgusu:** modelde saf bir diz fleksörü yok — diz fleksörleri (STa/STp/BFp/GP)
   aynı zamanda kalça ekstansörü. Salınımda aktif diz fleksiyonu kalça fleksiyonunu baltalıyor;
   bu yüzden diz aktif bükülemedi, quadriceps ile tutuldu. Bu, Johnson aktarımının via point'siz
   iki noktalı yollarının (H4) dinamik sonucudur.
3. **Afferent büyüklükleri model ekstrapolasyonudur:** SM Ia tepesi ~600 pps çıkıyor (kalça çok
   gerildiği için); Blum/Vincent fit aralığının (≤ ~250 pps) ötesindedir. Yön doğru, mutlak değer
   güvenilmez.
4. **Distal limit çevrimi yalnız marjinal kararlı:** kilitli config 6 s boyunca kararlı, ama küçük
   parametre değişimi çöküşe (kalça/diz/bilek köşe sınırlarına) götürüyor. Tam kararlı bir distal
   çekici bu indirgenmiş modelde (gerçek temas mekaniği yok, sabit ayak, hafif segmentler) yok.
   Bu bir bulgudur, gizlenen bir başarısızlık değil.

**Karşılaştırma:** §H'nin referans tabanlı döngüsü fizyolojik olarak sadık ve sağlam kararlı bir
tam bacak kapalı döngüsüdür (kalça + diz + bilek izliyor, refleks gerekli, bozucu reddi var).
§I'nin emergent döngüsü referans sadakatini özerklikle değiştirir ve indirgenmiş modelin sınırına
dayanır: kalça, diz, ritim ve yük emergent, ayak tutulu. İkisi projenin iki ucudur.

**Kalan iş (özerkliği ilerletmek):** gerçek çok cisimli temas + gövde ağırlığı desteği (sabit ayak
ve hafif eklem sorununu kaldırır); modele saf bir diz fleksörü (kısa başlı biceps) ve via point
eklemek (aktif salınım diz fleksiyonu); iğcik fitini fizyolojik aralıkta doyurmak (SM Ia
patlamasını önler); optimizasyon tabanlı kazanç ayarı (elle ayarın kırılganlığını aşar).

**Üreten:** `stage0_grid.py` (üç boyutlu ızgara), `stage1_analiz.py` (sinerji ve rol çıkarımı),
`cl_emergent.py` (emergent çekirdek: FSM + sinerji + temas + refleks), `cl_emergent_teslim.py`
(sonuç koşusu ve şekil), `cl_emergent.png`/`.npz`.

---

# J · 01.09.2026 — Ayak ve diz modelinin doğrulaması (PCSA + fleksör anatomisi)

**Bağlam:** emergent döngüde ayak plantar fleksiyon sınırına dayanıyordu. "Model hatası mı, kontrol
hatası mı" sorusu birincil kaynağa (*Scaling of muscle architecture and fiber types in the rat
hindlimb*, Tablo 1–2) karşı sınandı.

**Kontrol 1 — kas kuvvetleri (F_max) doğru, birincil kaynakla tutarlı.** Model F_max'i Tablo 1
PCSA'sına bölündü; özgül gerilim σ = F_max/PCSA **19 kasta medyan 20,8 N/cm² (std 3,5)** —
neredeyse sabit. Yani `faz1a.osim`'in F_max değerleri tam olarak bu tablodan σ ≈ 20,8 ile
türetilmiştir. Tek görünür sapma Per'de (σ = 36); sebebi modeldeki Per'in PerL + PerB birleşimi
olmasıdır: 0,19 + 0,14 = 0,33 alınınca σ = 20,7. Üreten: `kas_par` / `cl_grid3d` F_max değerleri
Tablo 1'e karşı.

- Bu ölçüm §A'daki "`build_osim.py` 10 N yer tutucu koyuyor" endişesini kapatır: çalışılan
  `faz1a.osim` yer tutucu değil, gerçek PCSA türevi F_max kullanıyor.
- Ayak: Sol F_max **1,34 N doğru** (PCSA 0,07 = en küçük plantar fleksör; Tablo 2: %80 tip I,
  yavaş postural kas). Plantar fleksör / dorsifleksör baskınlığı kas kümesine bağlıdır:
  PCSA {Sol, MG, LG, Pla} / {TA, EDL, PerL, PerB} = **1,80**; kod alt kümesi {Sol, MG, LG} /
  {TA, EDL} = **2,48**; tam anatomi F_max ≈ **2,61**; moment kapasitesi (F_max × moment kolu)
  ≈ **2,78**. [Düzeltme: bu satır ilk yazımında "2,18" diyordu; tutarsız bir alt kümeydi, ikinci
  denetimde (§K) düzeltildi. Yön aynı, baskınlık ~2,5–2,8, yani bilek problemi ilk çerçevelemeden
  biraz daha zordur.]
- **Sonuç:** emergent döngüde ayağın plantar fleksiyona çökmesi model hatası değildir.
  Denetleyici dorsifleksöre, 2,2× güçlü plantar fleksörü dengeleyecek orantılı sürüşü vermiyordu;
  bu kontrol tarafı bir hatadır ve kazanç optimizasyonuyla düzelir. Modele dokunmak gerekmez.

**Kontrol 2 — saf (monoartiküler) diz fleksörü modelde yok, sıçanda da muhtemelen yok.** Modelin
bütün diz fleksörleri biartikülerdir (BFp kalça −10,7 / diz −13,8; STa −12,8 / −15,6; STp −7,6 /
−15,2; GP −14,9 / −12,4 mm); BFa üç eklemde de moment kolu ~0 (işlevsiz); Pop diz −1,6 (küçük).
Tablo 1 biceps femoris'i **tek** kas olarak listeliyor (biartiküler hamstring, 2670 mg, en büyük);
ayrı bir monoartiküler diz fleksörü yok. "Diz fleksörleri" grubu biartiküler hamstring +
gastrocnemius'tur.

- **Sonuç:** modelin saf diz fleksöründen yoksun olması anatomiye sadık görünüyor (kesin model
  kaynağı için Johnson 2008 açılmalı). Modele monoartiküler diz fleksörü eklemek anatomi uydurmak
  olur. Sıçanda salınımdaki diz fleksiyonu biartiküler eşgüdüm ve pasif dinamiktir; denetleyici
  bunu üretmelidir, model bir kas eklenerek "düzeltilmemelidir". Güven düzeyi: Tablo 1'den güçlü
  çıkarım; birincil kaynak nitel (sıçan miyoloji atlası ile pekişir).

**Kontrol 3 — rijit ile elastik tendon karşılaştırması:** literatür sorusu değil, model ayarı
testidir (Aşil esnekliği bilekte fark yaratır mı). Ertelendi, düşük öncelikli.

**Karar:** çekirdek `.osim` dosyasına dokunulmaz — hem ayak kuvvetleri hem diz fleksörü tamamlayıcı
kümesi anatomik olarak sadıktır. Emergent döngünün sınırları kontrol tarafı (ayak sürüş dengesi),
gerçek biartiküler/pasif diz fleksiyonu ve yapısal rijit ayak / MTP eksikliğidir (§G, §I). Poster
açısından yan ürün: **PCSA doğrulaması (σ = 20,8) modelin kuvvetlerini birincil kaynağa karşı
doğrular** ve sunulabilir bir doğrulamadır.

---

# K · 01.09.2026 — Emergent döngünün bağımsız denetimi ve düzeltmeler

Emergent kod bağımsız bir denetimden geçirildi (denetim: Deniz); bulgular büyük ölçüde doğru
çıktı ve kod ile kayıt buna göre düzeltildi.

**B1 — r(t) [Ia/II] döngüyü taşımıyordu (en kritik; kabul edildi).** Denetim ölçümü: `GIa=0`
ritmi bozmuyordu (Ia etkisizdi); `II` hesaplanıp kaydediliyor ama excitation'a hiç beslenmiyordu
(kullanılmayan kod; `grep` ile doğrulandı — yalnız `e+=GIa*Ia*0.001` vardı); hız terimi
`clip(vlm,-20,20)` tipik lif hızında (~34 mm/s) sürekli doygundu. Döngüyü taşıyan tek geri besleme
`load=Fy/Fref` idi (üstelik GRF vekili, gerçek Golgi/Ib değil). Yani "iğcik afferenti r(t) [Ia/II]
döngüyü taşıyor" ifadesi o kodla yanlıştı.

- **Düzeltme [`cl_emergent.py`]:** II excitation'a bağlandı; Ia + II artık fazik (kendi EMA
  ortalamalarından sapma, τ_ema = 0,12 s), yani ortalaması ~0 olan **yapısal** bir geri besleme
  (sabit sürüş seviyesiyle taklit edilemez); hız doygunluğu VCAP 20 → 45 mm/s. GIa/GII gerçek ve
  ayarlanabilir kazançlardır (PARSPEC'te 0–3).

**B2 — G9 ölçütü yapıyı değil büyüklüğü test ediyordu (kabul edildi).** Eski G9 `GIa=GIb=0`
yapıyordu; ancak `GIb*load` stance'te taban sürüşe %66 ekliyor (load ≈ 0,35, GIb × load ≈ 0,106 >
Ahe = 0,16'nın yarısından fazlası), yani sıfırlamak geri beslemeyle birlikte ekstansör sürüşünün
çoğunu da kaldırıyordu. Çöküş "yapı zorunlu"yu değil "ekstansör bu sürüş olmadan zayıf"ı
gösteriyordu.

- **Düzeltme [`cl_selfcheck.py`]:** G9 artık yapısal bir testtir — geri besleme, faz ortalaması
  sabit bir ileri beslemeyle değiştirilir (`fb='meanff'`); yürüyüş sabitle de ayakta kalıyorsa
  geri besleme yapısal değildi.
- **İlk ölçüm (kilitli config, düzeltme sonrası): G9 kalıyor.** live 7 geçiş / meanff 16 geçiş,
  ikisinde de nearlim 1,0 — sabit ortalamalı geri besleme yürüyüşü bozmuyor, hatta iyileştiriyor.
  Yani mevcut config'te gerçek yapısal kapalı döngü yoktur; FSM (kalça proprioseptif geçişi),
  ileri besleme ve sürüş seviyesi taşımaktadır. Bunu optimizasyonun G9'u geçirerek çözmesi
  gerekir; geçemezse "bu indirgenmiş modelde r(t) yapısal döngüyü taşıyamıyor" sonucu yazılır.
- Not: FSM'nin stance→swing geçişi kalçanın eşiğe inmesini gerektirir ve kalçayı indiren yük geri
  beslemesidir; yani bir tür kapanış vardır, ama G9'un test ettiği "iğcik r(t) yapısal katkısı"
  ölçütünü mevcut config geçmemektedir.

**B3 — §J'deki PF/DF oranı gevşekti (düzeltildi).** §J "2,18" diyordu; tutarsız bir alt kümeydi.
Doğrusu kümeye bağlıdır: PCSA tam küme 1,80; kod alt kümesi 2,48; F_max 2,61; moment kapasitesi
2,78. Baskınlık ~2,5–2,8 → bilek nötrü için gereken cdf/cpf ≈ 3,0; PARSPEC'te cdf tavanı 0,15 →
**0,25** genişletildi. §J satırı düzeltildi.

**B4 — GMi ters işaretliydi (düzeltildi).** `HIP_FLX` içinde GMi'nin kalça moment kolu çalışma
aralığında ters (−0,5…−0,16 mm), yani gruba karşı çalışıyordu. GMi `HIP_FLX`'ten çıkarıldı.

**B5 — kullanılmayan ve yanıltıcı kod temizlendi.** `DISTAL`, `STANCE_SYN`, `KNE_FLX` (yalnız
`DISTAL`'ı besliyordu) ve `Foff` kaldırıldı; "monoartiküler" yorumu (BFp/STp aslında biartikülerdir
— §J ile çelişiyordu) silindi. Kod artık döngüde olmayan bir bileşen varmış izlenimi vermiyor.

**Denetimin doğrulayamadıkları:** afferent katsayıları (10,43; 26,59; 27,08; 14,43; 21,25 ve
üsteller) bu oturumda birincil kaynaktan görülmedi. 46_/02 (Oturum 6) kayıtlarında Blum 2020 (Ia)
ve Vincent 2017 (II) birincil kaynaklarına karşı doğrulanmıştı; kod yorumuna bu referans eklendi.

**Durum:** kod ve kabul ölçütleri artık gerçeği yansıtıyor. "u(t)/r(t) kapalı döngü" iddiası
mevcut config'te G9'dan kalıyor (yapısal değil); poster iddiası ancak G9 geçtikten sonra
edilebilir.

---

# K.2 · 02.09.2026 — İkinci denetim: bilek sınıra dayanması sayısal bir yapaylıktır

7b düzeltmelerini içeren sürüm yeniden denetlendi (denetim: Deniz). Düzeltmeler doğrulandı
(II besleniyor, Ia/II fazik, VCAP = 45, GMi çıkarılmış, kullanılmayan kod temizlenmiş, G9
`meanff` ile yapısal, §J düzeltmesi yapılmış). En kritik yeni bulgu: emergent döngüde bileğin
−35°'ye dayanması bir kontrol dengesi hatası **değil**, açık Euler integrasyonunun bilek
serbestlik derecesinde yakınsamamasıdır. Önceki değerlendirmeler (görev tanımı belgesi, §J,
§K ve ilk denetimin statik moment hesabı) bunu kontrol hatası sanıyordu; hiçbiri zaman adımı
duyarlılığına bakmamıştı.

**Kanıt (üreten: `cl_emergent.run`, dt taraması, aynı oturum):**

- Bilek eylemsizliği çok küçük: M[ankle, ankle] = 1,1e-7; M[hip, hip] = 1,4e-5 → ~120×. Bilek
  ivmesi 1e4–1e5 rad/s²; dt = 1e-4'te açık Euler bu stiff serbestlik derecesinde kararsız
  (salınıp ızgara sınırına dayanıyor, `wa=0` ile kilitleniyor).
- Zaman adımı duyarlılığı: dt = 1e-4 → bilek −35…−35; dt = 5e-5 → +55 (öteki sınıra dayalı);
  dt = 3e-5 → diz −155'e dayalı; dt = 2e-5 → bilek 15…24 (canlı); dt = 1e-5 → 15…24 (2e-5 ile
  birebir aynı, yani yakınsak). En büyük yakınsak adım dt = 2e-5'tir.
- Yapaylık kontrolü kilitliyordu: dt = 1e-4'te bilek cdf'den bağımsızdı (cdf = 0,06…0,25 → hep
  −35). dt = 2e-5'te bilek cdf'ye monoton yanıt veriyor: cdf = 0,06 → −35…−15; 0,10 → −9…7;
  0,135 → 23…42; 0,18 → 38…55. Yani sayısal düzeltme, "cdf ile ayağı dengele" planını uygulanabilir
  kılıyor. Fizyolojik nötr için cdf ≈ 0,10 (cdf/cpf ≈ 2,2 — ilk turdaki ~3,0 statik tahminden
  düşük; statik hesap dinamiği ve yerçekimi katkısını atlıyordu).

**Düzeltme [`cl_emergent.py`, `cl_selfcheck.py`]:** varsayılan dt 1e-4 → 2e-5 (`run` ve `_run`).
Bu bir integratör düzeltmesidir, kontrol değişikliği değil. Maliyet: benzetim ~5× yavaş;
CMA-ES çok çekirdekli makinede hâlâ uygulanabilir.

**Yeni referans durum (üreten: `cl_selfcheck.verify`, dt = 2e-5):**

- Kilitli config (cdf = 0,06): G3 hâlâ kalıyor (bilek −35), ama artık gerçek kontrol nedeniyle
  (zayıf dorsifleksör sürüşü), yapaylık nedeniyle değil.
- Elle dengelenmiş config (cdf = 0,10, Adf = 0,10): G1, G2, G3, G4, G5, G7, G8 geçiyor
  (bilek −17…4, kalça 21…56, diz −139…−124, stance 0,55, adım sıklığı 2,0 Hz) — dokuz ölçütün
  yedisi. G6 (temas modülasyonu) ve G9 (yapısal döngü) kalıyor; PASS_kritik yalnız G9'dan kalıyor.
- Sonuç: ayak sınırı sorunu (§J ve §K'nin ana konusu) çözüldü; kalan iki ölçüt gerçek bilimsel
  sorulardır (temas modülasyonu ve r(t)'nin yapısal katkısı), sayısal değil. CMA-ES artık doğru
  dinamiğe karşı optimize eder.

**Küçük düzeltmeler:** (1) fazik gerekçe düzeltildi — 7b'deki kod yorumu ve §K "fazik → ~0 ortalama
→ sabitle taklit edilemez" diyordu; ancak faz bazlı ortalama ~0 değildir (üreten:
`refl_stance/swing_mean`; VL swing 0,10, Sol swing −0,058, TA swing 0,048). `meanff` testi yine
geçerlidir: faz ortalamalarını gerçek değerleriyle sabitler, geriye faz içi zamanlamayı test eder.
(2) Kullanılmayan `SPINDLE` değişkeni kaldırıldı. (3) G9, ölü yürüyüşte (live < 6 geçiş) True
dönebiliyor; G1'in ve fitness'ın n_transition < 6 erken dönüşü bunu PASS_kritik'e taşımıyor —
bilinen ve korumalı bir durum.

**Doğrulanamayanlar:** dt = 5e-6 ile 2e-5'in ötesinde yakınsama teyidi koşu süresi sınırını aştı;
iddia "2e-5 yakınsaktır (1e-5 ile birebir)" biçimindedir, "daha küçük dt farklı verir" değil. Tam
CMA-ES koşulmadı (oturum tek çekirdekliydi, `cma` yoktu); PASS_kritik'in erişilebilirliği elle bir
config ile 7/9'a kadar gösterildi, G9 açık kaldı.

---

# K.3 · 02.09.2026 — İkinci denetimin bağımsız doğrulanması

7c sürümü (`rat_emergent_cc_7c`) ve `55_CC_DEVIR.md` bağımsız bir oturumda yeniden koşularak
§K.2'nin zaman adımı bulgusu sınandı. **Her noktada doğrulandı.**

**Ölçülen (üreten: `cl_emergent.run`, `cl_selfcheck.verify`, 7c sürümü):**

- Bilek eylemsizliği: M[ankle, ankle] = 1,13e-7; M[hip, hip] = 1,17e-5 → **oran 104×** (§K.2'nin
  "~120×" değeriyle aynı mertebe; küçük fark config ve ortalama farkından). Bilek gerçekten
  kalçanın ~1/100'ü kadardır.
- Zaman adımı yakınsaması (cdf = 0,10): dt = 1e-4 → bilek −35…54, son yarı ortalaması **−35
  (sınırda)**; dt = 2e-5 → **4…10**; dt = 1e-5 → **5…10** (2e-5 ile birebir). Yani 2e-5 yakınsak,
  1e-4 yanıltıcı bir yapaylıktır; §K.2 doğrudur.
- Ölçüt okuması (cdf = 0,10, Adf = 0,10, dt = 2e-5, `verify`): **G3 geçiyor** (bilek −9…7, kalça
  21…56, diz −139…−125, stance 0,57, adım sıklığı 2,0 Hz); G6 (temas 0,18 ile 0,14 N, oran ~1,3)
  ve **G9 (yapısal: live 5 geçiş, meanff 10 — meanff bozmuyor)** kalıyor. §K.2'nin "7/9, G6 + G9
  kalır" tablosuyla birebir aynı. (G1 bu koşuda Tsim = 2,5 kısa olduğu için düştü; uzun koşuda
  geçiyor.)

**Değerlendirme:** ikinci denetim doğru ve titizdir; zaman adımı bulgusu §J ve §K'nin çerçevesini
düzeltmektedir — bilek "kontrol dengesi" sanılıp dt = 1e-4'te optimize edilmeye çalışılmıştı, o
arama sayısal bir yapaylıkla uğraşıyordu. `run`/`_run` varsayılanının dt = 2e-5 olması doğru
düzeltmedir ve korunmalıdır.

**Kalan iki ölçüt bilimsel, sayısal değil:** G6 (salınımda ayak yerden kalkmıyor → temas modüle
olmuyor; muhtemelen rijit ayak / MTP yapısal sınırı) ve G9 (r(t) yapısal döngüyü taşımıyor;
`meanff` sabitiyle yürüyüş bozulmuyor). "u(t)/r(t) kapalı döngü" iddiası ancak G9 geçerse
edilebilir. `55_CC_DEVIR.md`'nin üç sınır uyarısı (G9'u zorlama; G6 yapısal olabilir, birkaç
denemeden sonra bırak; çekirdeğe ve dt'ye dokunma) doğrudur. CMA-ES doğru dinamiğe (dt = 2e-5)
karşı koşulmalıdır.

---

# L · 03.09.2026 — CMA-ES optimizasyonu: dokuz kabul ölçütünün dokuzu geçildi

**Görev:** 54/55 numaralı görev tanımı belgeleri uyarınca `cl_emergent.py` denetleyicisinin 13 parametresini (PARSPEC) CMA-ES ile optimize etmek;
dt = 2e-5, çekirdek dosyalar ve denetleyici yapısı değiştirilmeden. Kabul ölçütleri ve fitness
`cl_selfcheck.py`'den alındı ve değiştirilmedi. Donanım: 32 çekirdek, yerel koşu.

**Koşu zinciri (kayıt dosyalarıyla):**

1. Referans selfcheck (kilitli config, dt = 2e-5) [`log1_baseline_selfcheck.txt`]: G3/G5/G6
   kalıyor (bilek −35…−35 sınırda). Selfcheck'in kendi varsayılanı cdf = 0,06'dır; §K.2'nin
   "7/9 geçer" dediği elle ayarlanmış config (cdf = 0,10) değildir.
2. CMA-ES koşusu 1 (arama Tsim = 3, popsize = 32, workers = 32) [log2]: maliyet 234 → 1,79
   (jenerasyon 33); worker başlatma hatasıyla (WinError 87) düştü, en iyi çözüm `cl_best.json`'a
   kayıtlıydı.
3. Koşu 2 (önceki en iyi çözümden başlatma — warm start, 150 jenerasyon, Tsim = 3) [log3]:
   maliyet 1,79 → 0,056. **Tsim = 6 ile doğrulamada G3 kaldı** (bilek −35…−4, nearlim 0,48):
   kısa ufuklu optimum 3 s'den sonra bileği yavaşça sınıra sürüklüyor, arama penceresi bunu
   görmüyordu.
4. Koşu 3 (arama ufku Tsim = 6'ya eşitlendi — ölçütler ve fitness aynı, yalnız değerlendirme
   penceresi doğrulamayla eşitlendi) [log4]: maliyet 2,73 → 0,097 (son iyileşme jenerasyon 46).
   **`verify(P, Tsim=6)`: 9/9 ölçüt geçti, PASS_kritik = True, PASS = True.**

**Optimizasyon tarafında yapılan değişiklikler (yalnız `cl_optimize.py`, koşu yapılandırması):**
workers 8 → 32, popsize 16 → 32; `cl_best.json` varsa önceki en iyi çözümden başlatma
(sigma = 0,10); arama Tsim 3 → 6. Çekirdek dosyalar (`.osim`, `.mot`, `kas_par`, ızgara),
dt = 2e-5, `cl_emergent.py` ve `cl_selfcheck.py` değiştirilmedi.

**Ölçüt okuması (üreten: `cl_optimize.py` nihai `verify` [log4]; aynı P ile deterministik yeniden
koşu `cl_teslim_9of9.py` birebir aynı sayıları verdi):** adım sıklığı 2,9 Hz; stance 0,58; kalça
26…52° (ROM 26°); diz −141…−129°; bilek 18…19°; live nearlim 0,00; F_c stance 0,167 N / swing
0,112 N; refl_HE std 0,101. En iyi parametre kümesi [`cl_best_9of9.json`]: Ahe = 0,276,
Ake = 0,297, cpf = 0,002, cdf = 0,040, Apf_st ≈ 0,0003, Ahf = 0,598, Adf = 0,023, **GIb = 0,015,
GIa = 0,091, GII = 0,059**, kc = 137, hip_ext = 26,3°, hip_flx = 50,7°.

**G9 yapısal kanıtı (asıl hedef; üreten: log4 + `cl_teslim_9of9.png` son panel):** canlı geri
beslemeyle bilek 6 s boyunca 18…19°'de, sınırdan uzak (nearlim 0,00). Geri beslemenin faz
ortalaması sabitle değiştirildiğinde (`meanff`) bilek yaklaşık 3. saniyede +55° dorsifleksiyon
sınırına tırmanıp orada kalıyor (nearlim 1,00, son yarı 51…55°). G9, nearlim ölçütünden geçiyor
(1,00 > 0,00 + 0,05). Yani iğcik r(t)'nin faz içi zamanlaması bileği sınırdan uzak tutan şeydir ve
sabit sürüş seviyesiyle taklit edilemez; **yapısal kapalı döngü bu modelde ilk kez nesnel olarak
gösterilmiştir** (§K ve §K.2'de açık kalan ölçüt).

Dipnot: `verify` çıktısındaki "live geçiş 17, meanff 39" iki farklı metriği karıştırır — `live_tr`
yalnız swing→stance basışlarını, `meanff_tr` tüm geçişleri sayar; eşdeğer karşılaştırma 34 ile
39'dur (üreten: `cl_teslim_9of9.py`). Bu karışıklık G9'un geçiş sayısı ölçütünü yalnız tutucu
yönde saptırır (`meanff_tr` şişkin → ölçüt zor ateşlenir); G9 zaten nearlim ölçütünden geçtiği için
sonuç etkilenmez. Fitness'taki yapısal ödül terimi de aynı karışık metriği kullanır (`struct_gap`
geçiş terimi); nearlim bileşeni baskın olduğundan sonuç değişmez, ama düzeltilebilir.

**Çekinceler (9/9'a rağmen):**

1. **Bilek 18…19°'de dorsifleksiyonda sabitlenmiş (ROM ~1°).** Hedef ayağı toe-down −25…0°
   aralığına oturtmaktı ve "ayağı dorsifleksiyonda çevrimletme" uyarısı vardı; G4'ün formal aralığı
   (−40…35) geçiliyor, ancak optimizasyon G3'ü ayağı toe-down aralığında sürerek değil,
   dorsifleksiyonda sabit tutup yükü küçülterek çözdü.
2. **Yük taşıma minimal:** F_c stance ortalaması 0,167 N (referans durumda 1,30 N'du); G6 eşiği
   (0,167 > 0,112 × 1,3 = 0,146) kıl payı geçiliyor. Çevrim içi modülasyon gerçek ve nettir
   (her adımda 0 → 0,33 N; şekil panel 2), ancak FSM stance'iyle kısmen faz kaymalıdır;
   stance/swing ortalama farkını küçülten budur. GIb'nin 0,015'e düşmesi tutarlıdır: yük refleksi
   fiilen kapalıdır, döngüyü iğcik (GIa/GII) taşımaktadır.
3. **Diz ROM'u 12°** (−141…−129); G4 alt sınırına (−150) 9° mesafede.
4. Ia SM ~300–560 pps — Blum fit aralığının (≲250) üstü; §I madde 3'teki ekstrapolasyon çekincesi
   bu config'te de geçerlidir.

**Yorum:** ölçütler ölçüt tanımı değiştirilmeden geçildi ve G9 kanıtı güçlüdür; iğcik geri
beslemesinin yapısal gerekliliği artık nesneldir. Ancak elde edilen rejim "yük taşıyan toe-down
yürüyüş"ten çok "minimal yüklü ritim"dir: optimizasyon, rijit ayak ve MTP'si olmayan modelde yük
ile sınır uzaklığını aynı anda sağlayamayıp yükü küçülten çözüme gitmiştir. Bu, 54 numaralı belgedeki "gerçek stance
yuvarlanması ancak MTP ile gelir" yapısal sınırıyla tutarlıdır. Poster iddiası "u(t)/r(t) yapısal
kapalı döngü (G9 nesnel)" olarak edilebilir; "yük taşıyan digitigrad yürüyüş" iddiası bu config
ile edilmemelidir. Toe-down ve daha yüksek yük istenirse iki yol vardır: (a) mevcut ölçütler
içinde farklı başlangıçlarla yeni arama (G9'u bozma riski var), (b) MTP eklemi eklemek (ayrı iş).

**Üreten:** `cl_best_9of9.json` (en iyi P), `cl_optimize.py` (warm start + Tsim = 6 arama),
`cl_teslim_9of9.py` → `cl_teslim_9of9.png`/`.npz` (zaman serileri, faz portresi, G9 live–meanff
karşılaştırması), `log1`…`log4` (koşu kayıtları). O günkü kopyalar: `tum/04_kapali_dongu_ESKI/`.

---
# M · 05.09.2026 — Köprü ortamı: NEURON ile OpenSim tek süreçte koşuyor

**Soru:** PREPRINT bölüm 14 soru 3 ve `SDLC/05_MIMARI_RISK.md` risk-1, köprünün iki Python
ortamını (3.14 NEURON / 3.13 OpenSim) nasıl buluşturacağını açık bırakıyordu. Risk-1'in gerekçesi
"tek ortamda ikisi birden **kurulamaz**" idi.

**Ölçüm 1 — tekerlek denetimi (PyPI JSON API).** `neuron==9.0.2` şu ABI etiketlerini yayımlıyor:
cp310, cp311, cp312, **cp313**, cp314 (macosx_11_0_arm64 dahil). `opensim==4.6` ise cp311, cp312,
**cp313** yayımlıyor (3.14 yok). Yani **ortak payda Python 3.13'tür**; risk-1'in "kurulamaz"
gerekçesi NEURON tarafı için yanlıştır — doğru olan yalnızca `opensim`'in 3.14 tekerleği
olmadığıdır.

**Ölçüm 2 — kurulum.** `~/.venvs/usk26-kopru` (Python 3.13.14) kuruldu:
neuron 9.0.2 · opensim 4.6 · numpy 2.5.2 · scipy 1.18.1 · matplotlib 3.11.1.
Beyan: `requirements-kopru.txt`. Ortam proje **dışındadır** (boşluksuz yol zorunluluğu, risk-4).

**Ölçüm 3 — tek süreçte çalışma.** İki import sırası da denendi ve her ikisinde de yalnız import
değil, iki simülatörün de **iş yaptığı** doğrulandı:

| Sıra | NEURON (tek bölme, pasif, IClamp, 1 ms) | OpenSim (model yükle, realizePosition) |
|---|---|---|
| `from neuron import h` sonra `import opensim` | t = 1,000 ms · v = −68,1211 mV | 38 kas · TA boyu 0,036766 m |
| `import opensim` sonra `from neuron import h` | t = 1,000 ms · v = −68,1211 mV | 38 kas · TA boyu 0,036766 m |

İki sırada da sayılar birebir aynı; sembol çakışması, çökme veya sessiz bozulma gözlenmedi.

**Ölçüm 4 — ileri dinamik maliyeti.** `rat_hindlimb_faz1a.osim`, `Manager` +
RungeKuttaMerson (doğruluk 1e-4), 0,5 ms dış adım: **65,6 ms CPU/adım** → 0,387 s'lik yürüyüş
çevrimi ≈ **51 s**. 38 kasın boyunu okumak: **0,013 ms/çağrı** (ihmal edilebilir).
Donanım: bu makine (Darwin/arm64).

**Sonuç:** köprü **tek süreçte, tek Python döngüsünde** kurulabilir; süreçler arası iletişim veya
OpenSim'siz bir kas modeli gerekmiyor. `05_MIMARI_RISK.md` risk-1 ve PREPRINT 14.3 buna göre
güncellendi. Bu ortam bundan sonra projenin NEURON ortamıdır (`nrnivmodl` dahil).

**Üreten:** bu oturumun kontrol betiği (geçici); ortam beyanı `requirements-kopru.txt`.

---

# N · 05.09.2026 — İP-4a kapandı: dört `.mod` klasörü derlendi, model GUI'siz koşuyor

**Engel neydi:** `module1_2.mod` NEURON 9 ile derlenmiyordu (`U used as both variable and
function`). `SDLC/00_DURUM.md` ve `02_IS_PAKETLERI.md` tek çakışma olduğunu kaydediyordu.

**Ölçüm 1 — engel sanılandan bir fazlaydı.** `nocmodl` ilk hatada durduğu için ikincisi
görülmemişti. Dosyada **iki** ad çakışması vardır:

| Satır | Ad | Çakışma |
|---|---|---|
| 10 | `U` | `RANGE U` + `FUNCTION U (x)` (s.133) |
| 11 | `phi` | `RANGE phi` + `FUNCTION phi (x)` (s.138) |

Ayrıca aynı satırdaki `phi0`, hiçbir `PARAMETER`/`ASSIGNED`/`STATE` bloğunda tanımlı değildi.

**Ölçüm 2 — düzeltmenin güvenliği.** `U` ve `phi` hiçbir yerde **değişken olarak**
okunmuyor/yazılmıyor; tek kullanımları `U(Ca)` (s.111, 114) ve `phi(cli)` (s.155) — üçü de
fonksiyon çağrısı. `.hoc` ve `.ses` dosyalarının tamamı tarandı: `U`, `U_CaSP`, `phi`,
`phi_CaSP` erişimi **sıfır**. NMODL'de `SUFFIX`'li mekanizmanın `FUNCTION`'ları `RANGE`'de
olmasalar da `U_CaSP(x)` adıyla dışarı açılır — yetenek kaybı yoktur. Düzeltme iki `RANGE`
satırıyla sınırlıdır; denklemlere dokunulmamıştır.

**Ölçüm 3 — derleme.** Köprü ortamının `nrnivmodl`'ü ile **dört klasörün dördü de** derlendi
(`Successfully created arm64/special`):

| Klasör | `.mod` sayısı | Sonuç |
|---|---|---|
| `fig2_4_6` | 12 | 12/12 (önceki oturumda 11/12 idi) |
| `fig3_5_7` | 12 | 12/12 |
| `fig8` | 12 | 12/12 |
| `fig9` | 12 | 12/12 |

Figüre özel mekanizmalarda (`syn_ramp`, `SawtoothIClamp`, `mStepIClamp`, `syn_Ia_sinewave`)
başka NEURON 9 uyumsuzluğu **çıkmadı**. Kalan uyarılar zararsızdır: `Could not translate using
cnexp method; using derivimplicit`, `Warning: dt undefined`, `libomp` arama yolu uyarısı.

**Ölçüm 4 — YENİ KISIT: NEURON'un HOC dizgi arayüzü ASCII dışı karakter kabul etmiyor.**
`h.xopen()`'a bu reponun mutlak yolu verildiğinde:
`python string arg cannot decode into c_str ... 'ascii' codec can't encode characters in
position 46-47`. Konum 46-47 = `Sıçan` kelimesinin `ı` ve `ç` harfleri. Bu, risk-4'ün
(boşluklu yol `nrnivmodl`'ü kırıyor) **ikinci ve ayrı bir yüzüdür**; boşluk değil, Türkçe
karakter kırıyor ve derleyiciyi değil HOC yorumlayıcısını etkiliyor.
**Kural:** NEURON'a verilen her yol (`xopen`, `nrn_load_dll`, `load_file`) **göreli** olmalıdır;
mutlak yol yasaktır. Python tarafı `os.chdir()` ile konumlanır.

**Ölçüm 5 — GUI'siz koşu.** `neuron/kopru/motor_unit_batch.hoc` (orijinalden yalnız iki satır
farklı: `nrngui.hoc` → `stdrun.hoc`, `fig.ses` çıkarılıp sayısal ayarları taşınmış) ile
`fig2_4_6` modeli koştu:

| Büyüklük | Ölçülen |
|---|---|
| Bölme sayısı | 315 section, **2655 segment** (`fixnseg.hoc` `d_lambda` kuralından) |
| Koşu maliyeti | 12,51 s CPU / 3000 ms simülasyon → **4,17 s CPU per simüle saniye** |
| Soma voltajı | min −70,75 · maks **+23,09 mV** (aksiyon potansiyeli üretiliyor) |
| Aksiyon potansiyeli sayısı (NetCon, eşik −40 mV, `is` üzerinde) | 28 |
| İlk / son aksiyon potansiyeli | 1270,7 ms / 2975,4 ms |
| Ortalama ateşleme frekansı | 15,8 Hz |

Koşu koşulu: `dpath=600 µm`, `xm.amp=−8 mm`, `gmax_IaSyn=9,3e-6 S/cm²`, `RampIClamp` tepe
20 nA @ 5 s (Kim'in Fig 2-7 varsayılanı). Ateşlemenin 1,27 s'de başlaması üçgen akım rampasının
eşiği o civarda geçmesiyle tutarlıdır.

**Sonuç:** İP-4a'nın derleme ve GUI'siz koşu adımları **bitti**. Kalan adım Kim Fig 2-7'nin
tolerans aralıklı yeniden üretimidir (`dpath` taraması).

**Ölçek notu (İP-4b girdisi):** 4,17 s CPU / simüle saniye tek hücre içindir. 38 havuz için
naif ölçek ≈ 158 s CPU / simüle saniye. Ayak bileği aşaması (2 havuz) rahat; 38 havuza
geçerken `nseg` indirimi gerekebilir — gerekirse PIC konum etkisinin korunduğu gösterilecektir.

---

# O · 05.09.2026 — Motonöron havuzu için Python kurulumu ve HOC ile çapraz kontrolü

**Sorun:** `v_e_moto6_export.hoc` global `create soma, dend[311]` kullanıyor, **template değil**.
38 motonöron havuzu (PREPRINT 6.4) aynı morfolojiden çok hücre gerektiriyor; bu dosya buna
elverişli değil.

**Seçilen yol:** Kim'in kaynak dosyalarına dokunulmadı. Morfoloji bir kez HOC'tan
okunup veriye döküldü (`kod/kopru/morfoloji_cikar.py` → `veri/kopru/moto_morfoloji.npz`:
315 section, 312'sinde 3B nokta, toplam 1580 nokta); biyofizik `kod/kopru/nrn_hucre.py`'de
Kim'in hoc dosyalarıyla **aynı sırayla** yeniden uygulandı. Sıra kritiktir: geometri → bağlantı →
pasif (Ra, cm) → aktif → kas bölmesi kablo özelliği → `nseg` (d_lambda). `fixnseg.hoc:40-43`
`nseg`'i en sona bırakır çünkü d_lambda kuralı Ra ve cm'e bağlıdır.

**Risk:** yeniden uygulama sessiz sapma üretebilir.

**Çapraz kontrol (04_KURALLAR: bağımsız ikinci yöntem).** İki kurulum **aynı süreçte, aynı
uyaranla** (`RampIClamp` tepe 20 nA), aynı zaman adımıyla (0,025 ms) 3000 ms koşturuldu.
İki hücre elektriksel olarak bağımsızdır. Aralık testten önce ilan edildi: aksiyon potansiyeli zamanı farkı
< 0,025 ms (bir entegrasyon adımı); bu bir **regresyon** aralığıdır, literatür doğrulaması değildir.

| Büyüklük | HOC (Kim zinciri) | Python (`nrn_hucre.py`) |
|---|---|---|
| section sayısı | 315 | 315 |
| segment sayısı | 2655 | 2655 |
| Cav1.3 PIC nokta süreci (`dpath`=600 µm) | — | 86 |
| `IaSyn` takılı segment (`D_path`<1400 µm) | — | 1692 |
| aksiyon potansiyeli sayısı | 28 | 28 |
| soma v min | −70,7496 mV | −70,7496 mV |
| soma v maks | +23,0852 mV | +23,0852 mV |
| ilk aksiyon potansiyeli | 1270,675 ms | 1270,675 ms |
| son aksiyon potansiyeli | 2975,425 ms | 2975,425 ms |

**Aksiyon potansiyeli zamanı farkı: maks 0,000000 ms · ortalama 0,000000 ms.
Soma voltaj izinin maksimum farkı: 0,000000 mV.**

Yani iki kurulum bit düzeyinde aynıdır; aralık kıl payı değil, tam eşleşmeyle geçilmiştir.
Koşu maliyeti (iki hücre birlikte, 3000 ms): 24,4 s CPU.

**Sonuç:** `nrn_hucre.MotoNoron`, Kim modelinin doğrulanmış bir yeniden kurulumudur ve havuz
için çoğaltılabilir. Karşılaştırma kas modülü (`CaSP`/`fHill`) **açıkken** yapıldı ki model HOC
ile birebir aynı olsun; köprüde kas modülünün kapatılması ayrı ve bilinçli bir karardır
(kas dinamiği OpenSim'dedir — PREPRINT 4.3 kural 1). Kapatılırken `muscle_unit` bölmesi ve kablo
özellikleri (`g_pas`=2e-3, `cm`=20) **korunur**; bölme `is(0)`'a bağlı olduğu için silinmesi
başlangıç segmentindeki elektriksel yükü değiştirip ateşleme eşiğini kaydırırdı.

**Üreten:** `kod/kopru/capraz_kontrol.py`.

---

# P · 05.09.2026 — Ayak bileğinde tam kapalı döngü: ilk koşu ve zaman adımı yarılama testi

**Ne kuruldu.** `PREPRINT.md` bölüm 8'in köprüsü, tek eklemde (ayak bileği) uçtan uca koştu.
Zincir: CPG (Morris-Lecar yarım-merkez) → örüntü oluşturma katmanı → 10 motonöron havuzu →
`u(t)` → OpenSim **ileri dinamiği** → hareket → kas-tendon boyu/hızı → iğcik → Ia/II →
iletim gecikmesi → Ia sinapsı. **Bilek açısı reçete değildir**; kas kuvvetlerinden doğar.
Üreten: `kod/kopru/kos_ayakbilegi.py`. Ortam: `~/.venvs/usk26-kopru` (tek süreç).

Kaslar (PREPRINT 6.4 moment kolu gruplandırması): dorsifleksör TA, EDL, Per · plantar fleksör
Sol, MG, LG, Pla, TP, FDL, FHL. Havuz başına bir temsilî Kim hücresi (2655 segment).

## P.1 · Yol boyunca bulunan üç hata (hepsi sessizdi)

| # | Belirti | Sebep | Nasıl bulundu |
|---|---|---|---|
| 1 | Bütün motonöronlar sustu, `u(t)` = 0 | **NEURON nesneleri Python'da referans tutulmadığında çöp toplayıcı siliyor.** `gradli_baglanti()` dönüşü bir değişkende saklanmıyordu; CPG → PF sinapsı sessizce yok oldu | Sinaps yalıtılmış olarak sınandığında çalıştı, devrede çalışmadı; fark referans tutmaktı |
| 2 | Kas uyarımı hiçbir etki yapmıyor (TA %100 ile bilek yörüngesi pasif koşuyla **birebir aynı**) | `PrescribedController.prescribeControlForActuator` fonksiyonu **kopyalar**; dışarıdan tutulan `Constant` nesnesi modeldeki değil | Beş farklı uyarımın birebir aynı yörüngeyi vermesi. Çözüm: fonksiyonlar `initSystem()` sonrası kontrolcünün kendi kümesinden alınır |
| 3 | İki yarım-merkez de −80 mV'a çakıldı, salınım yok | `oz_yu2021` Tablo 2'nin `gCPG` değeri **yoğunluktur (mS/cm²)**, nokta süreci µS'i değil; dönüşüm atlanınca sinaps membran iletkenliğinin ~40 katı oldu | Birim denetimi: Tablo 2 "µS/cm²" yazıyor ama Iext ile 1000 kat tutarsız; mS/cm² okununca tutarlı (özetin kendi uyarısı) |

## P.2 · CPG kalibrasyonu

`oz_yu2021`'in `phiN` = 0,0005 /ms değeri Aplysia ölçeğinde T ≈ 2254 ms verir; bizim ölçülmüş
yürüyüş çevrimimiz **T = 0,387 s**'dir. `phiN`, serbest çevrim periyodu 387 ms olacak şekilde
ikiye bölmeyle arandı `[tasarım]`:

| Büyüklük | Değer |
|---|---|
| `gCPG` | 0,006 mS/cm² |
| `phiN` | 0,0152 /ms |
| Ölçülen serbest çevrim periyodu | **386,9 ms** (hedef 387,0) |
| Yarım-merkez genliği | −19,56 … +26,84 mV |
| RG-F ile RG-E korelasyonu | **−0,957** (zıtfaz — yarım-merkezin tanımı) |

## P.3 · Antagonist moment dengesi (yeni ölçüm)

Eşit CPG sürüşüyle eklem plantar fleksiyon ucuna çöküyor ve orada kalıyordu. Sebep ölçüldü:

| Eklem açısı | Dorsifleksör kapasite | Plantar fleksör kapasite | Oran |
|---|---|---|---|
| +18,9° | 54,78 N·mm | −141,39 N·mm | 2,58 |
| 0° | 48,74 | −147,69 | 3,03 |
| −40° | 25,59 | −113,60 | 4,44 |
| −80° | 9,42 | −49,53 | 5,26 |

(Kapasite = |Σ F_max · moment kolu|.) Merkezi sinir sistemi bu dengesizliği sürüş dağılımıyla
çözer; buradaki karşılığı, grup sürüşünün moment kapasitesiyle **ters ölçeklenmesidir**
`[tasarım]`. +14°'de (ölçülmüş yürüyüş bilek aralığının ortası, PREPRINT 5.2) ölçülen kapasiteler
53,68 / 144,36 N·mm → plantar fleksör sürüş ölçeği **0,372**. Bu uygulanmadan bilek −81,6°'de
takılıyordu; uygulandıktan sonra salınım başladı.

## P.4 · Kapalı döngü koşusu (3 s, ikinci yarı; geçici rejim atıldı)

| Büyüklük | Ölçülen | Referans / aralık |
|---|---|---|
| **Çevrim süresi** | **0,402 s** | `ic.kopru_cevrim_suresi` 0,387 s, aralık [0,348 – 0,426] → **ARALIKTA** |
| Bilek açısı | −11,08 … +62,86° (ROM 73,94°) | ölçülmüş yürüyüş aralığı −2,89 … +30,65° → **DIŞARIDA (çok geniş)** |
| `u_DF` – `u_PF` korelasyonu | −0,699 | zıtfaz bekleniyor → **sağlandı** |
| TA havuzu, etkin faz | 25,8 Hz | `gorassini2000.mn_frekans_TA_swing` 97 Hz, aralık [80 – 110] → **DIŞARIDA (düşük)** |
| Sol havuzu, etkin faz | 12,3 Hz | `gorassini2000.mn_frekans_SOL_yuruyus` 28 Hz, aralık [20 – 35] → **DIŞARIDA (düşük)** |
| MG/LG havuzu, etkin faz | 11,9 / 12,2 Hz | `gorassini2000.mn_frekans_MGLG_ortagec` 67 Hz, aralık [50 – 90] → **DIŞARIDA (düşük)** |

**Okunuşu.** Döngünün **yapısı** çalışıyor: ritim CPG'den doğuyor, iki grup zıtfaz almaşıyor,
hareket kas kuvvetinden doğuyor, iğcik geri beslemesi devrede ve çevrim süresi ölçülmüş yürüyüş
çevrimine düşüyor. Ama **nicel olarak kalibre değil**: ateşleme frekansları Gorassini aralıklarının
2–5 kat altında, eklem açıklığı fizyolojik aralığın 2 katından fazla. Bu iki sapma aynı yöne
işaret ediyor: havuz az ateşliyor ama kas fazla iş yapıyor — yani `u = f_MN / f_ref` eşlemesindeki
`f_ref` ve `pf_mn` sinaptik ağırlığı birlikte kalibre edilmemiş durumda.

**Bu sayıların hiçbiri bir iddia olarak sunulmamaktadır.** İlk uçtan uca koşunun ölçümleridir.

## P.5 · Zaman adımı yarılama testi — KISMEN DÜŞTÜ

PREPRINT bölüm 8 bu testi **zorunlu** sayar: kuplaj dışsaldır, ortak Jacobian kurulamaz
(`oz_fietkiewicz2023` §3b). Aralıklar testten önce ilan edildi (iç ölçüm yakınsama aralığı):
çevrim süresi %5, ROM %10, ateşleme oranı %10. NEURON adımı (0,025 ms) sabit tutuldu; yalnız
**alışveriş adımı** yarılandı. Koşu 4 s.

| Ölçüt | `dt_k` = 0,30 ms | `dt_k` = 0,15 ms | Bağıl fark | Aralık | Sonuç |
|---|---|---|---|---|---|
| Çevrim süresi | 0,3812 s | 0,3927 s | %2,91 | %5 | **geçti** |
| Havuz DF ateşleme | 25,60 Hz | 25,28 Hz | %1,26 | %10 | **geçti** |
| Havuz PF ateşleme | 12,05 Hz | 12,09 Hz | %0,38 | %10 | **geçti** |
| `u` zıtfaz korelasyonu | −0,722 | −0,729 | — | — | değişmiyor |
| **Eklem ROM** | **78,39°** | **61,33°** | **%21,77** | %10 | **DÜŞTÜ** |

**Yorum.** Sinirsel taraf (ritim, frekans, faz ilişkisi) alışveriş adımından bağımsızdır;
mekanik açıklık o adımda değildir. Aralık **genişletilmemiştir** (04_KURALLAR: post-hoc aralık
genişletme yasak); bunun yerine sebep arandı.

## P.6 · Üç noktalı yakınsama taraması — sebep bulundu: adım çok kabaydı

İki nokta bir eğilim göstermez; üçüncü nokta eklendi. Aynı koşu (3 s), yalnız köprü adımı
değişken:

| `dt_k` | Çevrim süresi | Eklem ROM | Açı aralığı | CPU |
|---|---|---|---|---|
| 0,300 ms | 0,4020 s | 73,94° | −11,08 … +62,86° | 187,0 s |
| 0,150 ms | 0,3749 s | 54,41° | +14,00 … +68,41° | 269,0 s |
| 0,075 ms | 0,3787 s | 54,10° | +8,08 … +62,18° | 457,6 s |

Ardışık bağıl farklar: ROM **%26,4** (0,30 → 0,15), sonra **%0,57** (0,15 → 0,075).
Çevrim süresinde **%1,00** (0,15 → 0,075).

**Sonuç: çözüm yakınsıyor; sorun kuplajın kendisi değil, 0,3 ms'in çok kaba olmasıydı.**
Bu, ilk hipotezle (sıfırıncı derece tutma + bilek DOF'unun çok küçük eylemsizliği) tutarlıdır:
uyarım köprü adımı boyunca sabit tutuluyor ve `M[ankle,ankle]` ≈ 1,1·10⁻⁷ olduğu için
0,3 ms'lik tutma hızlı geçişlerde belirgin biçimde farklı itki veriyor.

**Karar:** üretim köprü adımı **0,15 ms** yapıldı. Gecikmelerin tam sayı adım olma özelliği
korunuyor: Ia 1,5/0,15 = **10 adım**, II 1,8/0,15 = **12 adım**, efferent 6/0,15 = **40 adım**;
NEURON adımının katı olma özelliği de korunuyor (0,15/0,025 = **6 adım**). Bedeli yaklaşık
1,4 kat CPU'dur.

**Aralık değil, adım değiştirildi.** Ölçüt banda uymadığında önce modelin sorgulanması kuralının
(04_KURALLAR, madde 2) uygulanmasıdır bu.

## P.7 · Üretim adımıyla (0,15 ms) kapalı döngü koşusu — kanonik sonuç

| Büyüklük | Ölçülen | Referans / aralık | Sonuç |
|---|---|---|---|
| **Çevrim süresi** | **0,375 s** | `ic.kopru_cevrim_suresi` 0,387 s · aralık [0,348 – 0,426] | **ARALIKTA** |
| Bilek açısı | +14,00 … +68,41° (ROM 54,41°) | ölçülmüş yürüyüş −2,89 … +30,65° | **dışarıda** |
| `u_DF` – `u_PF` korelasyonu | **−0,734** | zıtfaz bekleniyor | **sağlandı** |
| TA havuzu, etkin faz | 24,52 Hz | `gorassini2000.mn_frekans_TA_swing` 97 · [80 – 110] | **dışarıda (düşük)** |
| Sol havuzu, etkin faz | 12,27 Hz | `gorassini2000.mn_frekans_SOL_yuruyus` 28 · [20 – 35] | **dışarıda (düşük)** |
| MG / LG havuzu, etkin faz | 12,25 / 12,21 Hz | `gorassini2000.mn_frekans_MGLG_ortagec` 67 · [50 – 90] | **dışarıda (düşük)** |

Koşu maliyeti: 3 s simülasyon → 242,5 s CPU (10 havuz × 2655 segment + OpenSim ileri dinamiği).

## P.8 · Adım yarılama testi — üretim adımıyla GEÇTİ

Aynı test, üretim adımı (0,15 ms) ile yarısı (0,075 ms) karşılaştırılarak tekrarlandı.
Aralıklar değiştirilmedi (çevrim süresi %5, ROM %10, ateşleme %10).

| Ölçüt | `dt_k` = 0,150 ms | `dt_k` = 0,075 ms | Bağıl fark | Aralık | Sonuç |
|---|---|---|---|---|---|
| Çevrim süresi | 0,3749 s | 0,3787 s | %0,99 | %5 | **geçti** |
| Eklem ROM | 54,41° | 54,10° | %0,57 | %10 | **geçti** |
| Havuz DF ateşleme | 25,25 Hz | 24,87 Hz | %1,51 | %10 | **geçti** |
| Havuz PF ateşleme | 12,25 Hz | 11,96 Hz | %2,36 | %10 | **geçti** |
| `u` zıtfaz korelasyonu | −0,734 | −0,716 | — | — | değişmiyor |

**PREPRINT bölüm 8'in zorunlu saydığı sayısal kararlılık kontrolü karşılanmıştır.**
Köprünün sonucu alışveriş adımından bağımsızdır.

## P.9 · Bugün ne iddia edilebilir, ne edilemez

**Edilebilir** (yakınsadı ve aralıkta): kapalı döngü **yapısal olarak çalışıyor** — ritim CPG'den
doğuyor, antagonist gruplar zıtfaz almaşıyor (−0,734), hareket kas kuvvetinden doğuyor
(kinematik reçete değil), iğcik geri beslemesi devrede ve **çevrim süresi ölçülmüş yürüyüş
çevrimine düşüyor** (0,375 s vs 0,387 s).

**Edilemez** (aralık dışında): motonöron ateşleme frekansları Gorassini aralıklarının 2–5 katı
altında; eklem açıklığı ölçülmüş yürüyüş aralığının dışında ve tamamen dorsifleksiyonda.
Bu iki sapma aynı yöne işaret ediyor: **havuz az ateşliyor ama kas fazla iş yapıyor**, yani
`u = f_MN / f_ref` eşlemesindeki `f_ref` ile PF → motonöron ağırlığı `pf_mn` birlikte kalibre
edilmemiş durumdadır. Bir sonraki adım budur.

**Ayrıca kaynaksız kalan bileşenler** (PREPRINT 6.1): `IaIN` ve `Renshaw` devrededir ama
literatür kaynakları yoktur; `II` katsayıları da izlenebilir bir kaynağa dayanmıyor. Bu
üçüne dayanan hiçbir sonuç bildirilmemektedir.

**Üreten:** `kod/kopru/adim_yarilama.py`, `kod/kopru/kos_ayakbilegi.py`.
**Artefakt:** `arsiv/veri/kosum_ayakbilegi.npz`, `sekiller/kopru_ayakbilegi.png` + `.csv`.
(07.09.2026 düzeltmesi: dosya adı bu kayıtta `kosum_` yazılıydı ama üreten betik `kosu_`
yazar — koşu dosyası o gün arşive alındı, güncel koşu `veri/kopru/kosu_ayakbilegi.npz`'dir.)

---

# Q · 07.09.2026 — 38 havuz + 3 DOF: tam bacak kapalı döngüsü ve kalibrasyonu

**Ne kuruldu.** Köprü, PREPRINT 6.4'ün tam uygulamasına ölçeklendi: tek CPG yarım-merkez çifti →
**6 örüntü oluşturma (PF) grubu** (kalça/diz/bilek × fleksör/ekstansör; RG-F fleksör yanını,
RG-E ekstansör yanını sürer) → **38 motonöron havuzu** (kas başına bir Kim hücresi, 2655 segment)
→ `u(t)` → OpenSim **ileri dinamiği, 3 serbestlik derecesi** (hip_flx, knee_flx, ankle_flx) →
iğcik → Ia/II → gecikme → Ia sinapsı. Grup başına birer IaIN, Renshaw ve II aktarım internöronu
(6'şar adet; IaIN/Renshaw `[tasarım]`, kaynaksız — hiçbir sonuç bunlara dayandırılmaz).
Biartiküler kaslar tek havuz, iki PF'ten girdi; işaret kararsız 6 kas (Pir, GMi, OE, OI, Pec,
BFa) havuzlu ama PF sürüşsüz. Eşleşme verisi `kod/kopru/devre_par.json` `havuz_eslesme`.
Üreten: `kod/kopru/{kopru,kos_tumbacak,kalibrasyon_tumbacak}.py`.

Eklem ROM karşılaştırma aralıkları koşulardan **önce** ilan edildi
(`referans_degerler.json`: `ic.kopru_{kalca,diz,bilek}_araligi`, ölçüt örtüşme oranı ≥ 0,5).

## Q.1 · Regresyon: genelleme eski davranışı korudu

Çok-eklem genellemesinden sonra `kos_ayakbilegi.py` (eski biçim: 2 grup + 1 DOF) yeniden
koşuldu: çevrim süresi **0,375 s**, zıtfaz korelasyonu **−0,734**, bilek +14,00…+68,41°,
TA 24,52 Hz, Sol 12,27 Hz — P.7'nin kanonik değerleriyle birebir aynı.

## Q.2 · Eşleşme kararlarında model verisi hakemliği

PREPRINT 6.4 karar tablosu ile D6 diyagramı iki yerde ayrışıyordu; ızgaradan ölçülerek karara
bağlandı (referans poz hip 37,5 / knee −122,5 / ankle 17,5°, `cl_grid3d.npz` R matrisi):

| Kas | r_hip [mm] | r_knee [mm] | r_ankle [mm] | Karar |
|---|---|---|---|---|
| EDL | −0,00 | **−0,63** | +2,57 | tek girdili (bilek-DF): diz kolu önemsiz — karar tablosundaki "EDL biartiküler" kaydı model ölçümüyle desteklenmiyor |
| BFp | −10,74 | **−13,82** | 0 | çift girdili (kalça-ext + diz-flx) |
| STa | −12,79 | **−15,57** | 0 | çift girdili |
| STp | −7,64 | **−15,21** | 0 | çift girdili |
| GP | −14,93 | **−12,39** | 0 | çift girdili |
| GA | −8,18 | **−9,48** | 0 | çift girdili |

BFp/STa/STp/GP/GA dizde **en güçlü fleksörlerdir** (Pop −1,60'ın ~10 katı); karar tablosunun
"iki PF'ten girdi" kararı doğrulandı, D6 diyagramının kutu görünümü eksikti.

## Q.3 · Eklem başına antagonist moment kapasitesi (ölçülmüş yürüyüş orta pozunda)

| Grup | Kapasite [N·mm] | Denge ölçeği |
|---|---|---|
| kalça-flx / kalça-ext | 229,3 / 415,4 | 1,0 / 0,552 |
| diz-flx / diz-ext | 358,1 / 127,9 | 0,357 / 1,0 |
| bilek-DF / bilek-PF | 53,7 / 144,4 | 1,0 / 0,372 |

## Q.4 · Yol boyunca bulunan ve çözülen üç sayısal engel

1. **Modelde koordinat aralığı yok → eklemler savruluyor.** H8'in bilinen bulgusunun (koordinat
   `range`'leri `.osim`'e kopyalanmamış) ileri dinamikteki sonucu: devre kalibre olana kadar
   eklemler kas geometrisinin tanım alanı dışına çıkıyor ve integratör sürünüyor (ölçüldü:
   ilk pf_mn taramasında 1,5 s'lik koşular 30+ dk CPU'da ~0,5 s'te kaldı; süreçler %100 CPU'da
   canlıydı, ilerlemiyordu). Çözüm: serbest koordinatlara **kırpmalı sınır** — `cl_emergent.py`
   satır 110-114'ün *uyarlanmış* OpenSim karşılığı (birebir değil; fark R.9'da);
   sınırlar `cl_grid3d` ızgara tanım alanı. `.osim`
   **değişmedi** (çekirdek modele dokunulmaz, bölüm J kararı).
2. **CoordinateLimitForce denendi ve reddedildi.** Bilek DOF eylemsizliği ~1,1·10⁻⁷ olduğundan
   her yay sertliği ~1 kHz'lik mod üretip değişken adımlı integratörü mikro-adımlara düşürüyor
   (ölçüldü: K=0,1 N·m/derece ile 0,5 s koşu 10+ dk CPU'da bitmedi; kırpmayla aynı koşu
   **114,3 s**). K.2'deki dersin (bilek stiff) yeni yüzü.
3. **Kırpma hedefi ızgara ucunda olamaz.** Koordinat tam uç düğümde tutulunca kas sarma
   geometrisi kötü koşullu ve integratör tek adımda dakikalarca sürünüyor (ölçüldü: pay=0,75
   koşusu 13 dk'da 0,01 s ilerledi). Çözüm: kırpma hedefi sınırdan 0,5° içeri; sınırların
   kendisi ızgara ucundan 1° içeri. Sınıra dayanma oranı ve kırpma olay sayısı her koşuda
   raporlanır.

## Q.5 · K1: pf_mn log-taraması (f_ref sabit — Gorassini değerleri fizyolojik çapa)

Koşullar: 1,5 s, ikinci yarı değerlendirilir, pay=0,5, kırpmalı sınır (ızgara ucunda), 4 koşu.
Etkin-faz frekansları Hz; ROM örtüşmesi = kesişim/birleşim (hedef: ölçülmüş yürüyüş aralıkları).

| pf_mn | TA [80–110] | Sol [20–35] | MG/LG [50–90] | kalça ört. | diz ört. | bilek ört. |
|---|---|---|---|---|---|---|
| 0,6 (eski) | 22,6 dış | 11,9 dış | 0,0 dış | 0,80 | 0,49 | 0,11 |
| **1,2** | **82,0 İÇİNDE** | **21,2 İÇİNDE** | 11,5 dış | 0,70 | 0,63 | 0,20 |
| 2,4 | 81,0 içinde | 62,0 dış (üst) | 24,8 dış | 0,19 | 0,51 | 0,00 |
| 4,8 | 61,8 dış | 82,3 dış | 110,9 dış | 0,44 | 0,46 | 0,00 |

**Üretim değeri pf_mn = 1,2:** TA ve Sol ilk kez Gorassini aralıklarının içinde; P.9'un
"havuz az ateşliyor" teşhisi bu eksende kapandı. 2,4+ doyum rejimi (biartiküler u→1,0,
eklemler tanım alanı sınırlarına çöküyor).

## Q.6 · Biartiküler pay: 0,5 susturuyor, 1,0 doyuruyor; üretim 0,75 (kullanıcı kararı)

pay=0,5'te (K1 tablosu) MG/LG/Pla/GP/GA **hiç ateşlemiyor**: iki PF girdisi zıt fazlı olduğundan
üst üste binmiyor ve yarım ağırlık hiçbir fazda eşiği geçemiyor — Gorassini MG/LG hedefi
(67 Hz) ile çelişir. pay=1,0'da (2 s koşu, pf_mn=1,2): kalça örtüşmesi 0,82'ye çıktı ve bileğin
dorsifleksiyon saplanması çözüldü (−23,7…+7,3°), ama hamstringler doydu (BFp/STa/STp/GP/GA
u tepe ≈ 1,0) ve **diz fleksiyon sınırına çöktü** (−155…−138,6°; zamanın %60'ı sınırda);
Sol 18,2'ye düştü. Üretim değeri **0,75 ara noktadır ve tam karşılaştırma koşusu (K2b)
tamamlanmadan kullanıcı kararıyla seçilmiştir** — kanonik koşunun ölçümleri bu seçimin
sınavıdır; MG/LG aralık dışında kalırsa pay yeniden taranmalıdır (`devre_par.json`
`_pay_kalibrasyon` notu).

## Q.7 · Kanonik koşu — YAPILAMADI, YERİNE KÖK SEBEP BULUNDU (bölüm R)

Kanonik koşu iki kez denendi ve ikisinde de tamamlanamadı. Sebebi bir CPU/süre sorunu değil,
modelde yapısal bir hata çıktı. Ayrıntı ve düzeltme **bölüm R**'dedir. Q.7 ve Q.8 tabloları,
R'deki düzeltmenin ardından üretilecek kanonik koşuyla doldurulacaktır.

## Q.8 · Adım yarılama testi (3 DOF) — R düzeltmesinden sonraya bırakıldı

Test 3 s × 2 adım boyunda başlatıldı, aynı kök sebep yüzünden ilerlemedi ve durduruldu.

---

# R · Biartiküler kas eşleşmesi hatası: teşhis, literatür denetimi ve düzeltme (07.09.2026)

## R.1 · Arıza: kanonik koşu 1,28 s'te çöktü

Köprü adımı başına maliyet ölçüldü (OpenSim `Manager` günlüğünden, 100 bloklu ortalamalar):

| köprü adımı | sim t | CPU/adım | integratör iç adım (alınan/denenen) | projeksiyon |
|---|---|---|---|---|
| 20 000 | 0,00 s | 3,3 ms | 523 / 581 | 0 |
| 22 000 | 0,30 s | 3,3 ms | 2 637 / 2 915 | 0 |
| 23 000 | 0,45 s | 9,2 ms | 597 / 668 | 93 |
| 25 000 | 0,75 s | **1 039 ms** | 1 920 / 2 241 | 182 |
| 26 000 | 0,90 s | **4 252 ms** | 262 447 / 353 952 | 315 |
| son 200 | 1,25→1,28 s | **2 436 ms** | 1 373 / 1 587 | 360 |

730 kat yavaşlama. Bu hızla kalan 1,72 s ≈ 8 saat sürerdi. Sistem sağlıklıydı (yük 3,5/10
çekirdek, bellek %77 boş, takas 0), yani yavaşlık sayısaldı. Üç eklem de fizyolojik yürüyüş
aralığının dışına, kırpma sınırlarına dayanmıştı (zamanın %23–39'u sınırın 6° yakınında);
ölçülmüş yürüyüş ROM'u ızgara tanım alanının rahatça içinde olduğuna göre kırpma kutusu dar
değildi — **devre bacağı sınıra sürüyordu.**

## R.2 · Kök sebep: grup üyeliği moment kolundan türetilmişti

`devre_par.json` `havuz_eslesme.gruplar` nöral grup üyeliğini **moment kolu işaretinden**
türetiyordu. Moment kolu mekanik bir olgudur; nöral grup üyeliği ölçülmüş **EMG fazına/sinerjiye**
göre tanımlanır. İkisinin karıştırılması, dokuz biartiküler kasın **hepsini** zıt fazlı iki gruba
üye yapmıştı:

| kas | grup 1 | grup 2 | RG fazları |
|---|---|---|---|
| BFp, STa, STp, GP, GA | kalca_ext | diz_flx | E + F |
| MG, LG, Pla | diz_flx | bilek_pf | F + E |
| RF | kalca_flx | diz_ext | F + E |

`_syn` her çağrıda yeni bir `Exp2Syn` yarattığı için birleştirme **toplamadır**
(`kopru.py:304-307`, `338-341`), yani kas her iki fazda da sürülür. Üstelik `kopru.py:313` aynı
kasa her iki eklemin antagonist IaIN'inden inhibisyon veriyordu, aynı `pay` çarpanıyla: her
fazda eşzamanlı uyarı + inhibisyon → simetrik iptal.

Ölçüldü — faz modülasyonu (AC/DC, sinaptik ağırlıklardan) ve CPG'ye faz kilitlenmesi
(`|r(CPG)|`, 0,5 s'lik koşu verisinden), iki bağımsız yol:

| | monoartiküler (23) | biartiküler (9) |
|---|---|---|
| AC/DC | %100 | RF **%0** · MG/LG/Pla %3 · hamstring %21 |
| ort. \|r(CPG)\| | 0,658 | **0,168** |
| ort. modülasyon | 1,000 | 0,444 |
| sessiz kas (u ≡ 0) | 0 | **6** (GP, GA, MG, LG, Pla) |

Sonuç: `diz_flx`'in 9 kasından 8'i biartikülerdi, tek monoartikülerı zayıf Pop (moment kolu
−1,60 mm). Diz antagonistsiz kaldı (zıtfaz korelasyonu **r = −0,014**, yani dizde ritim yok) ve
sınıra çöktü.

**`biartikuler_pay` bu kusuru çözemez.** Zıt fazlı iki girdinin toplamı ölçekten bağımsız olarak
ritimsizdir: pay küçükse hiçbir faz eşiği geçemez (Q.6: pay=0,5'te beş kas 0 Hz), büyükse iki
yarım çevrim üst üste binip tonik doyum olur (Q.6: pay=1,0'da hamstringler u≈1,0, diz fleksiyon
sınırında). İkisi aynı kusurun iki eşiğidir. Planlanan K2b taraması bu yüzden **terk edildi**.

## R.3 · Basit hata ihtimalleri elendi

- **Moment kolu işaretleri ve grup atamalarının mekanik doğruluğu:** 2197 ızgara düğümünün
  tamamında grup başına Σ(Fmax·r) işareti %100 kararlı. Yanlış işaretli gruba konmuş kas yok.
- **İndeksleme:** `self.kaslar` sırası her yerde korunuyor; Ia/II doğru kasa dönüyor.
  (Küçük not: `kopru.py:413` kayda gecikmesiz `ia, ii` yazıyor, devreye gecikmeli gidiyor —
  yalnız raporlama tutarsızlığı.)
- **Kas parametreleri iki kaynakta birebir aynı:** `cl_grid3d.npz` ile `.osim` arasında `Fmax`,
  `lmo`, `tsl`, `alp` farkı **0**, kas sırası örtüşüyor. `osim_mekanik.py`'ye bunu koruyan
  assert eklendi.
- **H8 bugünkü modelden doğrulandı:** `grep -c "<range>" model/rat_hindlimb_faz1a.osim` → **0**.
  Kırpmalı sınır kararı artık devralınan metne değil kendi ölçümümüze dayanıyor.

## R.4 · Literatür denetimi

- **"İki eksitatör girdiyi topla ve ölçekle" biçiminin literatürde karşılığı yok.** Shevtsova ve
  ark. 2016 (Tablo 5.A2, Şekil 5.6) bifonksiyonel havuz için ayrı bir PF popülasyonu kurar; bu
  popülasyon iki yarım-merkezden eksitasyon alır **ve** faza özgü inhibitör popülasyonlar fazla
  eksitasyonu oyar. İnhibisyon her bir eksitasyonun 4 katıdır (0,005 / −0,02). Bizde toplama
  vardı, oyma yoktu.
- **Bifonksiyonel motonöron havuzları resiprokal Ia inhibisyonunun DIŞINDA tutulur** (aynı tablo:
  Mn-PBSt ve Mn-RF hiç Ia inhibisyonu almaz; Mn-E/Mn-F −0,04 alır). Bizde tam tersi yapılmıştı.
- **EMG kanıtı grup atamasını doğrudan çürütüyor** (Markin ve ark. 2012, s. 2062, Şekil 5A/5B):
  MG/LG/Pla + FHL hem fiktif hem gerçek lokomosyonda **ekstansör kümesinin** üyesi, tek patlama,
  basma fazı. Hamstring (PBSt) baskın deseni tip 1 (%73) fleksör fazın **başında** tek kısa
  patlama; RF tip 1 (%53) fleksör fazın **sonunda**. İkinci patlamalar faz **geçişlerinde** olur,
  karşı fazın ortasında değil.
- **Projenin kendi ölçümü literatürle uyumlu, devre ikisiyle de uyumsuzdu:**
  `D7_yuruyus_zamanlama.md` — BFp tepe %65, RF %66,5, STp %77; MG/LG/Pla salınımda sessiz.

Künye: Markin SN, Lemay MA, Prilutsky BI, Rybak IA (2012) J Neurophysiol 107:2057–2071.
Shevtsova NA, Hamade K, Chakrabarty S, Markin SN, Prilutsky BI, Rybak IA (2016)
*Modeling the Organization of Spinal Cord Neural Circuits Controlling Two-Joint Muscles*,
Springer, s. 121–159, DOI 10.1007/978-1-4939-3267-2_5.

## R.5 · Düzeltme (Aşama 1): üyelik EMG fazına göre yeniden türetildi

| kas | eski | yeni | dayanak |
|---|---|---|---|
| MG, LG, Pla | diz_flx + bilek_pf | **bilek_pf** | Markin 2012 s.2062, ekstansör kümesi |
| BFp, STa, STp, GP, GA | kalca_ext + diz_flx | **diz_flx** | PBSt tip 1 (%73); D7: BFp %65 |
| RF | kalca_flx + diz_ext | **kalca_flx** | RF tip 1 (%53); D7: %66,5 |

Artık hiçbir kas birden fazla gruba üye değil (32 sürülen + 6 sürüşsüz = 38, çakışma yok).
`biartikuler_pay` üretim yolunda işlevsizdir (`len(uyelik)==1` → 1,0); parametre Aşama 2 için
kodda bırakıldı. Kapasiteler yeniden ölçüldü: kalca_ext 415,4 → 204,1 · diz_flx 358,1 → 262,1 ·
diz_ext 127,9 → 74,3 (hamstringler, MG/LG/Pla ve RF ilgili gruplardan çıktığı için).

## R.6 · Denenip ölçülerek reddedilen: çapraz-eklem işaretli kapasite

Denge ölçeğinin biartiküler kasın öteki eklemdeki momentini görmediği tespit edilmişti. Kapasite
"aynı RG fazında sürülen bütün kasların bu eklemdeki **işaretli** moment toplamı" olarak yeniden
tanımlandı ve **koşuldu**. Sonuç patolojik:

- `kalca_flx` kapasitesi 229,3 → **18,0 N·mm** (F fazındaki hamstringlerin kalça ekstansiyon
  kolları aynı fazdaki hip fleksörlerini götürüyor),
- denge bunu "F fazı zayıf" diye okuyup `kalca_ext`'i 0,552 → **0,088**'e kısıyor,
- kalça 0,09 s'te 37,2° → 65,9° monoton doyuma gidiyor (u_max=1,0) ve integratör kilitleniyor.

**Ders:** işaretli net moment bir *kapasite* ölçüsü değildir; birbirini götüren iki kas
"kapasitesiz" değildir. Tanım geri alındı; gerekçe `kopru.py::_kapasite_olc` içinde kayıtlı.

## R.7 · Düzeltme sonrası ölçüm (1,2 s koşu, pf_mn=1,2)

**Kök sebep ölçütleri — GEÇTİ:**

| ölçüt | önce | sonra |
|---|---|---|
| biartiküler ort. \|r(CPG)\| | 0,168 | **0,567** |
| monoartiküler ort. \|r(CPG)\| | 0,658 | 0,553 |
| biartiküler ort. modülasyon | 0,444 | **1,000** |
| sessiz kas sayısı | 6 | **0** |
| diz zıtfaz korelasyonu | −0,014 | **−0,726** |
| en uzun tamamlanan koşu | 1,28 s (çökerek) | 1,2 s (temiz) |

Biartiküler kaslar artık monoartikülerlerle aynı faz kilitlenmesine sahip. Üç eklemde de
zıtfaz kuruldu (kalça −0,557 · diz −0,726 · bilek −0,795). Regresyon: `kos_ayakbilegi.py`
`pf_mn=0,6` ile altı ölçütte birebir geçti (aşağıda R.8).

**Lokomosyon ölçütleri — GEÇMEDİ (majör sapma, kullanıcıya raporlandı):**

| eklem | ölçülen [derece] | hedef [derece] | örtüşme (ölçüt ≥0,5) | sınırda |
|---|---|---|---|---|
| kalça | −9,00 … 17,55 | 9,01 … 65,42 | **0,11** | 0,60 |
| diz | −122,88 … −91,00 | −139,73 … −107,65 | **0,31** | 0,59 |
| bilek | −34,00 … 42,33 | −2,89 … 30,65 | **0,44** | 0,36 |

Çevrim süresi ölçülemedi (kalça geçişi yetersiz). Frekanslar: TA 80,98 Hz **aralıkta** [80–110];
Sol 19,69 Hz aralık dışı [20–35]; MG/LG 19,3 Hz aralık dışı [50–90]. Kırpma 1295 olay.
Düşük ateşleyen gruplar tam olarak denge ölçeği en küçük olanlardır (diz_flx 0,283 ·
bilek_pf 0,372) — kalibrasyon ekseni burasıdır. **Aralıklar genişletilmedi.**

**Pasif kontrol ayrımı:** pasif koşu (u=0, NEURON yok) da bileği −34,00'e dayıyor
(pasif bilek −34,00…13,98, kırpma 224 olay). Yani bileğin alt sınıra oturması **mekanik**
bir özelliktir (yer teması olmayan serbest salınan uzuv), devre kusuru değil. Kalça −9,00 ve
diz −91,00 yalnız canlı koşuda görülüyor — onlar devre kaynaklıdır.

## R.8 · P.7/Q.1 tabanı bayattı — düzeltme

Q.1'de "regresyon birebir geçti" diye kayıtlı ayak bileği değerleri (0,375 s · −0,734 ·
+14,00…+68,41° · TA 24,52 · Sol 12,27) **pf_mn=0,6 ile** üretilmiştir. Üretim değeri aynı oturumda
1,2'ye çıkarıldığı halde (commit `be9f06e`) taban güncellenmemişti. Ölçüldü:

- `pf_mn=0,6` ile bugünkü kod: 0,3749 s · 14,00…68,41° · −0,7337 · TA 24,52 · Sol 12,27 —
  **altı ölçüt de birebir**, yani R.5 düzeltmesi tek eklemli yolda etkisizdir.
- `pf_mn=1,2` (üretim) ile: çevrim 0,393 s · bilek 6,51…66,15° · −0,845 · TA 82,62 · Sol 22,42.
  **Yeni ayak bileği tabanı budur.**

## R.9 · Belge doğruluğu düzeltmesi

`devre_par.json` `kopru.eklem_siniri._gerekce` kırpma kuralını devralınan
`cl_emergent.py:110-114`'ün **"birebir karşılığı"** diye tanımlıyordu. **Birebir değil:**
devralınan kod sınırın kendisine kırpar ve hızı float eşitlik kontrolüyle sıfırlar; bizimki
sınırdan 0,5° içeri kırpar, hızı koşulsuz sıfırlar ve sınırlar ızgara ucundan 1° içeridedir.
Sapma bilinçli ve gerekçeli; yanlış olan yalnız "birebir" nitelemesiydi, düzeltildi.

Not: `osim_mekanik.py:47` ve bu belgenin Q.4 maddesi "OpenSim karşılığı" diyordu — teknik olarak
yanlış değildi ama aynı yanılgıya açıktı; ikisi de "uyarlanmış karşılık" olarak netleştirildi.

## R.10 · Sıradaki adım

Aşama 1 kök sebebi çözdü ama fizyolojik lokomosyon üretmiyor. İki aday eksen:
1. **Kalibrasyon:** `diz_flx` (0,283) ve `bilek_pf` (0,372) grupları hedef frekansların
   3-4 katı altında ateşliyor; denge ölçeği ile `pf_mn` etkileşimi taranmalı.
2. **Aşama 2 (literatürün gösterdiği):** bifonksiyonel havuz başına ayrı PF popülasyonu +
   faza özgü oyucu inhibisyon (Shevtsova 2016 deseni), ve bifonksiyonel havuzların resiprokal
   Ia inhibisyon devresinden çıkarılması. Hamstring/RF'nin ikinci patlamasını fizyolojik
   yerinde ancak bu üretir. `PREPRINT.md` 6.4'ün "iki PF'ten girdi" kararı bu aşamada
   literatüre uygun biçimini alır — **bilimsel iddia değişikliği, kullanıcı onayı gerekir.**

Ayrıca Markin ve ark. 2012 (s. 2067–2068) gerçek yürüyüşteki iki eklemli kas desenlerinin büyük
ölçüde **afferent geri beslemeye** bağlı olduğunu söylüyor; Aşama 2'den sonra kalan tutarsızlık
devre hatası değil Ia/II ölçeği sorunu olabilir — ayrı hipotez olarak izlenmeli.

---

# S · 07.09.2026 — Hesaplama maliyetinin dökümü ve sonucu değiştirmeyen hızlandırma

R.1 maliyetin **kırpma rejiminde** nasıl patladığını ölçtü. Bu bölüm tamamlayıcı soruyu ölçer:
sağlıklı rejimde maliyet nerede duruyor ve **sonuç değişmeden** ne kadarı geri alınabilir?

**Bu bölümdeki hiçbir değişiklik projeye uygulanmamıştır.** `neuron/kopru/*.mod` ve
`kod/kopru/*.py` dosyalarına dokunulmadı; ölçümler geçici kopyalar üzerinde yapıldı.

## S.1 · Maliyet dökümü (sağlıklı rejim, kırpmasız pencere)

Ölçüm: 38 havuz + 3 DOF, `dt_k` = 0,15 ms, gerçek köprü (`kos_tumbacak.kur()`), 0,05 s koşu,
`cProfile`; NEURON ve mekanik ayrıca yalıtılmış olarak ölçüldü. Bu pencerede kırpma olayı 0.

| bileşen | maliyet | pay | nasıl ölçüldü |
|---|---|---|---|
| **NEURON** (38 hücre, `IaKopru` takılı) | **174,4 s CPU / sim-s** | ~%82 | yalıtılmış, 100 ms |
| OpenSim `Manager.integrate` | 19,2 s CPU / sim-s (2,9 ms/çağrı) | ~%9 | profil, 333 çağrı |
| Python döngüleri + kayıt | ~19 s CPU / sim-s | ~%9 | fark hesabı |
| köprünün profilli toplamı | 211,6 s CPU / sim-s | — | 0,05 s gerçek koşu |

Mekanik yalıtılmış (600 adım, u=0): sınırsız **2,67 ms/adım**, kırpmalı sınır 2,76, kas kaydı
açık 2,73.

**İki yaygın sezgi ölçülerek yanlışlandı:**

- `kas_durumu()` (aktivasyon + tendon kuvveti kaydı) ek maliyeti **−0,03 ms/adım**, yani gürültü
  içinde. Entegratör Dynamics aşamasını zaten gerçekliyor; kaydı seyreltmenin anlamı yok.
- `man.initialize()` kırpma olayı başına **0,96 ms**. Her adımda tetiklense bile ≤6,4 s CPU/sim-s.
  Kırpmanın asıl maliyeti bu değil, R.1'de ölçülen integratör iç adım patlamasıdır.

**R.1 ile uzlaştırma.** R.1 tablosu sağlıklı rejimde 3,3 ms/köprü adımı gösteriyor; buradaki
toplam ise 211,6 s/sim-s × 0,15 ms ≈ **32 ms/adım**. Çelişki değil: R.1 değerleri OpenSim
`Manager` günlüğünden okunmuştur, yani **OpenSim payıdır** (burada bağımsız olarak 2,9 ms
ölçüldü — örtüşüyor); NEURON payı onun üstüne ~26 ms ekler. `00_DURUM`'daki ~230 s CPU/sim-s
ile de tutarlıdır.

## S.2 · NEURON çok iş parçacığı: 3,4 kat, sonuç bit düzeyinde aynı

38 motonöron elektriksel olarak bağımsızdır (yalnız `NetCon` olaylarıyla haberleşirler), bu
yüzden NEURON'un kendi iş parçacığı bölümlemesine uygundurlar. Ölçüm: 38 Kim hücresi, havuz
kurulumuyla aynı biçimde `IaKopru` takılı, somaya 15 nA `IClamp`, 100 ms,
`h.ParallelContext().nthread(n)`.

| `nthread` | CPU | s CPU / sim-s | hızlanma | soma v maks farkı | AP sayısı farkı |
|---|---|---|---|---|---|
| 1 | 17,44 s | 174,4 | 1,00x | — | — |
| 4 | 7,10 s | 71,0 | 2,46x | **0,000e+00 mV** | **0** |
| 6 | 5,16 s | 51,6 | **3,38x** | **0,000e+00 mV** | **0** |
| 8 | 5,10 s | 51,0 | 3,42x | **0,000e+00 mV** | **0** |

Makine: Mac16,12, 10 çekirdek (4 performans + 6 verimlilik); doyum `nthread` = 6'da.
Aynı sınama `IaSyn`'li (pointer'sız) hücreyle: 151,6 → 39,7 s CPU/sim-s, **3,82x**, fark yine 0.
`cache_efficient(1)` ölçülebilir etki vermedi (%1 altı, gürültü).

Beklenen uçtan uca: NEURON 174 → 52; toplam 212 → ~90 s CPU/sim-s, yani **~2,35 kat**.
Kanonik 3 s koşu ~12-15 dk yerine ~5-6 dk.

## S.3 · Engel: `IaKopru` iş parçacığı güvenli değil (aşıldı, ama bir risk açık)

Gerçek köprüde `pc.nthread()` çağrıldığında NEURON reddediyor:

```
RuntimeError: hocobj_call error: hoc_execerror: IaKopru is not thread safe
```

Sebep: `syn_Ia_kopru.mod` bir `POINTER` (`gsc`) kullanıyor ve NMODL pointer'lı mekanizmaları
varsayılan olarak güvensiz sayıyor. Bizim kullanımımızda pointer **yalnız okunuyor** (Python
adım aralarında yazar, mekanizma hiç yazmaz) ve her havuzun kendi vektörü var.

Sınandı: geçici kopyalara `NEURON { THREADSAFE ... }` satırı eklenip `nrnivmodl` ile derlendi
(`nocmodl` "Thread Safe" bastı); S.2 tablosu **bu yamayla** alınmıştır. Yani engel tek satırla
aşılıyor ve sonuç değişmiyor.

**Açık risk — sınanmadı:** `GradeSyn`'in `vpre` pointer'ı *başka bir hücrenin* voltajını okuyor
(RG↔RG, RG→PF, IIrly→RG; 14 sinaps). Pre ve post hücreler farklı iş parçacığına düşerse bu
gerçek bir yarış koşuludur. Uygulamadan önce gradlı bağlı 14 hücre (2 ML + 6 PF + 6 IIrly)
`pc.partition()` ile tek iş parçacığına sabitlenmeli ve özdeşlik yeniden sınanmalıdır. Maliyet
kaybı yok: yükün tamamı motonöronlardadır.

## S.4 · Sürüşsüz 6 havuz yapısal olarak sıfır üretiyor

`havuz_eslesme.surussuz` (Pir, GMi, OE, OI, Pec, BFa) hiçbir PF grubunun üyesi değil;
`_devre_kur` grup üyeleri üzerinden döndüğü için bu altı havuz PF, II-aktarım, Renshaw ve IaIN
bağlantılarının **hiçbirini** almıyor. Tek girdileri Ia'dır ve Ia tek başına ateşletemez
(reobaz ~10 nA, `devre_par.json` `agirlik_uS._not`).

Ölçüldü (0,5 s duman koşusu `kosu_tumbacak.npz`): altı havuzun toplam aksiyon potansiyeli **0**,
`u` tam olarak 0,000. Aksiyon potansiyeli yoksa `f` sıfır kalır, `u = clip(f/f_ref)` tam
sıfırdır ve efferent tampon zaten sıfırla başlar — yani bu havuzların kurulmayıp kasa doğrudan
`u = 0` yazılması kalan 32 havuz için **matematiksel olarak aynıdır**.

Bütçe payı NEURON maliyetinin %16'sı. Kalibrasyon taramalarında kapatmak ölçülebilir kazanç
verir; kanonik/yayın koşusunda açık bırakmak figür dürüstlüğü açısından tercih edilir (raster
"38 havuz" gösterir ve sessizlik bir bulgudur). Öneri: `devre_par.json`'a bayrak, varsayılanı
açık, kanonik koşuda bu altı havuzun aksiyon potansiyeli sayısının 0 olduğunu doğrulayan assert.

Not: bu, R.2'deki "sessiz kas" bulgusundan **ayrı bir kategoridir**. R'nin saydığı altı sessiz
kas sürülen biartikülerlerdi ve R.5 düzeltmesiyle konuşmaya başladılar; buradaki altı havuz
tasarım gereği sürüşsüzdür.

## S.5 · Ölçülüp reddedilenler ve ucuz kalemler

| aday | karar | gerekçe |
|---|---|---|
| `cache_efficient(1)` | etkisiz | %1 altı fark (gürültü), ölçüldü |
| `kas_durumu()` seyreltme | gereksiz | ek maliyeti ölçülemedi (S.1) |
| `nseg` indirimi / `d_lambda` büyütme | **hayır** | PIC hot-spot konumu ve `IaSyn` dağılımı segment konumlarına bağlı; Kim Tip I/IV/III davranışını değiştirir |
| `dt_k` büyütme | **hayır** | 0,3 ms adım yarılama testini düşürdü (P.5–P.7) |
| entegratör doğruluğunu gevşetme | hayır | OpenSim payı zaten %9 |
| kilitli koordinatları modelden çıkarma | öncelik değil | OpenSim %9; 3 kat kazanç bile toplamda %6 |

Ucuz ve bit düzeyinde aynı iki kalem: (1) profilde `SetMuscles_get` **50.692 çağrı / 334 adım** —
`oku()` ve `kas_durumu()` kas nesnelerini her adımda yeniden çekiyor, kurulumda bir listeye
alınabilir (~%0,5); (2) `h.continuerun(h.t + dt)` yerine adım indeksinden hedef hesaplamak
(hız değil, kayan nokta sürüklenmesine karşı sağlamlık).

**Süreç düzeyinde paralellik.** `adim_yarilama.py` iki koşuyu aynı süreçte sırayla yapıyor.
İkisi bağımsızdır ve zaten aynı süreçte art arda koşamıyorlar — ölçüldü: ikinci `kos()` çağrısı
`Manager.initialize` içinde `Expected stage to be at least Topology ... was Empty` ile düşüyor.
Ayrı süreçlerde paralel koşturmak sıfır riskle duvar saatini yarıya indirir. 10 çekirdekte
tercih: tek kanonik koşu 1 süreç × 6 iş parçacığı; yarılama 2 süreç × 4; parametre taraması
N süreç × 1-2.

## S.6 · Üreten ve yeniden üretim

Ölçüm betikleri geçicidir (depoya girmedi). Yeniden üretim reçetesi:

1. **NEURON payı:** `nrn_hucre.MotoNoron` ile 38 hücre kur, her birine 15 nA `IClamp`,
   `h.dt = 0.025`, `h.continuerun(100)`, CPU süresini ölç.
2. **Çok iş parçacığı:** `neuron/kopru/*.mod` kopyalarına `THREADSAFE` ekle, ayrı bir dizinde
   `nrnivmodl` ile derle, oraya `chdir` edip aynı koşuyu `h.ParallelContext().nthread(n)` ile
   tekrarla; soma voltajlarını ve aksiyon potansiyeli sayılarını `nthread=1` ile karşılaştır.
3. **Mekanik payı:** `osim_mekanik.Mekanik` ile 600 adım `adim()`, `limitler` açık/kapalı ve
   `kas_durumu()` açık/kapalı dört bileşimde.
4. **Köprü profili:** `kos_tumbacak.kur()` + `kk.kos(0.05)` çevresinde `cProfile`.

Uyarı: aynı süreçte `kos()` iki kez çağrılamaz (yukarıdaki `Manager` hatası); her ölçüm noktası
temiz bir süreçte koşulmalıdır.

---

# T · 09.09.2026 — Kanonik koşu tamamlandı; iki yakınsama testi; PIC'in çözünürlük bağımlılığı

Bu oturum üç şey ölçtü: (1) kanonik 3 s tam bacak koşusu **ilk kez tamamlandı** (Q.7 kapandı),
(2) tam bacak zaman adımı yarılama testi **ilk kez koşuldu** (Q.8), (3) yeni bir **uzamsal
yakınsama** testi kuruldu ve segment indirimi denemesi bu testte **düştü**.

## T.1 · Kanonik koşu — Q.7 KAPANDI

`kos_tumbacak.py 3.0`, referans çözünürlük (`d_lambda` = 0,1; havuz başına 2655 segment).
3,0 s simülasyon → **823,6 s CPU**; sınır kırpma olayı 3105 (pasif kontrol koşusunda 998).
Değerlendirme ikinci yarıda (geçici rejim atılır).

| ölçüt | ölçülen | aralık / ölçüt | sonuç |
|---|---|---|---|
| **çevrim süresi** | **0,386 s** | 0,387 · [0,348–0,426] | **ARALIKTA** |
| TA havuzu, etkin faz | **82,71 Hz** | 97 · [80–110] | **ARALIKTA** |
| Soleus havuzu | 16,95 Hz | 28 · [20–35] | dışarıda (düşük) |
| MG / LG havuzu | 17,52 / 17,41 Hz | 67 · [50–90] | dışarıda (düşük) |
| kalça ROM örtüşmesi | 0,10 (−9,00…16,80°) | ≥ 0,5 | kaldı |
| diz ROM örtüşmesi | 0,30 (−122,21…−91,00°) | ≥ 0,5 | kaldı |
| bilek ROM örtüşmesi | 0,43 (−34,00…25,09°) | ≥ 0,5 | kaldı |
| antagonist zıtfaz (kalça/diz/bilek) | −0,548 / −0,775 / −0,787 | zıtfaz | sağlandı |
| sessiz kas (sürülen 32 havuz) | 0 | 0 | sağlandı |

**Yeni olan:** çevrim süresi tam bacakta **ilk kez ölçülebildi ve aralığa düştü.** R.7'nin
1,2 s'lik koşusunda kalça ortalama geçişi yetersiz olduğu için ölçülememişti. R.1'de aynı koşu
1,28 s'te integratör çöküşüyle durmuştu; R.5 düzeltmesinden sonra 3 s temiz tamamlanıyor.

Eklem sınırına yaslanma oranı: kalça %52, diz %51, bilek %32. Yani ritim doğru periyotta ama
uzuv fizyolojik açıklıkta hareket etmiyor; iki bulgu birlikte okunmalıdır.

Artefakt: `veri/kopru/kosu_tumbacak.npz` (`d_lambda` ve `segment_havuz` alanları bu oturumda
eklendi — figürler hangi ızgarada üretildiklerini dosyadan okuyor).
Figürler: `sekiller/kopru_tumbacak_{raster,nedensellik,pasif}.png` + `.csv`.
GUI: `veri/goruntuleme/kopru_tumbacak.mot` (607 satır, 53 sütun; OpenSim `Storage` ile doğrulandı).

## T.2 · Q.8 · Zaman adımı yarılama (tam bacak) — dokuz ölçüt geçti, biri kıl payı düştü

`adim_yarilama.py 3.0 --tumbacak`; `dt_k` 0,150 → 0,075 ms, iki tam 3 s koşu (1111,6 + 1264,3 s
CPU). Aralıklar testten önce ilan edilmişti (çevrim %5, ROM %10, ateşleme %10).

| ölçüt | 0,150 ms | 0,075 ms | bağıl fark | sonuç |
|---|---|---|---|---|
| çevrim süresi | 0,3861 s | 0,3860 s | **%0,02** | geçti |
| ROM kalça | 25,80° | 25,57° | %0,88 | geçti |
| ROM diz | 31,21° | 29,86° | %4,32 | geçti |
| ROM bilek | 59,09° | 62,27° | %5,10 | geçti |
| havuz kalça-flx / kalça-ext / diz-ext / bilek-df | — | — | ≤ %0,02 | geçti |
| havuz diz-flx | 15,65 Hz | 15,09 Hz | %3,54 | geçti |
| **havuz bilek-pf** | **17,83 Hz** | **19,83 Hz** | **%10,05** | **DÜŞTÜ** |

**Okunuşu.** Ritmin ve mekaniğin taşıdığı büyüklükler adımdan bağımsızdır (çevrim süresi %0,02;
eklem açıklıkları ≤ %5,1). Yakınsamayan tek büyüklük **en düşük ateşleyen grubun** oranıdır ve
oradaki **mutlak fark 2 Hz'dir**; küçük tabanda bu %10'u 0,05 puanla aşıyor. Aynı grup
(`bilek_pf`, denge ölçeği 0,372) R.10'un kalibrasyon ekseninde zaten işaretlidir.
**Aralık genişletilmedi** (04_KURALLAR). Sonuç: bilek plantar fleksör havuzunun ateşleme oranı
bugün bir sayı olarak bildirilemez; çevrim süresi ve eklem açıklıkları bildirilebilir.

**Yan bulgu — yeniden üretilebilirlik:** yarılamanın `dt_k` = 0,150 kolu, **ayrı bir süreçte**
kanonik koşuyu birebir yeniden üretti (T 0,3861 vs 0,3860; kalça 25,80 · diz 31,21 · bilek 59,09
— üçü de aynı). Koşu süreçten bağımsız olarak tekrarlanabilir.

Artefakt: `veri/kopru/yakinsama_zaman.json` (assert'lerden **önce** yazılır; düşen bir ölçüt de
bir ölçüm sonucudur ve figüre girer).

## T.3 · Yeni test: uzamsal (çözünürlük) yakınsaması — köprü düzeyinde DÜŞTÜ

`PREPRINT` 8 zamansal yakınsama testini zorunlu sayar; bu onun uzamsal karşılığıdır ve bu
oturumda kuruldu (`kod/kopru/uzamsal_yakinsama.py`). İki aşamalı: tek hücre (reobaz, f-I, PIC
histerezi) ve köprü (çevrim süresi, eklem ROM, havuz ateşleme). Bantlar testten önce ilan edildi
ve betiğin başlığında gerekçesiyle duruyor. Her çözünürlük noktası ayrı süreçte koşar (S.5).

**Aşama A — tek hücre: GEÇTİ**

| ölçüt | `d_l`=0,1 | `d_l`=1,0 | fark |
|---|---|---|---|
| segment | 2655 | 485 | 5,47 kat az |
| PIC toplam `gcalbar` | 0,40513 | 0,40513 | eşit (inşa gereği, T.4) |
| reobaz | 4,607 nA | 4,446 nA | %3,50 (bant %10) |
| f @ 1,5× ve 2,0× reobaz | 10,0 / 15,0 Hz | 10,0 / 15,0 Hz | %0 |
| PIC histerez kategorisi | var | var | aynı |
| histerez `dI` (rapor, assert değil) | 2,610 nA | 3,965 nA | +%52 |
| \|D_path − 600\| ort / maks | 9,8 / 29,2 µm | **63,4 / 259,4 µm** | — |

**Aşama B — köprü (1,2 s): DÜŞTÜ**

| ölçüt | `d_l`=0,1 | `d_l`=1,0 | bağıl fark | sonuç |
|---|---|---|---|---|
| ROM bilek | 76,33° | 59,84° | **%21,60** | **DÜŞTÜ** (bant %10) |
| ROM kalça / diz | 26,55 / 31,88° | 27,12 / 31,76° | %2,10 / %0,38 | geçti |
| havuz `bilek_pf` | 20,15 Hz | 22,20 Hz | %9,23 | geçti (sınırda) |
| diğer beş havuz | — | — | ≤ %4,50 | geçti |
| **CPU** | **282,5 s** | **391,2 s** | **0,72 kat (YAVAŞLADI)** | — |

**Karar: `d_lambda` = 1,0 reddedildi**, bant genişletilmedi, üretim Kim'in 0,1 değerinde kaldı.
`devre_par.json`'a `hucre` bloğu **eklenmedi**; koddaki parametreleştirme varsayılanı 0,1'dir ve
`capraz_kontrol.py` bit düzeyinde geçmeye devam ediyor.

**Hücre düzeyinde geçen bir değişiklik köprü düzeyinde düşüyor** — testin iki aşamalı olmasının
gerekçesi budur. Tek hücre ölçütleri, hücrenin kaba ızgarada da makul davrandığını gösteriyor;
kapalı döngüde ise yörünge değişiyor.

## T.4 · PIC iletkenliği `nseg`'e bağlıdır (bulundu ve düzeltildi)

`nrn_hucre._pic_yerlestir`, PIC nokta sürecinin iletkenliğini `yoğunluk × segment alanı` ile
hesaplıyordu — Kim'in `add_pics_istim.hoc:57`'si de öyle. Segment uzayınca alan büyüdüğü için
**toplam PIC iletkenliği çözünürlüğe bağlıdır**. Ölçüldü (38 hücre, 15 nA, 100 ms):

| ayar | PIC toplam `gcalbar` | ortalama AP | soma v |
|---|---|---|---|
| `d_l`=0,1 (referans) | 0,40513 | 2 | −54,56 mV |
| `d_l`=1,0, Kim formülü aynen | **2,54489** (6,3 kat) | **17** | −39,20 mV |
| `d_l`=1,0, toplam korunmuş | 0,40513 | 2 | −53,26 mV |

Düzeltilmezse hücre 8,5 kat fazla aksiyon potansiyeli üretir ve **hiçbir yerde hata vermez**.
Düzeltme: `gcalbar` artık segment alanından değil, referans çözünürlükte bir kez kurulan
tablodan okunur (`_pic_referans`, süreç başına tek hücre kurulumu ≈ 0,1 s). PIC taşıyan kesit
kümesi her iki çözünürlükte de **aynı 86 kesittir** (kesme testi kesit uçlarına bakar,
segmentlere değil), bu yüzden eşleme kesit adıyla birebir kurulabiliyor ve değerler nokta nokta
özdeş çıkıyor.

**Düzeltilemeyen kısım:** PIC noktası hedefe en yakın **segment merkezine** düşer; kaba ızgarada
konum hatası 9,8 → 63,4 µm (maks 29,2 → 259,4 µm). Kesirli `x` bunu çözmez (nokta süreci içinde
bulunduğu segmente atanır). Kim'in duyarlı olduğu eksen budur (`oz_kim2020` §4b, Tip I/IV/III);
histerez `dI`'nin %52 büyümesi bununla tutarlıdır.

Ia sinapsı etkilenmez: `IaSyn`/`IaKopru` bir **yoğunluk** mekanizmasıdır, toplam iletkenlik kesit
alanına bağlıdır ve segment sayısından bağımsızdır (Ia segmenti 1692 → 354 düşer, toplam sabit).

## T.5 · Ölçülüp reddedilen: hibrit çözünürlük

Her yer `d_lambda`=1,0, yalnız PIC taşıyan 86 kesit 0,1'de tutulur. Ölçüldü: PIC konum hatası ve
soma voltajı referansla **birebir aynı** (9,8 / 29,2 µm, −54,56 mV) ama o 86 kesit ince ızgaranın
2655 segmentinin **1190'ını** taşıdığından segment 1507'de kalıyor ve hızlanma 5,09 kat yerine
yalnız **1,72 kat** oluyor. Hedeflenen indirimle bağdaşmadığı için uygulanmadı.

## T.6 · Segment indirimi köprüyü hızlandırmıyor

S.2'de NEURON payının izole ölçümü 5,09 kat hızlanma gösteriyordu (172,1 → 33,6 s CPU/sim-s).
Köprü düzeyinde ölçüldüğünde koşu **%38 pahalılaştı** (282,5 → 391,2 s). İki koşu paralel
süreçlerdeydi, yani CPU rakamları temiz bir hız ölçümü değildir; ama *yavaşlama yönü* çekişmeyle
açıklanamaz. En olası açıklama R.1'in bilinen rejimidir: kaba hücre yörüngeyi değiştirip
eklemleri kırpma sınırlarına daha çok sürüyor, integratör iç adımları patlıyor ve NEURON'dan
kazanılan pay OpenSim tarafında fazlasıyla geri veriliyor.

**Ders:** NEURON payının izole hızlanması köprü hızlanması demek değildir; hızlandırma
iddiaları köprü düzeyinde ölçülmelidir.

## T.7 · Bağımsız yeniden üretimler (figür üretirken ölçüldü)

- **Moment kolları.** `dogrulama_momentkolu.png` modeli açıp `computeMomentArm`'ı canlı çağırıyor.
  Diz −120°, `cl_grid3d` FIX pozunda: RF **+3,697** · VL **+3,727** · VI **+3,723** ·
  VM **+3,703** · SM **−3,88** · STa −15,47 · STp −14,99 · BFp −13,77 · GP −12,34 · GA −9,40 ·
  Pla −4,13 · MG −3,43 · LG −3,08 · Pop −1,59 mm. A bölümünün 27.07.2026 tablosunu ≤ 0,02 mm
  farkla yeniden üretiyor (LG 0,15 ve Pop 0,07 mm sapıyor; ikisi de poza duyarlı).
- **Sarma açık/kapalı.** Quadriceps sarma kapatıldığında RF **−0,65** · VL **−1,18** ·
  VI **−0,61** · VM **−0,97** mm — H1 tablosunun **birebir** yeniden üretimi.
- **Yeni ölçüm — moment kolu poza bağlıdır.** SM'nin *diz* moment kolu kalça açısıyla
  −3,98 (kalça −10°) → −3,50 mm (kalça +85°) arasında değişiyor. Kayıtlı −3,87 mm bu aralığın
  içindedir ama tek başına bir sayı değil, **pozuyla birlikte** bir sayıdır. `PREPRINT` 9.1'de
  ölçüm pozu yazılmalıdır.
- **Salınım fazı zamanlaması.** `veri/u_swing_v2.csv`'den bağımsız olarak yeniden hesaplandı;
  `PREPRINT` 9.2'nin grup toplamlarını **birebir** verdi (7,851 / 1,431 / 0,502 / 0,883 /
  1,197 / 1,444) ve tepe zamanlarını da (%68,5 / %66,5 / %76,0 / %65,0 / %85,5 / %87,0).
- **HOC çapraz kontrolü.** 315/315 section, 2655/2655 segment, 28/28 aksiyon potansiyeli,
  zaman farkı **0,000000 ms**, soma voltaj farkı **0,000000 mV**.

## T.8 · Üreten ve yeniden üretim

Yeni dosyalar: `kod/kopru/uzamsal_yakinsama.py`, `kod/kopru/figur_ortak.py`,
`kod/kopru/figur_dogrulama.py`, `RAPOR_GECERLILIK.md`.
Değişenler: `nrn_hucre.py` (`d_lambda` parametresi + PIC referans tablosu), `kopru.py`
(çözünürlük `devre_par.hucre`'den okunur), `kos_tumbacak.py` (çıktıya çözünürlük provenance'ı),
`kos_ayakbilegi.py` (`par_yol`), `adim_yarilama.py` ve `capraz_kontrol.py` (artefakt yazımı).

```bash
P=$HOME/.venvs/usk26-kopru/bin/python
$P -u kod/kopru/kos_tumbacak.py 3.0                            # T.1
$P -u kod/kopru/adim_yarilama.py 3.0 --tumbacak                # T.2
$P -u kod/kopru/uzamsal_yakinsama.py 1.2 --tumbacak --dl 1.0   # T.3
$P kod/kopru/figur_tumbacak.py && $P kod/kopru/figur_dogrulama.py
$P kod/kopru/gui_disaver.py --tumbacak
```

Uyarı: `veri/kopru/yakinsama_uzam.json` bu oturumun koşusunun **ekran çıktısından** üretildi
(JSON yazma özelliği betiğe koşudan sonra eklendi); ham log `arsiv/loglar/` altındadır
(git-ignore) ve sayılar T.3'te tam olarak durur. Sonraki koşular dosyayı kendileri yazar.
