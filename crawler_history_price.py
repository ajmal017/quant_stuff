import sys,os,csv
import pandas as pd
import numpy as np
import quandl
from quandl.errors.quandl_error import NotFoundError

quandl.ApiConfig.api_key='a_H4H4Fzdt1suKJSY1Tf'

# read the selected stocks
company_list=[]
for market in ['NASDAQ','NYSE']:
  df = pd.read_csv(market+'marketlist_select.csv')
  print("sucessfully loaded company list from " + market)
  company_list = company_list + df['Symbol'].tolist()

# remove the redudant company
company_list = list(set(company_list))
print("sucessfully collect all companies, total number= " + \
        str(len(company_list)))

print("getting stock history price from quandl, database:WIKI")
start_date_ = str(sys.argv[1])
end_date_ = str(sys.argv[2])
print("history starts from " + start_date_)
print("history ends at " + end_date_)
stock_price_dir ='stock_price_history/' + start_date_ + '-' + end_date_
if not os.path.exists(stock_price_dir):
  os.makedirs(stock_price_dir)
for company in company_list:
  try:
    print("getting stock price of: " + company)
    price_data = quandl.get('WIKI/' + company,start_date=start_date_, end_date=end_date_)
    price_data.to_csv(stock_price_dir + '/' + company +'.csv',encoding='utf-8')
  except NotFoundError as e:
    print('error: {} '.format(str(e)))

print("Sucessfully downloaded stock history price from quandl, database:WIKI")


  


