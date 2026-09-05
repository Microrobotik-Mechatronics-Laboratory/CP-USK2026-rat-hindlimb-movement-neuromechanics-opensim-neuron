# cl_teslim_9of9.py — 9/9 kapiyi gecen en iyi P (cl_best_9of9.json) icin TESLIM sekli.
# Ayni koşu: live (reclog) + meanff (G9 yapisal kanit). Zaman serileri + faz portresi + live-vs-meanff.
# Cikti: sekiller/cl_teslim_9of9.png + veri/kapali_dongu/cl_teslim_9of9.npz + stdout ozet (ureten: bu dosya).
import json, numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # kod/yollar.py icin
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from cl_emergent import run
from yollar import VERI_CL, SEKILLER

P = json.load(open(VERI_CL/'cl_best_9of9.json'))['P']
TS = 6.0
print("live kosuluyor (Tsim=%.0f, dt=2e-5)..." % TS)
L = run(dict(P), Tsim=TS, dt=2e-5, rec=20, reclog=True)
print("meanff kosuluyor (G9 yapisal test)...")
M = run(dict(P), Tsim=TS, dt=2e-5, rec=20, fb='meanff',
        fb_st=L['refl_stance_mean'], fb_sw=L['refl_swing_mean'])

d = np.degrees
t = L['t']; h2 = len(t)//2
tdL = [x for x,s in L['transitions'] if s=='SWING->STANCE']
tdM = [x for x,s in M['transitions'] if s=='SWING->STANCE']
st = L['state'][h2:] > 0.5
print("OZET (son yari, ayni koşu):")
print("  live: gecis %d | hip %.0f..%.0f knee %.0f..%.0f ankle %.0f..%.0f | stance %.2f" % (
    len(L['transitions']), d(L['hip'][h2:]).min(), d(L['hip'][h2:]).max(),
    d(L['knee'][h2:]).min(), d(L['knee'][h2:]).max(),
    d(L['ankle'][h2:]).min(), d(L['ankle'][h2:]).max(), float(L['state'][h2:].mean())))
print("  live: Fc stance %.3fN swing %.3fN | kadans %.2fHz" % (
    float(L['Fc'][h2:][st].mean()), float(L['Fc'][h2:][~st].mean()),
    1.0/np.mean(np.diff(tdL[-4:])) if len(tdL)>4 else 0))
print("  meanff: gecis %d | ankle %.0f..%.0f (son yari)" % (
    len(M['transitions']), d(M['ankle'][len(M['t'])//2:]).min(), d(M['ankle'][len(M['t'])//2:]).max()))

fig, ax = plt.subplots(6, 1, figsize=(11, 14), sharex=False)
W = (t >= 2.0) & (t <= 5.0)   # 3 s'lik temsili pencere

# stance golgeleme yardimcisi
def shade(a, tt, ss):
    df = np.diff(ss.astype(int)); on = tt[1:][df==1]; off = tt[1:][df==-1]
    if ss[0] == 1: on = np.r_[tt[0], on]
    if ss[-1] == 1: off = np.r_[off, tt[-1]]
    for o, f in zip(on, off): a.axvspan(o, f, color='0.85', zorder=0)

shade(ax[0], t[W], L['state'][W])
ax[0].plot(t[W], d(L['hip'][W]), label='kalca'); ax[0].plot(t[W], d(L['knee'][W]), label='diz')
ax[0].plot(t[W], d(L['ankle'][W]), label='bilek')
ax[0].set_ylabel('aci (deg)'); ax[0].legend(loc='center right', fontsize=8)
ax[0].set_title('Emergent kapali dongu, 9/9 kapi (cl_best_9of9.json) — golge=stance')

shade(ax[1], t[W], L['state'][W])
ax[1].plot(t[W], L['Fc'][W], 'k'); ax[1].set_ylabel('temas Fc (N)')

shade(ax[2], t[W], L['state'][W])
for k, lab in [('uHE','u kalca-ekst (SM)'), ('uHF','u kalca-flex (IP)'), ('uKE','u diz-ekst (VL)'),
               ('uPF','u Sol'), ('uTA','u TA')]:
    ax[2].plot(t[W], L[k][W], label=lab, lw=0.9)
ax[2].set_ylabel('u(t)'); ax[2].legend(loc='center right', fontsize=7, ncol=2)

shade(ax[3], t[W], L['state'][W])
ax[3].plot(t[W], L['IaHE'][W], label='Ia SM (pps)')
ax[3].plot(t[W], L['IIHE'][W], label='II SM (pps)')
a3 = ax[3].twinx(); a3.plot(t[W], L['reflHE'][W], 'r', lw=0.8, label='refl SM')
a3.set_ylabel('refleks katkisi', color='r')
ax[3].set_ylabel('r(t) afferent'); ax[3].legend(loc='upper right', fontsize=8)

ax[4].plot(d(L['hip'][h2:]), d(L['knee'][h2:]), lw=0.6)
ax[4].set_xlabel('kalca (deg)'); ax[4].set_ylabel('diz (deg)')
ax[4].set_title('faz portresi (son yari) — kapali halka = limit-cevrim', fontsize=9)

ax[5].plot(t, d(L['ankle']), label='bilek LIVE', lw=0.9)
ax[5].plot(M['t'], d(M['ankle']), label='bilek MEANFF (geri besleme faz-ort sabit)', lw=0.9)
ax[5].axhline(-35, color='r', ls='--', lw=0.7); ax[5].axhline(35, color='r', ls='--', lw=0.7)
ax[5].set_xlabel('t (s)'); ax[5].set_ylabel('bilek (deg)')
ax[5].set_title('G9 yapisal kanit: live limitten uzak; meanff limite cakiliyor (gecis %d vs %d)'
                % (len(L['transitions']), len(M['transitions'])), fontsize=9)
ax[5].legend(loc='center right', fontsize=8)

plt.tight_layout()
plt.savefig(SEKILLER/'cl_teslim_9of9.png', dpi=140)
np.savez_compressed(VERI_CL/'cl_teslim_9of9.npz',
    **{k: v for k, v in L.items() if isinstance(v, np.ndarray)},
    meanff_t=M['t'], meanff_ankle=M['ankle'], meanff_state=M['state'],
    n_trans_live=len(L['transitions']), n_trans_meanff=len(M['transitions']))
print("kaydedildi: cl_teslim_9of9.png / .npz")
