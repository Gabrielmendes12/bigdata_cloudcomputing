# bigdata_cloudcomputing

# 🛒 E-commerce API - Django + Azure MySQL + Azure Cosmos DB

Esta é uma API REST para um sistema de e-commerce, desenvolvida com **Django REST Framework**, utilizando **MySQL** para gestão de usuários, endereços e cartões de crédito, e **Azure Cosmos DB** para gerenciamento de produtos.

---
## Tecnologias Utilizadas

- Python 3.13
- Django 4+
- Django REST Framework
- MySQL 
- Azure Cosmos DB (API for Core SQL)
- Postman (para testes)

---

## Instalação e Execução

### 1. Clone o repositório
```bash
git clone https://github.com/Gabrielmendes12/ecommerce-api.git
cd ecommerce-api
```

### 2. Crie o ambiente virtual e ative
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure suas variáveis de ambiente

Crie um arquivo `.env` na raiz com o seguinte conteúdo:

```env
# MySQL
DB_NAME=seubanco
DB_USER=seuusuario
DB_PASSWORD=suasenha
DB_HOST=localhost
DB_PORT=3306

# Azure Cosmos DB
COSMOSDB_URI=https://<seu-endpoint>.documents.azure.com:443/
COSMOSDB_KEY=chave-secreta
COSMOSDB_DATABASE_ID=ecommerce
COSMOSDB_CONTAINER_ID=produtos
```

### 5. Aplique as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Rode o servidor
```bash
python manage.py runserver
```

---
## 🧱 Arquitetura do Projeto

```
ecommerce_api/
├── ecommerce_api/         # Projeto Django principal
├── usuarios/              # App para usuários, endereços e cartões
├── produtos/              # App para produtos (Azure Cosmos DB)
├── manage.py
├── requirements.txt
└── .env
```

### Banco de dados:

| Entidade           | Armazenado em   |
|--------------------|-----------------|
| Usuários           | MySQL           |
| Endereços          | MySQL           |
| Cartões de crédito | MySQL           |
| Produtos           | Azure Cosmos DB |

---

## 🔌 Endpoints da API

### 🧍 Usuários

| Método | Endpoint          | Descrição                     |
|--------|-------------------|-------------------------------|
| GET    | `/usuarios/`      | Lista todos os usuários       |
| POST   | `/usuarios/`      | Cria um novo usuário          |
| GET    | `/usuarios/<id>/` | Detalha um usuário específico |

### 🏠 Endereços

| Método | Endpoint                   | Descrição                         |
|--------|----------------------------|-----------------------------------|
| POST   | `/usuario/<id>/endereco/`  | Adiciona um endereço a um usuário|
| GET    | `/usuario/<id>/enderecos/` | Lista os endereços de um usuário |

**Exemplo de POST:**
```json
{
  "logradouro": "Rua das Flores",
  "complemento": "Casa 2",
  "bairro": "Jardim",
  "cidade": "Rio de Janeiro",
  "estado": "RJ",
  "tipo": "Residencial"
}
```

---

### 💳 Cartões de Crédito

| Método | Endpoint                    | Descrição                         |
|--------|-----------------------------|------------------------------------|
| POST   | `/cartao/`                  | Cria um cartão para um usuário    |
| GET    | `/cartao/<id>/get_saldo/`   | Consulta o saldo do cartão        |
| POST   | `/cartao/<id>/autorizacao/` | Realiza uma transação             |

**Exemplo de criação de cartão:**
```json
{
  "numero": "1234123412341234",
  "data_expiracao": "2025-12-01T00:00:00Z",
  "cvv": "123",
  "saldo": 300.00,
  "usuario": 1
}
```

**Exemplo de Autorização:**
POST `/cartao/1/autorizacao/`
```json
{
  "valor": 50.00
}
```

---

### 🛍️ Produtos (Cosmos DB)

| Método | Endpoint                              | Descrição                              |
|--------|---------------------------------------|----------------------------------------|
| GET    | `/produtos/`                          | Lista todos os produtos                |
| POST   | `/produto/`                           | Cria um novo produto                   |
| PUT    | `/produto/<id>/`                      | Atualiza um produto                    |
| DELETE | `/produto/<id>/<categoria>/`          | Deleta um produto (usa partition key)  |

**Exemplo de criação:**
```json
{
  "nome": "Fone Bluetooth",
  "descricao": "Fone sem fio com cancelamento de ruído",
  "preco": 199.90,
  "categoria": "eletronicos",
  "imagem_url": "https://meusite.com/fone.jpg"
}
```

**Exemplo de deleção:**
```
DELETE /produto/abcd1234-uuid/eletronicos/
```

---
