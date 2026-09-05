TITLE Graded (non-spiking) sigmoid synapse for the half-center oscillator
: --- USK26 koprusu ---------------------------------------------------------------
: Yarim-merkez osilatorunde (HCO) karsilikli inhibisyon DIKENE degil, presinaptik
: voltajin surekli sigmoid fonksiyonuna baglidir (oz_yu2021 3d: Ethresh, Eslope).
: NEURON'un yerlesik Exp2Syn'i olay tabanlidir ve bu islevi goremez, bu yuzden ayri
: bir nokta sureci yazildi.
:
:   s = 1/(1 + exp(-(vpre - ethr)/eslope))
:   i = gsyn * s * (v - esyn)
:
: vpre bir POINTER'dir; kurulumda presinaptik hucrenin _ref_v'sine baglanir.
: [tasarim] Kaynak mimari oz_yu2021'dir; parametre degerleri Aplysia olcegindedir ve
: bu projede yuruyus cevrimine (T = 0.387 s) kalibre edilir.
: ---------------------------------------------------------------------------------

NEURON {
	POINT_PROCESS GradeSyn
	RANGE gsyn, esyn, ethr, eslope, i, s
	POINTER vpre
	NONSPECIFIC_CURRENT i
}

UNITS {
	(mV) = (millivolt)
	(nA) = (nanoamp)
	(uS) = (microsiemens)
}

PARAMETER {
	gsyn   = 0		(uS)	: sinaptik tepe iletkenlik
	esyn   = -80	(mV)	: oz_yu2021 Tablo 2 -- E_syn^CPG (inhibitor)
	ethr   = 0		(mV)	: oz_yu2021 Tablo 2 -- Ethresh (0 = release, 30 = escape)
	eslope = 2		(mV)	: oz_yu2021 Tablo 2 -- Eslope
}

ASSIGNED {
	v		(mV)
	i		(nA)
	vpre	(mV)
	s
}

BREAKPOINT {
	s = 1/(1 + exp(-(vpre - ethr)/eslope))
	i = gsyn*s*(v - esyn)
}
