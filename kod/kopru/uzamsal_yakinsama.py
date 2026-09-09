# =============================================================================
# uzamsal_yakinsama.py — uzamsal cozunurluk (d_lambda) yakinsama testi.
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru)
# Kullanim: uzamsal_yakinsama.py [sure_s]              -> ayak bilegi kosucusu (1 DOF, 10 havuz)
#           uzamsal_yakinsama.py [sure_s] --tumbacak   -> tum bacak kosucusu (3 DOF, 38 havuz)
#           uzamsal_yakinsama.py [sure_s] --dl 1.0     -> aday cozunurluk (JSON yerine)
#           uzamsal_yakinsama.py [sure_s] --tek 1.0    -> ic kullanim: tek nokta, JSON basar
# Cikti: ekrana karsilastirma tablosu; aralık disina cikilirsa assert duser.
#
# NEDEN: PREPRINT bolum 8 ZAMANSAL yakinsama testini (adim yarilama) zorunlu sayar; bu onun
# UZAMSAL karsiligidir. Motonoronun segment sayisi CPU maliyetini dogrudan belirliyor
# (DOGRULAMA S.1: butcenin %82'si NEURON) ve kabalastirma iki yerden sonuca sizabilir:
#   1) PIC nokta sureci -- Kim'in formulu yogunluk x SEGMENT ALANI kullaniyor, yani nseg'e
#      bagli. Bu, nrn_hucre.py'de referans tabloyla giderildi (toplam PIC cozunurlukten
#      bagimsiz); test bunu dogrular (raporlanan "PIC toplam" iki tarafta esit olmali).
#   2) PIC KONUMU -- nokta, hedefe en yakin segment MERKEZINE duser; kaba izgarada hedeften
#      uzaklasir (olculdu: |D_path-600| ort 9.8 -> 63.4 um, maks 29.2 -> 259.4 um). Bu
#      duzeltilemez ve Kim'in duyarli oldugu eksendir (oz_kim2020 4b, Tip I/IV/III).
#      Asama A tam da bunu sinar.
#
# NE KARSILASTIRILIR: yorunge degil, MAKROSKOPIK olcutler (adim_yarilama.py ile ayni gerekce).
#   Asama A (tek hucre, ucuz): reobaz, f-I noktalari, PIC histerezisi.
#   Asama B (kopru): cevrim suresi, eklem basina ROM, grup atesleme orani.
#
# ARALIKLAR (testten ONCE ilan edildi, ic_olcum regresyon araligi):
#   reobaz               : bagil fark < %10
#   f-I noktalari        : bagil fark < %10
#   PIC histerez KATEGORI: ayni olmali (var/yok). Esik: dI > 0.1 x I_onset ise "var".
#   cevrim suresi        : bagil fark < %5
#   eklem ROM (her eklem): bagil fark < %10
#   grup atesleme orani  : bagil fark < %10
# Gerekce: bu bir SAYISAL yakinsama testidir, literatur karsilastirmasi degil. Kopru
# bantlari adim_yarilama.py ile ayni tutuldu -- ayni sinif bir yakinsama sinamasidir ve iki
# testin sonucu ancak ayni bantla karsilastirilabilir. Tek hucre bantlari ayni mertebede
# secildi. Histerezisin BUYUKLUGU assert edilmez, yalniz raporlanir: dI iki esigin farkidir,
# bagil hatasi yukselir; literaturle iliskili olan nicelik kategoridir (Kim Tip I/IV/III).
#
# NEDEN AYRI SUREC: NEURON ve OpenSim durumu surec icinde birikir; DOGRULAMA S.5 ayni surecte
# ikinci bir kos() cagrisinin Manager.initialize icinde dustugunu kaydediyor. Bu yuzden her
# d_lambda noktasi kendi surecinde kosar (ayrica iki kosu paralel gider, duvar saati yarilanir).
# =============================================================================
import sys, json, time, pathlib, tempfile, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np

ARALIK_T, ARALIK_ROM, ARALIK_F = 0.05, 0.10, 0.10        # kopru duzeyi
ARALIK_REOBAZ, ARALIK_FI = 0.10, 0.10                    # tek hucre
HISTEREZIS_ESIK = 0.10                                   # dI / I_onset -> "var" kategorisi
PAR_YOL = pathlib.Path(__file__).resolve().parent / 'devre_par.json'
D_LAMBDA_REF = 0.1                                       # Kim'in fixnseg.hoc degeri
FI_CARPAN = (1.5, 2.0)                                   # reobazin kati olarak f-I noktalari
RAMPA_MS, RAMPA_KAT = 6000.0, 2.5                        # ucgen rampa suresi ve tepe/reobaz


# ==================== Asama A: tek hucre ====================================================
def _spike_say(h, kayit, ms):
    kayit.resize(0)
    h.finitialize(-70.0)
    h.continuerun(ms)
    return np.array(kayit)


def tek_hucre_olc(dl):
    """Bir motonoronu kurar ve PIC'e duyarli uc olcumu doner. Hucre sonunda birakilir."""
    import nrn_hucre
    from nrn_ortam import h
    hucre = nrn_hucre.MotoNoron('UY%g' % dl, d_lambda=dl, pic_ref_d_lambda=D_LAMBDA_REF)
    h.dt = 0.025
    kayit = hucre.ap_kaydet()
    ic = h.IClamp(hucre.soma(0.5))
    ic.delay, ic.dur, ic.amp = 0.0, 1e9, 0.0

    # reobaz: ikili arama (0.5 s'lik basamakta en az bir aksiyon potansiyeli)
    alt, ust = 0.0, 30.0
    assert len(_spike_say(h, kayit, 500.0)) == 0, 'hucre uyarimsiz atesliyor'
    ic.amp = ust
    assert len(_spike_say(h, kayit, 500.0)) > 0, 'reobaz 30 nA ustunde, arama araligi dar'
    for _ in range(12):                       # 30/2^12 = 0.007 nA cozunurluk
        orta = 0.5 * (alt + ust)
        ic.amp = orta
        if len(_spike_say(h, kayit, 500.0)) > 0:
            ust = orta
        else:
            alt = orta
    reo = ust

    # f-I: reobazin katlarinda kararli faz atesleme orani (ilk 100 ms gecici rejim atilir)
    fi = []
    for c in FI_CARPAN:
        ic.amp = c * reo
        z = _spike_say(h, kayit, 500.0)
        z = z[z > 100.0]
        fi.append(float(len(z) / 0.4) if len(z) else 0.0)
    ic.amp = 0.0

    # PIC histerezisi: ucgen rampa (RampIClamp -- Kim'in kendi mekanizmasi, fig2_4_6)
    # RampIClamp'in gecikme parametresinin adi 'del' -- Python anahtar kelimesi oldugu icin
    # oznitelik olarak yazilamaz; varsayilani 0 ve rampanin hemen baslamasi zaten istenen.
    rmp = h.RampIClamp(hucre.soma(0.5))
    rmp.dur, rmp.pkamp, rmp.bias = RAMPA_MS, RAMPA_KAT * reo, 0.0
    z = _spike_say(h, kayit, RAMPA_MS)
    if len(z) >= 2:
        i_on = 2 * rmp.pkamp / RAMPA_MS * z[0]                       # cikista ilk AP akimi
        i_off = -2 * rmp.pkamp / RAMPA_MS * (z[-1] - RAMPA_MS)       # inişte son AP akimi
        dI = i_on - i_off
        kategori = 'var' if dI > HISTEREZIS_ESIK * i_on else 'yok'
    else:
        i_on = i_off = dI = float('nan')
        kategori = 'atesleme yok'

    h.distance(0, hucre.soma(0))
    dpath_hata = np.array([abs(h.distance(hucre.soma(0), p.get_segment()) - hucre.dpath)
                           for p in hucre.iCaL])
    return dict(d_lambda=dl, segment=hucre.segment_sayisi(), pic_nokta=len(hucre.iCaL),
                pic_toplam=float(sum(p.gcalbar for p in hucre.iCaL)),
                dpath_hata_ort=float(dpath_hata.mean()), dpath_hata_maks=float(dpath_hata.max()),
                reobaz=float(reo), fi=fi, i_on=float(i_on), i_off=float(i_off),
                dI=float(dI), histerezis=kategori)


# ==================== Asama B: kopru (ayri surecte tek nokta) ================================
def kopru_olc(dl, sure, tumbacak):
    """Tek bir d_lambda noktasinda kopruyu kosar. AYRI SURECTE cagrilir (bkz. baslik)."""
    par = json.load(open(PAR_YOL))
    par.setdefault('hucre', {})['d_lambda'] = dl
    par['hucre']['pic_referans_d_lambda'] = D_LAMBDA_REF
    tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
    json.dump(par, tmp)
    tmp.close()

    if tumbacak:
        import kos_tumbacak as K
    else:
        import kos_ayakbilegi as K
    t0 = time.perf_counter()
    kk = K.kur(par_yol=tmp.name)
    iz = kk.kos(sure, kas_kaydi=False) if tumbacak else kk.kos(sure)
    cpu = time.perf_counter() - t0
    o = K.ozet(kk, iz)
    roms = ({ad: e['rom'] for ad, e in o['eklemler'].items()} if tumbacak
            else {'ankle_flx': o['rom']})
    frek = {g: float(np.mean([o['frek'][k][0] for k in kl])) for g, kl in kk.gruplar.items()}
    h0 = kk.havuz[kk.kaslar[0]].hucre
    return dict(d_lambda=dl, T=o['T'], roms=roms, frek=frek, cpu=round(cpu, 1),
                segment=h0.segment_sayisi(),
                pic_toplam=float(sum(p.gcalbar for p in h0.iCaL)))


if __name__ == '__main__':
    argv = [a for a in sys.argv[1:] if not a.startswith('--')]
    tumbacak = '--tumbacak' in sys.argv
    sure = float(argv[0]) if argv else 1.2

    # --- ic kullanim: tek nokta kosar, sonucu JSON olarak basar ---------------------------
    if '--tek' in sys.argv:
        dl = float(sys.argv[sys.argv.index('--tek') + 1])
        print('UZAY ' + json.dumps(kopru_olc(dl, sure, tumbacak)), flush=True)
        sys.exit(0)

    # Aday deger --dl ile verilebilir: uretim degeri JSON'a ANCAK bu test gectikten sonra
    # yazilir (SDLC/04_KURALLAR'in "once model sorgulanir" mantiginin uygulamasi), yani
    # sinama sirasinda JSON henuz eski degeri tasiyor olur.
    if '--dl' in sys.argv:
        dl_uretim = float(sys.argv[sys.argv.index('--dl') + 1])
    else:
        dl_uretim = float(json.load(open(PAR_YOL)).get('hucre', {}).get('d_lambda', D_LAMBDA_REF))
    if dl_uretim == D_LAMBDA_REF:
        print('UYARI: devre_par.hucre.d_lambda referans degerle ayni (%.3f); test iki AYNI '
              'noktayi karsilastirir. Aday degeri --dl ile ver.' % dl_uretim)
    bagil = lambda x, y: abs(x - y) / max(abs(x), abs(y), 1e-12)

    # --- Asama A: tek hucre ---------------------------------------------------------------
    print('\n=== Asama A: tek hucre (PIC duyarli olcumler) ===')
    a = tek_hucre_olc(D_LAMBDA_REF)
    b = tek_hucre_olc(dl_uretim)
    tek_a, tek_b = a, b                  # Asama B'de a/b yeniden baglaniyor; artefakt icin sakla
    print('%-30s %14s %14s %10s' % ('olcut', 'd_l=%.3f' % a['d_lambda'],
                                    'd_l=%.3f' % b['d_lambda'], 'bagil fark'))
    print('%-30s %14d %14d %9.2fx' % ('segment', a['segment'], b['segment'],
                                      a['segment'] / max(b['segment'], 1)))
    print('%-30s %14.5f %14.5f %10s' % ('PIC toplam gcalbar', a['pic_toplam'], b['pic_toplam'],
                                        'ESIT' if abs(a['pic_toplam'] - b['pic_toplam']) < 1e-12
                                        else 'AYRISIYOR'))
    print('%-30s %14.1f %14.1f %10s' % ('|D_path-hedef| ort [um]', a['dpath_hata_ort'],
                                        b['dpath_hata_ort'], '(rapor)'))
    print('%-30s %14.1f %14.1f %10s' % ('|D_path-hedef| maks [um]', a['dpath_hata_maks'],
                                        b['dpath_hata_maks'], '(rapor)'))
    print('%-30s %14.3f %14.3f %9.2f%%' % ('reobaz [nA]', a['reobaz'], b['reobaz'],
                                           100 * bagil(a['reobaz'], b['reobaz'])))
    for i, c in enumerate(FI_CARPAN):
        print('%-30s %14.2f %14.2f %9.2f%%'
              % ('f @ %.1f x reobaz [Hz]' % c, a['fi'][i], b['fi'][i],
                 100 * bagil(a['fi'][i], b['fi'][i])))
    print('%-30s %14.3f %14.3f %10s' % ('histerezis dI [nA]', a['dI'], b['dI'], '(rapor)'))
    print('%-30s %14s %14s %10s' % ('histerezis kategorisi', a['histerezis'], b['histerezis'],
                                    'AYNI' if a['histerezis'] == b['histerezis'] else 'FARKLI'))

    assert abs(a['pic_toplam'] - b['pic_toplam']) < 1e-12, (
        'PIC toplam iletkenligi cozunurluge gore degisiyor: olculen %.6f vs %.6f, beklenen '
        'esitlik, aralık=[0, 1e-12], kaynak=nrn_hucre referans tablosu (insa geregi esit olmali)'
        % (a['pic_toplam'], b['pic_toplam']))
    assert bagil(a['reobaz'], b['reobaz']) < ARALIK_REOBAZ, (
        'reobaz cozunurluge bagli: olculen bagil fark=%.4f, beklenen=0, aralık=[0, %.2f], '
        'kaynak=ic_olcum uzamsal yakinsama araligi' % (bagil(a['reobaz'], b['reobaz']), ARALIK_REOBAZ))
    for i, c in enumerate(FI_CARPAN):
        assert bagil(a['fi'][i], b['fi'][i]) < ARALIK_FI, (
            'f-I noktasi (%.1f x reobaz) cozunurluge bagli: olculen bagil fark=%.4f, beklenen=0, '
            'aralık=[0, %.2f], kaynak=ic_olcum uzamsal yakinsama araligi'
            % (c, bagil(a['fi'][i], b['fi'][i]), ARALIK_FI))
    assert a['histerezis'] == b['histerezis'], (
        'PIC histerez kategorisi degisti: olculen "%s", beklenen "%s", olcut=dI > %.2f x I_on, '
        'kaynak=oz_kim2020 4b (Tip I/IV/III ayrimi)'
        % (b['histerezis'], a['histerezis'], HISTEREZIS_ESIK))
    print('\nAsama A GECTI.')

    # --- Asama B: kopru, iki nokta paralel ayri sureclerde ---------------------------------
    print('\n=== Asama B: kopru (%s, %.2f s) ===' % ('tum bacak' if tumbacak else 'ayak bilegi', sure))
    from yollar import KOK
    ortak = [sys.executable, str(pathlib.Path(__file__).resolve()), str(sure)]
    if tumbacak:
        ortak.append('--tumbacak')
    isler = [subprocess.Popen(ortak + ['--tek', str(dl)], cwd=str(KOK),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
             for dl in (D_LAMBDA_REF, dl_uretim)]
    sonuc = []
    for pr, dl in zip(isler, (D_LAMBDA_REF, dl_uretim)):
        cikti, hata = pr.communicate()
        satir = [s for s in cikti.splitlines() if s.startswith('UZAY ')]
        assert satir, 'd_lambda=%s kosusu sonuc basmadi:\n%s\n%s' % (dl, cikti[-2000:], hata[-2000:])
        sonuc.append(json.loads(satir[0][5:]))
    a, b = sonuc

    print('%-30s %14s %14s %10s' % ('olcut', 'd_l=%.3f' % a['d_lambda'],
                                    'd_l=%.3f' % b['d_lambda'], 'bagil fark'))
    print('%-30s %14d %14d %9.2fx' % ('segment/havuz', a['segment'], b['segment'],
                                      a['segment'] / max(b['segment'], 1)))
    print('%-30s %14.1f %14.1f %9.2fx' % ('CPU [s]', a['cpu'], b['cpu'],
                                          a['cpu'] / max(b['cpu'], 1e-9)))
    print('%-30s %14.4f %14.4f %9.2f%%' % ('cevrim suresi [s]', a['T'], b['T'],
                                           100 * bagil(a['T'], b['T'])))
    for ad in a['roms']:
        print('%-30s %14.2f %14.2f %9.2f%%' % ('ROM %s [derece]' % ad, a['roms'][ad],
                                               b['roms'][ad], 100 * bagil(a['roms'][ad], b['roms'][ad])))
    for g in a['frek']:
        print('%-30s %14.2f %14.2f %9.2f%%' % ('havuz %s [Hz]' % g, a['frek'][g], b['frek'][g],
                                               100 * bagil(a['frek'][g], b['frek'][g])))

    # Artefakt ASSERT'LERDEN ONCE yazilir (adim_yarilama.py ile ayni gerekce): dusen olcut de
    # bir olcum sonucudur ve figure girer.
    from yollar import VERI_KOPRU
    VERI_KOPRU.mkdir(parents=True, exist_ok=True)
    with open(VERI_KOPRU / 'yakinsama_uzam.json', 'w') as fh:
        json.dump(dict(tur='uzamsal cozunurluk (d_lambda) yakinsamasi',
                       kosucu='kos_tumbacak' if tumbacak else 'kos_ayakbilegi',
                       sure_s=sure, d_lambda=[a['d_lambda'], b['d_lambda']],
                       bantlar=dict(T=ARALIK_T, ROM=ARALIK_ROM, frekans=ARALIK_F,
                                    reobaz=ARALIK_REOBAZ, fi=ARALIK_FI),
                       tek_hucre=[tek_a, tek_b], a=a, b=b), fh, indent=1)
    print('yazildi: veri/kopru/yakinsama_uzam.json')

    # Cevrim suresi kisa kosularda olculemeyebilir (kalca ortalama gecisi < 3; DOGRULAMA R.7'de
    # 1,2 s kosuda da olculememisti). Iki tarafta da olculemiyorsa bu bir SAPMA DEGILDIR --
    # atlanir ve raporlanir; yalniz BIR tarafta olculebiliyorsa gercek bir farktir, duser.
    T_a, T_b = np.isfinite(a['T']), np.isfinite(b['T'])
    assert T_a == T_b, (
        'cevrim suresi bir cozunurlukte olculuyor digerinde olculmuyor: olculen %s vs %s, '
        'beklenen ikisinde de ayni, aralık=[0, %.2f], kaynak=ic_olcum uzamsal yakinsama araligi'
        % (a['T'], b['T'], ARALIK_T))
    if T_a and T_b:
        assert bagil(a['T'], b['T']) < ARALIK_T, (
            'cevrim suresi cozunurluge bagli: olculen bagil fark=%.4f, beklenen=0, '
            'aralık=[0, %.2f], kaynak=ic_olcum uzamsal yakinsama araligi'
            % (bagil(a['T'], b['T']), ARALIK_T))
    else:
        print('not: cevrim suresi iki tarafta da olculemedi (kalca gecisi yetersiz) -- '
              'T olcutu atlandi, kosu suresi bunun icin kisa.')
    for ad in a['roms']:
        assert bagil(a['roms'][ad], b['roms'][ad]) < ARALIK_ROM, (
            'eklem %s ROM cozunurluge bagli: olculen bagil fark=%.4f, beklenen=0, '
            'aralık=[0, %.2f], kaynak=ic_olcum uzamsal yakinsama araligi'
            % (ad, bagil(a['roms'][ad], b['roms'][ad]), ARALIK_ROM))
    for g in a['frek']:
        assert bagil(a['frek'][g], b['frek'][g]) < ARALIK_F, (
            'havuz %s atesleme orani cozunurluge bagli: olculen bagil fark=%.4f, beklenen=0, '
            'aralık=[0, %.2f], kaynak=ic_olcum uzamsal yakinsama araligi'
            % (g, bagil(a['frek'][g], b['frek'][g]), ARALIK_F))
    print('\nUZAMSAL YAKINSAMA TESTI GECTI: sonuc segment cozunurlugunden bagimsiz.')
