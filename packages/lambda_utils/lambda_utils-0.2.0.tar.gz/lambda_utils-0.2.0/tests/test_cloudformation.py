import json
from mock import patch
from lambda_utils import cloudformation as module
from lambda_utils.cloudformation import Cloudformation, send_signal
import pytest

@pytest.fixture()
def stack_arn(region, account_id, stack_name):
    'arn:aws:cloudformation:{region}:{account_id}:stack/{stack_name}'.format(
        region=region,
        account_id=account_id,
        stack_name=stack_name
    )


@pytest.fixture()
def stack_id(stack_arn, unique_id):
    return "{stack_arn}/{unique_id}".format(stack_arn=stack_arn, unique_id=unique_id)


@pytest.fixture(params=['Create', 'Update', 'Delete'])
def request_type(request):
    return request.param


@pytest.fixture()
def logical_resource_id(random_string):
    return "LogicalResourceId{random_string}".format(random_string=random_string)


@pytest.fixture()
def custom_resource_event(request, region, account_id, stack_id, stack_name, request_type, lambda_arn, lambda_name, unique_id, logical_resource_id):
    return {
        'StackId': stack_id,
        'ResponseURL': 'https://cloudformation-custom-resource-response-euwest1.s3-eu-west-1.amazonaws.com/{stack_id}'.format(stack_id=stack_id),
        'RequestType': request_type,
        'ServiceToken': lambda_arn,
        'ResourceType': 'Custom::{lambda_name}'.format(lambda_name=lambda_name),
        'PhysicalResourceId': '{stack_name}-{logical_resource_id}'.format(stack_name=stack_name, logical_resource_id=logical_resource_id),
        'RequestId': unique_id,
        'LogicalResourceId': logical_resource_id,
        'ResourceProperties': {

        }

    }


@pytest.fixture(params=['SNS', 'Lambda'])
def event(request, custom_resource_event):
    if request.param == 'SNS':
        return {
            'Records': [{
                'EventVersion': '1.0',
                'EventSubscriptionArn': 'arn:aws:sns:eu-west-1:211099707286:triggerInstanceHealthCheck:803d4d60-e718-44f5-9b5d-9bfe99e4e032',
                'EventSource': 'aws:sns',
                'Sns': {
                    'SignatureVersion': '1',
                    'Timestamp': '2017-02-10T14:24:24.208Z',
                    'Signature': 'dLPVXinxVg/Hut0x3n8MvEd9tIsLjeSiZOoQXJpaFtSb61CSNSAZ4lcCn2fUAJVbFFlbHkKVn+iR2RKqD35Xx6YZFp8oBBsjW9ItUONacNgCvoqNbFcEb1g0vl5ryvRPMS1xmRi1iy5M4MHm8KdsFdTUDQ18Idbl5NTmVJ/TAH50NZooGVa3iA/9MUDYTt59o7c3rie4P0gE9DgG0r4zXbCnZdXgYAuVCu4IaeP44Ve5MwtX4rFnqBkPQzyaIiDSXK/qZGNMiUcgRkcbp7X4IP0iPWIekAIKH0VuomeJMjtjFU7Gzt1oz5vhWTv+Q7m2hSvK7xpMgdRCX8qEEIHXUw==',
                    'SigningCertUrl': 'https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-b95095beb82e8f6a046b3aafc7f4149a.pem',
                    'MessageId': '11fe9630-84ae-5327-b49b-c7274bf66063',
                    'Message': json.dumps(custom_resource_event),
                    'MessageAttributes': {},
                    'Type': 'Notification',
                    'UnsubscribeUrl': 'https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-1:211099707286:triggerInstanceHealthCheck:803d4d60-e718-44f5-9b5d-9bfe99e4e032',
                    'TopicArn': 'arn:aws:sns:eu-west-1:211099707286:triggerInstanceHealthCheck',
                    'Subject': 'AWS CloudFormation custom resource request'
                }
            }]
        }

    return custom_resource_event


@patch.object(module, 'send_signal')
def test_function_response(send_signal_mock, event, custom_resource_event, context):
    @Cloudformation()
    def function(event, context):
        return event

    function(event, context)

    send_signal_mock.assert_called_once_with(custom_resource_event, 'SUCCESS', None, custom_resource_event)


@patch.object(module, 'send_signal')
def test_exception_raised(send_signal_mock, event, custom_resource_event, context, random_string):
    @Cloudformation()
    def function(event, context):
        raise Exception(random_string)

    with pytest.raises(Exception):
        function(event, context)

    send_signal_mock.assert_called_once_with(custom_resource_event, 'FAILED', random_string, None)


@patch.object(module.urllib2, 'build_opener')
def test_send_signal(build_opener, custom_resource_event, random_string):
    send_signal(custom_resource_event, 'SUCCESS', random_string)

    build_opener.assert_called_once_with(module.urllib2.HTTPHandler)
    build_opener.return_value.open.assert_called_once()

@patch.object(module.urllib2, 'build_opener')
def test_send_signal_non_serializable_reason(build_opener, custom_resource_event, random_string):
    send_signal(custom_resource_event, 'SUCCESS', object())

    build_opener.assert_called_once_with(module.urllib2.HTTPHandler)
    build_opener.return_value.open.assert_called_once()
