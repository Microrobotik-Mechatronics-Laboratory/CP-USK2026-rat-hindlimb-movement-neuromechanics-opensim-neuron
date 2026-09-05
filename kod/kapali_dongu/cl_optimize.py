# cl_optimize.py — EMERGENT denetleyiciyi CMA-ES ile optimize et (paralel).
# Fitness ve kapilar cl_selfcheck'ten; simulasyon cl_emergent (saf numpy, OpenSim gerekmez).
#   pip install cma
# Kosum:  python cl_optimize.py            (CMA-ES, paralel)
#         python cl_optimize.py random 300 (yedek: rastgele arama)
import numpy as np, json, sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # kod/yollar.py icin
from multiprocessing import Pool
from cl_selfcheck import fitness, verify, vec2P, PARSPEC
from yollar import VERI_CL
BEST = VERI_CL/'cl_best.json'

def _f(x):
    try: return fitness(vec2P(x), Tsim=6.0)   # arama = dogrulama ufku (Tsim=3 optimumu 6 s'de bilegi limite surukluyordu)
    except Exception: return 1e6

def run_cma(gens=60, popsize=32, workers=32, seed=0):   # Tsim=6 aramasi ~2x yavas; 60 jen ~6-7 saat
    import cma
    x0=[0.4]*len(PARSPEC); sig=0.25
    if BEST.exists():
        b=json.load(open(BEST))
        x0=[(b['P'][n]-lo)/(hi-lo) for (n,lo,hi) in PARSPEC]
        sig=0.10
        print("ilik baslangic: maliyet %.3f"%b['cost'])
    es=cma.CMAEvolutionStrategy(x0, sig, {'bounds':[0,1],'popsize':popsize,'seed':seed})
    best=(1e18,None); t0=time.time()
    with Pool(workers) as pool:
        for g in range(gens):
            X=es.ask(); F=pool.map(_f,X); es.tell(X,F)
            i=int(np.argmin(F))
            if F[i]<best[0]:
                best=(F[i],list(X[i])); print("jenerasyon %d: yeni en iyi maliyet %.3f (%.0f s)"%(g,F[i],time.time()-t0))
                _save(vec2P(best[1]),best[0])
            if es.stop(): break
    print("\n=== EN IYI (Tsim=6 dogrulama) ==="); P=vec2P(best[1]); verify(P,Tsim=6.0)
    return P

def run_random(n=300, workers=8):
    Xs=[np.random.rand(len(PARSPEC)) for _ in range(n)]; best=(1e18,None)
    with Pool(workers) as pool:
        F=pool.map(_f,Xs)
    i=int(np.argmin(F)); best=(F[i],list(Xs[i])); print("en iyi maliyet %.3f"%F[i])
    P=vec2P(best[1]); _save(P,best[0]); verify(P,Tsim=6.0); return P

def _save(P,cost):
    json.dump({'P':{k:(list(v) if isinstance(v,(list,np.ndarray)) else float(v) if isinstance(v,(int,float,np.floating)) else v)
                    for k,v in P.items()},'cost':float(cost)}, open(BEST,'w'),indent=2)

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='random': run_random(int(sys.argv[2]) if len(sys.argv)>2 else 300)
    else: run_cma()
    print("kaydedildi: cl_best.json (en iyi parametreler)")
