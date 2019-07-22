import boto3
import os

dynamodb = boto3.resource('dynamodb')

my_table_name = os.environ['MY_TABLE_NAME']
table = dynamodb.Table(my_table_name)

with table.batch_writer() as batch:
    batch.put_item(
        Item={
            'app_id': 'my-app',
            'created_at': 1561397870,
            'message': 'This is a message 6.',
            'active': True,
        }
    )
    batch.put_item(
        Item={
            'app_id': 'my-app',
            'created_at': 1558719470,
            'message': 'This is a message 5.',
            'active': True,
        }
    )
    batch.put_item(
        Item={
            'app_id': 'my-app',
            'created_at': 1556127470,
            'message': 'This is a message 4.',
            'active': True,
        }
    )
    batch.put_item(
        Item={
            'app_id': 'my-app',
            'created_at': 1553449070,
            'message': 'This is a message 3.',
            'active': True,
        }
    )
    batch.put_item(
        Item={
            'app_id': 'my-app',
            'created_at': 1551029870,
            'message': 'This is a message 2.',
            'active': True,
        }
    )
    batch.put_item(
        Item={
            'app_id': 'my-app',
            'created_at': 1548351470,
            'message': 'This is a message 1.',
            'active': True,
        }
    )

