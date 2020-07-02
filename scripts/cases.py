# -*- coding: utf-8 -*-

import requests
import pandas as pd
import os
import re
from lxml import etree, html

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
    
confirmed = Case("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
)
deaths = Case("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
)
recovered = Case("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
)

# print(deaths.collect_case())
# print(Case.collect_case(deaths))

