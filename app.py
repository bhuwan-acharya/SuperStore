import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.sidebar import create_sidebar
from components.content import create_content, content_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://use.fontawesome.com/releases/v5.8.1/css/all.css"], use_pages=True, suppress_callback_exceptions=True)


from pages.home_page import home_callbacks
from pages.graph_page import graphs_callbacks

app.layout = html.Div([
    dcc.Location(id='url'),
    create_sidebar(),  
    html.Div([
    create_content(),
    dash.page_container
    ], className="content")
])

content_callbacks(app),
home_callbacks(app)
graphs_callbacks(app)


if __name__ == '__main__':
    app.run_server(debug=True)
