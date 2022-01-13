from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash
import dash_bootstrap_components as dbc

import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from data_clean.data_cleaning import dropped_columns, excluded_states


# Create Server/Dash Apps
server = Flask(__name__)
app = dash.Dash(
    __name__,
    server = server,
    external_stylesheets=[dbc.themes.SIMPLEX],
    suppress_callback_exceptions=True,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1"
        }
    ]
)


# Connect to Database
app.server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kjknwxubymslie:86d99d26f810414bf8b82c2813dcdd9bd1987bcd6d36a075ee979c396e4e65a7@ec2-34-193-235-32.compute-1.amazonaws.com:5432/d53c1rrm6cmp71'
app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app.server)

class CovidData(db.Model):
    __tablename__ = 'covid_data'

    Id = db.Column(db.Integer, primary_key=True)
    Province_State = db.Column(db.String(25))
    Confirmed = db.Column(db.Integer)
    Deaths = db.Column(db.Integer)
    Active = db.Column(db.Float)
    Incident_Rate = db.Column(db.Float)
    Total_Test_Results = db.Column(db.Float)
    Case_Fatality_Ratio = db.Column(db.Float)
    Testing_Rate = db.Column(db.Float)
    Date = db.Column(db.String(10))

    def __init__(self, Province_State, Confirmed, Deaths, Active, Incident_Rate, Total_Test_Results, Case_Fatality_Ratio, Testing_Rate, Date):
        self.Province_State = Province_State
        self.Confirmed = Confirmed
        self.Deaths = Deaths
        self.Active = Active
        self.Incident_Rate = Incident_Rate
        self.Total_Test_Results = Total_Test_Results
        self.Case_Fatality_Ratio = Case_Fatality_Ratio
        self.Testing_Rate = Testing_Rate
        self.Date = Date


# Update Database If Necessary 
def find_all_raw_urls(github_url, base_url):
    '''
    Extract all links from github repository page
    Filter the links for csv files which correspond to biweekly data
    Extract the date of each csv file which will be used later to name the file when saving it

    Parameters:
    -----------
    github_url: string of github repository url
    base_url: string of root raw_url

    Returns:
    extracted_dates: list of all available dates
    raw_urls: list of all available raw_urls
    '''
    
    page = requests.get(github_url)
    page_text = page.text
    soup = BeautifulSoup(page_text, 'html.parser')

    all_links = []
    filtered_csv_links = []
    extracted_dates = []
    raw_urls = []

    for link in soup.find_all('a'):
        href_link = link.get('href')
        all_links.append(href_link)

    r = re.compile('.*csv')
    all_csv_links = list(filter(r.match, all_links))
            
    for link in all_csv_links:
        if (link[-11:-9] == '13') or (link[-11:-9] == '27'):
            filtered_csv_links.append(link)
            
    for link in filtered_csv_links:
        extracted_date = link[-14:-4]
        extracted_dates.append(extracted_date)
        
    for date in extracted_dates:
        raw_url = base_url + date + '.csv'
        raw_urls.append(raw_url)
        
    return extracted_dates, raw_urls


def fill_database(connection, extracted_dates, raw_urls):
    '''
    Read an existing SQL table into memory
    If the table is empty then fill the table with all available records
    If the table is not empty then check for missing records and fill them in

    Parameters:
    -----------
    connection: database connection
    extracted_dates: list of all available dates
    raw_urls: list of all available raw_urls

    Returns:
    None
    '''

    df = pd.read_sql('covid_data', con = connection)
    
    # If database is empty then fill in every missing record
    if df.empty:
        for idx, _ in enumerate(raw_urls):
            tmp_df = pd.read_csv(raw_urls[idx])
            tmp_df = tmp_df[~tmp_df['Province_State'].isin(excluded_states)].reset_index(drop = True)
            tmp_df = tmp_df.drop(dropped_columns, axis = 1, errors = 'ignore')
            tmp_df['Date'] = extracted_dates[idx]
            tmp_df.reset_index(inplace = True)
            tmp_df = tmp_df.rename(columns = {'index': 'Id'})
            
            df = pd.concat([df, tmp_df], ignore_index = True).drop_duplicates(keep = False)
            df = df.drop(columns=['Id'], axis = 1)
            df.reset_index(inplace = True)
            df = df.rename(columns = {'index': 'Id'})
            
        df.to_sql('covid_data', con = connection, if_exists = 'append', index = False)
        print('Filled in empty database')
        return None
        
    # If database is not empty, then check for any missing records and append them in
    else:
        existing_dates = df['Date'].unique().tolist()
        existing_row_count = df.shape[0]
        
        for idx, _ in enumerate(extracted_dates):
            if extracted_dates[idx] not in existing_dates:
                tmp_df = pd.read_csv(raw_urls[idx])
                tmp_df = tmp_df[~tmp_df['Province_State'].isin(excluded_states)].reset_index(drop = True)
                tmp_df = tmp_df.drop(dropped_columns, axis = 1, errors = 'ignore')
                tmp_df['Date'] = extracted_dates[idx]
                tmp_df.reset_index(inplace = True)
                tmp_df = tmp_df.rename(columns = {'index': 'Id'})
                
                df = pd.concat([df, tmp_df], ignore_index = True).drop_duplicates(keep = False)
                df = df.drop(columns=['Id'], axis = 1)
                df.reset_index(inplace = True)
                df = df.rename(columns = {'index': 'Id'})
                
        df = df.iloc[existing_row_count:]
        df.to_sql('covid_data', con = connection, if_exists = 'append', index = False)
        print('Filled in all missing records')
        return None


def database_updater():
    '''
    Update database

    Parameters:
    -----------
    None

    Returns:
    None
    '''
    
    github_url = 'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports_us'
    base_url = 'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'

    extracted_dates, raw_urls = find_all_raw_urls(github_url, base_url)
    fill_database(db.engine, extracted_dates, raw_urls)
    print('covid_data table has been updated')

    return None

# database_updater()


if __name__ == '__main__':
    print('This is the app/server setup file')