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
                 baslangic=None, limitler=None):
        """limitler: {koordinat: (alt_derece, ust_derece)} -- verilirse adim() sinir asimini
        KIRPAR (deger sinira cekilir, hiz sifirlanir). Gerekce: modelde koordinat range'i yok
        (DOGRULAMA H8) ve 3 DOF ileri dinamikte eklemler kas geometrisinin tanim alani
        (cl_grid3d izgarasi) disina savrulup integratoru sunduruyor (olculdu). Tarif ve
        [tasarim] etiketi devre_par.json kopru.eklem_siniri'nda."""
        self.dt = float(dt_kopru_s)
        self.dogruluk = float(dogruluk)
        self.model = osim.Model(str(OSIM_FAZ1A))
        # Limitler KUVVET degil KIRPMADIR (adim() icinde): sinir asilirsa koordinat sinirdan
        # KIRPMA_ICERI kadar iceri cekilir, hizi sifirlanir -- devralinan kodun
        # (arsiv/kod/kapali_dongu/cl_emergent.py:110-114) UYARLANMIS OpenSim karsiligi.
        # BIREBIR DEGIL: devralinan kod sinirin kendisine kirpar ve hizi float esitlik
        # kontrolüyle sifirlar; burada hedef sinirdan 0.5 derece iceride ve hiz kosulsuz
        # sifirlanir -- DOGRULAMA R.9. Iki olculmus ders (07.09.2026):
        # 1) CoordinateLimitForce REDDEDILDI: bilek DOF'unun cok kucuk eylemsizliginde
        #    (M[ankle,ankle] ~ 1.1e-7) her yay sertligi ~1 kHz'lik mod uretip integratoru
        #    mikro-adimlara dusuruyor (0.5 s kosu > 10 dk CPU).
        # 2) Kirpma hedefi SINIRIN KENDISI OLAMAZ: izgara ucunda kas sarma geometrisi kotu
        #    kosullu; koordinat tam ucta tutulunca integrator tek adimda dakikalarca
        #    surunuyor (pay=0.75 kosusu 13 dk'da 0.01 s ilerledi). Hedef sinirdan 0.5 derece
        #    iceridedir; sinirin kendisi de cagiran tarafta izgara ucundan iceri cekilir.
        self.limitler = {ad: (np.radians(alt), np.radians(ust))
                         for ad, (alt, ust) in (limitler or {}).items()}
        self.KIRPMA_ICERI = np.radians(0.5)
        self.limit_olay = 0                     # kirpma sayaci; kosu sonunda raporlanir
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
        # Fmax IKI kaynaktan okunuyor: kuvvet uretimi izgaradan (self.izgara_par['Fmax']),
        # antagonist denge olcegi ise modelden (kopru._kapasite_olc -> getMaxIsometricForce).
        # Ikisi ayrisirsa denge olcegi kuvvet uretimiyle tutarsiz olur ve sessizce yanlis
        # sonuc verir. Olculdu (07.09.2026): fark 0 -- bu assert onu boyle tutar.
        F_izg = np.asarray(self.izgara_par['Fmax'], dtype=float)
        F_mod = np.array([self.mus.get(i).getMaxIsometricForce() for i in range(self.n)])
        assert np.allclose(F_izg, F_mod, rtol=0, atol=1e-9), (
            'Fmax izgara ile model arasinda ayrisiyor: maks fark=%.6g N (kas %s). Denge '
            'olcegi kuvvet uretimiyle tutarsiz olur.'
            % (np.abs(F_izg - F_mod).max(), self.adlar[int(np.argmax(np.abs(F_izg - F_mod)))]))

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
        if self.limitler:
            tasti = False
            for ad, (alt, ust) in self.limitler.items():
                c = self.koord[ad]
                v = c.getValue(self.s)
                if v < alt or v > ust:
                    # hedef sinirdan iceride: ucta kotu kosullu geometriden uzak dur
                    c.setValue(self.s, (alt + self.KIRPMA_ICERI) if v < alt
                                       else (ust - self.KIRPMA_ICERI))
                    c.setSpeedValue(self.s, 0.0)
                    tasti = True
            if tasti:
                # state elle degisti; integrator yeni durumdan yeniden baslatilir
                self.limit_olay += 1
                self.man.initialize(self.s)
        return self.oku()

    def oku(self):
        """q [rad], qd [rad/s], kas-tendon boyu [m] ve hizi [m/s] doner."""
        self.model.realizeVelocity(self.s)
        q = np.array([self.koord[n].getValue(self.s) for n in self.serbest])
        qd = np.array([self.koord[n].getSpeedValue(self.s) for n in self.serbest])
        lmt = np.array([self.mus.get(i).getLength(self.s) for i in range(self.n)])
        vlmt = np.array([self.mus.get(i).getLengtheningSpeed(self.s) for i in range(self.n)])
        return q, qd, lmt, vlmt

    def kas_durumu(self):
        """Kas kasilma durumu: aktivasyon [0..1] ve tendon kuvveti [N].

        Aktivasyon bir durum degiskenidir (Thelen aktivasyon dinamigi cozer) ve dogrudan
        okunur; tendon kuvveti Dynamics asamasi ister. realizeDynamics'in ek maliyeti kosuda
        olculur; kuvvet kaydi pahali cikarsa cagiran taraf seyreltir."""
        self.model.realizeDynamics(self.s)
        akt = np.array([self.mus.get(i).getActivation(self.s) for i in range(self.n)])
        fk = np.array([self.mus.get(i).getTendonForce(self.s) for i in range(self.n)])
        return akt, fk

    def kas_indisleri(self, adlar):
        return [self.adlar.index(a) for a in adlar]
