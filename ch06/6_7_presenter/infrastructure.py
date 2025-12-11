# Framework & Drivers Layer (Infrastructure)
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any


class DynamoDBClient:
    def __init__(self, region: str = "ap-northeast-2"):
        self.client = boto3.resource("dynamodb", region_name=region)

    def get_item(self, table_name: str, key: Dict[str, Any]) -> Dict[str, Any]:
        try:
            table = self.client.Table(table_name)
            response = table.get_item(Key=key)
            return response
        except ClientError as e:
            raise ValueError(f"Failed to retrieve data: {str(e)}")
