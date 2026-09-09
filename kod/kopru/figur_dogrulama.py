# =============================================================================
# figur_dogrulama.py — projenin DOGRULANMIS sayilarini figure ceviren betik.
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru)
# Girdi:  model/rat_hindlimb_faz1a.osim (moment kolu CANLI hesaplanir, OpenSim)
#         veri/u_swing_v2.csv                  (salinim fazi kas komutlari)
#         veri/kopru/yakinsama_{zaman,uzam}.json (yakinsama testlerinin kendi ciktilari)
#         veri/kopru/capraz_kontrol.npz          (HOC <-> Python karsilastirmasi)
# Cikti:  sekiller/dogrulama_{momentkolu,salinim,yakinsama,capraz}.png + .csv
#
# NEDEN: kapali dongu figurleri (figur_tumbacak.py) devrenin CALISTIGINI gosterir; bu betik
# projenin DOGRULAMA kaydindaki sayilari gorunur kilar -- hangi olcut hangi ilan edilmis
# aralikta gecti, hangisi kaldi. Ikisi ayri sorulardir ve rapor ikisini ayri baslikta sunar.
#
# KURAL: figurler ELLE TASINAN sayidan degil, artefakttan uretilir. Yakinsama ve capraz kontrol
# figurleri ilgili testin kendi yazdigi dosyayi okur; moment kolu figuru modeli acip
# computeMomentArm'i kendisi cagirir. Aralıklar literatur/referans_degerler.json'dan kimlikle
# okunur (figur_ortak.bant).
#
# BILINEN SAPMALAR (figurlerin kendisinde de yazilidir):
# - Quadriceps'in +3.7 mm'sini ANATOMI DEGIL femur_dist WrapTorus uretir (DOGRULAMA H1);
#   bu yuzden moment kolu figurunde sarma acik/kapali paneli vardir.
# - Johnson 2008 Sekil 3 ile sayisal karsilastirma HALA YAPILMADI (DOGRULAMA D); bu figur
#   "deneysel olcumlerle uyumludur" demez, yalnizca modelin kendi geometrisini gosterir.
# - Moment kolu POZA baglidir: iki eklemli kaslarda diz moment kolu kalca acisiyla degisir
#   (olculdu, panel c). Kayitli tek bir sayi ancak pozuyla birlikte anlamlidir.
# =============================================================================
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from figur_ortak import plt, kaydet, kaydet_tablo, bant, referanslar
from yollar import OSIM_FAZ1A, GRID3D, U_SWING, VERI_KOPRU

QUAD = ['RF', 'VL', 'VI', 'VM']
DIZ_FLX = ['SM', 'STa', 'STp', 'BFp', 'GP', 'GA', 'Pla', 'MG', 'LG', 'Pop']
OLCULMUS_DIZ = (-139.73, -107.65)        # PREPRINT 5.2, olculmus yuruyus araligi
REF_DIZ = -120.0                          # DOGRULAMA A'nin olcum acisi

# PREPRINT 9.2 gruplandirmasi (moment kolu isaretine gore) -- salinim figuru bunu kullanir.
# Not: devrenin BUGUNKU grup uyeligi EMG fazina gore tanimlidir (DOGRULAMA R.5); bu figur
# ID+SO sonucunu bildirinin kendi cumlesiyle karsilastirdigi icin PREPRINT 9.2 gruplarini alir.
SALINIM_GRUP = {
    'kalca fleksor': ['IP', 'TFL', 'RF', 'GMe', 'GMa'],
    'diz ekstansor': ['VL', 'VI', 'VM', 'RF'],
    'diz fleksor': ['Pop', 'MG', 'LG', 'Pla'],
    'kalca ekstansor': ['SM', 'BFp', 'STa', 'STp', 'GP', 'GA', 'AB', 'AM', 'AL', 'QF', 'CF',
                        'GI', 'GS'],
    'bilek dorsifleksor': ['TA', 'EDL', 'Per'],
    'bilek plantarfleksor': ['Sol', 'MG', 'LG', 'Pla', 'TP', 'FDL', 'FHL'],
}


# ==================== 1) moment kollari (OpenSim, canli hesap) ==============================
def _model_kur(sarma_kapali=()):
    """Modeli FIX pozunda kurar. sarma_kapali: bu kaslarin PathWrap kumesi bosaltilir (H1)."""
    import opensim as osim
    m = osim.Model(str(OSIM_FAZ1A))
    if sarma_kapali:
        mus0 = m.getMuscles()
        adlar0 = [mus0.get(i).getName() for i in range(mus0.getSize())]
        for k in sarma_kapali:
            ws = mus0.get(adlar0.index(k)).updGeometryPath().updWrapSet()
            for j in range(ws.getSize() - 1, -1, -1):
                ws.remove(j)
    s = m.initSystem()
    g = np.load(GRID3D, allow_pickle=True)
    fix = dict(zip([str(x) for x in g['cnames']], [float(v) for v in g['FIX']]))
    cs = m.getCoordinateSet()
    for i in range(cs.getSize()):
        c = cs.get(i)
        if c.getName() in fix:
            c.setValue(s, fix[c.getName()])
    m.realizePosition(s)
    mus = m.getMuscles()
    return m, s, mus, [mus.get(i).getName() for i in range(mus.getSize())]


def _ma(m, s, mus, adlar, kaslar, supur, acilar_derece, moment=None):
    """supur koordinati taranirken kaslarin MOMENT koordinatindaki moment kolu [mm].

    Iki koordinat AYRIDIR: iki eklemli bir kasin diz moment kolunun kalca acisina nasil
    bagli oldugunu gormek icin kalca supurulur ama moment DIZ'den alinir. Ayrilmazsa
    supurulen eklemin momenti cizilir ve figur sessizce yanlis olur (bu hata yapildi)."""
    moment = moment if moment is not None else supur
    cikti = {k: np.zeros(len(acilar_derece)) for k in kaslar}
    for i, a in enumerate(acilar_derece):
        supur.setValue(s, np.radians(a))
        m.realizePosition(s)
        for k in kaslar:
            cikti[k][i] = mus.get(adlar.index(k)).computeMomentArm(s, moment) * 1000.0
    return cikti


def figur_momentkolu(ad='dogrulama_momentkolu'):
    g = np.load(GRID3D, allow_pickle=True)
    diz_ac = np.linspace(np.degrees(g['KNE'][0]), np.degrees(g['KNE'][-1]), 60)
    kalca_ac = np.linspace(np.degrees(g['HIP'][0]), np.degrees(g['HIP'][-1]), 40)

    m, s, mus, adlar = _model_kur()
    cs = m.getCoordinateSet()
    diz, kalca = cs.get('knee_flx'), cs.get('hip_flx')
    egri = _ma(m, s, mus, adlar, QUAD + DIZ_FLX, diz, diz_ac)
    diz.setValue(s, np.radians(REF_DIZ)); m.realizePosition(s)
    ref_deger = {k: mus.get(adlar.index(k)).computeMomentArm(s, diz) * 1000.0
                 for k in QUAD + DIZ_FLX}
    kalca_fix = np.degrees(kalca.getValue(s))
    # panel c: SM ve RF diz moment kolunun KALCA acisina bagimliligi (iki eklemli kaslar)
    sm_kalca = _ma(m, s, mus, adlar, ['SM', 'RF'], kalca, kalca_ac, moment=diz)
    kalca.setValue(s, np.radians(kalca_fix)); m.realizePosition(s)

    # panel b: quadriceps sarma acik/kapali (H1)
    m2, s2, mus2, adlar2 = _model_kur(sarma_kapali=QUAD)
    cs2 = m2.getCoordinateSet(); diz2 = cs2.get('knee_flx')
    diz2.setValue(s2, np.radians(REF_DIZ)); m2.realizePosition(s2)
    sarmasiz = {k: mus2.get(adlar2.index(k)).computeMomentArm(s2, diz2) * 1000.0 for k in QUAD}

    fig = plt.figure(figsize=(14.5, 10))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.3, 1.0], hspace=0.42, wspace=0.22,
                          right=0.86)

    a = fig.add_subplot(gs[0, :])
    a.axhline(0, color='k', lw=0.8)
    a.axvspan(*OLCULMUS_DIZ, color='0.9', zorder=0, label='olculmus yuruyus diz araligi')
    for k in QUAD:
        a.plot(diz_ac, egri[k], lw=1.6, label='%s (ekstansor)' % k)
    for k in DIZ_FLX:
        a.plot(diz_ac, egri[k], lw=1.0, ls='--', alpha=0.8, label=k)
    a.axvline(REF_DIZ, color='k', lw=0.8, ls=':')
    a.text(REF_DIZ, a.get_ylim()[1], ' %.0f derece (DOGRULAMA A olcum acisi)' % REF_DIZ,
           fontsize=7, va='top')
    a.set_xlabel('diz acisi knee_flx [derece]')
    a.set_ylabel('diz moment kolu [mm]')
    a.set_title('(a) Diz moment kollari -- model geometrisinden CANLI hesaplandi '
                '(OpenSim computeMomentArm). Poz: cl_grid3d FIX (kalca %.1f derece)' % kalca_fix)
    a.legend(fontsize=6.5, ncol=1, loc='upper left', bbox_to_anchor=(1.005, 1.0),
             borderaxespad=0.0)
    a.grid(alpha=0.25)

    b = fig.add_subplot(gs[1, 0])
    x = np.arange(len(QUAD))
    b.bar(x - 0.2, [ref_deger[k] for k in QUAD], 0.4, label='sarma ACIK (modeldeki hal)')
    b.bar(x + 0.2, [sarmasiz[k] for k in QUAD], 0.4, color='tab:red', label='sarma KAPALI')
    bant(b, 'ic.quad_diz_moment_kolu')
    b.axhline(0, color='k', lw=0.8)
    b.set_xticks(x); b.set_xticklabels(QUAD)
    b.set_ylabel('diz moment kolu [mm] @ %.0f derece' % REF_DIZ)
    b.set_title('(b) +3,7 mm ANATOMIDEN DEGIL femur_dist WrapTorus\'undan geliyor (H1):\n'
                'sarma kapatilinca quadriceps FLEKSOR oluyor', fontsize=9)
    b.set_ylim(min(sarmasiz.values()) * 1.6, 5.4)
    b.legend(fontsize=7, loc='upper left')
    b.grid(alpha=0.25, axis='y')

    c = fig.add_subplot(gs[1, 1])
    c.plot(kalca_ac, sm_kalca['SM'], lw=1.6, color='tab:purple', label='SM')
    c.plot(kalca_ac, sm_kalca['RF'], lw=1.2, color='tab:olive', label='RF')
    bant(c, 'ic.sm_diz_moment_kolu')
    c.axvline(kalca_fix, color='k', lw=0.8, ls=':')
    c.set_xlabel('kalca acisi hip_flx [derece]   (diz sabit %.0f derece)' % REF_DIZ)
    c.set_ylabel('DIZ moment kolu [mm]')
    c.set_title('(c) Iki eklemli kasin diz moment kolu POZA baglidir:\n'
                'SM %.2f .. %.2f mm arasinda degisiyor' %
                (sm_kalca['SM'].min(), sm_kalca['SM'].max()), fontsize=9)
    c.legend(fontsize=7, loc='center left')
    c.grid(alpha=0.25)

    fig.suptitle('Kas-iskelet dogrulamasi: moment kollari  '
                 '(Johnson 2008 Sekil 3 ile SAYISAL karsilastirma YAPILMADI -- DOGRULAMA D)',
                 fontsize=11)
    kaydet(fig, ad, sikistir=True)

    satirlar = []
    for i, x0 in enumerate(diz_ac):
        for k in QUAD + DIZ_FLX:
            satirlar.append(('a_diz_suprusu', '%.3f' % x0, k, '%.4f' % egri[k][i]))
    for k in QUAD:
        satirlar.append(('b_sarma_acik', '%.1f' % REF_DIZ, k, '%.4f' % ref_deger[k]))
        satirlar.append(('b_sarma_kapali', '%.1f' % REF_DIZ, k, '%.4f' % sarmasiz[k]))
    for i, x0 in enumerate(kalca_ac):
        for k in ('SM', 'RF'):
            satirlar.append(('c_kalca_suprusu', '%.3f' % x0, k, '%.4f' % sm_kalca[k][i]))
    kaydet_tablo(ad, ['panel', 'x_derece', 'kas', 'r_mm'], satirlar,
                 aciklama='OpenSim computeMomentArm, model/rat_hindlimb_faz1a.osim, '
                          'poz cl_grid3d FIX (kalca %.2f derece); panel b sarma kumesi '
                          'bosaltilarak olculdu' % kalca_fix)
    return ref_deger, sarmasiz, kalca_fix


# ==================== 2) salinim fazi zamanlamasi ==========================================
def figur_salinim(ad='dogrulama_salinim'):
    with open(U_SWING) as fh:
        satir = [s for s in fh if not s.startswith('#')]
    bas = satir[0].strip().split(',')
    veri = np.array([[float(x) for x in s.strip().split(',')] for s in satir[1:]])
    gait, U = veri[:, 0], veri[:, 1:]
    kaslar = bas[1:]
    tepe = {k: U[:, j].max() for j, k in enumerate(kaslar)}
    tepe_t = {k: gait[U[:, j].argmax()] for j, k in enumerate(kaslar)}
    etkin = sorted([k for k in kaslar if tepe[k] > 0.005], key=lambda k: tepe_t[k])

    fig, ax = plt.subplots(2, 1, figsize=(11, 9),
                           gridspec_kw=dict(height_ratios=[1.5, 1.0], hspace=0.28))
    M = np.array([U[:, kaslar.index(k)] / tepe[k] for k in etkin])
    im = ax[0].imshow(M, aspect='auto', origin='lower', cmap='magma',
                      extent=[gait[0], gait[-1], -0.5, len(etkin) - 0.5])
    for i, k in enumerate(etkin):
        ax[0].plot(tepe_t[k], i, 'w|', ms=12, mew=2)
    ax[0].set_yticks(range(len(etkin)))
    ax[0].set_yticklabels(['%s (tepe %.4f)' % (k, tepe[k]) for k in etkin], fontsize=7)
    ax[0].set_xlabel('yuruyus cevrimi [%]')
    ax[0].set_title('(a) Salinim fazi kas aktivasyonlari (ID + statik optimizasyon, '
                    'veri/u_swing_v2.csv). Beyaz cizgi = tepe zamani.\n'
                    'Her kas KENDI tepesine normalize -- mutlak degerler kucuktur (a <= 0.077)',
                    fontsize=9)
    fig.colorbar(im, ax=ax[0], label='normalize aktivasyon', pad=0.01)

    grup_t, grup_top = {}, {}
    for gad, kl in SALINIM_GRUP.items():
        top = U[:, [kaslar.index(k) for k in kl if k in kaslar]].sum(1)
        grup_top[gad] = top.sum()
        grup_t[gad] = gait[top.argmax()]
        ax[1].plot(gait, top, lw=1.4, label='%s (tepe %%%.1f)' % (gad, grup_t[gad]))
    ax[1].set_xlabel('yuruyus cevrimi [%]')
    ax[1].set_ylabel('grup toplam aktivasyonu')
    ax[1].legend(fontsize=7, ncol=2)
    ax[1].grid(alpha=0.25)
    ax[1].set_title('(b) Grup duzeyinde sira. BILDIRININ IDDIASI: kalca fleksor -> bilek '
                    'dorsifleksor -> kalca ekstansor.\nOLCULEN: kalca fleksor %%%.1f -> diz '
                    'fleksor %%%.1f -> bilek dorsifleksor %%%.1f (son iki halka yer degistiriyor, '
                    'PREPRINT 10.4)'
                    % (grup_t['kalca fleksor'], grup_t['diz fleksor'],
                       grup_t['bilek dorsifleksor']), fontsize=9)
    sut = {'gait_pct': gait}
    for k in etkin:
        sut['a_' + k] = U[:, kaslar.index(k)]
    for gad in SALINIM_GRUP:
        sut['grup_' + gad.replace(' ', '_')] = U[:, [kaslar.index(k)
                                                     for k in SALINIM_GRUP[gad]]].sum(1)
    kaydet(fig, ad, sutunlar=sut, sikistir=True,
           aciklama='kaynak veri/u_swing_v2.csv; grup tepe zamanlari: ' +
                    ' | '.join('%s %%%.1f (toplam %.3f)' % (g, grup_t[g], grup_top[g])
                               for g in SALINIM_GRUP))
    return grup_t, grup_top


# ==================== 3) yakinsama testleri ================================================
def figur_yakinsama(ad='dogrulama_yakinsama'):
    kayitlar = []
    for dosya, tur, etiketler in (
            ('yakinsama_zaman.json', 'zaman adimi yarilama', ('dt_ms', 'd_lambda')),
            ('yakinsama_uzam.json', 'uzamsal cozunurluk', ('d_lambda', 'dt_ms'))):
        yol = VERI_KOPRU / dosya
        if not yol.exists():
            print('atlandi (artefakt yok): %s' % dosya)
            continue
        with open(yol) as fh:
            kayitlar.append((tur, json.load(fh)))
    if not kayitlar:
        print('yakinsama figuru atlandi: hicbir artefakt yok')
        return None

    bagil = lambda x, y: abs(x - y) / max(abs(x), abs(y), 1e-12)
    fig, ax = plt.subplots(1, len(kayitlar), figsize=(6.5 * len(kayitlar), 5.2), squeeze=False)
    satirlar = []
    for ci, (tur, j) in enumerate(kayitlar):
        a, b = j['a'], j['b']
        olcut, fark, band = [], [], []
        if np.isfinite(a.get('T', float('nan'))) and np.isfinite(b.get('T', float('nan'))):
            olcut.append('cevrim suresi'); fark.append(bagil(a['T'], b['T']))
            band.append(j['bantlar']['T'])
        for k in a['roms']:
            olcut.append('ROM ' + k); fark.append(bagil(a['roms'][k], b['roms'][k]))
            band.append(j['bantlar']['ROM'])
        for k in a['frek']:
            olcut.append('f ' + k); fark.append(bagil(a['frek'][k], b['frek'][k]))
            band.append(j['bantlar']['frekans'])
        y = np.arange(len(olcut))
        renk = ['tab:green' if f < s else 'tab:red' for f, s in zip(fark, band)]
        A = ax[0][ci]
        A.barh(y, 100 * np.array(fark), color=renk)
        for i, s in enumerate(set(band)):
            A.axvline(100 * s, color='k', ls='--', lw=1.0)
        A.set_yticks(y); A.set_yticklabels(olcut, fontsize=8)
        A.invert_yaxis()
        A.set_xlabel('iki ayar arasindaki bagil fark [%]')
        gecti = all(f < s for f, s in zip(fark, band))
        A.set_title('%s -- %s\n%s, %.1f s | kesikli cizgi = ILAN EDILMIS bant'
                    % (tur, 'GECTI' if gecti else 'DUSTU', j['kosucu'], j['sure_s']),
                    fontsize=10, color='tab:green' if gecti else 'tab:red')
        A.grid(alpha=0.25, axis='x')
        for o, f, s in zip(olcut, fark, band):
            satirlar.append((tur, o, '%.6f' % f, '%.3f' % s, 'gecti' if f < s else 'DUSTU'))
    fig.suptitle('Sayisal yakinsama: sonuc, cozum adimindan ve izgara cozunurlugunden '
                 'bagimsiz mi?', fontsize=11)
    kaydet(fig, ad, sikistir=True)
    kaydet_tablo(ad, ['test', 'olcut', 'bagil_fark', 'bant', 'sonuc'], satirlar,
                 aciklama='kaynak: veri/kopru/yakinsama_*.json (testlerin kendi ciktisi); '
                          'bantlar testten ONCE ilan edildi (SDLC/04_KURALLAR)')
    return satirlar


# ==================== 4) HOC <-> Python capraz kontrolu =====================================
def figur_capraz(ad='dogrulama_capraz'):
    yol = VERI_KOPRU / 'capraz_kontrol.npz'
    if not yol.exists():
        print('capraz figuru atlandi: %s yok (once capraz_kontrol.py kosun)' % yol.name)
        return None
    d = np.load(yol)
    t, vh, vp = d['t_ms'], d['v_hoc'], d['v_py']
    fark = np.abs(vh - vp)

    fig, ax = plt.subplots(2, 1, figsize=(11, 7),
                           gridspec_kw=dict(height_ratios=[2.0, 1.0], hspace=0.3))
    ax[0].plot(t, vh, lw=1.6, color='tab:blue', label='HOC (Kim 2020 kendi zinciri)')
    ax[0].plot(t, vp, lw=0.8, color='tab:orange', ls='--', label='Python (nrn_hucre.py)')
    ax[0].set_ylabel('soma voltaji [mV]')
    ax[0].legend(fontsize=8, loc='upper left')
    ax[0].grid(alpha=0.25)
    ax[0].set_title('(a) Ayni uyaran (RampIClamp), ayni surec, ayni zaman adimi: '
                    'iki kurulum ust uste biniyor\n'
                    '%d/%d section, %d/%d segment, %d/%d aksiyon potansiyeli'
                    % (int(d['sec_hoc']), int(d['sec_py']), int(d['nseg_hoc']),
                       int(d['nseg_py']), d['ap_hoc'].size, d['ap_py'].size), fontsize=10)
    # ilk aksiyon potansiyeli cevresine yakinlastirilmis pencere
    if d['ap_hoc'].size:
        t0 = float(d['ap_hoc'][0])
        ic = ax[0].inset_axes([0.62, 0.08, 0.36, 0.45])
        m = (t > t0 - 5) & (t < t0 + 15)
        ic.plot(t[m], vh[m], lw=1.8, color='tab:blue')
        ic.plot(t[m], vp[m], lw=0.9, color='tab:orange', ls='--')
        ic.set_title('ilk aksiyon potansiyeli (%.3f ms)' % t0, fontsize=7)
        ic.tick_params(labelsize=6)
        ic.grid(alpha=0.25)

    ax[1].plot(t, fark, lw=0.8, color='tab:red')
    ax[1].set_xlabel('zaman [ms]')
    ax[1].set_ylabel('|HOC - Python| [mV]')
    ax[1].set_ylim(-1e-3, max(1e-2, fark.max() * 1.2))
    ax[1].grid(alpha=0.25)
    apf = (np.abs(d['ap_hoc'] - d['ap_py']).max() if d['ap_hoc'].size == d['ap_py'].size
           and d['ap_hoc'].size else float('nan'))
    ax[1].set_title('(b) Fark izi: voltajda maks %.6f mV, aksiyon potansiyeli zamaninda '
                    'maks %.6f ms (aralık bir entegrasyon adimi = %.3f ms)'
                    % (fark.max(), apf, float(d['dt_ms'])), fontsize=10)
    fig.suptitle('Motonoron kurulumunun bagimsiz ikinci yontemle capraz kontrolu '
                 '(SDLC/04_KURALLAR)', fontsize=11)
    a = max(1, len(t) // 12000)                 # CSV icin seyreltme (yalniz kaynak dosyada)
    kaydet(fig, ad, sikistir=True,
           sutunlar=dict(t_ms=t[::a], v_hoc=vh[::a], v_py=vp[::a], fark_mV=fark[::a]),
           aciklama='kaynak veri/kopru/capraz_kontrol.npz; CSV 1/%d seyreltildi, PNG tam '
                    'cozunurlukten cizildi; voltaj maks fark %.6g mV' % (a, fark.max()))
    return fark.max(), apf


if __name__ == '__main__':
    hangi = [a for a in sys.argv[1:] if not a.startswith('-')]
    hepsi = not hangi
    if hepsi or 'momentkolu' in hangi:
        figur_momentkolu()
        print('yazildi: sekiller/dogrulama_momentkolu.{png,csv}')
    if hepsi or 'salinim' in hangi:
        figur_salinim()
        print('yazildi: sekiller/dogrulama_salinim.{png,csv}')
    if hepsi or 'yakinsama' in hangi:
        if figur_yakinsama():
            print('yazildi: sekiller/dogrulama_yakinsama.{png,csv}')
    if hepsi or 'capraz' in hangi:
        if figur_capraz():
            print('yazildi: sekiller/dogrulama_capraz.{png,csv}')
