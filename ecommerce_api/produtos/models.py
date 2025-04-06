import uuid
""""
O que isso permite:
Criar e manipular objetos Produto dentro do seu código;
Converter facilmente de/para dicionário (para se comunicar com o Cosmos DB)."""

"""
📌 O que significa id=None?
No Python, isso define um parâmetro opcional. Ou seja:

Se você passar um ID ao criar o produto, ele será usado.

Se não passar nada, será gerado um ID automaticamente.

Isso é útil porque:

Ao criar um novo produto, normalmente você não tem um ID ainda — ele precisa ser único.

Mas ao atualizar ou deletar um produto, o ID já existe e deve ser mantido.

🔁 E o que faz id or str(uuid.uuid4())?
É um "atalho elegante" que significa:

“Se id tiver valor (não for None), usa ele.
Senão, gera um UUID aleatório.”
"""

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
