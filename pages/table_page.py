import dash
from dash import dcc, html, callback, Output, Input, State, callback_context, no_update
import dash_bootstrap_components as dbc
import pandas as pd
from dash_ag_grid import AgGrid
from data import df
from components.filter import filter_df
from components.validate import validate_date
import random


dash.register_page(__name__, path='/table', name='Table') 

# Define column definitions, setting 'Order ID' and 'Ship Date' as non-editable
editable_columns = ['Customer Name', 'Product Name', 'Category','Sub-Category']
column_defs = [
    {'field': col, 'editable': col in editable_columns, 'filter':True,  'checkboxSelection': col == 'Row ID'}
    for col in df.columns
]

layout = html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div(id='notice-container'),
                    html.H3('Super Store Sales Table'),
                     AgGrid(
                        id='table-editable',
                        rowData=df.to_dict('records'),
                        columnDefs=column_defs,
                        defaultColDef = {'editable': False},
                        style={'height': '60vh', 'width': '100%'},
                        dashGridOptions = {"rowDragManaged": True,
                                        "animateRows": True,
                                        "suppressMoveWhenRowDragging": True,
                                        "rowDragEntireRow": True,  
                                        "rowDragMultiRow": True,
                                        "rowSelection": "multiple",
                                        "singleClickEdit": True,
                                        "pagination": True,
                                        }
                        ),
                ])
            ]), 
            html.Div([
                html.Button('Add New Entry', id='add-row-button', className='btn btn-primary px-4', n_clicks=0),
                html.Button('Delete', id='delete-row-button', className='btn btn-danger px-4', n_clicks=0),
            ],id='add-delete-buttons')
        ], fluid=True),
        dcc.Store(id='visibility-state', data={'visible': False}),
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    # Input fields for adding new data
                    html.Div([
                    html.Label('Add New Data', className='h5'),
                    html.Button('×', id='close-button', className='close-btn'),
                    ], className='d-flex justify-content-between py-2'),
                    html.Div([
                        html.Div([
                            html.Label('Product ID *:', htmlFor='input-product-id'),
                            dcc.Input(id='input-product-id', type='text', placeholder='Product ID',
                                      ),
                        ], className='container add-data-inputs'),
                        html.Div([
                            html.Label('Customer Name :', htmlFor='input-customer-name'),
                            dcc.Input(id='input-customer-name', type='text', placeholder='Customer Name',),
                        ], className='container add-data-inputs'),
                        html.Div([
                            html.Label('Category :', htmlFor='input-category'),
                            dcc.Dropdown(id='dropdown-category', placeholder='Category', value='Furniture'),
                        ], className='container add-data-inputs'),
                        html.Div([
                            html.Label('Sub-Category :', htmlFor='input-sub-category'),
                            dcc.Dropdown(id='dropdown-sub-category', placeholder='Sub-Category', value='Bookcases'),
                        ], className='container add-data-inputs'),
                        html.Div([
                            html.Label('Quantity *:', htmlFor='input-quantity'),
                            dcc.Input(id='input-quantity', type='number', min = 0, step=1,placeholder='Quantity',
                                       ),
                        ], className='container add-data-inputs'),
                    ], className='container p-3 card'),
                    # Add button
                    html.Div([
                        html.Button('Add', id='add-button', className='btn btn-primary px-4', n_clicks=0),
                    ], className='d-flex justify-content-center p-3'),
                    html.Div(id='table-container'),
                    html.Div(id='message-container'),
                ])
            ], className='card p-5')
        ],id='add-entry-container' , className='container p-5')
    ],)

@callback(
    Output('dropdown-category', 'options'),
    Input('url', 'pathname')  
)
def set_category_options(pathname):
    if pathname != '/table':  
        return no_update
    categories = df['Category'].unique()
    return [{'label': cat, 'value': cat} for cat in categories]

@callback(
    Output('dropdown-sub-category', 'options'),
    [Input('dropdown-category', 'value'),
      Input('url', 'pathname')  ],
)
def set_subcategory_options(selected_category, pathname):
    if not selected_category or pathname != '/table': 
        return no_update
    filtered_df = df[df['Category'] == selected_category]
    sub_categories = filtered_df['Sub-Category'].unique()
    return [{'label': sub_cat, 'value': sub_cat} for sub_cat in sub_categories]

@callback(
    Output('visibility-state', 'data'),
    [Input('add-row-button', 'n_clicks'),
     Input('close-button', 'n_clicks')],
    [State('visibility-state', 'data')]
)
def toggle_visibility(add_clicks, close_clicks, visibility_data):
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == 'add-row-button':
        visibility_data['visible'] = True
    elif triggered_id == 'close-button':
        visibility_data['visible'] = False
    return visibility_data

# Callback to update the style of 'add-entry-container' based on visibility state
@callback(
    Output('add-entry-container', 'style'),
    [Input('visibility-state', 'data')]
)
def update_container_style(visibility_data):
    if visibility_data['visible']:
        return {'display': 'block'}
    else:
        return {'display': 'none'}
        

@callback(
    [
    Output('notice-container', 'children'),
    Output('table-editable', 'rowData'),
    Output('message-container', 'children'),
    Output('input-product-id', 'value'),
    Output('input-customer-name', 'value'),
    Output('dropdown-category', 'value'),
    Output('dropdown-sub-category', 'value'),
    Output('input-quantity', 'value'),],
    [
    Input('add-button', 'n_clicks'),
    Input('delete-row-button', 'n_clicks'),
    Input('country-dropdown', 'value'),
    Input('state-dropdown', 'value'),
    Input('city-dropdown', 'value'),
    Input('start-date-picker', 'date'),
    Input('end-date-picker', 'date'),
    Input('date-granularity-dropdown', 'value'),
    ],
    [
    State('input-product-id', 'value'),
    State('input-customer-name', 'value'),
    State('dropdown-category', 'value'),
    State('dropdown-sub-category', 'value'),
    State('input-quantity', 'value'),
    State('table-editable', 'selectedRows'),
    ],
)
def update_table(add_clicks, delete_clicks,selected_countries, selected_states, selected_cities, start_date, end_date, granularity, product_id, customer_name, category, sub_category, quantity, selected_rows):
    global df

    filtered_df = df.copy()
    if(validate_date(start_date, end_date) != 'valid'):
        return no_update,no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    filtered_df = filtered_df[(filtered_df['Order Date'] >= start_date) & (filtered_df['Order Date'] <= end_date)]
    
    filtered_df = filter_df(df, selected_countries, selected_states, selected_cities, start_date, end_date)
    # Filtering the DataFrame based on the date range, country and cities END

    # Adding and deleting functionality START
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'add-button':

          # Validate the required inputs are not empty
        if not product_id or quantity is None:
            return no_update,no_update, dbc.Alert("Please enter values for all required fields.", color="danger", duration=4000), product_id, customer_name, category, sub_category, quantity	

        # Check if the new Product ID already exists
        if product_id in df['Product ID'].values:
            return no_update,no_update, dbc.Alert( "Product ID ' {} 'already Exits. Entry not added.".format(product_id), color="danger", duration=4000), product_id, customer_name, category, sub_category, quantity 
        
        try:
            quantity = int(quantity)
        except ValueError:
            return '',no_update, dbc.Alert( "Invalid quantity. Entry not added.", color="danger", duration=4000), product_id, customer_name, category, sub_category, quantity
       

        # Create a new row (dict) for the new entry
        new_entry = {
            'Product ID': product_id,
            'Quantity': quantity,
        }
        # Populate 'Customer Name', 'Category', and 'Sub-Category' with validation
        for field, value in {'Customer Name': customer_name, 'Category': category, 'Sub-Category': sub_category}.items():
            if value:  
                new_entry[field] = value
            else: 
                if not df[field].isnull().all():
                    new_entry[field] = random.choice(df[field].dropna().values)
                else:
                    new_entry[field] = 'Default'

        
        # Populate the remaining columns with random values from the corresponding column in df
        for col in df.columns:
            if col not in new_entry:
                if not df[col].isnull().all():  
                    new_entry[col] = random.choice(df[col].dropna().values)
                else:
                    new_entry[col] = 'Default'
        # Append the new entry to the DataFrame
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        filtered_df = filter_df(df, selected_countries, selected_states, selected_cities, start_date, end_date)
        return no_update,filtered_df.to_dict('records'), dbc.Alert("Entry added successfully.", color="success", duration=4000), '', '', None, None, ''

    elif triggered_id == 'delete-row-button':
        if not selected_rows:
            return dbc.Alert("No rows selected for deletion.", color="warning", duration=4000),no_update, no_update,no_update, no_update,no_update, no_update, no_update
        

        # Get the primary key values of the selected rows
        selected_ids = [row['Product ID'] for row in selected_rows]
        
        # Remove selected rows from the DataFrame
        df = df[~df['Product ID'].isin(selected_ids)]
        filtered_df = filter_df(df, selected_countries, selected_states, selected_cities, start_date, end_date)
        return dbc.Alert("Selected rows deleted successfully.", color="success", duration=4000),filtered_df.to_dict('records'), no_update, '', '', None, None, ''
    
    # Adding and deleting functionality END 

    return no_update,filtered_df.to_dict('records'), no_update, no_update,no_update,no_update,no_update,no_update


