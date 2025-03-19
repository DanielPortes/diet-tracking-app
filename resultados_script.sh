mkdir -p resultados/neo4j
mkdir -p resultados/mongodb
touch resultados/neo4j/.gitkeep
touch resultados/mongodb/.gitkeep

# Atualizar .gitignore para não ignorar a pasta resultados
echo -e "\n# Manter a pasta resultados, mas ignorar os arquivos PNG (eles serão adicionados manualmente)\nresultados/**/*.png" >> .gitignore

# Criar arquivo README na pasta resultados
cat > resultados/README.md << 'EOF'
# Resultados das Consultas

Esta pasta contém os screenshots dos resultados das consultas executadas em cada banco de dados.

## Estrutura

- `neo4j/` - Screenshots dos resultados das consultas Neo4j (Cypher)
  - `neo4j_consulta_1.png` - Resultado da consulta "Encontrar todos os pacientes de um nutricionista específico"
  - `neo4j_consulta_2.png` - Resultado da consulta "Encontrar todas as refeições de um paciente em um período específico"
  - etc.

- `mongodb/` - Screenshots dos resultados das consultas MongoDB
  - `mongo_consulta_1.png` - Resultado da consulta "Encontrar todos os pacientes de um nutricionista específico"
  - `mongo_consulta_2.png` - Resultado da consulta "Buscar todas as refeições de um paciente em um período específico"
  - etc.

## Como Adicionar Resultados

1. Execute a consulta no respectivo banco de dados
2. Capture a tela com o resultado
3. Salve a imagem com o nome apropriado na pasta correspondente
4. Adicione a imagem ao controle de versão: `git add resultados/<banco>/<nome_do_arquivo>.png`

**Observação**: Os arquivos PNG estão ignorados no .gitignore por padrão. É necessário forçar a adição (usando `git add -f` ou removendo a entrada do .gitignore) para incluí-los no repositório.
EOF

# Criar arquivos de placeholder para cada resultado esperado
for i in $(seq 1 10); do
  echo "Placeholder para o resultado da consulta $i - Neo4j" > resultados/neo4j/placeholder_$i.txt
  echo "Placeholder para o resultado da consulta $i - MongoDB" > resultados/mongodb/placeholder_$i.txt
done