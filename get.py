import json
import boto3

client = boto3.client('dynamodb')
feedbacks_table = 'proj_feedbacks'

def lambda_handler(event, context):
    scan = client.scan(
        TableName=feedbacks_table)
    
    items = scan['Items']
    
    response = []
    
    for item in items:
        feedback = deep_clean_field(item)
        response.append(feedback)
    
    return {
        'N° de Items': len(response),
        'Items': response
    }

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