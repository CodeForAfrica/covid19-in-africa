import os
import pandas as pd
from scripts import utils

population = pd.read_csv('./datasets/population_estimates.csv', index_col=0)
location = pd.read_csv('./datasets/location_data.csv', index_col=0)

base_url = """https://raw.githubusercontent.com/CSSEGISandData/COVID-19/\
master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_"""

url_dict = {
    "Confirmed": f"{base_url}confirmed_global.csv",
    "Deaths": f"{base_url}deaths_global.csv",
    "Recovered": f"{base_url}recovered_global.csv"
}


def fetch_time_series_data(url_dict):
    """Collect coronavirus time series data for Africa from the JHU CSSE
    COVID-19 Data repository.

    Parameters:
    ----------
    url_dict: dict
        A dictionary of URLs with keys 'Confirmed', 'Deaths' and 'Recovered',
        and values - links to the respective time series files.

    Returns:
    -------
    A DataFrame with daily cummulative coronavirus data for each country in
    Africa.
    """
    case_time_series_list = []
    # Gather global data for the given label
    for label, url in url_dict.items():
        # Get global data for the given label
        unwanted_cols = ['Province/State', 'Lat', 'Long']
        global_cases = pd.read_csv(url).drop(unwanted_cols, axis=1)

        # Select data for Africa
        africa_cases = (global_cases[global_cases['Country/Region']
                        .isin(utils.Africa)])
        africa_cases.set_index('Country/Region', inplace=True)

        # Create a pivot table with date & country as a MultiIndex, and the
        # data as a series.
        data_series = africa_cases.unstack().rename(label)
        case_time_series_list.append(data_series)

    # Combine the data in a DataFrame. Reset the index to restore country and
    # date as columns.
    combined = pd.concat(case_time_series_list, axis=1).reset_index()

    # Re-order the columns. 'level_0' is actually 'Date', after index-reset.
    africa_time_series = (combined[['Country/Region', 'level_0', 'Confirmed',
                                    'Deaths', 'Recovered']]
                          .rename(columns={'level_0': 'Date'}))
    africa_time_series['Date'] = pd.to_datetime(africa_time_series['Date'])

    # Sort the time series data by Date (descending) and Country (ascending)
    africa_time_series.sort_values(by=['Date', 'Country/Region'],
                                   ascending=[False, True], inplace=True)

    # Save africa time series data
    africa_time_series.to_csv('./datasets/africa_time_series.csv', index=False)

    return africa_time_series.set_index('Country/Region')


def compile_daily_data():
    """Get coronavirus case data for the latest date.

    Returns:
    -------
    A tuple of DataFrames: time series data and data for the latest date.
    """
    # Extract data for the latest date.
    africa_time_series = fetch_time_series_data(url_dict)
    latest_date = africa_time_series['Date'].max()
    latest_days_data = \
        africa_time_series[africa_time_series['Date'] == latest_date]

    # Calculate and include active cases
    active_cases = (latest_days_data['Confirmed']
                    - latest_days_data['Recovered']
                    - latest_days_data['Deaths']).rename('Active')

    # Calculate new cases (change in values)
    previous_date = latest_date - pd.Timedelta('1D')
    previous_days_data = \
        africa_time_series[africa_time_series['Date'] == previous_date]
    case_cols = ['Confirmed', 'Deaths', 'Recovered']
    new_cases = latest_days_data[case_cols] - previous_days_data[case_cols]
    new_cases.columns = [f'{col} (New)' for col in case_cols]

    # Compute incidence rate (cases per 100,000 persons)
    # Note that the population values are given in thousands, so we multiply
    # the quotient by 100 instead of 100,000.
    incidence_rate = \
        ((latest_days_data['Confirmed'] / population['2020_estimates'] * 100)
         .rename('Incidence Rate'))

    # Compute case-fatality ratio as a percentage
    case_fatality_ratio = \
        ((latest_days_data['Deaths'] / latest_days_data['Confirmed'] * 100)
         .rename('Case - Fatality Ratio'))

    # Putting everything together
    africa_latest_day = pd.concat([latest_days_data, active_cases, new_cases,
                                   incidence_rate, case_fatality_ratio,
                                   location], axis=1)

    # Sort in descending order of confirmed cases
    africa_latest_day.sort_values(by='Confirmed', ascending=False,
                                  inplace=True)

    return africa_time_series, africa_latest_day


def gather_data_and_plot_results():
    """Collect the latest data and add it to the records."""
    africa_time_series, africa_latest_day = compile_daily_data()

    # Calculate and save cummulative totals
    cummulative_totals = africa_time_series.groupby('Date').sum()
    cummulative_totals.to_csv('./datasets/cummulative_totals.csv')

    # Plot the data
    utils.plot_africa_totals(cummulative_totals)    # a lineplot of totals
    utils.plot_daily_confirmed(africa_latest_day)  # barplot: cases by country
    utils.plot_geoscatter(africa_latest_day)  # bubble map of cases in Africa
    utils.plot_daily_stats(  # barplots of derived statistics
        africa_latest_day[['Incidence Rate', 'Case - Fatality Ratio']])

    # Add latest data to daily records
    latest_date = africa_latest_day['Date'].max()
    path = f'./datasets/daily/{latest_date.year}'

    if not os.path.isdir(path):  # if the folder doesn't yet exist,
        os.makedirs(path)        # create it

    filename = f"{path}/{latest_date.strftime('%m-%d-%Y')}.csv"

    # Name the index (County/Region), then restore it as a column
    africa_latest_day.rename_axis(index='Country/Region', inplace=True)
    africa_latest_day.reset_index(inplace=True)

    # Add daily data entry for latest date
    africa_latest_day[
        ['Country/Region', 'Date', 'Confirmed', 'Deaths', 'Recovered',
         'Active', 'Incidence Rate', 'Case - Fatality Ratio']
    ].to_csv(filename, index=False)

    # Save the whole daily dataset for the dashboard
    africa_latest_day.to_csv('./datasets/dashboard_data.csv', index=False)


if __name__ == "__main__":
    gather_data_and_plot_results()
