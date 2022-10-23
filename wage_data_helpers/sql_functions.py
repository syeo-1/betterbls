# create functions to write to the database the initial data

import sqlite3

conn = sqlite3.connect('/mnt/c/Users/seans/OneDrive/Desktop/better_bls_flask/wage_stats.db')
cursor = conn.cursor()


def create_county_wage_table_if_not_exists(county_code):
    create_table_sql = (
        f'CREATE TABLE IF NOT EXISTS county_{county_code} '
        '('
        'occupation_code varchar(255),'
        'occupation_title varchar(255),'
        'level varchar(255), '
        'employment int, '
        'employment_rse double, '
        'employment_per_1000_jobs double, '
        'location_quotient double, '
        'median_hourly_wage double, '
        'mean_hourly_wage double'
        ');'
    )

    cursor.execute(create_table_sql)

    # save changes to database
    conn.commit()
    
    # print(create_table_sql)

def drop_table(county_code):
    drop_sql = f'DROP TABLE county_{county_code}'

    cursor.execute(drop_sql)

    conn.commit()


# make a table to store county codes and the full actual county name!
def create_county_name_table():
    pass

def insert_dataframe_into_db(county_code, dataframe):
    pass


if __name__ == "__main__":
    create_tables(42660)