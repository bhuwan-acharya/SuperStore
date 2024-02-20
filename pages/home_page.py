import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from callbacks.salesChart import sales_callbacks  
from callbacks.profitChart import profit_callbacks  

dash.register_page(__name__, path='/', name='Home') # '/' is home page

layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5('Sales Overview'), className='text-center'),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(html.H3(id='total-sales-text', children='Total Sales: $0', className='text-center fw-bold')),
                        dbc.Col([
                            html.H5('Sales by Category', className='text-center fw-bold'),
                            html.Div([
                                 dcc.Graph(id='pie-chart', config={'displayModeBar': False}, className='pie-chart'),
                            ], className='pie-chart-container'),
                            ], className='pie-chart-col'
                            ),
                        dbc.Col([
                            dbc.Card([
                                html.P('Select graph type', className='text-center fw-bold p-1 mb-0'),
                                html.Hr(className='mt-0 mb-0'),
                                html.Div([
                                dcc.RadioItems(id='sales-radio', options=[{'label': 'Line', 'value': 'line'}, {'label': 'Bar', 'value': 'bar'}, {'label': 'Scatter', 'value': 'scatter'}], value='line')
                            ], className='d-flex justify-content-center p-1'),
                            ]),
                        ]
                        ),
                    ], className='d-flex justify-content-center flex-wrap align-items-center'),
                    dcc.Graph(id='sales-graph'),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col([
                            html.H5('Top 5 product with high sales', className='text-center fw-bold'),
                            dcc.Graph(id='top-sold-product',config={'displayModeBar': False}, ),
                            ], width=6),
                        dbc.Col(
                            [
                                html.H5('Top 5 product with least sales', className='text-center fw-bold'),
                                dcc.Graph(id='least-sold-product',config={'displayModeBar': False}, ),
                            ], width=6, className='border-start'),
                    ]),
                ]),
            ]),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5('Profit Overview'),className='text-center'),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(html.H3(id='total-profit-text', children='Total profit: $0', className='text-center fw-bold')),
                        dbc.Col([
                            html.H5('Profit by Category', className='text-center fw-bold'),
                            html.Div([
                                 dcc.Graph(id='profit-pie-chart', config={'displayModeBar': False}, className='pie-chart'),
                            ], className='pie-chart-container'),
                            ], className='pie-chart-col'
                            ),
                        dbc.Col([
                            dbc.Card([
                                html.P('Select graph type', className='text-center fw-bold p-1 mb-0'),
                                html.Hr(className='mt-0 mb-0'),
                                html.Div([
                                dcc.RadioItems(id='profit-radio', options=[{'label': 'Line', 'value': 'line'}, {'label': 'Bar', 'value': 'bar'}, {'label': 'Scatter', 'value': 'scatter'}], value='line')
                            ], className='d-flex justify-content-center p-1'),
                            ]),
                        ]
                        ),
                    ], className='d-flex justify-content-center flex-wrap align-items-center'),
                    dcc.Graph(id='profit-graph'),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col([
                            html.H5('Top 5 product with high profit', className='text-center fw-bold'),
                            dcc.Graph(id='profit-top-sold-product',config={'displayModeBar': False}, ),
                            ], width=6),
                        dbc.Col(
                            [
                                html.H5('Top 5 product with least profit', className='text-center fw-bold'),
                                dcc.Graph(id='profit-least-sold-product',config={'displayModeBar': False}, ),
                            ], width=6, className='border-start'),
                    ]),
                
                ]),
            ]),
        ], width=6),
    ]),

     # Cards as links to other pages
    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                dcc.Link(html.H5("To Table Page", className="card-title"), href='/table' , 
                         className='text-decoration-none text-dark fw-bold text-center '
                         ),
            ]),
            className="mt-4",
        ), width=6),
        dbc.Col(dbc.Card(
            dbc.CardBody([
                 dcc.Link(html.H5("To Graph Page", className="card-title"), href='/graph' , 
                         className='text-decoration-none text-dark fw-bold text-center '
                         ),
            ]),
            className="mt-4",
        ), width=6),
    ]),

], className="home-container")


def home_callbacks(app):
    return sales_callbacks(app),profit_callbacks(app)

