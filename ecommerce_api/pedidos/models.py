import uuid
from django.utils import timezone

class Pedido:
    def __init__(self, produto_id, valor, id_pedidousuario, numero_cartao, data_pedido=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.produto_id = produto_id
        self.valor = valor
        self.id_pedidousuario = id_pedidousuario
        self.numero_cartao = numero_cartao[-4:]  # só os 4 últimos dígitos
        self.data_pedido = data_pedido or timezone.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "valor": self.valor,
            "id_pedidousuario": self.id_pedidousuario,
            "numero_cartao": self.numero_cartao,
            "data_pedido": self.data_pedido
        }

    @staticmethod
    def from_dict(data):
        return Pedido(
            id=data.get("id"),
            produto_id=data.get("produto_id"),
            valor=data.get("valor"),
            id_pedidousuario=data.get("id_pedidousuario"),
            numero_cartao=data.get("numero_cartao"),
            data_pedido=data.get("data_pedido")
        )