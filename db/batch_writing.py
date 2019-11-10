import boto3
import os
import json
import time

dynamodb = boto3.resource('dynamodb')

my_table_name = os.environ['MY_TABLE_NAME']
table = dynamodb.Table(my_table_name)

with table.batch_writer() as batch:
    message1 = {
            'app_id': 'my-app',
            'created_at': int(time.time()),
            'message': 'Lo ultimo que se pierde es la barriga, señor Esperanza.',
            'active': True,
        }
    batch.put_item(Item=message1)
    print("Message inserted: " + json.dumps(message1))
    message2 = {
            'app_id': 'my-app',
            'created_at': int(time.time()+1),
            'message': 'Es que no me tienen paciencia.',
            'active': True,
        }
    batch.put_item(Item=message2)
    print("Message inserted: " + json.dumps(message2))
    message3 = {
            'app_id': 'my-app',
            'created_at': int(time.time()+2),
            'message': 'Bueno, pero no se enoje.',
            'active': True,
        }
    batch.put_item(Item=message3)
    print("Message inserted: " + json.dumps(message3))
    message4 = {
            'app_id': 'my-app',
            'created_at': int(time.time()+3),
            'message': '¡Pues al cabo que ni queria!',
            'active': True,
        }
    batch.put_item(Item=message4)
    print("Message inserted: " + json.dumps(message4))
    message5 = {
            'app_id': 'my-app',
            'created_at': int(time.time()+4),
            'message': 'Ahora si te descalabro los cachetes.',
            'active': True,
        }
    batch.put_item(Item=message5)
    print("Message inserted: " + json.dumps(message5))
    message6 = {
            'app_id': 'my-app',
            'created_at': int(time.time()+5),
            'message': '¡Tenia que ser el Chavo del 8!',
            'active': True,
        }
    batch.put_item(Item=message6)
    print("Message inserted: " + json.dumps(message6))
