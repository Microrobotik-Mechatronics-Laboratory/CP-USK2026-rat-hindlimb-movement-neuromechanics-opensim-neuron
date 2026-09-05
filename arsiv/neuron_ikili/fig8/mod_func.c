#include <stdio.h>
#include "hocdec.h"
/* change name when structures in neuron.exe change*/
/* and also change the mos2nrn1.sh script */
int nocmodl5_5;
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," CaL.mod");
fprintf(stderr," CaN.mod");
fprintf(stderr," Ca_conc.mod");
fprintf(stderr," KCa.mod");
fprintf(stderr," KDr.mod");
fprintf(stderr," Naf.mod");
fprintf(stderr," Nap.mod");
fprintf(stderr," SawtoothIClamp.mod");
fprintf(stderr," Xm.mod");
fprintf(stderr," module1_2.mod");
fprintf(stderr," module3.mod");
fprintf(stderr," syn_Ia.mod");
fprintf(stderr, "\n");
    }
_CaL_reg();
_CaN_reg();
_Ca_conc_reg();
_KCa_reg();
_KDr_reg();
_Naf_reg();
_Nap_reg();
_SawtoothIClamp_reg();
_Xm_reg();
_module1_2_reg();
_module3_reg();
_syn_Ia_reg();
}
