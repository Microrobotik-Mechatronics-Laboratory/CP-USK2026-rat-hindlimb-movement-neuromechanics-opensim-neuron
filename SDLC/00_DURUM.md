# DURUM — Anlık Proje Panosu

> SICAK: Bu dosya her oturum kapanışında güncellenir. Yeni oturumda **ilk okunacak** dosyadır.

**Son güncelleme:** 2026-09-05

## Şu anki odak
SDLC kurumsal-hafıza sistemi yeni kuruldu. Proje bilimsel olarak "kapalı-döngü teslim (9of9)"
aşamasında; sıradaki teknik cephe NEURON motonöron modelinin bu makinede (Darwin) derlenip
Python hattına entegre edilmesi.

## Sıradaki somut adım
- **İP-4:** `inline-supplementary-material-1/` altındaki `.mod` dosyalarını Darwin'de
  `nrnivmodl` ile yeniden derle (mevcut `.o`/`.dll` ikilileri Windows-derlenmiş, bu makinede çalışmaz).

## Aktif iş paketi
İP-4 (NEURON modeli derleme & entegrasyon) — bkz. `02_IS_PAKETLERI.md`.

## Açık sorular
- NEURON modeli hangi noktada kapalı-döngü kontrolcüye (`04_kapali_dongu`) bağlanacak? (motonöron
  havuzu mu, sadece PIC/refleks parametreleri mi?)

## Bloke edenler / riskler
- Çalışmaya-kritik bazı dosyalar depo dışında (başka bilgisayarda): güncel `cl_*.py`,
  `cl_grid3d.npz`, `cl_best.json`, `Geometry/`. Detay: `05_MIMARI_RISK.md`.
- Bildirilmeyen çalışma-zamanı bağımlılıkları: `opensim`, `scipy`, `cma` (pyproject/uv.lock'ta yok).

## Bekleyen
- `main` üzerinde origin'in önünde **6 yerel commit** var; push kullanıcı onayı bekliyor
  (kullanıcı 2026-09-05 oturumunda "şimdilik bekle" dedi).
