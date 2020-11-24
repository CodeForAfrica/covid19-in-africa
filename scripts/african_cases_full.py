import pandas as pd
import utils

base_url = """https://raw.githubusercontent.com/CSSEGISandData/COVID-19/\
master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_"""

url_dict = {
    "Confirmed": f"{base_url}confirmed_global.csv",
    "Deaths": f"{base_url}deaths_global.csv",
    "Recovered": f"{base_url}recovered_global.csv"
}


def fetch_data(label, url):
    """Fetch data from the John Hopkins API.

    Parameters:
    ----------
    label: str
        One of 'Confirmed', 'Recovered' or 'Deaths'.
    url : str
        A link to the data set.

    Returns:
    -------
    A Series of the data in the supplied url, indexed by date and country.
    """
    # Gather global data for the given label
    unwanted_cols = ['Province/State', 'Lat', 'Long']
    global_cases = pd.read_csv(url).drop(unwanted_cols, axis=1)

    # Select data for African countries
    africa_df = global_cases[global_cases['Country/Region'].isin(utils.Africa)]
    africa_df = africa_df.set_index('Country/Region')

    # Create a pivot table with date & country as a MultiIndex, and the data
    # as a series.
    data_series = africa_df.unstack()
    return data_series.rename(label)


def compile_africa_data(url_dict):
    """Get and save the historic and daily Africa coronavirus data, then plot
    basic visualisations.

    Parameters:
    ----------
    url_dict: dict
        A dictionary of 'label': 'url' pairs.
    """
    # Create a list of Series for confirmed, recovered and death cases
    cases_list = [fetch_data(label, url) for label, url in url_dict.items()]

    # Combine the data as a DataFrame. Reset the index so that country and
    # date are restored as columns.
    combined = pd.concat(cases_list, axis=1).reset_index()

    # Package the data as per the format in the archives, and save it.
    africa_historic = pd.DataFrame({
        'Country/Region': combined['Country/Region'],
        'Date': pd.to_datetime(combined['level_0']).dt.strftime('%m-%d-%Y'),
        'Confirmed': combined['Confirmed'],
        'Deaths': combined['Deaths'],
        'Recovered': combined['Recovered']
    })
    africa_historic.to_csv('./datasets/africa_historic_data.csv', index=False)

    # Extract data for the latest date.
    dates = africa_historic['Date']
    africa_daily = africa_historic[dates == dates.max()]

    # Sort in descending order of confirmed cases, and save.
    africa_daily = africa_daily.sort_values(by='Confirmed', ascending=False)
    filename = f'./datasets/daily/{dates.max()}_c19_african_cases.csv'
    africa_daily.to_csv(filename, index=False)

    # Fetch location data for use in geographical plots
    coordinates = pd.read_csv(url_dict['Confirmed'],
                              usecols=['Country/Region', 'Lat', 'Long'])
    geo_data = africa_daily.merge(coordinates, on='Country/Region')

    utils.plot_africa_totals(africa_historic)  # lineplots of total cases
    utils.plot_daily_confirmed(africa_daily)  # barplot of cases by country
    utils.plot_geoscatter(geo_data)  # bubble map of cases in Africa


if __name__ == "__main__":
    compile_africa_data(url_dict)
