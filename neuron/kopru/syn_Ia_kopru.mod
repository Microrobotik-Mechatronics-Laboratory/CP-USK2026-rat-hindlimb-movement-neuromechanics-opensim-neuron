TITLE Ia afferent synapse with an externally driven conductance scale
: --- USK26 koprusu ---------------------------------------------------------------
: Kim'in syn_Ia.mod'u tonik bir kacak akimdir: i = gmax*(v-e), gmax sabit ve kas boyuna
: gore ELLE uc degerden biri secilir (group_Ia.hoc:7-9; 0 / 9.3e-6 / 19e-6 S/cm2).
: Kapali donguda gmax her kopru adiminda igcik oraninin r(t) fonksiyonu olarak DEGISIR
: (PREPRINT 6.3: "bizim tasarimimizda xm surekli bir degiskendir").
:
: gmax dogrudan yazilabilirdi ama IaSyn bir YOGUNLUK mekanizmasidir ve tek hucrede
: D_path<1400 um kosulunu saglayan 1692 segmente takilir; her adimda hucre basina 1692
: atama, 38 havuzda adim basina ~64000 atama demektir. Bunun yerine olcek carpani gsc bir
: POINTER olarak disaridan tek bir skalere baglanir: kurulumda bir kez setpointer, sonra
: adim basina HUCRE BASINA TEK yazma.
:
: gmax birim-alan taban iletkenligi (Kim'in optimal boy degeri) olarak kalir; gsc birimsiz
: olcektir. gsc=1 iken davranis Kim'in orijinaliyle ayni olur.
: ---------------------------------------------------------------------------------

NEURON {
	SUFFIX IaKopru
	RANGE gmax, e, i
	POINTER gsc
	NONSPECIFIC_CURRENT i
}

UNITS {
	(mV) = (millivolt)
	(mA) = (milliamp)
	(S)  = (siemens)
}

PARAMETER {
	gmax = 9.3e-6	(S/cm2)		: group_Ia.hoc:8 -- optimal kas boyu (xm = -8 mm) tabani
	e    = 0		(mV)		: syn_Ia.mod -- ters donusum potansiyeli
}

ASSIGNED {
	v	(mV)
	i	(mA/cm2)
	gsc				: birimsiz olcek; disaridan (Python) yazilir
}

BREAKPOINT {
	i = gmax*gsc*(v - e)
}
