# spindle_fit.py — Kademe 2 fit (47_ B26 ADIM 2-3)
# Uc model ayni sinavda:
#   v2 TABAN : Ia = clip(10.033·d + 64.60·|v|^0.2729, 0)   [Vincent uc-nokta fiti, sabit]
#   K-model  : f = clip(b + kL·d + kV·max(v,0)^p, 0)        [kinematik, egrilere yeniden fit]
#   F-model  : f = clip(b + kF·F + kY·max(yank,0), 0)       [kuvvet+yank, Blum bicimi]
# Bolme: afferent basina cift-indisli denemeler egitim, tek-indisliler sinama;
#        aff502'nin 'pseudorand' denemeleri HICBIR zaman egitime girmez (salt sinama).
# Olcum: sinama spike'larinda RMSE (Hz) ve havuzlanmis R^2; ozellik sinavi ucgen serisinde.
import numpy as np, pickle, json
from scipy.optimize import least_squares
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # kod/yollar.py icin
from yollar import VERI

repo = pickle.load(open(VERI/'spindle_cache.pkl','rb'))   # spindle_onisle.py uretir

def v2_tahmin(r):
    return np.clip(10.033*r['L'] + 64.60*np.abs(r['v'])**0.2729, 0, None)

def k_tahmin(r, prm):
    b, kL, kV, p = prm
    return np.clip(b + kL*r['L'] + kV*np.maximum(r['v'],0)**p, 0, None)

def f_tahmin(r, prm):
    b, kF, kY = prm
    return np.clip(b + kF*r['F'] + kY*np.maximum(r['yank'],0), 0, None)

def spike_ornekle(r, f):
    return np.interp(r['st'], r['t'], f)

def kalinti(prm, denemeler, model):
    parcalar = []
    for r in denemeler:
        if len(r['st']) == 0: continue
        f = model(r, prm)
        parcalar.append(spike_ornekle(r, f) - r['ifr'])
    return np.concatenate(parcalar) if parcalar else np.array([0.0])

def metrikler(denemeler, tahmin_fn):
    olcum, model = [], []
    for r in denemeler:
        if len(r['st']) == 0: continue
        model.append(spike_ornekle(r, tahmin_fn(r)))
        olcum.append(r['ifr'])
    if not olcum: return dict(rmse=np.nan, r2=np.nan, n=0)
    o = np.concatenate(olcum); m = np.concatenate(model)
    rmse = float(np.sqrt(np.mean((m-o)**2)))
    r2 = float(1 - np.sum((m-o)**2)/np.sum((o-o.mean())**2))
    return dict(rmse=round(rmse,1), r2=round(r2,3), n=len(o))

sonuc = {}
for ad, denemeler in repo.items():
    spikeli = [r for r in denemeler if len(r['st'])>0]
    pseudo = [r for r in spikeli if r['tip']=='pseudorand']
    kalan = [r for r in spikeli if r['tip']!='pseudorand']
    egit = kalan[0::2]; sina = kalan[1::2] + pseudo
    # K-model fiti
    kfit = least_squares(kalinti, x0=[20.0, 10.0, 60.0, 0.3],
                         bounds=([0,-50,0,0.05],[200,200,500,1.0]),
                         args=(egit, k_tahmin), max_nfev=200)
    # F-model fiti
    F95 = np.percentile(np.concatenate([r['F'] for r in egit]), 95)
    ffit = least_squares(kalinti, x0=[10.0, 100.0, 5.0],
                         bounds=([0,0,0],[200,2000,200]),
                         args=(egit, f_tahmin), max_nfev=200)
    sonuc[ad] = dict(
        n_egit=len(egit), n_sina=len(sina), n_pseudo=len(pseudo), F95=round(float(F95),3),
        v2   = metrikler(sina, v2_tahmin),
        K    = metrikler(sina, lambda r: k_tahmin(r, kfit.x)),
        Fmod = metrikler(sina, lambda r: f_tahmin(r, ffit.x)),
        K_prm = [round(float(x),3) for x in kfit.x],
        F_prm = [round(float(x),3) for x in ffit.x],
    )
    if pseudo:
        sonuc[ad]['v2_pseudo'] = metrikler(pseudo, v2_tahmin)
        sonuc[ad]['K_pseudo'] = metrikler(pseudo, lambda r: k_tahmin(r, kfit.x))
        sonuc[ad]['F_pseudo'] = metrikler(pseudo, lambda r: f_tahmin(r, ffit.x))
    s = sonuc[ad]
    print(f"{ad}: sinama RMSE(Hz) v2={s['v2']['rmse']} K={s['K']['rmse']} F={s['Fmod']['rmse']} | "
          f"R2 v2={s['v2']['r2']} K={s['K']['r2']} F={s['Fmod']['r2']} | K_prm={s['K_prm']} F_prm={s['F_prm']}")

json.dump(sonuc, open(VERI/'spindle_fit_sonuc.json','w'), indent=1)
print('kaydedildi: spindle_fit_sonuc.json')
