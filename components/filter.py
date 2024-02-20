def filter_df(df, selected_countries, selected_states, selected_cities, start_date, end_date):
    filtered_df = df[(df['Order Date'] >= start_date) & (df['Order Date'] <= end_date)]
    if selected_countries:
        filtered_df = filtered_df[filtered_df['Country/Region'].isin(selected_countries)]

    if selected_states:
        filtered_df = filtered_df[filtered_df['State/Province'].isin(selected_states)]
    
    if selected_cities:
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]
    
    return filtered_df