# cl_sim2.py — vektorlestirilmis, faz-izgarali KAPALI DONGU cekirdegi.
# Duzeltmeler: (1) ileri-besleme EXCITATION = u_ff + tau_act*omega*du_ff/dphi (aktivasyon u_ff'yi izler),
# (2) refleks TUM kaslarda (her kas kestigi DOF'u kararlilastirir; dagitik gerilim refleksi).
import numpy as np
d=np.load('cl_ref.npz',allow_pickle=True)
gs=d['gs']; D7=[str(x) for x in d['D7']]; cnames=[str(x) for x in d['cnames']]; names=[str(x) for x in d['names']]
R0=d['R0']; LMT0=d['LMT0']; LM0=d['LM0']; MLL=d['MLL']; MLPqP=d['MLPqP']; Bbias=d['Bbias']
QREF=d['QREF']; QDREF=d['QDREF']; UFF=d['UFF']; tsl=d['tsl']; lmo=d['lmo']; cosa=d['cosa']; Fmax=d['Fmax']
Li=[int(x) for x in d['Li']]; Qleg=d['Qleg']; TAU_full=d['TAU_full']; T=float(d['T'])
nM=len(names); L=['hip_flx','knee_flx','ankle_flx']; Lc=[cnames.index(c) for c in L]
R0map={c:R0[i] for i,c in enumerate(D7)}
def fL(x): return np.exp(-((x-1)**2)/0.45)
def fV(vn):
    Af,Fl=0.25,1.4; k=2+2/Af; vn=np.clip(vn,-0.9999,None)
    return np.where(vn<=0,(1+vn)/(1-vn/Af),(k*Fl*vn+(Fl-1))/(k*vn+(Fl-1)))

NP=1024; ph=np.arange(NP)/NP
def grid(arr):  # (201,...) -> (NP,...) periyodik faz
    xp=gs/100.0
    if arr.ndim==1: return np.interp(ph,xp,arr,period=1.0)
    out=np.zeros((NP,)+arr.shape[1:])
    for idx in np.ndindex(arr.shape[1:]): out[(slice(None),)+idx]=np.interp(ph,xp,arr[(slice(None),)+idx],period=1.0)
    return out
# faz-izgaralar
Rg=np.stack([grid(R0map[c]) for c in L],axis=1)          # (NP,3,nM) bacak momentkollari
LM0g=grid(LM0); LMT0g=grid(LMT0); COEFg=(LMT0g-tsl)/LM0g  # (NP,nM)
QREFg=grid(QREF); QDREFg=grid(QDREF)                      # (NP,14)
MLLg=grid(MLL); MLPg=grid(MLPqP); BLg=grid(Bbias)[:,Li]; Qlegg=grid(Qleg)  # (NP,3,3),(NP,3),(NP,3),(NP,3)
TAUfg=grid(TAU_full)[:,Li]                                # (NP,3)
UFFg=grid(UFF)                                            # (NP,nM)
qref_leg=QREFg[:,Lc]                                      # (NP,3)
Slm=-Rg*COEFg[:,None,:]                                   # (NP,3,nM) dlm/dq_k
# prescribe D7 uyelerinin vlm katkisi + tam referans vlm
presc=[c for c in D7 if c not in L]
vlm_presc=np.zeros((NP,nM))
for c in presc: vlm_presc += (-grid(R0map[c])*COEFg)*QDREFg[:,cnames.index(c)][:,None]
vlm_ref_full=vlm_presc.copy()
for jj,c in enumerate(L): vlm_ref_full += Slm[:,jj,:]*QDREFg[:,cnames.index(c)][:,None]
# du_ff/dphi: once UFF'yi hafif yumusat (dikis 65%'te turev sicramasini onle), sonra merkezi fark
def smooth_per(A,w=15):
    k=np.ones(w)/w; out=np.zeros_like(A)
    for j in range(A.shape[1]):
        out[:,j]=np.convolve(np.concatenate([A[-w:,j],A[:,j],A[:w,j]]),k,'same')[w:w+A.shape[0]]
    return out
UFFs=smooth_per(UFFg,15)
dUFF=(np.roll(UFFs,-1,0)-np.roll(UFFs,1,0))/(2.0/NP)
# referans kas kuvveti + afferent (r_ref)
def forces(lm,vlm,act):
    lmn=lm/lmo; vn=vlm/(10*lmo); return act*Fmax*fL(lmn)*fV(vn)*cosa
Fref_g=forces(LM0g,vlm_ref_full,UFFg)
dmin_mm=LM0.min(axis=0)*1000
def afferent_arr(lm_mm,vlm_mm):
    dd=np.maximum(0.0,lm_mm-dmin_mm); vc=np.clip(vlm_mm,-20,20)
    Ia=np.maximum(0.0,10.43+26.59*dd+27.08*np.maximum(vc,0.0)**0.532+19.6)
    II=np.maximum(0.0,14.43*dd+21.25*np.sign(vc)*np.abs(vc)**0.358+43.3)
    return Ia,II
Iaref_g,IIref_g=afferent_arr(LM0g*1000,vlm_ref_full*1000)
# trim (reserve) faz-izgarasi: TAU_full_L - kas-torku(u_ff,ref) - Qleg  (durumdan bagimsiz)
TRIMg=TAUfg-np.einsum('pjm,pm->pj',Rg,Fref_g)-Qlegg

def gi(A,fi):  # (NP,...) lineer faz interpolasyonu
    i0=int(fi)%NP; f=fi-int(fi); i1=(i0+1)%NP
    return A[i0]*(1-f)+A[i1]*f

def run(omega,Tsim=None,dt=1e-4,reflex=None,trim=True,seed='ref',pert=None,fullrec=False):
    if Tsim is None: Tsim=8*T
    n=int(Tsim/dt); phi=0.0
    FE=[]; FA=[]; FIa=[]; FII=[]; FT=[]
    qaL=QREFg[0,Lc].copy(); waL=QDREFg[0,Lc].copy(); act=UFFg[0].copy()
    if seed=='off': qaL=qaL+np.array([0.20,-0.20,0.20]); waL[:]=0.0
    tau_act=0.020
    GIa=GII=GIb=0.0
    if reflex: GIa,GII,GIb=reflex.get('GIa',0),reflex.get('GII',0),reflex.get('GIb',0)
    rec=max(1,int(2e-4/dt))
    log={k:[] for k in ['t','phi','hip','knee','ankle','uSol','uTA','uVL','uBFp',
                        'aSol','aTA','aVL','aBFp','IaSol','IaTA','IISol','F_PF','F_TA','dev','esat']}
    for i in range(n):
        t=i*dt; phi=(phi+omega*dt)%1.0; fi=phi*NP
        Rl=gi(Rg,fi); lm0=gi(LM0g,fi); coef=gi(COEFg,fi); slm=gi(Slm,fi)
        qrl=gi(qref_leg,fi); vlmp=gi(vlm_presc,fi)
        lm=lm0+ (slm*(qaL-qrl)[:,None]).sum(0)
        vlm=vlmp + (slm*waL[:,None]).sum(0)
        F=forces(lm,vlm,act)
        Ia,II=afferent_arr(lm*1000,vlm*1000)
        # surucu: excitation ileri-besleme (aktivasyon gecikmesi on-telafisi, sinirli) + refleks
        e=gi(UFFg,fi)+np.clip(tau_act*omega*gi(dUFF,fi),-0.25,0.25)
        if reflex:
            dIa=Ia-gi(Iaref_g,fi); dII=II-gi(IIref_g,fi); dF=(F-gi(Fref_g,fi))/np.maximum(Fmax,1e-9)
            e=e+GIa*dIa+GII*dII-GIb*dF
        e=np.clip(e,0.0,1.0)
        act=act+dt*(e-act)/tau_act
        tmusc=Rl@F
        tapp=tmusc+gi(Qlegg,fi)+(gi(TRIMg,fi) if trim else 0.0)
        if pert and pert[0]<=t<pert[1]: tapp=tapp+np.array(pert[2])
        MLLp=gi(MLLg,fi); bL=gi(BLg,fi); mlp=gi(MLPg,fi)
        qddL=np.linalg.solve(MLLp,tapp-bL-mlp)
        waL=waL+dt*qddL; qaL=qaL+dt*waL
        for jj in range(3):
            lo,hi=qrl[jj]-0.6,qrl[jj]+0.6
            if qaL[jj]<lo: qaL[jj]=lo; waL[jj]=0.0
            if qaL[jj]>hi: qaL[jj]=hi; waL[jj]=0.0
        if i%rec==0:
            jS,jT,jV,jB,jM,jL=[names.index(x) for x in ['Sol','TA','VL','BFp','MG','LG']]
            dev=np.degrees(np.sqrt(np.mean((qaL-qrl)**2)))
            for k,val in [('t',t),('phi',phi),('hip',qaL[0]),('knee',qaL[1]),('ankle',qaL[2]),
                ('uSol',e[jS]),('uTA',e[jT]),('uVL',e[jV]),('uBFp',e[jB]),
                ('aSol',act[jS]),('aTA',act[jT]),('aVL',act[jV]),('aBFp',act[jB]),
                ('IaSol',Ia[jS]),('IaTA',Ia[jT]),('IISol',II[jS]),('F_PF',F[jS]+F[jM]+F[jL]),('F_TA',F[jT]),
                ('dev',dev),('esat',float(np.mean(e>=0.999)))]:
                log[k].append(val)
            if fullrec:
                FE.append(e.copy()); FA.append(act.copy()); FIa.append(Ia.copy()); FII.append(II.copy()); FT.append(t)
    out={k:np.array(v) for k,v in log.items()}
    if fullrec:
        out['full_t']=np.array(FT); out['full_e']=np.array(FE); out['full_a']=np.array(FA)
        out['full_Ia']=np.array(FIa); out['full_II']=np.array(FII); out['names']=np.array(names)
    return out

if __name__=='__main__':
    import sys
    full={'hip':'hip_flx','knee':'knee_flx','ankle':'ankle_flx'}
    def report(tag,Lg):
        h=len(Lg['t'])//2
        msg=[tag]
        for c in ['hip','knee','ankle']:
            ref=np.interp(Lg['phi'],ph,QREFg[:,cnames.index(full[c])])
            dev=np.degrees(np.sqrt(np.mean((Lg[c][h:]-ref[h:])**2)))
            msg.append("%s ROM %.0f/%.0f dev %.1f"%(c[0],np.degrees(Lg[c][h:].min()),np.degrees(Lg[c][h:].max()),dev))
        print(" | ".join(msg))
    print("=== ACIK DONGU (refleks yok) ===")
    report("acik", run(1.0/T,trim=True,reflex=None,Tsim=6*T))
    print("\n=== REFLEKS KAZANC TARAMASI (Gate 3), 6 dongu, kararli-yari dev ===")
    for gia in [0.004,0.01,0.02]:
        for gii in [0.0,0.005]:
            rfx={'GIa':gia,'GII':gii,'GIb':0.0}
            report("GIa=%.3f GII=%.3f"%(gia,gii), run(1.0/T,trim=True,reflex=rfx,Tsim=6*T))
