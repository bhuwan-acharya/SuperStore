from dash import html,dcc, Input, Output
import dash_bootstrap_components as dbc
from data import df
import pandas as pd
from components.dateBar import create_datebar

country = df['Country/Region'].unique()

# Preprocess the DataFrame to create mappings
country_to_states = df.groupby('Country/Region')['State/Province'].unique().to_dict()
state_to_cities = df.groupby('State/Province')['City'].unique().to_dict()

content = html.Div([
    html.Div([
        create_datebar(),
        dbc.Row([
            dbc.Col([
                   # Country State and City Dropdown
                html.Div([
                    html.Label('Country'),
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': i, 'value': i} for i in country],
                        value=['United States'],  # Default value
                        multi=True
                    )
                ]),
            ]),
            dbc.Col([
                        html.Div([
                        html.Label('State'),
                        dcc.Dropdown(
                            id='state-dropdown',
                            options=[],
                            value=[],
                            multi=True
                        )
                    ]),
            ]),
            dbc.Col([
                    html.Div([
                    html.Label('City'),
                    dcc.Dropdown(
                        id='city-dropdown',
                        options=[],
                        value=[],
                        multi=True
                    )
                ]),
            ]),
        ], class_name="country-input-row"),
        ]),
    html.Hr(),
    ])

def create_content():
    return content

def content_callbacks(app):
    @app.callback(
    Output('date-alert', 'children'),
    [
    Input('start-date-picker', 'date'),
    Input('end-date-picker', 'date'),
    ],
    )
    def update_datebar_validation(start_date, end_date):
        if (start_date is None or end_date is None):
            return ''
    
        try:
            start_date_dt = pd.to_datetime(start_date)
            end_date_dt = pd.to_datetime(end_date)
            if start_date_dt > end_date_dt:
                return dbc.Alert("Start date must be before end date.", duration=4000, color='danger') 
        except ValueError:
            return dbc.Alert("Invalid date format. Please enter valid dates.", duration=4000, color='danger')

    # Callbacks to update the dropdowns
    @app.callback(
        Output('state-dropdown', 'options'),
        Input('country-dropdown', 'value')
    )
    def set_states_options(selected_countries):
        if selected_countries:
            states_options = {state for selected_country in selected_countries for state in country_to_states.get(selected_country, [])}
            return [{'label': state, 'value': state} for state in sorted(states_options)]
        return []
    # Setting the default value of state based on the country selected
    @app.callback(
        Output('state-dropdown', 'value'),
        Input('state-dropdown', 'options')
    )
    def set_states_default(options):
        if options:
            return [options[0]['value']]
        return []

    #options fot the city dropdown based on the state selected
    @app.callback(
        Output('city-dropdown', 'options'),
        Input('state-dropdown', 'value')
    )
    def set_cities_options(selected_states):
        if selected_states :
            cities = {city for selected_state in selected_states for city in state_to_cities.get(selected_state, [])}
            return [{'label': city, 'value': city} for city in sorted(cities)]
        return []

    # Setting the default value of city based on the state selected
    @app.callback(
        Output('city-dropdown', 'value'),
        Input('city-dropdown', 'options')
    )
    def set_cities_default(options):
        if options:
            return [options[0]['value']]
        return []