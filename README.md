# Sistema de Comandas API (SQLModel + Async)

Este projeto consiste em uma API assíncrona robusta para o gerenciamento de comandas de consumo em estabelecimentos comerciais (como restaurantes, bares e cafés). Ele foi desenvolvido para a disciplina de **Desenvolvimento de Software para Persistência** (Trabalho Prático - Parte II), utilizando tecnologias modernas do ecossistema Python para persistência relacional assíncrona e upload de mídias físicas.

---

## Tecnologias Utilizadas

*   **[FastAPI](https://fastapi.tiangolo.com/)**: Construção da API REST ágil, moderna e autocomprovada com OpenAPI/Swagger.
*   **[SQLModel](https://sqlmodel.tiangolo.com/)**: Abstração ORM que unifica o poder de validação do Pydantic com a flexibilidade relacional do SQLAlchemy.
*   **[Alembic](https://alembic.sqlalchemy.org/)**: Controle de versão e migrações do banco de dados executado de forma 100% assíncrona.
*   **SQLite & PostgreSQL**: Compatibilidade total de schemas. A alteração de persistência ocorre bastando mudar uma linha no arquivo `.env`.
*   **[UV](https://github.com/astral-sh/uv)**: Gerenciador ultra-rápido de dependências e ambiente virtual do ecossistema Python.
*   **[fastapi-pagination](https://github.com/uriyyo/fastapi-pagination)**: Paginação integrada de alta performance aplicada diretamente no banco de dados para evitar vazamento de memória RAM.

---

## Modelo de Dados (ERD)

O sistema conta com **7 entidades interconectadas**, atendendo aos requisitos mínimos de relacionamentos Um-para-Muitos ($1 \leftrightarrow N$) e Muitos-para-Muitos ($N \leftrightarrow M$):

```mermaid
---
config:
  layout: elk
  look: classic
  theme: dark
---
erDiagram
    Cliente ||--o{ Comanda : "possui"
    Comanda ||--o{ ItemComanda : "contém"
    Mesa ||--o{ Comanda : "vinculada_a"
    Produto ||--o{ ItemComanda : "associado_a"
    Produto ||--o{ Documento : "possui"
    Comanda ||--o{ Pagamento : "recebe"

    Cliente {
        int id PK "Autoincrement"
        string nome "index"
        string telefone
        string email "index"
        string identificador
        datetime criado_em
        int comanda_id FK "comandas.is"
    }

    Mesa {
        int id PK "Autoincrement"
        int numero "unique"
        string nome
        int assentos
        string local
        string status "LIVRE/OCUPADA"
        int comanda_id FK "comandas.id"
    }

    Comanda {
        int id PK "Autoincrement"
        string codigo "index"
        string status "ABERTA/FECHADA/CANCELADA"
        datetime aberta_em
        datetime fechada_em
        float total_conta
        int cliente_id FK "clientes.id"
        int mesa_id FK "mesa.id"
    }

    ItemComanda {
        int id PK "Autoincrement"
        int comanda_id FK "Comandas.id"
        int produto_id FK "Produtos.id"
        int quantity
        float preco_unitario
    }

    Produto {
        int id PK "Autoincrement"
        string nome
        string descricao
        string categoria "BEBIDA/PRATO_PRINCIPAL/etc"
        float preco
        bool ativo
    }

    Documento {
        UUID id PK "UUIDv4"
        int Produto_id FK "Produtos.id"
        string arquivo
        string tipo
        string extensao
        int tamanho
        datetime criado_em
    }

    Pagamento {
        int id PK "Autoincrement"
        int comanda_id FK "comanda.id"
        float valor
        string metodo "DINHEIRO/CARTAO/PIX"
        string status "PAGO/ESTORNADO"
        datetime pago_em
    }
```

### Entidades do Domínio:
1.  **[Client](./app/models/client.py)**: Clientes do estabelecimento.
2.  **[Table](./app/models/table.py)**: Mesas físicas onde os clientes realizam o consumo.
3.  **[Command](./app/models/command.py)**: Controle central da comanda aberta com seu status e acumuladores.
4.  **[ItemCommand](./app/models/item_command.py)**: Itens consumidos associados à comanda, encapsulando quantidade e o histórico do preço unitário de venda.
5.  **[Product](./app/models/product.py)**: Produtos do cardápio.
6.  **[Payment](./app/models/payment.py)**: Pagamentos parciais ou totais aplicados à comanda.
7.  **[Document](./app/models/document.py)**: Anexos e fotos associados a produtos do cardápio, onde os arquivos físicos residem de forma local no sistema e o banco de dados armazena apenas seus metadados.

---

## Estrutura de Diretórios

O projeto está estruturado de forma modular e altamente extensível:

```text
├── alembic.ini                   # Configurações do migrador Alembic
├── migrations/                   # Scripts de migração de banco gerados
├── app/
│   ├── api/
│   │   ├── errors/               # Middleware de erros e exception handlers globais
│   │   └── routes/               # Rotas/Endpoints por domínio
│   ├── core/
│   │   ├── config.py             # Configurações do app através do .env
│   │   └── database.py           # Setup do motor e sessão assíncrona do SQLAlchemy
│   ├── models/                   # Entidades SQLModel representativas das tabelas
│   ├── repositories/             # Camada de persistência/acesso a dados genérica
│   ├── schemas/                  # Validação Pydantic (Create, Update, Response)
│   └── services/                 # Regras de negócios e transações
├── uploads/                      # Pasta local padrão para armazenamento físico de documentos
├── scripts/
│   ├── seed.py                   # Script de carga inicial (1.000+ registros via Faker pt_BR)
│   └── seeds/                    # Sub-seeds modulares
├── pyproject.toml                # Dependências e declaração de ferramentas do projeto
└── uv.lock                       # Arquivo de integridade e travamento do UV
```

---

## Instalação e Execução

### 1. Pré-requisitos
Certifique-se de possuir o **Python 3.10+** e o gerenciador de pacotes **`uv`** instalado em sua máquina.

### 2. Clonando e Instalando Dependências
Com o `uv` instalado, execute no terminal para sincronizar as dependências e o ambiente virtual:
```bash
uv sync
```

### 3. Configuração do `.env`
Crie ou edite o arquivo `.env` na raiz do projeto contendo as credenciais. Você pode alternar o driver de persistência comentando e descomentando as linhas:
```ini
# Para persistência em SQLite Local:
DATABASE_URL=sqlite+aiosqlite:///./comandas.db

# Para persistência em PostgreSQL (Nuvem ou Docker):
# DATABASE_URL=postgresql+asyncpg://usuario:senha@host:porta/banco
```

### 4. Executando as Migrações
Execute o comando a seguir para aplicar as atualizações do banco assincronamente através do Alembic:
```bash
uv run alembic upgrade head
```

### 5. Carga de Dados (Seeding Realista)
Popule o banco de dados configurado no `.env` com no mínimo **1.000 registros realistas** gerados através da biblioteca `Faker` (localização `pt_BR`):
```bash
uv run python scripts/seed.py
```

### 6. Executando o Servidor de Desenvolvimento
Inicie a aplicação utilizando o Uvicorn:
```bash
uv run uvicorn app.main:app --reload
```
Acesse a documentação interativa Swagger no endereço:
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## Endpoints de Consultas Analíticas e Relatórios

Além do CRUD completo para todas as entidades principais do domínio com suporte a paginação de alto desempenho (`fastapi-pagination`) e carregamento de relacionamentos ansiosos (*eager loading* via `selectinload` e `joinedload`), a aplicação expõe endpoints dedicados para relatórios analíticos:

*   **Filtros complexos**: Listagem de comandas por cliente ativo ou por período.
*   **Busca textual parcial**: Localização de produtos ou clientes pelo nome parcial.
*   **Agregações e Estatísticas**: Total arrecadado por comanda, ticket médio por mesa, contagem de comandas abertas, etc.
*   **Upload e Download de Arquivos**: Endpoints específicos em `/produtos/{produto_id}/documents` para controle integral de mídias de produtos com persistência exclusiva de metadados.

---

## Membros e Divisão de Tarefas

Consulte o arquivo **[divisao_tarefas.md](divisao_tarefas.md)** para mais detalhes de ownership sobre a arquitetura e componentes criados por cada membro.
