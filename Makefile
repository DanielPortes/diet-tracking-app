# Makefile para o Sistema de Acompanhamento de Dietas

# Variáveis
DOCKER_COMPOSE = docker-compose
NEO4J_CONTAINER = diet_app_neo4j
MONGODB_CONTAINER = diet_app_mongodb
TIMESTAMP = $(shell date +%Y%m%d_%H%M%S)
DUMPS_DIR = ./dumps

# Diretórios
DUMPS_NEO4J_DIR = $(DUMPS_DIR)/neo4j
DUMPS_MONGODB_DIR = $(DUMPS_DIR)/mongodb

# Comandos principais
.PHONY: setup start stop restart dump dump-neo4j dump-mongodb build-docs clean

# Configuração inicial: cria diretórios e inicia os serviços
setup:
	@echo "🔧 Configurando ambiente..."
	@mkdir -p $(DUMPS_NEO4J_DIR) $(DUMPS_MONGODB_DIR)
	@echo "📂 Diretórios de dumps criados."
	@echo "🐳 Iniciando containers Docker..."
	@$(DOCKER_COMPOSE) up -d
	@echo "⏳ Aguardando inicialização dos serviços... (30s)"
	@sleep 15
	@echo "✅ Ambiente configurado com sucesso!"

# Inicia os serviços
start:
	@echo "🚀 Iniciando containers Docker..."
	@$(DOCKER_COMPOSE) up -d
	@echo "⏳ Aguardando inicialização dos serviços... (30s)"
	@sleep 15
	@echo "✅ Serviços iniciados com sucesso!"

# Para os serviços
stop:
	@echo "🛑 Parando containers Docker..."
	@$(DOCKER_COMPOSE) down
	@echo "✅ Serviços parados com sucesso!"

# Reinicia os serviços
restart: stop start

# Carrega os dados nos bancos
load:
	@echo "📝 Carregando dados nos bancos..."
	@python load_all_databases.py
	@echo "✅ Dados carregados com sucesso!"

# Gera dump de ambos os bancos
dump: dump-neo4j dump-mongodb

# Gera dump do Neo4j
dump-neo4j:
	@echo "🗄️ Gerando dump do Neo4j..."
	@mkdir -p $(DUMPS_NEO4J_DIR)
	@echo "📋 Criando backup dos dados Neo4j para $(DUMPS_NEO4J_DIR)/neo4j_dump_$(TIMESTAMP).tar"
	@docker exec $(NEO4J_CONTAINER) tar -cf /tmp/neo4j_dump.tar -C /data/databases .
	@docker cp $(NEO4J_CONTAINER):/tmp/neo4j_dump.tar $(DUMPS_NEO4J_DIR)/neo4j_dump_$(TIMESTAMP).tar
	@echo "✅ Backup dos dados Neo4j criado com sucesso em: $(DUMPS_NEO4J_DIR)/neo4j_dump_$(TIMESTAMP).tar"


# Gera dump do MongoDB
dump-mongodb:
	@echo "🗄️ Gerando dump do MongoDB..."
	@mkdir -p $(DUMPS_MONGODB_DIR)
	@docker exec $(MONGODB_CONTAINER) mongodump --username admin --password senha123 --authenticationDatabase admin --db diet_app --out /data/db/mongodb_dump_$(TIMESTAMP)
	@docker cp $(MONGODB_CONTAINER):/data/db/mongodb_dump_$(TIMESTAMP) $(DUMPS_MONGODB_DIR)/
	@echo "✅ Dump do MongoDB criado com sucesso: $(DUMPS_MONGODB_DIR)/mongodb_dump_$(TIMESTAMP)"

# Constrói documentação local (para testar antes de publicar)
build-docs:
	@echo "📚 Gerando documentação local..."
	@cd docs && jekyll build
	@echo "✅ Documentação gerada em docs/_site"

# Limpa diretórios de build e logs
clean:
	@echo "🧹 Limpando diretórios temporários..."
	@rm -rf *.log
	@echo "✅ Limpeza concluída!"

# Ajuda
help:
	@echo "🔍 Comandos disponíveis:"
	@echo "  make setup       - Cria diretórios e inicia os serviços"
	@echo "  make start       - Inicia os containers Docker"
	@echo "  make stop        - Para os containers Docker"
	@echo "  make restart     - Reinicia os containers Docker"
	@echo "  make load        - Carrega os dados nos bancos"
	@echo "  make dump        - Gera dumps de ambos os bancos"
	@echo "  make dump-neo4j  - Gera dump apenas do Neo4j"
	@echo "  make dump-mongodb- Gera dump apenas do MongoDB"
	@echo "  make build-docs  - Constrói documentação local"
	@echo "  make clean       - Limpa diretórios temporários"
	@echo "  make help        - Exibe esta ajuda"