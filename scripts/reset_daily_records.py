from datetime import datetime
import os
import pandas as pd
import subprocess


population_estimates = pd.read_csv('./datasets/population_estimates.csv',
                                   index_col=0)
time_series_archive = pd.read_csv('./datasets/africa_time_series.csv',
                                  parse_dates=['Date'])


def update_daily_datasets():
    """Save fresh copies of the daily datasets from the time series data, so
    that any upstream(source) updates can be effected."""
    # Create a directory for each year
    for year in range(2020, datetime.today().year + 1):
        os.makedirs(f'datasets/daily/{year}', exist_ok=True)

    # Recreate and save data for each day from the time series data
    for date, data in time_series_archive.groupby('Date'):
        data.set_index('Country/Region', inplace=True)

        # Compute active cases
        data['Active'] = data['Confirmed'] - data['Recovered'] - data['Deaths']

        # Compute incidence rate (cases per 100,000 persons)
        # Note that the population values are given in thousands
        data['Incidence Rate'] = \
            data['Confirmed'] / population_estimates['2020_estimates'] * 100

        # Compute case-fatality ratio as a percentage
        data['Case - Fatality Ratio'] = \
            data['Deaths'] / data['Confirmed'] * 100

        # Restore countries' column
        data.reset_index(inplace=True)

        # Save updated dataset
        filename = f"{date.strftime('%m-%d-%Y')}.csv"
        data.sort_values(by='Confirmed', ascending=False, inplace=True)
        data.to_csv(f"datasets/daily/{date.year}/{filename}", index=False)

    # Get the number of files changed, by counting the lines in `git status`
    # short-format output, where number of lines = number of files changed.
    # Effectively run `git status -s | wc -l` from within this script.
    with subprocess.Popen(['git', 'status', '-s'],
                          stdout=subprocess.PIPE) as pipe:
        files_changed = subprocess.run(
            ['wc', '-l'], stdin=pipe.stdout, text=True, capture_output=True
        ).stdout.strip('\n')
        print(f'{files_changed} files have been updated.')


if __name__ == '__main__':
    data = update_daily_datasets()
