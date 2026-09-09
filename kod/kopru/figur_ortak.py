# =============================================================================
# figur_ortak.py — figur uretiminin ortak kurallarini tek yerde tutar (IP-9 cekirdegi).
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru) -- saf NumPy + matplotlib
# Girdi:  literatur/referans_degerler.json (ilan edilmis aralıklar)
# Cikti:  yok (kutuphane)
#
# NEDEN: SDLC/04_KURALLAR raporlama bolumu her figur icin ayni uc seyi istiyor -- Agg backend,
# cikti DAIMA sekiller/ altina ve PNG 300 dpi, ve her PNG'nin yaninda onu ureten sayisal veri
# CSV olarak. Bugune kadar her betik bunu kendi icinde tekrarliyordu; tekrar eden kural
# er ya da gec bir yerde tutulmaz. Burasi o kuralin tek uygulama noktasi.
#
# Aralik cizimi de buradadir: bir olcut figurde gosterilecekse aralik SAYISI koda gomulmez,
# referans_degerler.json'dan kimlikle okunur (04_KURALLAR: "kaynagi olmayan aralık test
# edilmez"; figur de bir raporlama bicimidir).
# =============================================================================
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import matplotlib
matplotlib.use('Agg')                      # 04_KURALLAR: figur Agg ile uretilir
import matplotlib.pyplot as plt            # noqa: E402 -- backend secimi importtan once olmali
from yollar import SEKILLER, LITERATUR

DPI = 300                                  # 04_KURALLAR: PNG 300 dpi
_REF = None


def referanslar():
    """referans_degerler.json kayitlarini {kimlik: kayit} olarak doner (bir kez okunur)."""
    global _REF
    if _REF is None:
        with open(LITERATUR / 'referans_degerler.json') as fh:
            _REF = {k['kimlik']: k for k in json.load(fh)['kayitlar']}
    return _REF


def bant(ax, kimlik, yatay=True, renk='tab:green', alpha=0.15, etiket=True):
    """Ilan edilmis aralıgi golge olarak cizer ve kunyesini etikete koyar.

    Aralik SAYISI buraya yazilmaz; kimlikle referans_degerler.json'dan okunur. Aralik tanimsiz
    (null) kayitlarda yalnizca deger cizgisi cizilir -- boyle kayitlar bir TOLERANS araligi
    degil, karsilastirma degeridir (orn. olculmus yuruyus araligi)."""
    r = referanslar()[kimlik]
    ad = '%s [%s]' % (r['buyukluk'], r['birim'])
    kunye = r['kaynak']['kunye']
    cizgi = ax.axhspan if yatay else ax.axvspan
    if r.get('aralik'):
        alt, ust = r['aralik']
        cizgi(alt, ust, color=renk, alpha=alpha, zorder=0,
              label=('aralik %.4g-%.4g (%s)' % (alt, ust, kunye)) if etiket else None)
    elif isinstance(r.get('deger'), (list, tuple)) and len(r['deger']) == 2:
        cizgi(r['deger'][0], r['deger'][1], color='0.85', zorder=0,
              label=('%s (%s)' % (ad, kunye)) if etiket else None)
    return r


def kaydet(fig, ad, sutunlar=None, aciklama='', sikistir=False):
    """PNG'yi sekiller/<ad>.png (300 dpi) olarak, kaynak veriyi <ad>.csv olarak yazar.

    sutunlar: {sutun_adi: 1B dizi} -- hepsi ayni uzunlukta olmali (sayisal CSV).
    Metin sutunu gereken tablolar icin kaydet_tablo() kullanilir."""
    SEKILLER.mkdir(exist_ok=True)
    fig.savefig(SEKILLER / (ad + '.png'), dpi=DPI,
                **({'bbox_inches': 'tight'} if sikistir else {}))
    plt.close(fig)
    if sutunlar:
        bas = list(sutunlar)
        veri = np.column_stack([np.asarray(sutunlar[k], dtype=float) for k in bas])
        with open(SEKILLER / (ad + '.csv'), 'w') as f:
            if aciklama:
                f.write('# %s\n' % aciklama)
            f.write('# %s.png kaynak verisi\n' % ad)
            f.write(','.join(bas) + '\n')
            for satir in veri:
                f.write(','.join('%.6g' % v for v in satir) + '\n')
    return SEKILLER / (ad + '.png')


def kaydet_tablo(ad, basliklar, satirlar, aciklama=''):
    """Metin sutunu iceren kaynak CSV'si (orn. kas adi + olculen deger + gecti/kaldi)."""
    SEKILLER.mkdir(exist_ok=True)
    with open(SEKILLER / (ad + '.csv'), 'w') as f:
        if aciklama:
            f.write('# %s\n' % aciklama)
        f.write('# %s.png kaynak verisi\n' % ad)
        f.write(','.join(basliklar) + '\n')
        for s in satirlar:
            f.write(','.join(str(x) for x in s) + '\n')
    return SEKILLER / (ad + '.csv')
