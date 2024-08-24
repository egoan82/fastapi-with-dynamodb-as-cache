import logging
import boto3

from core.settings import settings


class UsersDynamodb:
    def __init__(self):
        self.table_name = "users"
        _session = boto3.Session(
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region_name,
        )
        self.client = _session.client("dynamodb")

    def create_table(self):
        try:
            self.client.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {"AttributeName": "id", "KeyType": "HASH"}
                ],
                AttributeDefinitions=[
                    {"AttributeName": "id", "AttributeType": "S"},
                    {"AttributeName": "value", "AttributeType": "S"},
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
            )

            self.client.meta.client.get_waiter('table_exists').wait(TableName='users')
            return True
        except self.client.exceptions.ResourceInUseException:
            logging.info(f"Table {self.table_name} already exists.")
            return False

    def get_item(self, id: str):
        try:
            response = self.client.get_item(Key={"id": {"S": id}}, TableName=self.table_name)
            return response.get("Item", None)
        except Exception as e:
            logging.error(f"Error getting item {id}: {e.args[0]}")
            raise ValueError(f"Error getting item {id}: {e.args[0]}")

    def put_item(self, item: dict):
        try:
            self.client.put_item(Item=item, TableName=self.table_name)
        except Exception as e:
            logging.error(f"Error putting item {item}: {e.args[0]}")
            raise ValueError(f"Error putting item {item}: {e.args[0]}")

    def delete_item(self, id: str):
        try:
            result = self.client.delete_item(Key={"id": {"S": id}}, TableName=self.table_name)
            print(f"DeleteItem response: {result}")
        except Exception as e:
            logging.error(f"Error deleting item {id}: {e.args[0]}")
            raise ValueError(f"Error deleting item {id}: {e.args[0]}")
