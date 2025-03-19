---
layout: page
title: Consultas MongoDB
---

# Consultas MongoDB

Nesta seção, apresentamos as consultas implementadas no MongoDB. Cada consulta é descrita com seu objetivo, o código em JavaScript e uma explicação de como a consulta funciona.

## 1. Encontrar todos os pacientes de um nutricionista específico

**Objetivo**: Listar todos os pacientes atendidos por um determinado nutricionista.

```javascript
db.patients.find(
    {nutricionista_id: 1},
    {nome: 1, idade: 1, objetivo: 1, _id: 0}
)
```

**Explicação**: Esta consulta busca todos os documentos na coleção `patients` onde o campo `nutricionista_id` é igual a 1. O segundo parâmetro especifica os campos a serem retornados (`nome`, `idade`, e `objetivo`), excluindo o `_id`.

**Resultado**: [Veja a imagem do resultado](../resultados/mongo_consulta_1.png)

## 2. Buscar todas as refeições de um paciente em um período específico

**Objetivo**: Listar todas as refeições de um paciente em um intervalo de datas específico.

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

**Explicação**: Esta consulta busca documentos na coleção `meals` onde o `paciente_id` é 1 e a data está entre 18/10/2023 e 19/10/2023. Retorna os campos especificados e ordena os resultados por data e hora.

**Resultado**: [Veja a imagem do resultado](../resultados/mongo_consulta_2.png)

## 3. Calcular total de calorias consumidas por dia

**Objetivo**: Calcular o total de calorias consumidas por um paciente, agrupadas por dia.

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

**Explicação**: Esta consulta usa o framework de agregação do MongoDB para:
1. Filtrar refeições do paciente com ID 1
2. Agrupar os resultados por data (convertida para formato YYYY-MM-DD)
3. Calcular a soma das calorias para cada dia
4. Ordenar os resultados por data

**Resultado**: [Veja a imagem do resultado](../resultados/mongo_consulta_3.png)

## 4. Encontrar receitas adequadas para pacientes com restrições

**Objetivo**: Identificar receitas recomendadas em planos alimentares para pacientes com restrições específicas.

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

**Explicação**: Esta consulta complexa usa o framework de agregação para:
1. Encontrar pacientes com restrição de "Glúten"
2. Juntar os dados com a coleção `dietPlans` para encontrar os planos alimentares desses pacientes
3. Desempacotar o array de planos
4. Juntar com a coleção `recipes` para encontrar as receitas recomendadas
5. Desempacotar o array de receitas
6. Projetar apenas os campos desejados

**Resultado**: [Veja a imagem do resultado](../resultados/mongo_consulta_4.png)

## 5. Identificar pacientes com baixa adesão ao plano alimentar

**Objetivo**: Encontrar pacientes que têm baixa adesão (menos de 80%) ao plano alimentar.

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

**Explicação**: Esta consulta:
1. Agrupa as refeições por paciente, contando o total de refeições e quantas foram completas
2. Calcula a taxa de adesão (refeições completas / total de refeições)
3. Filtra apenas os pacientes com taxa de adesão abaixo de 0,8 (80%)
4. Busca os dados do paciente na coleção `patients`
5. Projeta os campos desejados e ordena por taxa de adesão

**Resultado**: [Veja a imagem do resultado](../resultados/mongo_consulta_5.png)

## 6. Rastrear progresso corporal de um paciente

**Objetivo**: Analisar a evolução das medidas corporais de um paciente ao longo do tempo.

```javascript
db.measurements.find(
    {paciente_id: 1},
    {data: 1, peso: 1, imc: 1, gordura_corporal: 1, "medidas.cintura": 1, _id: 0}
).sort({data: 1})
```

**Explicação**: Esta consulta recupera todas as medidas corporais do paciente com ID 1, incluindo a medida de cintura que está aninhada no objeto `medidas`. Os resultados são ordenados por data.

**Resultado**: [Veja a imagem do resultado](../resultados/mongo_consulta_6.png)

## 7. Encontrar alimentos mais recomendados nos planos alimentares

**Objetivo**: Identificar quais alimentos são mais frequentemente recomendados nos planos alimentares.

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

**Explicação**: Esta consulta:
1. Desempacota o array `alimentos_recomendados` de cada plano alimentar
2. Agrupa por ID de alimento e conta quantas vezes cada alimento aparece
3. Busca os detalhes de cada alimento na coleção `foods`
4. Projeta os campos desejados e ordena por número de recomendações em ordem decrescente

**Resultado**: [Veja a imagem do resultado](../resultados/mongo_consulta_7.png)

## 8. Analisar comunicação entre nutricionistas e pacientes

**Objetivo**: Visualizar todas as mensagens trocadas entre nutricionistas e pacientes.

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

**Explicação**: Esta consulta complexa:
1. Junta dados com as coleções `nutritionists` e `patients` para encontrar os nomes dos remetentes e destinatários
2. Usa condições para determinar se o remetente/destinatário é um nutricionista ou paciente
3. Projeta os campos desejados e ordena cronologicamente

**Resultado**: [Veja a imagem do resultado](../resultados/mongo_consulta_8.png)

## 9. Encontrar receitas que contêm determinado ingrediente

**Objetivo**: Listar todas as receitas que contêm um alimento específico.

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

**Explicação**: Esta consulta:
1. Filtra receitas que têm um ingrediente com `food_id` igual a 4
2. Busca os detalhes dos alimentos na coleção `foods`
3. Filtra novamente para garantir que o alimento seja "Brócolis"
4. Projeta os campos desejados

**Resultado**: [Veja a imagem do resultado](../resultados/mongo_consulta_9.png)

## 10. Visualizar próximas consultas agendadas

**Objetivo**: Listar todas as consultas futuras agendadas entre pacientes e nutricionistas.

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

**Explicação**: Esta consulta:
1. Filtra consultas com status "Agendada"
2. Busca os dados do paciente e do nutricionista em suas respectivas coleções
3. Desempacota os arrays resultantes
4. Projeta os campos desejados e ordena cronologicamente

**Resultado**: [Veja a imagem do resultado](../resultados/mongo_consulta_10.png)