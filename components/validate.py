import pandas as pd
import dash_bootstrap_components as dbc

def validate_date(start_date, end_date):
    if (start_date is None or end_date is None):
        return ''

    try:
        start_date_dt = pd.to_datetime(start_date)
        end_date_dt = pd.to_datetime(end_date)
        if start_date_dt > end_date_dt:
            return dbc.Alert("Start date must be before end date.", duration=4000, color='danger') 
    except ValueError:
        return dbc.Alert("Invalid date format. Please enter valid dates.", duration=4000, color='danger')
    return 'valid'