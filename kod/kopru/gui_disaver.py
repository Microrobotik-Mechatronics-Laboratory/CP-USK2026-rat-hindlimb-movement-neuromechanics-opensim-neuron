# =============================================================================
# gui_disaver.py — kapali dongu kosuyu OpenSim GUI'nin oynatabilecegi bicime cevirir.
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru) -- saf NumPy, OpenSim/NEURON gerektirmez
# Girdi:  veri/kopru/kosu_ayakbilegi.npz (kos_ayakbilegi.py uretir)
#         veri/kapali_dongu/cl_grid3d.npz (kilitli koordinatlarin degerleri: FIX/cnames)
# Cikti:  veri/goruntuleme/kopru_ayakbilegi.mot      -- 14 koordinat + 38 kas uyarimi (TEK DOSYA;
#                                                       GUI hem hareketi oynatir hem kaslari boyar)
#         veri/goruntuleme/kopru_ayakbilegi_koordinat.mot -- yalniz koordinat (yedek)
#
# Neden ayri bir betik: kosu yalnizca SERBEST koordinati kaydeder (ayak bileginde ankle_flx);
# GUI ise modelin 14 koordinatinin tamamini ister. Kilitli 13 koordinat kosuda sabit tutuldugu
# degerlere (cl_grid3d.npz FIX) doldurulur -- yani dosya kosunun gercekten oldugu pozu gosterir,
# uydurma bir poz degil.
#
# BILINEN SAPMALAR:
# - Kosu 0.15 ms adimla kaydedilir (3 s icin 20000 ornek). GUI icin seyreltilir; seyreltme
#   yalniz GORUNTULEME icindir, hesap dosyalari (npz) dokunulmadan kalir.
# - .mot dosyasi inDegrees=yes'tir; OpenSim aci koordinatlarini dereceye cevirir, otelemeleri
#   (sacrum_x/y/z) cevirmez -- bu yuzden otelemeler metre olarak yazilir.
# =============================================================================
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # kod/yollar.py icin
import numpy as np
from yollar import VERI, VERI_KOPRU, GRID3D

SERBEST = ('ankle_flx',)          # kos_ayakbilegi.py ile ayni
HEDEF_HZ = 200.0                  # GUI oynatmasi icin yeterli; hesap dosyasi seyreltilmez


def yaz_mot(yol, t, ad_sut, veri, ad='kopru_ayakbilegi'):
    with open(yol, 'w') as f:
        f.write('%s\nversion=1\nnRows=%d\nnColumns=%d\ninDegrees=yes\nendheader\n'
                % (ad, len(t), len(ad_sut) + 1))
        f.write('time\t' + '\t'.join(ad_sut) + '\n')
        for i in range(len(t)):
            f.write('%.6f\t' % t[i] + '\t'.join('%.6f' % v for v in veri[i]) + '\n')


def yaz_sto(yol, t, ad_sut, veri, ad='kopru_ayakbilegi_kuvvet'):
    with open(yol, 'w') as f:
        f.write('%s\nversion=1\nnRows=%d\nnColumns=%d\ninDegrees=no\nendheader\n'
                % (ad, len(t), len(ad_sut) + 1))
        f.write('time\t' + '\t'.join(ad_sut) + '\n')
        for i in range(len(t)):
            f.write('%.6f\t' % t[i] + '\t'.join('%.6f' % v for v in veri[i]) + '\n')


def main():
    d = np.load(VERI_KOPRU / 'kosu_ayakbilegi.npz', allow_pickle=True)
    g = np.load(GRID3D, allow_pickle=True)
    cnames = [str(x) for x in g['cnames']]
    fix = dict(zip(cnames, [float(v) for v in g['FIX']]))
    izg_kas = [str(x) for x in g['names']]
    kosu_kas = [str(x) for x in d['kaslar']]

    t_ham = d['t']
    adim = max(1, int(round(1.0 / (HEDEF_HZ * (t_ham[1] - t_ham[0])))))
    s = slice(None, None, adim)
    t = t_ham[s]

    # --- 1) koordinat dosyasi: serbest olan kosudan, kilitli olanlar FIX'ten ---------------
    ACI = {'sacrum_x', 'sacrum_y', 'sacrum_z'}          # bunlar oteleme, dereceye cevrilmez
    sut = np.zeros((len(t), len(cnames)))
    for j, n in enumerate(cnames):
        if n in SERBEST:
            k = SERBEST.index(n)
            sut[:, j] = np.degrees(d['q'][s, k])
        elif n in ACI:
            sut[:, j] = fix.get(n, 0.0)                 # metre, oldugu gibi
        else:
            sut[:, j] = np.degrees(fix.get(n, 0.0))
    (VERI / 'goruntuleme').mkdir(parents=True, exist_ok=True)
    yedek = VERI / 'goruntuleme' / 'kopru_ayakbilegi_koordinat.mot'
    yaz_mot(yedek, t, cnames, sut)

    # --- 2) kas uyarimi ---------------------------------------------------------------------
    # Kosuda yalniz 10 bilek kasi surulur; kalan 28 kas sifir uyarimdadir.
    akt = np.zeros((len(t), len(izg_kas)))
    for kx, kas in enumerate(kosu_kas):
        akt[:, izg_kas.index(kas)] = d['u'][s, kx]

    # --- 3) BIRLESIK dosya: OpenSim GUI tek dosyada hem oynatir hem kaslari boyar ------------
    # GUI, yuklenen hareket dosyasinda '<kas>.activation' sutunlarini gorurse kaslari o degere
    # gore renklendirir. inDegrees=yes yalniz KOORDINAT sutunlarini etkiler; aktivasyon
    # sutunlari donusume girmez.
    mot = VERI / 'goruntuleme' / 'kopru_ayakbilegi.mot'
    yaz_mot(mot, t, cnames + ['%s.activation' % k for k in izg_kas],
            np.hstack([sut, akt]))

    print('ornek sayisi : %d -> %d (%.0f Hz, seyreltme 1/%d)'
          % (len(t_ham), len(t), 1.0 / (t[1] - t[0]), adim))
    print('sure         : %.3f s' % t[-1])
    print('ankle_flx    : %.2f .. %.2f derece' % (sut[:, cnames.index('ankle_flx')].min(),
                                                  sut[:, cnames.index('ankle_flx')].max()))
    print('kas uyarimi  : %d kas surulu, %d kas sifir' % (len(kosu_kas), len(izg_kas) - len(kosu_kas)))
    print('yazildi      : %s   (koordinat + kas uyarimi, GUI icin bunu yukleyin)'
          % mot.relative_to(mot.parents[2]))
    print('               %s   (yalniz koordinat, yedek)' % yedek.relative_to(yedek.parents[2]))


if __name__ == '__main__':
    main()
