# rt_ara_uret.py — Oturum 6: rt_ara.npz'yi SAHNEDEN yeniden üretir (projeden aktarmak yerine;
# aktarım maliyeti ve hata riski yüksekti). Tarif 46_ §5'ten: lmt = GeometryPath.getLength
# (201 kare, g=0..100 %0,5 adım), lm = sqrt((lmt−tsl)² + (lmo·sinα0)²) [rijit tendon, kart
# kural 6], v = np.gradient(lm, t). DOĞRULAMA: bu üretimle u_stance_pipeline.salinim_dogrula
# u_swing_v2'yi hedef fark bandında yeniden üretmeli — üretim ancak o zaman geçerli sayılır.
import numpy as np, json
import opensim as osim

lines = open('OTURUM5_YUKLE/rat_walk_bone_smooth.mot').read().splitlines()
i0 = [i for i,l in enumerate(lines) if l.startswith('time')][0]
mcols = lines[i0].split()
mot = np.genfromtxt('OTURUM5_YUKLE/rat_walk_bone_smooth.mot', skip_header=i0+1)
T = mot[-1,0]
model = osim.Model('OTURUM5_YUKLE/rat_hindlimb_faz1a.osim')
st = model.initSystem()
cs = model.getCoordinateSet()
mus = model.getMuscles()
kp = json.load(open('kas_par.json'))
adlar = [mus.get(i).getName() for i in range(mus.getSize())]

g_ekseni = np.arange(0, 100.5, 0.5)
t_ekseni = g_ekseni/100.0*T
LMT = {n: [] for n in adlar}
for g in g_ekseni:
    t = g/100.0*T
    for k,c in enumerate(mcols):
        if c=='time': continue
        v = np.interp(t, mot[:,0], mot[:,k])
        cs.get(c).setValue(st, v if c in ('sacrum_x','sacrum_y','sacrum_z') else np.deg2rad(v), False)
    model.realizePosition(st)
    for i,n in enumerate(adlar):
        LMT[n].append(mus.get(i).getGeometryPath().getLength(st))

cikti = {}
for n in adlar:
    lmt = np.array(LMT[n])
    lmo, tsl, alp = kp[n]['lmo'], kp[n]['tsl'], kp[n]['alp']
    lm = np.sqrt(np.maximum(lmt - tsl, 1e-9)**2 + (lmo*np.sin(alp))**2)
    v = np.gradient(lm, t_ekseni)
    cikti[n] = np.column_stack([lm, v])
np.savez('rt_ara.npz', **cikti)
print('rt_ara.npz üretildi: %d kas × %s' % (len(cikti), cikti[adlar[0]].shape))
print('örnek TA lm/lmo aralığı: %.3f–%.3f' % ((cikti['TA'][:,0]/kp['TA']['lmo']).min(),
                                              (cikti['TA'][:,0]/kp['TA']['lmo']).max()))
