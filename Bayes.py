# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 09:18:48 2019

@author: DJ萧
"""

import numpy as np
import pymysql
import pandas as pd
import math

class Prior_table:
    table_count=0
##############build prior probability table###################################
    def __init__(self,dataset,labels):
        m,n=np.shape(dataset)
        Pc=[]
        ljudge=list(set(dataset[:,-1]))
        Dc=[]
        Uc=[]
        Thetac=[]
        for j in range(2):
            cursor.execute(str("select * from watermelon where %s='%s'"%(labels[-1],ljudge[j])))
            info=cursor.fetchall()
            Dc.append(len(info))
            Pc.append((len(info)+1)/(m+2))
        Pxc=[[] for i in range(n-1) ]
        Pxclis=[[] for i in range(n-1) ]
        for i in range(n-1):
            label=list(set(dataset[:,i]))
            if len(label)<15:
                for ii in range(2):
                    for j in range(len(label)):
                        cursor.execute(str("select * from watermelon where %s='%s' and %s='%s'"%(labels[i],label[j],labels[-1],ljudge[ii])))
                        info=cursor.fetchall()
                        Pxc[i].append((len(info)+1)/(float(Dc[ii])+len(label)))
                        Pxclis[i].append("%s='%s'|%s='%s'"%(labels[i],label[j],labels[-1],ljudge[ii]))
            else:
                uc=[];tc=[]
                for ii in range(2):
                     cursor.execute(str("select * from watermelon where %s='%s'"%(labels[-1],ljudge[ii])))
                     info=cursor.fetchall()
                     info=np.array(info)
                     info=list(map(float,info[:,i+1]))                    
                     uc.append(np.mean(info))
                     tc.append(np.std(info,ddof=1))
                Uc.append(uc)
                Thetac.append(tc)
        self.dataset=dataset
        self.labels=labels
        self.Pc=Pc
        self.Pxc=Pxc
        self.Pxclis=Pxclis
        self.Uc=Uc
        self.Thetac=Thetac
        Prior_table.table_count+=1
###############################################################################

##################execute bayes classification################################         
def Bayestry(test,table):
    m,n=np.shape(table.dataset)
    ljudge=list(set(table.dataset[:,-1]))
    P=[0.0,0.0]
    for ii in range(2):
        P[ii]=table.Pc[ii]
        for i in range(n-3):
            for j in range(len(table.Pxclis[i])):
                if table.Pxclis[i][j]==str("%s='%s'|%s='%s'"%(table.labels[i],test[i],table.labels[-1],ljudge[ii])):
                    tloc=j
            P[ii]=P[ii]*table.Pxc[i][tloc]
        for i in range(n-3,n-1):
            Pcons=1.0/(math.sqrt(2*math.pi)*table.Thetac[i+3-n][ii])*math.exp(-(float(test[i])-table.Uc[i+3-n][ii])**2/(2*table.Thetac[i+3-n][ii]**2))
            P[ii]=P[ii]*Pcons
    print(P)
    if P[0]>P[1]:
        print("否")
    else:
        print("是")
################################################################################

host='localhost'
port=3306
user='root'
password='your password'
db='watermelon(database name)'
conn=pymysql.connect(host=host,port=port,user=user,password=password,database=db)
dataset=pd.read_sql('select * from watermelon',conn)
cursor=conn.cursor()
#cursor.execute('select * from watermelon')
#dataset=cursor.fetchall()
dataset=dataset.drop('编号',axis=1)
labels=dataset.columns
dataset=np.array(dataset)

Ptable=Prior_table(dataset,labels)
test=['青绿','蜷缩','浊响','清晰','凹陷','硬滑',0.679,0.460]
Bayestry(test,Ptable)

        

                
    
