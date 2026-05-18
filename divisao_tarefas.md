## Divisão geral

| Dev | Responsabilidade principal | Entrega central |
|---|---|---|
| Dev 1 | Fundação da API e infraestrutura | Projeto base, config, banco async, Alembic, sessão, exceções, app startup |
| Dev 2 | CRUD das entidades principais da comanda | Models, schemas, services e rotas das entidades core |
| Dev 3 | Documentos, consultas complexas e carga de dados | Upload/download, filtros, agregações, paginação avançada, seed realista |


## Contexto do sistema

Sistema de comandas que possui as seguintes entidades:

- `Cliente`
- `Mesa`
- `Comanda` --> `N:N`
- `ItemComanda`
- `Produto` --> `N:N`
- `Category` --> `ENUM`
- `Pagamento`

## Responsabilidades por dev

### Miquéias Bento — Base técnica e arquitetura

Responsável por tudo que os outros dois vão reutilizar:

- Estrutura do projeto: `app/models`, `app/api/routes`, `app/core`, `app/db`, `app/schemas`, `app/services`, `app/repositories`, `alembic/`, `scripts/`.
- Configuração com `.env`, alternando entre SQLite e PostgreSQL por URL.
- Engine e sessão assíncronos com SQLModel/SQLAlchemy async.
- Alembic async, configuração de metadata e fluxo de migrações.
- Tratamento global de exceções, handlers e padrão de resposta de erro.
- Registro do FastAPI, OpenAPI, tags e dependências compartilhadas.
- Paginação base com `fastapi-pagination`.

Entregáveis:

1. `pyproject.toml`, `.python-version`, `uv.lock`, `.env.example` ou `.env`.
2. `database.py`, `settings.py`, `deps.py`.
3. `alembic.ini`, `migrations/env.py`, primeira migration.
4. Middleware e exception handlers.
5. Guia de convenções para os demais.

Definir o padrão oficial de consulta paginada, porque a lib `fastapi-pagination` trabalha com tipos como `Page[...]` e integração com SQLAlchemy via `fastapi_pagination.ext.sqlalchemy.paginate`, o que precisa ficar uniforme no projeto inteiro. [github](https://github.com/uriyyo/fastapi-pagination/blob/main/README.md)

### Francisco Mateus — Entidades core e CRUD principal

Implementa o coração do sistema de comandas:

- `Customer`
- `Table`
- `Product`
- `Category`
- `Command`
- `ItemCommand`
- `Payment`

Recorte:

- `Customer`: CRUD completo, busca por nome parcial.
- `Table`: CRUD completo, filtros por status.
- `Product`: CRUD completo, filtros por nome, preço, categoria.
- `Category`: CRUD completo.
- `Command`: CRUD completo, abrir/fechar comanda, associar cliente/mesa.
- `ItemCommand`: CRUD completo dentro da comanda.
- `Payment`: CRUD completo, adicionar pagamento à comanda.

Deve entregar:

- Models SQLModel.
- Schemas de entrada/saída.
- Services/repositories async.
- Rotas CRUD com paginação e filtros.
- Eager loading nas consultas relacionais.

### Devora Viana — Documentos, consultas analíticas e seed

- Entidade `Document` com metadados.
- Upload físico em pasta local e persistência só dos metadados no banco.
- Endpoints de documento.
- Consultas complexas, agregações, contagens, ordenações e filtros por data.
- Script de carga com Faker pt_BR.
- Compatibilidade da carga com banco definido no `.env`.

Vai associar documentos à entidade `Product`, porque faz bastante sentido armazenar foto do produto, ficha técnica ou cardápio em PDF. O FastAPI trabalha bem com `UploadFile`, inclusive com acesso a `filename` e `content_type`, e o arquivo pode ser salvo em diretório local enquanto o banco guarda apenas os metadados exigidos pelo trabalho. [dev](https://dev.to/awslearnerdaily/day-6-file-uploads-form-handling-in-fastapi-3kpl)

## Separação técnica interna

Para evitar conflito entre os 3, defina desde o início este contrato:

- **Dev 1** cria a base e congela convenções.
- **Dev 2** só trabalha nas entidades core e seus CRUDs.
- **Dev 3** só trabalha em `documents`, `reports`, `search`, `seed`.

Sugestão de ownership por pasta:

- `app/core`, `app/db`, `migrations` → Dev 1
- `app/models/core_*`, `app/api/routes/core_*`, `app/services/core_*` → Dev 2
- `app/models/document.py`, `app/api/routes/documents.py`, `app/api/routes/reports.py`, `scripts/seed.py` → Dev 3

## Backlog geral

### Dev 1
- Configurar `uv`, `pyproject.toml`, `.python-version`, `uv.lock`.
- Configurar `.env` com SQLite ativo e PostgreSQL comentado.
- Criar `settings`.
- Implementar `create_async_engine`.
- Implementar `AsyncSession`.
- Configurar Alembic async.
- Criar handlers de erro.
- Integrar `fastapi-pagination`.
- Subir app com Swagger funcionando.

### Dev 2
- Modelar `Customer`, `Table`, `Command`, `OrderItem`, `Product`, `Category`.
- Configurar relacionamentos.
- Implementar CRUD completo.
- Implementar paginação em todas as listagens.
- Implementar filtros simples e busca textual.
- Garantir eager loading nas consultas com relacionamentos.

### Dev 3
- Modelar `Document`.
- Implementar upload, replace, delete e download físico.
- Associar documentos a `Product` ou `Command`.
- Criar consultas complexas e estatísticas.
- Criar script `seed.py` com 100+ registros por entidade usando Faker pt_BR.
- Validar funcionamento em SQLite e PostgreSQL.
