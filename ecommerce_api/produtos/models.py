import uuid
"""
Criar e manipular objetos Produto
Converter facilmente de/para dicionário (para se comunicar com o Cosmos DB)."""

class Produto:
    def __init__(self, nome, descricao, preco, categoria, imagem_url, id=None):
        self.id = id or str(uuid.uuid4())
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria  # Partition Key!
        self.imagem_url = imagem_url

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "categoria": self.categoria,
            "imagem_url": self.imagem_url   
        }

    @staticmethod
    def from_dict(data):
        return Produto(
            id=data.get("id"),
            nome=data.get("nome"),
            descricao=data.get("descricao"),
            preco=data.get("preco"),
            categoria=data.get("categoria"),
            imagem_url=data.get("imagem_url")
        )
