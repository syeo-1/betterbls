# a script to scrape data from bls for a particular metro/nonmetro region using beautiful soup

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from tabulate import tabulate
import sqlite3
import re

conn = sqlite3.connect('/mnt/c/Users/seans/OneDrive/Desktop/better_bls_flask/wage_stats.db')

seattle_code = 42660
number_code_regex = r"\(\d\)"

def process_employment(employment):
    return int(employment.replace(',', ''))

def process_employment_rse(employment_rse):
    return float(employment_rse[:-1])

def process_employment_per_1000(employment_per_1000):
    return float(employment_per_1000)

def process_location_quotient(location_quotient):
    return float(location_quotient)

def process_median_hourly_wage(median_hourly_wage):
    return float(median_hourly_wage[1:])

def process_mean_hourly_wage(mean_hourly_wage):
    return float(mean_hourly_wage[1:])

def process_annual_mean_wage(annual_mean_wage):
    return int(annual_mean_wage[1:].replace(',', ''))

def process_mean_wage_rse(mean_wage_rse):
    return float(mean_wage_rse[:-1])


# retrieves wage data for a metro/non-metro area and creates a dataframe from the table on the website
def get_data(code):

    # download contents of the page
    url = f'https://www.bls.gov/oes/current/oes_{str(code)}.htm'

    try:
        print(f'getting data for {code} county code')
        site_html = requests.get(url).text
        # print('REQUEST COMPLETED?!')
    except:
        print(f'was not able to retrieve webpage with code: {code}')
        return
    
    # print('HERE???')


    # create beautifulsoup object
    soup = BeautifulSoup(site_html, 'html.parser')

    # find the wage data table in the website
    wage_table = soup.find('table', class_ = 'sortable_datatable')

    # define dataframe for wage data
    wage_df = pd.DataFrame(columns=[
        'occupation_code',
        'occupation_title',
        'level',         
        'employment',    
        'employment_rse_percent',
        'employment_per_1000_jobs',
        'location_quotient',
        'median_hourly_wage_usd',
        'mean_hourly_wage_usd',
        'annual_mean_wage_usd',
        'mean_wage_rse_percent'
    ])

    # process the data and place into the dataframe
    for row in wage_table.tbody.find_all('tr'):
        column_data = row.find_all('td')

        occupation_code = column_data[0].text
        occupation_title = column_data[1].text
        level = column_data[2].text

        # only these have possibility of matching the regex
        employment = np.nan if re.match(number_code_regex, column_data[3].text) else process_employment(column_data[3].text)
        employment_rse = np.nan if re.match(number_code_regex, column_data[4].text) else process_employment_rse(column_data[4].text)
        employment_per_1000 = np.nan if re.match(number_code_regex, column_data[5].text) else process_employment_per_1000(column_data[5].text)
        location_quotient = np.nan if re.match(number_code_regex, column_data[6].text) else process_location_quotient(column_data[6].text)
        median_hourly_wage = np.nan if re.match(number_code_regex, column_data[7].text) else process_median_hourly_wage(column_data[7].text)
        mean_hourly_wage = np.nan if re.match(number_code_regex, column_data[8].text) else process_mean_hourly_wage(column_data[8].text)
        annual_mean_wage = np.nan if re.match(number_code_regex, column_data[9].text) else process_annual_mean_wage(column_data[9].text)
        mean_wage_rse = np.nan if re.match(number_code_regex, column_data[10].text) else process_mean_wage_rse(column_data[10].text)

        wage_df = wage_df.append({
            'occupation_code': occupation_code,
            'occupation_title': occupation_title,
            'level': level,
            'employment': employment,
            'employment_rse_percent': employment_rse,
            'employment_per_1000_jobs': employment_per_1000,
            'location_quotient': location_quotient,
            'median_hourly_wage_usd': median_hourly_wage,
            'mean_hourly_wage_usd': mean_hourly_wage,
            'annual_mean_wage_usd': annual_mean_wage,
            'mean_wage_rse_percent': mean_wage_rse,
        }, ignore_index=True)

    # wage_df.to_csv('wage_data.csv', index=False)
    # print('GET TO HERE?')
    # try:
    #     wage_df.to_sql(name=f'county_{code}', con=conn, if_exists='replace', )
    # except ValueError:
    #     print(f'exception occured: {ValueError}')
    print(f'COMPLETED RETRIEVAL FOR COUNTY CODE: {code}')
    return {
        'wage_df': wage_df,
        'county_code': code
    }


def save_wage_dataframe_to_database(wage_dataframe, county_code):
    wage_dataframe.to_sql(name=f'county_{county_code}', con=conn, if_exists='replace', )

if __name__ == "__main__":
    wage_dataframe = get_data(seattle_code)
    save_wage_dataframe_to_database(wage_dataframe, seattle_code)