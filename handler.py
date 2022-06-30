import json


def handler(event, context):
    print("COMECOU")
    print("event: ", str(event))
    print("context: ", str(context))
    print("TERMINOU")
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
        "context": context
    }

    return {"statusCode": 200, "body": json.dumps(body)}
