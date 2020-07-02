import requests
import pandas as pd
import os
import re
from lxml import etree, html

confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

Africa = ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde", "Central African Republic", "Chad",
"Comoros", "Democratic Republic of the Congo", "Republic of the Congo", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Ethiopia", "Gabon",
"Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania",
"Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone",
"Somalia", "South Africa", "South Sudan", "Sudan", "Swaziland", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"]

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
def africa_today():
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
    df_wide = df[df['Country/Region'].apply(lambda x: x in Africa)].melt(id_vars = ['Country/Region', 'source']).rename(columns = {"variable":"Date"})
    df_wide['Date'] = pd.to_datetime(df_wide['Date']).dt.strftime('%m-%d-%Y')
    df_max = df_wide[df_wide['Date'] == df_wide.Date.max()]
    african_cases = df_max.pivot_table(index = ['Country/Region', 'Date'], columns = 'source', values = 'value').reset_index()

    return african_cases

#TODO add storage path
def download_daily_case():
    """Collect, tranfrom and download to datasets folder
      """
    global_cases = collect_case(url_dict)
    african_daily = africa_today()
    return african_daily

  
if __name__ == "__main__":
    url_dict = {"Confirmed":confirmed_url, "Deaths": deaths_url, "Recovered":recovered_url}
    download_daily_case()
