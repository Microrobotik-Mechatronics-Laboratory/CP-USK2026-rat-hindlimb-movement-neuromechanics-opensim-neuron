# u_stance_pipeline.py — Oturum 5, 31 Ağustos 2026
# Stance SO makinesi — DİSKE KAYITLI tek doğruluk kaynağı (H9 dersinden sonra).
# Çekirdek, DOKUNULMAZ u_swing_v2'yi yeniden üreterek doğrulanır (GRF'siz mod);
# stance modunda Lewis GRF'si YER ÇERÇEVESİNDE uygulanır: F = [AP, +V (yukarı +y), ML],
# istasyon = ayak gövdesinde v_cal + s·(v_toe − v_cal), Q_j = F·∂p/∂q_j (sonlu fark),
# talep = tau_ID − Q, çözüm: min Σa² + W·Σrezerv² (lsq_linear, W=1e6, 0≤a≤1).
# Kanıtlanmış çekirdek ayarları (salınım taraması, bu dosyanın üstündeki koşu kaydı):
#   DOF kısıtları = hip_flx, hip_add, hip_int, knee_flx, ankle_flx, ankle_add, ankle_int
#   kapasite = Fmax · fL_gauss(lmn; γ=0.45) · fV_Thelen(vn; Af=0.25, Flen=1.4) · cos(α0)
#   pasif kuvvet YOK, vn = v / (10·lmo)  [vmax = 10 lmo/s]
import numpy as np, json, csv, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # kod/yollar.py icin
import opensim as osim
from scipy.optimize import lsq_linear
from yollar import VERI, OSIM_FAZ1A, MOT_SMOOTH, U_SWING, KAS_PAR, LEWIS_GRF
# Kısıt kümeleri (31 Ağustos gecesi yeniden-üretim testleriyle KİMLİKLENDİ):
#   salınım SO = D7 (hip3+knee+ankle3), talep = tau_ID       → u_swing_v2'yi üretir
#   stance  SO = D6 (ankle_int HARİÇ),  talep = tau_ID − Q   → cop_recete/A_c'yi üretir
#     (ankle_int'i kısıtlamamanın nedeni: o eksende kas kapasitesi yok denecek kadar az;
#      kısıtlanırsa çözücü FDL'yi doyurup çözümü bozuyor — yeniden-üretim testi kanıtı)
D7 = ['hip_flx','hip_add','hip_int','knee_flx','ankle_flx','ankle_add','ankle_int']
D6 = ['hip_flx','hip_add','hip_int','knee_flx','ankle_flx','ankle_add']
W = 1e6
V_CAL = np.array([-0.005185,-0.000906,0.000543])
V_TOE = np.array([ 0.026419,-0.012510, 0.003049])
SF = np.array([0.0, 0.10, 0.20, 0.40, 0.70, 1.0])   # stance kesri çapaları
STANCE_SON = 67.5                                     # Lewis: stance = döngünün %0–67,5'i
KUTLE = 0.28                                          # kg (Johnson donör varsayımı)

class Makine:
    def __init__(self):
        self.ra = np.load(VERI/'rt_ara.npz', allow_pickle=True)   # rt_ara_uret.py uretir
        self.kp = json.load(open(KAS_PAR))
        idt = np.load(VERI/'id_tau.npz', allow_pickle=True)   # repoda .json karsiligi var, bicim donusumu yapilmadi
        self.idcols = [str(c) for c in idt['cols']]; self.TAU = idt['TAU']
        self.grf = json.load(open(LEWIS_GRF))
        lines = open(MOT_SMOOTH).read().splitlines()
        i0 = [i for i,l in enumerate(lines) if l.startswith('time')][0]
        self.mcols = lines[i0].split()
        self.mot = np.genfromtxt(MOT_SMOOTH, skip_header=i0+1)
        self.T = self.mot[-1,0]
        self.model = osim.Model(str(OSIM_FAZ1A))
        self.st = self.model.initSystem()
        self.cs = self.model.getCoordinateSet()
        self.foot = self.model.getBodySet().get('foot')
        mus = self.model.getMuscles()
        rows = [r for r in csv.reader(open(U_SWING)) if r and not r[0].startswith('#')]
        self.names = rows[0][1:]
        self.uswing = np.array(rows[1:], float)
        self.mobj = {mus.get(i).getName(): mus.get(i) for i in range(mus.getSize())}
        self.Fmax = np.array([self.mobj[n].getMaxIsometricForce() for n in self.names])
        self.lmo  = np.array([self.kp[n]['lmo'] for n in self.names])
        self.cosa = np.cos([self.kp[n]['alp'] for n in self.names])

    def kin(self, g):
        # DİKKAT (H10 dersi): yalnız sacrum_x/y/z ÇEVİRİDİR (metre, ham geçer);
        # sacrum_pitch/roll/yaw dahil BÜTÜN açılar dereceden radyana çevrilir.
        # 31 Ağustos gecesi bu satırdaki yanlış koşul (startswith('sacrum_'))
        # sacrum_pitch'i radyan sanıp sahneyi bozdu ve yanıltıcı H10 alarmı üretti.
        t = g/100.0*self.T
        for j,c in enumerate(self.mcols):
            if c=='time': continue
            v = np.interp(t, self.mot[:,0], self.mot[:,j])
            self.cs.get(c).setValue(self.st, v if c in ('sacrum_x','sacrum_y','sacrum_z') else np.deg2rad(v), False)
        self.model.realizePosition(self.st)

    def kapasite(self, row):
        lm = np.array([self.ra[n][row,0] for n in self.names])
        v  = np.array([self.ra[n][row,1] for n in self.names])
        lmn = lm/self.lmo; vn = np.clip(v/(10*self.lmo), -0.9999, None)
        fL = np.exp(-((lmn-1)**2)/0.45)
        Af, Fl = 0.25, 1.4; k = 2+2/Af
        fV = np.where(vn<=0, (1+vn)/(1-vn/Af), (k*Fl*vn+(Fl-1))/(k*vn+(Fl-1)))
        return self.Fmax*fL*fV*self.cosa

    def kollar(self, g):
        self.kin(g)
        return {c: np.array([self.mobj[n].computeMomentArm(self.st, self.cs.get(c)) for n in self.names]) for c in D7}

    def Fyer(self, g):
        # YER ÇERÇEVESİ: x = model x (AP kanalı), y = yukarı (V, +y), z = ML
        return np.array([np.interp(g, self.grf[k]['pct'], self.grf[k]['Nkg']) for k in ['AP','V','ML']])*KUTLE

    def Q(self, g, s):
        F = self.Fyer(g)
        loc = osim.Vec3(*(V_CAL + s*(V_TOE-V_CAL)))
        out = {}
        for c in D7:
            co = self.cs.get(c); q0 = co.getValue(self.st); h = 1e-5
            co.setValue(self.st, q0+h, False); self.model.realizePosition(self.st)
            pp = np.array([self.foot.findStationLocationInGround(self.st, loc).get(i) for i in range(3)])
            co.setValue(self.st, q0-h, False); self.model.realizePosition(self.st)
            pm = np.array([self.foot.findStationLocationInGround(self.st, loc).get(i) for i in range(3)])
            co.setValue(self.st, q0, False); self.model.realizePosition(self.st)
            out[c] = float(F @ ((pp-pm)/(2*h)))
        return out

    def coz(self, g, s=None):
        # s=None → salınım modu (D7, GRF yok); s verilirse stance modu (D6, tau_ID − Q)
        DOF = D7 if s is None else D6
        row = int(round(g*2))
        ARM = self.kollar(g)             # kin(g) burada kuruluyor
        ARM = {c: ARM[c] for c in DOF}
        cap = self.kapasite(row)
        tdem = np.array([self.TAU[row, self.idcols.index(c)] for c in DOF])
        if s is not None:
            Qd = self.Q(g, s)
            tdem = tdem - np.array([Qd[c] for c in DOF])
        A = np.array([ARM[c]*cap for c in DOF])
        M = np.vstack([np.sqrt(W)*A, np.eye(len(self.names))])
        b = np.concatenate([np.sqrt(W)*tdem, np.zeros(len(self.names))])
        x = lsq_linear(M, b, bounds=(0,1), max_iter=300).x
        rez = A@x - tdem                 # rezerv (N·m)
        return x, np.abs(rez).max()

    def salinim_dogrula(self):
        farklar = []
        for gi, g in enumerate(self.uswing[:,0]):
            x,_ = self.coz(g, s=None)
            farklar.append(np.abs(x - self.uswing[gi,1:]).max())
        return float(np.max(farklar))

    def stance_kos(self, degerler, gs=None):
        if gs is None: gs = np.arange(0, 65.5, 0.5)
        U = np.zeros((len(gs), len(self.names))); R = np.zeros(len(gs))
        for i,g in enumerate(gs):
            s = float(np.interp(g/STANCE_SON, SF, degerler))
            U[i], R[i] = self.coz(g, s=s)
        return gs, U, R

if __name__ == '__main__':
    mk = Makine()
    print('salınım yeniden üretimi (u_swing_v2, DOKUNULMAZ): maks fark = %.4f' % mk.salinim_dogrula())
