---
layout: home
title: Sistema de Acompanhamento de Dietas
---

# Sistema de Acompanhamento de Dietas - NoSQL

Um sistema de banco de dados NoSQL para nutricionistas acompanharem a dieta dos seus pacientes, utilizando Neo4j (banco
de grafos) e MongoDB (banco de documentos).

## Índice

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Modelo de Dados](#modelo-de-dados)
  - [Modelo de Grafos (Neo4j)](#modelo-de-grafos-neo4j)
  - [Modelo de Documentos (MongoDB)](#modelo-de-documentos-mongodb)
- [Consultas](#consultas)
  - [Consultas Neo4j (Cypher)](#consultas-neo4j-cypher)
  - [Consultas MongoDB](#consultas-mongodb)
- [Configuração e Execução](#configuração-e-execução)
- [Dump do Banco](#dump-do-banco)

## Visão Geral

Este projeto implementa um sistema de acompanhamento de dietas que permite:

- Gerenciar pacientes e nutricionistas
- Registrar planos alimentares e refeições
- Acompanhar medidas corporais
- Monitorar a adesão às dietas
- Facilitar a comunicação entre paciente e nutricionista
- Sugerir receitas adequadas às restrições alimentares

O sistema utiliza dois tipos de SGBDs NoSQL:

- **Neo4j**: banco de dados de grafos para modelar os relacionamentos complexos entre entidades
- **MongoDB**: banco de documentos para armazenar informações complexas aninhadas

## Estrutura do Projeto

```
sistema-acompanhamento-dietas/
├── .github/workflows/                 # Workflows CI/CD e GitHub Pages
├── docs/                              # Documentação
├── dumps/                             # Diretório para dumps
├── scripts/                           # Scripts Python
├── docker-compose.yml                 # Configuração Docker
├── Makefile                           # Automação de tarefas
├── requirements.txt                   # Dependências Python
└── README.md                          # Documentação principal
```

## Modelo de Dados

O sistema utiliza dois modelos de dados diferentes para explorar as capacidades de cada tipo de banco de dados NoSQL.

### Modelo de Grafos (Neo4j)

O modelo de grafos representa entidades como nós e relacionamentos como arestas, permitindo modelar de forma natural as relações complexas entre nutricionistas, pacientes, planos alimentares, etc.

[Ver detalhes do Modelo de Grafos](modelagem/grafos)

### Modelo de Documentos (MongoDB)

O modelo de documentos organiza os dados em coleções de documentos JSON, permitindo armazenar estruturas aninhadas e flexíveis.

[Ver detalhes do Modelo de Documentos](modelagem/documentos)

## Consultas

O sistema implementa diversas consultas para demonstrar as capacidades de cada banco de dados.

### Consultas Neo4j (Cypher)

Consultas em linguagem Cypher que exploram as capacidades do Neo4j para navegação em grafos e análise de relacionamentos.

[Ver detalhes das Consultas Neo4j](consultas/neo4j)

### Consultas MongoDB

Consultas utilizando a API de agregação e consultas do MongoDB que exploram as capacidades de armazenamento e recuperação de documentos.

[Ver detalhes das Consultas MongoDB](consultas/mongodb)

## Configuração e Execução

### Pré-requisitos

- Docker e Docker Compose
- Python 3.7+
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório ou copie os arquivos para seu diretório de trabalho

2. Crie um ambiente virtual Python (opcional, mas recomendado)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate     # Windows
   ```

3. Instale as dependências
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o script de configuração completa (inicia os containers e carrega os dados)
   ```bash
   make setup
   make load
   ```

   Alternativamente, você pode executar:
   ```bash
   python load_all_databases.py
   ```

5. Acesse as interfaces web:
    - Neo4j Browser: http://localhost:7474
        - Login: neo4j
        - Senha: senha123
    - MongoDB Express: http://localhost:8081
        - Login: admin
        - Senha: senha123

## Dump do Banco

Para criar dumps dos bancos de dados, utilize o comando:

```bash
make dump
```

Ou para cada banco individualmente:

```bash
make dump-neo4j    # Apenas Neo4j
make dump-mongodb  # Apenas MongoDB
```

Os dumps serão armazenados no diretório `dumps/`.