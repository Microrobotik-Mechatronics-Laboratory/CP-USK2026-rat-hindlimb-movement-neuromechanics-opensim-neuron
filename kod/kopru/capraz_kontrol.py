# =============================================================================
# capraz_kontrol.py — Python'da kurulan motonoron, HOC'un kurduguyla ayni mi?
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru)
# Girdi: neuron/kopru/motor_unit_batch.hoc (HOC referansi) + kod/kopru/nrn_hucre.py (Python)
# Cikti: ekrana karsilastirma tablosu; sapma varsa assert dusurur.
#
# Neden: nrn_hucre.py, Kim'in hoc dosyalarindaki biyofizigi Python'da yeniden uyguluyor
# (38 havuz icin gerekli, cunku v_e_moto6_export.hoc template degil global create kullaniyor).
# Yeniden uygulama sessiz sapma riski tasir. 04_KURALLAR'in "bagimsiz ikinci yontemle capraz
# kontrol" kurali geregi iki kurulum AYNI surecte, AYNI uyaranla, AYNI zaman adimiyla kosturulup
# aksiyon potansiyeli zamanlari karsilastirilir. Iki hucre elektriksel olarak bagimsizdir; ayni surecte
# durmalari birbirlerini etkilemez, yalnizca hesap iki katina cikar.
#
# Karsilastirma kas modulu ACIK yapilir (kas_modulu=True) ki model HOC ile birebir ayni olsun;
# koprudeki CaSP/fHill kesimi ayri ve bilincli bir karardir (nrn_hucre.py bilinen sapmalari).
#
# ARALIK: aksiyon potansiyeli zamani farki < 0.025 ms (bir entegrasyon adimi). Bu bir REGRESYON araligidir,
# literatur dogrulamasi degildir: iki kurulum ayni denklemleri cozdugu icin fark ancak kayan
# nokta duzeyinde olabilir; bir adimdan buyuk fark yapisal sapma demektir.
# =============================================================================
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from nrn_ortam import h, yukle
from yollar import NRN_BATCH_GORELI
import nrn_hucre

TSTOP, DT, ESIK, ARALIK_MS = 3000.0, 0.025, -40.0, 0.025

# --- HOC referans kurulumu (Kim'in kendi zinciri) ---------------------------------------
yukle(NRN_BATCH_GORELI)
hoc_soma, hoc_iseg = h.soma, getattr(h, 'is')
hoc_sec = list(h.allsec())
dik_hoc = h.Vector()
nc_hoc = h.NetCon(hoc_iseg(0.5)._ref_v, None, sec=hoc_iseg)
nc_hoc.threshold = ESIK; nc_hoc.record(dik_hoc)
v_hoc = h.Vector().record(hoc_soma(0.5)._ref_v)

# --- Python kurulumu --------------------------------------------------------------------
py = nrn_hucre.MotoNoron('py', dpath=600.0, kas_modulu=True)
dik_py = py.ap_kaydet(ESIK)
v_py = h.Vector().record(py.soma(0.5)._ref_v)
st = h.RampIClamp(py.soma(0.5)); st.pkamp = 20      # add_pics_istim.hoc:72-74 ile ayni uyaran
py._st = st

# --- tek kosu, iki hucre ---------------------------------------------------------------
h.dt = DT
t0 = time.perf_counter(); h.finitialize(-70); h.continuerun(TSTOP); t1 = time.perf_counter()

d_h, d_p = np.array(dik_hoc), np.array(dik_py)
vh, vp = np.array(v_hoc), np.array(v_py)
nseg_h = sum(s.nseg for s in hoc_sec)

print('kosu: tstop=%.0f ms, iki hucre birlikte %.1f s CPU' % (TSTOP, t1 - t0))
print()
print('%-28s %14s %14s' % ('buyukluk', 'HOC', 'Python'))
print('%-28s %14d %14d' % ('section sayisi', len(hoc_sec), len(py.sec)))
print('%-28s %14d %14d' % ('segment sayisi', nseg_h, py.segment_sayisi()))
print('%-28s %14d %14d' % ('CaL nokta sureci (PIC)', int(h.iCaL_say) if hasattr(h, 'iCaL_say') else -1, len(py.iCaL)))
print('%-28s %14d %14d' % ('IaSyn takili segment', -1, len(py.ia_bolmeleri)))
print('%-28s %14d %14d' % ('aksiyon potansiyeli sayisi', d_h.size, d_p.size))
print('%-28s %14.4f %14.4f' % ('soma v min [mV]', vh.min(), vp.min()))
print('%-28s %14.4f %14.4f' % ('soma v maks [mV]', vh.max(), vp.max()))
if d_h.size:
    print('%-28s %14.3f %14.3f' % ('ilk aksiyon potansiyeli [ms]', d_h[0], d_p[0] if d_p.size else np.nan))
    print('%-28s %14.3f %14.3f' % ('son aksiyon potansiyeli [ms]', d_h[-1], d_p[-1] if d_p.size else np.nan))

# --- aralık sinamasi ----------------------------------------------------------------------
assert d_h.size == d_p.size, (
    'aksiyon potansiyeli SAYISI farkli: olculen(Python)=%d, beklenen(HOC)=%d, aralık=tam esleme, '
    'kaynak=neuron/fig2_4_6 Kim 2020 hoc zinciri' % (d_p.size, d_h.size))
if d_h.size:
    fark = np.abs(d_h - d_p)
    print()
    print('aksiyon potansiyeli zamani farki: maks %.6f ms, ortalama %.6f ms' % (fark.max(), fark.mean()))
    assert fark.max() < ARALIK_MS, (
        'aksiyon potansiyeli ZAMANI aralıktan disari: olculen maks fark=%.6f ms, beklenen=0.0 ms, '
        'aralık=[0, %.3f] ms (bir entegrasyon adimi), kaynak=ic_olcum regresyon araligi'
        % (fark.max(), ARALIK_MS))
dv = np.abs(vh - vp).max()
print('soma voltaj izi maks farki: %.6f mV' % dv)
print()
print('CAPRAZ KONTROL GECTI: Python kurulumu HOC kurulumuyla ayni davraniyor.')
