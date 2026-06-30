# Sistema de Comandas API

API assíncrona para gerenciamento de comandas de consumo em restaurantes, bares e cafés. O projeto usa FastAPI, Beanie ODM e MongoDB para persistir clientes, mesas, produtos, comandas, pagamentos e documentos de produtos.

## Tecnologias

* **FastAPI** para API REST e documentação OpenAPI/Swagger.
* **Beanie ODM** e **Motor** para acesso assíncrono ao MongoDB.
* **MongoDB** como banco principal.
* **Pydantic** para validação e serialização.
* **fastapi-pagination** para paginação em consultas.
* **Faker pt_BR** para carga realista de dados.
* **uv** para dependências e execução.

## Modelo de Dados

```mermaid
erDiagram
    Client ||--o{ Command : "abre"
    Table ||--o{ Command : "recebe"
    Command ||--o{ ItemCommand : "contem"
    Product ||--o{ ItemCommand : "vendido_em"
    Product ||--o{ Document : "possui"
    Command ||--o{ Payment : "recebe"

    Client {
        ObjectId id
        string name
        string phone
        string email
        string tax_id
        datetime created_at
    }

    Table {
        ObjectId id
        int number
        string name
        int seats
        string location
        string status
    }

    Product {
        ObjectId id
        string name
        string description
        string category
        float price
        bool active
    }

    Command {
        ObjectId id
        DBRef client
        DBRef table
        list items
        string status
        float total_amount
        datetime opened_at
        datetime closed_at
    }

    ItemCommand {
        DBRef product
        int quantity
        float unit_price
        string observation
    }

    Payment {
        ObjectId id
        DBRef command
        float amount
        string method
        string status
        datetime paid_at
    }

    Document {
        UUID id
        DBRef product
        string original_filename
        string content_type
        string extension
        int size_bytes
        datetime created_at
    }
```

## Estrutura

```text
app/
  api/routes/          Rotas por domínio e /analytics
  core/                Configuração e inicialização do MongoDB
  models/              Documentos Beanie
  repositories/        Consultas e agregações
  schemas/             Schemas Pydantic
  services/            Regras de negócio
docker/                Arquivos auxiliares de infraestrutura
seed.py                Carga de dados realistas
pyproject.toml         Dependências do projeto
```

## Configuração

Instale as dependências:

```bash
uv sync
```

Crie ou ajuste o arquivo `.env` na raiz. Você pode informar a URL completa:

```ini
MONGO_URL=mongodb://admin:adminpassword@localhost:27017/
DATABASE_NAME=yourmenu
```

Ou usar as variáveis separadas:

```ini
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_ROOT_USER=admin
MONGO_ROOT_PASSWORD=adminpassword
DATABASE_NAME=yourmenu
```

## MongoDB

Com Docker, suba um MongoDB local compatível com o `.env`:

```bash
docker run --name sistema-comandas-mongo -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=adminpassword -d mongo:7
```

Se já existir um MongoDB local, basta apontar `MONGO_URL` para ele.

## Seed

Popule o banco com dados realistas:

```bash
uv run python seed.py
```

Por padrão o script limpa as coleções antes de inserir novos dados. Para manter os dados existentes e adicionar novos registros:

```bash
uv run python seed.py --no-clean
```

O seed cria clientes, mesas, produtos, documentos, comandas com itens consistentes e pagamentos vinculados.

## Executando

```bash
uv run uvicorn app.main:app --reload
```

Documentação interativa:

```text
http://localhost:8000/docs
```

## Rotas Analíticas

As rotas de relatórios ficam no prefixo `/analytics`:

* `GET /analytics/commands/by-date-range`: comandas abertas ou fechadas dentro de um período, com paginação.
* `GET /analytics/products/search`: busca textual em nome e descrição de produtos.
* `GET /analytics/commands/summary`: listagem paginada de comandas ordenada por `opened_at`, `closed_at` ou `total_amount`.
* `GET /analytics/commands/count`: total de comandas cadastradas.
* `GET /analytics/commands/{command_id}`: consulta de uma comanda com relacionamentos resolvidos.
* `GET /analytics/revenue-by-category`: faturamento e quantidade vendida por categoria.
* `GET /analytics/client-ranking`: ranking de consumo de clientes em comandas fechadas.
* `GET /analytics/table-stats`: faturamento, quantidade de comandas e ticket médio por mesa.

Exemplo:

```bash
curl "http://localhost:8000/analytics/commands/summary?sort_by=total_amount&order=desc&page=1&size=20"
```

## Observações

O modelo `Product` declara um índice textual composto em `name` e `description` para habilitar busca full-text no MongoDB. A criação do índice ocorre durante a inicialização do Beanie.
