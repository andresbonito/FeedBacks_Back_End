import json
import boto3

client = boto3.client('dynamodb')
feedbacks_table = 'proj_feedbacks'

def lambda_handler(event, context):
    print(f'Evento: {event}')
    
    id = event['id']

    response = get_feedbacks(id)
    print(response)
    
    
    feedbacks_ids = []
    
    for item in response:
        new_response = deep_clean_field(item)
        feedbacks_ids.append(new_response)
    
    print(feedbacks_ids)
    
    
    return feedbacks_ids[0]


def get_feedbacks(id):
    response = client.query(
        TableName=feedbacks_table,
        KeyConditionExpression='#id = :id',
        ExpressionAttributeNames={
            '#id': 'id'
        },
        ExpressionAttributeValues={
            ':id': {
                'S': id
            }
        }
    )
    
    items = response['Items']
    
    return items
    
def deep_clean_field(raw_dict: dict):
    response = {}

    for key, value in raw_dict.items():
        if key in ['S', 'N', 'B', 'L', 'NS', 'SS', 'BS', 'BOOL', ]:
            return value
        if key in ['NULL', ]:
            return None
        elif key in ['M', ]:
            return deep_clean_field(value)
        else:
            response.update({key: deep_clean_field(value)})

    return response