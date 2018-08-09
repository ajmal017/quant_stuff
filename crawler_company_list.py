import urllib.request, urllib.parse,http.client
from bs4 import BeautifulSoup
import sys,os,csv
import pandas as pd
import numpy as np
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
headers = {'User-Agent':user_agent,}

def getMarket(market):
  mylist = []
  try:
    url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=" + market + "&render=download"
    #req = urllib.request.Request(url,None,headers)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
      the_page = response.read().decode('utf-8')
      wrapper = csv.reader(the_page.strip().split('\n'))
      count = 0
      for record in wrapper:
        if count ==0:
          count += 1
          pass
        else:
          mylist.append(record)
  except (urllib.error.URLError,urllib.error.HTTPError,urllib.error.ContentTooShortError,http.client.HTTPException) as e:
    count =0
  return mylist


for market in ['NASDAQ','NYSE','AMEX']:
  print("getting company_list from " + market + " Stock Exchange")
  market_list= getMarket(market)
  if not os.path.exists(market):
    os.makedirs(market)
  with open(market + "marketlist.csv","w") as output:
    writer = csv.writer(output,lineterminator='\n')
    writer.writerows(market_list)
  list_data = list(map(list, zip(*market_list)))
  data_frame_dict = {'Symbol':list_data[0],'MarketCap':list(np.float_(list_data[3]))}
  df = pd.DataFrame(data_frame_dict, columns = ['Symbol', 'MarketCap'])
  df_select= df[df['MarketCap']>50.0e+9]
  print("Number of Companies with MarketCap exceeds 100.0e+9: " + str(df_select['MarketCap'].count() ))
  df_select.to_csv(market + "marketlist_select2.csv",sep=',',encoding='utf-8')


 
