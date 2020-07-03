# -*- coding: utf-8 -*-

import requests
import pandas as pd
import os

from utils import Africa




class Case:
    
    def __init__(self,url):
        self.url = url
        
    def collect_case(self):
        """Load csv
        Arg:
        url : link to source file 

        Returns:
        global_cases : Dataframe with global cases.
        """
        global_cases = pd.read_csv(self.url)

        return global_cases
    
    def transform(self):
        """Reshape and sort with most recent first.
        Arg:
        global_cases : Dataframe with all global / international cases

        Return:
        africa_cases : tranformed Dataframe with most recent case on first row
        """
        select_columns = ['Province/State','Lat','Long']
        # df = global_cases.copy()
        global_cases = self.collect_case()
        df = global_cases.copy()
        df.drop(select_columns,axis=1, inplace=True)
        df = df[df['Country/Region'].apply(lambda x: x in Africa)].T.reset_index()
        df.columns = df.iloc[0]
        df.rename(columns={'Country/Region':'Date'},inplace=True)
        df.drop([0],axis=0,inplace=True)
        
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%m-%d-%Y')
        # sort to have the latest update on top row
        df.sort_values('Date',ascending=False, inplace=True)
        african_cases = df.copy()

        return african_cases
    
    def daily(self):
        """Extract most recent case and transform
        Returns:
        daily_case : Dataframe with country / <date>-case columns
        """
        african_cases = self.transform()
        df = african_cases.copy()
        df_latest = df.iloc[0].reset_index()
        df_latest.columns = df_latest.iloc[0]
        df_latest.drop([0],axis=0,inplace=True)
        df_latest.rename(columns={'Date':'Country'},inplace=True)
        daily_case = df_latest.copy()
        return daily_case
        
        
        

    
    
    
confirmed = Case("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
)
deaths = Case("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
)
recovered = Case("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
)
    
    
    


# print(deaths.collect_case())
# print(Case.collect_case(deaths))

print(recovered.daily())


