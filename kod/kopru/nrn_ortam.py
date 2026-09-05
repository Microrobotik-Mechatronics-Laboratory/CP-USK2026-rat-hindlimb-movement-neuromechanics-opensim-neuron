# =============================================================================
# nrn_ortam.py — NEURON'u dogru calisma dizininde ve dogru sirayla ayaga kaldirir.
# Ortam: kopru (Python 3.13, ~/.venvs/usk26-kopru)
# Cikti: h (HocObject) ve derlenmis mekanizmalar yuklu bir NEURON ortami.
#
# Neden ayri bir modul: NEURON tarafinin iki kirilgan kurali var ve ikisi de tek yerde
# tutulmazsa her betikte tekrar hata uretir.
#
# KURAL 1 — yollar goreli olmak zorunda. NEURON'un HOC dizgi arayuzu ASCII disi karakter
#   kabul etmiyor ("python string arg cannot decode into c_str"); bu reponun yolu Turkce
#   karakter iceriyor (.../USK26 - Sican arka bacak .../). Bu yuzden once os.chdir ile
#   neuron/fig2_4_6 icine girilir, HOC'a yalniz goreli ad verilir. (DOGRULAMA N, olcum 4)
#
# KURAL 2 — mekanizmalar KENDILIGINDEN yuklenir. NEURON, import aninda calisma dizinindeki
#   arm64/libnrnmech.dylib dosyasini otomatik yukler. Bu yuzden chdir IMPORT'TAN ONCE olmali
#   ve ayrica nrn_load_dll cagrilmamalidir; cagrilirsa "user defined name already exists: CaL"
#   hatasi alinir.
# =============================================================================
import os, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # kod/yollar.py icin
from yollar import NEURON_FIG

if 'neuron' in sys.modules:
    raise RuntimeError('nrn_ortam once ice aktarilmali: neuron zaten yuklu, '
                       'mekanizmalar yanlis dizinden gelmis olabilir')

os.chdir(NEURON_FIG)                 # KURAL 1 + KURAL 2: import'tan ONCE
from neuron import h                 # noqa: E402 -- sira kasitli
h.load_file('stdrun.hoc')

# Mekanizmalarin gercekten yuklendigini burada dogrula; sessizce eksik yuklenirse
# hata cok sonra, anlamsiz bir yerde patlar.
for mek in ('CaL', 'IaSyn', 'Naf', 'KDr', 'CaN', 'KCa', 'Nap', 'Ca_conc'):
    if not hasattr(h, mek):
        raise RuntimeError('NEURON mekanizmasi yuklenmedi: %s -- neuron/fig2_4_6 icinde '
                           'nrnivmodl kosuldu mu?' % mek)


def yukle(*hoc_dosyalari):
    """Verilen HOC dosyalarini sirayla acar. Adlar neuron/fig2_4_6'ya GORELI olmalidir."""
    for f in hoc_dosyalari:
        h.xopen(f)
