from telnetlib import Telnet
import os
import sys
import time
import datetime as dt
import csv
import argparse
import math

def make_qa(date,b):
    qa='''Select ... [A]pproaches, [E]phemeris, [F]tp,[M]ail,[R]edisplay, [S]PK,?,<cr>: E
Observe, Elements, Vectors  [o,e,v,?] : o
Coordinate center [ <id>,coord,geo  ] : geo
Starting UT  [>=   1599-Dec-11 23:59] : 2017-Jun-10 00:00
Ending   UT  [<=   2500-Dec-30 23:58] : 2017-Jun-11 00:00
Output interval [ex: 10m, 1h, 1d, ? ] : 1d
Accept default output [ cr=(y), n, ?] : n
Select table quantities [ <#,#..>, ?] : 1,9,19,20,23,24,25,28,36
Output reference frame [J2000, B1950] : J2000
Time-zone correction   [ UT=00:00,? ] : 0
Output UT time format   [JD,CAL,BOTH] : CAL
Output time digits  [MIN,SEC,FRACSEC] : MIN
Output R.A. format       [ HMS, DEG ] : HMS
Output high precision RA/DEC [YES,NO] : NO
Output APPARENT [ Airless,Refracted ] : Refracted
Set units for RANGE output [ KM, AU ] : AU
Suppress RANGE_RATE output [ YES,NO ] : YES
Minimum elevation [ -90 <= elv <= 90] : -90
Maximum air-mass  [ 1 <=   a  <= 38 ] : 38
Print rise-transit-set only [N,T,G,R] : N
Skip printout during daylight [ Y,N ] : N
Solar elongation cut-off   [ 0, 180 ] : [0,180]
Local Hour Angle cut-off       [0-12] : [0-12]
Spreadsheet CSV format        [ Y,N ] : N
Select... [A]gain, [N]ew-case, [F]tp, [K]ermit, [M]ail, [R]edisplay, ? : N
'''
    def qa_iter(sq):
        for line in qa.splitlines():
            colon=line.rfind(": ")
            yield line[0:colon+1],line[colon+2:len(qa)]

    qa=[(q,a) for q,a in qa_iter(qa)]
    
    if b:
        return qa
    else:
        qa[2]=('Use previous center  [ cr=(y), n, ? ] :','y')
        qa[3]=(qa[3][0],date.strftime("%Y-%b-%d %H:%M"))
        qa[4]=(qa[4][0],(date+dt.timedelta(days=1)).strftime("%Y-%b-%d %H:%M"))
        return qa
        


    

def bootstrap(tn):
    tn.read_until(b"Horizons>")
    tn.write(b"1;\n") # ceres
    for q,a in make_qa(None,True):
        out=tn.read_until(q.encode('ascii')).decode('ascii')
        #print(out)
        tn.write(a.encode('ascii'))
        tn.write(b"\n")
    tn.write(b"\n")
    tn.write(b"\n")
    tn.read_until(b"Horizons>")
    print('bootstrap finished ...')

def load_bodies(dopythona):
#    with open("dopythona.txt", 'rt') as csvfile:
    with open(dopythona, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        asteroidy=[int(row[0]) for row in reader]    
    return asteroidy
    
def get_oms(tn, bodies):
    def f(b):
        tn.write(b"%d;\n"%(b))
        parametry=tn.read_until(b"?,<cr>:").decode('ascii')
        #print(parametry)
        omstart=parametry.find(" OM= ")+5
        omend=parametry.find(" ",omstart)
        print('OM for ', b, ' loaded')

        OM= float(parametry[omstart:omend])
		
        return OM
    return [f(b) for b in bodies]
'''
def correction(x):
    return -1.849 + 1.911*math.sin(1.721e-02*x + 1.308)

    
def observation_dates(om):
    #refs=[dt.date(r,3,21) for r in range(2017,2023)] 
    #refs=[dt.date(r,3,21) for r in range(2017,2019)]
    refs=[dt.datetime(2017,3,20,10,29),
      dt.datetime(2017,9,22,20,2),
      dt.datetime(2018,3,20,16,15),
      dt.datetime(2018,9,23,1,54),
      dt.datetime(2019,3,20,21,58),
      dt.datetime(2019,9,23,7,50),
      dt.datetime(2020,3,20,3,50),
      dt.datetime(2020,9,22,13,51),
      dt.datetime(2021,3,20,9,37),
      dt.datetime(2021,9,22,19,21),
      dt.datetime(2022,3,20,15,33),
      dt.datetime(2022,9,23,1,4)]

    #delta=[dt.timedelta(days=om/360*365.25), dt.timedelta(days=((om+180)/360*365.25) % 365 )]
    #delta=[dt.timedelta(days=om/360*365.25)]
    #delta2=[x+correction(x)/360*365.25 for x in delta]
    x=dt.timedelta(days=om/360*365.25)
    x=x + x+correction(x)/360*365.25
    ret= [ref + x for ref in refs]
    ret.sort()
    return ret

'''

def correction(x):
    return -1.849 + 1.911*math.sin(1.721e-02*x + 1.308)
    
ROK=365.25636

def observation_dates(om):
    refs=[dt.datetime(2017,3,20,10,29),
      dt.datetime(2018,3,20,16,15),
      dt.datetime(2019,3,20,21,58),
      dt.datetime(2020,3,20,3,50),
      dt.datetime(2021,3,20,9,37),
      dt.datetime(2022,3,20,15,33)]

    delta=[om/360*ROK, ((om+180)/360*ROK) % ROK ]
    delta2=[x-correction(x)/360*ROK for x in delta]

    ret= [ref + dt.timedelta(days=x) for ref in refs for x in delta2 ]
    ret.sort()
    return ret

    
def make_final_line(out,n):
    start=out.find('$$SOE')
    stop=out.find('$$EOE')
    important=out[start+6:stop]
    #print(important.splitlines()[0])
    ret='%08d %s' % (n,important.splitlines()[1])
    return ret


def main():
    
    parser = argparse.ArgumentParser(description='JPL')
    parser.add_argument('-f', help='file',  required=True)
    args = parser.parse_args()
    
    tn=Telnet('horizons.jpl.nasa.gov', 6775)
    #tn.set_debuglevel(1)

    outf=open('o_'+args.f, 'w')
    dopythona = args.f

    bootstrap(tn)

    #omy

    asteroidy=load_bodies(dopythona)
    oms=get_oms(tn, asteroidy)


    for i in range(len(oms) ):
        tn.write(b"\n") 
        tn.read_until(b"Horizons>")
        print(i)
        for date in observation_dates(oms[i]):
            tn.write(b"%d;\n"%(asteroidy[i])) 
            j=0
            for q,a in make_qa(date,False):
                out=tn.read_until(q.encode('ascii')).decode('ascii')
                j+=1
                if j == 25:
                    line = make_final_line(out,asteroidy[i])
                    print(line)
                    outf.write(line)
                    outf.write('\n')
                tn.write(a.encode('ascii'))
                tn.write(b"\n")

        
    tn.write(b"\n")
    tn.close()
    outf.close()
    
if __name__=="__main__":
    main()
