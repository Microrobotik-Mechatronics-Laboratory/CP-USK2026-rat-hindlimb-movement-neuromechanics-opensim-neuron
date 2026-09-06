# =============================================================================
# morfoloji_cikar.py — Kim 2020 motonoronunun morfolojisini bir kez HOC'tan okuyup
#                      veri/kopru/moto_morfoloji.npz dosyasina dokerf.
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru)
# Girdi:  neuron/fig2_4_6/v_e_moto6_export.hoc (Kim'in morfoloji dosyasi; DEGISTIRILMEZ)
#         + add_hil_is.hoc, add_muscle_unit.hoc (akson tepecigi, baslangic segmenti, kas bolmesi)
# Cikti:  veri/kopru/moto_morfoloji.npz
#
# Neden bu adim var: v_e_moto6_export.hoc global "create soma, dend[311]" kullaniyor, template
# degil. 38 motonoron havuzu icin ayni morfolojiden COK hucre gerekiyor. HOC dosyasina cerrahi
# mudahale etmek yerine morfoloji bir kez okunup veri olarak saklanir; hucreler Python'da bu
# veriden kurulur (kod/kopru/nrn_hucre.py). Boylece Kim'in kaynak dosyalari hic degismez ve
# kosu aninda prototip hucre bellekte durmak zorunda kalmaz.
#
# Dogruluk guvencesi: Python'da kurulan hucrenin HOC'un kurdugu hucreyle ayni davrandigi
# kod/kopru/capraz_kontrol.py ile aksiyon potansiyeli zamanlari uzerinden sinanir (04_KURALLAR: bagimsiz
# ikinci yontemle capraz kontrol).
#
# BILINEN SAPMALAR:
# - 3B nokta verisi (pt3d) oldugu gibi tasinir; nseg burada KAYDEDILMEZ, cunku d_lambda kurali
#   Ra/cm atandiktan SONRA uygulanmalidir (fixnseg.hoc:41-42 sirasi).
# =============================================================================
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))      # nrn_ortam icin
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # kod/yollar.py icin
import numpy as np
from nrn_ortam import h, yukle       # chdir + mekanizma yukleme kurallari orada
from yollar import VERI_KOPRU

yukle('v_e_moto6_export.hoc', 'add_hil_is.hoc', 'add_muscle_unit.hoc')

adlar, ebeveyn, ebeveyn_x, cocuk_x, L, diam, pt3d = [], [], [], [], [], [], []
for sec in h.allsec():
    ad = sec.name()
    sr = h.SectionRef(sec=sec)
    if sr.has_parent():
        p = sr.parent
        # trueparentseg(): baglantinin ebeveyn uzerindeki x konumu; orient(): kendi ucundaki x
        ebeveyn.append(p.name())
        ebeveyn_x.append(float(sec.parentseg().x))
        cocuk_x.append(float(sec.orientation()))
    else:
        ebeveyn.append(''); ebeveyn_x.append(np.nan); cocuk_x.append(np.nan)
    adlar.append(ad); L.append(float(sec.L)); diam.append(float(sec.diam))
    pt3d.append(np.array([[sec.x3d(i), sec.y3d(i), sec.z3d(i), sec.diam3d(i)]
                          for i in range(sec.n3d())], dtype=float))

VERI_KOPRU.mkdir(parents=True, exist_ok=True)
cik = VERI_KOPRU / 'moto_morfoloji.npz'
np.savez_compressed(
    cik,
    adlar=np.array(adlar), ebeveyn=np.array(ebeveyn),
    ebeveyn_x=np.array(ebeveyn_x), cocuk_x=np.array(cocuk_x),
    L=np.array(L), diam=np.array(diam),
    pt3d_duz=np.concatenate([p for p in pt3d if len(p)]) if any(len(p) for p in pt3d) else np.zeros((0, 4)),
    pt3d_sayi=np.array([len(p) for p in pt3d]),
)
print('section sayisi :', len(adlar))
print('3B noktasi olan :', int(sum(1 for p in pt3d if len(p))))
print('toplam 3B nokta :', int(sum(len(p) for p in pt3d)))
print('yazildi         :', cik.name)
