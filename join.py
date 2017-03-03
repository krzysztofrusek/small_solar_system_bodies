from telnetlib import Telnet
import os
import sys
import time
import datetime as dt
import csv
import argparse
import math

import glob
with open('o2.txt','w') as o:
    
    for f in glob.glob('o_poprawka*'):
        with open(f,'r') as file:
            for line in file:
                sline=line.split(' ')
                sline=list(filter(lambda x:bool(x),line.split(' ')))

                #odleglosc w duzej dokladnosci
                if len(sline[10])>10:
                    sline.insert(10,'0.00')
                    #pass
                tmp=sline[16].split('/')
                sline[16]=tmp[0]
                if tmp[1]:                    
                    sline.insert(16,tmp[1])
                #o.write('lll'+str(n)+str(sline)+'\n')
                o.write(",".join(sline))
