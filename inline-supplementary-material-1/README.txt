The simulation data used for the present study can be reproduced via the following steps. 


STEP 1: Set the value of "dpath" and "gcalbar" for the localization of Cav1.3 channels and their peak conductance over the motoneuron in the hoc file (add_pics_istim.hoc or add_pics_syns.hoc).

STEP 2: Set the value of "gmax_IaSyn" for the localization of muscle spindle inputs and thier peak conductance over the motoneuron in the hoc file (group_Ia.hoc).

STEP 3: Run the main hoc file (motor_unit.hoc).

STEP 4: Set the value of "amp" for the state of muscle length on the Xm[0] GUI window.

STEP 5: Push the "Init & Run" botton on the RunControl GUI window for starting simulation.

The STEP 1-5 should be repeated for simulations at different conditions of "dpath" and "xm". The defualt values of "dpath" and "xm" were set to 600 microns and -8 mm for Figs 2-7 and 800 microns and -16 mm for Figs 8. For Fig 9, the defualt value of "dpath" was set to 800 microns and the value of "Gaff" varied from 0 to 19 uS/cm^2 in a sinusoidal form. The simulation codes were compiled for use in the Microsoft Windows operating system (version > 7 and 64 bit).