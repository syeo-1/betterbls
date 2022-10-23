from wage_data_helpers.retrieve_data import get_data
from wage_data_helpers.threaded_function_run import threaded_function
from wage_data_helpers.process_metro_nonmetro_regions import process_metro_nonmetro_code_data
from wage_data_helpers.threaded_function_run import do_something
from wage_data_helpers.retrieve_data import save_wage_dataframe_to_database

filename = 'metro_nonmetro_regions.txt'

if __name__ == '__main__':
    county_codes = process_metro_nonmetro_code_data(filename)
    # for code in county_codes:
    #     get_data(code)
    # threaded_function(get_data, county_codes)
    data_pairs = threaded_function(get_data, county_codes[:16])

    for data_pair in data_pairs:
        save_wage_dataframe_to_database(data_pair['wage_df'], data_pair['county_code'])
    
