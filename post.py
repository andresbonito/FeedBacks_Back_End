import json
import boto3

client = boto3.client('dynamodb')
feedbacks_table = 'proj_feedbacks'

def lambda_handler(event, context):
    print(f'Evento: {event}')

    feedback_id = event['feedback_id']
    coment = event['comentario']
    rating = event['classificacao']
    info = event['informacoes_produto']
    print(f'FeedbackId: {feedback_id}')
    print(f'Comentario: {coment}')
    print(f'Classificacao: {rating}')
    print(f'Informacoes Produto: {info}')
    
    if rating == '1':
        coment = 'Pessimo produto'
        info = 'Celular android'
    elif rating == '2':
        coment = 'Produto ruim'
        info = 'Gillete'
    elif rating == '3':
        coment = 'Produto mediano'
        info = 'Livro 2por1'
    elif rating == '4':
        coment = 'Bom produto'
        info = 'Maquina de barbear'
    elif rating == '5':
        coment = 'Produto maravilhoso'
        info = 'Iphone'
    print(f'Novo Comentario: {coment}')
    print(f'Novo Informacoes Produto: {info}')
    
    raw_dict = {
        'feedback_id': {'S': feedback_id},
        'comentario': {'S': coment},
        'classificacao': {'S': rating},
        'infos_produto': {'S': info}
    }
    
    response = creating_item_ddb(raw_dict)
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {
            'Operação': "Concluida!",
            'Item': raw_dict
        }
    else:
        return {
            'Operação': "Falha!",
            'Item': raw_dict
        }
    
def creating_item_ddb(raw_dict: dict):
    response = client.put_item(
        TableName=feedbacks_table,
        Item=raw_dict,
        ConditionExpression="attribute_not_exists(feedback_id)"
        )
        
    return response