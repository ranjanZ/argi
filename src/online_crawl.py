from lxml.html import parse
from lxml import etree
import re
import os
from io import StringIO, BytesIO
import numpy as np 
import requests
from lxml import html
import json
import datetime





def state_wise_rain(http_path):
    page = requests.get(http_path)
    html_content = html.fromstring(page.content)

    script=html_content.xpath("//body/script")[-1]
    t=script.text_content()

    t=t.split(";")[7]
    t=t.replace("\n","").replace("\r","")
    #t=t.replace("<\\/br>","-1,")
    t=t.replace("<\\/br>",",")
    t=re.sub(r"\s+", " ", t)

    t=t.split("areas\": [")[-1]
    t=t.split("]")[0]
    t="{\"areas\":["+t+"]}"
    D=json.loads(t)
    
    L=[]
    for idx in range(len(D['areas'])):
        id1=int(D['areas'][idx]['id'])
        title=D['areas'][idx]['title']
        d=D['areas'][idx]['balloonText']
        d=d.split(",")
        ar=float(d[2].split(":")[1].replace("mm",""))
        nr=float(d[3].split(":")[1].replace("mm",""))
        l=[id1,title,ar,nr]
        L.append(l)
    L=np.array(L)
    return(L)






def dist_wise_rain(http_path):
    page = requests.get(http_path)
    html_content = html.fromstring(page.content)

    script=html_content.xpath("//body//script")[-1]
    t=script.text_content()

    t=t.split(";")[7]
    t=t.replace("\n","").replace("\r","")
    #t=t.replace("<\\/br>","-1,")
    t=t.replace("<\\/br>",",")
    t=re.sub(r"\s+", " ", t)

    t=t.split("areas\": [")[-1]
    t=t.split("]")[0]
    t="{\"areas\":["+t+"]}"
    D=json.loads(t)

    L=[]
    for idx in range(len(D['areas'])):
        id1=int(D['areas'][idx]['id'])
        title=D['areas'][idx]['title']
        d=D['areas'][idx]['balloonText']
        d=d.split(",")
        ar=float(d[2].split(":")[1].replace("mm",""))
        nr=float(d[3].split(":")[1].replace("mm",""))
        l=[id1,title,ar,nr]
        L.append(l)
    L=np.array(L)
    return(L)


"""
http_path_state_M="https://mausam.imd.gov.in/imd_latest/contents/index_rainfall_subdiv.php?msg=M"
http_path_state_D="https://mausam.imd.gov.in/imd_latest/contents/index_rainfall_subdiv.php?msg=D"

http_path_dist_D="https://mausam.imd.gov.in/imd_latest/contents/rainfallinformation.php?msg=D"
http_path_dist_M="https://mausam.imd.gov.in/imd_latest/contents/rainfallinformation.php?msg=M"




DS_D=state_wise_rain(http_path_state_D)
DS_M=state_wise_rain(http_path_state_M)

DD_D=dist_wise_rain(http_path_dist_D)
DD_M=dist_wise_rain(http_path_dist_M)


t=DD[DD[:,1].argsort()]
t1=datetime.datetime.now()

file_name="data/"+str(t1.year)+"_"+str(t1.month)+"_"+str(t1.day) +".npz"
np.savez(file_name,rain_state=DS,rain_dist=DD)
D=np.load("./data/"+str(t1.year)+"_"+str(t1.month)+"_"+str(t1.day-4) +".npz")
DD0=D['rain_dist']
DS0=D['rain_state']


################POST REQUEST DATA
import requests 


for d in DD:
    data = {'raw_data':d}
    r = requests.post(url ="http://0.0.0.0:8000/ai/test/", data =data)
    print(r)






"""



