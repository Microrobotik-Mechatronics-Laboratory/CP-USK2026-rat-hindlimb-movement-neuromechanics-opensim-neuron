# =============================================================================
# kod_02_swing_id_so.py
# Swing ID -> SO -> u_swing_v2.csv  (40_ kaydı 8g/8h)
# Girdiler: rat_hindlimb_faz1a.osim, rat_walk_bone_smooth.mot
# Yöntem: ID (kas kuvvetleri hariç, 15 Hz) -> her swing örnekleminde
#   R (7 DOF x 38 kas, OpenSim computeMomentArm)
#   rijit tendon: lm=sqrt((lmt-tsl)^2+(lmo·sinα0)^2), cosα=(lmt-tsl)/lm
#   fL=exp(-(l~-1)^2/γ); fPE Thelen; fV: Thelen a=1 kapalı-form
#     konsantrik (1+u)/(1-u/Af), eksantrik (1+c·Flen·u)/(1+c·u), c=(2+2/Af)/(Flen-1)
#     u = (dlm/dt)/(lmo·Vmax); dlm periyodik merkezi farktan
#   SO: min Σa² + 1e6·Σr²  k.k.  R·(Fmax·fL·fV·cosα·a) + R·(Fmax·fPE·cosα) + r = τ_ID
# Bayraklar: fV'nin (0.25+0.75a) terimi ihmal; pelvis reçeteli; stance kullanılamaz.
# =============================================================================
import opensim as osim, numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # kod/yollar.py icin
from scipy.optimize import minimize
from yollar import VERI, OSIM_FAZ1A, MOT_SMOOTH
DEG=np.pi/180; T=0.387; DUTY=64.8
MODEL=str(OSIM_FAZ1A); MOT=str(MOT_SMOOTH); ID_STO=VERI/'id_bone.sto'   # ID ara ciktisi

# ---- 1) ID ----
idt=osim.InverseDynamicsTool()
idt.setModelFileName(MODEL); idt.setCoordinatesFileName(MOT)
idt.setStartTime(0.0); idt.setEndTime(T)
ex=osim.ArrayStr(); ex.append('Muscles'); idt.setExcludedForces(ex)
idt.setLowpassCutoffFrequency(15.0)
idt.setResultsDir(str(VERI)); idt.setOutputGenForceFileName('id_bone.sto')
assert idt.run()

L=open(ID_STO).read().splitlines()
i0=[i for i,l in enumerate(L) if l.strip()=='endheader'][0]+1
hdr=L[i0].split('\t')
D={h:np.array([float(l.split('\t')[hdr.index(h)]) for l in L[i0+1:] if l.strip()]) for h in hdr}
gid=D['time']/T*100

# ---- 2) model + kinematik ----
m=osim.Model(MODEL); s=m.initSystem()
cs=m.getCoordinateSet(); mus=m.getMuscles(); N=mus.getSize()
mn=[mus.get(i).getName() for i in range(N)]
th=[osim.Thelen2003Muscle.safeDownCast(mus.get(i)) for i in range(N)]
par=lambda f: np.array([f(x) for x in th])
Fmax=par(lambda x:x.getMaxIsometricForce()); lmo=par(lambda x:x.getOptimalFiberLength())
tsl=par(lambda x:x.getTendonSlackLength());  a0=par(lambda x:x.getPennationAngleAtOptimalFiberLength())
gam=par(lambda x:x.get_KshapeActive()); kpe=par(lambda x:x.get_KshapePassive())
e0=par(lambda x:x.get_FmaxMuscleStrain()); Af=par(lambda x:x.get_Af())
Flen=par(lambda x:x.get_Flen()); Vmax=par(lambda x:x.getMaxContractionVelocity())

Lm=open(MOT).read().splitlines()
j0=Lm.index('endheader')+1; mh=Lm[j0].split('\t')
C={h:np.array([float(l.split('\t')[mh.index(h)]) for l in Lm[j0+1:] if l.strip()]) for h in mh}
g=C['time']/T*100
DOFS=['hip_flx','hip_add','hip_int','knee_flx','ankle_flx','ankle_add','ankle_int']
co=[cs.get(k) for k in DOFS]
def setpose(j):
    for k in ['sacrum_pitch','sacroiliac_flx','hip_add','hip_flx','knee_flx','ankle_flx','ankle_add']:
        cs.get(k).setValue(s,C[k][j]*DEG,False)
    m.assemble(s); m.realizePosition(s)

# ---- 3) lmt(t) -> fV(t) ----
LM=np.zeros((len(g),N))
for j in range(len(g)):
    setpose(j)
    for i in range(N): LM[j,i]=mus.get(i).getLength(s)
dt=T/(len(g)-1)
dlmt=(np.roll(LM,-1,0)-np.roll(LM,1,0))/(2*dt)
lmf=np.sqrt(np.maximum(LM-tsl,1e-5)**2+(lmo*np.sin(a0))**2)
u=(np.maximum(LM-tsl,1e-5)/lmf)*dlmt/(lmo*Vmax)
c=(2+2/Af)/(Flen-1)
fV=np.where(u<=0,np.clip((1+u)/(1-u/Af),0,None),(1+c*Flen*u)/(1+c*u))

# ---- 4) SO (swing) ----
sw=np.where(g>=DUTY)[0]
tauM=np.vstack([D[k+'_moment'] for k in DOFS]).T
U=np.zeros((len(sw),N)); RES=np.zeros((len(sw),7)); prev=np.full(N,0.05)
for row,j in enumerate(sw):
    setpose(j)
    R=np.array([[mus.get(i).computeMomentArm(s,co[k]) for i in range(N)] for k in range(7)])
    ln=lmf[j]/lmo; cA=np.maximum(LM[j]-tsl,1e-5)/lmf[j]
    fL=np.exp(-(ln-1)**2/gam)
    fPE=np.where(ln>1,(np.exp(kpe*(ln-1)/e0)-1)/(np.exp(kpe)-1),0.0)
    tau=np.array([np.interp(g[j],gid,tauM[:,k]) for k in range(7)])
    A=R*(Fmax*fL*fV[j]*cA); tp=R@(Fmax*fPE*cA); W=1e6
    f=lambda x: np.sum(x[:N]**2)+W*np.sum(x[N:]**2)
    jac=lambda x: np.concatenate([2*x[:N],2*W*x[N:]])
    cons={'type':'eq','fun':lambda x:A@x[:N]+tp+x[N:]-tau,'jac':lambda x:np.hstack([A,np.eye(7)])}
    sol=minimize(f,np.r_[prev,np.zeros(7)],jac=jac,method='SLSQP',constraints=[cons],
                 bounds=[(0,1)]*N+[(-1,1)]*7,options=dict(maxiter=300,ftol=1e-12))
    U[row]=sol.x[:N]; RES[row]=sol.x[N:]; prev=sol.x[:N]
print("max|rezerv| (N·mm):",(np.abs(RES).max(0)*1000).round(4))
hdr2="gait_pct,"+",".join(mn)
out=["# u_swing v2 (bkz. 40_ kaydi 8h)",hdr2]
for j2 in range(len(sw)):
    out.append(f"{g[sw[j2]]:.1f},"+",".join(f"{U[j2,i]:.5f}" for i in range(N)))
open(VERI/'u_swing_v2.csv','w').write("\n".join(out))
print("u_swing_v2.csv yazildi")
