from dash import Input, Output, no_update
import plotly.express as px
import pandas as pd
import numpy as np
from data import df
from components.filter import filter_df
from components.granularity import granularity_freq
from components.validate import validate_date

def create_timeline(app):

    @app.callback(   
        [
        Output('sales-timeline', 'figure'),
        Output('profit-timeline', 'figure'),
        Output('profit-ratio-timeline', 'figure'),
        Output('returns-timeline', 'figure'),
        Output('days-to-ship-timeline', 'figure'),
        Output('quantity-timeline', 'figure'),
        Output('dicount-timeline', 'figure'),
        ],
        [
        Input('country-dropdown', 'value'),
        Input('state-dropdown', 'value'),
        Input('city-dropdown', 'value'),
        Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'),
        Input('date-granularity-dropdown', 'value'),
        ]
    )
    def update_timeline(selected_countries, selected_states, selected_cities, start_date, end_date, granularity):
   
        if(validate_date(start_date, end_date) != 'valid'):
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update
        
        filtered_df = df[(df['Order Date'] >= start_date) & (df['Order Date'] <= end_date)]
        
        filtered_df = filter_df(filtered_df, selected_countries, selected_states, selected_cities, start_date, end_date)
        freq = granularity_freq(granularity)

        profit_grouped_df = filtered_df.groupby([pd.Grouper(key='Order Date', freq=freq)]).agg({'Profit': 'sum'}).reset_index()

        sales_grouped_df = filtered_df.groupby([pd.Grouper(key='Order Date', freq=freq)]).agg({'Sales': 'sum'}).reset_index()

        returned_grouped_df = filtered_df.groupby([pd.Grouper(key='Order Date', freq=freq)]).agg({'Returned': 'sum'}).reset_index()

        # For days to ship
        filtered_df['Days to Ship'] = (pd.to_datetime(filtered_df['Ship Date']) - pd.to_datetime(filtered_df['Order Date'])).dt.days
        day_to_ship_grouped_df = filtered_df.groupby([pd.Grouper(key='Order Date', freq=freq)]).agg({'Days to Ship': 'mean'}).reset_index()
        day_to_ship_grouped_df['Days to Ship'] = day_to_ship_grouped_df['Days to Ship'].fillna(0)

        # For profit ratio
        profit_ratio_grouped_df = filtered_df.groupby([pd.Grouper(key='Order Date', freq=freq)]).agg(
        Total_Profit=('Profit', 'sum'),
        Total_Sales=('Sales', 'sum')
        ).reset_index()
        # Calculate profit ratio and replace infinite values or NaN with 0
        profit_ratio_grouped_df['Profit Ratio'] = (profit_ratio_grouped_df['Total_Profit'] / profit_ratio_grouped_df['Total_Sales']).replace([np.inf, -np.inf, np.nan], 0) * 100

        # For quantity
        quantity_grouped_df = filtered_df.groupby([pd.Grouper(key='Order Date', freq=freq)]).agg({'Quantity': 'sum'}).reset_index()

        # For discount
        discount_grouped_df = filtered_df.groupby([pd.Grouper(key='Order Date', freq=freq)]).agg({'Discount': 'mean'}).reset_index()
        discount_grouped_df['Discount'] = discount_grouped_df['Discount'].fillna(0)

        profit_fig = px.line(
        profit_grouped_df, 
        x='Order Date', 
        y='Profit',  
        markers=True  
        )
        profit_fig.update_layout(
            yaxis_title='Total <br> profit($)',
            xaxis_title='',
            margin=dict(l=0, r=0, t=0, b=0),  
        )

        sales_fig = px.line(
        sales_grouped_df, 
        x='Order Date', 
        y='Sales',  
        markers=True  
        )
        sales_fig.update_layout(
            yaxis_title='Total <br> Sales($)',
            xaxis_title='',
            margin=dict(l=0, r=0, t=0, b=0), 
        )


        days_to_ship_fig = px.line(
        day_to_ship_grouped_df, 
        x='Order Date', 
        y='Days to Ship',  
        markers=True  
        )
        days_to_ship_fig.update_layout(
            yaxis_title='Days <br> To Ship',
            xaxis_title='',
            margin=dict(l=0, r=0, t=0, b=0), 
        )


        profit_ratio_fig = px.line(
        profit_ratio_grouped_df, 
        x='Order Date', 
        y='Profit Ratio',  
        markers=True  
        )
        profit_ratio_fig.update_layout(
            yaxis_title='Profit <br> Ration(%)',
            xaxis_title='',
            margin=dict(l=0, r=0, t=0, b=0), 
        )

        returned_fig = px.line(
        returned_grouped_df, 
        x='Order Date', 
        y='Returned',  
        markers=True  
        )
        returned_fig.update_layout(
            yaxis_title='Total No. of<br> Returns',
            xaxis_title='',
            margin=dict(l=0, r=0, t=0, b=0), 
        )


        quantity_fig = px.line(
        quantity_grouped_df, 
        x='Order Date', 
        y='Quantity',  
        markers=True  
        )
        quantity_fig.update_layout(
            yaxis_title='Total <br> Quantity',
            xaxis_title='',
            margin=dict(l=0, r=0, t=0, b=0),  
        )


        discount_fig = px.line(
        discount_grouped_df, 
        x='Order Date', 
        y='Discount',  
        markers=True  
        )
        discount_fig.update_layout(
            yaxis_title='Average <br> Discount(%)',
            margin=dict(l=0, r=0, t=0, b=0),  
        )
        return sales_fig, profit_fig, profit_ratio_fig, returned_fig, days_to_ship_fig, quantity_fig, discount_fig
    
