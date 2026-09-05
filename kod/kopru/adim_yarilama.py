# =============================================================================
# adim_yarilama.py — zaman adimi yarilama testi (step-halving convergence check).
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru)
# Cikti: ekrana karsilastirma tablosu; aralık disina cikilirsa assert duser.
#
# NEDEN ZORUNLU (PREPRINT bolum 8): iki simulator DISSAL olarak kuplenmistir; ortak bir
# Jacobian kurulamaz ve pointer/alisveris tabanli kuplaj Jacobian'in capraz terimlerini
# dusurur (oz_fietkiewicz2023 3b madde 8). Bu, sonucun zaman adimina bagli olmasi riskini
# dogurur. Kullanicinin sonucun adimdan bagimsiz oldugunu HER ZAMAN dogrulamasi gerekir.
#
# NE KARSILASTIRILIR: yorunge degil, MAKROSKOPIK olcutler. Aksiyon potansiyeli tabanli bir devrede iki
# farkli adimla birebir ayni yorunge beklenmez; beklenen, cevrim suresi / ROM / atesleme
# oranlarinin degismemesidir.
#
# ARALIK (testten ONCE ilan edildi, ic_olcum regresyon araligi):
#   cevrim suresi        : bagil fark < %5
#   eklem ROM            : bagil fark < %10
#   grup atesleme orani  : bagil fark < %10
# Gerekce: bu bir SAYISAL yakinsama testidir, literatur karsilastirmasi degil. Aralıklar,
# NEURON adimi (0.025 ms) degismeden yalniz ALISVERIS adimi yarilandiginda beklenen
# kalinti farki kapsar; daha genis bir fark kuplajin adima bagimli oldugunu gosterir.
# =============================================================================
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import kos_ayakbilegi as KA

ARALIK_T, ARALIK_ROM, ARALIK_F = 0.05, 0.10, 0.10


def kos(dt_ms, sure):
    kk = KA.kur(dt_kopru_ms=dt_ms)
    t0 = time.perf_counter()
    iz = kk.kos(sure)
    o = KA.ozet(kk, iz)
    o['cpu'] = time.perf_counter() - t0
    o['dt'] = dt_ms
    o['gruplar'] = kk.gruplar
    return o


if __name__ == '__main__':
    sure = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
    # Uretim adimi devre_par.json'dan okunur; test onu ve YARISINI karsilastirir.
    import json
    dt0 = json.load(open(pathlib.Path(__file__).resolve().parent / 'devre_par.json'))['kopru']['dt_kopru_ms']
    a = kos(dt0, sure)
    b = kos(dt0 / 2.0, sure)
    bagil = lambda x, y: abs(x - y) / max(abs(x), abs(y), 1e-12)

    print('\n%-24s %14s %14s %10s' % ('olcut', 'dt_k=%.3f ms' % dt0, 'dt_k=%.4f ms' % (dt0 / 2), 'bagil fark'))
    print('%-24s %14.4f %14.4f %9.2f%%' % ('cevrim suresi [s]', a['T'], b['T'], 100 * bagil(a['T'], b['T'])))
    print('%-24s %14.2f %14.2f %9.2f%%' % ('eklem ROM [derece]', a['rom'], b['rom'], 100 * bagil(a['rom'], b['rom'])))
    print('%-24s %14.3f %14.3f %10s' % ('u zitfaz korelasyonu', a['korel_u'], b['korel_u'], '-'))
    fa = {g: np.mean([a['frek'][k][0] for k in kl]) for g, kl in a['gruplar'].items()}
    fb = {g: np.mean([b['frek'][k][0] for k in kl]) for g, kl in b['gruplar'].items()}
    for g in fa:
        print('%-24s %14.2f %14.2f %9.2f%%' % ('havuz %s atesleme [Hz]' % g, fa[g], fb[g],
                                               100 * bagil(fa[g], fb[g])))
    print('%-24s %14.1f %14.1f %10s' % ('CPU [s]', a['cpu'], b['cpu'], '-'))

    assert bagil(a['T'], b['T']) < ARALIK_T, (
        'cevrim suresi adima bagli: olculen bagil fark=%.4f, beklenen=0, aralık=[0, %.2f], '
        'kaynak=ic_olcum sayisal yakinsama araligi' % (bagil(a['T'], b['T']), ARALIK_T))
    assert bagil(a['rom'], b['rom']) < ARALIK_ROM, (
        'eklem ROM adima bagli: olculen bagil fark=%.4f, beklenen=0, aralık=[0, %.2f], '
        'kaynak=ic_olcum sayisal yakinsama araligi' % (bagil(a['rom'], b['rom']), ARALIK_ROM))
    for g in fa:
        assert bagil(fa[g], fb[g]) < ARALIK_F, (
            'havuz %s atesleme orani adima bagli: olculen bagil fark=%.4f, beklenen=0, '
            'aralık=[0, %.2f], kaynak=ic_olcum sayisal yakinsama araligi'
            % (g, bagil(fa[g], fb[g]), ARALIK_F))
    print('\nADIM YARILAMA TESTI GECTI: sonuc kopru adimindan bagimsiz.')
