# =============================================================================
# kos_tumbacak.py — Asama 4: TUM BACAKTA kapali dongu (3 serbestlik derecesi, 38 havuz).
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru)
# Girdi:  kod/kopru/devre_par.json (havuz_eslesme dahil); model/rat_hindlimb_faz1a.osim;
#         veri/kapali_dongu/cl_grid3d.npz; literatur/referans_degerler.json (araliklar)
# Cikti:  veri/kopru/kosu_tumbacak.npz  (canli kosu + pasif kontrol + spike dokumleri)
#
# Zincir: CPG (Morris-Lecar yarim-merkez) -> 6 PF grubu -> 38 motonoron havuzu -> u(t) ->
#         OpenSim ileri dinamigi (hip_flx + knee_flx + ankle_flx) -> hareket -> igcik ->
#         Ia/II -> gecikme -> Ia sinapsi. Eklem acilari RECETE DEGILDIR; kas kuvvetinden dogar.
#
# PASIF KONTROL: ayni mekanik model, ayni baslangic pozu, u = 0 (noron surusu yok).
# "Hareketi noronlar uretiyor" iddiasinin dogrudan kaniti: pasif kosuda ritmik hareket
# olmamali, canli kosuda olmali. NEURON hic kurulmadan kosulur (ucuz).
#
# BILINEN SAPMALAR:
# - IaIN ve Renshaw devrededir ama literatur setinde KAYNAKLARI YOKTUR (PREPRINT 6.1);
#   hicbir sonuc bunlara dayandirilarak iddia edilmez. II katsayilari [varsayim].
# - GMa modelin moment koluna gore kalca fleksoru surulur (PREPRINT acik soru 4).
# - Surussuz 6 kas (Pir, GMi, OE, OI, Pec, BFa) havuzludur ama PF surusu almaz
#   (moment kolu isareti kararsiz; devre_par.havuz_eslesme._surussuz_notu).
# =============================================================================
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from yollar import VERI_KOPRU, LITERATUR

SERBEST = ('hip_flx', 'knee_flx', 'ankle_flx')
REF_JSON = LITERATUR / 'referans_degerler.json'
# eklem -> (serbest indeksi, referans kayit kimligi)
ROM_KAYIT = {'hip_flx': 'ic.kopru_kalca_araligi',
             'knee_flx': 'ic.kopru_diz_araligi',
             'ankle_flx': 'ic.kopru_bilek_araligi'}
FREK_KAYIT = {'TA': 'gorassini2000.mn_frekans_TA_swing',
              'Sol': 'gorassini2000.mn_frekans_SOL_yuruyus',
              'MG': 'gorassini2000.mn_frekans_MGLG_ortagec',
              'LG': 'gorassini2000.mn_frekans_MGLG_ortagec'}


def referanslar():
    r = json.load(open(REF_JSON))
    return {k['kimlik']: k for k in r['kayitlar']}


def kur(dt_kopru_ms=None, par_yol=None):
    """par_yol: kalibrasyon taramasi degistirilmis parametre dosyasiyla kurabilsin diye."""
    from kopru import Kopru, Gecikme
    if par_yol is None:
        par_yol = pathlib.Path(__file__).resolve().parent / 'devre_par.json'
    with open(par_yol) as fh:
        pozlar = json.load(fh)['havuz_eslesme']['denge_pozu_derece']
    kk = Kopru(gruplar=None, serbest=SERBEST, par_yol=par_yol)
    # baslangic pozu: olculmus yuruyus orta noktalari (denge olcumuyle ayni poz)
    for ad in SERBEST:
        kk.mek.koord[ad].setValue(kk.mek.s, np.radians(pozlar[ad]))
    if dt_kopru_ms is not None:                 # zaman adimi yarilama testi icin
        kk.dt_ms = dt_kopru_ms
        kk.dt_s = dt_kopru_ms * 1e-3
        kk.mek.dt = kk.dt_s
        kp = kk.par['kopru']
        n = len(kk.kaslar)
        kk.g_ia = Gecikme(round(kp['gecikme_ia_ms'] / dt_kopru_ms), n)
        kk.g_ii = Gecikme(round(kp['gecikme_ii_ms'] / dt_kopru_ms), n)
        kk.g_ef = Gecikme(round(kp['gecikme_efferent_ms'] / dt_kopru_ms), n)
    return kk


def pasif_kos(sure_s, dt_s=None):
    """Noron surusu OLMADAN ayni mekanik kosu: u = 0 sabit. NEURON kurulmaz.
    Limit kuvvetleri canli kosuyla AYNI (karsilastirma adil olsun)."""
    from osim_mekanik import Mekanik
    from yollar import GRID3D
    with open(pathlib.Path(__file__).resolve().parent / 'devre_par.json') as fh:
        par = json.load(fh)
    pozlar = par['havuz_eslesme']['denge_pozu_derece']
    if dt_s is None:
        dt_s = par['kopru']['dt_kopru_ms'] * 1e-3
    g = np.load(GRID3D, allow_pickle=True)
    eksen = {'hip_flx': 'HIP', 'knee_flx': 'KNE', 'ankle_flx': 'ANK'}
    limitler = {ad: (float(np.degrees(g[eksen[ad]][0])), float(np.degrees(g[eksen[ad]][-1])))
                for ad in SERBEST}
    mek = Mekanik(serbest=SERBEST, dt_kopru_s=dt_s,
                  baslangic={ad: np.radians(v) for ad, v in pozlar.items()},
                  limitler=limitler, limit_par=par['kopru'].get('limit_kuvveti'))
    mek.baslat()
    mek.uyarim_yaz(np.zeros(mek.n))
    nadim = int(round(sure_s / dt_s))
    t = np.zeros(nadim)
    q = np.zeros((nadim, len(SERBEST)))
    for k in range(nadim):
        qk, _, _, _ = mek.adim()
        t[k] = (k + 1) * dt_s
        q[k] = qk
    return dict(t=t, q=q)


def ortusme(a, b):
    """Iki [alt, ust] araliginin ortusme orani (kesisim / birlesim)."""
    kes = max(0.0, min(a[1], b[1]) - max(a[0], b[0]))
    bir = max(a[1], b[1]) - min(a[0], b[0])
    return kes / bir if bir > 0 else 0.0


def ozet(kk, iz, yari_atla=True):
    """Kosunu sayisal ozeti + referans araliklariyla karsilastirma (rapor; assert degil,
    cunku kalibrasyon sureci bu ozetle yurur; sert dogrulama adim_yarilama + kanonik rapor)."""
    n = len(iz['t']) // 2 if yari_atla else 0
    t = iz['t'][n:]
    ix = {k: i for i, k in enumerate(kk.kaslar)}
    ref = referanslar()

    # cevrim suresi: kalca acisinin ortalama gecisleri (en genis ROM'lu eklem)
    qh = np.degrees(iz['q'][n:, SERBEST.index('hip_flx')])
    e = qh.mean()
    gec = np.where((qh[:-1] < e) & (qh[1:] >= e))[0]
    T = float(np.mean(np.diff(t[gec]))) if len(gec) > 2 else float('nan')

    eklemler = {}
    for j, ad in enumerate(SERBEST):
        q = np.degrees(iz['q'][n:, j])
        olc = [float(q.min()), float(q.max())]
        hedef = ref[ROM_KAYIT[ad]]['deger']
        # sinira dayanma orani: limit kuvvetinin tanim alani sinirina 6 derece yakinlikta
        # gecirilen zaman payi (cl_selfcheck nearlim deseni). Yuksekse devre sinira yasliyor.
        if ad in kk.limitler:
            alt, ust = kk.limitler[ad]
            yakin = float(np.mean((q < alt + 6.0) | (q > ust - 6.0)))
        else:
            yakin = 0.0
        eklemler[ad] = dict(aralik=olc, rom=olc[1] - olc[0], hedef=hedef,
                            ortusme=ortusme(olc, hedef), sinir_yakin=yakin)

    # havuz basina ETKIN faz ortalama atesleme orani (kendi tepesinin uzerindeki adimlar)
    frek = {}
    for k in kk.kaslar:
        f = iz['f'][n:, ix[k]]
        etkin = f > 0.2 * f.max() if f.max() > 0 else np.zeros(len(f), bool)
        frek[k] = (float(f[etkin].mean()) if etkin.any() else 0.0, float(f.max()))

    u_grup = {g: iz['u'][n:, jx].mean(1) for g, jx in kk._grup_ix.items()}
    # eklem ici antagonist zitfaz korelasyonlari
    korel = {}
    for gad, g in kk.grup_tanim.items():
        kr = kk.karsi[gad]
        if (g['eklem'], gad) < (kk.grup_tanim[kr]['eklem'], kr):
            korel[g['eklem']] = float(np.corrcoef(u_grup[gad], u_grup[kr])[0, 1])

    # biartikuler kaslarin u tepe degerleri (pay=0.5 olceginin kontrolu)
    biart = {k: float(iz['u'][n:, ix[k]].max())
             for k, gr in kk.uyelik.items() if len(gr) > 1}
    return dict(T=T, eklemler=eklemler, frek=frek, korel=korel, biart=biart,
                u_ort={g: float(v.mean()) for g, v in u_grup.items()})


def rapor(kk, o):
    ref = referanslar()
    ck = ref['ic.kopru_cevrim_suresi']
    icinde = ck['aralik'][0] <= o['T'] <= ck['aralik'][1] if np.isfinite(o['T']) else False
    print('\n--- ikinci yari (gecici rejim atildi) ---')
    print('cevrim suresi   : %.3f s   (referans %.3f, aralik [%.3f-%.3f], kaynak %s) -> %s'
          % (o['T'], ck['deger'], ck['aralik'][0], ck['aralik'][1],
             ck['kaynak']['kunye'], 'ARALIKTA' if icinde else 'DISARIDA'))
    print('\n%-10s %18s %18s %9s %10s' % ('eklem', 'olculen [derece]', 'hedef [derece]',
                                          'ortusme', 'sinirda'))
    for ad, e in o['eklemler'].items():
        print('%-10s %8.2f..%8.2f %8.2f..%8.2f %8.2f %9.2f  (olcut >= 0.5, %s)'
              % (ad, e['aralik'][0], e['aralik'][1], e['hedef'][0], e['hedef'][1],
                 e['ortusme'], e['sinir_yakin'], ROM_KAYIT[ad]))
    print('\nantagonist u korelasyonlari (zitfaz beklenir):',
          {k: round(v, 3) for k, v in o['korel'].items()})
    print('\n%-6s %12s %12s %26s' % ('kas', 'f_etkin Hz', 'f_maks Hz', 'Gorassini araligi'))
    for k in kk.kaslar:
        fe, fm = o['frek'][k]
        if k in FREK_KAYIT:
            r = ref[FREK_KAYIT[k]]
            dur = 'ARALIKTA' if r['aralik'][0] <= fe <= r['aralik'][1] else 'disarida'
            ek = '%.0f [%.0f-%.0f] %s' % (r['deger'], r['aralik'][0], r['aralik'][1], dur)
        else:
            ek = '-'
        print('%-6s %12.2f %12.2f %26s' % (k, fe, fm, ek))
    print('\nbiartikuler u tepeleri:', {k: round(v, 3) for k, v in sorted(o['biart'].items())})


if __name__ == '__main__':
    import time
    sure = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0

    print('=== pasif kontrol kosusu (u = 0, NEURON yok) ===')
    t0 = time.perf_counter()
    pasif = pasif_kos(sure)
    print('pasif: %.1f s simulasyon -> %.1f s CPU' % (sure, time.perf_counter() - t0))
    for j, ad in enumerate(SERBEST):
        q = np.degrees(pasif['q'][:, j])
        print('  %-10s %8.2f .. %8.2f derece (ROM %.2f)' % (ad, q.min(), q.max(), q.max() - q.min()))

    print('\n=== canli kosu (38 havuz, 3 DOF) ===')
    t0 = time.perf_counter()
    kk = kur()
    print('kurulum        : %.1f s CPU' % (time.perf_counter() - t0))
    assert all(k not in kk.uyelik for k in kk.surussuz), 'surussuz kasa PF baglanmis'
    print('havuz          : %d (%d surusluk + %d surussuz)'
          % (len(kk.havuz), len(kk.uyelik), len(kk.surussuz)))
    print('bolme/havuz    : %d segment' % list(kk.havuz.values())[0].hucre.segment_sayisi())
    print('PF/IaIN/RC/IIrly: %d / %d / %d / %d' % (len(kk.pf), len(kk.iain),
                                                   len(kk.renshaw), len(kk.ii_rly)))
    print('kopru adimi    : %.3f ms | gecikme Ia %d adim, II %d, efferent %d'
          % (kk.dt_ms, kk.g_ia.n, kk.g_ii.n, kk.g_ef.n))
    print('moment kapasitesi [N*mm]:', {g: round(v, 1) for g, v in kk.kapasite.items()})
    print('denge olcegi           :', {g: round(v, 3) for g, v in kk.denge.items()})
    t0 = time.perf_counter()
    iz = kk.kos(sure, ilerleme=int(0.5 / kk.dt_s))
    print('kosu: %.1f s simulasyon -> %.1f s CPU' % (sure, time.perf_counter() - t0))

    o = ozet(kk, iz)
    rapor(kk, o)

    spk = kk.spike_dokum()
    VERI_KOPRU.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        VERI_KOPRU / 'kosu_tumbacak.npz',
        kaslar=np.array(kk.kaslar), serbest=np.array(SERBEST),
        gruplar=json.dumps(kk.gruplar), surussuz=np.array(kk.surussuz),
        kapasite=json.dumps(kk.kapasite), denge=json.dumps(kk.denge),
        pasif_t=pasif['t'], pasif_q=pasif['q'], **spk, **iz)
    print('\nyazildi: veri/kopru/kosu_tumbacak.npz')
