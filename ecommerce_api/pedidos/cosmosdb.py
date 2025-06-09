from azure.cosmos import CosmosClient
from decouple import config

class CosmosDBPedidos:
    def __init__(self):
        self.client = CosmosClient(
            config("COSMOSDB_URI"),
            credential=config("COSMOSDB_KEY")
        )
        self.database = self.client.get_database_client(config("COSMOSDB_DATABASE_ID"))
        self.container = self.database.get_container_client(config("COSMOSDB_CONTAINER_PEDIDOS"))

    def create_item(self, data: dict):
        return self.container.create_item(body=data)

    def list_by_usuario(self, id_pedidousuario: str):
        query = "SELECT * FROM c WHERE c.id_pedidousuario = @usuario"
        params = [{"name": "@usuario", "value": id_pedidousuario}]
        return list(self.container.query_items(
            query=query,
            parameters=params,
            enable_cross_partition_query=True
        ))

    def get_item(self, pedido_id: str, id_pedidousuario: str):
        return self.container.read_item(
            item=pedido_id,
            partition_key=id_pedidousuario
        )

# Instância global
cosmos_pedidos = CosmosDBPedidos()