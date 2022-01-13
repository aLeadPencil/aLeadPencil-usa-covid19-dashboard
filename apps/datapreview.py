import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, dash_table
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


# Create Data Table
data_table = dash_table.DataTable(
    # Horizontal scrollbar for table when page is loaded on a smaller screen
    style_table = {
        'overflowX': 'auto',
    },

    # Change header color / font weight
    style_header = {
        'backgroundColor': '#48a1cf99',
        'fontWeight': 'bold'
    },

    # Change cell border color
    style_cell = {
        'border': '1px solid #48a1cf'
    },

    # Change selected background color of cells
    style_data_conditional = [
        {
            'if': {'state': 'active'},
            'backgroundColor': '#48a1cf50',
            'border': '1px solid #48a1cf'
        }
    ],

    # Maintain same table height regardless of contents in cell
    css = [
        {
            'selector': '.dash-spreadsheet td div',
            'rule': '''
                line-height: 15px
                max-height: 50px; 
                min-height: 50px; 
                height: 50px;
                display: block;
                overflow-y: hidden;
            '''
        }
    ],

    columns = [{'name': i, 'id': i} for i in df.columns],
    page_size = 10,
    data = df.to_dict('records')
)


# Create Offcanvas
offcanvas = html.Div(
    children=[
        dbc.Button(
            children=['Data Dictionary'],
            id="open-offcanvas",
            n_clicks=0,
            outline=True,
            color='light'
        ),

        dbc.Offcanvas(
            html.P(
                children=[
                    html.Span('Province_State: ', className="text-info"),
                    html.Span('Province, state or dependency name.'),
                    html.Br(),
                    html.Br(),

                    html.Span('Confirmed: ', className="text-info"),
                    html.Span('Counts include confirmed and probable (where reported).'),
                    html.Br(),
                    html.Br(),

                    html.Span('Deaths: ', className="text-info"),
                    html.Span('Counts include confirmed and probable (where reported).'),
                    html.Br(),
                    html.Br(),

                    html.Span('Recovered: ', className="text-info"),
                    html.Span('Recovered cases are estimates based on local media reports, and state and local reporting when available, and therefore may be substantially lower than the true number.'),
                    html.Br(),
                    html.Br(),

                    html.Span('Active: ', className="text-info"),
                    html.Span('Active cases = total cases - total recovered - total deaths.'),
                    html.Br(),
                    html.Br(),

                    html.Span('Incident_Rate: ', className="text-info"),
                    html.Span('Cases per 100,000 persons.'),
                    html.Br(),
                    html.Br(),

                    html.Span('Total_Test_Results: ', className="text-info"),
                    html.Span('Total number of people who have been tested.'),
                    html.Br(),
                    html.Br(),

                    html.Span('Case_Fatality_Ratio : ', className="text-info"),
                    html.Span('Number recorded deaths * 100/ Number confirmed cases.'),
                    html.Br(),
                    html.Br(),

                    html.Span('Testing_Rate: ', className="text-info"),
                    html.Span('Total test results per 100,000 persons. The "total test results" are equal to "Total test results (Positive + Negative)"'),
                    html.Br(),
                    html.Br(),

                    html.Span('Date: ', className="text-info"),
                    html.Span('The most recent date the data was updated.'),
                    html.Br(),
                    html.Br(),
                ]
            ),
            id="offcanvas",
            title="Data Dictionary",
            is_open=False,
            scrollable=True
        ),
    ]
)


# Callback For Offcanvas
@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


# Page Layout Parts
page_content_1 = dbc.Container(
    children=[
        dbc.Row(
            className="g-0",
            children=[
                dbc.Col(
                    children=[
                        dbc.Card(
                            className="text-center py-3",
                            children=[
                                html.Div(
                                    dbc.Button(
                                        className="text-light",
                                        children=['Data Table'],
                                        outline=True,
                                        disabled=True,
                                        style={'opacity': '1'},

                                    )
                                ),
                            ],
                            color="dark",
                            style={'border': '0px', 'border-radius': '0', 'border-right': '0.1em solid #48a1cf'}
                        ),
                    ],
                    lg=9
                ),

                dbc.Col(
                    dbc.Card(
                        className="text-center py-3",
                        children=[offcanvas],
                        color="dark",
                        style={'border': '0px', 'border-radius': '0',}
                    )
                )
            ]
        ),
        data_table
    ]
)


# Page Layout
layout = html.Div(
    children=[
        page_content_1
    ]
)

if __name__ == '__main__':
    print('This is the df preview layout file')