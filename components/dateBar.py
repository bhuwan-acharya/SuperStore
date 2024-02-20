from dash import html, dcc
import dash_bootstrap_components as dbc
from data import df

datebar=html.Div([
    dbc.Row([
        dbc.Col([
                # Start date picker
            html.Div([
                html.Label('START DATE'),
                dcc.DatePickerSingle(
                    id='start-date-picker',
                    date=df['Order Date'].min()  
                    )
                ], className="date-input"),
        ]),
        dbc.Col([
                # End date picker
            html.Div([
                html.Label('END DATE'),
                dcc.DatePickerSingle(
                    id='end-date-picker',
                    date=df['Order Date'].max()  
                )
            ], className="date-input"),
        ]),
        dbc.Col([
            html.Div([
                html.Label('DATE GRANULARITY'),
                dcc.Dropdown(
                    id='date-granularity-dropdown',
                    options=[
                        {'label': 'Weekly', 'value': 'Week'},
                        {'label': 'Monthly', 'value': 'Month'},
                        {'label': 'Quarterly', 'value': 'Quarter'},
                        {'label': 'Yearly', 'value': 'Year'},
                    ],
                    value='Month'  
                )
            ], className="date-input"),
        ]),
    ], className="date-input-row"),
    html.Div(
         id="date-alert",
    ),
])

def create_datebar():
    return datebar