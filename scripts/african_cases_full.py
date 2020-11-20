import requests
import pandas as pd
import os
import re
from lxml import etree, html

from utils import Africa, plot_africa_totals


confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

#url_dict = {"Confirmed":confirmed_url, "Deaths": deaths_url, "Recovered":recovered_url}
#Function to collect cases
def collect_case(links):
    """Load csv
    Arg:
    url : link to file
    Returns:
    list_cases : Dataframe with global cases.
    """
    global_case_list = []
    for key, url in links.items():
        cases = pd.read_csv(url).assign(source = key )
        global_case_list.append(cases)

        list_cases = pd.concat(global_case_list, ignore_index=True)
    return list_cases

#Function to return Africa's most recent cases
def africa_cases():
    """Return the most recent cases for African countries
    Arg:
    global_cases : Dataframe with all global / international cases
    Return:
    africa_cases : transformed dataset with today's African cases
    """
    select_columns = ['Province/State','Lat','Long']
    global_cases = collect_case(url_dict)
    df = global_cases.copy()
    df.drop(select_columns,axis=1, inplace=True)

    #transpose dataframe
    df_wide = df[df['Country/Region'].apply(lambda x: x in Africa)].melt(id_vars = ['Country/Region', 'source']).rename(columns = {"variable":"Date"})
    df_wide['Date'] = pd.to_datetime(df_wide['Date']).dt.strftime('%m-%d-%Y')
    africa_historic = df_wide.pivot_table(index = ['Country/Region', 'Date'], columns = 'source', values = 'value').reset_index().sort_values(['Date', 'Country/Region'], ascending = [False, True])
    plot_africa_totals(africa_historic)
    #extract most recent
    africa_today = africa_historic[africa_historic['Date'] == africa_historic.Date.max()].sort_values('Confirmed', ascending = False)

    return africa_today, africa_historic

#export
def download_daily_case():
    """Exports files to the datasets folder
    Returns:
      csv files in the datasets folder
    """
#     today's cases
#    Add_filename
    filename = str(africa_cases()[1].Date.max())+"_c19_african_cases.csv"
    africa_cases()[0].to_csv('./datasets/daily/'+filename, index = False)
#     historic cases
    africa_cases()[1].to_csv('./datasets/africa_historic_data.csv', index = False)



if __name__ == "__main__":
    url_dict = {"Confirmed":confirmed_url, "Deaths": deaths_url, "Recovered":recovered_url}
    download_daily_case()
