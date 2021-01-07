import logging
import requests
import json
import random

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

precaution_steps = ['Please conserve energy - at home, at work, everywhere to make better environment. :)', 'Please use carpool, public transportation, bike, or walk whenever possible. It makes big difference. :)', 'Keep car, boat, and other engines properly tuned. It causes less pollution. :)', 'Be sure your tires are properly inflated to save fuel and reduce air pollution.', 'Consider using gas logs instead of wood to help the environment.', 'Combine errands and reduce trips. Walk to errands when possible.']
greet = ['hey Sid.', 'hello, how may i help you.', 'hi, i am Polly your air pollution info bot. you can ask me air quality status of a city or of a component (like so2, pm25 etc).']
bye_res = ['bye :)', 'bubyee, let me know if you want something else.', 'thanks bye.']

def build_response(message, session_attributes = {}):
	logger.debug('Close. Message: {}\nSession attributes: {}'.format(message, session_attributes))
	return {
		'sessionAttributes': session_attributes,
		'dialogAction':{
			'type':'Close',
			'fulfillmentState':'Fulfilled',
			'message':{
				'contentType':'PlainText',
				'content':message
			}
		}
	}


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
	logger.debug('ElicitSlot. intentName: {}, slots: {}, slotToElicit: {} , message: {}'.format(intent_name, slots, slot_to_elicit, message))
	return {
		'sessionAttributes': session_attributes,
		'dialogAction': {
			'type': 'ElicitSlot',
			'intentName': intent_name,
			'slots': slots,
			'slotToElicit': slot_to_elicit,
			'message':{
				'contentType':'PlainText',
				'content':message
			}
		}
	}


def delegate(session_attributes, slots):
	logger.debug('Delegate. slots: {}'.format(slots))
	return {
		'sessionAttributes': session_attributes,
		'dialogAction': {
			'type': 'Delegate',
			'slots': slots
		}
	}

def confirm_intent(session_attributes, intent_name, slots, message):
	logger.debug('confirm intent: {} {} {} {}'.format(session_attributes, intent_name, slots, message))
	return {
		'sessionAttributes': session_attributes,
		'dialogAction': {
			'type': 'ConfirmIntent',
			'intentName': intent_name,
			'slots': slots,
			'message': {
				'contentType': 'PlainText',
				'content': message
			}
		}
	}
	

def error_message(message_content):
	return {
		'contentType': 'PlainText', 
		'content': message_content
	}


def build_validation_result(is_valid, violated_slot, message_content):
	if message_content == None:
		return {
			'isValid': is_valid,
			'violatedSlot': violated_slot
		}
	return {
		'isValid': is_valid,
		'violatedSlot': violated_slot,
		'message': message_content
	}


def airQualityByComponent(intent_request):
	source = intent_request['invocationSource']
	output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
	slots = intent_request['currentIntent']['slots']
	city = slots['city']
	logger.debug(city)
	parameter = slots['component']
	try:
		res = requests.post('https://cpfze7wuoc.execute-api.us-east-1.amazonaws.com/v1/airQualityByComponent', data=json.dumps({'city':city, 'parameter':parameter}))
		logger.debug(res.json())
		res = json.loads(res.json()['body'])
	except Exception as e:
		logger.debug(e)
		return build_response('Sorry, something went wrong.')
	logger.debug(res)
	logger.debug(type(res))
	quantity = res['value']
	logger.debug(quantity)
	if parameter == 'pm25':
		if quantity <= 60:
			reply = 'safe'
		elif quantity > 60 and quantity <= 90:
			reply = 'moderate'
		elif quantity > 90 and quantity <= 120:
			reply = 'poor'
		elif quantity < 120 and quantity <= 250:
			reply = 'very poor'
		else:
			reply = 'hazardous'
	elif parameter == 'pm10':
		if quantity <= 100:
			reply = 'safe'
		elif quantity > 100 and quantity <= 250:
			reply = 'moderate'
		elif quantity > 250 and quantity <= 350:
			reply = 'poor'
		elif quantity < 350 and quantity <= 430:
			reply = 'very poor'
		else:
			reply = 'hazardous'
	else:
		reply = 'ok'
	return build_response('Air quality is {} in {}. {} value {}.\n{}'.format(reply, city.title(), parameter, quantity, random.choice(precaution_steps)))

def airQualityByCity(intent_request):
	source = intent_request['invocationSource']
	output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
	slots = intent_request['currentIntent']['slots']
	city = slots['city']
	logger.debug(city)
	try:
		res = requests.post('https://cpfze7wuoc.execute-api.us-east-1.amazonaws.com/v1/airQualityByCity', data=json.dumps({'city':city}))
		logger.debug(res.json())
		res = json.loads(res.json()['body'])
	except Exception as e:
		logger.debug(e)
		return build_response('Sorry, something went wrong.')
	logger.debug(res)
	response = 'Here is the summary of air quanliy of {}:\n'.format(city.title())
	for k,v in res.items():
		response += '{} : {}\n'.format(k,v)
	response += random.choice(precaution_steps)
	return build_response(response)

def greeting(intent_request):
	return build_response(random.choice(greet))

def bye(intent_request):
	return build_response('{}\n{}'.format(random.choice(bye_res), random.choice(precaution_steps)))

def airPollutionReduction(intent_request):
	res = ''
	for item in precaution_steps:
		res += item
		res += '\n'
	return build_response(res)


def dispatch(intent_request):
	logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))
	intent_name = intent_request['currentIntent']['name']
	if intent_name == 'airQualityByCity':
		return airQualityByCity(intent_request)
	if intent_name == 'airQualityByComponent':
		return airQualityByComponent(intent_request)
	if intent_name == 'airQualityPredictionByCity':
		return build_response(intent_request)
	if intent_name == 'greeting':
		return greeting(intent_request)
	if intent_name == 'bye':
		return bye(intent_request)
	if intent_name == 'airPollutionReduction':
		return airPollutionReduction(intent_request)
	raise Exception('Intent with name ' + intent_name + ' not supported')


def lambda_handler(event, context):
	logger.debug(event)
	logger.debug('event.bot.name={}'.format(event['bot']['name']))
	return dispatch(event)