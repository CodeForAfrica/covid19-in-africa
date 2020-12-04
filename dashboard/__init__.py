import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


data = pd.read_csv('dashboard/data.csv', parse_dates=['Date'])
latest_date = data['Date'].dt.strftime('%b %d, %Y')[0]

# Initialize Dash app
app = Dash(__name__,
           title="Covid19 in Africa",
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}])

server = app.server  # gunicorn access-point

app.layout = html.Div(className='content', children=[
    # Side pane in widescreen, top block in mobile
    html.Div(className='side-pane', children=[
        # Introduction
        html.H1('COVID-19 IN AFRICA'),
        dcc.Markdown(f"""
        This simple dashboard tracks Coronavirus cases in Africa. It uses the
        [JHU CSSE COVID-19 Data](https://github.com/CSSEGISandData/COVID-19),
        which is updated daily by 05:15 UTC with values for the past day.

        Resource Date: {latest_date}
        """),

        # Totals spotlight box
        html.Div(className='total', id='total'),

        # Dropdown menu
        html.P('Select:'),
        dcc.Dropdown(
            id='metric',
            options=[
                {'label': 'Confirmed Cases', 'value': 'Confirmed'},
                {'label': 'Active Cases', 'value': 'Active'},
                {'label': 'Recovered', 'value': 'Recovered'},
                {'label': 'Deaths', 'value': 'Deaths'},
                {'label': 'Incidence Rate', 'value': 'Incident_Rate'},
                {'label': 'Case - Fatality Ratio',
                 'value': 'Case_Fatality_Ratio'}
            ],
            style={'color': 'white'},
            value='Confirmed'
        ),
        html.Table(id='value-table', className='value-table'),
    ]),


    # Geographical scatterplot (Bubble-map)
    html.Div([
        dcc.Graph(id='map', config={"scrollZoom": False})]),

])


@app.callback(Output('map', 'figure'), [Input('metric', 'value')])
def draw_geo_scatter(metric):
    """Create a geo-scatterplot of Africa for the given metric.

    Parameters
    ----------
    metric: str
        One of 'Confirmed', 'Deaths', 'Recovered', 'Active', 'Incident_Rate',
        or 'Case_Fatality_Ratio'.

    Returns
    -------
    A plotly Figure.
    """
    fig = px.scatter_geo(data, lat='Lat', lon='Long', color=metric,
                         size=metric, scope='africa', height=700, width=700,
                         template='plotly_dark', size_max=50,
                         hover_name='Country/Region',
                         color_continuous_scale=['cyan', 'orangered'])
    fig.update_layout(paper_bgcolor='#444')
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    fig.update_geos(bgcolor='#444', countrycolor='lawngreen', landcolor='#444')
    return fig


@app.callback(Output('total', 'children'), [Input('metric', 'value')])
def display_totals(metric):
    """Dynamically style and display the details of the current metric in the
    highlighed box.

    Parameters
    ----------
    metric: str
        One of 'Confirmed', 'Deaths', 'Recovered', 'Active', 'Incident_Rate',
        or 'Case_Fatality_Ratio'.

    Returns
    -------
    HTML spans with the customised text.
    """
    color = 'orangered'
    headline = f"Total {metric.title()} Cases:"
    value = f"{data[metric].sum():,}"

    if metric == 'Incident_Rate':
        value = f"{data[metric].max():,.2f}"
        headline = "Maximum Incidence Rate (cases per 100,000 persons):"

    if metric == 'Case_Fatality_Ratio':
        value = f"{data[metric].max():,.2f}"
        headline = 'Maximum Case - Fatality Ratio:'

    if metric == 'Deaths':
        headline = f"Total {metric.title()}:"

    if metric == 'Recovered':
        color = 'cyan'

    return [html.Span(headline), html.Br(),
            html.Span(value, id='total-value', style={'color': color})]


@app.callback(Output('value-table', 'children'), [Input('metric', 'value')])
def draw_table(metric):
    """Create a table of the values of metric in each country.

    Parameters
    ----------
    metric: str
        One of 'Confirmed', 'Deaths', 'Recovered', 'Active', 'Incident_Rate',
        or 'Case_Fatality_Ratio'.

    Returns
    -------
    A HTML table.
    """
    X = data[['Country/Region', metric]].sort_values(by=metric,
                                                     ascending=False)
    color = 'cyan' if metric == 'Recovered' else 'orangered'
    return [html.Tr([html.Td(country),
                     html.Td(f'{round(value, 4):,}', style={'color': color})])
            for country, value in X.values]


if __name__ == '__main__':
    app.run_server(debug=True)
