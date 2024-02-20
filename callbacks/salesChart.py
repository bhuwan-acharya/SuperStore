from dash import Input, Output, no_update
import plotly.express as px
import pandas as pd
from data import df
from components.filter import filter_df
from components.validate import validate_date
from components.granularity import granularity_freq
from components.graphType import graph_types


# Function to register callbacks, which takes the Dash app instance as an argument
def sales_callbacks(app):
    @app.callback(
        [
        Output('sales-graph', 'figure'),
        Output('pie-chart', 'figure'),
        Output('top-sold-product', 'figure'),
        Output('least-sold-product', 'figure'),
        ],
        [Input('country-dropdown', 'value'),
         Input('state-dropdown', 'value'),
         Input('city-dropdown', 'value'),
         Input('start-date-picker', 'date'),
         Input('end-date-picker', 'date'),
         Input('date-granularity-dropdown', 'value'),
         Input('sales-radio', 'value'),
         ]
    )
    def update_graph(selected_countries, selected_states, selected_cities, start_date, end_date, granularity, graph_type):

        if(validate_date(start_date, end_date) != 'valid'):
            return no_update,no_update,no_update,no_update 
        
        filtered_df = filter_df(df, selected_countries, selected_states, selected_cities, start_date, end_date)

        if selected_cities:
            granularity_region = 'City'
            color_column = 'City'
        elif selected_states:
            granularity_region = 'State/Province'
            color_column = 'State/Province'
        else:
            granularity_region = 'Country/Region'
            color_column = 'Country/Region'

        freq = granularity_freq(granularity)

        grouped_trend = filtered_df.groupby([pd.Grouper(key='Order Date', freq=freq), granularity_region]).agg({'Sales': 'sum'}).reset_index()

        trend_fig = graph_types(grouped_trend,graph_type, color_column,'Sales Trend','Sales')
        trend_fig.update_layout(title={
            'text':'Sales Trend',                      
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
        )

        # Pie Chart
        grouped_pie_chart = filtered_df.groupby('Category')['Sales'].sum().reset_index()
        custom_colors = ['#636EFA', '#FF8D47', '#82C09A']
        pie_chart = px.pie(grouped_pie_chart, names='Category', values='Sales', 
             hole=.5, color_discrete_sequence=custom_colors)
        pie_chart.update_traces(textposition='inside', textinfo='percent+label')
        pie_chart.update_layout(showlegend=False, 
                  margin=dict(t=0, b=0, l=0, r=0), 
                  )

        #  top 5 products with high sales
        top_products = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5).reset_index()
        top_products['Product Name'] = [' '.join(name.split()[:2]) for name in top_products['Product Name']]
        top_5_high_sold_products = px.bar(top_products, x='Product Name', y='Sales')
        top_5_high_sold_products.update_layout(showlegend=False, 
                  margin=dict(t=0, b=20, l=0, r=0), 
                  xaxis_tickangle=-45,
                  )

        # top 5 Product with least sales
        least_products = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=True).head(5).reset_index()
        least_products['Product Name'] = [' '.join(name.split()[:2]) for name in least_products['Product Name']]
        least_sold_products = px.bar(least_products, x='Product Name', y='Sales', color_discrete_sequence=['#ff8d47'])
        least_sold_products.update_layout(showlegend=False, 
                                          xaxis_tickangle=-45,
                                            margin=dict(t=0, b=20, l=0, r=0), 
                                            )



             
        return trend_fig, pie_chart, top_5_high_sold_products, least_sold_products
    
    @app.callback(
        Output('total-order-sales-text', 'children'),
        [Input('country-dropdown', 'value'),
         Input('state-dropdown', 'value'),
         Input('city-dropdown', 'value'),
         Input('start-date-picker', 'date'),
         Input('end-date-picker', 'date'),
         ]
    )
    def update_total_orders(selected_countries, selected_states, selected_cities, start_date, end_date):

        filtered_df = filter_df(df, selected_countries, selected_states, selected_cities, start_date, end_date)

        return f'Total Orders: {filtered_df['Quantity'].sum()}'
    @app.callback(
        Output('total-sales-text', 'children'),
        [Input('country-dropdown', 'value'),
         Input('state-dropdown', 'value'),
         Input('city-dropdown', 'value'),
         Input('start-date-picker', 'date'),
         Input('end-date-picker', 'date'),
         ]
    )
    def update_total_orders(selected_countries, selected_states, selected_cities, start_date, end_date):
        if(validate_date(start_date, end_date) != 'valid'):
            return no_update
        filtered_df = filter_df(df, selected_countries, selected_states, selected_cities, start_date, end_date)
        
        return f'Total Sales: ${filtered_df['Sales'].sum().round(2)}'
