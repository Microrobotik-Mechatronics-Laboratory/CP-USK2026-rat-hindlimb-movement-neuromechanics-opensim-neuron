# =============================================================================
# adim_yarilama.py — zaman adimi yarilama testi (step-halving convergence check).
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru)
# Kullanim: adim_yarilama.py [sure_s]              -> ayak bilegi kosucusu (1 DOF, 10 havuz)
#           adim_yarilama.py [sure_s] --tumbacak   -> tum bacak kosucusu (3 DOF, 38 havuz)
# Cikti: ekrana karsilastirma tablosu; aralık disina cikilirsa assert duser.
#
# NEDEN ZORUNLU (PREPRINT bolum 8): iki simulator DISSAL olarak kuplenmistir; ortak bir
# Jacobian kurulamaz ve pointer/alisveris tabanli kuplaj Jacobian'in capraz terimlerini
# dusurur (oz_fietkiewicz2023 3b madde 8). Bu, sonucun zaman adimina bagli olmasi riskini
# dogurur. Kullanicinin sonucun adimdan bagimsiz oldugunu HER ZAMAN dogrulamasi gerekir.
#
# NE KARSILASTIRILIR: yorunge degil, MAKROSKOPIK olcutler. Aksiyon potansiyeli tabanli bir
# devrede iki farkli adimla birebir ayni yorunge beklenmez; beklenen, cevrim suresi / ROM /
# atesleme oranlarinin degismemesidir. Cok eklemde ROM olcutu EKLEM BASINA ayri sinanir.
#
# ARALIK (testten ONCE ilan edildi, ic_olcum regresyon araligi):
#   cevrim suresi        : bagil fark < %5
#   eklem ROM (her eklem): bagil fark < %10
#   grup atesleme orani  : bagil fark < %10
# Gerekce: bu bir SAYISAL yakinsama testidir, literatur karsilastirmasi degil. Aralıklar,
# NEURON adimi (0.025 ms) degismeden yalniz ALISVERIS adimi yarilandiginda beklenen
# kalinti farki kapsar; daha genis bir fark kuplajin adima bagimli oldugunu gosterir.
# =============================================================================
import sys, pathlib, time, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np

ARALIK_T, ARALIK_ROM, ARALIK_F = 0.05, 0.10, 0.10


def kos(K, dt_ms, sure, tumbacak):
    kk = K.kur(dt_kopru_ms=dt_ms)
    t0 = time.perf_counter()
    iz = kk.kos(sure, kas_kaydi=False) if tumbacak else kk.kos(sure)
    o = K.ozet(kk, iz)
    roms = ({ad: e['rom'] for ad, e in o['eklemler'].items()} if tumbacak
            else {'ankle_flx': o['rom']})
    frek = {g: float(np.mean([o['frek'][k][0] for k in kl])) for g, kl in kk.gruplar.items()}
    return dict(T=o['T'], roms=roms, frek=frek, cpu=time.perf_counter() - t0, dt=dt_ms)


if __name__ == '__main__':
    argv = [a for a in sys.argv[1:] if not a.startswith('--')]
    tumbacak = '--tumbacak' in sys.argv
    sure = float(argv[0]) if argv else 3.0
    if tumbacak:
        import kos_tumbacak as K
    else:
        import kos_ayakbilegi as K
    # Uretim adimi devre_par.json'dan okunur; test onu ve YARISINI karsilastirir.
    dt0 = json.load(open(pathlib.Path(__file__).resolve().parent / 'devre_par.json'))['kopru']['dt_kopru_ms']
    a = kos(K, dt0, sure, tumbacak)
    b = kos(K, dt0 / 2.0, sure, tumbacak)
    bagil = lambda x, y: abs(x - y) / max(abs(x), abs(y), 1e-12)

    print('\nkosucu: %s' % ('kos_tumbacak (3 DOF, 38 havuz)' if tumbacak
                            else 'kos_ayakbilegi (1 DOF, 10 havuz)'))
    print('%-26s %14s %14s %10s' % ('olcut', 'dt_k=%.3f ms' % dt0,
                                    'dt_k=%.4f ms' % (dt0 / 2), 'bagil fark'))
    print('%-26s %14.4f %14.4f %9.2f%%' % ('cevrim suresi [s]', a['T'], b['T'],
                                           100 * bagil(a['T'], b['T'])))
    for ad in a['roms']:
        print('%-26s %14.2f %14.2f %9.2f%%'
              % ('ROM %s [derece]' % ad, a['roms'][ad], b['roms'][ad],
                 100 * bagil(a['roms'][ad], b['roms'][ad])))
    for g in a['frek']:
        print('%-26s %14.2f %14.2f %9.2f%%'
              % ('havuz %s [Hz]' % g, a['frek'][g], b['frek'][g],
                 100 * bagil(a['frek'][g], b['frek'][g])))
    print('%-26s %14.1f %14.1f %10s' % ('CPU [s]', a['cpu'], b['cpu'], '-'))

    # Artefakt ASSERT'LERDEN ONCE yazilir: testin DUSTUGU durumda da sayilar figure ve
    # rapora girer -- dusen bir olcut de bir olcum sonucudur, saklanmaz (04_KURALLAR).
    from yollar import VERI_KOPRU
    VERI_KOPRU.mkdir(parents=True, exist_ok=True)
    with open(VERI_KOPRU / 'yakinsama_zaman.json', 'w') as fh:
        json.dump(dict(tur='zaman adimi yarilama (step-halving)',
                       kosucu='kos_tumbacak' if tumbacak else 'kos_ayakbilegi',
                       sure_s=sure, dt_ms=[a['dt'], b['dt']],
                       bantlar=dict(T=ARALIK_T, ROM=ARALIK_ROM, frekans=ARALIK_F),
                       a=a, b=b), fh, indent=1)
    print('yazildi: veri/kopru/yakinsama_zaman.json')

    assert bagil(a['T'], b['T']) < ARALIK_T, (
        'cevrim suresi adima bagli: olculen bagil fark=%.4f, beklenen=0, aralık=[0, %.2f], '
        'kaynak=ic_olcum sayisal yakinsama araligi' % (bagil(a['T'], b['T']), ARALIK_T))
    for ad in a['roms']:
        assert bagil(a['roms'][ad], b['roms'][ad]) < ARALIK_ROM, (
            'eklem %s ROM adima bagli: olculen bagil fark=%.4f, beklenen=0, aralık=[0, %.2f], '
            'kaynak=ic_olcum sayisal yakinsama araligi'
            % (ad, bagil(a['roms'][ad], b['roms'][ad]), ARALIK_ROM))
    for g in a['frek']:
        assert bagil(a['frek'][g], b['frek'][g]) < ARALIK_F, (
            'havuz %s atesleme orani adima bagli: olculen bagil fark=%.4f, beklenen=0, '
            'aralık=[0, %.2f], kaynak=ic_olcum sayisal yakinsama araligi'
            % (g, bagil(a['frek'][g], b['frek'][g]), ARALIK_F))
    print('\nADIM YARILAMA TESTI GECTI: sonuc kopru adimindan bagimsiz.')
