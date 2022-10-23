# process the metro/non-metro regions into a set
# make sure things aren't repeated

# filename = 'metro_nonmetro_regions.txt'

def process_metro_nonmetro_code_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        codes = list(set([line.rstrip() for line in lines]))
        return codes

# print(process_metro_nonmetro_code_data())