import os
import subprocess
import time
import sys


def print_header(message):
    """Imprime cabeçalho formatado para melhor visualização"""
    print("\n" + "=" * 80)
    print(f"  {message}")
    print("=" * 80 + "\n")


def check_docker_running():
    """Verifica se o Docker está em execução"""
    try:
        subprocess.run(["docker", "info"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL,
                       check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def check_docker_compose_exists():
    """Verifica se o Docker Compose está instalado"""
    try:
        subprocess.run(["docker-compose", "--version"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL,
                       check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def start_docker_services():
    """Inicia serviços Docker usando docker-compose"""
    print_header("Iniciando serviços Docker (Neo4j e MongoDB)")

    try:
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        print("Serviços iniciados com sucesso!")

        # Dá um tempo para os serviços inicializarem completamente
        print("Aguardando inicialização completa dos serviços... (30 segundos)")
        time.sleep(30)  # Aguarda 30 segundos para inicialização
        return True
    except subprocess.SubprocessError as e:
        print(f"Erro ao iniciar serviços Docker: {e}")
        return False


def load_neo4j_data():
    """Carrega dados no Neo4j usando o script Python"""
    print_header("Carregando dados no Neo4j")

    try:
        # Executa o script para carregar dados no Neo4j
        result = subprocess.run([sys.executable, "load_data.py"], check=True)
        print("Dados carregados no Neo4j com sucesso!")
        return True
    except subprocess.SubprocessError as e:
        print(f"Erro ao carregar dados no Neo4j: {e}")
        return False


def load_mongodb_data():
    """Carrega dados no MongoDB usando o script Python"""
    print_header("Carregando dados no MongoDB")

    try:
        # Executa o script para carregar dados no MongoDB
        result = subprocess.run([sys.executable, "load_mongodb_data.py"], check=True)
        print("Dados carregados no MongoDB com sucesso!")
        return True
    except subprocess.SubprocessError as e:
        print(f"Erro ao carregar dados no MongoDB: {e}")
        return False


def main():
    """Função principal que coordena o carregamento de dados"""
    print_header("SISTEMA DE ACOMPANHAMENTO DE DIETAS - CONFIGURAÇÃO DE BANCOS")

    # Verificar se o Docker está em execução
    if not check_docker_running():
        print("ERRO: Docker não está em execução. Inicie o Docker e tente novamente.")
        return False

    # Verificar se o Docker Compose está instalado
    if not check_docker_compose_exists():
        print("ERRO: Docker Compose não está instalado. Instale-o e tente novamente.")
        return False

    # Iniciar serviços Docker
    if not start_docker_services():
        return False

    # Carregar dados no Neo4j
    neo4j_success = load_neo4j_data()

    # Carregar dados no MongoDB
    mongodb_success = load_mongodb_data()

    # Exibir resumo final
    print_header("RESUMO DA CONFIGURAÇÃO")
    print(f"Neo4j: {'SUCESSO' if neo4j_success else 'FALHA'}")
    print(f"MongoDB: {'SUCESSO' if mongodb_success else 'FALHA'}")

    if neo4j_success and mongodb_success:
        print("\nTodos os bancos de dados foram configurados com sucesso!")
        print("\nAcesse:")
        print("- Neo4j Browser: http://localhost:7474 (usuário: neo4j, senha: senha123)")
        print("- MongoDB Express: http://localhost:8081 (usuário: admin, senha: senha123)")
        return True
    else:
        print("\nHouve problemas na configuração de um ou mais bancos de dados.")
        print("Verifique as mensagens de erro acima e tente novamente.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)