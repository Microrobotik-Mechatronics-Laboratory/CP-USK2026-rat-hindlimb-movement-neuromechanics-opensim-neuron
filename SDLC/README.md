# SDLC — Projenin Kurumsal Hafızası

Bu klasör, projenin **tek doğruluk kaynağıdır** (single source of truth). Amacı: yeni bir
Claude oturumu açıldığında, hiçbir ek açıklama yapılmadan projenin ne olduğunu, nerede
kaldığımızı ve nasıl çalıştığımızı bilmesi.

> Oturum başında kök dizindeki `CLAUDE.md` bu klasörü otomatik okutur. Ayrıca istediğiniz
> zaman **"SDLC klasörünü oku"** diyebilirsiniz.

## Dosyalar ve okuma sırası

| Dosya | İçerik | Değişim sıklığı |
|---|---|---|
| `00_DURUM.md` | **Anlık durum panosu** — şu an neredeyiz, sıradaki adım | SICAK — her oturum |
| `03_GUNLUK.md` | **Oturum günlüğü** — ne yaptık (append-only, tarihli) | SICAK — her oturum |
| `01_PROJE.md` | Proje tanımı, amaç, kapsam, kas-NEURON köprüsü, kaynaklar | referans (nadir) |
| `02_IS_PAKETLERI.md` | İş paketleri (WBS) ve durumları | yarı-sıcak |
| `04_KURALLAR.md` | Git, bağımlılık, dokümantasyon, yorum, test, raporlama kuralları | referans (nadir) |
| `05_MIMARI_RISK.md` | Veri-akış haritası + bilinen riskler | referans (nadir) |
| `06_KURULUM.md` | Sıfırdan kurulum (uv, iki ortam, NEURON derlemesi) | referans (nadir) |

**Sıcak dosyalar** (SICAK) her oturum güncellenir. Diğerleri sadece ilgili şey değişince.

**Projeyi ilk kez kuruyorsanız** doğrudan `06_KURULUM.md`'ye gidin. Proje **iki ayrı Python
ortamı** ister (3.14 NEURON / 3.13 OpenSim); sebebi orada anlatılır.

Bu klasöre **kopyalanmayan**, referans verilen kaynaklar:
- `../PREPRINT.md` — bildiri özeti (dokunulmaz referans), taahhüt kontrol listesi ve bildiri ile
  doğrulanmış durum arasındaki farklar. **Ne yapmaya çalıştığımızın anlatımı buradadır.**
- `../README.md` — klasör/dosya manifestosu (kapı belgesi)
- `../DOGRULAMA.md` — bilimsel doğrulama defteri
- `../literatur/` — literatür özetleri + testlerin okuduğu `referans_degerler.json`

---

## Oturum-Başı Protokolü

1. **`00_DURUM.md` oku** (zorunlu, her zaman).
2. **`03_GUNLUK.md`'nin son kaydını oku.**
3. Göreve göre gerekirse:
   - kod/git/test/yorum yazacaksan → `04_KURALLAR.md`
   - kapsam/hedef/iş paketi → `01_PROJE.md` + `02_IS_PAKETLERI.md`
   - teknik akış/risk → `05_MIMARI_RISK.md`
   - ortam kurulumu/çalıştırma → `06_KURULUM.md`
   - literatür değeri veya tolerans bandı → `../literatur/referans_degerler.json`
4. Kullanıcıya **2-3 satır özet** ver: "Şu an X iş paketindeyiz, son oturumda Y yaptık,
   sıradaki adım Z." Ekstra soru sormadan çalışmaya hazır ol.

## Oturum-Kapanış Protokolü

1. **`00_DURUM.md` güncelle:** şu anki odak, sıradaki somut adım, açık sorular, bloke edenler,
   "Son güncelleme" tarihi (bugünün tarihi).
2. **`03_GUNLUK.md`'ye tarihli yeni kayıt ekle** (append-only — eski kayıtlar ASLA düzenlenmez):
   ne yapıldı, kararlar, sonuç/artefakt, değişen dosyalar, commit hash'i.
3. İlerleme olduysa **`02_IS_PAKETLERI.md`** durumlarını güncelle.
4. Kural/kapsam/risk değiştiyse (nadiren) ilgili referans dosyasını güncelle.
5. **Otomatik commit** (bkz. `04_KURALLAR.md` commit biçimi). **Push için kullanıcıya sor.**

> Bu iki protokolü `logger` alt-ajanı da yürütebilir: `logger` ajanını çağırmak,
> kapanış adımlarını sizin yerinize sırayla uygular.
