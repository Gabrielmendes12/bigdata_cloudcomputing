#Este arquivo gerencia a conexão com o Cosmos DB e permite acessar coleções específicas.

from azure.cosmos import CosmosClient
from django.conf import settings

class CosmosDBProdutos:
    def __init__(self):
        self.client = CosmosClient(settings.COSMOSDB_URI, credential=settings.COSMOSDB_KEY)
        self.database = self.client.get_database_client(settings.COSMOSDB_DATABASE_ID)
        self.container = self.database.get_container_client(settings.COSMOSDB_CONTAINER_PRODUTOS)

    def list_items(self):
        return list(self.container.read_all_items())

    def create_item(self, data):
        return self.container.create_item(body=data)

    def update_item(self, item_id, data):
        return self.container.replace_item(item=item_id, body=data)

    def delete_item(self, item_id, partition_key_value):
        # O partition_key_value deve ser o valor da chave de partição do item que você deseja excluir.
        # Isso é necessário para o Cosmos DB, pois ele usa chaves de partição para distribuir dados.
        # O item_id é o ID do item que você deseja excluir.
        return self.container.delete_item(item=item_id, partition_key=partition_key_value)
    """
    def get_item(self, item_id, partition_key_value):
        return self.container.read_item(item=item_id, partition_key=partition_key_value)"""
    def get_item(self, item_id, partition_key_value=None):
        if partition_key_value:
            return self.container.read_item(item=item_id, partition_key=partition_key_value)
        else:
            query = f"SELECT * FROM c WHERE c.id = '{item_id}'"
            items = list(self.container.query_items(query=query, enable_cross_partition_query=True))
            if not items:
                raise Exception("Produto não encontrado.")
            return items[0]
# Instância global reutilizável
cosmos_produtos = CosmosDBProdutos()