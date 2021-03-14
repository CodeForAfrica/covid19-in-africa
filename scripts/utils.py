from matplotlib.figure import Figure
import matplotlib.dates as mdates
import plotly.express as px

Africa = [
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi",
    "Cameroon", "Cabo Verde", "Central African Republic", "Chad", "Comoros",
    "Congo (Brazzaville)", "Congo (Kinshasa)", "Cote d'Ivoire",
    "Democratic Republic of the Congo", "Republic of the Congo", "Djibouti",
    "Egypt", "Equatorial Guinea", "Eritrea", "Ethiopia",  "Eswatini", "Gabon",
    "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya",
    "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali",
    "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger",
    "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles",
    "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan",
    "Swaziland", "Tanzania", "Togo", "Tunisia", "Uganda", "Western Sahara",
    "Zambia", "Zimbabwe"]


def despine(ax, sides=['left', 'right', 'top', 'bottom']):
    """Remove the bordering box (spines) from Matplotlib axes."""

    [ax.spines[side].set_visible(False) for side in sides]


def plot_africa_totals(data,
                       colors=dict(Confirmed='blue', Deaths='orangered',
                                   Recovered='lawngreen', Active='grey')):
    """Create lineplots of coronavirus case totals in Africa.

    Parameters:
    ----------
    data: pd.DateFrame
        A dataframe of cummulative totals of coronavirus case data in Africa,
        indexed by date.
    colors: dict, valid matplotlib color input
        Colors to apply to the 'confirmed', 'deaths', 'recovered' and 'active'
        lineplots, respectively'.
    """
    latest_date = data.index[-1].strftime('%b %d, %Y')  # used in title

    data['Active'] = data['Confirmed'] - data['Deaths'] - data['Recovered']
    # Create a matplotlib Figure, with lineplots for 'confirmed', 'recovered',
    # and 'deaths'
    fig = Figure(figsize=(10, 5), dpi=180)
    fig.suptitle(f'Total Coronavirus Cases in Africa as at {latest_date}',
                 size=18)
    ax = fig.subplots()
    for label in data.columns:
        ax.plot(data[label], lw=2, color=colors[label], label=label)

    # Annotate lineplots with current totals
    for line in ax.lines:
        x_coord, y_coord = line.get_xydata()[-1]  # position of latest totals
        ax.annotate(f'{line.get_ydata().max():,}',  # latest total
                    xy=(x_coord+4, y_coord), style='oblique')

    ax.tick_params(axis='x', rotation=60)  # rotate x-axis ticks (dates) by 60°
    ax.yaxis.grid()  # draw horizontal gridlines
    ax.set_ylabel('Total Cases', size=14)
    despine(ax)  # remove bordering box

    # Show y-axis ticks as full plain text, instead of in scientific notation
    ax.ticklabel_format(axis='y', style='plain')
    ax.yaxis.set_major_formatter(lambda x, p: f'{x:,.0f}')  # comma separation

    # Set the x-axis to show dates in 2-week intervals
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  # e.g. Jan 20

    fig.legend(loc='right')
    fig.savefig('images/africa_totals.png', bbox_inches='tight',
                transparent=True)


def plot_daily_confirmed(daily_data):
    """Create a bar plot of a day's confirmed cases.

    Parameters:
    ----------
    daily_data: pd.DataFrame
        A dataframe of daily coronavirus case data, with columns for 'Date',
        'Country/Region', and 'Confirmed'.
    """
    latest_date = daily_data['Date'].astype('datetime64').max()\
                                    .strftime('%b %d, %Y')
    data = daily_data['Confirmed'].sort_values()

    # Create a horizontal barplot with a bar for each country
    fig = Figure(figsize=(6, 12), dpi=150)
    ax = fig.subplots()
    ax.set_title(f'Confirmed Coronavirus Cases by Country as at {latest_date}',
                 size=18)
    data.plot.barh(x='Country/Region', ax=ax, width=0.9, color='teal')

    # Annotate bars with country-confirmed-case tally
    for p in ax.patches:
        ax.annotate(f'{p.get_width():,}', style='oblique',
                    xy=(p.get_x()+p.get_width(), p.get_y()+.2))
    despine(ax)  # remove bordering box
    ax.tick_params(size=15)  # set fontsize for ticks (country names)
    ax.get_xaxis().set_visible(False)  # hide x-axis

    fig.savefig('images/africa_daily.png', transparent=True,
                bbox_inches='tight')


def plot_geoscatter(geo_data):
    """Create a bubble map of active coronavirus cases in Africa.

    Parameters:
    ----------
    geodata: pd.DataFrame
        A DataFrame with columns 'Lat' and 'Lon', of latitude and longitude
        values respectively, having 'Active' case data.
    """
    # On occassion, the Active cases column (= Confirmed - Recovered - Deaths)
    # has negative values due to error(s). Negative values in the `size`
    # arguement of `scatter_geo` raise a ValueError. The following ensures the
    # values are non-negative:
    geo_data['Active'] = geo_data['Active'].clip(lower=0)

    fig = px.scatter_geo(
        geo_data, lat='Lat', lon='Lon', scope='africa', size='Active',
        color='Active', height=600, width=600, size_max=50,
        color_continuous_scale=['cyan', 'yellow', 'orangered'],
        title='Geographic Scatter-plot of Active Coronavirus Cases'
    )
    # Save geographical scatter-plot as png image file
    with open('images/geo_scatter.png', 'wb') as pic:
        pic.write(fig.to_image(format='png', scale=2))


def plot_daily_stats(daily_stats):
    """Plot a pair of horizontal bar-plots for coronavirus incidence-rate &
    case-fatality-ratio in Africa.

    Parameters:
    ----------
    daily_stats: pd.DataFrame
        A DataFrame with the incidence-rate and case-fatality-ratio info,
        indexed by country.
    """
    fig = Figure(figsize=(12, 12), tight_layout=True)
    ax1, ax2 = fig.subplots(nrows=1, ncols=2)

    # Horizontal barplot of incidence rate
    daily_stats['Incidence Rate'].sort_values()\
                                 .plot.barh(ax=ax1, color='darkviolet')
    ax1.set_title('Incidence Rate (Cases Per 100,000 Persons)', size=16)
    ax1.set_ylabel('Country/Region')
    despine(ax1)  # remove bordering box
    ax1.get_xaxis().set_visible(False)  # hide x-axis

    # Horizontal barplot of case-fatality-ratio
    daily_stats['Case - Fatality Ratio'].sort_values()\
                                        .plot.barh(ax=ax2, color='dimgray')
    ax2.set_title(
        'Case-Fatality Ratio \n(№ Recorded Deaths / № Cases * 100%)',
        size=16)
    ax2.set_ylabel('Country/Region')
    despine(ax2)  # remove bordering box
    ax2.get_xaxis().set_visible(False)  # hide x-axis

    # Annotate the bars
    for p in ax1.patches:
        ax1.annotate(f'{p.get_width():,.2f}', (p.get_width(), p.get_y()))

    for p in ax2.patches:
        ax2.annotate(f'{p.get_width():.2f}%', (p.get_width(), p.get_y()))

    fig.savefig('images/stats.png', transparent=True)
