from all_index import *

import  matplotlib.pyplot  as plt
from store_numpy import *
from statsmodels.tsa.ar_model import AR








#get mean and varience over different marketc in a district
def get_mean_var(PT):
    L=[]
    P=[]
    time=PT[0][1]
    for l in PT:
        price=l[0]
        tm=l[1]

        if(tm!=time):
            time=tm
            P=np.array(P)
            v=np.var(P)
            m=np.mean(P)
            L.append([m,v])
            P=[]
        P.append(price)
        
            

    L=np.array(L)
    return L

#remove repeated entry in the data. Data Shape (num_entry,5)
def remove_rep_entry(Data):
    Data=np.unique(Data,axis=0)
    return(Data)




#removie zero price or replace that with min max or mode
def remove_zero_price(Data):

    #remove all the data 
    Mask1=Data[:,1]!=0
    Mask2= Data[:,2]!=0
    Mask3= Data[:,3]!=0
    Mask=np.logical_or(Mask2,Mask1)
    Mask=np.logical_or(Mask,Mask3)
    Data=Data[Mask]
    S=np.array([Mask1[~Mask2],Mask2[~Mask2],Mask3[~Mask2]])
    S=S.astype("float64").sum(axis=0)

    t=Data[~Mask1]
    if(len(t)>0 and len(S)>0):
        t[:,1]=(Mask1[~Mask1]*Data[~Mask1][:,1]+Mask2[~Mask1]*Data[~Mask1][:,2]+Mask3[~Mask1]*Data[~Mask1][:,3])/S
        Data[~Mask1]=t

    t=Data[~Mask2]
    if(len(t)>0 and len(S)>0):
        t[:,2]=(Mask1[~Mask2]*Data[~Mask2][:,1]+Mask2[~Mask2]*Data[~Mask2][:,2]+Mask3[~Mask2]*Data[~Mask2][:,3])/S
        Data[~Mask2]=t

    t=Data[~Mask3]
    if(len(t)>0 and len(S)>0):
        t[:,3]=(Mask1[~Mask3]*Data[~Mask3][:,1]+Mask2[~Mask3]*Data[~Mask3][:,2]+Mask3[~Mask3]*Data[~Mask3][:,3])/S
        Data[~Mask3]=t

    return Data





#remove outliers if the data is out of the interval std and mean 

#intvl=time interval or buffer,  alpha=is the number of std we want to consider to determine threshold
def remove_outliers(Data,intvl=10,alpha=2):
      Data=Data[Data[:,-1].argsort()]    #sorting with respec to date
      Datap=Data[:,1:4]
      Count=np.zeros_like(Datap)
      ZM=np.zeros_like(Datap)
      ZS=np.zeros_like(Datap)
      for j in range(Datap.shape[0]-intvl+1):
          #z_score=np.abs(stats.zscore(Datap[j:j+intvl],axis=0))
          #z_score=np.nan_to_num(z_score,0)

          #Z[j:j+intvl]=z_scorec
          ZS[j:j+intvl]+=np.std(Datap[j:j+intvl],axis=0)    #incorporate date also later
          ZM[j:j+intvl]+=np.mean(Datap[j:j+intvl],axis=0)    #incorporate date also later
          Count[j:j+intvl]+=1

      ZM=ZM/Count
      ZS=ZS/Count

      THp=ZM+alpha*ZS
      THn=ZM-alpha*ZS
      Maskp=Datap<THp
      Maskn=Datap>THn
      Mask=np.logical_and(Maskp,Maskn)

      """
      #visulize the data and the threshold +/-
      plt.figure("data_min") 
      plt.plot(THn[:,0])
      #plt.figure("data")
      plt.plot(Datap[:,0])
      #plt.figure("Thp")
      plt.plot(THp[:,0])
      plt.figure("mask")
      plt.plot(Mask[:,0])



      plt.figure("data_max")
      plt.plot(THn[:,1])
      #plt.figure("data")
      plt.plot(Datap[:,1])
      #plt.figure("Thp")
      plt.plot(THp[:,1])
      """


    
      M=np.logical_and(Mask[:,0],Mask[:,1])
      M=np.logical_and(Mask[:,1],M)

      Data=Data[M]  #select those which are with in the threshold
      return(Data)



#merger different types of  quality goup by date and take mean 
#TODo: consider the varience before merge
def merge_diff_types(Data):
    L=[]
    for n in np.unique(Data[:,-1]):
        mask = Data[:,-1] == n
        if(np.sum(mask)>=2):
            print Data[mask]


        t=np.mean(Data[mask], axis = 0)
        L.append(t[:])
    
    L=np.array(L)
    return L





#fill missing Data from other market under same dist
def fill_missing_data(Data,base_market="Rampurhat",dist='Birbhum'):
    d=(datetime(2020, 1, 1)-datetime(2009, 1, 1)).days
    all_market_id=DM_pair[dist_D[dist]]
    base_market_id=market_D[base_market]


    plt.plot(Data[:,-1],Data[:,-2])
    
    Data_list=[]

    for mrkt in all_market_id:
        file_path=path+str(dist_D[dist])+"/"+str(int(mrkt))+".npy"
        M_data=np.load(file_path)

        M_data=basic_preporcess(M_data)
        #plt.plot(M_data[:,-1],M_data[:,-2])

        if(len(M_data)>0):
            idx=M_data[:,-1].astype("int32")        #dates
            temp=-np.ones((d,5))
            temp[idx]=M_data
            Data_list.append(temp)
                
    Data_list=np.array(Data_list)








#preprocess in basic way from the Data of shape(#num_sample,5)
def basic_preporcess(Data):
    Data=remove_rep_entry(Data)
    Data=remove_zero_price(Data)
    Data=remove_outliers(Data,intvl=10,alpha=2)
    Data=Data[Data[:,-1].argsort()]    #sorting with respec to date
    Data=merge_diff_types(Data)
    return(Data)







def read_data(path="/media/ranjan/DATAPART/agri_data/root/Onion/",dist='Birbhum',market="Rampurhat"):
    #file_path=path+str(dist_D[dist])+"/"+str(market_D[market])+".npy"
    file_path=path+str(dist_D[dist])+"/"+str(int((DM_pair[dist_D[dist]][0])))+".npy"
    Data=np.load(file_path)
    Data=remove_rep_entry(Data)
    Data=remove_zero_price(Data)
    Data=remove_outliers(Data,intvl=10,alpha=2)
    Data=Data[Data[:,-1].argsort()]    #sorting with respec to date
    Data=merge_diff_types(Data)
    unique_cat=np.unique(Data[:,0])
    print("# of catagory: ",len(unique_cat))
    plt.figure("mode1")
    for  cate in unique_cat:
        t=Data[Data[:,0]==cate]
        #plt.figure(cate)
        plt.plot(t[:,-1],t[:,-2],"o") 


    plt.figure("max1")
    for  cate in unique_cat:
        t=Data[Data[:,0]==cate]
        #plt.figure(cate)
        plt.plot(t[:,-1],t[:,-3],"o") 

    plt.figure("min1")
    for  cate in unique_cat:
        t=Data[Data[:,0]==cate]
        #plt.figure(cate)
        plt.plot(t[:,-1],t[:,-4],"o") 

def divide_train_test(Data,per=0.6):
    ln=Data.shape[0]
    idx=int(ln*per)
    train_data=Data[:idx]
    test_data=Data[idx:]

















def  f(): 
    # AR example
    from statsmodels.tsa.ar_model import AR
    from random import random
    # contrived dataset
    data = [x + random() for x in range(1, 100)]
    # fit model
    model = AR(data)
    model_fit = model.fit()
    # make prediction
    yhat = model_fit.predict(len(data), len(data))
    print(yhat)












"""
idx=np.cumsum(np.unique(PT[:, 1], return_counts=True)[1])[:-1]
A=np.split(PT[:,0],idx)
L=[]
for i in range(len(A)):
    l=A[i]
    mean=np.mean(l)
    var=np.std(l)
    L.append([])










numpy_file_path="/media/ranjan/DATAPART/agri_data/root/Onion/1.npy"


D=np.load(numpy_file_path)

#Sorted by date
D=D[D[:,-1].argsort()]
#mar_list_pdist=np.unique(D[D[:,0]==k][:,1])  #marketlist_per_dist
#m1=D[D[:,1]==mar_list_pdist[1]]



PT=D[:,-2:]
L=get_mean_var(PT)
plt.plot(L[:,0])

"""










