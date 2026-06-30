## Divisão geral

| Dev | Responsabilidade principal | Entrega central |
|---|---|---|
| Dev 1 | Fundação da API e infraestrutura | Projeto base, config, MongoDB/Beanie, FastAPI startup, pagination, Docker |
| Dev 2 | CRUD das entidades principais da comanda | Models, schemas, services, rotas das entidades core |
| Dev 3 | Documentos, relatórios, consultas e seed | Upload/download no MinIO, relatórios, filtros, seed realista |


## Contexto do sistema

Sistema de comandas que possui as seguintes entidades:

- `Client`
- `Table`
- `Command`
- `ItemCommand`
- `Product`
- `Payment`
- `Document`

Relacionamentos principais:

- `Client` 1:N `Command`
- `Table` 1:N `Command`
- `Command` 1:N `ItemCommand`
- `Product` 1:N `ItemCommand`
- `Product` 1:N `Document`
- `Command` 1:N `Payment`

## Responsabilidades por dev

### Miquéias Bento — Base técnica e arquitetura

Responsável pela infraestrutura, configuração e pelo contrato técnico do projeto:

- Estrutura do projeto: `app/core`, `app/models`, `app/api/routes`, `app/services`, `app/repositories`, `app/schemas`.
- Configuração de ambiente com `.env` e Docker Compose.
- Inicialização do MongoDB com Beanie e Motor.
- Registro do FastAPI, OpenAPI, tags, middleware e handlers globais de erro.
- Integração de `fastapi-pagination` em todas as listagens.
- Deploy Docker com `Dockerfile` e `docker/docker-compose.yaml`.
- Definição de convenções de rotas, validação e erros.

Entregáveis:

1. `pyproject.toml`, `.python-version`, `uv.lock`.
2. `app/core/config.py`, `app/core/database.py`.
3. `docker/Dockerfile`, `docker/docker-compose.yaml`.
4. `app/main.py`, app startup e `@app.on_event("startup")`.
5. Arquivo `.env` compatível com Docker Compose (`mongo`, `minio`) e com alternância por comentários.

### Francisco Mateus — Entidades core e CRUD principal

Responsável pelo domínio central do sistema de comandas:

- Modelagem e CRUD de `Client`, `Table`, `Product`, `Command`, `ItemCommand`, `Payment`.
- Schemas de entrada e saída (`Pydantic` / `Beanie`).
- Serviços e repositórios para regras de negócio das entidades core.
- Rotas REST com paginação, filtros e ordenação.
- Busca parcial e filtros por relacionamento.
- Consulta de comando com itens, cliente e mesa carregados.

Entregáveis:

- Modelos `Beanie` para as entidades core.
- Schemas Pydantic para requests/responses.
- Serviços que encapsulam regras de criação, atualização e exclusão.
- Rotas CRUD com `page`/`size` e `order_by` quando aplicável.
- Validação de dados e tratamento de exceções específicas.

### Devora Viana — Documentos, relatórios e seed

Responsável pela parte de documentos e relatórios analíticos:

- Modelagem de `Document` com metadados no MongoDB.
- Integração com MinIO para armazenamento físico de arquivos.
- Upload, download, substituição e exclusão de arquivos.
- Endpoints obrigatórios de documentos e download.
- Consultas analíticas, agregações, relatórios e filtros por data.
- Script `seed.py` para popular o banco com dados reais.

Entregáveis:

- `app/models/document.py` e `app/repositories/document_repository.py`.
- Rotas de documento: upload, listagem, metadados, download, update, delete.
- Integração com `app/services/storage_service.py`.
- Script de carga `seed.py` com Faker pt_BR e 100+ registros por entidade.
- Endpoints de relatórios/analytics no prefixo `/analytics`.

## Separação técnica interna

Para evitar conflito entre os 3, mantenha este contrato de ownership:

- **Dev 1**: infraestrutura, configuração, inicialização do app e padrões.
- **Dev 2**: entidades core, CRUDs e regras de negócio principais.
- **Dev 3**: documentos, relatórios, pesquisa avançada e seed.

Sugestão de ownership por pasta:

- `app/core`, `app/main.py`, `docker/` → Dev 1
- `app/models/client.py`, `app/models/table.py`, `app/models/product.py`, `app/models/command.py`, `app/models/payment.py`, `app/api/routes/*` core → Dev 2
- `app/models/document.py`, `app/api/routes/document_router.py`, `app/api/routes/reports_router.py`, `app/services/storage_service.py`, `scripts/seed.py`, `seed.py` → Dev 3

## Backlog geral

### Dev 1
- Configurar `uv`, `pyproject.toml`, `.python-version`, `uv.lock`.
- Criar `.env` com configuração de MongoDB e MinIO para Docker Compose.
- Implementar `app/core/config.py` e `app/core/database.py`.
- Criar `docker/docker-compose.yaml` com serviços `api`, `mongo`, `minio`, `mongo-express`.
- Registrar FastAPI e ativar `fastapi-pagination`.
- Implementar handlers globais de erro e validação.
- Garantir que o app inicie com `uv run uvicorn app.main:app --reload`.

### Dev 2
- Modelar entidades core e relacionamentos com `Beanie`.
- Criar schemas Pydantic e serviços para CRUD.
- Implementar rotas REST completas para `Client`, `Table`, `Product`, `Command`, `Payment`.
- Adicionar filtros de busca parcial, ordenação e paginação.
- Garantir dados consistentes entre `Command`, `ItemCommand`, `Client` e `Table`.
- Validar respostas e erros para operações CRUD.

### Dev 3
- Modelar `Document` e metadados obrigatórios.
- Implementar upload/download via MinIO e armazenamento de metadados em Mongo.
- Criar endpoints de documentos por produto e de download (`/documents/{id}/download`).
- Criar consultas analíticas e relatórios no prefixo `/analytics`.
- Desenvolver `seed.py` com Faker pt_BR e dados reais para todas as coleções.
- Garantir que a seed use as variáveis do `.env` e funcione dentro do Docker.

