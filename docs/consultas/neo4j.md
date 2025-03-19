# Consultas Neo4j (Cypher)

Nesta seção, apresentamos as consultas implementadas utilizando a linguagem Cypher para o banco de dados Neo4j. Cada consulta é descrita com seu objetivo, o código Cypher e uma explicação de como a consulta funciona.

## 1. Encontrar todos os pacientes de um nutricionista específico

**Objetivo**: Listar todos os pacientes atendidos por um determinado nutricionista, incluindo o objetivo do paciente.

```cypher
MATCH (n:Nutricionista {nome: "Ana Silva"})-[:ATENDE]->(p:Paciente)
RETURN n.nome AS Nutricionista, p.nome AS Paciente, p.objetivo AS Objetivo
```

**Explicação**: Esta consulta encontra o nutricionista "Ana Silva" e percorre o relacionamento `ATENDE` para encontrar todos os seus pacientes. Para cada paciente, retornamos o nome do nutricionista, o nome do paciente e seu objetivo de tratamento.

**Resultado**: [Veja a imagem do resultado](../resultados/1.png)

## 2. Encontrar todas as refeições de um paciente em um período específico

**Objetivo**: Listar todas as refeições de um paciente em um intervalo de datas específico.

```cypher
MATCH (p:Paciente {nome: "João Pereira"})-[:CONSOME]->(r:Refeicao)
WHERE r.data >= "2023-10-18" AND r.data <= "2023-10-19"
RETURN p.nome AS Paciente, r.tipo AS TipoRefeicao, r.data AS Data,
       r.calorias AS Calorias, r.adesao AS Adesao
ORDER BY r.data, r.hora
```

**Explicação**: Esta consulta localiza o paciente "João Pereira" e todas as refeições que ele consumiu. Filtramos apenas as refeições que ocorreram entre 18/10/2023 e 19/10/2023. Os resultados são ordenados por data e hora.

**Resultado**: [Veja a imagem do resultado](../resultados/2.png)

## 3. Calcular a soma de calorias consumidas por um paciente em um dia

**Objetivo**: Calcular o total de calorias consumidas por um paciente em um dia específico.

```cypher
MATCH (p:Paciente {nome: "João Pereira"})-[:CONSOME]->(r:Refeicao)
WHERE r.data = "2023-10-18"
RETURN p.nome AS Paciente, r.data AS Data, SUM(r.calorias) AS TotalCalorias
```

**Explicação**: Esta consulta encontra todas as refeições consumidas pelo paciente "João Pereira" na data 18/10/2023 e soma o valor de calorias para calcular o total consumido nesse dia.

**Resultado**: [Veja a imagem do resultado](../resultados/3.png)

## 4. Encontrar receitas adequadas para pacientes com restrições alimentares

**Objetivo**: Identificar receitas recomendadas em planos alimentares para pacientes com restrições específicas.

```cypher
MATCH (p:Paciente)-[:SEGUE]->(pa:PlanoAlimentar)-[:RECOMENDA]->(r:Receita)
WHERE "Glúten" IN p.restricoes
RETURN p.nome AS Paciente, r.nome AS ReceitaAdequada, r.calorias AS Calorias
```

**Explicação**: Esta consulta encontra todos os pacientes que têm "Glúten" como uma de suas restrições alimentares, depois localiza os planos alimentares que eles seguem e, finalmente, identifica as receitas recomendadas nesses planos.

**Resultado**: [Veja a imagem do resultado](../resultados/4.png)

## 5. Identificar pacientes com baixa adesão ao plano alimentar

**Objetivo**: Encontrar pacientes que têm baixa adesão (menos de 80%) ao plano alimentar, com base nos registros de refeições.

```cypher
MATCH (p:Paciente)-[:CONSOME]->(r:Refeicao)
WITH p, COUNT(r) AS totalRefeicoes,
     SUM(CASE WHEN r.adesao = "Completa" THEN 1 ELSE 0 END) AS refeicoesCompletas
WHERE (refeicoesCompletas * 1.0 / totalRefeicoes) < 0.8
RETURN p.nome AS Paciente, totalRefeicoes, refeicoesCompletas,
       (refeicoesCompletas * 1.0 / totalRefeicoes) AS TaxaAdesao
ORDER BY TaxaAdesao
```

**Explicação**: Esta consulta conta o número total de refeições para cada paciente e quantas dessas refeições foram marcadas como "Completa". Depois, calcula a taxa de adesão (refeições completas dividido pelo total de refeições) e filtra apenas os pacientes com taxa menor que 0,8 (80%).

**Resultado**: [Veja a imagem do resultado](../resultados/5.png)

## 6. Rastrear o progresso de um paciente analisando medidas corporais

**Objetivo**: Analisar a evolução das medidas corporais de um paciente ao longo do tempo.

```cypher
MATCH (p:Paciente {nome: "João Pereira"})-[:POSSUI]->(m:MedidaCorporal)
RETURN p.nome AS Paciente, m.data AS Data, m.peso AS Peso, m.imc AS IMC,
       m.gordura_corporal AS GorduraCorporal, m.cintura AS Cintura
ORDER BY m.data
```

**Explicação**: Esta consulta recupera todas as medidas corporais registradas para o paciente "João Pereira" e as ordena por data, permitindo visualizar seu progresso ao longo do tempo.

**Resultado**: [Veja a imagem do resultado](../resultados/6.png)

## 7. Encontrar os alimentos mais recomendados nos planos alimentares

**Objetivo**: Identificar quais alimentos são mais frequentemente recomendados nos planos alimentares, agrupados por grupo alimentar.

```cypher
MATCH (pa:PlanoAlimentar)-[:INCLUI]->(a:Alimento)
RETURN a.nome AS Alimento, a.grupo AS Grupo, COUNT(pa) AS NumeroDeRecomendacoes
ORDER BY NumeroDeRecomendacoes DESC
```

**Explicação**: Esta consulta conta quantas vezes cada alimento aparece como recomendado em planos alimentares. Os resultados são agrupados por alimento e ordenados pelo número de recomendações em ordem decrescente.

**Resultado**: [Veja a imagem do resultado](../resultados/7.png)

## 8. Analisar a comunicação entre nutricionistas e pacientes

**Objetivo**: Visualizar todas as mensagens trocadas entre nutricionistas e pacientes, ordenadas cronologicamente.

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

**Explicação**: Esta consulta recupera todas as mensagens onde o remetente ou o destinatário é um nutricionista. Utiliza expressões CASE para formatar adequadamente os nomes dos remetentes e destinatários, independentemente se são nutricionistas ou pacientes.

**Resultado**: [Veja a imagem do resultado](../resultados/8.png)

## 9. Encontrar receitas que contêm determinado alimento

**Objetivo**: Listar todas as receitas que contêm um alimento específico.

```cypher
MATCH (r:Receita)-[:CONTEM]->(a:Alimento {nome: "Brócolis"})
RETURN r.nome AS Receita, r.calorias AS Calorias, r.dificuldade AS Dificuldade,
       r.tempo_preparo AS TempoPreparo
```

**Explicação**: Esta consulta busca todas as receitas que contêm "Brócolis" como um de seus ingredientes, exibindo detalhes como calorias, nível de dificuldade e tempo de preparo.

**Resultado**: [Veja a imagem do resultado](../resultados/9.png)

## 10. Visualizar próximas consultas agendadas

**Objetivo**: Listar todas as consultas futuras agendadas entre pacientes e nutricionistas.

```cypher
MATCH (p:Paciente)-[:AGENDA]->(c:Consulta {status: "Agendada"})-[:COM]->(n:Nutricionista)
RETURN p.nome AS Paciente, n.nome AS Nutricionista, c.data AS Data, c.hora AS Hora
ORDER BY c.data, c.hora
```

**Explicação**: Esta consulta encontra todas as consultas com status "Agendada", mostrando o paciente, o nutricionista, a data e a hora da consulta. Os resultados são ordenados cronologicamente.

**Resultado**: [Veja a imagem do resultado](../resultados/10.png)