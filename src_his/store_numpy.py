from all_index import *



from lxml import etree
import xlwt
import sys
import os
from shutil import copy
from dateutil import parser
from datetime import datetime
import numpy as np 





###############################################VAR#################################
state_D={}   #Dict for District
dist_D={}   #Dict for District
market_D={} #Dict for Market 
DM_pair={}  #district market pair
var_D={} #Dict for Market 

state_count=0   #countict for countistrict
dist_count=0   #countict for countistrict
market_count=0 #countict for Market 


var_count=0
VAR=(dist_D,market_D,var_D,dist_count,market_count,var_count)

###################################################################################

def save_all_meta_data(path="/media/ranjan/DATAPART/agri_data/"):
    np.savez(path+"meta_data.npz",state_D=state_D,dist_D=dist_D,market_D=market_D,DM_pair=DM_pair,var_D=var_D,state_count=state_count,dist_count=dist_count,market_count=market_count,var_count=var_count)

def load_all_meta_data(file_path="/media/ranjan/DATAPART/agri_data/meta_data.npz"): 
    global VAR
    
    #(dist_D,market_D,var_D,dist_count,market_count,var_count)=VAR
    global dist_count
    global market_count
    global var_count

    global dist_D
    global DM_pair
    global market_D
    global var_D
    Dict=np.load(file_path)
    dist_count=(Dict['dist_count']).tolist()
    market_count=Dict['market_count'].tolist()
    var_count=Dict['var_count'].tolist()
    state_D=Dict['state_D'].tolist()
    dist_D=Dict['dist_D'].tolist()
    var_D=Dict['var_D'].tolist()
    market_D=Dict['market_D'].tolist()
    DM_pair=Dict['DM_pair'].tolist()




#put new key if the key is not there otherwise return the same
def Put_new_key(D,key,base_count):
    if(not D.has_key(key)):
        base_count=base_count+1
        D[key]=base_count
    
    return D,base_count
        






#parse one file under items and save it to numpy 
def parse_file(file_path):
    global VAR
    
    #(dist_D,market_D,var_D,dist_count,market_count,var_count)=VAR
    global dist_count
    global market_count
    global var_count

    global dist_D
    global market_D
    global var_D


    f=open(file_path)
    tag=f.readline()
    for i in range(4):
        t=f.readline()

    Data=[]

    while(True):
        Ls=[]
        while(True):
            t=f.readline()
            Ls.append(t)

            if(t=='\t\t</tr><tr>\r\n'):
                break
            if(t==""):
                break

        if(t==""):
            break
        dist=Ls[3].split("\">")[1].split("</")[0]
        mrkt=Ls[5].split("\">")[1].split("</")[0]
        item=Ls[7].split("\">")[1].split("</")[0]
        var=Ls[9].split("\">")[1].split("</")[0]
        grad=Ls[11].split("\">")[1].split("</")[0]
        min_p=float((Ls[13].split("\">")[1].split("</")[0]))
        max_p=float(Ls[15].split("\">")[1].split("</")[0])
        mod_p=float(Ls[17].split("\">")[1].split("</")[0])
        date=Ls[19].split("\">")[1].split("</")[0]

        date=parser.parse(date)-datetime(2009, 1, 1)                    
        day=date.days

        dist_D,dist_count=Put_new_key(dist_D,dist,dist_count)
        #print dist_count
        market_D,market_count=Put_new_key(market_D,mrkt,market_count)
        var_D,var_count=Put_new_key(var_D,var,var_count)

        Data.append([dist_D[dist],market_D[mrkt],var_D[var],min_p,max_p,mod_p,day])
        #print(Data)
        
    Data=np.array(Data)
    return Data



#read all files under particular items and covert it to numpy for particular items
def read_all(path="/media/ranjan/DATAPART/agri_data/root_raw/Onion/"):
    #file_path="/media/ranjan/DATAPART/agri_data/root/Onion/Agmarknet_Parice_Report(8).xls"
    #VAR=(dist_D,market_D,var_D,dist_count,market_count,var_count)

    D=[]
    for d in os.listdir(path):
        print("processing dir",d)
        file_path=path+d
        data=parse_file(file_path)
        D.append(data)

    D=np.concatenate(D,axis=0)
    return D





#inilize all variables by the data
def find_unique(D):
    dist_id=np.unique(D[:,0])
    global DM_pair
    for idx in dist_id:
        mrkt_idl=list(np.unique(D[D[:,0]==idx][:,1]))
        DM_pair[idx]=mrkt_idl
        if(DM_pair.has_key(idx)):
            DM_pair[idx]=list(np.unique(DM_pair[idx]+mrkt_idl))
        else:
            DM_pair[idx]=mrkt_idl








#save data market(code) wise  under dist(code)  and intem
#save the data in District Code Wise folder and market
def save_data_district_market(D,numpy_path="/media/ranjan/DATAPART/agri_data/root/Onion/"):
    for dist in DM_pair.keys():
        ml=DM_pair[dist]   #marekt list

        dist_path=numpy_path+str(int(dist))+"/"
        t1=D[D[:,0]==dist]
        if(t1.shape[0]==0):    
            continue 

        try:
            os.mkdir(dist_path)
        except:
            pass
        for m in ml:
            file_name=dist_path+str(int(m))+".npy"
            #print(file_name) 
            t2=t1[t1[:,1]==m] 
            t2=t2[:,2:]     
            t2=t2[t2[:,-1].argsort()]       #sort according to the price
            if(t2.shape[0]!=0):    
                np.save(file_name,t2)



#save all data to numpy
def save_all(raw_root_path="/media/ranjan/DATAPART/agri_data/root_raw/",numpy_root_path="/media/ranjan/DATAPART/agri_data/root/"):
    for d in os.listdir(raw_root_path):
        print("processing",d)
        item_raw_path=raw_root_path+d+"/"
        item_numpy_path=numpy_root_path+d+"/"
        D=read_all(path=item_raw_path)
        find_unique(D)

        try:
            os.mkdir(item_numpy_path)
        except:
            pass

        save_data_district_market(D,numpy_path=item_numpy_path)




"""
if __name__ == "__main__":
    save_all()      #save_all data to numpy 
    save_all_meta_data()

"""


"""
load_all_meta_data()
dist_D_inv = dict(zip(dist_D.values(), dist_D.keys()))
market_D_inv = dict(zip(market_D.values(), market_D.keys()))
var_D_inv = dict(zip(var_D.values(), var_D.keys()))
"""



"""
D=read_all()
D=read_all(path="/media/ranjan/DATAPART/agri_data/root_raw/Ajwan/")
find_unique(D)
save_data_district_marker(D,numpy_path="/media/ranjan/DATAPART/agri_data/root/Onion/"):
"""













