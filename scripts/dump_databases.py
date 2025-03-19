#!/usr/bin/env python
"""
Script para geração automática de dumps do Neo4j e MongoDB.
Este script é uma alternativa à utilização do Makefile para ambientes
onde não é possível executar comandos make.
"""

import subprocess
import os
import datetime
import sys


def print_header(message):
    """Imprime cabeçalho formatado para melhor visualização."""
    print("\n" + "=" * 80)
    print(f"  {message}")
    print("=" * 80 + "\n")


def create_timestamp():
    """Cria um timestamp formatado para nomear os dumps."""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def check_docker_container(container_name):
    """Verifica se o container Docker especificado está em execução."""
    try:
        result = subprocess.run(
            ["docker", "ps", "-q", "-f", f"name={container_name}"],
            capture_output=True,
            text=True,
            check=True,
        )
        return bool(result.stdout.strip())
    except subprocess.SubprocessError:
        return False


def create_directory(directory):
    """Cria um diretório se ele não existir."""
    os.makedirs(directory, exist_ok=True)
    print(f"Diretório '{directory}' disponível.")


def dump_neo4j():
    """Cria um dump do banco Neo4j."""
    print_header("GERANDO DUMP DO NEO4J")

    container_name = "diet_app_neo4j"
    dumps_dir = "./dumps/neo4j"
    timestamp = create_timestamp()
    filename = f"neo4j_dump_{timestamp}.dump"

    if not check_docker_container(container_name):
        print(f"Erro: Container {container_name} não está em execução.")
        return False

    create_directory(dumps_dir)

    try:
        # Criar o dump dentro do container
        print("Executando comando de dump no container Neo4j...")
        dump_cmd = [
            "docker", "exec", container_name,
            "neo4j-admin", "database", "dump", "neo4j",
            "--to-path=/var/lib/neo4j/import"
        ]
        subprocess.run(dump_cmd, check=True)
        # Copiar o dump para o host
        print(f"Copiando dump para {dumps_dir}/{filename}...")
        copy_cmd = [
            "docker", "cp",
            f"{container_name}:/var/lib/neo4j/import/{filename}",
            f"{dumps_dir}/{filename}"
        ]
        subprocess.run(copy_cmd, check=True)

        print(f"Dump do Neo4j criado com sucesso: {dumps_dir}/{filename}")
        return True
    except subprocess.SubprocessError as e:
        print(f"Erro ao criar dump do Neo4j: {e}")
        return False


def dump_mongodb():
    """Cria um dump do banco MongoDB."""
    print_header("GERANDO DUMP DO MONGODB")

    container_name = "diet_app_mongodb"
    dumps_dir = "./dumps/mongodb"
    timestamp = create_timestamp()
    directory = f"mongodb_dump_{timestamp}"

    if not check_docker_container(container_name):
        print(f"Erro: Container {container_name} não está em execução.")
        return False

    create_directory(dumps_dir)

    try:
        # Criar o dump dentro do container
        print("Executando comando de dump no container MongoDB...")
        dump_cmd = [
            "docker", "exec", container_name,
            "mongodump", "--username", "admin", "--password", "senha123",
            "--authenticationDatabase", "admin", "--db", "diet_app",
            f"--out=/data/db/{directory}"
        ]
        subprocess.run(dump_cmd, check=True)

        # Copiar o dump para o host
        print(f"Copiando dump para {dumps_dir}/{directory}...")
        copy_cmd = [
            "docker", "cp",
            f"{container_name}:/data/db/{directory}",
            f"{dumps_dir}/{directory}"
        ]
        subprocess.run(copy_cmd, check=True)

        print(f"Dump do MongoDB criado com sucesso: {dumps_dir}/{directory}")
        return True
    except subprocess.SubprocessError as e:
        print(f"Erro ao criar dump do MongoDB: {e}")
        return False


def main():
    """Função principal que coordena a geração de dumps."""
    print_header("GERADOR DE DUMPS - SISTEMA DE ACOMPANHAMENTO DE DIETAS")

    # Determinar quais bancos incluir no dump
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "neo4j":
            return dump_neo4j()
        elif sys.argv[1].lower() == "mongodb":
            return dump_mongodb()
        else:
            print(f"Erro: Banco '{sys.argv[1]}' não reconhecido.")
            print("Uso: python dump_databases.py [neo4j|mongodb]")
            return False

    # Se nenhum banco for especificado, fazer dump de ambos
    neo4j_success = dump_neo4j()
    mongodb_success = dump_mongodb()

    # Exibir resumo final
    print_header("RESUMO DOS DUMPS")
    print(f"Neo4j: {'SUCESSO' if neo4j_success else 'FALHA'}")
    print(f"MongoDB: {'SUCESSO' if mongodb_success else 'FALHA'}")

    return neo4j_success and mongodb_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)