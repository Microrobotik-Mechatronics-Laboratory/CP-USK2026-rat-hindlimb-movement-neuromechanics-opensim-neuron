# cop_dienes_turetme.py — CoP'nin Dienes 2022'nin yayımlı moment/kuvvet eğrilerinden
# türetilmesi (Deniz'in getirdiği reçete + 31 Ağustos düzeltmeleri; 47_ B23).
# Denklem (bilek etrafında yarı-statik moment dengesi, ayak ağırlığı/ataleti ihmal — etiketli):
#   iç moment M_ic (Dienes, dorsifleksiyon +) + dış moment tau_dis = 0
#   tau_dis = d·F_v + z_a·F_h   (d = x_CoP − x_bilek; z_a = bilek yüksekliği; x ileri, y yukarı)
#   → d = (−M_ic − z_a·F_h) / F_v      [birimler: N·m/kg / N/kg = m → kütleden bağımsız,
#                                        uzunluk DIENES hayvanının metresi]
import numpy as np, json
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # kod/yollar.py icin
from yollar import VERI, LEWIS_GRF

# NOT: bu iki girdi .npz bekliyor; depoda .json karsiliklari var (veri/dienes_bilek_momenti.json).
# Bicim donusumu yapilmadi -- bkz. kod/opensim/README.md eksik girdi tablosu.
d_mom = np.load(VERI/'dienes_bilek_momenti.npz')      # g (dongu %), M (N·m/kg), sd_ust, sd_alt
grf = json.load(open(LEWIS_GRF))          # ayni makalenin Fig 3'u (N/kg)
g = d_mom['g']; M = d_mom['M']

def Fk(g_):
    return (np.interp(g_, grf['AP']['pct'], grf['AP']['Nkg']),
            np.interp(g_, grf['V']['pct'],  grf['V']['Nkg']))

# --- stance sonu: V kanalinin tepe %5'inin altina indigi ilk nokta (kayitli tanim) ---
gg = np.arange(0,100.1,0.1)
V = np.interp(gg, grf['V']['pct'], grf['V']['Nkg'])
esik = 0.05*V.max()
stance_son = gg[np.argmax((gg>20) & (V<esik))]
print('stance sonu (V<%%5 tepe): %%%.1f dongu  (Tablo 1: 63.9±3.6)' % stance_son)

# --- geometri (bizim dogrulanmis sahneden; VARSAYIM etiketli) ---
# u_stance_pipeline sahnesinden stance karelerinde: bilek ekleminin yer-x izdusumu,
# bilek yuksekligi z_a, topuk-arka ve parmak-ucu yer-x'leri. Olcek: Dienes ayak
# parcasi (bilek→5.MT) 35.9 mm ↔ bizim model bilek→MTP istasyonu mesafesi.
from u_stance_pipeline import Makine, V_CAL, V_TOE
import opensim as osim
mk = Makine()
GREENE_MTP = 0.674                                # 47_ B19
st_g = np.arange(0, 66.0, 1.0)
geo = {'xa':[], 'za':[], 'xh':[], 'xt':[]}
mtp_loc = osim.Vec3(*(V_CAL + GREENE_MTP*(V_TOE-V_CAL)))
olcek_paydasi = []
for gi in st_g:
    mk.kin(float(gi))
    # bilek eklem merkezi: tibia-foot arasi; foot govdesinin eklem çerçevesi yerine
    # ayak govdesinde bilege yakin sabit nokta olarak V_CAL'in 5 mm ustu KULLANILMAZ;
    # bilek merkezini foot_j cocuk cercevesinden aliyoruz (model tanimi).
    j = mk.model.getJointSet().get('foot_j')
    p = j.getChildFrame().getPositionInGround(mk.st)
    geo['xa'].append(p.get(0)); geo['za'].append(p.get(1))
    th = mk.foot.findStationLocationInGround(mk.st, osim.Vec3(*V_CAL))
    tu = mk.foot.findStationLocationInGround(mk.st, osim.Vec3(*V_TOE))
    geo['xh'].append(th.get(0)); geo['xt'].append(tu.get(0))
    mt = mk.foot.findStationLocationInGround(mk.st, mtp_loc)
    olcek_paydasi.append(np.sqrt((mt.get(0)-p.get(0))**2 + (mt.get(1)-p.get(1))**2))
for k in geo: geo[k] = np.array(geo[k])
model_ayak = float(np.mean(olcek_paydasi))        # bizim bilek→MTP (m)
DIENES_AYAK = 0.0359                              # m (Tablo 1)
rho = model_ayak/DIENES_AYAK
print('model bilek→MTP %.1f mm; Dienes 35.9 mm; ölçek rho=%.3f' % (1000*model_ayak, rho))
print('bilek yüksekliği z_a (bizim sahne): %.1f–%.1f mm' % (1000*geo['za'].min(), 1000*geo['za'].max()))

def turet(z_carpan=1.0, M_carpan=1.0, rho_carpan=1.0):
    s_list = []
    for i, gi in enumerate(st_g):
        AP, Vv = Fk(gi)
        stf = gi/stance_son
        if stf < 0.05 or stf > 0.95 or Vv < esik:
            s_list.append(np.nan); continue
        z_a = geo['za'][i]/rho * z_carpan          # model m → Dienes m
        Mi = np.interp(gi, g, M) * M_carpan
        d = (-Mi - z_a*AP) / Vv                    # Dienes metresi
        d_model = d * rho * rho_carpan             # model metresine
        s = (geo['xa'][i] + d_model - geo['xh'][i]) / (geo['xt'][i] - geo['xh'][i])
        s_list.append(s)
    return np.array(s_list)

s_merkez = turet()
# duyarlilik: z_a %50 asagi/yukari, M ±%10, olcek ±%10
band = [turet(zc, mc, rc) for zc in (0.5,1.0,1.5) for mc in (0.9,1.0,1.1) for rc in (0.9,1.0,1.1)]
band = np.array(band)
s_alt = np.nanmin(band, axis=0); s_ust = np.nanmax(band, axis=0)
gecerli = ~np.isnan(s_merkez)
print('\ntüretilmiş CoP (0=topuk arkası, 1=parmak ucu):')
for gi in [5,10,15,20,25,30,35,40,45,50,55,60]:
    i = int(gi)
    if gecerli[i]:
        print('  %%%d döngü (stance %%%d): s = %.3f  [%.3f–%.3f]' %
              (gi, round(100*gi/stance_son), s_merkez[i], s_alt[i], s_ust[i]))
np.savez(VERI/'cop_dienes.npz', g=st_g, s=s_merkez, s_alt=s_alt, s_ust=s_ust,
         stance_son=stance_son, rho=rho, geo_za=geo['za'])
print('kaydedildi: cop_dienes.npz')

