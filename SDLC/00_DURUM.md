# DURUM — Anlık Proje Panosu

> SICAK: Bu dosya her oturum kapanışında güncellenir. Yeni oturumda **ilk okunacak** dosyadır.

**Son güncelleme:** 2026-09-05

## Şu anki odak
SDLC genişletildi: kurulum belgesi yazıldı, kas-NEURON köprüsü kapsama alındı, literatüre-yakınlık
test kuralı ve figür/rapor dışa aktarma standardı tanımlandı, `07_literatur/` iskeleti kuruldu.
Teknik cephe İP-4a: NEURON motonöron modelinin bu makinede derlenmesi — **derleme yolu çözüldü,
tek bir mekanizma dosyası kaldı.**

## Sıradaki somut adım
- **İP-4a:** `inline-supplementary-material-1/fig2_4_6/module1_2.mod` içindeki `U` çakışmasını çöz
  (`U` hem `RANGE` değişkeni satır 10, hem `FUNCTION` satır 133; NEURON 9 reddediyor). İlk
  denenecek: `RANGE` listesinden `U`'yu çıkarmak — önce HOC tarafının `U`'ya eriştiği yerleri
  kontrol et. Çözülünce `fig3_5_7`, `fig8`, `fig9` klasörlerini de derle.

## Aktif iş paketi
İP-4a (NEURON derleme + tek nöron doğrulaması) — bkz. `02_IS_PAKETLERI.md`.

## Bu oturumda kapanan
- **İP-4'ün "nereye bağlanacak?" sorusu kapandı:** iki aşamalı köprü tanımlandı
  (Aşama 1 tek nöron doğrulama, Aşama 2 havuz ile kas arasında u(t) çıkışı / r(t) Ia girişi).
  Tanım: `01_PROJE.md`; iş paketi: İP-4a / İP-4b.
- **Derleme yolu engeli çözüldü:** NEURON boşluksuz yola (`~/.venvs/usk26`) alındı; `fig2_4_6`'daki
  12 mekanizmanın 11'i derlendi.

## Açık sorular
- `module1_2.mod`'da `U`'yu `RANGE`'den çıkarmak HOC tarafını bozar mı? (GUI'den `U`'ya erişim
  varsa alternatif ad gerekir.)
- Aşama 2 köprüsü iki ayrı Python ortamını (3.14 NEURON / 3.13 OpenSim) nasıl buluşturacak?
  Kapalı-döngü saf NumPy olduğu için çalışma anında OpenSim gerekmiyor; bu ayrımın köprüyü
  kısıtlamadığı doğrulanmalı. Bkz. `05_MIMARI_RISK.md` risk-1.

## Bloke edenler / riskler
- `03_kod/rig.py` **depoda yok** — `kod_01_rat_walk_bone_uret.py` bunsuz koşmuyor (yeni bulgu).
- Çalışmaya-kritik diğer dosyalar depo dışında: güncel `cl_*.py`, `cl_grid3d.npz`, `cl_best.json`,
  `Geometry/`. Detay: `05_MIMARI_RISK.md` risk-6.
- Bildirilmeyen bağımlılıklar: `opensim`, `scipy`, `matplotlib`, `cma` (risk-2, İP-5).

## Bekleyen
- `main` üzerinde origin'in önünde **yerel commit'ler** var; push kullanıcı onayı bekliyor
  (kullanıcı 2026-09-05 oturumunda "şimdilik bekle" dedi).
- `07_literatur/` iskeleti hazır ama **boş**: makale PDF'leri konup özütler çıkarılacak (İP-7).
