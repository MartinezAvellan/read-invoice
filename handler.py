import codecs
import json
import boto3
import botocore

from app.model.line_ten import InvoiceLineTen
from app.model.line_twelve import InvoiceLineTwelve
from app.model.line_zero import InvoiceLineZero
from app.utils.constants import SQS_LOC_INVOICE
from app.utils.utils import send_sqs_message, get_request_id, is_str_or_dict


def handler(event, context):
    request_id = get_request_id(context)
    message = is_str_or_dict(event)
    try:
        bucket_name = message['Records'][0]['s3']['bucket']['name']
        file_name = message['Records'][0]['s3']['object']['key']
        s3 = boto3.resource('s3', region_name='sa-east-1')
        s3_object = s3.Object(bucket_name, file_name)
        line_stream = codecs.getreader('ISO-8859-1')
        count = 0
        for line in line_stream(s3_object.get()['Body']):
            msg_to_loc_queue = {}
            if line.startswith('00', 0, 2):
                line_zero = InvoiceLineZero(line)
            elif line.startswith('10', 0, 2):
                line_ten = InvoiceLineTen(line)
            elif line.startswith('12', 0, 2):
                count = count + 1
                line_twelve = InvoiceLineTwelve(line)
                msg_to_loc_queue['file_name'] = file_name
                msg_to_loc_queue['bucket_name'] = bucket_name
                msg_to_loc_queue.update(line_zero.__dict__())
                msg_to_loc_queue.update(line_ten.__dict__())
                msg_to_loc_queue.update(line_twelve.__dict__())
                msg_to_loc_queue['idtx'] = str('QT' + msg_to_loc_queue['cnpj_cedente'] + msg_to_loc_queue['data_geracao'] + str(count).zfill(11))
                send_sqs_message(request_id, file_name, SQS_LOC_INVOICE, json.dumps(msg_to_loc_queue))

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The File {} does not exist.".format(file_name))
        else:
            print("Exception {}".format(str(e)))
            raise


if __name__ == '__main__':
    eeeee = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'sa-east-1',
                          'eventTime': '2022-06-30T17:35:48.735Z', 'eventName': 'ObjectCreated:Put',
                          'userIdentity': {'principalId': 'AWS:AIDAYT3YFZIESZ6X7UGX6'},
                          'requestParameters': {'sourceIPAddress': '194.125.72.103'},
                          'responseElements': {'x-amz-request-id': 'V8MZFXX2RDZVS2RB',
                                               'x-amz-id-2': 'w97Ng5+Xg111lpjpu3Xi+kj9Dg7vaICTqIP0CInFBGvAp9ROg8jX7zABRHPf6aEK+2F8iDesS61Q4eK4zQ/s7KmApbKi3C7u'},
                          's3': {'s3SchemaVersion': '1.0', 'configurationId': 'a493f917-fcd1-4f22-acba-308a73c4af62',
                                 'bucket': {'name': 'read-invoice', 'ownerIdentity': {'principalId': 'A1H2DBHEAIKT02'},
                                            'arn': 'arn:aws:s3:::read-invoice'},
                                 'object': {'key': 'EcosyInstdePagamentoSA29042022.txt', 'size': 429320,
                                            'eTag': 'dc20d6d0fa1179c8cedfc97b8f085a0e',
                                            'sequencer': '0062BDDEF4A604F717'}}}]}

    handler(eeeee, None)
