### 5. Crie um Arquivo para Documentar Dumps

# Dumps do Banco

O sistema oferece funcionalidades para criar dumps (backups) dos bancos de dados Neo4j e MongoDB.

## Usando o Makefile

A maneira mais simples é usar os comandos disponíveis no Makefile:

```bash
# Gerar dumps de ambos os bancos
make dump

# Gerar apenas dump do Neo4j
make dump-neo4j

# Gerar apenas dump do MongoDB
make dump-mongodb
```