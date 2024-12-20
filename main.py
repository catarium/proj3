from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
from app.services.accu_service import get_location_key, get_weather
import requests



data = {
        'city': [],
        'lat': [],
        'lon': [],
        'forecasts': []
        }

current_day = None
current_city = None

app = Dash()

app.layout = [
    html.H1(children='Прогноз погоды', style={'textAlign':'center', 'fontFamily': 'Lato'}),
    dcc.Input(id='city_input', debounce=True),
    html.Br(),
    html.Button('Очистить', id='clear_button'),
    dcc.Graph(id='map', figure=px.line_map(data, lon='lon', lat='lat')),
    html.Div(children='Выберите через сколько дней', style={'textAlign':'center', 'fontFamily': 'Lato'}),
    dcc.Dropdown(list(range(1, 6)), id='day_choice'),
    html.Div(children='Выберите город', style={'textAlign':'center', 'fontFamily': 'Lato'}),
    dcc.Dropdown(id='city_choice'),
    dash_table.DataTable(id='forecast_table')
]


@callback(
    [Output('map', 'figure', allow_duplicate=True), 
     Output('city_choice', 'options', allow_duplicate=True), 
     Output('forecast_table', 'data', allow_duplicate=True), 
     Output('forecast_table', 'columns', allow_duplicate=True)],
    [Input('clear_button', 'n_clicks')],
    prevent_initial_call='initial_duplicate'
)
def clear(n_clicks):
    global data, current_city, current_day
    data = {
            'city': [],
            'lat': [],
            'lon': [],
            'forecasts': []
            }
    current_day = None
    current_city = None
    return update_graph('') + show_forecast()

 

@callback(
    [Output('map', 'figure', allow_duplicate=True), Output('city_choice', 'options', allow_duplicate=True)],
    [Input('city_input', 'value')],
    prevent_initial_call='initial_duplicate'
)
def update_graph(value):
    global data
    res = get_location_key(value)
    if res:
        data['city'].append(value)
        location = res[0]['GeoPosition']
        data['lon'].append(location['Longitude'])
        data['lat'].append(location['Latitude'])
        forecasts = get_weather(res[0]['Key'])
        data['forecasts'].append(forecasts)
    return (px.line_map(data, lon='lon', lat='lat'), data['city'])


def show_forecast():
    res = [{}]
    columns = [{'id': 'temp', 'name': 'Температура'}, {'id': 'tempfeel', 'name': 'Чувствуется как'}, {'id': 'wind', 'name': 'Скорость ветра'}, {'id': 'precip', 'name': 'Осадки'}]
    if not current_day or not current_city:
        return res, columns
    print(len(data['forecasts'][0]))
    forecast = data['forecasts'][data['city'].index(current_city)]['DailyForecasts'][current_day - 1]
    res[0]['temp'] = ((forecast['Temperature']['Minimum']['Value'] + forecast['Temperature']['Minimum']['Value']) / 2)
    res[0]['tempfeel'] = ((forecast['RealFeelTemperature']['Minimum']['Value'] + forecast['RealFeelTemperature']['Minimum']['Value']) / 2)
    res[0]['wind'] = ((forecast['Day']['Wind']['Speed']['Value'] + forecast['Night']['Wind']['Speed']['Value']) / 2)
    res[0]['precip'] = (forecast['Day']['PrecipitationType'] if forecast['Day']['HasPrecipitation'] else 'нет')
    columns = [{'id': 'temp', 'name': 'Температура'}, {'id': 'tempfeel', 'name': 'Чувствуется как'}, {'id': 'wind', 'name': 'Скорость ветра'}, {'id': 'precip', 'name': 'Осадки'}]
    return (res, columns)


@callback(
    [Output('forecast_table', 'data', allow_duplicate=True), Output('forecast_table', 'columns', allow_duplicate=True)],
    [Input('day_choice', 'value')],
    prevent_initial_call='initial_duplicate'
)
def set_day(value):
    global current_day
    current_day = value
    return show_forecast()


@callback(
    [Output('forecast_table', 'data', allow_duplicate=True), Output('forecast_table', 'columns', allow_duplicate=True)],
    [Input('city_choice', 'value')],
    prevent_initial_call='initial_duplicate'
)
def set_city(value):
    global current_city
    current_city = value
    return show_forecast()


if __name__ == '__main__':
    app.run(debug=True)

