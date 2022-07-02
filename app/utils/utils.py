import json
import uuid

import boto3


def get_request_id(context):
    try:
        if context and context.aws_request_id:
            return context.aws_request_id
        else:
            return uuid.uuid1()
    except Exception:
        return uuid.uuid1()


def is_str_or_dict(message):
    if type(message) is str:
        return json.loads(message)
    elif type(message) is dict:
        return message


def send_sqs_message(request_id, file_name, sqs_name, message):
    try:
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName=sqs_name)
        response = queue.send_message(MessageBody=message, MessageAttributes={
            'request_id': {
                'DataType': 'String',
                'StringValue': str(request_id)
            }
        })
        sqs_message = "Send to SQS [SQS_LOC_INVOICE] {}. HTTPStatusCode: {} - MessageId: {}".format(
            sqs_name,
            response.get('ResponseMetadata')["HTTPStatusCode"],
            response.get('MessageId')
        )
        print('{}|{}| result: {}'.format(request_id, file_name, sqs_message))
    except Exception as e:
        raise Exception('send_sqs_message({}, {}): {}'.format(sqs_name, message, e))
