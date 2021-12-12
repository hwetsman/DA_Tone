""" this attempt to create DAtone over time taking into account genetic polymorphism
.02 tries to make all variable global"""

import matplotlib.pyplot as plt
import streamlit as st
#import numpy as np
#import random
#import pandas as pd

def Calc_IC(ic_da,reuptake,produced,ic_loss,packaged):
    ic_da = ic_da +reuptake +produced - ic_loss - packaged
    return ic_da

def Calc_IV(iv_da,released,packaged):
    #iv_da = iv_da - released + packaged - iv_loss
    iv_da = iv_da - released + packaged
    return iv_da

def Calc_Released(iv_da,end_tone,percent_s):
    if iv_da > 10:
        released = max(1.5 * (end_tone/percent_s),0)
    if iv_da <= 10:
        released = 0
    print(released,'released')
    return released
    
def Calc_EC(ec_da,released,ec_loss,reuptake):
    ec_da = ec_da + released - ec_loss - reuptake
    return ec_da

def Calc_DA_Tone(l_receptors):
    tone = l_receptors * ec_da
    return tone

def Calc_IC_End(ic_end,end_pro,end_rel,ic_end_loss):
    ic_end = ic_end + end_pro - end_rel - ic_end_loss
    return ic_end

def Calc_EC_End(ec_end,end_rel,ec_end_loss):
    ec_end = ec_end + end_rel - ec_end_loss
    return ec_end

def Calc_DA_Recep(ec_da, da_threshold, da_receptors, max_receptors):
    if ec_da > da_threshold:
        da_receptors = max(da_receptors * .9, 0)
        #print(da_receptors,'recptors')
    else:
        da_receptors = min(da_receptors * 1.05, max_receptors)
        #print(da_receptors,'receptors')
    return da_receptors

################# Backbone Model
extracellular = []
time = []
intravesicular = []
intracellular = []
toneset = []
icend = []
ecend = []
endtone=[]
recept_list = []
#start with set amounts for compartments
iv_da = 1
ic_da = 1
ec_da = 1
ic_end = 1
ec_end = 10
end_tone = 10
#cycles = st.slider('Cycles',10,25000,500)
cycles = 500
max_da_receptors = 30 ##########DRD2 rs1800497
#max_da_receptors = st.slider('Maximum DA Receptors',10,100,30)
da_receptors = 1.9  ########## psychosocial 
#da_receptors = st.slider('Beginning DA Receptors',1,30,1.9) 
percent_s = .9 ###DRD2 rs2283265
#percent_s = st.slider('Percent D2s',.01,1,.9)
da_threshold = 20
#da_threshold = st.slider('DA Threshold for Receptor Drop',100,1,20)
reuptake_constant = .25
#reuptake_constant = st.slider('DAT Constant',.01,1,.25)
ic_loss_constant = .1
#ic_loss_constant = st.slider('MAOB Constant',.01,1,.1)
vmat_constant = .8
#vmat_constant = st.slider('VMAT Constant', .01,1,.8)


for i in range(cycles):
    #ic_da
    produced =5   
    packaged = max(ic_da * vmat_constant,0) 
    ic_loss = max(ic_da * ic_loss_constant,0) 
    reuptake = max(ec_da * reuptake_constant,0)
    ic_da = Calc_IC(ic_da,reuptake,produced,ic_loss,packaged)
    intracellular.append(ic_da)
    
    #iv_da
    #iv_loss = max(0,iv_da * .1)
    
    released = Calc_Released(iv_da,end_tone,percent_s)
    
    #iv_da = Calc_IV(iv_da,released,packaged,iv_loss)
    iv_da = Calc_IV(iv_da,released,packaged)
    intravesicular.append(iv_da)
        
    #ec_da
    ec_loss = max(.03 * ec_da,0)
    ec_da = Calc_EC(ec_da,released,ec_loss,reuptake)
    print(ec_da)
    print(da_threshold)
    extracellular.append(ec_da)
    time.append(i)
    
    #da_receptors = 3
    da_receptors = Calc_DA_Recep(ec_da, da_threshold, da_receptors, max_da_receptors)
    
    #tone
    l_receptors = min(da_receptors,max_da_receptors) * (1-percent_s)
    print(l_receptors,'l receptors')
    recept_list.append(l_receptors)

    da_tone = Calc_DA_Tone(l_receptors)
    print(da_tone,'da tone')
    toneset.append(da_tone)
    
######### ENDORPHIN SIDE ###################################################    
    end_pro = 1.25
    ic_end_loss = max(0,.01 * ic_end)
    end_rel = .01 * da_tone
    ic_end = max(0,Calc_IC_End(ic_end,end_pro,end_rel,ic_end_loss))
    icend.append(ic_end)
    
    ec_end_loss = max(0,.1 * ec_end)
    ec_end = max(0,Calc_EC_End(ec_end,end_rel,ec_end_loss))
    ecend.append(ec_end)

    end_rec = 1
    end_tone = ec_end * end_rec
    endtone.append(end_tone)

print(min(recept_list),max(recept_list),'receptlist')
print(min(extracellular),max(extracellular),'extracellular')    
plt.scatter(time,extracellular, color = 'black')
#plt.scatter(time,intracellular, color = 'magenta')
#plt.scatter(time,intravesicular,color = 'green')
plt.scatter(time,toneset, color = 'black',alpha = .05)
plt.scatter(time,recept_list, color = 'blue')    
#plt.scatter(time,icend, color = 'red')
#plt.scatter(time,ecend,color = 'blue')
#plt.scatter(time,endtone,color = 'green')
#plt.scatter(time,pro, color = 'red')
#plt.scatter(time,reup, color = 'cyan')
plt.show()