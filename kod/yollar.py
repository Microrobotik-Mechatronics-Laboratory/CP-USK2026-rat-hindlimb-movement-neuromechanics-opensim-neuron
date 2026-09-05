# =============================================================================
# yollar.py — depo icindeki kanonik yollar tek yerde.
# Ortam: her iki ortamda da calisir (yalniz standart kutuphane).
# Neden: betikler eskiden calisma dizinine ya da baska bir makinenin mutlak yoluna
# (KOK='/home/claude/oturum5/') bagliydi; boyle bir betik depoyu klonlayanda kosmaz.
# Kok, dosyanin kendi konumundan cozulur; betik nereden cagrilirsa cagrilsin ayni
# dosyayi bulur.
#
# Kullanim (kod/<altklasor>/ icindeki bir betikten):
#     import sys, pathlib
#     sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
#     from yollar import VERI, MODEL
# =============================================================================
from pathlib import Path

KOK       = Path(__file__).resolve().parents[1]

MODEL     = KOK / 'model'          # .osim modeller + Geometry/ mesh
VERI      = KOK / 'veri'           # girdi + uretilen seriler
VERI_CL   = VERI / 'kapali_dongu'  # kapali dongunun onceden pisirilmis izgaralari ve ciktilari
SEKILLER  = KOK / 'sekiller'       # yayin figurleri (04_KURALLAR: figur DAIMA buraya yazilir)
LITERATUR = KOK / 'literatur'      # ozutler + referans_degerler.json (tolerans bantlari)
NEURON    = KOK / 'neuron'         # Kim 2020 hoc/mod kaynak agaci
ARSIV     = KOK / 'arsiv'          # asilmis kusaklar; hesapta kullanilmaz

# Hattin cok yerden okunan tekil dosyalari
OSIM_FAZ1A = MODEL / 'rat_hindlimb_faz1a.osim'   # GUNCEL hesap modeli
MOT_SMOOTH = VERI  / 'rat_walk_bone_smooth.mot'  # olculmus kemik eklem acilari, T=0.387 s
U_SWING    = VERI  / 'u_swing_v2.csv'            # salinim fazi kas komutlari (38 kas x 71 ornek)
KAS_PAR    = VERI  / 'kas_par.json'
LEWIS_GRF  = VERI  / 'lewis_grf.json'
