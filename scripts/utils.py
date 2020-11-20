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


def plot_africa_totals(data, colors=['blue', 'orangered', 'lawngreen']):
    data['Date'] = data['Date'].astype('datetime64')
    data = data.groupby('Date').sum()
    latest = data.index.max().strftime('%d %h, %Y')

    fig = Figure(figsize=(10, 5), dpi=200)
    fig.suptitle(f'Total Coronavirus Cases in Africa as at {latest}', size=17)
    ax = fig.subplots()

    for idx, col in enumerate(data.columns):
        column = data[col]
        ax.plot(column.index, column, lw=2, color=colors[idx], label=col)

    ax.tick_params(axis='x', rotation=60)
    ax.yaxis.grid()  # horizontal gridlines
    ax.ticklabel_format(axis='y', style='plain')
    ax.set_ylabel('Total Cases')
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%h %d'))

    # remove bordering box
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    fig.legend(loc='right')
    fig.savefig('datasets/africa_totals.png')
