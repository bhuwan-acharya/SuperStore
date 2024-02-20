import pandas as pd

file_path = 'Superstore.xls'
df = pd.read_excel(file_path, sheet_name='Orders', header=0)
df_returns = pd.read_excel(file_path, sheet_name='Returns', header=0)

# Merge the returns data with the orders data
df = pd.merge(df, df_returns[['Order ID', 'Returned']], on='Order ID', how='left')
df['Returned'] = df['Returned'].fillna(0)
df['Returned'] = df['Returned'].apply(lambda x: 1 if x == 'Yes' else 0)

# Calculate Days to Ship
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])
df['Days to Ship'] = (df['Ship Date'] - df['Order Date']).dt.days

# Calculate Profit Ratio
df['Profit Ratio'] = (df['Profit'] / df['Sales']) * 100

