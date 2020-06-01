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



http_path="https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=166&Tx_State=0&Tx_District=0&Tx_Market=0&DateFrom=29-May-2020&DateTo=29-May-2020&Fr_Date=29-May-2020&To_Date=29-May-2020&Tx_Trend=0&Tx_CommodityHead=Alsandikai&Tx_StateHead=--Select--&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--"




page = requests.get(http_path)
html_content = html.fromstring(page.content)



