# covid19-in-africa

`covid19-in-africa` is a dataset repository for COVID-19 cases in Africa. We Load data from Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE) GitHub.



[![If you would like to help or track the progress of this project](https://img.shields.io/badge/Roadmap-data--pipeline-blueviolet)](https://github.com/orgs/covid19-in-africa/projects/1)

## Changelog

**Changes**:
TODO

Full changelog: [`CHANGELOG.md`](CHANGELOG.md) - TODO

## Update Status

**Commit Status**:
TODO
<Add status bar >

**Workflow status by countries**:

| Country | Status | Data Source |
| ------------- | ------------- | --- |

TODO


## Dataset

### Tabular Data

The **tabular data** files are located in `dataset` folder. The folder `dataset/daily` holds the daily updates in each country.

> The metadata for the tabular data is found in `.dataherb/metadata.yml`.

<!-- ### Other Data

Some of the countries publish more than simple tabular data. We cache the files in `documents` folder. -->

### Scrapers

The scripts that are being used to update the data are located in `scripts` folder. Most of the scripts require the `utils.py` module to run. Create a new environment and run `pip install -r requirements.txt` to install the requirements.

### Workflows

TODO
<!-- The workflows that update the dataset are defined in `.github/workflows`. The python scripts are scheduled to run on GitHub Actions. -->

## Notes
TODO

## Community
TODO
**Bugs and requests**: PRs are welcome.
