# -*- coding: utf-8 -*-
# from google.colab import drive
# drive.mount('/content/drive')

import requests
import pandas as pd
import os
import re
from lxml import etree, html

# confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
# deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

Africa = ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde", "Central African Republic", "Chad",
"Comoros", "Democratic Republic of the Congo", "Republic of the Congo", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Ethiopia", "Gabon", 
"Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", 
"Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", 
"Somalia", "South Africa", "South Sudan", "Sudan", "Swaziland", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"]


def collect_case(url):
  """Load csv
  Arg:
  url : link to file 

  Returns:
  global_cases : Dataframe with global cases.
  """
  global_cases = pd.read_csv(url)

  return global_cases

def transform():
  """Reshape and sort with most recent first.
  Arg:
  global_cases : Dataframe with all global / international cases

  Return:
  africa_cases : tranformed Dataframe with most recent case on first row
  """
  select_columns = ['Province/State','Lat','Long']
  global_cases = collect_case(url)
  df = global_cases.copy()
  df.drop(select_columns,axis=1, inplace=True)
  df = df[df['Country/Region'].apply(lambda x: x in Africa)].T.reset_index()
  df.columns = df.iloc[0]
  df.rename(columns={'Country/Region':'Date'},inplace=True)
  df.drop([0],axis=0,inplace=True)
  df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%m-%d-%Y')
  # sort to have the latest update on top row
  african_cases = df.sort_values('Date',ascending=False, inplace=True)

  return african_cases

def daily(african_cases):
  """Extract most recent case and transform
  Returns:
  daily_case : Dataframe with country / <date>-case columns
  """
  african_cases = transform()
  df = african_cases.copy()
  df_latest = df.iloc[0].reset_index()
  df_latest.columns = df_latest.iloc[0]
  df_latest.drop([0],axis=0,inplace=True)
  df_latest.rename(columns={'Date':'Country',df_latest.columns[1] : str(df_latest.columns[1])+'Recovered'},inplace=True)
  # daily csv
  filename = df_latest.columns[1] + '-recovered.csv'
  
  df_latest.to_csv('./datasets/'+filename)
  
  
def download_daily_case():
  """Collect, tranfrom and download to datasets folder
  """
  global_cases = collect_case(url)
  african_cases = transform()
  day_report = daily(african_cases)
  
  return day_report


  

  
  
if __name__ == "__main__":
  
  url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
  download_daily_case()
  
    
  


