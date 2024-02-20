import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc
from callbacks.timeline import create_timeline
from callbacks.bubbleChart import create_bubble_chart

dash.register_page(__name__, path='/graph', name='Graph') 

metrics = ['Days to Ship', 'Discount', 'Profit', 'Profit Ratio', 'Quantity', 'Returned', 'Sales']
# Initial default values for dropdowns
default_x_axis = 'Sales'
default_y_axis = 'Profit'
breakdown_variables = ['Segment', 'Ship Mode', 'Customer Name', 'Category', 'Sub-Category', 'Product Name']

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H4('Key Performance Indicators Over Time', className='text-center p-4'),
                html.Div([
                    dcc.Graph(id='sales-timeline', className='timeline-graph',   
                    ),
                    dcc.Graph(id='profit-timeline',  className='timeline-graph'),
                    dcc.Graph(id='profit-ratio-timeline',  className='timeline-graph'),
                    dcc.Graph(id='returns-timeline',  className='timeline-graph'),
                    dcc.Graph(id='days-to-ship-timeline',  className='timeline-graph'),
                    dcc.Graph(id='quantity-timeline',  className='timeline-graph'),
                    dcc.Graph(id='dicount-timeline',  className='timeline-graph'),
                ]),
            ], width=5, className='timeline-graph-container'),
            dbc.Col([
                html.H4('Comparative Performance Insights', className='text-center p-4'),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.H6('X-axis'),
                            dcc.Dropdown(id='x-axis-dropdown', options=[{'label': metric, 'value': metric} for metric in metrics],value=default_x_axis, className='bubble-chart-dropdown'),
                        ]),
                        dbc.Col([
                            html.H6('Y-axis'),
                            dcc.Dropdown(id='y-axis-dropdown',
                                          options=[{'label': metric, 'value': metric} for metric in metrics if metric != default_x_axis],  # Exclude default X-axis value
                                          value=default_y_axis,
                                          className='bubble-chart-dropdown'
                                         ),
                        ]),
                        dbc.Col([
                            html.H6('Breakdown'),
                            dcc.Dropdown(id='breakdown-dropdown', 
                                         options=[{'label': var, 'value': var} for var in breakdown_variables],
                                        value='Segment', className='bubble-chart-dropdown'),
                        ]),
                    ], ),
                    dcc.Graph(id='bubble-chart', className='bubble-chart',style={'height': '50rem'}),
                ], className='p-1'),

            ], width=7),
        ], className='graph-page-row'),
    ], fluid=True),
])

def graphs_callbacks(app):

    @app.callback(
        [Output('x-axis-dropdown', 'options'),
        Output('y-axis-dropdown', 'options')],
        [Input('x-axis-dropdown', 'value'),
        Input('y-axis-dropdown', 'value')]
    )
    def update_y_axis_options(selected_x_metric, selected_y_metric):
        x_axis_options = [{'label': metric, 'value': metric} for metric in metrics if metric != selected_y_metric]
        y_axis_options = [{'label': metric, 'value': metric} for metric in metrics if metric != selected_x_metric]
        return x_axis_options, y_axis_options
    return create_timeline(app), create_bubble_chart(app)
