import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

VALID_USERNAME = '1'
VALID_PASSWORD = '1'

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])
server = app.server

login_layout = html.Div([
    dbc.Card([
        html.H3("Login", className="card-title"),
        dcc.Input(id='username-input', type='text', placeholder='Username'),
        dcc.Input(id='password-input', type='password', placeholder='Password'),
        html.Div(id='login-status', children=''),
        html.Button('Login', id='login-button', n_clicks=0, className="btn btn-primary mt-3")

    ], body=True, style={'width': '300px', 'margin': 'auto', 'marginTop': '100px'})
])

sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="bg-light",
)

main_layout = dbc.Container([
    dbc.Row([
        dbc.Col(
                [
                    html.Img(src='assets/crossist_logo.png')
                ], width=4
            ),
        dbc.Col(html.Div("Crossist Dashboard",
                         style={'fontSize':50, 'textAlign': 'center'}), width="auto"),
    ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/':
        return login_layout
    elif pathname == '/main':
        return main_layout
    else:
        return '404 Page Not Found'


@app.callback(
    Output('login-status', 'children'),
    Output('url', 'pathname'),
    Input('login-button', 'n_clicks'),
    State('username-input', 'value'),
    State('password-input', 'value')
)
def handle_login(n_clicks, username, password):
    if n_clicks == 0:
        return '', '/'

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return 'Login successful', '/main'
    else:
        return 'Invalid username or password', '/'


if __name__ == "__main__":
    app.run(debug=False)
