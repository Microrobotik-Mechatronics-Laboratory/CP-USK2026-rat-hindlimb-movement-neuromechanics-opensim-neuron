# =============================================================================
# nrn_devre.py — omurilik devresinin NEURON tarafi: CPG yarim-merkezleri, oruntu olusturma
#                katmani (PF), resiprokal (IaIN) ve rekurren (Renshaw) inhibitor internoronlar.
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru)
# Kaynak mimari: PREPRINT bolum 6.1 diyagrami (literatur/diyagramlar/D2_omurilik_devresi.md)
#
# DURUM ETIKETLERI (PREPRINT 6.1 tablosu):
#   CPG yarim-merkezleri  [literaturden] mimari  -- oz_yu2021 3a (Morris-Lecar HCO)
#   Supraspinal tonik girdi [tasarim]
#   PF (oruntu olusturma) katmani [tasarim] -- gerekcesi KENDI olcumumuzdur (PREPRINT 6.4):
#       uc eklem farkli zamanlarda tepe yapiyor (kalca %68.5, diz %76.0, bilek %85.5);
#       tek fazli bir girdi bu gecikmeleri veremez.
#   IaIN (resiprokal inhibisyon)  [tasarim] -- literatur setinde KAYNAGI YOK
#   Renshaw (rekurren inhibisyon) [tasarim] -- literatur setinde KAYNAGI YOK
#
# DURUSTLUK NOTU (PREPRINT 6.1): IaIN ve Renshaw bu projenin literatur setinde kaynagi olmayan
# iki bilesendir. Kullanici karariyla ilk surumde DEVREDE tutuluyorlar ama hicbir sonuc
# bunlara dayandirilarak IDDIA EDILMEZ; her ciktida etiketleri tasinir.
#
# BAYRAKLAR:
# - Morris-Lecar parametreleri Aplysia olceginden gelir (oz_yu2021 Tablo 2); phin bu projede
#   yuruyus cevrimine kalibre edilir. Kalibrasyon degeri devre_par.json'dadir, koda gomulmez.
# - Internoronlar Kim'in kendi Naf/KDr mekanizmalariyla kurulur; yeni bir hucre modeli
#   uydurulmaz. Bu bir [tasarim] secimidir: internoron icin ayri bir kaynak yoktur.
# =============================================================================
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nrn_ortam import h


class MLHucre:
    """Morris-Lecar yarim-merkez hucresi (tek bolme). oz_yu2021 3a."""

    def __init__(self, ad, alan_um2=1000.0, **par):
        self.ad = ad
        self.sec = h.Section(name=ad, cell=self)
        # Tek bolme; L=diam secimi yalniz yuzey alanini belirler, ML denklemleri yogunluk
        # tabanlidir. Alan sinaptik iletkenligin (uS) yogunluga cevrilmesinde rol oynar.
        capr = (alan_um2 / 3.141592653589793) ** 0.5
        self.sec.L = self.sec.diam = capr
        self.sec.nseg = 1
        self.sec.cm = 1.0                      # oz_yu2021 Tablo 2: C = 1 uF/cm2
        self.sec.insert('MLhco')
        for k, v in par.items():
            setattr(self.sec(0.5).MLhco, k, v)

    def par(self, **kw):
        for k, v in kw.items():
            setattr(self.sec(0.5).MLhco, k, v)


class SpikeHucre:
    """Tek bolmeli aksiyon potansiyeli ureten internoron (PF, IaIN, Renshaw, II aktarim).
    Kim'in Naf/KDr mekanizmalarini kullanir; ayri bir hucre modeli uydurulmaz. [tasarim]"""

    def __init__(self, ad, alan_um2=1000.0, gnaf=0.35, gkdr=0.12, gpas=1.0 / 11000, epas=-70.0):
        self.ad = ad
        self.sec = h.Section(name=ad, cell=self)
        capr = (alan_um2 / 3.141592653589793) ** 0.5
        self.sec.L = self.sec.diam = capr
        self.sec.nseg, self.sec.cm, self.sec.Ra = 1, 1.0, 70.0
        self.sec.insert('pas'); self.sec.insert('Naf'); self.sec.insert('KDr')
        s = self.sec(0.5)
        s.pas.g, s.pas.e = gpas, epas
        s.Naf.gnafbar, s.KDr.gkdrbar = gnaf, gkdr
        s.ena, s.ek = 50.0, -80.0
        self.girdiler = []

    def sinaps(self, tau1=0.5, tau2=5.0, e=0.0):
        """Olay tabanli sinaps (NEURON yerlesigi Exp2Syn). e=0 eksitator, e=-80 inhibitor."""
        syn = h.Exp2Syn(self.sec(0.5))
        syn.tau1, syn.tau2, syn.e = tau1, tau2, e
        self.girdiler.append(syn)
        return syn

    def akim(self, amp=0.0):
        """Supraspinal tonik girdinin karsiligi: sabit akim. [tasarim]"""
        ic = h.IClamp(self.sec(0.5))
        ic.delay, ic.dur, ic.amp = 0.0, 1e9, amp
        self._ic = ic
        return ic

    def ap_kaydet(self, esik=-40.0):
        v = h.Vector()
        nc = h.NetCon(self.sec(0.5)._ref_v, None, sec=self.sec)
        nc.threshold = esik
        nc.record(v)
        self._nc = nc
        return v


def gradli_baglanti(once, sonra, gcpg_mscm2, esyn=-80.0, ethr=0.0, eslope=2.0):
    """Presinaptik voltaja bagli (aksiyon potansiyeli uretmeyen) sinaps: HCO karsilikli inhibisyonu. oz_yu2021 3c.

    BIRIM (kritik): oz_yu2021 Tablo 2'de gCPG, diger iletkenliklerle AYNI yogunluk birimindedir
    (mS/cm2). GradeSyn ise bir NOKTA surecidir ve uS ister. Donusum burada, tek yerde yapilir:
        gsyn[uS] = g[mS/cm2] * 1e-3 [S/cm2 basina] * alan[um2] * 1e-8 [cm2/um2] * 1e6 [uS/S]
                 = g[mS/cm2] * alan[um2] * 1e-5
    Bu donusum atlanirsa sinaps membranin toplam iletkenliginin ~40 katina cikar ve iki
    yarim-merkez de -80 mV'a cakilir (olculdu)."""
    alan = sonra.sec.L * 3.141592653589793 * sonra.sec.diam      # [um2], tek bolme
    syn = h.GradeSyn(sonra.sec(0.5))
    syn.gsyn = gcpg_mscm2 * alan * 1e-5
    syn.esyn, syn.ethr, syn.eslope = esyn, ethr, eslope
    h.setpointer(once.sec(0.5)._ref_v, 'vpre', syn)
    return syn


def hco(ad_f='RG_F', ad_e='RG_E', gcpg=0.008, phin=0.0005, iext=8e-4, ethr=0.0):
    """gcpg birimi mS/cm2'dir (oz_yu2021 Tablo 2 ile ayni)."""
    """Yarim-merkez cifti: iki ML hucresi + karsilikli gradli inhibisyon.
    Izole hucre kararli sabit noktadadir; salinim ancak bu inhibisyonla dogar (oz_yu2021 3b)."""
    f = MLHucre(ad_f, phin=phin, iext=iext)
    e = MLHucre(ad_e, phin=phin, iext=iext)
    sf = gradli_baglanti(f, e, gcpg, ethr=ethr)
    se = gradli_baglanti(e, f, gcpg, ethr=ethr)
    return dict(F=f, E=e, syn=(sf, se))


def par_oku(yol):
    """Sinaptik agirliklar ve kalibrasyon degerleri koda gomulmez; JSON'dan okunur."""
    with open(yol) as fh:
        return json.load(fh)
