from dash import html,dcc
import dash_bootstrap_components as dbc

sidebar = html.Div(
     [
        dcc.Link([
            html.Img(src="assets/logo.png", className="img-fluid" ),
            html.H2("Super Store", className="display-7 fw-bold text-center"),
        ], href="/", className='text-decoration-none text-dark'), 

        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink([html.I(className="fas fa-home fa-fw sidebar-icons"),"Home"], href="/", active="exact"),
                dbc.NavLink([html.I(className="fas fa-table fa-fw sidebar-icons"),"Table"],  href="/table", active="exact"),
                dbc.NavLink([html.I(className="fas fa-chart-bar fa-fw sidebar-icons"),"Graph"],  href="/graph", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)


def create_sidebar():
    return sidebar