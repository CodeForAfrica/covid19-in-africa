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


def plot_africa_totals(data, colors=['blue', 'orangered', 'lawngreen']):
    """Create lineplots of coronavirus case totals in Africa.

    Parameters:
    ----------
    data: pd.DateFrame
        A dataframe of historic coronavirus cases in Africa.
    colors: str, valid matplotlib color input
        Colors to apply to the 'confirmed', 'deaths', and 'recovered'
        lineplots, respectively'.
    """
    # Convert Date column values to Timestamps
    data['Date'] = data['Date'].astype('datetime64')

    # Calculate totals for each day. After this, only the columns 'Confirmed'
    # 'Deaths' and 'Recovered' remain, with 'Date' becoming the index.
    data = data.groupby('Date').sum()

    latest_date = data.index.max().strftime('%h %d, %Y')  # used in title

    # Create a matplotlib Figure, with lineplots for 'confirmed', 'recovered',
    # and 'deaths'
    fig = Figure(figsize=(10, 5), dpi=200)
    fig.suptitle(f'Total Coronavirus Cases in Africa as at {latest_date}',
                 size=18)
    ax = fig.subplots()
    for idx, label in enumerate(['Confirmed', 'Deaths', 'Recovered']):
        ax.plot(data[label].index, data[label], lw=2, color=colors[idx],
                label=label)

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

    # Set the x-axis to show dates in 2-week intervals
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%h %d'))  # e.g. Jan 20

    fig.legend(loc='right')
    fig.savefig('images/africa_totals.png', bbox_inches='tight',
                transparent=True)


def plot_daily_confirmed(daily_data):
    """Create a bar plot of a day's confirmed cases.

    Parameters:
    ----------
    daily_data: pd.DataFrame
        A dataframe of daily coronavirus cases, with columns for 'Date',
        'Country/Region', and 'Confirmed'.
    """
    latest_date = daily_data['Date'].astype('datetime64').max()\
                                    .strftime('%h %d, %Y')

    # Get and sort confirmed cases in ascending order
    data = daily_data.set_index('Country/Region')['Confirmed'].sort_values()

    # Create a horizontal barplot with country-confirmed-cases as bars
    fig = Figure(figsize=(6, 12))
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
    """Create a bubble map of coronavirus cases in Africa.

    Parameters:
    ----------
    geodata: pd.DataFrame
        A DataFrame with columns 'Lat' and 'Long', of latitude and longitude
        values respectively, with corresponding 'Confirmed` case data.
    """
    fig = px.scatter_geo(
        geo_data, lat='Lat', lon='Long', scope='africa', size='Confirmed',
        color='Confirmed', height=600, width=600,
        color_continuous_scale=['cyan', 'yellow', 'orangered'],
        title='Geographic Scatter-plot of Confirmed Cases'
    )
    # Save geographical scatter-plot as png image file
    with open('images/geo_scatter.png', 'wb') as pic:
        pic.write(fig.to_image(format='png', scale=2))
