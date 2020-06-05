import pandas as pd
from collections import Counter, defaultdict
from datetime import timedelta

from utils import *

contacts_file = 'SourceData/big_data_contracts.json'
persons_file = 'SourceData/big_data_persons.json'

def get_contacts_over_5min(data: list) -> list:
	contacts = []
	for row in data:
		delta = convert_to_datetime(row['To'])-convert_to_datetime(row['From'])
		if delta.seconds >= 300:
			contacts.append(row)
	return contacts

def get_id_contacts_total(data: list) -> dict:
	id_total = Counter()
	for row in data:
		id_total[row['Member1_ID']] += 1
		id_total[row['Member2_ID']] += 1
	return id_total

def _convert_to_excel_format(data: list, header: list) -> list:
	to_excel = []
	for row in data:
		to_excel.append({header[0]: row[0], header[1]: row[1]})
	return to_excel

def get_id_contacts_duration(data: list) -> dict:
	id_duration = defaultdict(timedelta)
	for row in data:
		delta = convert_to_datetime(row['To'])-convert_to_datetime(row['From'])
		id_duration[row['Member1_ID']] += delta
		id_duration[row['Member2_ID']] += delta
	return id_duration

def get_id_contacts_list(data: list) -> dict:
	id_contacts_list = defaultdict(list)
	for row in data:
		id_contacts_list[row['Member1_ID']].append(convert_to_datetime(row['From']))
		id_contacts_list[row['Member2_ID']].append(convert_to_datetime(row['From']))
	for contacts_list in id_contacts_list.values():
		contacts_list.sort()
	return id_contacts_list

def _get_id_intervals_list(data: dict) ->  dict:
	id_intervals_list = defaultdict(list)
	for member_id, contacts_list in data.items():
		for contact1,contact2 in (zip(contacts_list[:-1],contacts_list[1:])):
			id_intervals_list[member_id].append(contact2-contact1)
	return id_intervals_list

def _get_id_age_mapping(data: list) -> dict:
	id_age_mapping = {}
	for row in data:
		id_age_mapping[row['ID']] = row['Age']
	return id_age_mapping

def _get_key_average_value(data: dict) -> dict:
	key_average_value = {}
	for key, values_list in data.items():
		key_average_value[key] = _get_average_value(values_list)
	return key_average_value

def _get_average_value(data: list) -> timedelta:
	data_total = timedelta()
	for value in data:
		data_total += value
	return data_total/len(data)

def _get_age_intervals_list(mapping_data: dict, data: dict) -> dict:
	age_contacts_frequency_list = defaultdict(list)
	for memeber_id, frequency in data.items():
		age_contacts_frequency_list[mapping_data[memeber_id]].append(frequency)
	return age_contacts_frequency_list

if __name__ == '__main__':
	contacts_data = read_data_from_json(contacts_file)
	persons_data = read_data_from_json(persons_file)
	to_excel = {}
	
#2.4
	contacts_over_5min = get_contacts_over_5min(contacts_data)
	if contacts_over_5min:
		id_contacts_total = get_id_contacts_total(contacts_over_5min)
		id_contacts_total = sorted(id_contacts_total.items(), key=lambda x: x[1])
		id_contacts_total = _convert_to_excel_format(
			data = id_contacts_total,
			header = ['name', 'contacts total']
			)
		to_excel['2.4 contacts total'] = id_contacts_total

#2.5
	id_contacts_duration = get_id_contacts_duration(contacts_data)
	id_contacts_duration = sorted(id_contacts_duration.items(), key=lambda x: x[1])
	id_contacts_duration = [(row[0], str(row[1])) for row in id_contacts_duration]
	id_contacts_duration = _convert_to_excel_format(
		data = id_contacts_duration,
		header = ['name', 'contacts duration total']
		)
	to_excel['2.5 contacts duration'] = id_contacts_duration

#2.6
	if contacts_over_5min:
		id_contacts_list = get_id_contacts_list(contacts_over_5min)
		id_intervals_list = _get_id_intervals_list(id_contacts_list)
		id_average_interval = _get_key_average_value(id_intervals_list)
		id_age_mapping = _get_id_age_mapping(persons_data)
		age_intervals_list = _get_age_intervals_list(id_age_mapping, id_average_interval)
		age_average_interval = _get_key_average_value(age_intervals_list)
		age_average_interval = sorted(age_average_interval.items(), key=lambda x: x[1])
		age_average_interval = [(row[0], str(row[1]).split('.')[0]) for row in age_average_interval]
		age_average_interval = _convert_to_excel_format(
			data = age_average_interval,
			header = ['age group', 'average interval between contacts']
			)
		to_excel['2.6 contacts frequency'] = age_average_interval

	write_data_to_excel(to_excel, 'extended_output.xlsx')