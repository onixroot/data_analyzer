import json
import re
import pandas as pd
from datetime import datetime

def read_data_from_json(file: str) -> dict:
	with open(file, 'r', encoding='utf-8') as f:
		return json.load(f)

def convert_to_datetime(time: str) -> datetime:
	match = re.search('(\d*).(\d*).(\d{4})\s(\d*):(\d*):(\d*)', time)
	return datetime(*map(int, match.group(3,2,1,4,5,6)))

def write_data_to_excel(data: dict, name: str) -> None:
	writer = pd.ExcelWriter(name, engine='xlsxwriter')
	for key, value in data.items():
		df = pd.DataFrame(value)
		df.to_excel(writer, key, index=False)
	writer.save()	
