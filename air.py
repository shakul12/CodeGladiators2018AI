import requests, json
import pandas as pd
import numpy as np
from datetime import datetime
import glob
import os

cwd = os.getcwd()
for file_name in glob.glob(cwd +'/*.csv'):
	print(file_name)

	
	res = pd.read_csv(file_name)
	print(len(res))
	# print(res.iloc[0,])

	# for i in range(len(res)):
	# 	print(res.iloc[i,])

	# print(res.iloc[0,4][:10])
	# print(res.iloc[0,4][11:19])
	# print(res.iloc[0,4])
	# for i in range(len(res)):
	# 	print(i)
	# 	date = datetime.strptime(res.iloc[i,4], '%Y-%m-%dT%H:%M:%S-05:00')
	# 	# print(date)
	# 	print(datetime.strftime(date, '%d-%m-%Y %H:%M:%S'))

	headers = {
		'content-type': 'application/json'
	}
	for i in range(len(res)):
		try:
			date = res.iloc[i,4][:-6]
			date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
			data = json.dumps({
				'message': 'weather data',
				'data': 'weather',
				'date': datetime.strftime(date, '%d-%m-%Y %H:%M:%S'),
				'location': res.iloc[i,0],
				'city': res.iloc[i,1],
				'country': res.iloc[i,2],
				'parameter': res.iloc[i,5],
				'value': res.iloc[i,6],
				'location': '{},{}'.format(round(res.iloc[i,8], 2), round(res.iloc[i,9], 2))
			})
			p = requests.post('http://35.196.84.204:12201/gelf', headers=headers, data=data)
			print(p, i)
			print(data)
		except Exception as e:
			print(e)
			print(i)
