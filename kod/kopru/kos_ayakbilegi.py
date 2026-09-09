# =============================================================================
# kos_ayakbilegi.py — Asama 3: ayak bileginde TAM KAPALI DONGU (tek serbestlik derecesi).
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru)
# Girdi:  kod/kopru/devre_par.json; model/rat_hindlimb_faz1a.osim; veri/kapali_dongu/cl_grid3d.npz
# Cikti:  veri/kopru/kosu_ayakbilegi.npz
#         sekiller/kopru_ayakbilegi.png (300 dpi) + sekiller/kopru_ayakbilegi.csv
#
# Zincir: CPG (Morris-Lecar yarim-merkez) -> PF -> motonoron havuzu -> u(t) -> OpenSim ileri
#         dinamik -> hareket -> kas-tendon boyu/hizi -> igcik -> Ia/II -> gecikme -> Ia sinapsi
# Kinematik RECETE DEGILDIR: bilek acisi kas kuvvetlerinden dogar.
#
# Neden once tek eklem: kapali dongunun serbest parametreleri cok (sinaptik agirliklar, k_ia,
# f_ref, CPG surusu) ve karsilastirilacak referans yok. Tek eklemde zincirin tamami kosar ama
# hata ayiklama ucuzdur; ayni uretec 3 DOF / 38 havuz icin degismeden olceklenir.
#
# Antagonist cift PREPRINT 6.4'un moment kolu gruplandirmasindan:
#   dorsifleksor  TA (+3.43) EDL (+2.48) Per (+2.46)
#   plantarfleks. Sol (-4.00) MG (-3.43) LG (-3.08) Pla (-4.13) TP (-1.88) FDL (-2.25) FHL (-2.26)
#
# BILINEN SAPMALAR:
# - IaIN ve Renshaw devrededir ama literatur setinde KAYNAKLARI YOKTUR (PREPRINT 6.1);
#   hicbir sonuc bunlara dayandirilarak iddia edilmez.
# - Bilek eklemine acisal limit kuvveti yoktur (.osim'de CoordinateLimitForce tanimli degil);
#   acinin fizyolojik aralikta kalmasi devrenin isidir, modelin kisiti degil.
# =============================================================================
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from yollar import VERI_KOPRU, SEKILLER

DF = ['TA', 'EDL', 'Per']
PF = ['Sol', 'MG', 'LG', 'Pla', 'TP', 'FDL', 'FHL']


def kur(dt_kopru_ms=None, par_yol=None):
    """par_yol: tarama/yakinsama testleri degistirilmis parametre dosyasiyla kurabilsin diye
    (kos_tumbacak.kur ile ayni sozlesme)."""
    from kopru import Kopru, PAR_YOL
    kk = Kopru(gruplar={'DF': DF, 'PF': PF}, serbest=('ankle_flx',),
               par_yol=par_yol or PAR_YOL)
    if dt_kopru_ms is not None:                 # zaman adimi yarilama testi icin
        kk.dt_ms = dt_kopru_ms
        kk.dt_s = dt_kopru_ms * 1e-3
        kk.mek.dt = kk.dt_s
        kp = kk.par['kopru']
        n = len(kk.kaslar)
        from kopru import Gecikme
        kk.g_ia = Gecikme(round(kp['gecikme_ia_ms'] / dt_kopru_ms), n)
        kk.g_ii = Gecikme(round(kp['gecikme_ii_ms'] / dt_kopru_ms), n)
        kk.g_ef = Gecikme(round(kp['gecikme_efferent_ms'] / dt_kopru_ms), n)
    return kk


def ozet(kk, iz, yari_atla=True):
    """Kosuun sayisal ozeti. Gecici rejimi atmak icin varsayilan olarak ikinci yari alinir."""
    n = len(iz['t']) // 2 if yari_atla else 0
    t, q = iz['t'][n:], np.degrees(iz['q'][n:, 0])
    ix = {k: i for i, k in enumerate(kk.kaslar)}
    gr = {g: [ix[k] for k in kl] for g, kl in kk.gruplar.items()}
    u = {g: iz['u'][n:, j].mean(1) for g, j in gr.items()}
    gadlar = list(kk.gruplar)
    # cevrim suresi: bilek acisinin ortalama gecisleri
    e = q.mean()
    gec = np.where((q[:-1] < e) & (q[1:] >= e))[0]
    T = float(np.mean(np.diff(t[gec]))) if len(gec) > 2 else float('nan')
    # havuz basina ETKIN faz ortalama atesleme orani (kendi u'sunun ustunde oldugu adimlar)
    frek = {}
    for k in kk.kaslar:
        f = iz['f'][n:, ix[k]]
        etkin = f > 0.2 * f.max() if f.max() > 0 else np.zeros(len(f), bool)
        frek[k] = (float(f[etkin].mean()) if etkin.any() else 0.0, float(f.max()))
    return dict(T=T, aci_min=float(q.min()), aci_maks=float(q.max()), rom=float(q.max() - q.min()),
                korel_u=float(np.corrcoef(u[gadlar[0]], u[gadlar[1]])[0, 1]),
                u_ort={g: float(v.mean()) for g, v in u.items()}, frek=frek)


def figur(kk, iz, ad='kopru_ayakbilegi'):
    import matplotlib
    matplotlib.use('Agg')                       # 04_KURALLAR: figur Agg ile uretilir
    import matplotlib.pyplot as plt
    ix = {k: i for i, k in enumerate(kk.kaslar)}
    gr = {g: [ix[k] for k in kl] for g, kl in kk.gruplar.items()}
    t = iz['t']
    fig, ax = plt.subplots(4, 1, figsize=(9, 10), sharex=True)
    ax[0].plot(t, iz['vF'], lw=0.8, label='RG-F (dorsifleksor)')
    ax[0].plot(t, iz['vE'], lw=0.8, label='RG-E (plantar fleksor)')
    ax[0].set_ylabel('CPG [mV]'); ax[0].legend(fontsize=7, loc='upper right')
    ax[0].set_title('Ayak bileginde tam kapali dongu: CPG -> havuz -> kas -> hareket -> igcik -> Ia')
    for g, j in gr.items():
        ax[1].plot(t, iz['f'][:, j].mean(1), lw=0.8, label='havuz %s' % g)
    ax[1].set_ylabel('atesleme [Hz]'); ax[1].legend(fontsize=7, loc='upper right')
    for g, j in gr.items():
        ax[2].plot(t, iz['u'][:, j].mean(1), lw=0.8, label='u %s' % g)
    ax[2].set_ylabel('u(t) [birimsiz]'); ax[2].set_ylim(-0.05, 1.05)
    ax[2].legend(fontsize=7, loc='upper right')
    ax[3].plot(t, np.degrees(iz['q'][:, 0]), 'k', lw=1.0)
    ax[3].axhspan(-2.89, 30.65, color='0.85', zorder=0,
                  label='olculmus yuruyus araligi (PREPRINT 5.2)')
    ax[3].set_ylabel('ankle_flx [derece]'); ax[3].set_xlabel('zaman [s]')
    ax[3].legend(fontsize=7, loc='upper right')
    for a in ax:
        a.grid(alpha=0.3)
    fig.tight_layout()
    SEKILLER.mkdir(exist_ok=True)
    fig.savefig(SEKILLER / (ad + '.png'), dpi=300)      # 04_KURALLAR: 300 dpi
    # 04_KURALLAR: her figurun yaninda onu ureten sayisal veri CSV olarak
    bas = ['t_s', 'ankle_deg', 'vF_mV', 'vE_mV']
    sut = [t, np.degrees(iz['q'][:, 0]), iz['vF'], iz['vE']]
    for g, j in gr.items():
        bas += ['f_%s_Hz' % g, 'u_%s' % g]
        sut += [iz['f'][:, j].mean(1), iz['u'][:, j].mean(1)]
    np.savetxt(SEKILLER / (ad + '.csv'), np.column_stack(sut), delimiter=',',
               header=','.join(bas), comments='# ', fmt='%.6f')
    plt.close(fig)


if __name__ == '__main__':
    import time
    sure = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
    kk = kur()
    print('havuz          : %d (%s)' % (len(kk.havuz), ', '.join(kk.kaslar)))
    print('bolme/havuz    : %d segment' % list(kk.havuz.values())[0].hucre.segment_sayisi())
    print('kopru adimi    : %.3f ms | gecikme Ia %d adim, II %d, efferent %d'
          % (kk.dt_ms, kk.g_ia.n, kk.g_ii.n, kk.g_ef.n))
    print('moment kapasitesi: %s [N*mm] -> denge olcegi %s'
          % ({g: round(v, 2) for g, v in kk.kapasite.items()},
             {g: round(v, 3) for g, v in kk.denge.items()}))
    t0 = time.perf_counter()
    iz = kk.kos(sure, ilerleme=int(0.5 / kk.dt_s))
    print('kosu: %.1f s simulasyon -> %.1f s CPU' % (sure, time.perf_counter() - t0))

    o = ozet(kk, iz)
    print('\n--- ikinci yari (gecici rejim atildi) ---')
    print('cevrim suresi   : %.3f s   (olculmus yuruyus cevrimi 0.387 s)' % o['T'])
    print('bilek acisi     : %.2f .. %.2f derece (ROM %.2f)' % (o['aci_min'], o['aci_maks'], o['rom']))
    print('u_DF - u_PF korelasyonu: %+.3f  (zitfaz beklenir)' % o['korel_u'])
    print('\n%-6s %12s %12s' % ('kas', 'f_etkin Hz', 'f_maks Hz'))
    for k in kk.kaslar:
        print('%-6s %12.2f %12.2f' % (k, o['frek'][k][0], o['frek'][k][1]))

    VERI_KOPRU.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(VERI_KOPRU / 'kosu_ayakbilegi.npz', kaslar=np.array(kk.kaslar), **iz)
    figur(kk, iz)
    print('\nyazildi: veri/kopru/kosu_ayakbilegi.npz, sekiller/kopru_ayakbilegi.{png,csv}')
