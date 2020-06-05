import json
import pandas as pd
import re

from utils import *

small_data_file = 'SourceData/small_data_persons.json'
big_data_file = 'SourceData/big_data_persons.json'

def find_namesakes(data1: list, data2: list) -> list:
	namesakes = []
	for row1 in data1:
		surname1 = row1['Name'].split()[0]
		age1 = int(row1['Age'])
		for row2 in data2:
			surname2 = row2['Name'].split()[0]
			age2 = int(row2['Age'])
			if surname1==surname2 and abs(age1-age2)==10 and (row2, row1) not in namesakes:
				namesakes.append((row1, row2))
	return [{'namesakes_1': row[0], 'namesakes_2': row[1]} for row in namesakes]

def	find_diff_by_surname(data1: list, data2: list) -> list:
	diff_by_surname = []
	for row1 in data1:
		surname1 = row1['Name'].split()[0]
		surnames2_list = [row2['Name'].split()[0] for row2 in data2]
		if surname1 not in surnames2_list:
			diff_by_surname.append(row1)
	return diff_by_surname

def find_eng_letters_in_names(data: list) -> list:
	names = []
	for row in data:
		if re.search('[a-zA-Z]', row['Name']):
			names.append(row)
	return names

if __name__ == '__main__':
	to_excel = {}

#1.3
	small_data = read_data_from_json(small_data_file)
	big_data = read_data_from_json(big_data_file)
	to_excel['1.4 small'] = small_data
	to_excel['1.4 big'] = big_data

#1.4
	small_data.sort(key=lambda x: x['Name'].split()[0])
	big_data.sort(key=lambda x: x['Name'].split()[1])

#1.5
	diff_by_surname = find_diff_by_surname(small_data, big_data)
	to_excel['1.5 small vs big'] = diff_by_surname
	
#1.6
	namesakes_small = find_namesakes(small_data, small_data)
	namesakes_big = find_namesakes(big_data, big_data)
	namesakes_small_big = find_namesakes(small_data, big_data)
	to_excel['1.6 small vs small'] = namesakes_small
	to_excel['1.6 big vs big'] = namesakes_big
	to_excel['1.6 small vs big'] = namesakes_small_big
	
#1.7
	eng_letters_small = find_eng_letters_in_names(small_data)
	eng_letters_big = find_eng_letters_in_names(big_data)
	to_excel['1.7 small'] = eng_letters_small
	to_excel['1.7 big'] = eng_letters_big

	write_data_to_excel(to_excel, 'basic_output.xlsx')