# GitHub Workflow para o Sistema de Acompanhamento de Dietas

Este documento descreve o fluxo de trabalho de CI/CD implementado para o projeto de Sistema de Acompanhamento de Dietas usando Neo4j e MongoDB.

## Visão Geral do Workflow

O fluxo de trabalho automatizado foi configurado para:

1. **Corrigir automaticamente** problemas de formatação de código
2. **Verificar** a qualidade do código
3. **Testar** a integração com os bancos de dados
4. **Construir** imagens Docker
5. **Gerar** documentação

## Jobs Principais

### 1. Auto-formatação de Código

Este job executa automaticamente ferramentas para corrigir problemas comuns de estilo e formatação:

- **isort**: Ordena as importações de acordo com o estilo do Black
- **black**: Formata o código Python segundo padrões PEP
- **flake8-fixme**: Corrige problemas comuns detectados pelo flake8

Se alguma alteração for feita, o workflow faz commit e push automaticamente, o que evita ciclos de feedback desnecessários entre o CI/CD e os desenvolvedores.

### 2. Verificação de Qualidade de Código

Verifica se o código está de acordo com as melhores práticas usando:

- **flake8**: Detecta problemas de estilo e possíveis bugs
- **isort**: Verifica se as importações estão organizadas corretamente
- **black**: Confirma se o código está formatado segundo o padrão
- **mypy**: Realiza verificação de tipos estática

### 3. Testes de Integração

Testa a interação com os bancos de dados:

- Inicia containers Docker para Neo4j e MongoDB
- Verifica conectividade e funcionalidades básicas
- Testa carregamento e consulta de dados
- Executa testes unitários com pytest

### 4. Construção de Imagens Docker

Para produção:

- Cria uma imagem Docker com todos os scripts e dependências
- Publica a imagem no GitHub Container Registry
- Aplica tags apropriadas para versionamento

### 5. Geração de Documentação

Automatiza a criação de documentação:

- Gera documentação API com pdoc3
- Cria um site de documentação com MkDocs e Material theme
- Publica automaticamente no GitHub Pages

## Configuração Local

Para usar o mesmo conjunto de ferramentas de qualidade de código localmente:

1. Instale o pre-commit:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. Isso executará as mesmas verificações e correções automáticas cada vez que você fizer um commit.

## Triggers do Workflow

O workflow é acionado quando:

- Um push é feito para as branches `main`, `master` ou `development`
- Uma pull request é aberta ou atualizada target as branches `main` ou `master`
- Manualmente através da interface do GitHub ("workflow_dispatch")

## Configuração de Permissões

O workflow precisa das seguintes permissões:

- `contents: write` - Para fazer commit de correções automáticas
- `pull-requests: write` - Para atualizar pull requests
- `packages: write` - Para publicar imagens Docker (implícito no GitHub Actions)
- `pages: write` - Para publicar documentação no GitHub Pages (configurado na action peaceiris/actions-gh-pages)

## Arquivos de Configuração Adicionais

- **setup.cfg**: Configurações para flake8, isort e mypy
- **.pre-commit-config.yaml**: Configuração para verificações pré-commit locais
- **Dockerfile**: Definição da imagem Docker para o aplicativo
- **test_database_setup.py**: Testes para verificar a configuração e dados dos bancos

## Benefícios

- **Produtividade aumentada**: Correção automática de problemas comuns
- **Qualidade consistente**: Manutenção de padrões em todo o projeto
- **Integração contínua**: Detecção precoce de problemas
- **Entrega contínua**: Geração de artefatos prontos para implantação
- **Documentação atualizada**: Documentação sempre sincronizada com o código
