from wage_data_helpers.retrieve_data import get_data
from wage_data_helpers.threaded_function_run import threaded_function
from wage_data_helpers.process_metro_nonmetro_regions import process_metro_nonmetro_code_data
from wage_data_helpers.threaded_function_run import do_something
from wage_data_helpers.retrieve_data import save_wage_dataframe_to_database
from wage_data_helpers.retrieve_data import reset_county_wage_table

filename = 'metro_nonmetro_regions.txt'

# CURRENT RUNTIME IS about 25 minutes
if __name__ == '__main__':
    county_codes = process_metro_nonmetro_code_data(filename)

    # test = list(set([
    #     '33860',
    #     '19300',
    #     '0100004',
    #     '13820',
    #     '13820',
    #     '0100004',
    #     '0100004',
    #     '11500',
    #     '0100002',
    #     '0100002',
    #     '13820',
    #     '0100003',
    #     '0100003',
    #     '0100002',
    #     '0100002',
    #     '0100004',
    #     '22520',
    #     '0100003',
    #     '0100002',
    #     '0100004',
    #     '0100004',
    #     '0100001',
    #     '0100004',
    #     '0100003',
    #     '0100002',
    #     '33860',
    #     '0100003',
    #     '23460',
    #     '0100001',
    #     '0100001',
    #     '20020',
    #     '0100003',
    #     '46220',
    #     '20020',
    #     '20020',
    #     '0100002',
    #     '13820',
    #     '0100001',
    #     '22520',
    #     '19460',
    #     '12220',
    #     '26620',
    #     '33860',
    #     '0100004',
    #     '26620',
    #     '0100003',
    #     '0100001',
    #     '0100002',
    #     '33660',
    #     '0100003',
    # ]))
    wage_dataframes = threaded_function(get_data, county_codes)
    # data_pairs = threaded_function(get_data, test)

    # drop the table if it already exists in the database
    reset_county_wage_table()

    for wage_dataframe in wage_dataframes:
        save_wage_dataframe_to_database(wage_dataframe)
    
