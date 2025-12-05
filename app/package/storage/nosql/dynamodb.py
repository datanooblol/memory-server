import boto3
from typing import Dict, List, Optional
from ..base import NoSQLStorage

class DynamoDBStorage(NoSQLStorage):
    def __init__(self, config: Dict):
        self.dynamodb = boto3.resource('dynamodb', 
            region_name=config.get('region', 'us-east-1'),
            aws_access_key_id=config.get('access_key'),
            aws_secret_access_key=config.get('secret_key')
        )
    
    async def create_table(self, table_name: str, key_schema: Dict) -> None:
        # Create table with partition key
        try:
            table = self.dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': key_schema['partition_key'],
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': key_schema['partition_key'],
                        'AttributeType': 'S'
                    }
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            table.wait_until_exists()
        except Exception as e:
            if 'ResourceInUseException' not in str(e):
                raise
    
    async def put_item(self, table: str, item: Dict) -> None:
        table_obj = self.dynamodb.Table(table)
        table_obj.put_item(Item=item)
    
    async def get_item(self, table: str, key: Dict) -> Optional[Dict]:
        table_obj = self.dynamodb.Table(table)
        response = table_obj.get_item(Key=key)
        return response.get('Item')
    
    async def scan_items(self, table: str, filters: Dict = None) -> List[Dict]:
        table_obj = self.dynamodb.Table(table)
        
        if filters:
            # Simple filter implementation
            filter_expression = []
            expression_values = {}
            
            for key, value in filters.items():
                filter_expression.append(f"#{key} = :{key}")
                expression_values[f":{key}"] = value
            
            response = table_obj.scan(
                FilterExpression=" AND ".join(filter_expression),
                ExpressionAttributeNames={f"#{key}": key for key in filters.keys()},
                ExpressionAttributeValues=expression_values
            )
        else:
            response = table_obj.scan()
        
        return response.get('Items', [])