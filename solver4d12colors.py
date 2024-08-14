from pycryptosat import Solver
from prettytable import PrettyTable
from prettytable import NONE
#from fpdf import FPDF
#import math
import sys
def var(x,y,z,t,s):
    assert(0<=x and x<=11 and 0<=y and y<=11 and 0<=z and z<=11 and 0<=t and t<=11 and 1<=s and s<=18)
    return 19*19*19*19*x+19*19*19*y+19*19*z+19*t+s

cls=Solver()
for x in range(12):
    for y in range(12):
        for z in range(12):
            for t in range(12):
            #each unit cube contains a string
                cls.add_clause([var(x,y,z,t,s) for s in range(1,19)])
                for s in range(1,19):
                    for ss in range(s+1,19):
                    #each unit cube contains at most one string
                        cls.add_clause([-var(x,y,z,t,s),-var(x,y,z,t,ss)])

#constraint C_{1,1}
for y in range(12):
    for z in range(12):
        for t in range(12):
            for x in range(12):
                for xx in range(x+1,12):
                    for s in range(1,10):
                        for ss in range(10,19):
                            cls.add_clause([-var(x,y,z,t,s),-var(xx,y,z,t,ss)])
                            cls.add_clause([-var(x,y,z,t,ss),-var(xx,y,z,t,s)])
 

#uslov I_2 je sadrzan uslovom da nema + na prvoj poziciji
 
#constraint C_{2,1}
for x in range(12):
    for z in range(12):
        for t in range(12):
            for y in range(12):
                for yy in range(y+1,12):
                    for s in range(1,4):
                        for ss in range(4,10):
                            cls.add_clause([-var(x,y,z,t,s),-var(x,yy,z,t,ss)])
                            cls.add_clause([-var(x,y,z,t,ss),-var(x,yy,z,t,s)])
                            cls.add_clause([-var(x,y,z,t,s+9),-var(x,yy,z,t,ss+9)])
                            cls.add_clause([-var(x,y,z,t,ss+9),-var(x,yy,z,t,s+9)])
 
#constraint C_{2,2}                          
for x in range(12):
    for z in range(12):
        for t in range(12):
            for y in range(12):
                for yy in range(y+1,12):
                    for s in range(7,10):
                        for ss in range(7,10):
                            cls.add_clause([-var(x,y,z,t,s),-var(x,yy,z,t,ss)])
                            cls.add_clause([-var(x,y,z,t,s+9),-var(x,yy,z,t,ss+9)])

#constraint C_{3,1}
for x in range(12):
    for y in range(12):
        for t in range(12):
            for z in range(12):
                for zz in range(z+1,12):
                    for s in range(1,19,3):
                        cls.add_clause([-var(x,y,z,t,s),-var(x,y,zz,t,s+1)])
                        cls.add_clause([-var(x,y,zz,t,s),-var(x,y,z,t,s+1)])
                        cls.add_clause([-var(x,y,z,t,s),-var(x,y,zz,t,s+2)])
                        cls.add_clause([-var(x,y,zz,t,s),-var(x,y,z,t,s+2)])

#constraint C_{3,2}
for x in range(12):
     for y in range(12):
         for t in range(12):
             for z in range(12):
                 for zz in range(z+1,12):
                     for s in range(3,19,3):
                         cls.add_clause([-var(x,y,z,t,s),-var(x,y,zz,t,s)])                       

#constraint C_4
for x in range(12):
    for y in range(12):
        for z in range(12):
            for t in range(12):
                for tt in range(t+1,12):
                    for s in range(1,19):
                        cls.add_clause([-var(x,y,z,t,s),-var(x,y,z,tt,s)])
                        
#constraint C*_{1,2}
for y in range(12):
    for z in range(12):
        for t in range(12):
            for x in range(12):
                for xx in range(x+1,12):
                    for s in range(1,19):
                        cls.add_clause([-var(x,y,z,t,s),var(xx,y,z,t,s)])
                        cls.add_clause([var(x,y,z,t,s),-var(xx,y,z,t,s)])
                        
#centrally-symmetric constraint
for y in range(12):
    for z in range(6):
        for t in range(6):
            for s in range(1,19):
                cls.add_clause([-var(0,y,z,t,s),var(0,y,z+6,t+6,s)])
                cls.add_clause([var(0,y,z,t,s),-var(0,y,z+6,t+6,s)])
                
for y in range(12):
    for z in range(6):
        for t in range(6,12):
            for s in range(1,19):
                cls.add_clause([-var(0,y,z,t,s),var(0,y,z+6,t-6,s)])
                cls.add_clause([var(0,y,z,t,s),-var(0,y,z+6,t-6,s)])
                
#NNN and XNN constraint
for y in range(12):
    for z in range(6):
        cls.add_clause([var(0,y,z,0,1)])
        cls.add_clause([var(0,y,z,6,10)])
                        
sat, solution = cls.solve()

#print(sat)
#print(solution)
#c=0
v=[]
for k in range(len(solution)):
    if solution[k]==True:
        v.append([(k // (19*19*19*19)), (k // (19*19*19)) % 19,(k // (19*19)) % 19, (k // 19) % 19, k % 19 ])

for elm in v:
    if elm[4]==1:
        elm[4]= 'NNN'
    elif elm[4]==2:
        elm[4]='NNX'
    elif elm[4]==3:
        elm[4]='NN+'
    elif elm[4]==4:
        elm[4]='NXN'
    elif elm[4]==5:
        elm[4]='NXX'
    elif elm[4]==6:
        elm[4]='NX+'
    elif elm[4]==7:
        elm[4]='N+N'
    elif elm[4]==8:
        elm[4]='N+X'
    elif elm[4]==9:
        elm[4]='N++'
    elif elm[4]==10:
        elm[4]='XNN'
    elif elm[4]==11:
        elm[4]='XNX'
    elif elm[4]==12:
        elm[4]='XN+'
    elif elm[4]==13:
        elm[4]='XXN'
    elif elm[4]==14:
        elm[4]='XXX'
    elif elm[4]==15:
        elm[4]='XX+'
    elif elm[4]==16:
        elm[4]='X+N'
    elif elm[4]==17:
        elm[4]='X+X'
    else:
        elm[4]='X++'
        
        

   
        
#print(v)
l=[]
for k in range(len(v)):
    if v[k][0]==0:
        l.append(v[k])

t0=PrettyTable()
t0.header = False
t0.vrules= NONE
for k in range(12):
        for i in range(12):
            t0.add_row([l[144*k+i+12*j][4] for j in range(12)])
        t0.add_row(['---' for j in range(12)])

#print(t0)
f = open("out12new.txt", "w")
f.write(t0.get_string())
f.close()


