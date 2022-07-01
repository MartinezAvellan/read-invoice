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


def send_sqs_message(request_id, sqs_name, message):
    try:
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName=sqs_name)
        return queue.send_message(MessageBody=message, MessageAttributes={
            'request_id': {
                'DataType': 'String',
                'StringValue': request_id
            }
        })
    except Exception as e:
        raise Exception('send_sqs_message({}, {}): {}'.format(sqs_name, message, e))
