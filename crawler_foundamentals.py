import sys,os
sys.path.append('/home/tjz/twsapi_macunix/IBJts/IBJts/source/pythonclient')
import ibapi
from ib_insync import *
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import xml.etree.ElementTree as ET
import time
from datetime import datetime

ib = IB()
ib.connect('172.16.0.29', 4003, clientId=102)

df = pd.read_csv('NASDAQmarketlist_select.csv',sep=',',encoding='utf-8')
print("total number of stock contract: " + str(len(df))) 
dt = datetime.now()
date_str = str(dt.year) + "-" + str(dt.month) +"-"+ str(dt.day)
print("downloading foundamental reports on: " + date_str)

if not os.path.exists(date_str):
  os.makedirs(date_str)
  for market in ['NASDAQ','NYSE','AMEX']:
    data_dir= date_str+"/"+market
    os.makedirs(data_dir)
    df = pd.read_csv(market + 'marketlist_select.csv',sep=',',encoding='utf-8')
    for i in range(0,len(df)):
      contract_company= df.iloc[i]['Symbol']
      print("get contract info for " + contract_company)
      contract = Stock(contract_company, exchange='SMART', primaryExchange=market)
      report =ib.reqFundamentalData(contract, "ReportsFinStatements")
      print(contract)
      myfile = open(data_dir+"/"+contract_company+ ".xml", "w")  
      if type(report) == type('string'):
        myfile.write(report)  
  #ib.ContractDetails
