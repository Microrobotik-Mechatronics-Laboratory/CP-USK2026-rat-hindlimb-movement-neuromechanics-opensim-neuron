# =============================================================================
# nrn_hucre.py — Kim 2020 motonoronunu Python'da, cok ornekli (havuz) kurulabilir bicimde kurar.
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru)
# Girdi: veri/kopru/moto_morfoloji.npz (morfoloji_cikar.py uretir)
# Cikti: MotoNoron ornekleri (her biri bagimsiz section kumesi)
#
# Neden Python'da kuruluyor: Kim'in v_e_moto6_export.hoc dosyasi global "create soma, dend[311]"
# kullaniyor, template degil; ayni morfolojiden 38 havuz icin cok hucre uretmeye elverisli degil.
# Kaynak dosyalara cerrahi mudahale etmek yerine morfoloji veri olarak okunur ve biyofizik burada,
# Kim'in hoc dosyalariyla AYNI SIRAYLA uygulanir. Sira onemlidir:
#   geometri -> baglanti -> pasif (Ra, cm) -> aktif -> kas bolmesi kablo ozelligi -> nseg (d_lambda)
# fixnseg.hoc:41-42 nseg'i en SONA birakir cunku d_lambda kurali Ra ve cm'e baglidir.
#
# Kaynaklar (hepsi neuron/fig2_4_6 altinda, degistirilmedi):
#   mem_mechanism_pass.hoc  pasif ozellikler
#   mem_mechanism_acti.hoc  soma / hillock / is aktif kanallari, celsius=36
#   mem_mechanism_muscle.hoc kas bolmesinin kablo ozelligi (g_pas=2e-3, cm=20)
#   fixnseg.hoc             d_lambda kurali (freq=100, d_lambda=0.1)
#   add_pics_istim.hoc      Cav1.3 PIC yerlesimi (dpath, gcalbar)
#   group_Ia.hoc            Ia sinaps dagilimi (soma + D_path<1400 um dendritler)
#
# BILINEN SAPMALAR:
# - kas_modulu=False (varsayilan) oldugunda muscle_unit bolmesi KURULUR ve kablo ozellikleri
#   (g_pas=2e-3, cm=20) verilir ama CaSP/fHill takilmaz. Bolme silinmez, cunku is(0)'a bagli ve
#   cm=20 tasiyor; silmek is uzerindeki elektriksel yuku degistirip atesleme esigini kaydirir.
#   Kapali donguda kas dinamigi OpenSim'dedir (PREPRINT 4.3 kural 1).
# - Kim'in hucresi KEDI motonoronudur; sican icin PIC-konum etkisi zayif cikabilir
#   (oz_kim2020 6.1, yazarin kendi uyarisi).
# =============================================================================
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))      # nrn_ortam icin
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # kod/yollar.py icin
import numpy as np
from nrn_ortam import h
from yollar import VERI_KOPRU

# --- Kim'in sabitleri (kaynak dosya ve satir numarasiyla) --------------------------------
CELSIUS   = 36.0          # mem_mechanism_acti.hoc:5
G_PAS     = 1.0/11000     # mem_mechanism_pass.hoc:7   [S/cm2]
G_PAS_SOMA= 1.0/225       # mem_mechanism_pass.hoc:14
E_PAS     = -70.0         # mem_mechanism_pass.hoc:8   [mV]
RA        = 70.0          # mem_mechanism_pass.hoc:9   [Ohm*cm]
CM        = 1.0           # mem_mechanism_pass.hoc:10  [uF/cm2]
G_PAS_KAS = 2e-3          # mem_mechanism_muscle.hoc:7
CM_KAS    = 20.0          # mem_mechanism_muscle.hoc:8
ENA, EK   = 50.0, -80.0   # mem_mechanism_acti.hoc
FREQ, D_LAMBDA = 100.0, 0.1   # fixnseg.hoc:16-17
IA_SINIR  = 1400.0        # group_Ia.hoc:15  [um] D_path siniri (Segev 1990 dagilimi)
GMAX_IA   = 9.3e-6        # group_Ia.hoc:8   [S/cm2] optimal kas boyu (xm = -8 mm)

# add_pics_istim.hoc:52-61 -- gcalbar, somaya ulasan etkin Ca akimi 22 nA'da sabit kalacak
# sekilde konuma gore ayarlanmistir (Kim Tablo 1).
GCALBAR_TABLO = {100: 1.57, 200: 1.14, 300: 1.21, 400: 1.25, 500: 1.28,
                 600: 1.37, 700: 1.39, 800: 1.95, 900: 2.80, 1000: 4.10}

_MORF = None


def _morfoloji():
    """Morfolojiyi bir kez okur ve onbellekte tutar (38 hucre icin 38 kez okumaya gerek yok)."""
    global _MORF
    if _MORF is None:
        d = np.load(VERI_KOPRU / 'moto_morfoloji.npz', allow_pickle=False)
        say = d['pt3d_sayi']
        kes = np.concatenate([[0], np.cumsum(say)])
        _MORF = dict(
            adlar=[str(a) for a in d['adlar']], ebeveyn=[str(a) for a in d['ebeveyn']],
            ebeveyn_x=d['ebeveyn_x'], cocuk_x=d['cocuk_x'], L=d['L'], diam=d['diam'],
            pt3d=[d['pt3d_duz'][kes[i]:kes[i + 1]] for i in range(len(say))],
        )
    return _MORF


def _lambda_f(sec, freq):
    """fixnseg.hoc:19-38'in birebir karsiligi: AC boy sabiti cinsinden section uzunlugu."""
    if sec.n3d() < 2:
        return 1e5 * np.sqrt(sec.diam / (4 * np.pi * freq * sec.Ra * sec.cm))
    x1, d1, lam = sec.arc3d(0), sec.diam3d(0), 0.0
    for i in range(1, sec.n3d()):
        x2, d2 = sec.arc3d(i), sec.diam3d(i)
        lam += (x2 - x1) / np.sqrt(d1 + d2)
        x1, d1 = x2, d2
    lam *= np.sqrt(2) * 1e-5 * np.sqrt(4 * np.pi * freq * sec.Ra * sec.cm)
    return sec.L / lam


class MotoNoron:
    """Kim 2020 alfa motonoronu. Her ornek kendi section kumesine sahiptir."""

    def __init__(self, ad, dpath=600.0, gmax_ia=GMAX_IA, kas_modulu=False):
        self.ad = ad
        h.celsius = CELSIUS
        m = _morfoloji()

        # --- 1) geometri: morfoloji dosyasindan gelen section'lar --------------------------
        self.sec = {}
        for i, orij in enumerate(m['adlar']):
            # "dend[7]" -> "dend7": Python tarafinda kose parantez ad icinde sorun cikarir
            ad_py = orij.replace('[', '').replace(']', '')
            s = h.Section(name=ad_py, cell=self)
            s.L, s.diam = float(m['L'][i]), float(m['diam'][i])
            p = m['pt3d'][i]
            if len(p):
                s.pt3dclear()
                for x, y, z, d in p:
                    s.pt3dadd(float(x), float(y), float(z), float(d))
            self.sec[orij] = s
        self.soma = self.sec['soma']
        self.dend = [self.sec['dend[%d]' % i] for i in range(311)]
        self.hillock, self.iseg = self.sec['hillock'], self.sec['is']
        self.muscle_unit = self.sec['muscle_unit']

        # hillock konik: add_hil_is.hoc:8-12. nseg ONCE, sonra diam(0:1)=13:3 (segment
        # merkezlerinde dogrusal ara deger). nseg'i asagida d_lambda kurali yeniden belirler;
        # diam degerleri o sirada NEURON tarafindan yeniden ara-degerlenir.
        self.hillock.nseg = 10
        for seg in self.hillock:
            seg.diam = 13.0 + (3.0 - 13.0) * seg.x

        # --- 2) baglanti ------------------------------------------------------------------
        for i, orij in enumerate(m['adlar']):
            eb = m['ebeveyn'][i]
            if eb:
                self.sec[orij].connect(self.sec[eb](float(m['ebeveyn_x'][i])),
                                       float(m['cocuk_x'][i]))

        # --- 3) pasif ozellikler (mem_mechanism_pass.hoc) ----------------------------------
        for s in self.sec.values():
            s.insert('pas')
            s.Ra, s.cm = RA, CM
            for seg in s:
                seg.pas.g, seg.pas.e = G_PAS, E_PAS
        for seg in self.soma:
            seg.pas.g = G_PAS_SOMA

        # --- 4) aktif kanallar (mem_mechanism_acti.hoc) ------------------------------------
        self.soma.insert('Naf'); self.soma.insert('KDr'); self.soma.insert('CaN')
        self.soma.insert('Ca_conc'); self.soma.insert('KCa')
        for seg in self.soma:
            seg.Naf.gnafbar, seg.KDr.gkdrbar = 0.71, 0.23
            seg.CaN.gcanbar, seg.KCa.gkcabar = 0.013, 0.0258
            seg.ena, seg.ek = ENA, EK
        for s in (self.iseg, self.hillock):
            s.insert('Naf'); s.insert('Nap'); s.insert('KDr')
            for seg in s:
                seg.Naf.gnafbar, seg.Nap.gnapbar, seg.KDr.gkdrbar = 2.7, 0.033e-3, 0.17
                seg.ena, seg.ek = ENA, EK

        # --- 5) kas bolmesinin kablo ozelligi (mem_mechanism_muscle.hoc:7-8) ---------------
        # Bolme her halukarda kurulur ve cm=20 verilir; CaSP/fHill yalniz kas_modulu=True ise.
        self.muscle_unit.cm = CM_KAS
        for seg in self.muscle_unit:
            seg.pas.g = G_PAS_KAS
        if kas_modulu:
            self.muscle_unit.insert('CaSP')
            self.muscle_unit.insert('fHill')

        # --- 6) nseg: d_lambda kurali (fixnseg.hoc:40-43) ---------------------------------
        self.soma(0.5).area()                      # 3B noktalarin diam'a yansimasini zorlar
        for s in self.sec.values():
            s.nseg = int((s.L / (D_LAMBDA * _lambda_f(s, FREQ)) + 0.9) / 2) * 2 + 1

        # --- 7) Cav1.3 PIC yerlesimi (add_pics_istim.hoc:14-67) ---------------------------
        self.dpath = dpath
        self.iCaL = self._pic_yerlestir(dpath)

        # --- 8) Ia sinapslari (group_Ia.hoc) ----------------------------------------------
        self.ia_bolmeleri = self._ia_yerlestir(gmax_ia)

    # -- PIC ------------------------------------------------------------------------------
    def _pic_yerlestir(self, dpath):
        """Somadan yol uzakligi dpath'e en yakin noktaya her dalda bir CaL nokta sureci koyar."""
        h.distance(0, self.soma(0))
        max_dist = max(h.distance(self.soma(0), seg)
                       for s in self.sec.values() for seg in s.allseg())
        gcal = GCALBAR_TABLO.get(int(round(dpath)))
        if gcal is None:
            raise ValueError('dpath=%s icin Kim Tablo 1 gcalbar degeri yok; taranabilir '
                             'degerler: %s' % (dpath, sorted(GCALBAR_TABLO)))
        pic = []
        for s in self.sec.values():
            bas, son = h.distance(self.soma(0), s(0)), h.distance(self.soma(0), s(1))
            if not (bas <= dpath < son):
                continue
            err_min, x_min = max_dist, 0.0
            for seg in s.allseg():
                err = abs(dpath - h.distance(self.soma(0), seg))
                if err_min > err:
                    err_min, x_min = err, seg.x
            x_min = 1e-4 if x_min == 0 else (0.9999 if x_min == 1 else x_min)
            p = h.CaL(s(x_min))
            # add_pics_istim.hoc:57 -- yogunluk [mS/cm2] -> nokta sureci mutlak degerine
            p.gcalbar = gcal * s(x_min).area() * (1e-4) ** 2 * 1e3
            pic.append(p)
        return pic

    # -- Ia sinapslari --------------------------------------------------------------------
    def _ia_yerlestir(self, gmax):
        """soma + D_path<1400 um dendritlere IaSyn takar; takilan bolmelerin listesini doner."""
        h.distance(0, self.soma(0))
        hedef = [self.soma]
        hedef += [d for d in self.dend if h.distance(self.soma(0), d(1)) < IA_SINIR]
        bolmeler = []
        for s in hedef:
            s.insert('IaSyn')
            for seg in s:
                seg.IaSyn.gmax = gmax
                bolmeler.append(seg)
        return bolmeler

    def ia_yaz(self, gmax):
        """Ia iletkenligini kosu sirasinda gunceller (kopru: r(t) -> gmax_IaSyn)."""
        for seg in self.ia_bolmeleri:
            seg.IaSyn.gmax = gmax

    # -- olcum --------------------------------------------------------------------------
    def ap_kaydet(self, esik=-40.0):
        """NetCon ile aksiyon potansiyeli zamanlarini kaydeder.
        Esik -40 mV: oz_fietkiewicz2023 3b. Baslangic segmenti (is) izlenir; AP orada dogar."""
        v = h.Vector()
        nc = h.NetCon(self.iseg(0.5)._ref_v, None, sec=self.iseg)
        nc.threshold = esik
        nc.record(v)
        self._nc = nc                      # cop toplayici silmesin
        return v

    def segment_sayisi(self):
        return sum(s.nseg for s in self.sec.values())
