# cl_selfcheck.py — EMERGENT yuruyusun KENDINI DENETLEMESI.
# Iki sey saglar:
#   verify(P)  -> dogru/yanlis KAPILARI (agent basari/basarisizligi bilir)
#   fitness(P) -> CMA-ES icin skaler MALIYET (kucuk=iyi)
# En kritik kapi G9: refleks(Ia/yuk) kapatilinca yuruyus bozuluyor mu? Bozuluyorsa
# r(t) DOGRU sekilde donguyu tasiyor demektir (ileri-besleme oynatmasi degil).
import numpy as np
from cl_emergent import run, HIP, KNE, ANK
d=np.degrees
LIM={'hip':(d(HIP[0]),d(HIP[-1])),'knee':(d(KNE[0]),d(KNE[-1])),'ankle':(d(ANK[0]),d(ANK[-1]))}

def _td(L): return np.array([t for t,s in L['transitions'] if s=='SWING->STANCE'])

def _run(P,Tsim,dt=1e-4):
    try: return run(dict(P),Tsim=Tsim,dt=dt,rec=20)
    except Exception: return None

def verify(P, Tsim=5.0, verbose=True):
    L=_run(P,Tsim)
    if L is None: return {'PASS':False,'PASS_kritik':False,'reason':'sim cokti'}
    td=_td(L); t=L['t']; h2=len(t)//2; R={'n_transition':len(L['transitions'])}
    G1=len(td)>=6
    if len(td)>4:
        pers=np.diff(td); per=float(np.mean(pers[-4:])); cad=1/per
        cv=float(np.std(pers[len(pers)//2:])/max(np.mean(pers[len(pers)//2:]),1e-6))
    else: per=cad=0.0; cv=9.0
    R['cadence_Hz']=cad; R['period_s']=per; R['period_CV']=cv
    for c in ['hip','knee','ankle']:
        v=d(L[c][h2:]); lo,hi=LIM[c]
        R[c+'_min']=float(v.min()); R[c+'_max']=float(v.max())
        R[c+'_nearlim']=float(np.mean((v<lo+6)|(v>hi-6)))
    G2=cv<0.15
    G3=all(R[c+'_nearlim']<0.05 for c in ['hip','knee','ankle'])
    G4=(10<=R['hip_min'] and R['hip_max']<=75 and -150<=R['knee_min'] and R['knee_max']<=-90
        and -40<=R['ankle_min'] and R['ankle_max']<=35 and (R['hip_max']-R['hip_min'])>20)
    stance=float(L['state'][h2:].mean()); R['stance_ratio']=stance; G5=0.5<=stance<=0.7
    st=L['state'][h2:]>0.5; Fc=L['Fc'][h2:]
    R['Fc_stance']=float(Fc[st].mean()) if st.any() else 0.0
    R['Fc_swing']=float(Fc[~st].mean()) if (~st).any() else 0.0
    G6=R['Fc_stance']>0.1 and R['Fc_stance']>R['Fc_swing']*1.3
    ue=L['uHE'][h2:]; R['uHE_rng']=(float(ue.min()),float(ue.max()))
    G7=(ue.min()>=0 and ue.max()<=1.0 and (ue.max()-ue.min())>0.02)
    R['IaHE_std']=float(np.std(L['IaHE'][h2:])) if 'IaHE' in L else 0.0
    G8=R['IaHE_std']>5
    # G9 KAPALI DONGU testi: refleks (Ia + yuk) kapat; r(t) tasiyorsa yuruyus bozulur.
    # Uc olcut (ayak pinlenmesinden etkilenmesin diye): limit-yakinlik, ritim sayisi, periyot-CV.
    R['reflexon_nearlim']=max(R[c+'_nearlim'] for c in ['hip','knee','ankle'])
    Loff=_run(dict(P,GIa=0.0,GIb=0.0),Tsim)
    if Loff is not None and len(_td(Loff))>4:
        h2o=len(Loff['t'])//2; tdo=_td(Loff); perso=np.diff(tdo)
        offnear=max(float(np.mean((d(Loff[c][h2o:])<LIM[c][0]+6)|(d(Loff[c][h2o:])>LIM[c][1]-6))) for c in ['hip','knee','ankle'])
        offcv=float(np.std(perso[len(perso)//2:])/max(np.mean(perso[len(perso)//2:]),1e-6))
        R['reflexoff_nearlim']=offnear; R['reflexoff_CV']=offcv
        G9=(offnear>R['reflexon_nearlim']+0.03) or (len(Loff['transitions'])<len(td)-2) or (offcv>cv+0.05)
    else:
        R['reflexoff_nearlim']=1.0; R['reflexoff_CV']=9.0; G9=True   # kapatinca coker = r(t) gerekli
    gates={'G1_ritim':G1,'G2_kararli':G2,'G3_limitten_uzak':G3,'G4_ROM':G4,'G5_stance':G5,
           'G6_temas':G6,'G7_u_gecerli':G7,'G8_r_canli':G8,'G9_kapali_dongu':G9}
    R['gates']=gates; R['PASS']=all(gates.values())
    R['PASS_kritik']=G1 and G2 and G3 and G4 and G9   # olmazsa-olmaz: kararli, limitten uzak, fizyolojik, r(t) tasiyor
    if verbose:
        print("=== SELF-CHECK (dogru/yanlis kapilari) ===")
        for k,v in gates.items(): print("  [%s] %s"%('GECER' if v else 'KALIR ',k))
        print("  kadans %.1fHz stance %.2f | hip %.0f..%.0f knee %.0f..%.0f ankle %.0f..%.0f"%(
            cad,stance,R['hip_min'],R['hip_max'],R['knee_min'],R['knee_max'],R['ankle_min'],R['ankle_max']))
        print("  temas stance %.2fN swing %.2fN | r(t) Ia_HE std %.0f"%(R['Fc_stance'],R['Fc_swing'],R['IaHE_std']))
        print("  KAPALI-DONGU: refleks-kapali limit-yakinlik %.2f vs acik %.2f (off>on ise r(t) tasiyor)"%(
            R['reflexoff_nearlim'],R['reflexon_nearlim']))
        print("  >>> KRITIK GECER: %s | TUM GECER: %s"%(R['PASS_kritik'],R['PASS']))
    return R

def fitness(P, Tsim=3.5):
    R=verify(P,Tsim=Tsim,verbose=False)
    if not R or R.get('reason'): return 1e6
    if R['n_transition']<6: return 1e5-R['n_transition']*100
    c=0.0
    c+=30*max(R[x+'_nearlim'] for x in ['hip','knee','ankle'])   # limitten uzak dur (en onemli)
    c+=20*R['period_CV']                                          # cevrim-cevrim kararli
    c+=10*abs(R['stance_ratio']-0.58)                             # walk stance orani
    c+=2*max(0,abs(R['cadence_Hz']-3.0)-1.0)                      # 2-4 Hz bandi
    c+=5*max(0,0.15-R['Fc_stance'])/0.15                          # stance'te yuk
    c+=3*max(0,R['Fc_swing']-R['Fc_stance']*0.5)                  # swing'de bosal
    if not R['gates']['G4_ROM']: c+=15                            # fizyolojik ROM
    c+=8*max(0,R['reflexon_nearlim']+0.02-R['reflexoff_nearlim']) # KAPALI DONGU: r(t) tasisin
    return float(c)

# CMA-ES parametre uzayi (isim, alt, ust) — normalize [0,1] -> [lo,hi]
PARSPEC=[('Ahe',0.05,0.40),('Ake',0.10,0.50),('cpf',0.0,0.15),('cdf',0.0,0.15),
         ('Apf_st',0.0,0.10),('Ahf',0.10,0.60),('Adf',0.0,0.15),('GIb',0.0,1.0),
         ('GIa',0.0,0.40),('kc',40.,150.),('hip_ext_deg',15.,30.),('hip_flx_deg',45.,65.)]
FIXED=dict(yg=-0.010, cc=4.0, bf=0.3, tau=0.020, bd=[1.5e-3,3e-3,6e-3],
           Foff=0.05, Fref=2.0, h0=45, k0=-118, a0=5)
def vec2P(x):
    P=dict(FIXED)
    for (n,lo,hi),xi in zip(PARSPEC,x): P[n]=lo+min(max(xi,0),1)*(hi-lo)
    return P

if __name__=='__main__':
    P=dict(FIXED, Ahe=0.16,Ake=0.27,cpf=0.045,cdf=0.06,Apf_st=0.03,Ahf=0.40,Adf=0.06,
           GIb=0.3,GIa=0.10,hip_ext_deg=22,hip_flx_deg=55,kc=80.0)
    R=verify(P, Tsim=4.0)
