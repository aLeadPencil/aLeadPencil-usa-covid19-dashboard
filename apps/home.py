from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
from app import app, db


# Read in data
sql_query = '''
SELECT
    *
FROM
    covid_data
LIMIT 100
'''
df = pd.read_sql(sql = sql_query, con = db.engine)
df = df.drop(['Id'], axis=1)


# Create Download/Source/Contact Cards
download_card = dbc.Card(
    className="justify-content-center text-center py-1",
    children=[
        dbc.Row(
            dbc.Col(html.H2('Copy of Data'))
        ),

        dbc.Row(
            dbc.Col(
                children=[
                    dbc.Button(
                        children=['Download'],
                        id='btn-download-data',
                        color='dark'
                    ),

                    dcc.Download(id="download-data")
                ]
            )
        )
    ],
    color='light',
    style={'border': '1px solid black', 'height': '100%'}
)

source_card = dbc.Card(
    className="justify-content-center text-center py-1",
    children=[
        dbc.Row(
            dbc.Col(html.H2('View Source Code'))
        ),

        dbc.Row(
            dbc.Col(
                dbc.Button(
                    children=[
                        dcc.Link(
                            'GitHub',
                            href='https://www.github.com',
                            target='_blank',
                            style={'text-decoration': 'none', 'color': 'white'}
                        )
                    ],
                    color='dark',
                )
            )
        )
    ],
    color='light',
    style={'border': '1px solid black', 'height': '100%'}
)

contact_card = dbc.Card(
    className="justify-content-center text-center py-1",
    children=[
        dbc.Row(
            dbc.Col(html.H2('Contact Me'))
        ),

        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Button(
                        children=[
                            dcc.Link(
                                'LinkedIn',
                                href='https://www.linkedin.com/in/kvn-chu/',
                                target='_blank',
                                style={'text-decoration': 'none', 'color': 'white'}
                            )
                        ],
                        color='dark'
                    )
                ),

                dbc.Col(
                    dbc.Button(
                        children=[
                            dcc.Link(
                                'Email Me',
                                href="mailto:kchu8150@gmail.com",
                                target='_blank',
                                style={'text-decoration': 'none', 'color': 'white'}
                            )
                        ],
                        color='dark'
                    )
                )
            ]
        )
    ],
    color='light',
    style={'border': '1px solid black', 'height': '100%'}
)


# Page Layout Parts
page_content_1 = dbc.Container(
    className="mt-5 mb-3",
    children=[
        dbc.Row(
            dbc.Col(
                children=[
                    html.H1(className="text-center", children=['VISUALIZATION OF COVID-19 DATA IN THE US']),
                    html.Hr(),
                    html.H5(
                        className="mt-4", 
                        children=[
                            'As the Covid-19 pandemic continues on, there is new data available everyday regarding it. This dashboard aims to provide users data visualizations surrounding the pandemic that are always up to date. The data used in this dashboard is automatically webscraped every 2 weeks from John Hopkins University\'s ',
                            html.A(children=['GitHub Repository'], href="https://github.com/CSSEGISandData/COVID-19", target="_blank", style={'color': '#48a1cf'}),
                            ' and saved into a PostgreSQL database.'
                        ]
                    ),

                    html.H5(
                        className="mt-5",
                        children=[
                            'The dashboard consists of two main pages:',
                        ]
                    ),

                    html.H5(
                        className="mt-1 mb-4",
                        children=[
                            html.Span(html.A(children=['Data Preview'], href="/data-preview", style={'color': '#48a1cf'})),
                            ' showcases a table of what the raw data table looks like and provides a data dictionary for columns in the table.',

                            html.Br(),

                            html.Span(html.A(children=['Dashboard'], href="/dashboard", style={'color': '#48a1cf'})),
                            ' showcases all the visualizations and trends of the data.'
                        ]
                    ),

                    html.Hr()
                ]
            )
        )
    ]
)

page_content_2 = dbc.Container(
    dbc.Row(
        children=[
            dbc.Col(download_card),
            dbc.Col(source_card),
            dbc.Col(contact_card)
        ]
    )
)


# Callback To Download Data
@app.callback(
    Output("download-data", "data"),
    Input("btn-download-data", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_csv, filename="data.csv")


# Page Layout
layout = html.Div(
    children=[
        page_content_1,
        page_content_2
    ]
)

if __name__ == '__main__':
    print('This is the home layout file')