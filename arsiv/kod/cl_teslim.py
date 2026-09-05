# cl_teslim.py — Oturum 7 NIHAI TESLIM. Arka bacak kapali-dongu yuruyus:
# tum kaslarin u(t) ve r(t)'si + eklem acilari, 3 hizda; bozucu on/off; ozet sekil.
import numpy as np, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from cl_sim2 import run, T, ph, QREFg, cnames, names
full={'hip':'hip_flx','knee':'knee_flx','ankle':'ankle_flx'}
BG={'GIa':0.004,'GII':0.005,'GIb':0.0}
def refc(Lg,c): return np.interp(Lg['phi'],ph,QREFg[:,cnames.index(full[c])])

# --- 3 hiz, tam kayit ---
SP={'yavas':0.7/T,'nominal':1.0/T,'hizli':1.4/T}
DATA={}
for lab,om in SP.items():
    DATA[lab]=run(om,trim=True,reflex=BG,Tsim=7*T,fullrec=True)
# bozucu on/off (nominal)
pt=(3*T,3*T+0.03,[0.0,0.0,0.004])
POFF=run(1.0/T,trim=True,reflex=None,pert=pt,Tsim=6*T)
PON =run(1.0/T,trim=True,reflex=BG,pert=pt,Tsim=6*T)
# acik dongu (refleks yok) divergence
OPEN=run(1.0/T,trim=True,reflex=None,Tsim=6*T)

# --- npz kaydet ---
sav={}
for lab in SP:
    L=DATA[lab]
    for c in ['hip','knee','ankle']: sav['%s_%s'%(lab,c)]=L[c]; sav['%s_%s_ref'%(lab,c)]=refc(L,c)
    sav['%s_t'%lab]=L['t']; sav['%s_phi'%lab]=L['phi']
    sav['%s_full_t'%lab]=L['full_t']; sav['%s_u'%lab]=L['full_e']; sav['%s_a'%lab]=L['full_a']
    sav['%s_Ia'%lab]=L['full_Ia']; sav['%s_II'%lab]=L['full_II']
sav['names']=np.array(names); sav['T']=T; sav['gains']=json.dumps(BG)
sav['pert_off_t']=POFF['t']; sav['pert_off_ankle']=POFF['ankle']; sav['pert_off_ankle_ref']=refc(POFF,'ankle')
sav['pert_on_t']=PON['t']; sav['pert_on_ankle']=PON['ankle']; sav['pert_on_ankle_ref']=refc(PON,'ankle')
np.savez('cl_kapali_dongu.npz', **sav)
print("kaydedildi: cl_kapali_dongu.npz  (3 hiz tam u(t)/r(t) + bozucu)")

# --- SEKIL: 6 panel ---
fig,ax=plt.subplots(2,3,figsize=(15,8))
L=DATA['nominal']; h=len(L['t'])//2
# A: eklem izleme (son 2 cevrim, % cevrim)
last=L['t']>=L['t'][-1]-2*T
for c,col in zip(['hip','knee','ankle'],['C0','C1','C2']):
    ax[0,0].plot((L['t'][last]%T)/T*100, np.degrees(L[c][last]),'.',ms=1,color=col,label=c)
    ax[0,0].plot((L['t'][last]%T)/T*100, np.degrees(refc(L,c)[last]),'k--',lw=0.6,alpha=0.5)
ax[0,0].set_title('A. Eklem izleme (nokta=kapali dongu, kesik=referans)'); ax[0,0].set_xlabel('% cevrim'); ax[0,0].set_ylabel('aci (deg)'); ax[0,0].legend(fontsize=8)
# B: bilek limit-cevrimi + bozuk baslangictan yakinsama
Loff=run(1.0/T,trim=True,reflex=BG,seed='off',Tsim=6*T)
ax[0,1].plot(np.degrees(Loff['ankle']),np.degrees(np.gradient(Loff['ankle'],Loff['t'])),'C3',lw=0.4,alpha=0.7,label='bozuk baslangic')
ax[0,1].plot(np.degrees(L['ankle'][h:]),np.degrees(np.gradient(L['ankle'],L['t'])[h:]),'C2',lw=1.2,label='limit cevrim')
ax[0,1].set_title('B. Bilek faz-portresi (limit cevrime yakinsama)'); ax[0,1].set_xlabel('bilek aci (deg)'); ax[0,1].set_ylabel('aci hizi (deg/s)'); ax[0,1].legend(fontsize=8)
# C: u(t) excitation
g100=(L['t'][last]%T)/T*100
for n,col in zip(['Sol','TA','VL','BFp'],['C2','C3','C0','C4']):
    ax[0,2].plot(g100, L['u'+n][last],'.',ms=1,color=col,label=n)
ax[0,2].set_title('C. u(t) sinirsel surus (excitation)'); ax[0,2].set_xlabel('% cevrim'); ax[0,2].set_ylabel('u'); ax[0,2].legend(fontsize=8)
# D: r(t) afferent
for n,col,ls in [('IaSol','C2','-'),('IaTA','C3','-'),('IISol','C2','--')]:
    ax[1,0].plot(g100, L[n][last],'.',ms=1,color=col)
ax[1,0].plot([],[],'C2-',label='Ia Sol'); ax[1,0].plot([],[],'C3-',label='Ia TA'); ax[1,0].plot([],[],'C2--',label='II Sol')
ax[1,0].set_title('D. r(t) igcik afferenti'); ax[1,0].set_xlabel('% cevrim'); ax[1,0].set_ylabel('pps'); ax[1,0].legend(fontsize=8)
# E: refleks on/off (dev vs zaman)
ax[1,1].plot(OPEN['t']/T, OPEN['dev'],'C3',label='refleks KAPALI (iraksar)')
ax[1,1].plot(L['t']/T, L['dev'],'C2',label='refleks ACIK (izler)')
ax[1,1].axvspan(3,3.08,color='gray',alpha=0.3)
ax[1,1].plot(PON['t']/T,PON['dev'],'C0',lw=0.8,label='bozucu+refleks (toparlar)')
ax[1,1].set_title('E. Refleks gerekli + bozucu reddi'); ax[1,1].set_xlabel('cevrim'); ax[1,1].set_ylabel('RMS sapma (deg)'); ax[1,1].legend(fontsize=8); ax[1,1].set_ylim(0,40)
# F: degisken hiz bilek izi (CPG fazina gore -> hizdan bagimsiz temiz tek cevrim)
for lab,col in zip(['yavas','nominal','hizli'],['C0','C2','C3']):
    Ls=DATA[lab]; per=1.0/SP[lab]; last2=Ls['t']>=Ls['t'][-1]-per
    ax[1,2].plot(Ls['phi'][last2]*100, np.degrees(Ls['ankle'][last2]),'.',ms=2,color=col,label='%s (%.2fs)'%(lab,per))
ax[1,2].set_title('F. Degisken hiz — bilek (tek oruntu, omega olcekli)'); ax[1,2].set_xlabel('% cevrim (CPG faz)'); ax[1,2].set_ylabel('bilek aci (deg)'); ax[1,2].legend(fontsize=8)
plt.tight_layout(); plt.savefig('cl_kapali_dongu.png',dpi=110)
print("kaydedildi: cl_kapali_dongu.png")
