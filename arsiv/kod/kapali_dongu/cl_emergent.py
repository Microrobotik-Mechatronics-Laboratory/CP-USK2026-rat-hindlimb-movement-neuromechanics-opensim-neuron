# cl_emergent.py — EMERGENT kapali dongu: FSM CPG + anatomik sinerji + gercek temas
#   + YAPISAL refleks (yuk + fazik igcik Ia/II). Referans servo YOK, olculmus GRF izi YOK.
# Denetim (Oturum 7b) sonrasi duzeltmeler:
#  - II artik excitation'a besleniyor; Ia/II FAZIK (EMA-sapmasi). TAM-CEVRIM ortalamasi ~0'dir;
#    ama FAZ-BAZLI ortalamasi ~0 DEGILDIR (orn. VL swing ~0.10). Bu yuzden "sabitle taklit
#    edilemez" gerekcesi degil, G9 su testi yapar: faz-ortalamasini meanff taklit eder, geriye
#    kalan FAZ-ICI zamanlama zorunlu mu (bkz. cl_selfcheck G9). GIa/GII gercek kazanc.
#  - hiz doyumu VCAP=45 mm/s (tipik lif hizi ~34; eski 20 surekli satureydi). Fit araligi
#    disi ekstrapolasyon; yon guvenilir, buyukluk degil.
#  - GMi HIP_FLX'ten cikarildi (ters isaretli hip momentkolu). Olu kod (DISTAL/STANCE_SYN/
#    KNE_FLX/Foff/SPINDLE) atildi.
#  - run(fb=...) modu: 'live' canli geri besleme, 'off' kapali, 'meanff' geri beslemeyi
#    faz-ortalamasi SABITle degistirir (G9 yapisal test icin).
# Denetim (Oturum 7c) sonrasi SAYISAL duzeltme:
#  - Bilek DOF eylemsizligi cok kucuk (M[ankle,ankle]~1.1e-7, hip'in ~1/120'si). Acik Euler
#    dt=1e-4'te bu stiff DOF'ta KARARSIZ: bilek salinip -35 grid limitine cakiliyordu. Bu bir
#    KONTROL hatasi DEGIL, entegrasyon artefaktiydi (cdf/cpf ile duzelmez). dt=2e-5'te sonuc
#    yakinsak (dt=1e-5 ile birebir ayni); 5e-5/3e-5 hala artefakt. Varsayilan dt 2e-5 yapildi.
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # kod/yollar.py icin
from yollar import VERI_CL
g=np.load(VERI_CL/'cl_grid3d.npz',allow_pickle=True)   # modul seviyesinde: import aninda gerekir
HIP=g['HIP']; KNE=g['KNE']; ANK=g['ANK']; R=g['R']; LM=g['LM']; LMT=g['LMT']
MLEG=g['MLEG']; BG=g['BG']; FTOE=g['FTOE']; FHEEL=g['FHEEL']
names=[str(x) for x in g['names']]; nM=len(names); tsl=g['tsl']; lmo=g['lmo']; cosa=g['cosa']; Fmax=g['Fmax']
def grad3(A):
    gh=np.gradient(A,HIP,axis=0); gk=np.gradient(A,KNE,axis=1); ga=np.gradient(A,ANK,axis=2)
    return np.stack([gh,gk,ga],axis=-1)
JTOE=grad3(FTOE); JHEEL=grad3(FHEEL)
jm={n:i for i,n in enumerate(names)}
def idx(nl): return [jm[n] for n in nl if n in jm]
# --- anatomik sinerji gruplari (moment kolu isaretinden; grid dogrulamasi) ---
HIP_EXT=idx(['SM','AB','AM']);   HIP_FLX=idx(['IP','TFL','GMa','GMe'])  # GMi cikti: hip momentkolu ters
KNE_EXT=idx(['VL','VI','VM'])
ANK_PF =idx(['Sol','MG','LG']);  ANK_DF =idx(['TA','EDL'])
VCAP=45.0                        # lif hizi doyumu (mm/s); tipik ~34, eski 20 satureydi
def fL(x): return np.exp(-((x-1)**2)/0.45)
def fV(vn):
    Af,Fl=0.25,1.4; k=2+2/Af; vn=np.clip(vn,-0.9999,None)
    return np.where(vn<=0,(1+vn)/(1-vn/Af),(k*Fl*vn+(Fl-1))/(k*vn+(Fl-1)))
def trilin(A,h,k,a):
    ih=np.clip(np.searchsorted(HIP,h)-1,0,len(HIP)-2); fk=np.clip(np.searchsorted(KNE,k)-1,0,len(KNE)-2); fa=np.clip(np.searchsorted(ANK,a)-1,0,len(ANK)-2)
    th=(h-HIP[ih])/(HIP[ih+1]-HIP[ih]); tk=(k-KNE[fk])/(KNE[fk+1]-KNE[fk]); ta=(a-ANK[fa])/(ANK[fa+1]-ANK[fa])
    th=min(max(th,0),1); tk=min(max(tk,0),1); ta=min(max(ta,0),1)
    c=A[ih:ih+2,fk:fk+2,fa:fa+2]
    w=np.array([[[(1-th)*(1-tk)*(1-ta),(1-th)*(1-tk)*ta],[(1-th)*tk*(1-ta),(1-th)*tk*ta]],
                [[th*(1-tk)*(1-ta),th*(1-tk)*ta],[th*tk*(1-ta),th*tk*ta]]])
    return np.tensordot(w,c,axes=([0,1,2],[0,1,2]))
dmin_mm=LM.reshape(-1,nM).min(0)*1000
def afferent(lm_mm,vlm_mm):   # Ia (Blum), II (Vincent); katsayilar 46_/02 kayitlarinda dogrulandi
    dd=np.maximum(0.0,lm_mm-dmin_mm); vc=np.clip(vlm_mm,-VCAP,VCAP)
    Ia=np.maximum(0.0,10.43+26.59*dd+27.08*np.maximum(vc,0.0)**0.532+19.6)
    II=np.maximum(0.0,14.43*dd+21.25*np.sign(vc)*np.abs(vc)**0.358+43.3)
    return Ia,II

def run(P, Tsim=4.0, dt=2e-5, rec=20, pert=None, fullrec=False, fb='live', fb_st=None, fb_sw=None, reclog=False):
    # dt=2e-5 ZORUNLU (yakinsak): bilek DOF stiff, dt>2e-5'te acik Euler kararsiz (bkz. bas yorum).
    yg=P['yg']; kc=P['kc']; cc=P['cc']; bf=P['bf']; GIb=P['GIb']; GIa=P['GIa']; GII=P.get('GII',0.0); tau=P['tau']
    aema=dt/max(P.get('tau_ema',0.12),dt)          # igcik EMA hizi (fazik referans)
    hip_ext=np.deg2rad(P['hip_ext_deg']); hip_flx=np.deg2rad(P['hip_flx_deg'])
    h=np.deg2rad(P['h0']); k=np.deg2rad(P['k0']); a=np.deg2rad(P['a0'])
    wh=wk=wa=0.0; act=np.full(nM,0.02); state='STANCE'; Fc=0.0
    Ia_ema=None; II_ema=None
    FE=[];FA=[];FIa=[];FII=[];FT=[]; RFL=[];RST=[]   # refl/state kaydi (G9 icin)
    log={x:[] for x in ['t','state','hip','knee','ankle','Fc','uHE','uKE','uPF','uHF','uTA','IaPF','IaHE','IaKE','IIHE','reflHE','trans']}
    trans=[]
    for i in range(int(Tsim/dt)):
        t=i*dt
        r=trilin(R,h,k,a); lmt=trilin(LMT,h,k,a); lm=trilin(LM,h,k,a)
        coef=(lmt-tsl)/lm; qd=np.array([wh,wk,wa]); vlm=-(r*coef).T@qd
        Ia,II=afferent(lm*1000, vlm*1000)
        if Ia_ema is None: Ia_ema=Ia.copy(); II_ema=II.copy()
        toe=trilin(FTOE,h,k,a); Jt=trilin(JTOE,h,k,a)
        vy=Jt[1]@qd; vx=Jt[0]@qd; pen=yg-toe[1]
        Fy=max(0.0, kc*pen - cc*vy) if pen>0 else 0.0
        Fx=-bf*vx if Fy>0 else 0.0; Fc=Fy; tau_c=Jt[0]*Fx+Jt[1]*Fy
        # FSM (faz degiskeni = kalca acisi)
        if state=='STANCE' and h<=hip_ext: state='SWING'; trans.append((t,'STANCE->SWING'))
        elif state=='SWING' and h>=hip_flx: state='STANCE'; trans.append((t,'SWING->STANCE'))
        # --- MERKEZI (feedforward) surus ---
        e=np.full(nM,0.0)
        for m in KNE_EXT: e[m]=P['Ake']
        for m in ANK_PF:  e[m]=P['cpf']
        for m in ANK_DF:  e[m]=P['cdf']
        if state=='STANCE':
            for m in HIP_EXT: e[m]=P['Ahe']
            for m in ANK_PF:  e[m]+=P['Apf_st']
        else:
            for m in HIP_FLX: e[m]=P['Ahf']
            for m in ANK_DF:  e[m]+=P['Adf']
        # --- GERI BESLEME r(t): yuk (stance, tonik-Pearson) + FAZIK igcik Ia/II (EMA-sapmasi; faz-ort meanff'te taklit edilir) ---
        refl=np.zeros(nM)
        if state=='STANCE':
            load=Fy/max(P['Fref'],1e-6)
            for m in HIP_EXT: refl[m]+=GIb*load
            for m in KNE_EXT: refl[m]+=GIb*load
        refl=refl + GIa*(Ia-Ia_ema)/100.0 + GII*(II-II_ema)/100.0    # fazik: gerilim/uzunluk sapmasi
        Ia_ema+=aema*(Ia-Ia_ema); II_ema+=aema*(II-II_ema)
        if   fb=='live':   e=e+refl
        elif fb=='meanff': e=e+(fb_st if state=='STANCE' else fb_sw)   # geri beslemeyi faz-ort SABITle degistir
        # fb=='off': hicbir sey ekleme
        e=np.clip(e,0,1)
        act=act+dt*(e-act)/tau
        F=act*Fmax*fL(lm/lmo)*fV(vlm/(10*lmo))*cosa
        tau_m=r@F; bg=trilin(BG,h,k,a); M=trilin(MLEG,h,k,a)
        tap=tau_m+tau_c-bg-np.asarray(P['bd'])*qd
        if pert and pert[0]<=t<pert[1]: tap=tap+np.array(pert[2])
        qdd=np.linalg.solve(M, tap)
        wh+=dt*qdd[0]; wk+=dt*qdd[1]; wa+=dt*qdd[2]; h+=dt*wh; k+=dt*wk; a+=dt*wa
        h=min(max(h,HIP[0]),HIP[-1]); k=min(max(k,KNE[0]),KNE[-1]); a=min(max(a,ANK[0]),ANK[-1])
        if h in(HIP[0],HIP[-1]): wh=0.0
        if k in(KNE[0],KNE[-1]): wk=0.0
        if a in(ANK[0],ANK[-1]): wa=0.0
        if reclog: RFL.append(refl.copy()); RST.append(1 if state=='STANCE' else 0)
        if i%rec==0:
            for x,v in [('t',t),('state',1 if state=='STANCE' else 0),('hip',h),('knee',k),('ankle',a),
                ('Fc',Fc),('uHE',e[HIP_EXT[0]]),('uKE',e[KNE_EXT[0]]),('uPF',e[jm['Sol']]),
                ('uHF',e[HIP_FLX[0]]),('uTA',e[jm['TA']]),('IaPF',Ia[jm['Sol']]),
                ('IaHE',Ia[HIP_EXT[0]]),('IaKE',Ia[KNE_EXT[0]]),('IIHE',II[HIP_EXT[0]]),('reflHE',refl[HIP_EXT[0]]),('trans',len(trans))]:
                log[x].append(v)
            if fullrec: FE.append(e.copy());FA.append(act.copy());FIa.append(Ia.copy());FII.append(II.copy());FT.append(t)
    out={x:np.array(v) for x,v in log.items()}; out['transitions']=trans
    if reclog:
        RFL=np.array(RFL); RST=np.array(RST)
        out['refl_stance_mean']=RFL[RST==1].mean(0) if (RST==1).any() else np.zeros(nM)
        out['refl_swing_mean'] =RFL[RST==0].mean(0) if (RST==0).any() else np.zeros(nM)
    if fullrec:
        out['full_t']=np.array(FT);out['full_e']=np.array(FE);out['full_a']=np.array(FA)
        out['full_Ia']=np.array(FIa);out['full_II']=np.array(FII);out['names']=np.array(names)
    return out
