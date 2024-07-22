# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 22:03:11 2024

@author: sun
"""

import numpy as np
import struct
import os
import shutil
import matplotlib.pyplot as plt

inlayers=49

ihirac=1
ilblf4=1
icntnm=1
iaersl=0
iemit=1
iscan=0
ifiltr=0
iplot=0
itest=0
iatm=1
imrg=1
ilas=0
iod=1
ixsect=0

bwn=2326
ewn=2631
delta_wn=0.01
n_wv=int((ewn-bwn)/delta_wn)+1

nOD=int(n_wv/2400)

height=np.zeros(inlayers)

gas_od=np.zeros([inlayers,n_wv])

od_all=np.zeros([inlayers,n_wv+nOD*10])

wvn=np.linspace(bwn,ewn,num=n_wv)

for ii in range(1,inlayers+1):
    OD_fname='ODint_{:03d}'.format(ii)
    with open(OD_fname,'rb') as fb:
        fb.seek(1056+8+24+8+4)  #ignore discription and second number data
        data3=fb.read(n_wv*4+nOD*40)
        data3=struct.unpack(f'{n_wv+nOD*10}f',data3)           
    data4=np.array(data3)
    od_all[ii-1,:]=data4
    print('Finishing OD file:'+str(ii))
     
#    index=[0,1,2,3,4,5,6,7,8,9]
    indice=[] 
    for iOD in range(1,nOD+1):
        index=[x for x in range(2400*iOD+10*(iOD-1),2400*iOD+10*iOD)]
        indice.append(index)
#    print(indice)
    gas_od[ii-1,:]=np.delete(od_all[ii-1,:],indice)    

od_fname='GAS_OD_IBMAX_0_{:02d}'.format(2)
np.savetxt(od_fname,gas_od.T,fmt='%20.8e')

gasTau=np.sum(gas_od.T,axis=1)
gasT=np.exp(-gasTau)

plt.plot(wvn,gasT)
#plt.yscale('log')
plt.show()

        
        
        
    
