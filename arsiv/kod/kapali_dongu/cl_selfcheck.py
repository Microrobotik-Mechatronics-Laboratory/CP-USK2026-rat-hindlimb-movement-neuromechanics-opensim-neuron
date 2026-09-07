# cl_selfcheck.py — EMERGENT yuruyusun KENDINI DENETLEMESI: verify(P) kapilari + fitness(P).
# G9 (denetim 7b sonrasi): YAPISAL kapali-dongu testi. Geri beslemeyi faz-ortalamasi SABIT
# ileri-beslemeyle degistir; yuruyus SABITle de ayakta kalirsa geri besleme sadece surus
# SEVIYESIYDI (yapi degil). meanff'te bozulursa geri beslemenin zamanlamasi/yapisi zorunlu
# = gercek u(t)/r(t) kapali dongu.
import numpy as np
from cl_emergent import run, HIP, KNE, ANK
d=np.degrees
LIM={'hip':(d(HIP[0]),d(HIP[-1])),'knee':(d(KNE[0]),d(KNE[-1])),'ankle':(d(ANK[0]),d(ANK[-1]))}
def _td(L): return np.array([t for t,s in L['transitions'] if s=='SWING->STANCE'])
def _run(P,Tsim,dt=2e-5,**kw):   # dt=2e-5 yakinsak; dt=1e-4 bilek DOF'ta artefakt (Oturum 7c)
    try: return run(dict(P),Tsim=Tsim,dt=dt,rec=20,**kw)
    except Exception: return None
def _near(L,h2):
    return max(float(np.mean((d(L[c][h2:])<LIM[c][0]+6)|(d(L[c][h2:])>LIM[c][1]-6))) for c in ['hip','knee','ankle'])
def _cv(L):
    td=_td(L); p=np.diff(td)
    return float(np.std(p[len(p)//2:])/max(np.mean(p[len(p)//2:]),1e-6)) if len(td)>4 else 9.0

def verify(P, Tsim=5.0, verbose=True):
    L=_run(P,Tsim,reclog=True)
    if L is None: return {'PASS':False,'PASS_kritik':False,'reason':'sim cokti'}
    td=_td(L); t=L['t']; h2=len(t)//2; R={'n_transition':len(L['transitions'])}
    G1=len(td)>=6
    cv=_cv(L); cad=1/np.mean(np.diff(td[-4:])) if len(td)>4 else 0.0
    R['cadence_Hz']=cad; R['period_CV']=cv
    for c in ['hip','knee','ankle']:
        v=d(L[c][h2:]); R[c+'_min']=float(v.min()); R[c+'_max']=float(v.max())
        R[c+'_nearlim']=float(np.mean((v<LIM[c][0]+6)|(v>LIM[c][1]-6)))
    live_near=_near(L,h2)
    G2=cv<0.15
    G3=all(R[c+'_nearlim']<0.05 for c in ['hip','knee','ankle'])
    G4=(10<=R['hip_min'] and R['hip_max']<=75 and -150<=R['knee_min'] and R['knee_max']<=-90
        and -40<=R['ankle_min'] and R['ankle_max']<=35 and (R['hip_max']-R['hip_min'])>20)
    stance=float(L['state'][h2:].mean()); R['stance_ratio']=stance; G5=0.5<=stance<=0.7
    st=L['state'][h2:]>0.5; Fc=L['Fc'][h2:]
    R['Fc_stance']=float(Fc[st].mean()) if st.any() else 0.0
    R['Fc_swing']=float(Fc[~st].mean()) if (~st).any() else 0.0
    G6=R['Fc_stance']>0.1 and R['Fc_stance']>R['Fc_swing']*1.3
    ue=L['uHE'][h2:]; G7=(ue.min()>=0 and ue.max()<=1.0 and (ue.max()-ue.min())>0.02)
    R['IaHE_std']=float(np.std(L['IaHE'][h2:])); R['reflHE_std']=float(np.std(L['reflHE'][h2:]))
    G8=R['IaHE_std']>5
    # --- G9 YAPISAL: geri beslemeyi faz-ort SABITle degistir ---
    Lmff=_run(P,Tsim,fb='meanff',fb_st=L['refl_stance_mean'],fb_sw=L['refl_swing_mean'])
    if Lmff is not None and len(_td(Lmff))>1:
        h2m=len(Lmff['t'])//2; R['meanff_tr']=len(Lmff['transitions']); R['live_tr']=len(td)
        R['meanff_nearlim']=_near(Lmff,h2m); R['meanff_CV']=_cv(Lmff)
        # meanff BOZULUYORSA (ritim dusuyor / limite gidiyor / degiskenlik artiyor) -> yapi zorunlu
        G9=(R['meanff_tr']<len(td)-2) or (R['meanff_nearlim']>live_near+0.05) or (R['meanff_CV']>cv+0.08)
    else:
        R['meanff_tr']=0; R['live_tr']=len(td); R['meanff_nearlim']=1.0; R['meanff_CV']=9.0; G9=True
    R['live_nearlim']=live_near
    gates={'G1_ritim':G1,'G2_kararli':G2,'G3_limitten_uzak':G3,'G4_ROM':G4,'G5_stance':G5,
           'G6_temas':G6,'G7_u_gecerli':G7,'G8_r_canli':G8,'G9_yapisal_kapali_dongu':G9}
    R['gates']=gates; R['PASS']=all(gates.values())
    R['PASS_kritik']=G1 and G2 and G3 and G4 and G9
    if verbose:
        print("=== SELF-CHECK (denetim 7b: G9 yapisal) ===")
        for k,v in gates.items(): print("  [%s] %s"%('GECER' if v else 'KALIR ',k))
        print("  kadans %.1fHz stance %.2f | hip %.0f..%.0f knee %.0f..%.0f ankle %.0f..%.0f"%(
            cad,stance,R['hip_min'],R['hip_max'],R['knee_min'],R['knee_max'],R['ankle_min'],R['ankle_max']))
        print("  temas stance %.2fN swing %.2fN | refl_HE std %.3f (r(t) surusu ne kadar module ediyor)"%(
            R['Fc_stance'],R['Fc_swing'],R['reflHE_std']))
        print("  G9 yapisal: live gecis %d nearlim %.2f  vs  meanff gecis %d nearlim %.2f CV %.2f"%(
            R['live_tr'],live_near,R['meanff_tr'],R['meanff_nearlim'],R['meanff_CV']))
        print("  >>> KRITIK GECER: %s | TUM GECER: %s"%(R['PASS_kritik'],R['PASS']))
    return R

def fitness(P, Tsim=3.5):
    R=verify(P,Tsim=Tsim,verbose=False)
    if not R or R.get('reason'): return 1e6
    if R['n_transition']<6: return 1e5-R['n_transition']*100
    c=0.0
    c+=30*max(R[x+'_nearlim'] for x in ['hip','knee','ankle'])
    c+=20*R['period_CV']; c+=10*abs(R['stance_ratio']-0.58)
    c+=2*max(0,abs(R['cadence_Hz']-3.0)-1.0)
    c+=5*max(0,0.15-R['Fc_stance'])/0.15; c+=3*max(0,R['Fc_swing']-R['Fc_stance']*0.5)
    if not R['gates']['G4_ROM']: c+=15
    # YAPISAL kapali-dongu odulu: meanff (sabit-ort geri besleme) live'dan BELIRGIN kotu olsun
    struct_gap=(R.get('meanff_nearlim',0)-R.get('live_nearlim',0)) + 0.02*max(0,R['live_tr']-R.get('meanff_tr',R['live_tr']))
    c+=10*max(0, 0.05-struct_gap)          # yapi zorunlu degilse ceza (r(t) sus olmasin)
    return float(c)

# CMA-ES parametre uzayi — denetim 7b: cdf tavani 0.25 (bilek notru cdf/cpf~3 gerektiriyor), GII eklendi
PARSPEC=[('Ahe',0.05,0.40),('Ake',0.10,0.50),('cpf',0.0,0.15),('cdf',0.0,0.25),
         ('Apf_st',0.0,0.10),('Ahf',0.10,0.60),('Adf',0.0,0.20),('GIb',0.0,1.0),
         ('GIa',0.0,3.0),('GII',0.0,3.0),('kc',40.,150.),('hip_ext_deg',15.,30.),('hip_flx_deg',45.,65.)]
FIXED=dict(yg=-0.010, cc=4.0, bf=0.3, tau=0.020, tau_ema=0.12, bd=[1.5e-3,3e-3,6e-3],
           Fref=2.0, h0=45, k0=-118, a0=5)
def vec2P(x):
    P=dict(FIXED)
    for (n,lo,hi),xi in zip(PARSPEC,x): P[n]=lo+min(max(xi,0),1)*(hi-lo)
    return P
if __name__=='__main__':
    P=dict(FIXED, Ahe=0.16,Ake=0.27,cpf=0.045,cdf=0.06,Apf_st=0.03,Ahf=0.40,Adf=0.06,
           GIb=0.3,GIa=0.10,GII=0.0,hip_ext_deg=22,hip_flx_deg=55,kc=80.0)
    verify(P, Tsim=4.0)
