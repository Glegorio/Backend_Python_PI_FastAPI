<a id="top"></a>

<p align="center">
  <img src="docs/assets/readme-cover.svg" alt="Valentes de Davi — Futebol, comunidade e tecnologia. Backend com Python, FastAPI e MySQL." width="100%">
</p>

<h1 align="center">ONG Valentes de Davi · Backend</h1>

<p align="center">
  A base de dados por trás de um projeto que começa em campo.<br>
  API para a gestão de assistidos de uma ONG de futebol.
</p>

<p align="center">
  <strong>Projeto Integrador</strong> &nbsp; / &nbsp; Em desenvolvimento &nbsp; / &nbsp; Python · FastAPI · MySQL
</p>

<p align="center">
  <a href="#portugues">O projeto</a> &nbsp; · &nbsp;
  <a href="#tecnologias">Engenharia</a> &nbsp; · &nbsp;
  <a href="#executar-localmente">Execução local</a> &nbsp; · &nbsp;
  <a href="#endpoints-de-assistidos">API</a> &nbsp; · &nbsp;
  <a href="#english">English</a>
</p>

---

<a id="portugues"></a>

## 01 / O projeto

Este backend oferece a base para organizar os dados dos assistidos (alunos) da ONG Valentes de Davi. A aplicação utiliza FastAPI, validação com Pydantic e acesso assíncrono ao MySQL por meio do SQLAlchemy e do driver aiomysql.

O projeto está em desenvolvimento inicial. Atualmente, a API concentra suas funcionalidades no módulo de assistidos. O esquema do banco também contempla voluntários, aulas e chamadas, cujas APIs ainda não foram implementadas.

### O que já existe

| Recurso | Situação |
| --- | --- |
| Cadastro de assistidos | Implementado, com verificação de CPF duplicado quando informado |
| Listagem de assistidos | Implementada, com paginação por `skip` e `limit` e filtro `apenas_ativos` |
| Consulta, atualização parcial e desativação por ID | Rotas e serviços definidos no módulo de assistidos |
| Exclusão lógica | Serviço implementado; preserva o registro e define `ativo=false` |
| Documentação da API | Swagger UI, ReDoc e esquema OpenAPI |
| Voluntários, aulas e chamadas | Tabelas definidas em `Schema.sql`; sem módulos de API |
| Autenticação e autorização | Ainda não implementadas |
| Testes automatizados e migrações versionadas | Ainda não incluídos |

<a id="tecnologias"></a>

## 02 / Engenharia

| Tecnologia | Uso |
| --- | --- |
| Python | Linguagem da aplicação |
| FastAPI | Rotas HTTP e documentação automática |
| Uvicorn | Servidor ASGI |
| SQLAlchemy 2 | Mapeamento ORM e sessões assíncronas |
| MySQL + aiomysql | Persistência e driver assíncrono |
| Pydantic 2 + pydantic-settings | Validação dos dados e configurações de ambiente |
| python-dotenv | Suporte ao carregamento de variáveis do `.env` |

As dependências e suas versões mínimas estão em [`requirements.txt`](requirements.txt).

<a id="estrutura"></a>

### Organização do código

```text
.
├── app/
│   ├── main.py                  # Aplicação, CORS, rotas e healthcheck
│   ├── core/
│   │   ├── config.py            # Configurações e carregamento do .env
│   │   └── database.py          # Engine, sessões e base do ORM
│   └── modules/
│       └── assistidos/
│           ├── models.py        # Modelo ORM
│           ├── schemas.py       # Contratos de entrada e saída
│           ├── service.py       # Operações de persistência
│           └── router.py        # Endpoints do módulo
├── requirements.txt
├── Schema.sql                  # Criação do banco, tabelas e índices
└── README.md
```

O módulo separa a interface HTTP, as operações de persistência e os contratos de dados:

```text
REQUISIÇÃO HTTP
      │
      ▼
   router.py ─── schemas.py
      │         entrada e resposta · Pydantic
      ▼
   service.py
      │         consultas e regras de persistência
      ▼
   models.py ── MySQL
                sessão assíncrona · SQLAlchemy + aiomysql
```

| Decisão | Aplicação no projeto |
| --- | --- |
| Organização por domínio | Rotas, schemas, modelo e serviço de assistidos ficam no mesmo módulo. |
| Persistência assíncrona | Serviços usam `AsyncSession` e operações com `await`. |
| Atualização parcial | `exclude_unset=True` mantém os campos que não foram enviados no `PATCH`. |
| Preservação de registros | A exclusão lógica altera `ativo` para `false`, sem remover a linha do banco. |

<a id="executar-localmente"></a>

## 03 / Do código à execução

**Pré-requisitos:** Python 3 compatível com as dependências, `pip` e uma instância MySQL acessível. Execute os comandos a partir da raiz do projeto.

**1. Crie e ative um ambiente virtual.**

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source venv/bin/activate
```

**2. Instale as dependências.**

```bash
python -m pip install -r requirements.txt
```

**3. Prepare o banco.**

Em uma instalação nova, execute [`Schema.sql`](Schema.sql) pelo cliente MySQL ou por uma ferramenta de administração. O script cria o banco `ong_futebol`, suas quatro tabelas e os índices.

Exemplo dentro do cliente MySQL, aberto na raiz do projeto:

```sql
SOURCE Schema.sql;
```

O usuário que executar o script precisa de permissão para criar o banco, as tabelas e os índices. O script não é uma migração versionada: executá-lo novamente pode gerar erros nos índices já existentes. A aplicação não cria as tabelas automaticamente na inicialização.

**4. Configure o ambiente.**

Crie ou ajuste o arquivo `.env` na raiz. Os valores abaixo são exemplos; substitua as credenciais pela configuração do seu MySQL.

```dotenv
PROJECT_NAME="ONG Valentes de Davi Backend API"
VERSION="V.0.0.1"
API_V1_STR="/api/v1"
DATABASE_URL="mysql+aiomysql://seu_usuario:sua_senha@localhost:3306/ong_futebol"
```

| Variável | Finalidade |
| --- | --- |
| `PROJECT_NAME` | Nome exibido na documentação e no healthcheck |
| `VERSION` | Versão informada pela API |
| `API_V1_STR` | Prefixo das rotas de negócio e do esquema OpenAPI |
| `DATABASE_URL` | Conexão MySQL com o driver `aiomysql` |

Mantenha credenciais reais fora do Git. Caracteres reservados no usuário ou na senha precisam de codificação de URL na string de conexão.

**5. Inicie a API.**

```bash
python -m uvicorn app.main:app --reload
```

| Acesso local | Endereço padrão |
| --- | --- |
| Healthcheck | <http://127.0.0.1:8000/> |
| Swagger UI | <http://127.0.0.1:8000/docs> |
| ReDoc | <http://127.0.0.1:8000/redoc> |
| OpenAPI JSON | <http://127.0.0.1:8000/api/v1/openapi.json> |

O healthcheck informa o estado da aplicação, o nome do projeto, a versão e o caminho da documentação. Ele não verifica a conexão com o banco de dados.

<a id="endpoints-de-assistidos"></a>

## 04 / Contrato da API

Os caminhos abaixo consideram o prefixo padrão `/api/v1`.

| Método | Caminho declarado | Operação | Sucesso previsto |
| --- | --- | --- | --- |
| `POST` | `/api/v1/assistido/` | Cadastrar assistido | `201` |
| `GET` | `/api/v1/assistido/` | Listar assistidos | `200` |
| `GET` | `/api/v1/assistido/{assitido_id}` | Consultar por ID | `200` |
| `PATCH` | `/api/v1/assistido/{assitido_id}` | Atualizar parcialmente | `200` |
| `DELETE` | `/api/v1/assistido/{assitido_id}` | Desativar sem apagar o registro | `204` |

Parâmetros da listagem:

| Parâmetro | Padrão | Descrição |
| --- | --- | --- |
| `skip` | `0` | Quantidade de registros a ignorar |
| `limit` | `100` | Quantidade máxima de registros retornados |
| `apenas_ativos` | `true` | Retorna apenas ativos; `false` inclui ativos e inativos |

Exemplo: `GET /api/v1/assistido/?skip=0&limit=20&apenas_ativos=true`.

Exemplo de corpo para cadastro, com dados fictícios:

```json
{
  "nome_completo": "Aluno de Exemplo",
  "data_nascimento": "2013-05-20",
  "nome_responsavel": "Responsável de Exemplo",
  "telefone_responsavel": "11999990000",
  "posicao_campo": "Atacante"
}
```

O CPF é opcional. Nome completo, data de nascimento, nome e telefone do responsável são obrigatórios. A resposta inclui `id`, `ativo`, `criado_em` e `atualizado_em`. Os schemas validam tipos e limites de tamanho; não há validação dos dígitos verificadores do CPF.

---

<a id="english"></a>

## 05 / English documentation

<details>
<summary><strong>Read the full documentation in English</strong></summary>

[Voltar ao português / Back to Portuguese](#portugues)

### About

Backend for the Valentes de Davi football NGO management system, developed as an academic integration project. It uses FastAPI, Pydantic validation and asynchronous MySQL access through SQLAlchemy and aiomysql.

The project is in early development. The API currently focuses on beneficiaries/students, called **assistidos** in the code. The database schema also includes volunteers, classes/training sessions and attendance, whose APIs have not been implemented yet.

### Current status

| Feature | Status |
| --- | --- |
| Student registration | Implemented, with a duplicate CPF check when provided |
| Student listing | Implemented, with `skip`/`limit` pagination and an `apenas_ativos` filter |
| Fetch, partial update and deactivation by ID | Routes and services defined in the student module |
| Soft deletion | Service implemented; preserves the record and sets `ativo=false` |
| API documentation | Swagger UI, ReDoc and OpenAPI schema |
| Volunteers, classes and attendance | Tables in `Schema.sql`; no API modules yet |
| Authentication and authorization | Not implemented yet |
| Automated tests and versioned migrations | Not included yet |

### Technology and architecture

| Technology | Purpose |
| --- | --- |
| Python | Application language |
| FastAPI | HTTP routes and automatic API documentation |
| Uvicorn | ASGI server |
| SQLAlchemy 2 | ORM mapping and asynchronous sessions |
| MySQL + aiomysql | Persistence and asynchronous driver |
| Pydantic 2 + pydantic-settings | Data validation and environment configuration |
| python-dotenv | Support for loading `.env` variables |

Dependencies and minimum versions are listed in [`requirements.txt`](requirements.txt).

The application follows **routes → services → models/database**, with Pydantic schemas for request and response data. See the [project structure](#estrutura) above: `app/main.py` defines the application, `app/core/` holds configuration and database access, and `app/modules/assistidos/` contains the student module.

### Local setup

**Requirements:** Python 3 compatible with the dependencies, `pip` and an accessible MySQL instance. Run commands from the project root.

**1. Create and activate a virtual environment.**

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source venv/bin/activate
```

**2. Install dependencies.**

```bash
python -m pip install -r requirements.txt
```

**3. Initialize the database.**

For a fresh installation, run [`Schema.sql`](Schema.sql) using the MySQL client or a database administration tool. It creates the `ong_futebol` database, its four tables and indexes.

Inside the MySQL client, launched from the project root:

```sql
SOURCE Schema.sql;
```

The database user needs permission to create the database, tables and indexes. This script is not a versioned migration: running it again may fail on existing indexes. The application does not create tables automatically at startup.

**4. Configure the environment.**

Create or update `.env` in the project root. These are example values; replace the credentials with your MySQL configuration.

```dotenv
PROJECT_NAME="ONG Valentes de Davi Backend API"
VERSION="V.0.0.1"
API_V1_STR="/api/v1"
DATABASE_URL="mysql+aiomysql://your_user:your_password@localhost:3306/ong_futebol"
```

| Variable | Purpose |
| --- | --- |
| `PROJECT_NAME` | Name displayed in the documentation and healthcheck |
| `VERSION` | Version reported by the API |
| `API_V1_STR` | Prefix for business routes and the OpenAPI schema |
| `DATABASE_URL` | MySQL connection using the `aiomysql` driver |

Keep real credentials out of Git. Reserved characters in the username or password must be URL-encoded in the connection string.

**5. Start the API.**

```bash
python -m uvicorn app.main:app --reload
```

| Local resource | Default URL |
| --- | --- |
| Healthcheck | <http://127.0.0.1:8000/> |
| Swagger UI | <http://127.0.0.1:8000/docs> |
| ReDoc | <http://127.0.0.1:8000/redoc> |
| OpenAPI JSON | <http://127.0.0.1:8000/api/v1/openapi.json> |

The healthcheck reports application status, project name, version and documentation path. It does not check database connectivity.

### Student endpoints

Paths below use the default `/api/v1` prefix. API field names remain in Portuguese.

| Method | Declared path | Operation | Intended success status |
| --- | --- | --- | --- |
| `POST` | `/api/v1/assistido/` | Register a student | `201` |
| `GET` | `/api/v1/assistido/` | List students | `200` |
| `GET` | `/api/v1/assistido/{assitido_id}` | Fetch by ID | `200` |
| `PATCH` | `/api/v1/assistido/{assitido_id}` | Partially update | `200` |
| `DELETE` | `/api/v1/assistido/{assitido_id}` | Deactivate without removing the record | `204` |

List query parameters:

| Parameter | Default | Description |
| --- | --- | --- |
| `skip` | `0` | Number of records to skip |
| `limit` | `100` | Maximum number of returned records |
| `apenas_ativos` | `true` | Only active records; `false` includes active and inactive records |

Example: `GET /api/v1/assistido/?skip=0&limit=20&apenas_ativos=true`.

Example registration body using fictional data:

```json
{
  "nome_completo": "Example Student",
  "data_nascimento": "2013-05-20",
  "nome_responsavel": "Example Guardian",
  "telefone_responsavel": "11999990000",
  "posicao_campo": "Atacante"
}
```

CPF (Brazilian individual taxpayer ID) is optional. The student's full name, birth date, guardian's name and guardian's phone number are required. Responses include `id`, `ativo`, `criado_em` and `atualizado_em`. Schemas validate types and length constraints; CPF check digits are not validated.

</details>

---

<p align="center">
  <strong>VALENTES DE DAVI</strong><br>
  <sub>Futebol, comunidade e tecnologia · Projeto Integrador</sub><br><br>
  <a href="#top">Voltar ao início / Back to top</a>
</p>
