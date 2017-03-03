from telnetlib import Telnet
import os
import sys
import time

#1; E e geo eclip 2018-jan-01 00:00 2018-jan-02 00:00 1d



#ASTNAM=1 TABLE_TYPE= 'ELEMENTS e geo eclip START_TIME='2018-jan-01' STOP_TIME='2018-jan-02'   STEP_SIZE='1 d'



tn=Telnet('horizons.jpl.nasa.gov', 6775)
#tn.set_debuglevel(10)

for i in range(30):
    tn.read_until(b"Horizons>")
    tn.write(b"%d;\n"%(i+1))
    parametry=tn.read_until(b"?,<cr>:").decode('ascii')
    #print(parametry)
    omstart=parametry.find(" OM= ")+5
    omend=parametry.find(" ",omstart)

    OM= float(parametry[omstart:omend])
    print(OM)
    tn.write(b"\n")
tn.close()