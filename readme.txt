Subscription based API Creation
------------------------------------------------
* build api on API Gateway
* make a lambda function to provide json data and upload the necessary dependencies in a zip file
* give Lambda Function in the integration type of api gateway and provide the name of lambda function created in previous step
* generate user plans, api keys and attach with the api's


Testing of API's
------------------------------------------------
* open postman
* choose post request from dropdown
* in the url, mention the api url (e.g https://cpfze7wuoc.execute-api.us-east-1.amazonaws.com/v1/airQualityByCity)
* attach the json with the required parameters in the body (e.g {"city": "delhi"})
* provide the api key in headers, and set "content-type" as "application/json"
* send the request