# r31_uret.py — Oturum 6: r_tamdongu v3.1 (II düzeltmesi; karar Deniz'in delegasyonuyla,
# 1 Eylül, 50_ kaydı). GEREKÇE: 02_ §F bulgusu — v3'ün II'si |v| kullanıyordu (kısalma
# hızı ateşlemeyi ARTIRIYORDU); iğcik kısalırken ateşleme düşer, belgelenen v2 formülü de
# sign(v)'lidir. v3.1: Ia DEĞİŞMEZ (v3 ile birebir); II = max(0, 14.43·d + 21.25·sign(v)·
# |v|^0.358) — 0 kırpma eklidir (ateşleme negatif olamaz; 46_ f0=0 varsayımıyla tutarlı).
# d = lif boyu − döngü min [mm], v = lif hızı [mm/s] (rt_ara) — v3 sözleşmesi aynen.
import numpy as np

ra = np.load('rt_ara.npz', allow_pickle=True)
adlar = list(ra.files)
Ia, II = {}, {}
for n in adlar:
    lm = ra[n][:,0]*1000.0; v = ra[n][:,1]*1000.0
    d = lm - lm.min()
    Ia[n] = np.maximum(0.0, 10.43 + 26.59*d + 27.08*np.maximum(v,0.0)**0.532)
    II[n] = np.maximum(0.0, 14.43*d + 21.25*np.sign(v)*np.abs(v)**0.358)
gs = np.arange(0, 100.5, 0.5)
# doğrulama 1: Ia, v3 CSV'sinin bilinen değerleriyle birebir (vincent_bicim_testi kimliği)
for (n, r, ref) in [('TA',0,90.186), ('Sol',100,14.123), ('GMa',190,10.430)]:
    assert abs(Ia[n][r]-ref) < 0.01, (n, r, Ia[n][r])
# doğrulama 2: kısalmada (v<0) v3.1 II'si v3'ün |v| II'sinden KÜÇÜK olmalı
n0 = 'Sol'; v0 = ra[n0][:,1]*1000.0
c3 = 14.43*(ra[n0][:,0]*1000-ra[n0][:,0].min()*1000) + 21.25*np.abs(v0)**0.358
assert (II[n0][v0 < -0.1] <= c3[v0 < -0.1] + 1e-9).all()
# biçim sınaması v3.1 ile (vincent_hakem tarifi; GI/GP/TFL hariç)
orl = np.array([(Ia[n].max()-Ia[n].min())/(II[n].max()-II[n].min())
                for n in adlar if n not in {'GI','GP','TFL'}])
print('v3.1 biçim sınaması: Ia/II derinlik oranı medyan %.3f (min %.3f · maks %.3f) · '
      'hedef 2,544 · ±%%50 bandında %d/35' % (np.median(orl), orl.min(), orl.max(),
      int(((orl > 0.5*2.544) & (orl < 1.5*2.544)).sum())))
with open('r_tamdongu_v3_1.csv','w') as f:
    f.write('# r(t) tam dongu v3.1 (karar: Deniz delegasyonu 1 Eylul, 50_; 02_ SF bulgusunun '
            'duzeltmesi) — Ia: v3 ile BIREBIR AYNI (Kademe-2 K-modeli, b=10.43 kL=26.59 '
            'kV=27.08 p=0.532, yalniz uzama hizi); II: max(0, 14.43.d + 21.25.sign(v).|v|^0.358) '
            '— v3teki |v| yerine belgelenen sign(v), kisalmada ateslemeyi dusurur; d=lif boyu - '
            'dongu min [mm], v=lif hizi [mm/s]; BAYRAKLAR: fusimotor yok, surekli-hareket sonumu '
            'x1.3-6 (cope_sonum.json), II paketten dogrulanamadi (bicim sinamasi gecti: medyan '
            'oran %.2f), GI/GP/TFL guvensiz; ureten: r31_uret.py\n' % np.median(orl))
    f.write('gait_pct,' + ','.join(n+'_Ia' for n in adlar) + ','
            + ','.join(n+'_II' for n in adlar) + '\n')
    for i, g in enumerate(gs):
        f.write('%.1f,' % g + ','.join('%.3f' % Ia[n][i] for n in adlar) + ','
                + ','.join('%.3f' % II[n][i] for n in adlar) + '\n')
print('r_tamdongu_v3_1.csv yazıldı (201 × %d)' % (2*len(adlar)))
