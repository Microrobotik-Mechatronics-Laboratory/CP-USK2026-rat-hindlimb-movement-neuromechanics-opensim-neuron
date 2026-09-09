# =============================================================================
# kopru.py — NEURON (omurilik) ile OpenSim (kas-iskelet) arasindaki iki yonlu kopru.
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru) -- ikisi de AYNI surectedir
# Girdi:  kod/kopru/devre_par.json (parametreler), model + izgara (osim_mekanik uzerinden)
# Cikti:  Kopru nesnesi; kos() cagrisi zaman serilerini dondurur
#
# YONTEM: iki simulator tek Python denetim dongusunde AYNI zaman adimiyla eszamanli
# ilerletilir (oz_fietkiewicz2025 3b). PREPRINT bolum 8'in sozde-kodu:
#     her adimda: NEURON ilerlet -> aksiyon potansiyellerini oku -> u(t) -> OpenSim'e yaz -> OpenSim ilerlet
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
# BILINEN SAPMALAR:
# - r(t) -> gmax_IaSyn esleme [tasarim]: Kim'in uc capasi (gmax = 0 / 9.3e-6 / 19e-6 S/cm2,
#   xm = -16 / -8 / 0 mm) uzerinden dogrusal. gsc birimsiz olcektir; gsc=1 Kim'in optimal
#   boy degeridir, ust sinir 19/9.3 = 2.043'tur. PREPRINT 6.3'un uygulamasi.
# - aksiyon potansiyeli -> u(t) [tasarim]: NetCon esigi -40 mV (oz_fietkiewicz2023 3b), ustel filtreyle
#   anlik atesleme orani, u = clip(f_MN/f_ref, 0, 1). f_ref oz_gorassini2000 araliklarindan.
# - IaIN ve Renshaw KAYNAKSIZ bilesenlerdir (PREPRINT 6.1); devrededirler ama hicbir sonuc
#   bunlara dayandirilarak iddia edilmez.
# - hucre.d_lambda [tasarim]: motonoronun uzamsal cozunurlugu. Kim'in degeri 0.1; kabalastirma
#   maliyeti ve PIC duzeltmesi nrn_hucre.py basliginda olculmus sayilarla anlatilir, sinamasi
#   kod/kopru/uzamsal_yakinsama.py'dedir.
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

    def __init__(self, kas, f_ref, dpath=600.0, d_lambda=nrn_hucre.D_LAMBDA,
                 pic_ref_d_lambda=nrn_hucre.D_LAMBDA):
        self.kas = kas
        self.f_ref = float(f_ref)
        self.hucre = nrn_hucre.MotoNoron('MN_' + kas, dpath=dpath, kas_modulu=False,
                                         d_lambda=d_lambda, pic_ref_d_lambda=pic_ref_d_lambda)
        # Ia sinapsini kopru surumuyle degistir: gmax sabit kalir, olcek gsc disaridan yazilir
        self.gsc = h.Vector(1)
        self.gsc.x[0] = 0.0
        self._ia_koprule()
        self.ap_zamanlari = self.hucre.ap_kaydet()
        self.n_ap = 0
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
        """Aksiyon potansiyeli sayacindan ustel filtreli anlik atesleme orani. NetCon kaydi birikimlidir."""
        yeni = len(self.ap_zamanlari) - self.n_ap
        self.n_ap += yeni
        anlik = yeni / (dt_ms * 1e-3)                 # bu adimdaki aksiyon potansiyeli -> Hz
        a = dt_ms / tau_ms
        self.f += a * (anlik - self.f)
        return self.f

    def u(self):
        return min(1.0, max(0.0, self.f / self.f_ref))


class Kopru:
    """Kapali dongu: CPG -> PF -> havuzlar -> u(t) -> OpenSim -> igcik -> Ia/II -> geri."""

    def __init__(self, gruplar=None, serbest=('ankle_flx',), par_yol=PAR_YOL, dpath=600.0):
        """gruplar: {'DF': ['TA','EDL','Per'], 'PF': ['Sol', ...]} -- tek eklemli antagonist
        cift (eski bicim; ilk grup RG-F'e, ikinci RG-E'ye baglanir). None verilirse eslesme
        devre_par.json'daki havuz_eslesme'den kurulur: 6 PF grubu + surussuz kaslar (38 havuz).
        serbest:  OpenSim'de serbest birakilacak koordinatlar"""
        with open(par_yol) as fh:
            self.par = json.load(fh)
        kp = self.par['kopru']
        self.dt_ms = kp['dt_kopru_ms']
        self.dt_s = self.dt_ms * 1e-3
        h.dt = kp['dt_neuron_ms']
        assert abs(self.dt_ms / h.dt - round(self.dt_ms / h.dt)) < 1e-12, \
            'kopru adimi NEURON adiminin tam kati olmali'

        # --- grup tanimlarini normalize et ------------------------------------------------
        # Ic temsil: grup_tanim[gad] = {kaslar, rg (F/E), koordinat, eklem}. Eski iki-gruplu
        # bicim tek eklemin ozel halidir; davranisi birebir korunur (regresyon guvencesi).
        if gruplar is not None:
            gadlar = list(gruplar)
            assert len(gadlar) == 2, 'eski bicim tek antagonist cift icindir'
            self.grup_tanim = {
                gadlar[0]: dict(kaslar=list(gruplar[gadlar[0]]), rg='F',
                                koordinat=serbest[0], eklem='e0'),
                gadlar[1]: dict(kaslar=list(gruplar[gadlar[1]]), rg='E',
                                koordinat=serbest[0], eklem='e0')}
            self.surussuz = []
            self.denge_pozlari = {serbest[0]: self.par['sinaps'].get('denge_pozu_derece', 14.0)}
        else:
            he = self.par['havuz_eslesme']
            self.grup_tanim = {gad: dict(kaslar=list(g['kaslar']), rg=g['rg'],
                                         koordinat=g['koordinat'], eklem=g['eklem'])
                               for gad, g in he['gruplar'].items()}
            self.surussuz = list(he['surussuz'])
            self.denge_pozlari = {k: float(v) for k, v in he['denge_pozu_derece'].items()}
            for gad, g in self.grup_tanim.items():
                assert g['koordinat'] in serbest, \
                    '%s grubunun koordinati (%s) serbest degil' % (gad, g['koordinat'])

        self.gruplar = {gad: list(g['kaslar']) for gad, g in self.grup_tanim.items()}
        # kas listesi: gruplardaki ilk gorunum sirasi + surussuzler sonda; biartikuler tek kez
        self.kaslar = []
        for g in self.grup_tanim.values():
            for kas in g['kaslar']:
                if kas not in self.kaslar:
                    self.kaslar.append(kas)
        self.kaslar += [k for k in self.surussuz if k not in self.kaslar]
        # uyelik: kas kac PF grubunda? Biartikuler kasin HER PF baglantisi biartikuler_pay
        # carpaniyla olceklenir [tasarim]. Ilk deger 0.5 (=1/uyelik) idi; olculdu (07.09.2026,
        # 0.5 s kosu): biartikulerlerin iki PF'i ZIT fazli oldugu icin girdiler ust uste
        # binmiyor ve 0.5 pay kasi hicbir fazda esik ustune cikaramiyor (MG/LG/Pla/GP/GA
        # 0 Hz) -- Gorassini MG/LG hedefi (67 Hz) ile celisir. Pay bu yuzden parametredir
        # ve kalibrasyonda taranir; deger devre_par.havuz_eslesme.biartikuler_pay'dadir.
        self.uyelik = {}
        for gad, g in self.grup_tanim.items():
            for kas in g['kaslar']:
                self.uyelik.setdefault(kas, []).append(gad)
        pay_c = float(self.par.get('havuz_eslesme', {}).get('biartikuler_pay', 0.5))
        self.pay = {kas: (pay_c if len(gr) > 1 else 1.0) for kas, gr in self.uyelik.items()}
        self._grup_ix = {g: [self.kaslar.index(x) for x in k] for g, k in self.gruplar.items()}
        self.ii_olcek = 1e-4     # [tasarim] pps -> nA; II aktarim internoronunun surus olcegi

        # --- mekanik ---------------------------------------------------------------------
        # Yeni modda (38 havuz / 3 DOF) serbest koordinatlara izgara tanim alaninda limit
        # kuvveti eklenir; eski ayak bilegi modu limitsiz kalir (davranis birebir korunur).
        g = np.load(GRID3D, allow_pickle=True)
        limitler = None
        if gruplar is None:
            # izgara ucundan 1 derece iceri: tam ucta kas sarma geometrisi kotu kosullu
            # (olculdu -- osim_mekanik.py sinir notu, madde 2)
            eksen = {'hip_flx': 'HIP', 'knee_flx': 'KNE', 'ankle_flx': 'ANK'}
            limitler = {ad: (float(np.degrees(g[eksen[ad]][0])) + 1.0,
                             float(np.degrees(g[eksen[ad]][-1])) - 1.0)
                        for ad in serbest}
        self.limitler = limitler or {}
        self.mek = Mekanik(serbest=serbest, dt_kopru_s=self.dt_s, limitler=limitler)
        self.ix = self.mek.kas_indisleri(self.kaslar)          # 38'lik dizide bizim kaslar
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
        # olceklenmesidir. [tasarim] -- olculen kapasiteler kosu ciktisina yazilir.
        # Cok eklemde denge EKLEM ICINDE kurulur: her eklemin antagonist cifti kendi
        # koordinatindaki kapasiteyle olceklenir. Kapasite grubun KENDI uyelerinden hesaplanir;
        # capraz eklem (isaretli) surumu denendi ve olculerek reddedildi -- _kapasite_olc.
        self.kapasite = self._kapasite_olc(self.denge_pozlari)
        self.denge = {}
        for eklem in {g['eklem'] for g in self.grup_tanim.values()}:
            uye = [gad for gad, g in self.grup_tanim.items() if g['eklem'] == eklem]
            c_ref = min(self.kapasite[gad] for gad in uye)
            for gad in uye:
                self.denge[gad] = c_ref / self.kapasite[gad]

        # --- devre -----------------------------------------------------------------------
        self._devre_kur(kp, dpath)

        # --- gecikmeler ------------------------------------------------------------------
        n = len(self.kaslar)
        self.g_ia = Gecikme(round(kp['gecikme_ia_ms'] / self.dt_ms), n)
        self.g_ii = Gecikme(round(kp['gecikme_ii_ms'] / self.dt_ms), n)
        self.g_ef = Gecikme(round(kp['gecikme_efferent_ms'] / self.dt_ms), n)
        for ad, gc in (('Ia', self.g_ia), ('II', self.g_ii), ('efferent', self.g_ef)):
            assert gc.n >= 1, '%s gecikmesi kopru adimindan kucuk' % ad

    def _kapasite_olc(self, pozlar_derece):
        """Grup basina |sum(Fmax * moment kolu)| [N*mm], grubun KENDI uyeleri ve KENDI
        koordinatina gore.

        CAPRAZ EKLEM SURUMU DENENDI VE OLCULEREK REDDEDILDI (07.09.2026, DOGRULAMA R):
        "ayni RG fazinda surulen butun kaslarin bu eklemdeki ISARETLI moment toplami"
        tanimi denendi. Sonuc patolojik: kalca_flx kapasitesi 229.3 -> 18.0 N*mm'ye
        cokuyor, cunku F fazinda surulen hamstringlerin kalca EKSTANSIYON kollari ayni
        fazdaki hip fleksorlerini goturuyor. Denge bunu "F fazi zayif" diye okuyup
        kalca_ext'i 0.552 -> 0.088'e kisiyor ve kalca tek yonde doyup sinira dayaniyor
        (olculdu: 0.09 s'te hip 37.2 -> 65.9 derece monoton, u_max=1.0, integrator stall).
        Ders: ISARETLI net moment bir KAPASITE olcusu degildir; birbirini goturen iki kas
        "kapasitesiz" degildir. Denge olcegi grubun kendi cekme gucune bakmalidir.

        Biartikuler kasin oteki eklemde urettigi moment bu olcuye girmez; o etki mekanikte
        zaten vardir (moment kolu matrisi tasir) ve fizyolojik olarak da gercektir.

        pozlar_derece: {koordinat: derece} -- serbest koordinatlarin tamami olcum pozuna
        (olculmus yuruyus orta noktasi) kurulur, olcum bittikten sonra geri alinir. Boylece
        biartikuler kasin her iki eklemdeki kolu ayni gercekci pozda olculur."""
        import opensim as osim   # noqa: F401 -- osim_mekanik zaten yukledi
        eski = {ad: self.mek.koord[ad].getValue(self.mek.s) for ad in self.mek.serbest}
        for ad, derece in pozlar_derece.items():
            self.mek.koord[ad].setValue(self.mek.s, np.radians(derece))
        self.mek.model.realizePosition(self.mek.s)
        kap = {}
        for gad, g in self.grup_tanim.items():
            koord = self.mek.koord[g['koordinat']]
            s = 0.0
            for kas in g['kaslar']:
                mu = self.mek.mus.get(self.mek.adlar.index(kas))
                s += mu.getMaxIsometricForce() * mu.computeMomentArm(self.mek.s, koord)
            kap[gad] = abs(s) * 1000.0
        for ad, v in eski.items():
            self.mek.koord[ad].setValue(self.mek.s, v)
        self.mek.model.realizePosition(self.mek.s)
        return kap

    # -- devre kurulumu -------------------------------------------------------------------
    def _devre_kur(self, kp, dpath):
        c, i_p, s_p = self.par['cpg'], self.par['internoron'], self.par['sinaps']
        ir = self.par['iain_renshaw']
        eks, inh, ag = s_p['eksitator'], s_p['inhibitor'], s_p['agirlik_uS']
        self.cpg = nrn_devre.hco(gcpg=c['gcpg_mScm2'], phin=c['phin_per_ms'],
                                 iext=c['iext_mAcm2'], ethr=c['ethr_mV'])
        gadlar = list(self.grup_tanim)
        self.pf, self.iain, self.renshaw, self.ii_rly = {}, {}, {}, {}
        self.havuz = {}
        # KRITIK: NEURON nesneleri Python tarafinda referans tutulmazsa cop toplayici siler ve
        # sinaps SESSIZCE yok olur (olculdu: CPG -> PF surusu kayboldu, PF hic ateslemedi,
        # tum motonoronlar sustu). Her NetCon, Exp2Syn ve GradeSyn burada tutulur.
        self._nc = []
        self._gsyn = []
        self._in_spk = {}                    # internoron spike kayitlari (raster icin)

        # ayni eklemin karsi grubu (resiprokal inhibisyon cifti)
        self.karsi = {}
        for gad, g in self.grup_tanim.items():
            es = [x for x, gg in self.grup_tanim.items()
                  if gg['eklem'] == g['eklem'] and x != gad]
            assert len(es) == 1, 'eklem %s icin antagonist cift kurulamadi' % g['eklem']
            self.karsi[gad] = es[0]
        n_eklem = len({g['eklem'] for g in self.grup_tanim.values()})

        # gFB kolu eklemlere bolunur: her IIrly -> RG baglantisi gcpg*gfb_carpan/n_eklem tasir,
        # boylece toplam gFB tek eklemli kurulumla ayni olcekte kalir (oz_yu2021 odunlesimi
        # korunur) [tasarim]. Eski modda n_eklem=1 -> birebir ayni davranis.
        rg = {gad: self.cpg[g['rg']] for gad, g in self.grup_tanim.items()}

        # havuzlar: kas basina BIR kez (biartikuler kas iki grupta uyedir ama tek havuzdur);
        # surussuz kaslarin havuzu da kurulur, yalniz PF/II/RC/IaIN baglantisi almazlar.
        # Uzamsal cozunurluk [tasarim] -- koda gomulmez, devre_par.hucre'den okunur. Blok
        # yoksa Kim'in degeri (0.1) kullanilir, yani eski kosularla karsilastirma bozulmaz.
        # PIC iletkenliginin cozunurlukten bagimsiz tutulmasi nrn_hucre basliginda anlatilir.
        hp = self.par.get('hucre', {})
        self.d_lambda = float(hp.get('d_lambda', nrn_hucre.D_LAMBDA))
        self.pic_ref_d_lambda = float(hp.get('pic_referans_d_lambda', nrn_hucre.D_LAMBDA))
        for kas in self.kaslar:
            fr = kp['f_ref_Hz'].get(kas, kp['f_ref_Hz']['varsayilan'])
            self.havuz[kas] = Havuz(kas, fr, dpath=dpath, d_lambda=self.d_lambda,
                                    pic_ref_d_lambda=self.pic_ref_d_lambda)

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
            # CPG -> PF: gradli eksitasyon (RG bir ML hucresi, aksiyon potansiyeli uretmez)
            self._gsyn.append(nrn_devre.gradli_baglanti(
                rg[gad], self.pf[gad], c['gcpg_mScm2'] * self.par['sinaps']['cpg_pf_carpan'],
                esyn=eks['e_mV'], ethr=c['ethr_mV'], eslope=c['eslope_mV']))

        # PF -> havuz (eksitator), havuz -> Renshaw -> havuz (rekurren inhibisyon),
        # PF -> IaIN -> karsi havuz (resiprokal inhibisyon), II aktarim -> havuz + CPG.
        # Biartikuler kas her uye grubuyla baglanir; agirliklar pay=1/uyelik ile olceklenir.
        for gad in gadlar:
            karsi = self.karsi[gad]
            for kas in self.gruplar[gad]:
                hv = self.havuz[kas]
                pay = self.pay[kas]
                self._eks(self.pf[gad], hv.hucre.soma(0.5), eks,
                          ag['pf_mn'] * self.denge[gad] * pay)
                self._eks(self.ii_rly[gad], hv.hucre.soma(0.5), eks, ag['ii_mn'] * pay)
                if ir['renshaw_etkin']:
                    self._eks_h(hv, self.renshaw[gad], eks, ag['mn_rc'] * pay)
                    self._inh(self.renshaw[gad], hv.hucre.soma(0.5), inh, ag['rc_mn'] * pay)
                if ir['iain_etkin']:
                    self._inh(self.iain[karsi], hv.hucre.soma(0.5), inh, ag['iain_mn'] * pay)
            if ir['iain_etkin']:
                self._eks(self.pf[gad], self.iain[gad].sec(0.5), eks, ag['pf_iain'])
                # IaIN <-> IaIN (eklem ici) ve RC -> IaIN: D2 diyagraminda var, agirliklari
                # varsayilan 0.0 (kurulmaz) -- KAYNAKSIZ [tasarim] bilesen, etkinlestirme
                # kullanici karari (devre_par._rc_iain_notu).
                if ag.get('iain_iain', 0.0) > 0:
                    self._inh(self.iain[karsi], self.iain[gad].sec(0.5), inh, ag['iain_iain'])
                if ir['renshaw_etkin'] and ag.get('rc_iain', 0.0) > 0:
                    self._inh(self.renshaw[gad], self.iain[gad].sec(0.5), inh, ag['rc_iain'])
            # II -> CPG geri besleme kolu (gFB): oz_yu2021'in gFB/gCPG odunlesimi
            self._gsyn.append(nrn_devre.gradli_baglanti(
                self.ii_rly[gad], rg[gad],
                c['gcpg_mScm2'] * self.par['sinaps']['gfb_carpan'] / n_eklem,
                esyn=eks['e_mV'], ethr=-20.0, eslope=c['eslope_mV']))

        # internoron spike kayitlari (salt gozlemci NetCon; dinamigi degistirmez)
        for gad in gadlar:
            self._in_spk['PF_' + gad] = self.pf[gad].ap_kaydet()
            self._in_spk['IIrly_' + gad] = self.ii_rly[gad].ap_kaydet()
            if ir['iain_etkin']:
                self._in_spk['IaIN_' + gad] = self.iain[gad].ap_kaydet()
            if ir['renshaw_etkin']:
                self._in_spk['RC_' + gad] = self.renshaw[gad].ap_kaydet()

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

    # -- kosu ----------------------------------------------------------------------------
    def kos(self, sure_s, ilerleme=None, kas_kaydi=True):
        """kas_kaydi: OpenSim'den aktivasyon + tendon kuvveti de kaydedilir (kasilma kaniti
        figurleri icin). realizeDynamics maliyeti eklenir; kapatilirsa eski davranis."""
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
        if kas_kaydi:
            iz['akt'] = np.zeros((nadim, nk))
            iz['Fkas'] = np.zeros((nadim, nk))

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

            # 4) aksiyon potansiyellerinden u(t), sonra efferent gecikme
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
            if kas_kaydi:
                akt38, fk38 = self.mek.kas_durumu()      # 38'lik model dizisi
                iz['akt'][k], iz['Fkas'][k] = akt38[self.ix], fk38[self.ix]
            if ilerleme and (k + 1) % ilerleme == 0:
                print('  adim %6d/%d  t=%.3f s  q=%s derece  u_max=%.3f'
                      % (k + 1, nadim, iz['t'][k],
                         '/'.join('%.1f' % d for d in np.degrees(q)), u.max()), flush=True)
        return iz

    def spike_dokum(self):
        """Havuz ve internoron aksiyon potansiyeli zamanlarini numpy dizilerine doker.

        Donen sozluk (zamanlar saniye, kopru saatiyle ayni eksende):
          spike_t / spike_kas   : motonoron havuzlari (kas indeksi self.kaslar sirasinda)
          in_spike_t / in_spike_ix : internoronlar (PF, IaIN, RC, IIrly)
          in_adlar              : internoron adlari (in_spike_ix bu listeye indekstir)
        """
        st, sk = [], []
        for j, kas in enumerate(self.kaslar):
            z = np.array(self.havuz[kas].ap_zamanlari) * 1e-3        # ms -> s
            st.append(z)
            sk.append(np.full(len(z), j, dtype=int))
        in_adlar = list(self._in_spk)
        it, ii_ = [], []
        for j, ad in enumerate(in_adlar):
            z = np.array(self._in_spk[ad]) * 1e-3
            it.append(z)
            ii_.append(np.full(len(z), j, dtype=int))
        bos = np.zeros(0)
        return dict(
            spike_t=np.concatenate(st) if st else bos,
            spike_kas=np.concatenate(sk) if sk else bos.astype(int),
            in_spike_t=np.concatenate(it) if it else bos,
            in_spike_ix=np.concatenate(ii_) if ii_ else bos.astype(int),
            in_adlar=np.array(in_adlar))
