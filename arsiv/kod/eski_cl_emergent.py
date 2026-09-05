# cl_emergent.py — EMERGENT kapali dongu: sonlu-durum CPG + anatomik sinerji + gercek
# ayak-yer temasi + gerilim/yuk refleksi. Referans servo YOK, olculmus GRF izi YOK.
# Ritim bacagin durumundan dogar; yuk temastan dogar; kinematik kaslardan cikar.
import numpy as np
g=np.load('cl_grid3d.npz',allow_pickle=True)
HIP=g['HIP']; KNE=g['KNE']; ANK=g['ANK']; R=g['R']; LM=g['LM']; LMT=g['LMT']
MLEG=g['MLEG']; BG=g['BG']; FTOE=g['FTOE']; FHEEL=g['FHEEL']
names=[str(x) for x in g['names']]; nM=len(names); tsl=g['tsl']; lmo=g['lmo']; cosa=g['cosa']; Fmax=g['Fmax']
# temas Jacobian'lari (izgara gradyani) ayak istasyonu (x,y) / (hip,knee,ankle)
def grad3(A):  # A (nH,nK,nA,2) -> (nH,nK,nA,2,3)
    gh=np.gradient(A,HIP,axis=0); gk=np.gradient(A,KNE,axis=1); ga=np.gradient(A,ANK,axis=2)
    return np.stack([gh,gk,ga],axis=-1)
JTOE=grad3(FTOE); JHEEL=grad3(FHEEL)
jm={n:i for i,n in enumerate(names)}
def idx(nl): return [jm[n] for n in nl if n in jm]
# --- anatomik sinerji gruplari ---
# stance hip ekstansoru: DIZ momentkolu KUCUK olanlar (SM -3.9, AB, AM) -> dizi cokertmez
HIP_EXT=idx(['SM','AB','AM']);       HIP_FLX=idx(['IP','TFL','GMa','GMe','GMi'])
KNE_EXT=idx(['VL','VI','VM']);       KNE_FLX=idx(['BFp','STp'])  # monoartikuler (RF disari: kalcayi karistirir)
ANK_PF =idx(['Sol','MG','LG']);      ANK_DF =idx(['TA','EDL'])
STANCE_SYN=sorted(set(HIP_EXT+KNE_EXT+ANK_PF))
DISTAL=sorted(set(KNE_EXT+KNE_FLX+ANK_PF+ANK_DF))   # II uzunluk refleksiyle kararlilastirilir
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
def afferent(lm_mm,vlm_mm):
    d=np.maximum(0.0,lm_mm-dmin_mm); vc=np.clip(vlm_mm,-20,20)
    Ia=np.maximum(0.0,10.43+26.59*d+27.08*np.maximum(vc,0.0)**0.532+19.6)
    II=np.maximum(0.0,14.43*d+21.25*np.sign(vc)*np.abs(vc)**0.358+43.3)
    return Ia,II

def run(P, Tsim=4.0, dt=1e-4, rec=20, pert=None, fullrec=False):
    yg=P['yg']; kc=P['kc']; cc=P['cc']; bf=P['bf']
    FE=[];FA=[];FIa=[];FII=[];FT=[]
    GIb=P['GIb']; GIa=P['GIa']; tau=P['tau']
    hip_ext=np.deg2rad(P['hip_ext_deg']); hip_flx=np.deg2rad(P['hip_flx_deg']); Foff=P['Foff']
    # baslangic: stance-benzeri, hafif fleksiyon
    h=np.deg2rad(P['h0']); k=np.deg2rad(P['k0']); a=np.deg2rad(P['a0'])
    wh=wk=wa=0.0; act=np.full(nM,0.02); state='STANCE'; Fc=0.0
    log={x:[] for x in ['t','state','hip','knee','ankle','Fc','uHE','uKE','uPF','uHF','uTA','IaPF','trans']}
    trans=[]
    for i in range(int(Tsim/dt)):
        t=i*dt
        r=trilin(R,h,k,a); lmt=trilin(LMT,h,k,a); lm=trilin(LM,h,k,a)
        coef=(lmt-tsl)/lm
        qd=np.array([wh,wk,wa])
        vlm=-(r*coef).T@qd            # (nM,)
        Ia,II=afferent(lm*1000, vlm*1000)
        # temas: parmak
        toe=trilin(FTOE,h,k,a); Jt=trilin(JTOE,h,k,a)  # (2,),(2,3)
        vy=Jt[1]@qd; vx=Jt[0]@qd
        pen=yg-toe[1]
        Fy=max(0.0, kc*pen - cc*vy) if pen>0 else 0.0
        Fx=-bf*vx if Fy>0 else 0.0
        Fc=Fy
        tau_c=Jt[0]*Fx+Jt[1]*Fy       # (3,) contact genellestirilmis kuvvet
        # --- FSM: faz degiskeni KALCA acisi (kedi/rat lokomosyonu; Grillner/Prochazka) ---
        if state=='STANCE' and h<=hip_ext:
            state='SWING'; trans.append((t,'STANCE->SWING'))
        elif state=='SWING' and h>=hip_flx:
            state='STANCE'; trans.append((t,'SWING->STANCE'))
        # --- sinerji surus: KALCA+DIZ emergent; bilek tonik ko-kontraksiyon (digitigrad tutus) ---
        e=np.full(nM,0.0)
        for m in KNE_EXT: e[m]=P['Ake']               # POSTURAL: quad dizi ~-115'te tutar (iki faz)
        for m in ANK_PF:  e[m]=P['cpf']               # bilek plantarfleksor tonusu (toe-down)
        for m in ANK_DF:  e[m]=P['cdf']
        if state=='STANCE':
            for m in HIP_EXT: e[m]=P['Ahe']           # kalcayi geri suprur (propulsiyon)
            for m in ANK_PF:  e[m]+=P['Apf_st']       # itis
            load=Fy/max(P['Fref'],1e-6)               # yuk refleksi (pozitif kuvvet, kendini sinirlar)
            for m in HIP_EXT: e[m]+=GIb*load
            for m in KNE_EXT: e[m]+=GIb*load
        else:
            for m in HIP_FLX: e[m]=P['Ahf']           # kalcayi one savurur (protraksiyon)
            for m in ANK_DF:  e[m]+=P['Adf']          # parmak temizligi
        e=e+GIa*Ia*0.001                                # gerilim refleksi (homonim Ia)
        e=np.clip(e,0,1)
        act=act+dt*(e-act)/tau
        F=act*Fmax*fL(lm/lmo)*fV(vlm/(10*lmo))*cosa
        tau_m=r@F                      # (3,) kas torku
        bg=trilin(BG,h,k,a)
        M=trilin(MLEG,h,k,a)
        tap=tau_m+tau_c-bg-np.asarray(P['bd'])*qd
        if pert and pert[0]<=t<pert[1]: tap=tap+np.array(pert[2])   # dis bozucu tork
        qdd=np.linalg.solve(M, tap)
        wh+=dt*qdd[0]; wk+=dt*qdd[1]; wa+=dt*qdd[2]
        h+=dt*wh; k+=dt*wk; a+=dt*wa
        # izgara sinirlari
        h=min(max(h,HIP[0]),HIP[-1]); k=min(max(k,KNE[0]),KNE[-1]); a=min(max(a,ANK[0]),ANK[-1])
        if h in(HIP[0],HIP[-1]): wh=0.0
        if k in(KNE[0],KNE[-1]): wk=0.0
        if a in(ANK[0],ANK[-1]): wa=0.0
        if i%rec==0:
            for x,v in [('t',t),('state',1 if state=='STANCE' else 0),('hip',h),('knee',k),('ankle',a),
                ('Fc',Fc),('uHE',e[HIP_EXT[0]]),('uKE',e[KNE_EXT[0]]),('uPF',e[jm['Sol']]),
                ('uHF',e[HIP_FLX[0]]),('uTA',e[jm['TA']]),('IaPF',Ia[jm['Sol']]),
                ('IaHE',Ia[HIP_EXT[0]]),('IaKE',Ia[KNE_EXT[0]]),('IIHE',II[HIP_EXT[0]]),('trans',len(trans))]:
                if x not in log: log[x]=[]
                log[x].append(v)
            if fullrec: FE.append(e.copy());FA.append(act.copy());FIa.append(Ia.copy());FII.append(II.copy());FT.append(t)
    out={x:np.array(v) for x,v in log.items()}; out['transitions']=trans
    if fullrec:
        out['full_t']=np.array(FT);out['full_e']=np.array(FE);out['full_a']=np.array(FA)
        out['full_Ia']=np.array(FIa);out['full_II']=np.array(FII);out['names']=np.array(names)
    return out

if __name__=='__main__':
    P=dict(yg=-0.010, kc=80.0, cc=4.0, bf=0.3, tau=0.020, bd=[1.5e-3,3e-3,6e-3],
           Ahe=0.16, Ake=0.27, cpf=0.045, cdf=0.06, Apf_st=0.03, Ahf=0.40, Adf=0.06,
           GIb=0.3, GIa=0.10, hip_ext_deg=22, hip_flx_deg=55, Foff=0.05, Fref=2.0,
           h0=45, k0=-118, a0=5)
    L=run(P, Tsim=6.0)
    tr=L['transitions']; print("gecis sayisi: %d"%len(tr))
    td=[t for t,s in tr if s=='SWING->STANCE']
    if len(td)>3: print("periyot (touchdown araligi): %.3f s (kadans %.1f Hz)"%(np.mean(np.diff(td[-4:])),1/np.mean(np.diff(td[-4:]))))
    h2=len(L['t'])//2
    print("kararli-yari eklem: (min .. max, ort)")
    for c in ['hip','knee','ankle']:
        v=np.degrees(L[c][h2:]); print("  %-6s %.0f .. %.0f (ort %.0f, genlik %.0f)"%(c,v.min(),v.max(),v.mean(),v.max()-v.min()))
    print("temas kuvveti: %.3f .. %.3f N | Ia_PF %.0f-%.0f"%(L['Fc'][h2:].min(),L['Fc'][h2:].max(),L['IaPF'][h2:].min(),L['IaPF'][h2:].max()))
    st=L['state'][h2:]; print("stance orani: %.2f"%st.mean())
