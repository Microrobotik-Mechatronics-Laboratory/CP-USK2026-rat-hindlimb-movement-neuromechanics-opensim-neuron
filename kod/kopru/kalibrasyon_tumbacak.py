# =============================================================================
# kalibrasyon_tumbacak.py — f_ref sabitken pf_mn / cpg_pf_carpan / k_ia taramasinin TEK kosusu.
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru)
# Girdi:  kod/kopru/devre_par.json (taban), komut satiri parametreleri
# Cikti:  stdout'a tek satir JSON (skor + olcumler); tarama tablosu DOGRULAMA'ya islenir.
#
# NEDEN BU YAPI: NEURON durumu surec icinde birikir; her parametre noktasi TEMIZ bir
# surecte kosulmalidir. Bu betik tek nokta kosar; taramayi ust kabuk paralel yurutur.
#
# KALIBRASYON HEDEFI (DOGRULAMA P.9 teshisi: havuz az atesliyor, kas fazla is yapiyor):
#   - f_ref SABIT tutulur -- Gorassini degerleri fizyolojik CAPADIR, hedeftir (kalibre edilmez).
#   - pf_mn buyutulerek havuz frekanslari Gorassini araliklarina cekilir;
#   - cpg_pf_carpan / k_ia ile cevrim suresi ve eklem ROM ortusmesi ayarlanir.
# Araliklar literatur/referans_degerler.json'dan okunur; POST-HOC GENISLETME YASAK
# (SDLC/04_KURALLAR). Skor kucuk = iyi.
# =============================================================================
import sys, json, argparse, pathlib, tempfile, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np


def skorla(o, ref):
    """Kucuk = iyi. Bilesenler ayri ayri da raporlanir (secim tabloyla yapilir)."""
    import math
    fs = 0.0
    frek_durum = {}
    for kas, kimlik in (('TA', 'gorassini2000.mn_frekans_TA_swing'),
                        ('Sol', 'gorassini2000.mn_frekans_SOL_yuruyus'),
                        ('MG', 'gorassini2000.mn_frekans_MGLG_ortagec'),
                        ('LG', 'gorassini2000.mn_frekans_MGLG_ortagec')):
        r = ref[kimlik]
        f = o['frek'][kas][0]
        icinde = r['aralik'][0] <= f <= r['aralik'][1]
        uzak = 0.0 if icinde else abs(math.log(max(f, 0.5) / r['deger']))
        fs += uzak
        frek_durum[kas] = dict(f=round(f, 2), aralikta=bool(icinde), uzaklik=round(uzak, 3))
    rs = 1.0 - float(np.mean([e['ortusme'] for e in o['eklemler'].values()]))
    ck = ref['ic.kopru_cevrim_suresi']
    T = o['T']
    if not np.isfinite(T):
        ts = 2.0
    elif ck['aralik'][0] <= T <= ck['aralik'][1]:
        ts = 0.0
    else:
        ts = abs(T - ck['deger']) / ck['deger']
    return dict(skor=round(fs + rs + ts, 4), frekans_skoru=round(fs, 4),
                rom_skoru=round(rs, 4), cevrim_skoru=round(ts, 4), frek_durum=frek_durum)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--pf_mn', type=float, default=None)
    ap.add_argument('--cpg_pf', type=float, default=None)
    ap.add_argument('--k_ia', type=float, default=None)
    ap.add_argument('--sure', type=float, default=1.5)
    ap.add_argument('--etiket', default='')
    args = ap.parse_args()

    taban = pathlib.Path(__file__).resolve().parent / 'devre_par.json'
    par = json.load(open(taban))
    if args.pf_mn is not None:
        par['sinaps']['agirlik_uS']['pf_mn'] = args.pf_mn
    if args.cpg_pf is not None:
        par['sinaps']['cpg_pf_carpan'] = args.cpg_pf
    if args.k_ia is not None:
        par['kopru']['k_ia'] = args.k_ia
    tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
    json.dump(par, tmp)
    tmp.close()

    import kos_tumbacak as KT
    ref = KT.referanslar()
    t0 = time.perf_counter()
    kk = KT.kur(par_yol=tmp.name)
    iz = kk.kos(args.sure, kas_kaydi=False)      # kalibrasyonda kas kaydi kapali (CPU)
    cpu = time.perf_counter() - t0
    o = KT.ozet(kk, iz)
    s = skorla(o, ref)
    cikti = dict(etiket=args.etiket,
                 pf_mn=par['sinaps']['agirlik_uS']['pf_mn'],
                 cpg_pf=par['sinaps']['cpg_pf_carpan'],
                 k_ia=par['kopru']['k_ia'],
                 sure=args.sure, cpu_s=round(cpu, 1),
                 T=None if not np.isfinite(o['T']) else round(o['T'], 4),
                 eklemler={ad: dict(aralik=[round(v, 2) for v in e['aralik']],
                                    ortusme=round(e['ortusme'], 3),
                                    sinir_yakin=round(e.get('sinir_yakin', 0.0), 3))
                           for ad, e in o['eklemler'].items()},
                 korel={k: round(v, 3) for k, v in o['korel'].items()},
                 biart_u_tepe={k: round(v, 3) for k, v in o['biart'].items()},
                 **s)
    print('KALIB ' + json.dumps(cikti))
