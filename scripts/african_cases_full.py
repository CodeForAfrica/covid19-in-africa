import pandas as pd
from utils import Africa, plot_africa_totals

base_url = """https://raw.githubusercontent.com/CSSEGISandData/COVID-19/\
master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_"""
url_dict = {
    "Confirmed": f"{base_url}confirmed_global.csv",
    "Deaths": f"{base_url}deaths_global.csv",
    "Recovered": f"{base_url}recovered_global.csv"
}


def fetch_data(name, url):
    """Fetch data from the John Hopkins API

    Parameters:
    name: str
        A label, one of 'Confirmed', 'Recovered' or 'Deaths' as per url
    url : str
        A link to a data set

    Returns:
    A DataFrame of the data in the supplied url
    """
    unwanted_cols = ['Province/State', 'Lat', 'Long']
    df = pd.read_csv(url).drop(unwanted_cols, axis=1)
    africa_df = df[df['Country/Region'].isin(Africa)]
    africa_df = africa_df.set_index('Country/Region').unstack()
    return africa_df.rename(name)


def compile_africa_data(url_dict):
    """Get and save the combined historic and daily Africa data

    Parameters:
    ----------
    url_dict: dict
        A dictionary of 'name': 'url' pairs
    """
    data_list = [fetch_data(name, url) for name, url in url_dict.items()]

    combined = pd.concat(data_list, axis=1).reset_index()

    africa_historic = pd.DataFrame({
        'Country/Region': combined['Country/Region'],
        'Date': pd.to_datetime(combined['level_0']).dt.strftime('%m-%d-%Y'),
        'Confirmed': combined['Confirmed'],
        'Deaths': combined['Deaths'],
        'Recovered': combined['Recovered']
    })
    africa_historic.to_csv('./datasets/africa_historic_data.csv', index=False)

    dates = africa_historic['Date']
    africa_daily = africa_historic[dates == dates.max()]
    filename = f'./datasets/daily/{dates.max()}_c19_african_cases.csv'
    africa_daily.to_csv(filename, index=False)

    plot_africa_totals(africa_historic)


if __name__ == "__main__":
    compile_africa_data(url_dict)
