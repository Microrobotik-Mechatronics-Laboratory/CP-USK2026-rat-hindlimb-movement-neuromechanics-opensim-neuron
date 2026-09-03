# =============================================================================
# kod_01_rat_walk_bone_uret.py
# Bauman kemik açıları -> model koordinatları -> rat_walk_bone.mot (+smooth)
# Girdiler: bauman_fig4_v3_hipknee.csv (kalça/diz, bölge-tabanlı, 40_ kaydı 8d)
#           bauman_fig4_v2_kapali_devre.csv (bilek, 39_ kaydı)
#           rat_hindlimb_0_2.osim yanında rig.py (FK; proje deposunda)
# Sabitler: T=0,387 s (GB2002 Fig1A level medyan; 40_ kaydı 1. bölüm)
#           sacrum_pitch 4-nokta (Bauman Fig 3 kemik pelvis doğrusu; 8. bölüm 6)
# Çıktılar: rat_walk_bone.mot (ham v4), rat_walk_bone_smooth.mot (15 Hz)
# =============================================================================
import numpy as np, csv, pickle, rig
from scipy.interpolate import CubicSpline
from scipy.signal import butter, filtfilt
DEG=np.pi/180
T=0.387                                   # s  (GB2002 Fig1A level medyan)
DUTY=64.8                                 # %  (Bauman Fig4 stance çizgisi)
ISCH=np.array([-13.77e-3,0.83e-3,-2.30e-3,1.0])   # pelvis: BFp/STa/SM origin centroid (±8° bayrak)
TOE =np.array([0.024,0,0,1.0])                     # foot x-ekseni vekili (yön x'ten bağımsız)
PITCH_PTS=[(0.0,24.6),(32.4,20.5),(64.8,23.5),(82.4,19.9)]  # Bauman Fig3 ölçümü

def oku(path, cols):
    rows=[r for r in csv.reader(open(path)) if r and not r[0].startswith('#')]
    h=rows[0]; return [np.array([float(r[h.index(c)]) for r in rows[1:]]) for c in cols]

g,hipA,kneeA = oku('bauman_fig4_v3_hipknee.csv',['gait_pct','hip_bone_mean','knee_bone_mean'])
ga,ankA0     = oku('bauman_fig4_v2_kapali_devre.csv',['gait_pct','ankle_bone_mean_deg'])
ankA=np.interp(g,ga,ankA0)

# ---- diz merkezi: iki-taraflı çember fiti (tibia translation spline yayları) ----
tib=[b for b in rig.bodies if b['name']=='tibia'][0]
th=np.linspace(-150,-20,131)*DEG; P=[]; Q=[]
for k in th:
    Tj=rig.joint_T(tib,{'knee_flx':k}); R,tv=Tj[:3,:3],Tj[:3,3]
    P.append(tv); Q.append(-R.T@tv)
P=np.array(P); Q=np.array(Q)
def circfit(xy):
    x,y=xy[:,0],xy[:,1]; A=np.c_[2*x,2*y,np.ones(len(x))]
    c=np.linalg.lstsq(A,x**2+y**2,rcond=None)[0]
    return np.array([c[0],c[1]])
cf=np.r_[circfit(P[:,:2]), P[:,2].mean()]     # femur-taraf (yarıçap~39,5=tibia sağlaması)
ct=np.r_[circfit(Q[:,:2]), Q[:,2].mean()]     # tibia-taraf (yarıçap~33,8~femur)
CF=np.r_[cf,1.0]; CT=np.r_[ct,1.0]

# ---- Bauman-tanımlı açılar (model geometrisi üstünde) ----
FIX=dict(sacrum_pitch=22.1*DEG,sacrum_roll=0,sacrum_yaw=0,sacrum_x=0,sacrum_y=0.05,sacrum_z=0,
         sacroiliac_flx=3.7*DEG,hip_add=-10*DEG,hip_int=0,ankle_add=-5*DEG,ankle_int=0)
def ang(u,v):
    c=np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v)
    return np.degrees(np.arccos(np.clip(c,-1,1)))
def bauman(hf,kf,af):
    q=dict(rig.defaults); q.update(FIX)
    q.update(hip_flx=hf*DEG,knee_flx=kf*DEG,ankle_flx=af*DEG)
    W=rig.fk(q); H=W['femur'][:3,3]; A=W['foot'][:3,3]
    K=0.5*((W['femur']@CF)[:3]+(W['tibia']@CT)[:3])
    I=(W['pelvis']@ISCH)[:3]; Tt=(W['foot']@TOE)[:3]
    return 180-ang(I-H,K-H), ang(H-K,A-K), ang(K-A,Tt-A)   # hip, knee, ankle (Bauman s.4)

# tablo tersi + 2 tur Gauss-Seidel (1D Newton)
def tab(coord_grid, idx):
    out=[]
    for v in coord_grid:
        args=[20,-90,10]; args[idx]=v
        out.append(bauman(*args)[idx])
    return np.array(out)
hg=np.linspace(-50,70,241); kg=np.linspace(-150,-20,261); ag=np.linspace(-30,60,181)
tabs=[tab(hg,0),tab(kg,1),tab(ag,2)]
inv=lambda tb,gr,val: np.interp(val,tb[::-1],gr[::-1]) if tb[0]>tb[-1] else np.interp(val,tb,gr)
hip=inv(tabs[0],hg,hipA); knee=inv(tabs[1],kg,kneeA); ank=inv(tabs[2],ag,ankA)
for _ in range(2):
    for i in range(len(g)):
        for idx,tgt in enumerate((hipA[i],kneeA[i],ankA[i])):
            v=[hip[i],knee[i],ank[i]]
            f=lambda x: bauman(*[x if j==idx else v[j] for j in range(3)])[idx]-tgt
            x=v[idx]; fx=f(x); d=(f(x+0.25)-fx)/0.25
            (hip,knee,ank)[idx].__setitem__(i,x-fx/d)

# ---- sacrum_pitch(t): 4 nokta + periyodik kübik ----
pc,pv=zip(*PITCH_PTS)
spf=CubicSpline(list(pc)+[100.0],list(pv)+[pv[0]],bc_type='periodic')
sp=spf(g)

def yaz(path, H,K,A, ad):
    t=g/100*T
    cols=['time','sacrum_pitch','sacrum_roll','sacrum_yaw','sacrum_x','sacrum_y','sacrum_z',
          'sacroiliac_flx','hip_flx','hip_add','hip_int','knee_flx','ankle_flx','ankle_add','ankle_int']
    fx=dict(sacrum_roll=0,sacrum_yaw=0,sacrum_x=0,sacrum_y=0.05,sacrum_z=0,
            sacroiliac_flx=3.7,hip_add=-10.0,hip_int=0,ankle_add=-5.0,ankle_int=0)
    L=[ad,'version=1',f'nRows={len(t)}',f'nColumns={len(cols)}','inDegrees=yes','endheader','\t'.join(cols)]
    for i in range(len(t)):
        vv=dict(fx); vv.update(time=t[i],sacrum_pitch=sp[i],hip_flx=H[i],knee_flx=K[i],ankle_flx=A[i])
        L.append('\t'.join(f"{vv[c]:.6f}" for c in cols))
    open(path,'w').write('\n'.join(L))
yaz('rat_walk_bone.mot',hip,knee,ank,'rat_walk_bone')

# ---- smooth: Butterworth 4, 15 Hz, sıfır-faz, periyodik dolgu ----
fs=201/T; b,a=butter(4,15/(fs/2))
sm=lambda x: filtfilt(b,a,np.concatenate([x[:-1],x[:-1],x]))[200:401]
yaz('rat_walk_bone_smooth.mot',sm(hip),sm(knee),sm(ank),'rat_walk_bone_smooth')
print("rat_walk_bone.mot + smooth yazildi")
