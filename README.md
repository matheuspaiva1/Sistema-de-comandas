# Sistema de Comandas - API com Delta Lake

Este projeto implementa um sistema de gerenciamento de comandas utilizando **FastAPI** para a interface REST e **Delta Lake** para a persistência de dados, seguindo os requisitos de desenvolvimento de software para persistência.

---

## 1. Mini Banco de Dados com Delta Lake

Implementação de uma classe em Python que gerencia a persistência de uma entidade no formato Delta Lake (biblioteca `deltalake`), suportando operações CRUD completas.

### Requisitos de Persistência

* **Persistência em Arquivo**: Utilização exclusiva do módulo `deltalake` para leitura e escrita.
* **Eficiência de Memória**: Nenhuma operação depende do carregamento completo dos dados na RAM.
* **Controle de IDs (autoincremento)**: Manutenção de um arquivo auxiliar `.seq` para incremento automático do identificador a cada nova inserção.

### Operações Obrigatórias

| Método | Descrição |
| :--- | :--- |
| `insert` | Insere um novo registro |
| `get` | Recupera um registro por ID |
| `list` | Retorna uma página de registros (paginação de tamanho variável) |
| `update` | Atualiza um registro existente |
| `delete` | Remove um registro |
| `count` | Retorna o total real de registros armazenados |
| `vacuum` | Compacta e limpa o arquivo de dados, descartando versões antigas e otimizando o espaço |

---

## 2. Entidade do Domínio

A entidade escolhida para este projeto é a **Comanda**, relacionada à gestão de consumo em estabelecimentos.
Atributos principais incluem: `id`, `clientId`, `tableId`, `status`, `fullValue`.

---

## 3. API REST com FastAPI

Interface RESTful validada com Pydantic, organizada em módulos dedicados.

### Endpoints e Funcionalidades

| ID | Funcionalidade | Descrição |
| :--- | :--- | :--- |
| **F1** | Inserção | Recebe JSON da entidade e insere no minibanco. |
| **F2** | Listagem Paginada | Define número e tamanho da página via *query string*. |
| **F3** | CRUD Completo | GET, POST, PUT/PATCH, DELETE agindo diretamente no arquivo. |
| **F4** | Contagem | Retorna o número total de registros. |
| **F5** | Exportação CSV | Streaming de todos os registros sem carregar tudo em memória. |
| **F6** | Exportação ZIP | Streaming de CSV compactado em formato `.zip`. |
| **F7** | Hash de Dado | Gera hash (MD5, SHA-1, SHA-256) de um valor recebido. |

---

## 4. Script de Carga Inicial

Scripts integrados (ex: `scripts/seed.py`) para população automática do banco com no mínimo **1.000 registros realistas** utilizando a biblioteca `Faker` (localização `pt_BR`).

---

## 5. Divisão de Tarefas

Consulte o arquivo `divisao_tarefas.txt` para detalhes sobre as implementações realizadas por cada membro do grupo.

---

## 📝 Observações Gerais e Diretrizes

* **Apresentação**: Obrigatória e presencial (5 min por membro).
* **Modularização**: Código organizado por funcionalidades e responsabilidades específicas.
* **Qualidade dos Dados**: Geração de dados realistas e coerentes.
* **Tipagem Moderna**: Utilização da sintaxe nativa do Python 3.10+ (ex: `list`, `str | None`) em vez do módulo `typing` legado.
* **Performance**: Proibição do carregamento da tabela inteira em memória; uso obrigatório de paginação e filtros.
* **Entrega**: Inclui apenas código-fonte, scripts de carga e `pyproject.toml`. Arquivos gerados (`data/`, `.venv`, etc) não devem ser versionados.
