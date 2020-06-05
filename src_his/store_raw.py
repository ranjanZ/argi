"""
from unstructured all the  files save raw data according to item name 
"""




from all_index import *
from lxml import etree
import xlwt
import sys
import os
from shutil import copy
import pandas as pd
from dateutil import parser
from datetime import datetime
import numpy as np 





#get the Comodity name from the raw dumped data
def divide_by_com(dir_path="/media/ranjan/DATAPART/agri_data/raw_data/"):
    D={}
    for d in os.listdir(dir_path):
        file_path=dir_path+d
        f=open(file_path)
        t=f.readlines()
        t1=t[12]
        item_name=t1.split("_0\">")[1].split("</")[0]
        item_name=item_name.replace("/","-")
        if(item_name in D):
            D[item_name]=D[item_name]+[file_path]
        else:
            D[item_name]=[file_path]

        print(item_name)
    
    items=list(D.keys())
    return D,items





#store data to corresponding folder according to the item name  from dumped filene
def store_to_folder(D,root_dir="/media/ranjan/DATAPART/agri_data/root_raw/"):
    items=list(D.keys())
    for item in items:
        dir_path=root_dir+item+"/"
        try:
            os.mkdir(dir_path)
        except:
            pass

        for f in D[item]:
            copy(f,dir_path)        





D,items=divide_by_com()
store_to_folder(D,root_dir="/media/ranjan/DATAPART/agri_data/root_raw/")



















