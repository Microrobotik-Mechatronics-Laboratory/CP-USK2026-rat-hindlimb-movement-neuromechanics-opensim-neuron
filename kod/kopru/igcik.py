# =============================================================================
# igcik.py — kas igciginin duyusal cikisi: kas-tendon boyundan Ia ve II atesleme orani.
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru) -- saf NumPy, OpenSim/NEURON gerektirmez
# Girdi:  veri/r_katsayilari_v3.json (Blum 2020 fiti), veri/kapali_dongu/cl_grid3d.npz (lm min)
# Cikti:  Ia(t), II(t) [pps], kas basina
#
# BICIM (kanonik kaynak: arsiv/kod/opensim/r31_uret.py, v3.1 -- 07.09.2026'da arsivlendi):
#     d  = lif boyu - dongu minimumu            [mm]
#     v  = lif hizi                             [mm/s]
#     Ia = max(0, b + kL*d + kV*max(v,0)^p)     b=10.43 kL=26.59 kV=27.08 p=0.532
#     II = max(0, 14.43*d + 21.25*sign(v)*|v|^0.358)
# Ia katsayilari JSON'dan okunur, koda gomulmez. II katsayilari JSON'da YOKTUR
# ("II bu pakette YOK"); v3.1 bicimindeki degerler burada acikca [varsayim] olarak durur.
#
# BILINEN SAPMALAR:
# - KALIBRASYON: r_katsayilari_v3.json'un 'surekli_hareket_sonumu' kaydi, surekli harekette
#   olcum ortalamasi ~15 Hz iken statik tahminin ~90 Hz (yaklasik 6 kat) ciktigini soyluyor.
#   Fit RAMPA-TUT protokoluna uygundur; lokomotor kullanimda asagi kalibrasyon gerekir.
#   Bu yuzden acik bir k_ia carpani vardir (devre_par.json), varsayilani 1.0 ve etkisi
#   raporlanir. Sessiz olcekleme YAPILMAZ.
# - arsiv/kod/kapali_dongu/cl_emergent.py:53-54 bu formullere JSON'da BULUNMAYAN +19.6 (Ia) ve
#   +43.3 (II) ofsetleri ekliyor ve hizi 45 mm/s'de doyuruyor. Burada JSON ve r31_uret.py
#   esas alinir; fark DOGRULAMA'ya not dusulmustur.
# - II icin fusimotor (gama) yoktur; Vincent araliklari da pasif kosuldan gelir (PREPRINT 11).
# =============================================================================
import json
import numpy as np

# r31_uret.py v3.1 II katsayilari. JSON'da karsiligi yok -> [varsayim].
II_KL, II_KV, II_P = 14.43, 21.25, 0.358


class Igcik:
    """Kas basina Ia/II ureten igcik modeli. Vektorlestirilmistir: tum kaslar tek cagrida."""

    def __init__(self, katsayi_yolu, lm_min_mm, k_ia=1.0, k_ii=1.0, v_doyum_mms=None):
        with open(katsayi_yolu) as fh:
            kj = json.load(fh)
        p = kj['Ia_kinematik_v3']
        self.b, self.kL, self.kV, self.p = p['b'], p['kL'], p['kV'], p['p']
        self.kaynak = p['kaynak']
        self.lm_min = np.asarray(lm_min_mm, dtype=float)
        self.k_ia, self.k_ii = float(k_ia), float(k_ii)
        self.v_doyum = v_doyum_mms          # None = doyum yok (r31_uret.py ile ayni)

    def __call__(self, lm_mm, vlm_mms):
        """lm_mm: lif boyu [mm], vlm_mms: lif hizi [mm/s]. Ikisi de (nKas,) dizi."""
        d = np.maximum(0.0, np.asarray(lm_mm) - self.lm_min)
        v = np.asarray(vlm_mms)
        if self.v_doyum is not None:
            v = np.clip(v, -self.v_doyum, self.v_doyum)
        ia = np.maximum(0.0, self.b + self.kL * d + self.kV * np.maximum(v, 0.0) ** self.p)
        ii = np.maximum(0.0, II_KL * d + II_KV * np.sign(v) * np.abs(v) ** II_P)
        return self.k_ia * ia, self.k_ii * ii


def lm_min_izgaradan(grid_npz, adlar=None):
    """Lif boyu minimumunu proje izgarasindan alir (cl_grid3d.npz LM, 13^3 dugum).

    Neden izgaradan: mevcut r(t) serisi (r_tamdongu_v3_1.csv) de ayni referansi kullaniyor
    (r31_uret.py: d = lm - lm.min()); ayni referans korunmazsa uretilen Ia oranlari eski
    seriyle karsilastirilamaz."""
    g = np.load(grid_npz, allow_pickle=True)
    izg_adlar = [str(x) for x in g['names']]
    lm_min = g['LM'].reshape(-1, len(izg_adlar)).min(0) * 1000.0      # m -> mm
    if adlar is None:
        return lm_min, izg_adlar
    ix = [izg_adlar.index(a) for a in adlar]
    return lm_min[ix], list(adlar)


def lif_boyu(lmt_m, tsl_m, lmo_m, alp_rad):
    """Rijit tendon kabulu: lm = sqrt((lmt-tsl)^2 + (lmo*sin a0)^2), cos a = (lmt-tsl)/lm.
    Kaynak: arsiv/kod/opensim/kod_02_swing_id_so.py:67 -- ayni formul, ayni kabul."""
    x = np.maximum(np.asarray(lmt_m) - np.asarray(tsl_m), 1e-5)
    lm = np.sqrt(x ** 2 + (np.asarray(lmo_m) * np.sin(np.asarray(alp_rad))) ** 2)
    return lm, x / lm


def lif_hizi(vlmt_ms, cosa):
    """Rijit tendonda lif hizi kas-tendon hizinin pennasyon izdusumudur (cl_emergent.py:71)."""
    return np.asarray(vlmt_ms) * np.asarray(cosa)
