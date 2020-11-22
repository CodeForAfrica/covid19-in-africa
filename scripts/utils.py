from matplotlib.figure import Figure
import matplotlib.dates as mdates

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
    """Removes the bordering box (spines) from Matplotlib axes."""

    [ax.spines[side].set_visible(False) for side in sides]


def plot_africa_totals(data, colors=['blue', 'orangered', 'lawngreen']):
    """Create a line plot of historical coronavirus case totals.

    Parameters:
    ----------
    data: pd.DateFrame
        A dataframe of historic coronavirus cases in Africa.
    colors: str, valid marplotlib color input
        Colors to apply to the 'confirmed', 'deaths', and 'recovered' lines
        respectively'."""

    data['Date'] = data['Date'].astype('datetime64')
    data = data.groupby('Date').sum()
    latest = data.index.max().strftime('%d %h, %Y')

    fig = Figure(figsize=(10, 5), dpi=200)
    fig.suptitle(f'Total Coronavirus Cases in Africa as at {latest}', size=18)
    ax = fig.subplots()
    # plot lines
    for idx, col in enumerate(data.columns):
        column = data[col]
        ax.plot(column.index, column, lw=2, color=colors[idx], label=col)

    # annotate line plots
    for ln in ax.lines:
        x_coord, y_coord = ln.get_xydata()[-1]
        ax.annotate(f'{ln.get_ydata().max():,}',
                    xy=(x_coord+4, y_coord), style='oblique')

    ax.tick_params(axis='x', rotation=60)
    ax.yaxis.grid()  # horizontal gridlines
    ax.ticklabel_format(axis='y', style='plain')
    ax.set_ylabel('Total Cases')
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%h %d'))
    despine(ax)
    fig.legend(loc='right')
    fig.savefig('datasets/africa_totals.png', bbox_inches='tight',
                transparent=True)


def plot_daily_confirmed(daily_data):
    """Create a bar plot of a day's confirmed cases.

    Parameters:
    ----------
    daily_data: pd.DataFrame
        A dataframe of daily coronavirus cases, with confirmed cases in
        descending order.
    """
    data = daily_data.set_index('Country/Region')['Confirmed'].sort_values()
    date = daily_data['Date'].astype('datetime64').max().strftime('%h %d, %Y')

    fig = Figure(figsize=(6, 12))
    ax = fig.subplots()

    data.plot.barh(x='Country/Region', ax=ax, width=0.9, color='teal')
    # annotate bars
    for p in ax.patches:
        ax.annotate(f'{p.get_width():,}', style='oblique',
                    xy=(p.get_x()+p.get_width(), p.get_y()+.2))
    despine(ax)
    ax.tick_params(size=15)
    ax.get_xaxis().set_visible(False)  # hide x-axis
    ax.set_title(f'Confirmed Coronavirus Cases by Country as at {date}',
                 size=18)
    fig.savefig('datasets/africa_daily.png', transparent=True,
                bbox_inches='tight')
