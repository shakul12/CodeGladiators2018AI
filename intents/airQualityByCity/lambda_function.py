import json
from pandasticsearch import DataFrame

def build_response(message):
    return {
    "isBase64Encoded": False,
    "statusCode": 200,
    "headers": { "my_header": "my_value"},
    "body": json.dumps(message)a
}

def lambda_handler(event, context):
	df = DataFrame.from_es(url='http://35.196.84.204:9200', index='weatherdata-india_0',compat=5)
	response_dict={}
	input_json=event['body']
	city=input_json['city']
	response_dict={}
	parameters=['so2','pm10','pm25','no2','o3','co']
	for para in parameters:
		resp=df.filter((df.city==city)&(df.parameter==para)).select('value','date').sort(df.timestamp.desc).collect()
		resp_val=resp[0]['value']
		resp_date=resp[0]['date']
		response_dict["%s value on %s"%(para,resp_date)]=resp_val
	return build_response(response_dict)