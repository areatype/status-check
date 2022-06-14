# HTTP Status Checker with Database and SMS Integration

App to check a website's HTTP/URL status and record the results.

If an HTTP/DNS error occurs, a text message is sent to the owner.


## Integrations

[AWS DynamoDB](https://aws.amazon.com/dynamodb/)
  * to store URL and client data
  * to store results from the HTTP check


[Twilio](https://www.twilio.com/)
  * To send text with any errors to owner 

## Variables & Data
- Variables are stored in a .env file and retrieved using dotenv
- Sample .env file is included
- Data structure is shown in data-example.json

## To Do
- Convert to a Flask app
- Add User accounts
- Add CRUD forms for Profile and Websites
- Create stats graphs with D3