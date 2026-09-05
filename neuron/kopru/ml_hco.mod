TITLE Morris-Lecar membrane for the CPG half-centers
: --- USK26 koprusu ---------------------------------------------------------------
: CPG yarim-merkezleri (RG-F, RG-E) icin iletkenlik tabanli Morris-Lecar hucresi.
: Mimari kaynagi oz_yu2021 3a (Skinner 1994 / Zhang-Lewis 2013 parametre hatti);
: izole hucre kararli sabit noktadadir, salinim ancak karsilikli inhibisyonla dogar
: (oz_yu2021 3b madde 1). Bu, PREPRINT 6.1'in "neden yarim-merkez" gerekcesidir.
:
:   minf = 0.5*(1 + tanh((v - e1)/e2))
:   winf = 0.5*(1 + tanh((v - e3)/e4))
:   tauw = 1/(phin*cosh((v - e3)/(2*e4)))
:   i    = -iext + gl*(v-el) + gca*minf*(v-eca) + gk*w*(v-ekml)
:
: BIRIM UYARISI: oz_yu2021 Tablo 2 iletkenlikleri "uS/cm2" diye yaziyor ama Iext ile
: 1000 kat tutarsiz cikiyor (0.005 uS/cm2 x 50 mV = 0.25 nA/cm2, Iext ise 0.8 uA/cm2).
: mS/cm2 okundugunda tutarli. Ozetin kendi uyarisi da bu yonde. Burada degerler NEURON'un
: standart yogunluk birimine (S/cm2) cevrilmistir: 0.005 mS/cm2 = 5e-6 S/cm2.
:
: [tasarim] phin, serbest cevrim periyodunu olculmus yuruyus cevrimine (T = 0.387 s)
: oturtmak icin kalibre edilir; Yu ve Thomas'in degeri (0.0005 /ms) Aplysia olceginde
: T ~ 2254 ms verir. Kalibrasyon kod/kopru/devre_par.json'da kayitlidir.
: ---------------------------------------------------------------------------------

NEURON {
	SUFFIX MLhco
	NONSPECIFIC_CURRENT i
	RANGE gl, gca, gk, el, eca, ekml, iext, e1, e2, e3, e4, phin, minf, winf
}

UNITS {
	(mV) = (millivolt)
	(mA) = (milliamp)
	(S)  = (siemens)
}

PARAMETER {
	gl   = 5e-6		(S/cm2)		: 0.005 mS/cm2  -- Tablo 2
	gca  = 1.5e-5	(S/cm2)		: 0.015 mS/cm2  -- Tablo 2
	gk   = 2e-5		(S/cm2)		: 0.020 mS/cm2  -- Tablo 2
	el   = -50		(mV)		: Tablo 2
	eca  = 100		(mV)		: Tablo 2
	ekml = -80		(mV)		: Tablo 2 (adi ek degil: NEURON'un k iyonuyla karismasin)
	iext = 8e-4		(mA/cm2)	: 0.8 uA/cm2   -- Tablo 2
	e1   = 0		(mV)		: Tablo 2 -- E1 (minf orta noktasi)
	e2   = 15		(mV)		: Tablo 2 -- E2 (minf egimi)
	e3   = 0		(mV)		: Tablo 2 -- E3 (winf orta noktasi)
	e4   = 15		(mV)		: Tablo 2 -- E4 (winf egimi)
	phin = 0.0005	(/ms)		: Tablo 2 -- phiN; kalibrasyonla degistirilir
}

ASSIGNED {
	v		(mV)
	i		(mA/cm2)
	minf
	winf
	tauw	(ms)
}

STATE { w }

INITIAL {
	rates(v)
	w = winf
}

BREAKPOINT {
	SOLVE states METHOD cnexp
	rates(v)
	i = -iext + gl*(v - el) + gca*minf*(v - eca) + gk*w*(v - ekml)
}

DERIVATIVE states {
	rates(v)
	w' = (winf - w)/tauw
}

PROCEDURE rates(vm (mV)) {
	minf = 0.5*(1 + tanh((vm - e1)/e2))
	winf = 0.5*(1 + tanh((vm - e3)/e4))
	tauw = 1/(phin*cosh((vm - e3)/(2*e4)))
}
