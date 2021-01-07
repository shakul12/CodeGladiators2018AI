from pandasticsearch import DataFrame
import json


def build_response(response):
    return {
    "isBase64Encoded": False,
    "statusCode": 200,
    "headers": { "my_header": "my_value"},
    "body": json.dumps(response)
}

def lambda_handler(event, context):
	df = DataFrame.from_es(url='http://35.196.84.204:9200', index='weatherdata-india_0',compat=5)
	response_dict={}
	input_json=event['body']
	parameters=input_json['parameter']
	parameters=parameters.lower()
	city=input_json['city']
	response=df.filter((df.city==city)&(df.parameter==parameters)).select('value').sort(df.timestamp.desc).collect()
	response=response[0]['value']
	response_dict['%s value for %s'% (parameters,city)]=response
	return build_response(response_dict)