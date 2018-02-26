The contents of this directory are meant to be run in an AWS Lambda function with the following config:

- A backbone SQS queue (as described in top level readme file) set up
- Python 3.6 as the runtime
- The `AmazonSQSFullAccess` policy attached to the executing role
- Name of aforementioned backbone SQS queue set to the `UTILITY_Q_NAME` environment variable
