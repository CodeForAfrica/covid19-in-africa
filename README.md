# covid19-in-africa

`covid19-in-africa` is a dataset repository for COVID-19 cases in Africa. We Load the data from the _Johns Hopkins University Center for Systems Science and Engineering_ (JHU CSSE) [CSSEGISandData /
COVID-19 GitHub repository](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data).

![africa totals](images/africa_totals.png)

![africa totals](images/africa_daily.png)

![africa totals](images/geo_scatter.png)
[![If you would like to help or track the progress of this project](https://img.shields.io/badge/Roadmap-data--pipeline-informational)](https://github.com/4bic/covid19-in-africa/projects/1)

## Changelog

**Changes**:

Full changelog: [`CHANGELOG.md`](CHANGELOG.md)

## Update Status

**Commit Status**:

![CI download historic Covid-19 Cases](https://github.com/CodeForAfrica/covid19-in-africa/workflows/CI%20download%20historic%20Covid-19%20Cases/badge.svg)

**Workflow status by countries**:

| Country | Status | Data Source |
| ------------- | ------------- | --- |

> TODO

## [Dataset](https://github.com/4bic/covid19-in-africa/tree/master/datasets)

### Tabular Data

The **tabular data** files are located in the `datasets` folder (_sample head as of Nov 24, 2020_). The folder `dataset/daily` holds the daily updates for each country.

<!-- > The metadata for the tabular data is found in `.dataherb/metadata.yml`. -->
Country/Region | Date       | Confirmed | Deaths | Recovered
-------------- | ---------- | --------- | ------ | ---------
Algeria        | 11-24-2020 | 77000     | 2309   | 50070
Angola         | 11-24-2020 | 14742     | 338    | 7444
Benin          | 11-24-2020 | 2916      | 43     | 2579
Botswana       | 11-24-2020 | 9992      | 31     | 7692
Burkina Faso   | 11-24-2020 | 2757      | 68     | 2557

<!-- ### Other Data

Some of the countries publish more than simple tabular data. We cache the files in `documents` folder. -->

## Scrapers

The scripts that are used to update the data are located in the `scripts` folder. Create a new environment and run:

    pip install -r scripts/requirements.txt
    python scripts/african_cases_full.py

to install the requirements, and save the latest available data.

## Workflows

The workflows that update the datasets are defined in `.github/workflows`. The python scripts are scheduled to run on GitHub Actions.

## Community

[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/CodeForAfrica/covid19-in-africa/issues)

**Bugs and requests**: PRs are welcome.

## License

The source code is licensed under the MIT license.
