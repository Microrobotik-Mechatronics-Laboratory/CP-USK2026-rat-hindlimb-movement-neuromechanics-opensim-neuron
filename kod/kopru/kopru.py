# =============================================================================
# kopru.py — NEURON (omurilik) ile OpenSim (kas-iskelet) arasindaki iki yonlu kopru.
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru) -- ikisi de AYNI surectedir
# Girdi:  kod/kopru/devre_par.json (parametreler), model + izgara (osim_mekanik uzerinden)
# Cikti:  Kopru nesnesi; kos() cagrisi zaman serilerini dondurur
#
# YONTEM: iki simulator tek Python denetim dongusunde AYNI zaman adimiyla eszamanli
# ilerletilir (oz_fietkiewicz2025 3b). PREPRINT bolum 8'in sozde-kodu:
#     her adimda: NEURON ilerlet -> dikenleri oku -> u(t) -> OpenSim'e yaz -> OpenSim ilerlet
#                 -> kas boyu/hizi oku -> igcikten r(t) -> gecikme -> Ia sinapsina yaz
#
# ==================== BIRIM VE ZAMAN SOZLESMESI (koprunun en kaygan yeri) ====================
#   buyukluk        NEURON        OpenSim       igcik fiti      donusum
#   zaman           ms            s             -               x1e-3
#   uzunluk         um            m             mm              x1e3
#   iletkenlik      S/cm2         -             -               -
#   kuvvet          -             N             -               -
#   oran            -             -             pps             -
# Kopru adimi dt_k = 0.3 ms. GEREKCE: 0.3 ms hem NEURON adiminin (0.025 ms) tam katidir
# (12 adim), hem Ia gecikmesinin (1.5 ms -> 5 adim) hem II gecikmesinin (1.8 ms -> 6 adim)
# tam bolenidir; gecikme yuvarlama hatasi SIFIR olur. Efferent gecikme 6 ms = 20 adim.
# =============================================================================================
#
# BAYRAKLAR:
# - r(t) -> gmax_IaSyn esleme [tasarim]: Kim'in uc capasi (gmax = 0 / 9.3e-6 / 19e-6 S/cm2,
#   xm = -16 / -8 / 0 mm) uzerinden dogrusal. gsc birimsiz olcektir; gsc=1 Kim'in optimal
#   boy degeridir, ust sinir 19/9.3 = 2.043'tur. PREPRINT 6.3'un uygulamasi.
# - diken -> u(t) [tasarim]: NetCon esigi -40 mV (oz_fietkiewicz2023 3b), ustel filtreyle
#   anlik atesleme orani, u = clip(f_MN/f_ref, 0, 1). f_ref oz_gorassini2000 bantlarindan.
# - IaIN ve Renshaw KAYNAKSIZ bilesenlerdir (PREPRINT 6.1); devrededirler ama hicbir sonuc
#   bunlara dayandirilarak iddia edilmez.
# =============================================================================
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from nrn_ortam import h                 # NEURON'u dogru dizinde ayaga kaldirir (chdir dahil)
import nrn_hucre, nrn_devre, igcik
from osim_mekanik import Mekanik
from yollar import R_KATSAYI, GRID3D

PAR_YOL = pathlib.Path(__file__).resolve().parent / 'devre_par.json'
GMAX_IA_KIM = (0.0, 9.3e-6, 19e-6)      # group_Ia.hoc:7-9 -- xm = -16 / -8 / 0 mm capalari
GSC_UST = GMAX_IA_KIM[2] / GMAX_IA_KIM[1]   # 2.043


class Gecikme:
    """Halka tamponu: kopru cozunurlugunde tam sayi adim gecikmesi (yuvarlama hatasi yok)."""

    def __init__(self, adim, boyut, baslangic=0.0):
        self.n = max(1, int(adim))
        self.buf = np.full((self.n, boyut), float(baslangic))
        self.i = 0

    def gecir(self, x):
        cikan = self.buf[self.i].copy()
        self.buf[self.i] = x
        self.i = (self.i + 1) % self.n
        return cikan


class Havuz:
    """Bir kasin motonoron havuzu. Ilk surumde havuz basina bir temsili hucre (PREPRINT 6.4)."""

    def __init__(self, kas, f_ref, dpath=600.0):
        self.kas = kas
        self.f_ref = float(f_ref)
        self.hucre = nrn_hucre.MotoNoron('MN_' + kas, dpath=dpath, kas_modulu=False)
        # Ia sinapsini kopru surumuyle degistir: gmax sabit kalir, olcek gsc disaridan yazilir
        self.gsc = h.Vector(1)
        self.gsc.x[0] = 0.0
        self._ia_koprule()
        self.dikenler = self.hucre.diken_kaydet()
        self.n_diken = 0
        self.f = 0.0                     # ustel filtreli anlik atesleme orani [Hz]

    def _ia_koprule(self):
        """Kim'in tonik IaSyn'i yerine POINTER'li IaKopru: adim basina TEK yazma."""
        for s in {seg.sec for seg in self.hucre.ia_bolmeleri}:
            s.uninsert('IaSyn')
            s.insert('IaKopru')
            for seg in s:
                seg.IaKopru.gmax = GMAX_IA_KIM[1]
                h.setpointer(self.gsc._ref_x[0], 'gsc', seg.IaKopru)

    def ia_yaz(self, gsc):
        self.gsc.x[0] = float(gsc)

    def oran_guncelle(self, dt_ms, tau_ms):
        """Diken sayacindan ustel filtreli anlik atesleme orani. NetCon kaydi birikimlidir."""
        yeni = len(self.dikenler) - self.n_diken
        self.n_diken += yeni
        anlik = yeni / (dt_ms * 1e-3)                 # bu adimdaki diken -> Hz
        a = dt_ms / tau_ms
        self.f += a * (anlik - self.f)
        return self.f

    def u(self):
        return min(1.0, max(0.0, self.f / self.f_ref))


class Kopru:
    """Kapali dongu: CPG -> PF -> havuzlar -> u(t) -> OpenSim -> igcik -> Ia/II -> geri."""

    def __init__(self, gruplar, serbest, par_yol=PAR_YOL, dpath=600.0):
        """gruplar: {'DF': ['TA','EDL','Per'], 'PF': ['Sol', ...]} -- antagonist cift adlari
        serbest:  OpenSim'de serbest birakilacak koordinatlar"""
        with open(par_yol) as fh:
            self.par = json.load(fh)
        kp = self.par['kopru']
        self.dt_ms = kp['dt_kopru_ms']
        self.dt_s = self.dt_ms * 1e-3
        h.dt = kp['dt_neuron_ms']
        assert abs(self.dt_ms / h.dt - round(self.dt_ms / h.dt)) < 1e-12, \
            'kopru adimi NEURON adiminin tam kati olmali'

        self.gruplar = {g: list(k) for g, k in gruplar.items()}
        self.kaslar = [k for g in self.gruplar.values() for k in g]
        self._grup_ix = {g: [self.kaslar.index(x) for x in k] for g, k in self.gruplar.items()}
        self.ii_olcek = 1e-4     # [tasarim] pps -> nA; II aktarim internoronunun surus olcegi

        # --- mekanik ---------------------------------------------------------------------
        self.mek = Mekanik(serbest=serbest, dt_kopru_s=self.dt_s)
        self.ix = self.mek.kas_indisleri(self.kaslar)          # 38'lik dizide bizim kaslar
        g = np.load(GRID3D, allow_pickle=True)
        adlar_izg = [str(x) for x in g['names']]
        jx = [adlar_izg.index(k) for k in self.kaslar]
        self.tsl, self.lmo, self.alp = g['tsl'][jx], g['lmo'][jx], g['alp'][jx]
        lm_min_hep, _ = igcik.lm_min_izgaradan(GRID3D)
        self.lm_min = lm_min_hep[jx]
        self.igcik = igcik.Igcik(R_KATSAYI, self.lm_min, k_ia=kp['k_ia'])

        # Ia -> gsc capasi [tasarim]: Kim'in "optimal boy" degeri gsc=1'e denk gelsin.
        # Optimal boy, uzama araliginin ortasi kabul edilir; oradaki DURAGAN Ia orani capadir.
        d_maks = (g['LM'].reshape(-1, len(adlar_izg)).max(0) * 1000.0)[jx] - self.lm_min
        self.r_capa = self.igcik.b + self.igcik.kL * (d_maks / 2.0)

        # --- antagonist denge olcegi ------------------------------------------------------
        # Iki grubun eklem uzerindeki maksimum moment kapasitesi esit DEGILDIR (olculdu:
        # bilekte plantar fleksorler dorsifleksorlerin 2.6-5.3 kati). Esit CPG surusu verilirse
        # eklem gucli grubun ucuna coker ve orada kalir. Merkezi sinir sistemi bu dengesizligi
        # surus dagilimiyla cozer; burada karsiligi, grup surusunun moment kapasitesiyle ters
        # olceklenmesidir. [tasarim] -- olculen kapasiteler kosum ciktisina yazilir.
        self.kapasite = self._kapasite_olc(self.par['sinaps'].get('denge_pozu_derece', 14.0))
        c_ref = min(self.kapasite.values())
        self.denge = {g: c_ref / self.kapasite[g] for g in self.kapasite}

        # --- devre -----------------------------------------------------------------------
        self._devre_kur(kp, dpath)

        # --- gecikmeler ------------------------------------------------------------------
        n = len(self.kaslar)
        self.g_ia = Gecikme(round(kp['gecikme_ia_ms'] / self.dt_ms), n)
        self.g_ii = Gecikme(round(kp['gecikme_ii_ms'] / self.dt_ms), n)
        self.g_ef = Gecikme(round(kp['gecikme_efferent_ms'] / self.dt_ms), n)
        for ad, gc in (('Ia', self.g_ia), ('II', self.g_ii), ('efferent', self.g_ef)):
            assert gc.n >= 1, '%s gecikmesi kopru adimindan kucuk' % ad

    def _kapasite_olc(self, poz_derece):
        """Grup basina |sum(Fmax * moment kolu)| [N*mm], verilen eklem pozunda."""
        import opensim as osim   # noqa: F401 -- osim_mekanik zaten yukledi
        koord = self.mek.koord[self.mek.serbest[0]]
        eski = koord.getValue(self.mek.s)
        koord.setValue(self.mek.s, np.radians(poz_derece))
        self.mek.model.realizePosition(self.mek.s)
        kap = {}
        for gad, kaslar in self.gruplar.items():
            s = 0.0
            for kas in kaslar:
                mu = self.mek.mus.get(self.mek.adlar.index(kas))
                s += mu.getMaxIsometricForce() * mu.computeMomentArm(self.mek.s, koord)
            kap[gad] = abs(s) * 1000.0
        koord.setValue(self.mek.s, eski)
        self.mek.model.realizePosition(self.mek.s)
        return kap

    # -- devre kurulumu -------------------------------------------------------------------
    def _devre_kur(self, kp, dpath):
        c, i_p, s_p = self.par['cpg'], self.par['internoron'], self.par['sinaps']
        ir = self.par['iain_renshaw']
        eks, inh, ag = s_p['eksitator'], s_p['inhibitor'], s_p['agirlik_uS']
        self.cpg = nrn_devre.hco(gcpg=c['gcpg_mScm2'], phin=c['phin_per_ms'],
                                 iext=c['iext_mAcm2'], ethr=c['ethr_mV'])
        gadlar = list(self.gruplar)
        assert len(gadlar) == 2, 'ilk surum tek antagonist cift icindir'
        self.pf, self.iain, self.renshaw, self.ii_rly = {}, {}, {}, {}
        self.havuz = {}
        # KRITIK: NEURON nesneleri Python tarafinda referans tutulmazsa cop toplayici siler ve
        # sinaps SESSIZCE yok olur (olculdu: CPG -> PF surusu kayboldu, PF hic ateslemedi,
        # tum motonoronlar sustu). Her NetCon, Exp2Syn ve GradeSyn burada tutulur.
        self._nc = []
        self._gsyn = []

        rg = {gadlar[0]: self.cpg['F'], gadlar[1]: self.cpg['E']}
        for gad in gadlar:
            ip = lambda ad: nrn_devre.SpikeHucre(ad, alan_um2=i_p['alan_um2'],
                                                 gnaf=i_p['gnaf_Scm2'], gkdr=i_p['gkdr_Scm2'],
                                                 gpas=i_p['gpas_Scm2'], epas=i_p['epas_mV'])
            self.pf[gad] = ip('PF_' + gad)
            self.ii_rly[gad] = ip('IIrly_' + gad)
            self.ii_rly[gad].akim(0.0)      # tonik akim bir kez kurulur; amp adim basina yazilir
            if ir['iain_etkin']:
                self.iain[gad] = ip('IaIN_' + gad)
            if ir['renshaw_etkin']:
                self.renshaw[gad] = ip('RC_' + gad)
            # CPG -> PF: gradli eksitasyon (RG bir ML hucresi, diken uretmez)
            self._gsyn.append(nrn_devre.gradli_baglanti(
                rg[gad], self.pf[gad], c['gcpg_mScm2'] * self.par['sinaps']['cpg_pf_carpan'],
                esyn=eks['e_mV'], ethr=c['ethr_mV'], eslope=c['eslope_mV']))
            for kas in self.gruplar[gad]:
                fr = kp['f_ref_Hz'].get(kas, kp['f_ref_Hz']['varsayilan'])
                self.havuz[kas] = Havuz(kas, fr, dpath=dpath)

        # PF -> havuz (eksitator), havuz -> Renshaw -> havuz (rekurren inhibisyon),
        # PF -> IaIN -> karsi havuz (resiprokal inhibisyon), II aktarim -> havuz + CPG
        for gi, gad in enumerate(gadlar):
            karsi = gadlar[1 - gi]
            for kas in self.gruplar[gad]:
                hv = self.havuz[kas]
                self._eks(self.pf[gad], hv.hucre.soma(0.5), eks, ag['pf_mn'] * self.denge[gad])
                self._eks(self.ii_rly[gad], hv.hucre.soma(0.5), eks, ag['ii_mn'])
                if ir['renshaw_etkin']:
                    self._eks_h(hv, self.renshaw[gad], eks, ag['mn_rc'])
                    self._inh(self.renshaw[gad], hv.hucre.soma(0.5), inh, ag['rc_mn'])
                if ir['iain_etkin']:
                    self._inh(self.iain[karsi], hv.hucre.soma(0.5), inh, ag['iain_mn'])
            if ir['iain_etkin']:
                self._eks(self.pf[gad], self.iain[gad].sec(0.5), eks, ag['pf_iain'])
            # II -> CPG geri besleme kolu (gFB): oz_yu2021'in gFB/gCPG odunlesimi
            self._gsyn.append(nrn_devre.gradli_baglanti(
                self.ii_rly[gad], rg[gad], c['gcpg_mScm2'] * self.par['sinaps']['gfb_carpan'],
                esyn=eks['e_mV'], ethr=-20.0, eslope=c['eslope_mV']))

    def _syn(self, hedef_seg, par):
        syn = h.Exp2Syn(hedef_seg)
        syn.tau1, syn.tau2, syn.e = par['tau1_ms'], par['tau2_ms'], par['e_mV']
        return syn

    def _eks(self, once_hucre, hedef_seg, par, agirlik):
        syn = self._syn(hedef_seg, par)
        nc = h.NetCon(once_hucre.sec(0.5)._ref_v, syn, sec=once_hucre.sec)
        nc.threshold, nc.weight[0], nc.delay = -40.0, agirlik, 0.5
        self._nc.append((nc, syn))
        return nc

    def _inh(self, once_hucre, hedef_seg, par, agirlik):
        return self._eks(once_hucre, hedef_seg, par, agirlik)

    def _eks_h(self, havuz, hedef_hucre, par, agirlik):
        """Motonoron -> internoron (Renshaw): kaynak bir MotoNoron nesnesidir."""
        syn = self._syn(hedef_hucre.sec(0.5), par)
        nc = h.NetCon(havuz.hucre.iseg(0.5)._ref_v, syn, sec=havuz.hucre.iseg)
        nc.threshold, nc.weight[0], nc.delay = -40.0, agirlik, 0.5
        self._nc.append((nc, syn))
        return nc

    # -- kosum ----------------------------------------------------------------------------
    def kos(self, sure_s, ilerleme=None):
        kp = self.par['kopru']
        nadim = int(round(sure_s / self.dt_s))
        nk = len(self.kaslar)
        q, qd, lmt, vlmt = self.mek.baslat()
        h.finitialize(-70.0)
        # CPG'yi izole sabit noktasina yakin baslat ve simetriyi kir (yoksa salinim dogmaz)
        self.cpg['F'].sec(0.5).v = 13.3
        self.cpg['E'].sec(0.5).v = 10.0

        iz = dict(t=np.zeros(nadim), q=np.zeros((nadim, len(self.mek.serbest))),
                  u=np.zeros((nadim, nk)), Ia=np.zeros((nadim, nk)), II=np.zeros((nadim, nk)),
                  f=np.zeros((nadim, nk)), gsc=np.zeros((nadim, nk)),
                  vF=np.zeros(nadim), vE=np.zeros(nadim))

        for k in range(nadim):
            # 1) mekanikten duyu: kas-tendon boyu/hizi -> lif boyu/hizi -> Ia, II
            lm, cosa = igcik.lif_boyu(lmt[self.ix], self.tsl, self.lmo, self.alp)
            vlm = igcik.lif_hizi(vlmt[self.ix], cosa)
            ia, ii = self.igcik(lm * 1000.0, vlm * 1000.0)

            # 2) iletim gecikmesi (tam sayi adim), sonra Ia -> gmax olcegi
            ia_g, ii_g = self.g_ia.gecir(ia), self.g_ii.gecir(ii)
            gsc = np.clip(ia_g / self.r_capa, 0.0, GSC_UST)
            for j, kas in enumerate(self.kaslar):
                self.havuz[kas].ia_yaz(gsc[j])
            # II aktarim internoronuna tonik akim olarak (pps -> nA, [tasarim] olcek)
            for gad, hcr in self.ii_rly.items():
                hcr._ic.amp = float(np.mean(ii_g[self._grup_ix[gad]])) * self.ii_olcek

            # 3) NEURON'u bir kopru adimi ilerlet
            h.continuerun(h.t + self.dt_ms)

            # 4) dikenlerden u(t), sonra efferent gecikme
            f = np.array([self.havuz[k2].oran_guncelle(self.dt_ms, kp['u_filtre_tau_ms'])
                          for k2 in self.kaslar])
            u_ham = np.array([self.havuz[k2].u() for k2 in self.kaslar])
            u = self.g_ef.gecir(u_ham)

            # 5) OpenSim'e yaz ve bir kopru adimi ilerlet
            tam_u = np.zeros(self.mek.n)
            tam_u[self.ix] = u
            self.mek.uyarim_yaz(tam_u)
            q, qd, lmt, vlmt = self.mek.adim()

            iz['t'][k] = (k + 1) * self.dt_s
            iz['q'][k], iz['u'][k], iz['Ia'][k], iz['II'][k] = q, u, ia, ii
            iz['f'][k], iz['gsc'][k] = f, gsc
            iz['vF'][k] = self.cpg['F'].sec(0.5).v
            iz['vE'][k] = self.cpg['E'].sec(0.5).v
            if ilerleme and (k + 1) % ilerleme == 0:
                print('  adim %6d/%d  t=%.3f s  q=%.1f derece  u_max=%.3f'
                      % (k + 1, nadim, iz['t'][k], np.degrees(q[0]), u.max()), flush=True)
        return iz
