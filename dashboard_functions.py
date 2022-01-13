import pandas as pd
import plotly.express as px
from dash import dcc
from data_clean.data_cleaning import us_state_abbrev
from app import db


def data_reader():
    '''
    Read cleaned data into memory

    Parameters:
    -----------
    None

    Returns:
    df: Pandas dataframe
    '''

    df = pd.read_sql('covid_data', con = db.engine)
    df = df.drop(['Id'], axis=1)
    df = df[df['Province_State'] != 'Recovered']
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by = 'Date', ascending = True)
    df['Date'] = df['Date'].astype(str)
    df['State_Code'] = df['Province_State'].map(us_state_abbrev)

    return df


def unique_states_and_cols(df):
    '''
    Return a list of unique states and columns from a dataframe

    Parameters:
    -----------
    df: dataframe

    Returns:
    unique_states: list
    unique_columns: list
    '''

    unique_states = sorted(df['Province_State'].unique().tolist())
    unique_cols = sorted(df.columns.tolist())
    dropped_cols = ['Province_State', 'State_Code']
    for col in dropped_cols:
        unique_cols.remove(col)

    return unique_states, unique_cols


def heatmap_generator(df, df_column, plot_title):
    '''
    Generate heatmap graph

    Parameters:
    -----------
    df: dataframe
    df_column: pandas series
    plot_title: str

    Returns:
    heatmap: dcc.Graph
    '''

    fig = px.choropleth(
        data_frame = df,
        locations = 'State_Code',
        locationmode = 'USA-states',
        color = df_column,
        scope = 'usa',
        color_continuous_scale = 'blues',
        hover_name = 'Province_State',
        hover_data = {
            'Date': False,
            'Incident_Rate': True,
            'State_Code': False
        },
        title=plot_title,
        animation_frame = 'Date'
    )

    fig.update_layout(
        title = {'x': 0.5, 'y': 0.85},
        margin = {'b': 0, 'l': 0, 'r': 0},
    )
    fig['layout']['updatemenus'][0]['pad']['l'] = 50
    
    heatmap = dcc.Graph(
        figure = fig,
    )

    return heatmap


def aggregated_stats_generator(df, unique_cols):
    '''
    Generate scatter plot graph

    Parameters:
    -----------
    df: dataframe
    unique_cols: list

    Returns:
    aggregated_stats: dcc.Graph
    '''

    df = df.groupby('Date').sum()
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])

    undisplayed_traces = ['Active', 'Case_Fatality_Ratio', 'Date', 'Incident_Rate', 'Recovered', 'Testing_Rate', 'Total_Test_Results']

    fig = px.scatter(
        data_frame = df,
        x = 'Date',
        y = unique_cols,
        log_y = True,
        title = 'Log(Y-Axis) Aggregated Stats'
    )

    fig.update_layout(
        title = {'x': 0.5},
        xaxis = {'title': 'Date'},
        yaxis = {'title': 'Counts'},
        legend = {'title': 'Category'},
    )

    fig.for_each_trace(
        lambda trace: trace.update(visible="legendonly") if trace.name in undisplayed_traces else ()
    )

    aggregated_stats = dcc.Graph(
        figure = fig
    )

    return aggregated_stats

if __name__=='__main__':
    print('This is the dashboard functions file')