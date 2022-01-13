import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

from app import app
from apps import home, dashboard, datapreview
from app import server #not used in file but necessary for heroku deployment


# Create navbar, error page
navbar_dropdown = dbc.Row(
    className='ms-auto',
    children=[
        dbc.Col(
            children=[
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem('Home', href='/'),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem('Data Preview', href='/data-preview'),
                        dbc.DropdownMenuItem('Dashboard', href='/dashboard')
                    ],
                    label='Explore',
                    menu_variant='dark',
                    nav=True,
                    in_navbar=True,
                    toggle_style={'color':'#9a9da0'},
                )
            ]
        )
    ],
    align='center'
)

navbar = dbc.Navbar(
    children=[
        dbc.Container(
            className='px-5',
            children=[
                html.A(
                    className='text-decoration-none',
                    children=[
                        dbc.Row(
                            className='g-0',
                            children=[
                                # dbc.Col(html.Img(src=PLOTLY_LOGO, height='30px')),
                                dbc.Col(dbc.NavbarBrand('USA COVID-19 DASHBOARD', className='ms-2'))
                            ],
                            align='center',
                        )
                    ],
                    href='/'
                ),

                dbc.NavbarToggler(id='navbar-toggler', n_clicks=0),
                
                dbc.Collapse(
                    navbar_dropdown,
                    id='navbar-collapse',
                    is_open=False,
                    navbar=True
                )
            ]
        )
    ],
    color='dark',
    dark=True
)

error_page = dbc.Container(
    children=[
        html.H1(
            className="text-center rounded mt-3",
            children=[
                "PAGE DOESN'T EXIST",
                html.Hr(),
                dbc.Button(
                    className="btn btn-secondary",
                    children=["Click Here To Return Home"],
                    href="/",
                    color='dark'
                )
            ]
        )
    ]
)


# Callbacks
# Callback For Page Loading
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/data-preview':
        return datapreview.layout
    elif pathname == '/dashboard':
        return dashboard.layout
    else:
        return error_page

# Callback For Navbar Toggler (Small Screens))
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# App Layout
app.layout = html.Div(
    children=[
        dbc.Row(
            className="mb-4 mx-0",
            children=[
                dbc.Col(children=[navbar], className="p-0")
            ]
        ),

        dcc.Location(id='url', refresh=False),
        html.Div(
            children=[],
            id='page-content'
        )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=False)