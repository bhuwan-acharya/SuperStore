from dash import no_update,Input, Output
import plotly.express as px
from data import df
from components.filter import filter_df
from components.validate import validate_date

def create_bubble_chart(app):

    @app.callback(
        Output('bubble-chart', 'figure'),
        [
        Input('country-dropdown', 'value'),
        Input('state-dropdown', 'value'),
        Input('city-dropdown', 'value'),
        Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'),
        Input('date-granularity-dropdown', 'value'),
        Input('x-axis-dropdown', 'value'),
        Input('y-axis-dropdown', 'value'),
        Input('breakdown-dropdown', 'value')
        ]
    )
    def update_bubble_chart(selected_countries, selected_states, selected_cities, start_date, end_date, granularity,selected_x_metric, selected_y_metric, selected_breakdown):
        if(validate_date(start_date, end_date) != 'valid'):
            return no_update


        filtered_df = df[(df['Order Date'] >= start_date) & (df['Order Date'] <= end_date)]
        
        filtered_df = filter_df(filtered_df, selected_countries, selected_states, selected_cities, start_date, end_date)

        # Truncate the 'Product Name' to the first two words for the legend
        filtered_df['Product Name'] = filtered_df['Product Name'].apply(lambda x: ' '.join(x.split()[:2]))

        filtered_df = filtered_df.groupby([selected_breakdown, 'Order Date']).agg({
            selected_x_metric: 'sum',
            selected_y_metric: 'sum',
            'Sales': 'sum'  
        }).reset_index()


        fig = px.scatter(
            filtered_df,
            x=selected_x_metric,
            y=selected_y_metric,
            size='Sales', 
            color=selected_breakdown,  
            hover_name=selected_breakdown, 
            title=f'{selected_x_metric} vs {selected_y_metric} by {selected_breakdown}',
            log_x=True, size_max=60,
        )
        fig.update_layout(
            yaxis_title=selected_y_metric,
            xaxis_title=selected_x_metric,
            title_x=0.5
        )
        return fig 
    
