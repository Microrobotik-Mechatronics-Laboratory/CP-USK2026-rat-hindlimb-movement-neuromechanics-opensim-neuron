# =============================================================================
# figur_tumbacak.py — 38 havuz / 3 DOF kosusunun kanit figurleri.
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru) -- saf NumPy + matplotlib
# Girdi:  veri/kopru/kosu_tumbacak.npz (kos_tumbacak.py uretir)
# Cikti:  sekiller/kopru_tumbacak_raster.png|csv        (tum noron tiplerinin aktivitesi)
#         sekiller/kopru_tumbacak_nedensellik.png|csv   (spike -> u -> aktivasyon -> kuvvet -> aci)
#         sekiller/kopru_tumbacak_pasif.png|csv         (canli vs u=0 pasif kontrol)
#
# 04_KURALLAR: Agg backend, cikti DAIMA sekiller/, 300 dpi, her figurun yaninda kaynak CSV.
#
# FIGURLERIN AMACI: hareketin gercekten noronlar tarafindan uretildigini gostermek.
#   raster      : CPG voltaji -> internoron spike'lari -> 38 havuzun spike'lari -> eklem acisi
#   nedensellik : secili kaslarda zincirin her halkasi ayni zaman ekseninde
#   pasif       : ayni model, u=0 -> ritmik hareket YOK; noron surusuyle VAR
# BILINEN SAPMALAR: IaIN/Renshaw [tasarim] (kaynaksiz; iddia edilmez), II [varsayim].
# =============================================================================
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from yollar import VERI_KOPRU, SEKILLER

SERBEST_AD = {'hip_flx': 'kalca', 'knee_flx': 'diz', 'ankle_flx': 'bilek'}
OLCULMUS = {'hip_flx': (9.01, 65.42), 'knee_flx': (-139.73, -107.65),
            'ankle_flx': (-2.89, 30.65)}          # PREPRINT 5.2
GRUP_RENK = {'kalca_flx': 'tab:red', 'kalca_ext': 'tab:blue',
             'diz_flx': 'tab:orange', 'diz_ext': 'tab:cyan',
             'bilek_df': 'tab:green', 'bilek_pf': 'tab:purple', 'surussuz': '0.6'}


def yukle():
    d = np.load(VERI_KOPRU / 'kosu_tumbacak.npz', allow_pickle=True)
    kaslar = [str(x) for x in d['kaslar']]
    gruplar = json.loads(str(d['gruplar']))
    surussuz = [str(x) for x in d['surussuz']]
    return d, kaslar, gruplar, surussuz


def kas_sirasi(kaslar, gruplar, surussuz):
    """Raster icin kaslar eklem grubuna gore siralanir; biartikuler ilk grubunda kalir."""
    sira, grup_of = [], {}
    for gad, kl in gruplar.items():
        for k in kl:
            if k not in grup_of:
                grup_of[k] = gad
                sira.append(k)
    for k in surussuz:
        grup_of[k] = 'surussuz'
        sira.append(k)
    assert set(sira) == set(kaslar)
    return sira, grup_of


def figur_raster(d, kaslar, gruplar, surussuz, ad='kopru_tumbacak_raster'):
    t = d['t']
    sira, grup_of = kas_sirasi(kaslar, gruplar, surussuz)
    yix = {k: i for i, k in enumerate(sira)}
    kix = {k: j for j, k in enumerate(kaslar)}
    st, sk = d['spike_t'], d['spike_kas']
    in_t, in_ix = d['in_spike_t'], d['in_spike_ix']
    in_adlar = [str(x) for x in d['in_adlar']]

    fig, ax = plt.subplots(4, 1, figsize=(11, 13), sharex=True,
                           gridspec_kw=dict(height_ratios=[1.2, 1.6, 5.0, 1.6]))
    ax[0].plot(t, d['vF'], lw=0.7, label='RG-F (fleksor yarim-merkezi)')
    ax[0].plot(t, d['vE'], lw=0.7, label='RG-E (ekstansor yarim-merkezi)')
    ax[0].set_ylabel('CPG [mV]')
    ax[0].legend(fontsize=7, loc='upper right')
    ax[0].set_title('Tam bacak kapali dongusu: CPG -> internoronlar -> 38 motonoron havuzu -> '
                    'kas -> hareket -> igcik -> Ia/II')

    for j, adx in enumerate(in_adlar):
        z = in_t[in_ix == j]
        ax[1].plot(z, np.full(len(z), j), '|', ms=4, mew=0.8,
                   color='k' if adx.startswith('PF') else
                         ('tab:red' if adx.startswith('IaIN') else
                          ('tab:blue' if adx.startswith('RC') else 'tab:green')))
    ax[1].set_yticks(range(len(in_adlar)))
    ax[1].set_yticklabels(in_adlar, fontsize=5)
    ax[1].set_ylabel('internoron')
    ax[1].text(0.995, 0.02, 'IaIN/Renshaw [tasarim] - kaynaksiz, iddia edilmez',
               transform=ax[1].transAxes, ha='right', va='bottom', fontsize=6, color='0.4')

    for k in sira:
        z = st[sk == kix[k]]
        ax[2].plot(z, np.full(len(z), yix[k]), '|', ms=4, mew=0.8,
                   color=GRUP_RENK[grup_of[k]])
    ax[2].set_yticks(range(len(sira)))
    ax[2].set_yticklabels(sira, fontsize=5)
    ax[2].set_ylabel('motonoron havuzu (38)')
    ax[2].invert_yaxis()
    icik = [plt.Line2D([0], [0], color=r, lw=3) for r in GRUP_RENK.values()]
    ax[2].legend(icik, list(GRUP_RENK), fontsize=6, loc='upper right', ncol=4)

    serbest = [str(x) for x in d['serbest']]
    for j, kd in enumerate(serbest):
        ax[3].plot(t, np.degrees(d['q'][:, j]), lw=1.0, label=SERBEST_AD[kd])
    ax[3].set_ylabel('eklem [derece]')
    ax[3].set_xlabel('zaman [s]')
    ax[3].legend(fontsize=7, loc='upper right')
    for a in ax:
        a.grid(alpha=0.25)
    fig.tight_layout()
    SEKILLER.mkdir(exist_ok=True)
    fig.savefig(SEKILLER / (ad + '.png'), dpi=300)
    plt.close(fig)

    # kaynak CSV: satir basina bir aksiyon potansiyeli (havuz + internoron)
    with open(SEKILLER / (ad + '.csv'), 'w') as f:
        f.write('# %s.png kaynak verisi: aksiyon potansiyeli zamanlari\n' % ad)
        f.write('t_s,kaynak,ad,grup\n')
        for z, j in zip(st, sk):
            k = kaslar[int(j)]
            f.write('%.6f,havuz,%s,%s\n' % (z, k, grup_of[k]))
        for z, j in zip(in_t, in_ix):
            f.write('%.6f,internoron,%s,-\n' % (z, in_adlar[int(j)]))


def figur_nedensellik(d, kaslar, gruplar, surussuz, secili=('TA', 'Sol', 'IP', 'VL'),
                      ad='kopru_tumbacak_nedensellik'):
    t = d['t']
    kix = {k: j for j, k in enumerate(kaslar)}
    st, sk = d['spike_t'], d['spike_kas']
    serbest = [str(x) for x in d['serbest']]
    kas_eklem = {'TA': 'ankle_flx', 'Sol': 'ankle_flx', 'IP': 'hip_flx', 'VL': 'knee_flx'}

    nk = len(secili)
    fig = plt.figure(figsize=(3.2 * nk, 11))
    gs = fig.add_gridspec(5, nk, height_ratios=[0.8, 1, 1, 1, 1.3], hspace=0.35, wspace=0.3)
    for c, k in enumerate(secili):
        j = kix[k]
        a0 = fig.add_subplot(gs[0, c])
        z = st[sk == j]
        a0.plot(z, np.zeros(len(z)), '|k', ms=10, mew=0.9)
        a0.set_yticks([])
        a0.set_title('%s' % k, fontsize=10)
        if c == 0:
            a0.set_ylabel('spike', fontsize=8)
        a1 = fig.add_subplot(gs[1, c], sharex=a0)
        a1.plot(t, d['f'][:, j], lw=0.8, color='tab:blue')
        if c == 0:
            a1.set_ylabel('f [Hz]', fontsize=8)
        a2 = fig.add_subplot(gs[2, c], sharex=a0)
        a2.plot(t, d['u'][:, j], lw=0.8, color='tab:orange', label='u (uyarim)')
        a2.plot(t, d['akt'][:, j], lw=0.8, color='tab:red', label='aktivasyon')
        a2.set_ylim(-0.05, 1.05)
        if c == 0:
            a2.set_ylabel('u / aktivasyon', fontsize=8)
        a2.legend(fontsize=6, loc='upper right')
        a3 = fig.add_subplot(gs[3, c], sharex=a0)
        a3.plot(t, d['Fkas'][:, j], lw=0.8, color='tab:green')
        if c == 0:
            a3.set_ylabel('tendon kuvveti [N]', fontsize=8)
        a4 = fig.add_subplot(gs[4, c], sharex=a0)
        je = serbest.index(kas_eklem[k])
        a4.plot(t, np.degrees(d['q'][:, je]), lw=0.9, color='k')
        a4.set_xlabel('zaman [s]', fontsize=8)
        if c == 0:
            a4.set_ylabel('eklem acisi [derece]', fontsize=8)
        a4.set_title(SERBEST_AD[kas_eklem[k]], fontsize=8)
        for a in (a0, a1, a2, a3, a4):
            a.grid(alpha=0.25)
            a.tick_params(labelsize=7)
    fig.suptitle('Nedensellik zinciri: motonoron aksiyon potansiyeli -> atesleme orani -> '
                 'u(t) -> kas aktivasyonu -> tendon kuvveti -> eklem acisi', fontsize=10)
    fig.savefig(SEKILLER / (ad + '.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)

    bas = ['t_s']
    sut = [t]
    for k in secili:
        j = kix[k]
        bas += ['f_%s_Hz' % k, 'u_%s' % k, 'akt_%s' % k, 'Fkas_%s_N' % k]
        sut += [d['f'][:, j], d['u'][:, j], d['akt'][:, j], d['Fkas'][:, j]]
    for jq, kd in enumerate(serbest):
        bas.append('%s_derece' % kd)
        sut.append(np.degrees(d['q'][:, jq]))
    np.savetxt(SEKILLER / (ad + '.csv'), np.column_stack(sut), delimiter=',',
               header=','.join(bas), comments='# ', fmt='%.6f')


def figur_pasif(d, ad='kopru_tumbacak_pasif'):
    t, tp = d['t'], d['pasif_t']
    serbest = [str(x) for x in d['serbest']]
    fig, ax = plt.subplots(len(serbest), 1, figsize=(10, 8.5), sharex=True)
    for j, kd in enumerate(serbest):
        qc = np.degrees(d['q'][:, j])
        qp = np.degrees(d['pasif_q'][:, j])
        ax[j].axhspan(*OLCULMUS[kd], color='0.88', zorder=0,
                      label='olculmus yuruyus araligi (PREPRINT 5.2)')
        ax[j].plot(t, qc, lw=1.0, color='tab:red',
                   label='noron suruslu (canli) - ROM %.1f' % (qc.max() - qc.min()))
        ax[j].plot(tp, qp, lw=1.0, color='0.3', ls='--',
                   label='pasif (u=0, noron yok) - ROM %.1f' % (qp.max() - qp.min()))
        ax[j].set_ylabel('%s [derece]' % SERBEST_AD[kd])
        ax[j].legend(fontsize=7, loc='upper right')
        ax[j].grid(alpha=0.25)
    ax[0].set_title('Ayni model, ayni baslangic: hareket yalniz noron surusuyle doguyor')
    ax[-1].set_xlabel('zaman [s]')
    fig.tight_layout()
    fig.savefig(SEKILLER / (ad + '.png'), dpi=300)
    plt.close(fig)

    bas = ['t_s'] + ['canli_%s_derece' % k for k in serbest] + \
          ['pasif_%s_derece' % k for k in serbest]
    n = min(len(t), len(tp))
    sut = [t[:n]] + [np.degrees(d['q'][:n, j]) for j in range(len(serbest))] + \
          [np.degrees(d['pasif_q'][:n, j]) for j in range(len(serbest))]
    np.savetxt(SEKILLER / (ad + '.csv'), np.column_stack(sut), delimiter=',',
               header=','.join(bas), comments='# ', fmt='%.6f')


if __name__ == '__main__':
    d, kaslar, gruplar, surussuz = yukle()
    figur_raster(d, kaslar, gruplar, surussuz)
    figur_nedensellik(d, kaslar, gruplar, surussuz)
    figur_pasif(d)
    print('yazildi: sekiller/kopru_tumbacak_{raster,nedensellik,pasif}.{png,csv}')
