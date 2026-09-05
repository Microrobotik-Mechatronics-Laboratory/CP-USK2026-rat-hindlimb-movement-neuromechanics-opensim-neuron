# DURUM — Anlık Proje Panosu

> SICAK: Bu dosya her oturum kapanışında güncellenir. Yeni oturumda **ilk okunacak** dosyadır.

**Son güncelleme:** 2026-09-05

## Şu anki odak
**`PREPRINT.md` sıfırdan yeniden yazıldı ve projenin bilimsel tek doğruluk kaynağı ilan edildi.**
Bildiri özetine sadık; omurilikten kasa uzanan kapalı döngünün nöron-kas mimarisi (CPG →
internöron → 38 motonöron havuzu → u(t) → OpenSim → iğcik → Ia) tasarım olarak yazıldı ve
`07_literatur/diyagramlar/` altında 8 Mermaid diyagramıyla gösterildi; diyagramlar PREPRINT'e
gömüldü. Eski basma fazı / fenomenolojik kapalı-döngü anlatısı preprintten çıkarıldı (dosyalar
duruyor). Teknik cephe hâlâ İP-4a: `module1_2.mod` derlenmiyor.

## Sıradaki somut adım
- **İP-4a:** `inline-supplementary-material-1/fig2_4_6/module1_2.mod` içindeki `U` çakışmasını çöz
  (`U` hem `RANGE` değişkeni satır 10, hem `FUNCTION` satır 133; NEURON 9 reddediyor). İlk
  denenecek: `RANGE` listesinden `U`'yu çıkarmak — önce HOC tarafının `U`'ya eriştiği yerleri
  kontrol et. Çözülünce `fig3_5_7`, `fig8`, `fig9` klasörlerini de derle.

## Aktif iş paketi
İP-4a (NEURON derleme + tek nöron doğrulaması) — bkz. `02_IS_PAKETLERI.md`.
Yol haritasının tamamı artık `PREPRINT.md` bölüm 13'tedir.

## Bu oturumda kapanan
- **PREPRINT yeniden kuruldu** (1056 satır, 11 gömülü diyagram): amaç, mimari, kas-iskelet tarafı,
  omurilik tasarımı, iğcik/afferent, köprü, bulgular, farklar, sınırlılıklar, doğrulama planı,
  yol haritası, açık sorular, kaynaklar.
- **`07_literatur/diyagramlar/` kuruldu** (D1–D8 + README + drift kuralı). 22 Mermaid bloğunun
  tamamı `mermaid-cli` ile derlenerek doğrulandı.
- **Kapsam kararları alındı** (kullanıcı): NEURON tarafı tasarım + hedef kapalı döngü olarak
  yazılır; kas başına bir motonöron havuzu (38); eski basma fazı/emergent anlatısı preprintten
  çıkarılır; semimembranosus için ölçülen −3,87 mm esas alınır.
- **Yeni ölçümler** (bu oturumda, `cl_grid3d.npz` ve `u_swing_v2.csv` üzerinden): 38 kasın üç
  eklem için moment kolu ve işaret kararlılığı tablosu; salınım fazı grup zamanlamaları.

## Açık sorular
- **Yeni:** `GMa` (gluteus maximus) modelde kalça **fleksörü** çıkıyor (+5,39 mm, ızgaranın
  tamamında aynı işaret); anatomide ekstansördür. Bağlantı noktası hatası mı, işaret sözleşmesi
  farkı mı? Salınım fazı sıra bulgusu buna bağlı (PREPRINT 10.4).
- **Yeni:** `IaIN` ve `Renshaw` katmanlarının literatür setinde kaynağı yok — kaynak eklenecek mi,
  ilk sürümde devre dışı mı bırakılacak? (PREPRINT 6.1)
- **Yeni:** Blum 2020'nin özütü yok; Ia denklemi özütsüz bir JSON kaydına dayanıyor.
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
- ~~push bekleyen commit~~ **Yapıldı:** 15 yerel commit `origin/main`'e rebase edilip
  push edildi (2026-09-05). Uzakta bu arada eklenen GitHub Actions workflow'ları
  (`.github/workflows/`, PR #1) yerele alındı; çakışma olmadı.
- ~~`07_literatur/` boş~~ **7 özüt eklendi** (Johnson, Kim, Vincent, Gorassini, Yu, Fietkiewicz
  2023/2025). Eksik: Blum 2020 özütü.
- Özütlerde hazır olup `referans_degerler.json`'a **girmemiş** bantlar var (Vincent 6, Gorassini 6,
  Kim 1, Johnson 1) — İP-8 girdisi.
