# Changelog

## 2020-12-03

- Move up daily the update schedule to 6:30 UTC.
- Update dependencies for scripts.

## 2020-12-02

- Add a basic, web-based dashboard.

## 2020-11-29

- Add a pair of barplots for incidence-rate and case-fatality-ratio.
- Add active cases, incidence-rate and case-fatality-ratio to daily reports.

## 2020-11-23

- Set `python3.8` in the GitHub workflow. It is stable, and more current than `python3.7`.
- Update the workflow schedule so that it runs only once a day. The geo-scatterplot image is always unique with each script run, thus triggering 2 commits a day with the twice-a-day schedule. Since the data source is currently updated once a day by 05:15 GMT, the current update time of 8:45 UTC(~GMT) is just fine.

## 2020-11-21 - 2020-11-22

### Added

- Line-plots of coronavirus case totals.
- Bar-plots of coronavirus confirmed case totals by country.
- Geographical scatterplot of confirmed coronavirus cases in Africa.
