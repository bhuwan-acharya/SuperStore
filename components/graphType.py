import plotly.express as px

def graph_types( df, gtype, color, title, y , x='Order Date'):
    custom_colors = ['#636EFA', '#FF8D47', '#82C09A']
    if gtype == 'bar':
            fig = px.bar(df, x='Order Date', y=y, color=color,title=title, color_discrete_sequence=custom_colors)
            fig.update_layout(barmode='stack')
    elif gtype == 'scatter':
        fig = px.scatter(df, x='Order Date', y=y, color=color,title=title, color_discrete_sequence=custom_colors)
    else:
            fig = px.line(df, x='Order Date', y=y, color=color,title=title, color_discrete_sequence=custom_colors)
    return fig
