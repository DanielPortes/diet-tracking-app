# Sistema de Acompanhamento de Dietas - NoSQL

Um sistema de banco de dados NoSQL para nutricionistas acompanharem a dieta dos seus pacientes, utilizando Neo4j (banco
de grafos) e MongoDB (banco de documentos).

## Índice

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração e Execução](#configuração-e-execução)
- [Modelo de Dados](#modelo-de-dados)
    - [Modelo de Grafos (Neo4j)](#modelo-de-grafos-neo4j)
    - [Modelo de Documentos (MongoDB)](#modelo-de-documentos-mongodb)
- [Consultas](#consultas)
    - [Consultas Neo4j (Cypher)](#consultas-neo4j-cypher)
    - [Consultas MongoDB](#consultas-mongodb)
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
diet-tracking-app/
├── docker-compose.yml       # Configuração dos containers Docker (Neo4j e MongoDB)
├── load_data.py             # Script para carregar dados no Neo4j
├── load_mongodb_data.py     # Script para carregar dados no MongoDB
├── load_all_databases.py    # Script para configurar ambos os bancos
├── requirements.txt         # Dependências Python
└── README.md                # Este arquivo
```

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
   python load_all_databases.py
   ```

   Alternativamente, você pode executar cada etapa manualmente:

   ```bash
   # Inicie os containers Docker
   docker-compose up -d

   # Aguarde alguns segundos para os serviços iniciarem
   sleep 30

   # Carregue os dados no Neo4j
   python load_data.py

   # Carregue os dados no MongoDB
   python load_mongodb_data.py
   ```

5. Acesse as interfaces web:
    - Neo4j Browser: http://localhost:7474
        - Login: neo4j
        - Senha: senha123
    - MongoDB Express: http://localhost:8081
        - Login: admin
        - Senha: senha123

## Modelo de Dados

### Modelo de Grafos (Neo4j)

O modelo de grafos representa entidades como nós e relacionamentos como arestas.

#### Nós (Entidades)

- **Nutricionista**: Profissionais que orientam os pacientes
- **Paciente**: Pessoas que buscam orientação nutricional
- **PlanoAlimentar**: Dietas elaboradas para os pacientes
- **Alimento**: Itens alimentares básicos com informações nutricionais
- **Receita**: Combinações de alimentos com instruções de preparo
- **Refeicao**: Registros de alimentação dos pacientes
- **MedidaCorporal**: Histórico de medições (peso, IMC, etc.)
- **Mensagem**: Comunicações entre nutricionistas e pacientes
- **Consulta**: Agendamentos de atendimentos

#### Relacionamentos

- **ATENDE**: Nutricionista → Paciente
- **CRIA**: Nutricionista → PlanoAlimentar
- **SEGUE**: Paciente → PlanoAlimentar
- **INCLUI**: PlanoAlimentar → Alimento
- **RECOMENDA**: PlanoAlimentar → Receita
- **CONTEM**: Receita → Alimento
- **CONSOME**: Paciente → Refeicao
- **INCLUI**: Refeicao → (Alimento | Receita)
- **POSSUI**: Paciente → MedidaCorporal
- **ENVIA**: (Nutricionista | Paciente) → Mensagem
- **PARA**: Mensagem → (Nutricionista | Paciente)
- **AGENDA**: Paciente → Consulta
- **COM**: Consulta → Nutricionista

### Modelo de Documentos (MongoDB)

O modelo de documentos organiza os dados em coleções de documentos JSON.

#### Coleções

1. **nutritionists**: Informações dos nutricionistas
2. **patients**: Dados dos pacientes, incluindo referência ao nutricionista
3. **foods**: Cadastro de alimentos com informações nutricionais
4. **recipes**: Receitas com ingredientes e instruções
5. **dietPlans**: Planos alimentares com referências a pacientes, nutricionistas e alimentos/receitas recomendados
6. **meals**: Refeições consumidas pelos pacientes
7. **measurements**: Histórico de medidas corporais dos pacientes
8. **messages**: Comunicações entre pacientes e nutricionistas
9. **appointments**: Consultas agendadas e realizadas

## Consultas

### Consultas Neo4j (Cypher)

#### 1. Encontrar todos os pacientes de um nutricionista específico

```cypher
MATCH (n:Nutricionista {nome: "Ana Silva"})-[:ATENDE]->(p:Paciente)
RETURN n.nome AS Nutricionista, p.nome AS Paciente, p.objetivo AS Objetivo
```

#### 2. Encontrar todas as refeições de um paciente em um período específico

```cypher
MATCH (p:Paciente {nome: "João Pereira"})-[:CONSOME]->(r:Refeicao)
WHERE r.data >= "2023-10-18" AND r.data <= "2023-10-19"
RETURN p.nome AS Paciente, r.tipo AS TipoRefeicao, r.data AS Data,
       r.calorias AS Calorias, r.adesao AS Adesao
ORDER BY r.data, r.hora
```

#### 3. Calcular a soma de calorias consumidas por um paciente em um dia

```cypher
MATCH (p:Paciente {nome: "João Pereira"})-[:CONSOME]->(r:Refeicao)
WHERE r.data = "2023-10-18"
RETURN p.nome AS Paciente, r.data AS Data, SUM(r.calorias) AS TotalCalorias
```

#### 4. Encontrar receitas adequadas para pacientes com restrições alimentares

```cypher
MATCH (p:Paciente)-[:SEGUE]->(pa:PlanoAlimentar)-[:RECOMENDA]->(r:Receita)
WHERE "Glúten" IN p.restricoes
RETURN p.nome AS Paciente, r.nome AS ReceitaAdequada, r.calorias AS Calorias
```

#### 5. Identificar pacientes com baixa adesão ao plano alimentar

```cypher
MATCH (p:Paciente)-[:CONSOME]->(r:Refeicao)
WITH p, COUNT(r) AS totalRefeicoes,
     SUM(CASE WHEN r.adesao = "Completa" THEN 1 ELSE 0 END) AS refeicoesCompletas
WHERE (refeicoesCompletas * 1.0 / totalRefeicoes) < 0.8
RETURN p.nome AS Paciente, totalRefeicoes, refeicoesCompletas,
       (refeicoesCompletas * 1.0 / totalRefeicoes) AS TaxaAdesao
ORDER BY TaxaAdesao
```

#### 6. Rastrear o progresso de um paciente analisando medidas corporais

```cypher
MATCH (p:Paciente {nome: "João Pereira"})-[:POSSUI]->(m:MedidaCorporal)
RETURN p.nome AS Paciente, m.data AS Data, m.peso AS Peso, m.imc AS IMC,
       m.gordura_corporal AS GorduraCorporal, m.cintura AS Cintura
ORDER BY m.data
```

#### 7. Encontrar os alimentos mais recomendados nos planos alimentares

```cypher
MATCH (pa:PlanoAlimentar)-[:INCLUI]->(a:Alimento)
RETURN a.nome AS Alimento, a.grupo AS Grupo, COUNT(pa) AS NumeroDeRecomendacoes
ORDER BY NumeroDeRecomendacoes DESC
```

#### 8. Analisar a comunicação entre nutricionistas e pacientes

```cypher
MATCH (origem)-[:ENVIA]->(m:Mensagem)-[:PARA]->(destino)
WHERE origem:Nutricionista OR destino:Nutricionista
RETURN
  CASE
    WHEN origem:Nutricionista THEN origem.nome
    ELSE origem.nome
  END AS Remetente,
  CASE
    WHEN destino:Nutricionista THEN destino.nome
    ELSE destino.nome
  END AS Destinatario,
  m.data AS Data, m.hora AS Hora, m.conteudo AS Mensagem
ORDER BY m.data, m.hora
```

#### 9. Encontrar receitas que contêm determinado alimento

```cypher
MATCH (r:Receita)-[:CONTEM]->(a:Alimento {nome: "Brócolis"})
RETURN r.nome AS Receita, r.calorias AS Calorias, r.dificuldade AS Dificuldade,
       r.tempo_preparo AS TempoPreparo
```

#### 10. Visualizar próximas consultas agendadas

```cypher
MATCH (p:Paciente)-[:AGENDA]->(c:Consulta {status: "Agendada"})-[:COM]->(n:Nutricionista)
RETURN p.nome AS Paciente, n.nome AS Nutricionista, c.data AS Data, c.hora AS Hora
ORDER BY c.data, c.hora
```

### Consultas MongoDB

#### 1. Encontrar todos os pacientes de um nutricionista específico

```javascript
db.patients.find(
    {nutricionista_id: 1},
    {nome: 1, idade: 1, objetivo: 1, _id: 0}
)
```

#### 2. Buscar todas as refeições de um paciente em um período específico

```javascript
db.meals.find(
    {
        paciente_id: 1,
        data: {
            $gte: ISODate("2023-10-18"),
            $lte: ISODate("2023-10-19")
        }
    },
    {tipo: 1, data: 1, hora: 1, calorias: 1, adesao: 1, _id: 0}
).sort({data: 1, hora: 1})
```

#### 3. Calcular total de calorias consumidas por dia

```javascript
db.meals.aggregate([
    {$match: {paciente_id: 1}},
    {
        $group: {
            _id: {$dateToString: {format: "%Y-%m-%d", date: "$data"}},
            totalCalorias: {$sum: "$calorias"}
        }
    },
    {$sort: {_id: 1}}
])
```

#### 4. Encontrar receitas adequadas para pacientes com restrições

```javascript
db.patients.aggregate([
    {$match: {restricoes: "Glúten"}},
    {
        $lookup: {
            from: "dietPlans",
            localField: "_id",
            foreignField: "paciente_id",
            as: "planos"
        }
    },
    {$unwind: "$planos"},
    {
        $lookup: {
            from: "recipes",
            localField: "planos.receitas_recomendadas",
            foreignField: "_id",
            as: "receitas"
        }
    },
    {$unwind: "$receitas"},
    {
        $project: {
            paciente: "$nome",
            receita: "$receitas.nome",
            calorias: "$receitas.calorias",
            _id: 0
        }
    }
])
```

#### 5. Identificar pacientes com baixa adesão ao plano alimentar

```javascript
db.meals.aggregate([
    {
        $group: {
            _id: "$paciente_id",
            totalRefeicoes: {$sum: 1},
            refeicoesCompletas: {
                $sum: {$cond: [{$eq: ["$adesao", "Completa"]}, 1, 0]}
            }
        }
    },
    {
        $project: {
            paciente_id: "$_id",
            totalRefeicoes: 1,
            refeicoesCompletas: 1,
            taxaAdesao: {$divide: ["$refeicoesCompletas", "$totalRefeicoes"]},
            _id: 0
        }
    },
    {$match: {taxaAdesao: {$lt: 0.8}}},
    {
        $lookup: {
            from: "patients",
            localField: "paciente_id",
            foreignField: "_id",
            as: "paciente"
        }
    },
    {$unwind: "$paciente"},
    {
        $project: {
            nome: "$paciente.nome",
            totalRefeicoes: 1,
            refeicoesCompletas: 1,
            taxaAdesao: 1
        }
    },
    {$sort: {taxaAdesao: 1}}
])
```

#### 6. Rastrear progresso corporal de um paciente

```javascript
db.measurements.find(
    {paciente_id: 1},
    {data: 1, peso: 1, imc: 1, gordura_corporal: 1, "medidas.cintura": 1, _id: 0}
).sort({data: 1})
```

#### 7. Encontrar alimentos mais recomendados nos planos alimentares

```javascript
db.dietPlans.aggregate([
    {$unwind: "$alimentos_recomendados"},
    {
        $group: {
            _id: "$alimentos_recomendados",
            contagem: {$sum: 1}
        }
    },
    {
        $lookup: {
            from: "foods",
            localField: "_id",
            foreignField: "_id",
            as: "alimento"
        }
    },
    {$unwind: "$alimento"},
    {
        $project: {
            nome: "$alimento.nome",
            grupo: "$alimento.grupo",
            recomendacoes: "$contagem",
            _id: 0
        }
    },
    {$sort: {recomendacoes: -1}}
])
```

#### 8. Analisar comunicação entre nutricionistas e pacientes

```javascript
db.messages.aggregate([
    {
        $lookup: {
            from: "nutritionists",
            localField: "de_id",
            foreignField: "_id",
            as: "nutricionista_de"
        }
    },
    {
        $lookup: {
            from: "patients",
            localField: "de_id",
            foreignField: "_id",
            as: "paciente_de"
        }
    },
    {
        $lookup: {
            from: "nutritionists",
            localField: "para_id",
            foreignField: "_id",
            as: "nutricionista_para"
        }
    },
    {
        $lookup: {
            from: "patients",
            localField: "para_id",
            foreignField: "_id",
            as: "paciente_para"
        }
    },
    {
        $project: {
            remetente: {
                $cond: {
                    if: {$eq: ["$de_tipo", "nutricionista"]},
                    then: {$arrayElemAt: ["$nutricionista_de.nome", 0]},
                    else: {$arrayElemAt: ["$paciente_de.nome", 0]}
                }
            },
            destinatario: {
                $cond: {
                    if: {$eq: ["$para_tipo", "nutricionista"]},
                    then: {$arrayElemAt: ["$nutricionista_para.nome", 0]},
                    else: {$arrayElemAt: ["$paciente_para.nome", 0]}
                }
            },
            data: 1,
            hora: 1,
            conteudo: 1,
            _id: 0
        }
    },
    {$sort: {data: 1, hora: 1}}
])
```

#### 9. Encontrar receitas que contêm determinado ingrediente

```javascript
db.recipes.aggregate([
    {$match: {"ingredientes.food_id": 4}},
    {
        $lookup: {
            from: "foods",
            localField: "ingredientes.food_id",
            foreignField: "_id",
            as: "alimentos"
        }
    },
    {$match: {"alimentos.nome": "Brócolis"}},
    {
        $project: {
            nome: 1,
            calorias: 1,
            dificuldade: 1,
            tempo_preparo: 1,
            _id: 0
        }
    }
])
```

#### 10. Visualizar próximas consultas agendadas

```javascript
db.appointments.aggregate([
    {$match: {status: "Agendada"}},
    {
        $lookup: {
            from: "patients",
            localField: "paciente_id",
            foreignField: "_id",
            as: "paciente"
        }
    },
    {
        $lookup: {
            from: "nutritionists",
            localField: "nutricionista_id",
            foreignField: "_id",
            as: "nutricionista"
        }
    },
    {$unwind: "$paciente"},
    {$unwind: "$nutricionista"},
    {
        $project: {
            paciente: "$paciente.nome",
            nutricionista: "$nutricionista.nome",
            data: 1,
            hora: 1,
            _id: 0
        }
    },
    {$sort: {data: 1, hora: 1}}
])
```

## Dump do Banco

### Neo4j

Para criar um dump do banco Neo4j:

```bash
docker exec diet_app_neo4j neo4j-admin dump --database=neo4j --to=/var/lib/neo4j/import/neo4j_dump.dump
docker cp diet_app_neo4j:/var/lib/neo4j/import/neo4j_dump.dump ./neo4j_dump.dump
```

### MongoDB

Para MongoDB, você pode usar o comando mongodump:

```bash
docker exec diet_app_mongodb mongodump --username admin --password senha123 --authenticationDatabase admin --db diet_app --out /data/db/mongodb_dump
docker cp diet_app_mongodb:/data/db/mongodb_dump ./mongodb_dump
```

Ou através do script Python:

```bash
# Descomente a linha create_mongodb_dump() no arquivo load_mongodb_data.py
python load_mongodb_data.py
```
