# cl_emergent_teslim.py — EMERGENT yuruyus teslim: kilitli config, tam u(t)/r(t),
# hip-knee limit cevrimi, degisken hiz (surus olcekli), sekil + npz.
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from cl_emergent import run
P=dict(yg=-0.010, kc=80.0, cc=4.0, bf=0.3, tau=0.020, bd=[1.5e-3,3e-3,6e-3],
       Ahe=0.16, Ake=0.27, cpf=0.045, cdf=0.06, Apf_st=0.03, Ahf=0.40, Adf=0.06,
       GIb=0.3, GIa=0.10, hip_ext_deg=22, hip_flx_deg=55, Foff=0.05, Fref=2.0, h0=45,k0=-118,a0=5)
L=run(dict(P),Tsim=5.0,dt=1e-4,rec=20,fullrec=True)
names=[str(x) for x in L['names']]; jm={n:i for i,n in enumerate(names)}
td=np.array([t for t,s in L['transitions'] if s=='SWING->STANCE'])
per=np.mean(np.diff(td[-5:])); print("kadans %.2f Hz, periyot %.3f s, gecis %d"%(1/per,per,len(L['transitions'])))
# degisken hiz
SPD={}
for s in [0.85,1.15]:
    SPD[s]=run(dict(P,Ahe=0.16*s,Ahf=0.40*s),Tsim=3.5,dt=1e-4,rec=20)
# npz
np.savez('cl_emergent.npz', t=L['t'],hip=L['hip'],knee=L['knee'],ankle=L['ankle'],state=L['state'],
         Fc=L['Fc'],uHE=L['uHE'],uKE=L['uKE'],uHF=L['uHF'],IaHE=L['IaHE'],IaKE=L['IaKE'],IIHE=L['IIHE'],
         full_t=L['full_t'],full_e=L['full_e'],full_Ia=L['full_Ia'],full_II=L['full_II'],names=L['names'],
         params=str(P))
print("kaydedildi: cl_emergent.npz")
# --- SEKIL ---
fig,ax=plt.subplots(2,3,figsize=(15,8))
t=L['t']; last=t>=t[-1]-4*per
ax[0,0].plot(t[last],np.degrees(L['hip'][last]),label='kalca'); ax[0,0].plot(t[last],np.degrees(L['knee'][last]),label='diz')
ax[0,0].plot(t[last],np.degrees(L['ankle'][last]),label='bilek')
# stance golgeleme
st=L['state'][last]; tt=t[last]
ax[0,0].fill_between(tt,-160,80,where=st>0.5,alpha=0.12,color='gray',step='mid',label='stance')
ax[0,0].set_title('A. Emergent eklem acilari (referans YOK)'); ax[0,0].set_xlabel('s'); ax[0,0].set_ylabel('deg'); ax[0,0].legend(fontsize=7,ncol=2)
# B limit cevrim hip-knee
ax[0,1].plot(np.degrees(L['hip'][last]),np.degrees(L['knee'][last]),lw=0.8)
ax[0,1].set_title('B. Kalca-diz limit cevrimi'); ax[0,1].set_xlabel('kalca (deg)'); ax[0,1].set_ylabel('diz (deg)')
# C u(t) sinerji (bir cevrim, faz)
ph=(t%per)/per*100
for n,lbl,c in [('SM','kalca-ekst','C0'),('IP','kalca-fleks','C1'),('VL','diz-ekst','C2'),('TA','bilek-DF','C3')]:
    j=jm[n]; ue=L['full_e'][:,j]; pht=(L['full_t']%per)/per*100
    m=L['full_t']>=L['full_t'][-1]-4*per
    ax[0,2].plot(pht[m],ue[m],'.',ms=1.5,color=c,label=lbl)
ax[0,2].set_title('C. u(t) kas aktivasyon komutu'); ax[0,2].set_xlabel('% cevrim'); ax[0,2].set_ylabel('u'); ax[0,2].legend(fontsize=7)
# D r(t) afferent (hareketli kaslar: hip ekst SM, diz ekst VL)
m=L['full_t']>=L['full_t'][-1]-4*per; pht=(L['full_t']%per)/per*100
for n,c,ls in [('SM','C0','-'),('VL','C2','-')]:
    j=jm[n]; ax[1,0].plot(pht[m],L['full_Ia'][m,j],'.',ms=1.5,color=c)
ax[1,0].plot([],[],'C0-',label='Ia kalca-ekst(SM)'); ax[1,0].plot([],[],'C2-',label='Ia diz-ekst(VL)')
ax[1,0].set_title('D. r(t) igcik afferenti (hareketli kaslar)'); ax[1,0].set_xlabel('% cevrim'); ax[1,0].set_ylabel('Ia (pps)'); ax[1,0].legend(fontsize=7)
# E state + contact
ax[1,1].plot(t[last],L['Fc'][last],'C3',label='ayak temas kuvveti (N)')
ax2=ax[1,1].twinx(); ax2.plot(t[last],L['state'][last],'C4',lw=0.8,alpha=0.6); ax2.set_ylabel('1=stance',color='C4')
ax[1,1].set_title('E. Duyusal ritim: FSM durumu + gercek temas yuku'); ax[1,1].set_xlabel('s'); ax[1,1].set_ylabel('N',color='C3'); ax[1,1].legend(fontsize=7,loc='upper right')
# F degisken hiz
cols={0.85:'C0',1.0:'C2',1.15:'C3'}
for s,Ls in [(0.85,SPD[0.85]),(1.0,L),(1.15,SPD[1.15])]:
    tds=np.array([tt for tt,ss in Ls['transitions'] if ss=='SWING->STANCE']); ps=np.mean(np.diff(tds[-4:]))
    phs=(Ls['t']%ps)/ps*100; mm=Ls['t']>=Ls['t'][-1]-ps
    ax[1,2].plot(phs[mm],np.degrees(Ls['hip'][mm]),'.',ms=2,color=cols[s],label='surus x%.2f (%.1fHz)'%(s,1/ps))
ax[1,2].set_title('F. Degisken hiz: kalca surusu olcekli'); ax[1,2].set_xlabel('% cevrim'); ax[1,2].set_ylabel('kalca (deg)'); ax[1,2].legend(fontsize=7)
plt.tight_layout(); plt.savefig('cl_emergent.png',dpi=110); print("kaydedildi: cl_emergent.png")
