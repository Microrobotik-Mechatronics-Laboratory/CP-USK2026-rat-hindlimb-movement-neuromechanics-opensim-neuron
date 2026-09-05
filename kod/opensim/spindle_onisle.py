# spindle_onisle.py — Blum 2020 ham verisini fit için ortak forma indirger (47_ B26 ADIM 1)
# Her deneme: 1 kHz'e yeniden örneklenmiş t, L (mm, taban çıkarılmış), v=dL/dt (mm/s),
# F (N), yank=dF/dt (N/s) + spike zamanları ve ölçülmüş anlık ateşleme (IFR).
# Kanal türetimleri: v ve yank, 1 kHz'e indirgendikten sonra 51 örneklik Savitzky-Golay
# türeviyle (pürüzsüz türev; ham fark alma 10 kHz gürültüsünü patlatır).
import numpy as np, scipy.io as sio
from scipy.signal import savgol_filter
import glob, pickle

FS = 1000.0
KOK = '/mnt/user-data/uploads/spindle_data/eLife_data/'

def deneme_isle(p):
    t = np.asarray(p.time).ravel().astype(float)
    L = np.asarray(p.Length).ravel().astype(float)
    F = np.asarray(p.Force).ravel().astype(float)
    if len(t) < 100: return None
    tg = np.arange(t[0], t[-1], 1.0/FS)
    Lg = np.interp(tg, t, L); Fg = np.interp(tg, t, F)
    pencere = 51 if len(tg) > 60 else (len(tg)//2*2-1)
    Lg = savgol_filter(Lg, pencere, 3)
    Fg = savgol_filter(Fg, pencere, 3)
    v  = savgol_filter(Lg, pencere, 3, deriv=1, delta=1.0/FS)
    yank = savgol_filter(Fg, pencere, 3, deriv=1, delta=1.0/FS)
    L0 = np.percentile(Lg, 5)          # taban boy (gerdirme öncesi)
    st = np.atleast_1d(getattr(p, 'spiketimes', np.array([]))).astype(float).ravel()
    fr = np.atleast_1d(getattr(p, 'firing_rate', np.array([]))).astype(float).ravel()
    n = min(max(len(st)-1, 0), len(fr))
    return dict(t=tg, L=Lg-L0, v=v, F=Fg, yank=yank,
                st=st[1:n+1], ifr=fr[:n])           # IFR, aralığı bitiren spike'a atanır

if __name__ == '__main__':
    depo = {}
    for yol in sorted(glob.glob(KOK+'aff[0-9]*_proc.mat')):
        ad = yol.split('/')[-1].replace('_proc.mat','')
        d = sio.loadmat(yol, squeeze_me=True, struct_as_record=False)
        pd = np.atleast_1d(d['proc_data'])
        tt = list(map(str, np.atleast_1d(d['info'].trial_type)))
        denemeler = []
        for i, p in enumerate(pd):
            try:
                r = deneme_isle(p)
            except Exception as e:
                r = None
            if r is not None:
                r['tip'] = tt[i] if i < len(tt) else '?'
                denemeler.append(r)
        depo[ad] = denemeler
        nsp = sum(len(r['st']) for r in denemeler)
        print(f"{ad}: {len(denemeler)} deneme islendi, toplam {nsp} spike")
    pickle.dump(depo, open('spindle_cache.pkl','wb'))
    print('kaydedildi: spindle_cache.pkl')
