<a id="top"></a>

<p align="center">
  <img src="docs/assets/readme-cover.svg" alt="Valentes de Davi — Futebol, comunidade e tecnologia. Backend com Python, FastAPI e MySQL." width="100%">
</p>

<p align="center"><sub>DOCUMENTAÇÃO DO SISTEMA &nbsp; / &nbsp; BACKEND &nbsp; / &nbsp; PROJETO INTEGRADOR</sub></p>

<h1 align="center">Da comunidade à organização.</h1>

<p align="center">
  A base de dados por trás de um projeto que começa em campo.<br>
  API da ONG Valentes de Davi para a gestão de assistidos, voluntários e aulas.
</p>

<p align="center">
  <strong>Projeto Integrador</strong> &nbsp; / &nbsp; Em desenvolvimento &nbsp; / &nbsp; Python · FastAPI · MySQL
</p>

<p align="center">
  <a href="#portugues">O projeto</a> &nbsp; · &nbsp;
  <a href="#tecnologias">Engenharia</a> &nbsp; · &nbsp;
  <a href="#executar-localmente">Execução local</a> &nbsp; · &nbsp;
  <a href="#contrato-api">API</a> &nbsp; · &nbsp;
  <a href="#english">English</a>
</p>

<p align="center">
  <img src="docs/assets/readme-overview.svg" alt="03 módulos: assistidos, voluntários e aulas. 15 operações de negócio. 04 tabelas MySQL com ORM assíncrono." width="100%">
</p>

### Guia de leitura

| Capítulo | Conteúdo |
| :--- | :--- |
| [01 / Visão do sistema](#portugues) | Contexto, módulos disponíveis e estágio do projeto |
| [02 / Arquitetura](#tecnologias) | Tecnologias, estrutura e responsabilidades |
| [03 / Modelo de dados](#modelo-de-dados) | Entidades, vínculos e regras de exclusão |
| [04 / Ambiente local](#executar-localmente) | Instalação, banco de dados e configuração |
| [05 / Referência da API](#contrato-api) | Rotas, contratos, exemplos e respostas |
| [06 / English](#english) | Technical documentation in English |

---

<a id="portugues"></a>

## <img src="docs/assets/readme-section-01.svg" alt="01 / Visão do sistema" width="100%">

> **Futebol, comunidade e tecnologia.** Uma base para organizar quem participa, quem ensina e o que acontece em campo.

Este backend oferece a base para organizar os dados dos assistidos (alunos), dos voluntários (equipe e treinadores) e das aulas da ONG Valentes de Davi. A aplicação utiliza FastAPI, validação com Pydantic e acesso assíncrono ao MySQL por meio do SQLAlchemy e do driver aiomysql.

O projeto está em desenvolvimento. Assistidos, voluntários e aulas possuem rotas, serviços, schemas e modelos ORM próprios, registrados na aplicação. O controle de chamadas já está modelado no banco e ainda não possui módulo de API.

### O que já existe

| Recurso | Situação |
| --- | --- |
| Cadastro de assistidos | Implementado, com verificação de CPF duplicado quando informado |
| Listagem de assistidos | Implementada, com paginação por `skip` e `limit` e filtro `apenas_ativos` |
| Consulta, atualização parcial e desativação por ID | Rotas e serviços definidos no módulo de assistidos |
| Cadastro de voluntários | Implementado, com validação de formato do e-mail e verificação de e-mail duplicado |
| Listagem de voluntários | Implementada, com paginação por `skip` e `limit` e filtro `apenas_ativos` |
| Consulta, atualização parcial e desativação de voluntários por ID | Rotas e serviços implementados, com resposta `404` para ID inexistente |
| Exclusão lógica | Implementada em assistidos e voluntários; preserva o registro e define `ativo=false` |
| Agendamento de aulas | Implementado, com vínculo a um voluntário existente e ativo |
| Listagem e consulta de aulas | Paginação e dados do voluntário na resposta; listagem por data/hora decrescente |
| Atualização e exclusão de aulas | Atualização parcial e exclusão definitiva do registro |
| Documentação da API | Swagger UI, ReDoc e esquema OpenAPI |
| Chamadas / presença | Tabela e relacionamentos definidos em `Schema.sql`; sem módulo de API |
| Autenticação e autorização | Ainda não implementadas |
| Testes automatizados e migrações versionadas | Ainda não incluídos |

<a id="tecnologias"></a>

---

## <img src="docs/assets/readme-section-02.svg" alt="02 / Arquitetura" width="100%">

| Tecnologia | Uso |
| --- | --- |
| Python | Linguagem da aplicação |
| FastAPI | Rotas HTTP e documentação automática |
| Uvicorn | Servidor ASGI |
| SQLAlchemy 2 | Mapeamento ORM e sessões assíncronas |
| MySQL + aiomysql | Persistência e driver assíncrono |
| Pydantic 2 + pydantic-settings | Validação dos dados e configurações de ambiente |
| email-validator | Validação de e-mails pelo tipo `EmailStr` do Pydantic |
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
│       ├── assistidos/
│       │   ├── models.py        # Modelo ORM de alunos
│       │   ├── schemas.py       # Contratos de entrada e saída
│       │   ├── service.py       # Operações de persistência
│       │   └── router.py        # Endpoints de assistidos
│       ├── voluntarios/
│       │   ├── models.py        # Modelo ORM de equipe/treinadores
│       │   ├── schemas.py       # Contratos e validação de e-mail
│       │   ├── service.py       # Operações de persistência
│       │   └── router.py        # Endpoints de voluntários
│       └── aulas/
│           ├── models.py        # Aula e vínculo com voluntário
│           ├── schemas.py       # Contratos e resposta com responsável
│           ├── service.py       # Agendamento, consultas e exclusão
│           └── router.py        # Endpoints de aulas/treinos
├── docs/assets/                # Capa e captura da documentação
├── requirements.txt
├── Schema.sql                  # Criação do banco, tabelas e índices
└── README.md
```

Os três módulos seguem a mesma separação entre interface HTTP, operações de persistência e contratos de dados:

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
| Organização por domínio | Assistidos, voluntários e aulas agrupam suas próprias rotas, schemas, modelo e serviço. |
| Persistência assíncrona | Serviços usam `AsyncSession` e operações com `await`. |
| Atualização parcial | `exclude_unset=True` mantém os campos que não foram enviados no `PATCH`. |
| Preservação de cadastros | Assistidos e voluntários usam exclusão lógica, alterando `ativo` para `false`. |
| Responsável pela aula | O serviço de aulas consulta o serviço de voluntários antes de cadastrar ou trocar o responsável. |
| Carregamento de relacionamentos | Consultas de aulas carregam o voluntário com `joinedload` para compor a resposta. |

---

<a id="modelo-de-dados"></a>

## <img src="docs/assets/readme-section-03.svg" alt="03 / Modelo de dados" width="100%">

O banco `ong_futebol` reúne quatro entidades. A relação entre aulas e voluntários já é utilizada pela API; as relações de presença estão definidas no [esquema SQL](Schema.sql).

```mermaid
flowchart LR
    V["VOLUNTÁRIOS<br/>Equipe e treinadores"] -->|"1 : N · responsável"| A["AULAS<br/>Agenda e local"]
    A -->|"1 : N"| C["CHAMADAS<br/>Presença por aula"]
    S["ASSISTIDOS<br/>Alunos e responsáveis"] -->|"1 : N"| C
    classDef implemented fill:#102C25,stroke:#C8DB95,color:#F2EEDF,stroke-width:2px;
    classDef planned fill:#F2EEDF,stroke:#102C25,color:#102C25,stroke-dasharray:5 5;
    class V,A,S implemented;
    class C planned;
```

<p align="center"><sub>Verde: entidades com módulo de API · Marfim: entidade definida no banco</sub></p>

| Entidade | Identificação e vínculos | Exclusão |
| :--- | :--- | :--- |
| `assistidos` | CPF opcional e único; dados do aluno e responsável | Lógica pela API: `ativo=false` |
| `voluntarios` | E-mail único; pode ser responsável por várias aulas | Lógica pela API: `ativo=false` |
| `aulas` | Título, data/hora, local e `voluntario_id` obrigatório | Definitiva pela API |
| `chamadas` | Par único `aula_id` + `assistido_id`; presença e observação | O SQL prevê exclusão em cascata ao remover a aula ou o assistido |

O vínculo da aula impede a exclusão física do voluntário referenciado (`ON DELETE RESTRICT`). A desativação de um voluntário preserva as aulas existentes; o cadastro de uma aula e a troca de responsável exigem um voluntário ativo.

---

<a id="executar-localmente"></a>

## <img src="docs/assets/readme-section-04.svg" alt="04 / Ambiente local" width="100%">

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
<a id="contrato-api"></a>

---

## <img src="docs/assets/readme-section-05.svg" alt="05 / Referência da API" width="100%">

**Base das rotas:** `/api/v1` &nbsp; · &nbsp; **Formato:** JSON &nbsp; · &nbsp; **Contratos:** OpenAPI

[Assistidos](#api-assistidos) &nbsp; / &nbsp; [Voluntários](#api-voluntarios) &nbsp; / &nbsp; [Aulas](#api-aulas) &nbsp; / &nbsp; [Respostas](#respostas)

### Documentação interativa

A interface Swagger UI, disponível em `/docs` com a API em execução, reúne assistidos, voluntários e aulas e permite consultar os contratos e enviar requisições.

<details>
<summary><strong>Ver capturas da documentação — assistidos e voluntários</strong></summary>

<p align="center">
  <a href="docs/assets/image.png">
    <img src="docs/assets/image.png" alt="Swagger UI da ONG Valentes de Davi com os endpoints de cadastro, listagem, consulta, atualização e desativação de assistidos." width="100%">
  </a>
  <br>
  <a href="docs/assets/image2.png">
    <img src="docs/assets/image2.png" alt="Swagger UI da ONG Valentes de Davi com os endpoints de cadastro, listagem, consulta, atualização e desativação de voluntários." width="100%">
  </a>
</p>

</details>

<a id="api-assistidos"></a>

### <img src="docs/assets/readme-section-05-1.svg" alt="05.1 / Assistidos" width="100%">

<sub>ALUNOS E RESPONSÁVEIS &nbsp; / &nbsp; CADASTRO E ACOMPANHAMENTO</sub>

Os caminhos abaixo consideram o prefixo padrão `/api/v1`.

| Método | Caminho declarado | Operação | Sucesso previsto |
| --- | --- | --- | --- |
| `POST` | `/api/v1/assistido/` | Cadastrar assistido | `201` |
| `GET` | `/api/v1/assistido/` | Listar assistidos | `200` |
| `GET` | `/api/v1/assistido/{assitido_id}` | Consultar por ID | `200` |
| `PATCH` | `/api/v1/assistido/{assitido_id}` | Atualizar parcialmente | `200` |
| `DELETE` | `/api/v1/assistido/{assitido_id}` | Desativar sem apagar o registro | `204` |

Parâmetros da listagem de assistidos:

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

<a id="api-voluntarios"></a>

### <img src="docs/assets/readme-section-05-2.svg" alt="05.2 / Voluntários" width="100%">

<sub>EQUIPE E TREINADORES &nbsp; / &nbsp; CADASTRO E VÍNCULO COM AULAS</sub>

Os caminhos usam o mesmo prefixo padrão `/api/v1`. O recurso é declarado no plural: `/voluntarios`.

| Método | Caminho declarado | Operação | Sucesso previsto |
| --- | --- | --- | --- |
| `POST` | `/api/v1/voluntarios/` | Cadastrar voluntário | `201` |
| `GET` | `/api/v1/voluntarios/` | Listar voluntários | `200` |
| `GET` | `/api/v1/voluntarios/{voluntario_id}` | Consultar por ID | `200` |
| `PATCH` | `/api/v1/voluntarios/{voluntario_id}` | Atualizar parcialmente | `200` |
| `DELETE` | `/api/v1/voluntarios/{voluntario_id}` | Desativar sem apagar o registro | `204` |

A listagem aceita `skip=0`, `limit=100` e `apenas_ativos=true`, com o mesmo significado dos parâmetros de assistidos. Exemplo: `GET /api/v1/voluntarios/?skip=0&limit=20&apenas_ativos=true`.

Exemplo de corpo para cadastro, com dados fictícios:

```json
{
  "nome_completo": "Voluntário de Exemplo",
  "email": "voluntario@example.com",
  "telefone": "11999990000",
  "funcao": "Treinador Sub-15"
}
```

Todos os campos do exemplo são obrigatórios. O nome aceita de 3 a 150 caracteres; o telefone, de 8 a 20; e a função, de 2 a 80. O e-mail é validado com `EmailStr`. A resposta acrescenta `id`, `ativo`, `criado_em` e `atualizado_em`.

---

<a id="api-aulas"></a>

### <img src="docs/assets/readme-section-05-3.svg" alt="05.3 / Aulas e treinos" width="100%">

<sub>AGENDA DE ATIVIDADES &nbsp; / &nbsp; RESPONSÁVEL, DATA E LOCAL</sub>

| Método | Caminho declarado | Operação | Sucesso previsto |
| --- | --- | --- | --- |
| `POST` | `/api/v1/aulas/` | Agendar aula com voluntário ativo | `201` |
| `GET` | `/api/v1/aulas/` | Listar aulas por data/hora decrescente | `200` |
| `GET` | `/api/v1/aulas/{aula_id}` | Consultar aula e responsável | `200` |
| `PATCH` | `/api/v1/aulas/{aula_id}` | Atualizar parcialmente | `200` |
| `DELETE` | `/api/v1/aulas/{aula_id}` | Excluir definitivamente | `204` |

A listagem aceita `skip=0` e `limit=100`. Retorna aulas de qualquer data, ordenadas por `data_hora` decrescente, e não utiliza o filtro `apenas_ativos`.

Exemplo: `GET /api/v1/aulas/?skip=0&limit=20`.

**Fluxo de cadastro:** cadastre um voluntário, copie o `id` retornado e informe esse valor em `voluntario_id`.

```json
{
  "titulo": "Treino Sub-13 Tático",
  "descricao": "Fundamentos de passe e posicionamento em campo.",
  "data_hora": "2026-11-07T09:00:00",
  "local": "Campo Principal",
  "voluntario_id": 1
}
```

| Campo | Contrato de cadastro |
| :--- | :--- |
| `titulo` | Obrigatório; de 3 a 100 caracteres |
| `descricao` | Opcional; texto ou `null` |
| `data_hora` | Obrigatório; data e hora, como no exemplo ISO 8601 |
| `local` | Obrigatório; de 2 a 150 caracteres |
| `voluntario_id` | Obrigatório; ID de voluntário existente e ativo |

A resposta acrescenta `id`, `criado_em`, `atualizado_em` e o objeto `voluntario`, com os dados do responsável. Ao enviar um novo `voluntario_id` no `PATCH`, o serviço também verifica se ele existe e está ativo.

**Exclusão de aulas:** o `DELETE` remove o registro do banco. No esquema SQL fornecido, chamadas vinculadas à aula também são removidas por `ON DELETE CASCADE`.

---

<a id="respostas"></a>

### <img src="docs/assets/readme-section-05-4.svg" alt="05.4 / Respostas e regras de operação" width="100%">

| Situação | Comportamento atual |
| --- | --- |
| CPF já cadastrado no `POST` de assistidos | Resposta `400` quando o CPF é informado e já existe |
| E-mail já cadastrado no `POST` de voluntários | Resposta `400` |
| Registro inexistente em consulta, atualização ou desativação | Resposta `404`, desde que os parâmetros da requisição sejam válidos |
| Dados incompatíveis com os schemas | Resposta `422` de validação |
| Voluntário inexistente ou inativo no cadastro de aula | Resposta `400` |
| Aula inexistente ou novo responsável inexistente/inativo no `PATCH` de aula | Resposta `404` |
| `PATCH` | Atualiza somente os campos enviados; assistidos e voluntários aceitam alterar `ativo` |
| `DELETE` de assistidos e voluntários | Define `ativo=false`, preserva os dados e retorna `204` sem corpo |
| `DELETE` de aulas | Remove o registro definitivamente e retorna `204` sem corpo |

A verificação explícita de duplicidade ocorre no cadastro. Os serviços de atualização não repetem essa consulta nem tratam conflitos de unicidade como uma resposta HTTP específica. Os parâmetros `skip` e `limit` também não possuem limites explícitos de validação nas rotas atuais.

---

<a id="english"></a>

## <img src="docs/assets/readme-section-06.svg" alt="06 / English documentation" width="100%">

<details>
<summary><strong>Read the full documentation in English</strong></summary>

[Voltar ao português / Back to Portuguese](#portugues)

### About

Backend for the Valentes de Davi football NGO management system, developed as an academic integration project. It uses FastAPI, Pydantic validation and asynchronous MySQL access through SQLAlchemy and aiomysql.

The project is in development. Students (**assistidos**), volunteers (**voluntarios**) and classes/training sessions (**aulas**) have API modules registered in the application, each with its own routes, services, schemas and ORM model. There are 15 business operations across these three modules. Attendance (**chamadas**) is defined in the database schema and does not yet have an API module.

### Current status

| Feature | Status |
| --- | --- |
| Student registration | Implemented, with a duplicate CPF check when provided |
| Student listing | Implemented, with `skip`/`limit` pagination and an `apenas_ativos` filter |
| Fetch, partial update and deactivation by ID | Routes and services defined in the student module |
| Volunteer registration | Implemented, with email format validation and a duplicate email check |
| Volunteer listing | Implemented, with `skip`/`limit` pagination and an `apenas_ativos` filter |
| Volunteer fetch, partial update and deactivation by ID | Implemented, with `404` responses for missing records |
| Soft deletion | Implemented for students and volunteers; preserves the record and sets `ativo=false` |
| Class scheduling | Implemented; requires an existing, active volunteer |
| Class listing and lookup | Paginated listing ordered by descending date/time; responses include volunteer data |
| Class update and deletion | Partial updates and permanent deletion |
| API documentation | Swagger UI, ReDoc and OpenAPI schema |
| Attendance | Table and relationships in `Schema.sql`; no API module yet |
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
| email-validator | Email validation through Pydantic's `EmailStr` type |
| python-dotenv | Support for loading `.env` variables |

Dependencies and minimum versions are listed in [`requirements.txt`](requirements.txt).

The application follows **routes → services → models/database**, with Pydantic schemas for request and response data. See the [project structure](#estrutura) above: `app/main.py` registers all three routers, `app/core/` holds configuration and database access, and `app/modules/` contains `assistidos/`, `voluntarios/` and `aulas/`. All use asynchronous sessions and partial updates with `exclude_unset=True`. Students and volunteers use soft deletion; classes use permanent deletion. Class queries load the volunteer relationship with `joinedload`.

### Data model

The [SQL schema](Schema.sql) defines four tables: `assistidos`, `voluntarios`, `aulas` and `chamadas`. Each class references one volunteer; each attendance record links one student to one class, with a unique constraint on that pair.

The class foreign key prevents physical deletion of a referenced volunteer (`ON DELETE RESTRICT`). Deactivating a volunteer preserves existing classes. Deleting a class permanently also removes related attendance records through the SQL schema's `ON DELETE CASCADE`.

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

### Volunteer endpoints

Paths use the default `/api/v1` prefix. The resource name is plural: `/voluntarios`. API field names remain in Portuguese.

| Method | Declared path | Operation | Intended success status |
| --- | --- | --- | --- |
| `POST` | `/api/v1/voluntarios/` | Register a volunteer | `201` |
| `GET` | `/api/v1/voluntarios/` | List volunteers | `200` |
| `GET` | `/api/v1/voluntarios/{voluntario_id}` | Fetch by ID | `200` |
| `PATCH` | `/api/v1/voluntarios/{voluntario_id}` | Partially update | `200` |
| `DELETE` | `/api/v1/voluntarios/{voluntario_id}` | Deactivate without removing the record | `204` |

Listing supports `skip=0`, `limit=100` and `apenas_ativos=true`, with the same meaning as the student listing parameters. Example: `GET /api/v1/voluntarios/?skip=0&limit=20&apenas_ativos=true`.

Example registration body using fictional data:

```json
{
  "nome_completo": "Example Volunteer",
  "email": "volunteer@example.com",
  "telefone": "11999990000",
  "funcao": "Treinador Sub-15"
}
```

All four fields are required. Name length is 3–150 characters, phone length is 8–20, and role length is 2–80. Email format is validated using `EmailStr`. Responses also include `id`, `ativo`, `criado_em` and `atualizado_em`.

### Class endpoints

| Method | Declared path | Operation | Intended success status |
| --- | --- | --- | --- |
| `POST` | `/api/v1/aulas/` | Schedule a class with an active volunteer | `201` |
| `GET` | `/api/v1/aulas/` | List classes by descending date/time | `200` |
| `GET` | `/api/v1/aulas/{aula_id}` | Fetch a class and its volunteer | `200` |
| `PATCH` | `/api/v1/aulas/{aula_id}` | Partially update | `200` |
| `DELETE` | `/api/v1/aulas/{aula_id}` | Permanently delete | `204` |

Listing accepts `skip=0` and `limit=100`, returns classes from any date and does not use `apenas_ativos`. Example: `GET /api/v1/aulas/?skip=0&limit=20`.

Register a volunteer first and use the returned ID as `voluntario_id`:

```json
{
  "titulo": "Under-13 tactical training",
  "descricao": "Passing and positioning practice.",
  "data_hora": "2026-11-07T09:00:00",
  "local": "Main field",
  "voluntario_id": 1
}
```

Title (3–100 characters), date/time, location (2–150 characters) and volunteer ID are required. Description is optional. The volunteer must exist and be active, both at creation and when assigning a new volunteer through `PATCH`.

Responses also include `id`, `criado_em`, `atualizado_em` and a nested `voluntario` object with the responsible volunteer's data. Class deletion is permanent; the supplied SQL schema cascades deletion to related attendance records.

### Behavior and validation

| Situation | Current behavior |
| --- | --- |
| Existing CPF on student registration | `400` when the provided CPF already exists |
| Existing email on volunteer registration | `400` |
| Missing record on fetch, update or deactivation | `404`, provided the request parameters are valid |
| Data that does not match the schemas | `422` validation response |
| Missing or inactive volunteer on class creation | `400` |
| Missing class or missing/inactive replacement volunteer on class update | `404` |
| `PATCH` | Updates only submitted fields; students and volunteers accept changes to `ativo` |
| Student and volunteer `DELETE` | Sets `ativo=false`, preserves the record and returns `204` with no body |
| Class `DELETE` | Permanently removes the record and returns `204` with no body |

Explicit duplicate checks occur during registration. Update services do not repeat these checks or translate uniqueness conflicts into a specific HTTP response. Current routes also do not set explicit validation bounds for `skip` and `limit`.

</details>

---

<p align="center">
  <strong>VALENTES DE DAVI</strong><br>
  <sub>Futebol, comunidade e tecnologia</sub><br>
  <sub>DOCUMENTAÇÃO DO BACKEND &nbsp; / &nbsp; PROJETO EM DESENVOLVIMENTO</sub><br><br>
  <a href="#top">Voltar ao início / Back to top</a>
</p>
