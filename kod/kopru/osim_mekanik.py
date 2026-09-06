# =============================================================================
# osim_mekanik.py — kapali dongunun mekanik yarisi: OpenSim ileri dinamigi.
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru)
# Girdi:  model/rat_hindlimb_faz1a.osim, veri/kapali_dongu/cl_grid3d.npz (kilit degerleri)
# Cikti:  her kopru adiminda q, qd, kas-tendon boyu ve hizi; girdi olarak kas uyarimi u(t)
#
# Neden ileri dinamik: bugunku hat (ID + statik optimizasyon) kinematigi RECETE olarak alip
# geriye dogru kas komutu cozer. Kapali donguda hareketin komuttan DOGMASI gerekir
# (PREPRINT bolum 2). Bu yuzden burada q recete degil, sonuctur.
#
# TASARIM KARARLARI:
# - Serbest olmayan koordinatlar KILITLENIR (set_locked). Kilit degerleri cl_grid3d.npz'nin
#   FIX/cnames dizilerinden alinir; boylece bu kosu mevcut kapali dongu sonuclariyla ayni
#   pozda olur ve karsilastirilabilir.
# - Kas uyarimi PrescribedController + Constant fonksiyonlarla verilir; her kopru adiminda
#   Constant'in degeri guncellenir. u UYARIM'dir (excitation); aktivasyon dinamigini
#   Thelen2003Muscle kendi cozer -- boylece sinyal iki kez filtrelenmez.
# - Entegratör RungeKuttaMerson, degisken ic adimli. Kopru adimi disaridan sabittir; NEURON
#   ile ayni ani paylasmak icin gereken budur, OpenSim'in ic adim sayisi serbesttir.
#
# BILINEN SAPMALAR:
# - Bilek DOF'unun eylemsizligi cok kucuktur (kapali dongu notu: M[ankle,ankle] ~ 1.1e-7,
#   kalcanin ~1/120'si). Acik entegrasyonda kararsizlik kaynagi budur; burada degisken adimli
#   ortuk-olmayan RK kullanildigi icin entegratör kendi adimini kucultur.
# - Kilitli koordinatlar OpenSim'de KISIT olarak uygulanir; s.getNQ() yine 14 doner ama
#   dinamik kisitlidir.
# =============================================================================
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # kod/yollar.py icin
import numpy as np
import opensim as osim
from yollar import OSIM_FAZ1A, GRID3D


class Mekanik:
    def __init__(self, serbest=('ankle_flx',), dt_kopru_s=3e-4, dogruluk=1e-4,
                 baslangic=None):
        self.dt = float(dt_kopru_s)
        self.dogruluk = float(dogruluk)
        self.model = osim.Model(str(OSIM_FAZ1A))
        g = np.load(GRID3D, allow_pickle=True)
        fix = dict(zip([str(x) for x in g['cnames']], [float(v) for v in g['FIX']]))
        self.izgara_par = dict(tsl=g['tsl'], lmo=g['lmo'], alp=g['alp'],
                               Fmax=g['Fmax'], adlar=[str(x) for x in g['names']])

        cs = self.model.getCoordinateSet()
        self.serbest = list(serbest)
        for i in range(cs.getSize()):
            c = cs.get(i)
            n = c.getName()
            if n in self.serbest:
                if baslangic and n in baslangic:
                    c.setDefaultValue(float(baslangic[n]))
                elif n in fix:
                    c.setDefaultValue(fix[n])
                continue
            if n in fix:
                c.setDefaultValue(fix[n])
            c.set_locked(True)                 # kilit: kisit olarak uygulanir

        # Kas uyarimini disaridan yazabilmek icin sabit fonksiyonlu kontrolcu
        self.mus = self.model.getMuscles()
        self.n = self.mus.getSize()
        self.adlar = [self.mus.get(i).getName() for i in range(self.n)]
        self.kont = osim.PrescribedController()
        self.kont.setName('kopru')
        for i in range(self.n):
            mu = self.mus.get(i)
            self.kont.addActuator(mu)
            self.kont.prescribeControlForActuator(mu.getName(), osim.Constant(0.0))
        self.model.addController(self.kont)

        self.s = self.model.initSystem()

        # KRITIK: prescribeControlForActuator fonksiyonu KOPYALAR. Disaridan yazilan nesne
        # modeldeki nesne degildir; ona setValue yapmak sessizce hicbir sey yapmaz (olculdu:
        # TA %100 uyarimla bile bilek yorungesi pasif kosula birebir ayni cikti). Bu yuzden
        # fonksiyon nesneleri initSystem'den SONRA kontrolcunun kendi kumesinden alinir.
        fs = self.kont.upd_ControlFunctions()
        self.fonk = [osim.Constant.safeDownCast(fs.get(i)) for i in range(self.n)]
        assert all(f is not None for f in self.fonk), 'kontrol fonksiyonlari Constant degil'
        self.koord = {n: cs.get(n) for n in self.serbest}
        # Izgara kas sirasi ile modelin kas sirasi ayni mi? (u ve lmt dizileri bu siraya bagli)
        assert self.adlar == self.izgara_par['adlar'], (
            'kas sirasi uyusmuyor: model=%s izgara=%s' % (self.adlar[:3], self.izgara_par['adlar'][:3]))

    # -- kosu --------------------------------------------------------------------------
    def baslat(self):
        self.model.equilibrateMuscles(self.s)
        self.s.setTime(0.0)
        self.man = osim.Manager(self.model)
        self.man.setIntegratorMethod(osim.Manager.IntegratorMethod_RungeKuttaMerson)
        self.man.setIntegratorAccuracy(self.dogruluk)
        self.man.initialize(self.s)
        self.t = 0.0
        return self.oku()

    def uyarim_yaz(self, u):
        """u: (38,) dizi, 0..1 arasi kas uyarimi (excitation)."""
        u = np.clip(np.asarray(u, dtype=float), 0.0, 1.0)
        for i in range(self.n):
            self.fonk[i].setValue(float(u[i]))

    def adim(self):
        self.t += self.dt
        self.s = self.man.integrate(self.t)
        return self.oku()

    def oku(self):
        """q [rad], qd [rad/s], kas-tendon boyu [m] ve hizi [m/s] doner."""
        self.model.realizeVelocity(self.s)
        q = np.array([self.koord[n].getValue(self.s) for n in self.serbest])
        qd = np.array([self.koord[n].getSpeedValue(self.s) for n in self.serbest])
        lmt = np.array([self.mus.get(i).getLength(self.s) for i in range(self.n)])
        vlmt = np.array([self.mus.get(i).getLengtheningSpeed(self.s) for i in range(self.n)])
        return q, qd, lmt, vlmt

    def kas_indisleri(self, adlar):
        return [self.adlar.index(a) for a in adlar]
