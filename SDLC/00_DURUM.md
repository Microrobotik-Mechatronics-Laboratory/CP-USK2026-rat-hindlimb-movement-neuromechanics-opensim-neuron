# DURUM — Anlık Proje Panosu

> SICAK: Bu dosya her oturum kapanışında güncellenir. Yeni oturumda **ilk okunacak** dosyadır.

**Son güncelleme:** 2026-09-05

## Şu anki odak
**Dizin hiyerarşisi yeniden kuruldu ve `PREPRINT.md` bilimsel tek doğruluk kaynağı olarak yazıldı.**
Numaralı klasörler (`01_..07_`) numarasız anlamlı adlara geçti (`model/ veri/ kod/ neuron/
sekiller/ literatur/`); aşılmış kuşaklar `arsiv/` altına ayrıldı; tüm yol referansları projenin
her yerinde güncellendi. Betikler artık çalışma dizinine bağlı değil (`kod/yollar.py`).
Bildiri özetine sadık; omurilikten kasa uzanan kapalı döngünün nöron-kas mimarisi (CPG →
internöron → 38 motonöron havuzu → u(t) → OpenSim → iğcik → Ia) tasarım olarak yazıldı ve
`literatur/diyagramlar/` altında 8 Mermaid diyagramıyla gösterildi; diyagramlar PREPRINT'e
gömüldü. Eski basma fazı / fenomenolojik kapalı-döngü anlatısı preprintten çıkarıldı (dosyalar
duruyor). Teknik cephe hâlâ İP-4a: `module1_2.mod` derlenmiyor.

## Sıradaki somut adım
- **İP-4a:** `neuron/fig2_4_6/module1_2.mod` içindeki `U` çakışmasını çöz
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
- **`literatur/diyagramlar/` kuruldu** (D1–D8 + README + drift kuralı). 22 Mermaid bloğunun
  tamamı `mermaid-cli` ile derlenerek doğrulandı.
- **Kapsam kararları alındı** (kullanıcı): NEURON tarafı tasarım + hedef kapalı döngü olarak
  yazılır; kas başına bir motonöron havuzu (38); eski basma fazı/emergent anlatısı preprintten
  çıkarılır; semimembranosus için ölçülen −3,87 mm esas alınır.
- **Yeni ölçümler** (bu oturumda, `veri/kapali_dongu/cl_grid3d.npz` ve `veri/u_swing_v2.csv`
  üzerinden): 38 kasın üç eklem için moment kolu ve işaret kararlılığı tablosu; salınım fazı
  grup zamanlamaları.
- **Terim denetimi:** uydurma Türkçe karşılıklar temizlendi; PREPRINT'e bölüm 16 (Terimler)
  eklendi — her terimin literatürdeki İngilizce özgün karşılığı ve bu çalışmada tanımlanan
  ölçütlerin ayrı listesi. Dizin yeniden düzenlemesinden sonra tüm dosya yolları güncellendi.
- **Dizin hiyerarşisi yeniden düzenlendi:** klasörler numarasız anlamlı adlara alındı; Kim 2020
  hoc/mod ağacı `neuron/` oldu (dış kaynak değil, kaynak kodumuz); doğrulama defteri köke
  `DOGRULAMA.md` olarak taşındı; `OKU.txt` kaldırılıp `README.md` klasör haritasına katlandı;
  aşılmış her şey `arsiv/` altına (kendi README'siyle) ayrıldı.
- **Yol sözleşmesi:** `kod/yollar.py` eklendi; hiçbir betik artık çıplak dosya adı veya yabancı
  mutlak yol (`/home/claude/oturum5/`, `/mnt/user-data/uploads/`) kullanmıyor. Kural
  `04_KURALLAR.md`'ye yazıldı.
- **Bağımlılık beyanı:** `matplotlib` + `cma` → `pyproject.toml`/`uv.lock`; `opensim` + `scipy`
  → yeni `requirements-opensim.txt`. Yazım hatalı `requiremnts.txt` kaldırıldı (risk-2, risk-10).
- **Doğrulama (koşularak):** `cl_teslim_9of9.py` yeniden koşuldu — 24 çıktı dizisi ve PNG taşıma
  öncesiyle **birebir aynı**; `kod_02_swing_id_so.py` `.venv-osim` ile koşuldu ve
  `u_swing_v2.csv`'yi **sıfır farkla** yeniden üretti; `neuron/fig2_4_6`'da `nrnivmodl`
  taşımadan önceki aynı hatayı veriyor (`module1_2.mod` `U` çakışması) — taşıma bir şey
  değiştirmedi.

## Açık sorular
- **Yeni:** `GMa` (gluteus maximus) modelde kalça **fleksörü** çıkıyor (+5,39 mm, ızgaranın
  tamamında aynı işaret); anatomide ekstansördür. Bağlantı noktası hatası mı, işaret sözleşmesi
  farkı mı? Salınım fazı sıra bulgusu buna bağlı (PREPRINT 10.4).
- **Yeni:** `IaIN` ve `Renshaw` katmanlarının literatür setinde kaynağı yok — kaynak eklenecek mi,
  ilk sürümde devre dışı mı bırakılacak? (PREPRINT 6.1)
- **Yeni:** Blum 2020'nin literatür özeti yok; Ia denklemi özeti çıkarılmamış bir JSON kaydına
  dayanıyor.
- `module1_2.mod`'da `U`'yu `RANGE`'den çıkarmak HOC tarafını bozar mı? (GUI'den `U`'ya erişim
  varsa alternatif ad gerekir.)
- Aşama 2 köprüsü iki ayrı Python ortamını (3.14 NEURON / 3.13 OpenSim) nasıl buluşturacak?
  Kapalı-döngü saf NumPy olduğu için çalışma anında OpenSim gerekmiyor; bu ayrımın köprüyü
  kısıtlamadığı doğrulanmalı. Bkz. `05_MIMARI_RISK.md` risk-1.

## Bloke edenler / riskler
- `kod/opensim/rig.py` **eksik ama kayıp değil** — git geçmişinde duruyor:
  `git show e0192ec^:kod/rig.py` (79 satır). Getirilene kadar `kod_01_rat_walk_bone_uret.py`
  koşmuyor (iki `bauman_fig4_*.csv` girdisi de eksik). → İP-5.
- ~~Çalışmaya-kritik dosyalar depo dışında~~ **Bu kayıt yanlıştı (2026-09-05'te yeniden ölçüldü):**
  `cl_grid3d.npz`, güncel `cl_*.py` ve `cl_best_9of9.json` **depodadır**; kapalı döngü bu makinede
  koşuyor. `model/Geometry/` de depodadır.
- `veri/kapali_dongu/cl_grid3d.npz` ve `arsiv/veri/cl_ref.npz` **yeniden üretilemez** —
  üreteçleri (`stage0_grid.py`, `gate2_ref.py`) hiç depoya girmedi. Birincil varlık gibi korunur.
- ~~Bildirilmeyen bağımlılıklar~~ **Kapandı** (risk-2).

## Bekleyen
- ~~push bekleyen commit~~ **Yapıldı:** 15 yerel commit `origin/main`'e rebase edilip
  push edildi (2026-09-05). Uzakta bu arada eklenen GitHub Actions workflow'ları
  (`.github/workflows/`, PR #1) yerele alındı; çakışma olmadı.
- ~~`literatur/` boş~~ **7 literatür özeti eklendi** (Johnson, Kim, Vincent, Gorassini, Yu,
  Fietkiewicz 2023/2025). Eksik: Blum 2020.
- Literatür özetlerinde hazır olup `referans_degerler.json`'a **girmemiş** bantlar var (Vincent 6, Gorassini 6,
  Kim 1, Johnson 1) — İP-8 girdisi.
