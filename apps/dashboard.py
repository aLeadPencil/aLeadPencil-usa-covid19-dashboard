import plotly.express as px
import dash
import dash_bootstrap_components as dbc
import plotly.io as pio
from dash import html, dcc, Input, Output
from app import app
from dashboard_functions import data_reader, unique_states_and_cols, heatmap_generator, aggregated_stats_generator
pio.templates.default = 'none'


# Read in data
df = data_reader()


# Dropdowns
# State Comparisons Dropdowns: States, Col1, Col2
unique_states, unique_cols = unique_states_and_cols(df)

states_dropdown = dcc.Dropdown(
    id = 'states-dropdown',
    options = [{'label': state, 'value': state} for state in unique_states],
    value = ['California', 'New York'],
    multi = True
)

column_dropdown1 = dcc.Dropdown(
    id = 'col-dropdown1',
    options = [{'label': col, 'value': col} for col in unique_cols],
    value = 'Confirmed',
)

column_dropdown2 = dcc.Dropdown(
    id = 'col-dropdown2',
    options = [{'label': col, 'value': col} for col in unique_cols],
    value = 'Deaths',
)


# Plots
# Overview Heatmaps
incident_rates_heatmap = heatmap_generator(df, df_column = 'Incident_Rate', plot_title = 'Incident Rates Across The US')
confirmed_cases_heatmap = heatmap_generator(df, df_column = 'Confirmed', plot_title = 'Confirmed Case Counts Across The US')

# Aggregated Stats Scatter Plots
aggregated_stats = aggregated_stats_generator(df, unique_cols)

# State Comparison Line Plots
fig_1 = dcc.Graph(
    id = 'fig-1',
    figure = {}
)

fig_2 = dcc.Graph(
    id = 'fig-2',
    figure = {}
)


# Callbacks to update graphs
# Callbacks for fig-1, fig-2
@app.callback(
    [
        Output(component_id='fig-1', component_property='figure'),
        Output(component_id='fig-2', component_property='figure'),

    ],
    [
        Input(component_id='states-dropdown', component_property='value'),
        Input(component_id='col-dropdown1', component_property='value'),
        Input(component_id='col-dropdown2', component_property='value')
    ]
)
def update_confirmed_cases(states_chosen, col_chosen1, col_chosen2):
    if (len(states_chosen) > 0) and (col_chosen1 is not None) and (col_chosen2 is not None):
        tmp_df = df[df['Province_State'].isin(states_chosen)]

        fig1 = px.line(
            data_frame = tmp_df,
            x = 'Date',
            y = col_chosen1,
            color = 'Province_State',
            log_y = True,
            title = '(Log) {} Counts'.format(col_chosen1)
        )
        
        fig1.update_layout(
            title = {'x': 0.5},
            xaxis = {'title': 'Date'},
            yaxis = {'title': 'Counts'},
            legend = {'title': 'State'},
        )

        fig1.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )


        fig2 = px.line(
            data_frame = tmp_df,
            x = 'Date',
            y = col_chosen2,
            color = 'Province_State',
            log_y = True,
            title = '(Log) {} Counts'.format(col_chosen2)
        )
        
        fig2.update_layout(
            title = {'x': 0.5},
            xaxis = {'title': 'Date'},
            yaxis = {'title': 'Counts'},
            legend = {'title': 'State'},
        )

        fig2.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        return fig1, fig2

    else:
        raise dash.exceptions.PreventUpdate


# Page Layout Parts
page_layout1 = dbc.Container(
    children=[
        dbc.Row(
            className="g-0",
            children=[
                dbc.Col(
                    dbc.Card(
                        className="text-light text-center bg-dark py-3",
                        children=[html.H4('Overview of Pandemic Across The US')]
                    )
                )
            ]
        ),

        dbc.Row(
            className="g-0",
            children=[
                dbc.Col(
                    incident_rates_heatmap
                ),

                dbc.Col(
                    confirmed_cases_heatmap
                )
            ]
        )
    ]
)

page_layout2 = dbc.Container(
    className="my-4",
    children=[
        dbc.Row(
            className="g-0",
            children=[
                dbc.Col(
                    dbc.Card(
                        className="text-light text-center bg-dark py-3",
                        children=[html.H4('Aggregated Statistics Since Beginning of Pandemic')]
                    )
                )
            ]
        ),

        dbc.Row(
            className="g-0",
            children=[
                dbc.Col(
                    aggregated_stats
                )
            ]
        )
    ]
)

page_layout3 = dbc.Container(
    className="my-4",
    children=[
        dbc.Row(
            className="g-0",
            children=[
                dbc.Col(
                    dbc.Card(
                        className="text-light text-center bg-dark py-2",
                        children=[
                            html.H4('State Comparisons'),
                            html.H6('Log(Y-Axis) to account for different population sizes')
                        ]
                    )
                )
            ]
        ),

        dbc.Row(
            className="g-0",
            children=[
                dbc.Col(states_dropdown),
            ]
        ),

        dbc.Row(
            className="g-0",
            children=[
                dbc.Col(column_dropdown1),
                dbc.Col(column_dropdown2)
            ]
        ),

        dbc.Row(
            className="g-0",
            children=[
                dbc.Col(fig_1),
                dbc.Col(fig_2)
            ]
        )
    ]
)


# Page Layout
layout = html.Div(
    children=[
        page_layout1,
        page_layout2,
        page_layout3
    ]
)


if __name__ == '__main__':
    print('This is the dashboard layout file')