import os
import time

from dotenv import load_dotenv
from neo4j import GraphDatabase

# Carregar variáveis de ambiente (opcional)
load_dotenv()

# Configurações de conexão
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "senha123")
MAX_CONNECTION_RETRY = 10
RETRY_INTERVAL = 5  # segundos


def wait_for_neo4j():
    """Espera até que o Neo4j esteja pronto para aceitar conexões"""
    driver = None
    for i in range(MAX_CONNECTION_RETRY):
        try:
            driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            # Verificar se a conexão está funcionando
            with driver.session() as session:
                result = session.run("RETURN 1 AS num")
                record = result.single()
                if record and record["num"] == 1:
                    print("Conexão com Neo4j estabelecida com sucesso!")
                    driver.close()
                    return True
        except Exception as e:
            print(f"Tentativa {i + 1}/{MAX_CONNECTION_RETRY}: Neo4j ainda não está pronto: {str(e)}")
            if driver:
                driver.close()
            time.sleep(RETRY_INTERVAL)

    print("Não foi possível conectar ao Neo4j após várias tentativas.")
    return False


def load_nutritionists(tx):
    query = """
    // Criar Nutricionistas
    CREATE (n1:Nutricionista {id: 1, nome: "Ana Silva", especialidade: "Nutrição Esportiva", 
            experiencia: 8, email: "ana@nutri.com", telefone: "21-99999-1111"})
    CREATE (n2:Nutricionista {id: 2, nome: "Carlos Mendes", especialidade: "Nutrição Clínica", 
            experiencia: 5, email: "carlos@nutri.com", telefone: "21-99999-2222"})
    CREATE (n3:Nutricionista {id: 3, nome: "Mariana Costa", especialidade: "Nutrição Funcional", 
            experiencia: 12, email: "mariana@nutri.com", telefone: "21-99999-3333"})
    """
    tx.run(query)
    print("Nutricionistas criados com sucesso!")


def load_patients(tx):
    query = """
    // Criar Pacientes
    CREATE (p1:Paciente {id: 1, nome: "João Pereira", idade: 35, genero: "M", altura: 178, 
            peso_inicial: 92, email: "joao@email.com", telefone: "21-88888-1111", 
            restricoes: ["Glúten"], alergias: ["Amendoim"], 
            objetivo: "Emagrecimento"})
    CREATE (p2:Paciente {id: 2, nome: "Maria Santos", idade: 42, genero: "F", altura: 165, 
            peso_inicial: 78, email: "maria@email.com", telefone: "21-88888-2222", 
            restricoes: ["Lactose"], alergias: [], 
            objetivo: "Controle de colesterol"})
    CREATE (p3:Paciente {id: 3, nome: "Pedro Alves", idade: 28, genero: "M", altura: 182, 
            peso_inicial: 75, email: "pedro@email.com", telefone: "21-88888-3333", 
            restricoes: [], alergias: [], 
            objetivo: "Ganho de massa muscular"})
    CREATE (p4:Paciente {id: 4, nome: "Lúcia Ferreira", idade: 55, genero: "F", altura: 160, 
            peso_inicial: 85, email: "lucia@email.com", telefone: "21-88888-4444", 
            restricoes: ["Sódio"], alergias: ["Frutos do mar"], 
            objetivo: "Controle de diabetes"})
    CREATE (p5:Paciente {id: 5, nome: "Ricardo Gomes", idade: 30, genero: "M", altura: 175, 
            peso_inicial: 88, email: "ricardo@email.com", telefone: "21-88888-5555", 
            restricoes: [], alergias: ["Nozes"], 
            objetivo: "Emagrecimento"})
    """
    tx.run(query)
    print("Pacientes criados com sucesso!")


def load_foods(tx):
    query = """
    // Criar Alimentos
    CREATE (a1:Alimento {id: 1, nome: "Maçã", porcao: "1 unidade (150g)", calorias: 95, 
            proteinas: 0.5, carboidratos: 25, gorduras: 0.3, fibras: 4.4, grupo: "Frutas"})
    CREATE (a2:Alimento {id: 2, nome: "Peito de Frango", porcao: "100g", calorias: 165, 
            proteinas: 31, carboidratos: 0, gorduras: 3.6, fibras: 0, grupo: "Carnes"})
    CREATE (a3:Alimento {id: 3, nome: "Arroz Integral", porcao: "100g cozido", calorias: 112, 
            proteinas: 2.6, carboidratos: 23.5, gorduras: 0.9, fibras: 1.8, grupo: "Cereais"})
    CREATE (a4:Alimento {id: 4, nome: "Brócolis", porcao: "100g", calorias: 34, 
            proteinas: 2.8, carboidratos: 6.6, gorduras: 0.4, fibras: 2.6, grupo: "Vegetais"})
    CREATE (a5:Alimento {id: 5, nome: "Salmão", porcao: "100g", calorias: 206, 
            proteinas: 22, carboidratos: 0, gorduras: 13, fibras: 0, grupo: "Peixes"})
    CREATE (a6:Alimento {id: 6, nome: "Lentilha", porcao: "100g cozida", calorias: 116, 
            proteinas: 9, carboidratos: 20, gorduras: 0.4, fibras: 7.9, grupo: "Leguminosas"})
    CREATE (a7:Alimento {id: 7, nome: "Iogurte Natural", porcao: "100g", calorias: 59, 
            proteinas: 3.5, carboidratos: 4.7, gorduras: 3.3, fibras: 0, grupo: "Laticínios"})
    CREATE (a8:Alimento {id: 8, nome: "Aveia", porcao: "30g", calorias: 117, 
            proteinas: 4, carboidratos: 21, gorduras: 2, fibras: 3, grupo: "Cereais"})
    CREATE (a9:Alimento {id: 9, nome: "Azeite", porcao: "1 colher (10ml)", calorias: 90, 
            proteinas: 0, carboidratos: 0, gorduras: 10, fibras: 0, grupo: "Óleos"})
    CREATE (a10:Alimento {id: 10, nome: "Banana", porcao: "1 unidade (120g)", calorias: 105, 
            proteinas: 1.3, carboidratos: 27, gorduras: 0.4, fibras: 3.1, grupo: "Frutas"})
    """
    tx.run(query)
    print("Alimentos criados com sucesso!")


def load_recipes(tx):
    query = """
    // Criar Receitas
    CREATE (r1:Receita {id: 1, nome: "Salada de Frango com Abacate", 
            instrucoes: "Corte o peito de frango em cubos e grelhe. Misture com abacate, tomate e folhas verdes. Tempere com azeite, limão e sal.", 
            tempo_preparo: 20, dificuldade: "Fácil", calorias: 320})
    CREATE (r2:Receita {id: 2, nome: "Bowl de Açaí com Frutas", 
            instrucoes: "Misture açaí congelado batido com banana. Adicione granola, frutas frescas e mel.", 
            tempo_preparo: 10, dificuldade: "Fácil", calorias: 450})
    CREATE (r3:Receita {id: 3, nome: "Salmão Grelhado com Legumes", 
            instrucoes: "Grelhe o filé de salmão. Refogue brócolis, cenoura e abobrinha. Sirva com arroz integral.", 
            tempo_preparo: 30, dificuldade: "Médio", calorias: 480})
    CREATE (r4:Receita {id: 4, nome: "Smoothie Proteico", 
            instrucoes: "Bata no liquidificador iogurte, banana, aveia, pasta de amendoim e mel.", 
            tempo_preparo: 5, dificuldade: "Fácil", calorias: 350})
    CREATE (r5:Receita {id: 5, nome: "Omelete de Legumes", 
            instrucoes: "Bata 2 ovos, adicione espinafre, tomate e queijo. Cozinhe em frigideira antiaderente.", 
            tempo_preparo: 15, dificuldade: "Fácil", calorias: 280})
    """
    tx.run(query)
    print("Receitas criadas com sucesso!")


def load_diet_plans(tx):
    query = """
    // Criar Planos Alimentares
    CREATE (pa1:PlanoAlimentar {id: 1, nome: "Emagrecimento Saudável", 
            descricao: "Plano focado em déficit calórico moderado com alimentos nutritivos", 
            objetivo: "Perda de peso", duracao: 90, calorias_diarias: 1800, 
            proteinas: "30%", carboidratos: "40%", gorduras: "30%"})
    CREATE (pa2:PlanoAlimentar {id: 2, nome: "Ganho de Massa", 
            descricao: "Plano focado em superávit calórico com alta proteína", 
            objetivo: "Hipertrofia", duracao: 120, calorias_diarias: 2800, 
            proteinas: "35%", carboidratos: "45%", gorduras: "20%"})
    CREATE (pa3:PlanoAlimentar {id: 3, nome: "Controle Glicêmico", 
            descricao: "Plano para controle de diabetes com baixo índice glicêmico", 
            objetivo: "Controle de glicemia", duracao: 180, calorias_diarias: 1600, 
            proteinas: "25%", carboidratos: "35%", gorduras: "40%"})
    CREATE (pa4:PlanoAlimentar {id: 4, nome: "Controle de Colesterol", 
            descricao: "Plano para redução de colesterol LDL e aumento de HDL", 
            objetivo: "Saúde cardiovascular", duracao: 90, calorias_diarias: 2000, 
            proteinas: "25%", carboidratos: "50%", gorduras: "25%"})
    CREATE (pa5:PlanoAlimentar {id: 5, nome: "Dieta Anti-inflamatória", 
            descricao: "Plano rico em antioxidantes e ômega-3", 
            objetivo: "Redução de inflamação", duracao: 60, calorias_diarias: 2200, 
            proteinas: "20%", carboidratos: "55%", gorduras: "25%"})
    """
    tx.run(query)
    print("Planos alimentares criados com sucesso!")


def load_meals(tx):
    query = """
    // Criar Refeições
    CREATE (ref1:Refeicao {id: 1, tipo: "Café da manhã", data: "2023-10-18", 
            hora: "08:00", calorias: 320, adesao: "Completa", registro_foto: true})
    CREATE (ref2:Refeicao {id: 2, tipo: "Almoço", data: "2023-10-18", 
            hora: "12:30", calorias: 580, adesao: "Parcial", registro_foto: true})
    CREATE (ref3:Refeicao {id: 3, tipo: "Lanche", data: "2023-10-18", 
            hora: "16:00", calorias: 180, adesao: "Completa", registro_foto: false})
    CREATE (ref4:Refeicao {id: 4, tipo: "Jantar", data: "2023-10-18", 
            hora: "20:00", calorias: 450, adesao: "Completa", registro_foto: true})
    CREATE (ref5:Refeicao {id: 5, tipo: "Café da manhã", data: "2023-10-19", 
            hora: "07:45", calorias: 340, adesao: "Completa", registro_foto: true})
    CREATE (ref6:Refeicao {id: 6, tipo: "Almoço", data: "2023-10-19", 
            hora: "13:00", calorias: 620, adesao: "Completa", registro_foto: true})
    CREATE (ref7:Refeicao {id: 7, tipo: "Lanche", data: "2023-10-19", 
            hora: "15:30", calorias: 200, adesao: "Parcial", registro_foto: false})
    CREATE (ref8:Refeicao {id: 8, tipo: "Jantar", data: "2023-10-19", 
            hora: "19:30", calorias: 380, adesao: "Não realizada", registro_foto: false})
    """
    tx.run(query)
    print("Refeições criadas com sucesso!")


def load_measurements(tx):
    query = """
    // Criar Medidas Corporais
    CREATE (m1:MedidaCorporal {id: 1, data: "2023-09-15", peso: 92, imc: 29.1, 
            gordura_corporal: 28, cintura: 102, quadril: 106, pressao: "130/85"})
    CREATE (m2:MedidaCorporal {id: 2, data: "2023-10-01", peso: 89.5, imc: 28.2, 
            gordura_corporal: 26.8, cintura: 99, quadril: 105, pressao: "128/83"})
    CREATE (m3:MedidaCorporal {id: 3, data: "2023-10-15", peso: 87.8, imc: 27.7, 
            gordura_corporal: 25.5, cintura: 97, quadril: 104, pressao: "125/82"})
    CREATE (m4:MedidaCorporal {id: 4, data: "2023-09-10", peso: 78, imc: 28.7, 
            gordura_corporal: 32, cintura: 91, quadril: 110, pressao: "135/88"})
    CREATE (m5:MedidaCorporal {id: 5, data: "2023-09-25", peso: 77.2, imc: 28.4, 
            gordura_corporal: 31.5, cintura: 90, quadril: 109, pressao: "132/86"})
    CREATE (m6:MedidaCorporal {id: 6, data: "2023-10-10", peso: 76.5, imc: 28.1, 
            gordura_corporal: 30.8, cintura: 88, quadril: 108, pressao: "130/85"})
    """
    tx.run(query)
    print("Medidas corporais criadas com sucesso!")


def load_messages(tx):
    query = """
    // Criar Mensagens
    CREATE (msg1:Mensagem {id: 1, conteudo: "Como está se sentindo com a nova dieta?", 
            data: "2023-10-15", hora: "14:30", lida: true})
    CREATE (msg2:Mensagem {id: 2, conteudo: "Estou me adaptando bem, mas sinto fome à tarde", 
            data: "2023-10-15", hora: "15:45", lida: true})
    CREATE (msg3:Mensagem {id: 3, conteudo: "Vamos ajustar seu lanche da tarde para resolver isso", 
            data: "2023-10-15", hora: "16:20", lida: true})
    CREATE (msg4:Mensagem {id: 4, conteudo: "Lembrete: sua consulta é amanhã às 14h", 
            data: "2023-10-16", hora: "09:00", lida: true})
    CREATE (msg5:Mensagem {id: 5, conteudo: "Confirmado, estarei lá", 
            data: "2023-10-16", hora: "09:15", lida: true})
    CREATE (msg6:Mensagem {id: 6, conteudo: "Como está se sentindo após a última consulta?", 
            data: "2023-10-20", hora: "11:00", lida: false})
    """
    tx.run(query)
    print("Mensagens criadas com sucesso!")


def load_appointments(tx):
    query = """
    // Criar Consultas
    CREATE (c1:Consulta {id: 1, data: "2023-09-15", hora: "14:00", 
            status: "Realizada", notas: "Avaliação inicial e definição de plano alimentar"})
    CREATE (c2:Consulta {id: 2, data: "2023-10-01", hora: "15:30", 
            status: "Realizada", notas: "Ajustes no plano devido à fome relatada"})
    CREATE (c3:Consulta {id: 3, data: "2023-10-17", hora: "14:00", 
            status: "Realizada", notas: "Progresso acima do esperado, reforço positivo"})
    CREATE (c4:Consulta {id: 4, data: "2023-11-01", hora: "16:00", 
            status: "Agendada", notas: ""})
    CREATE (c5:Consulta {id: 5, data: "2023-09-10", hora: "09:30", 
            status: "Realizada", notas: "Avaliação inicial, paciente com colesterol alto"})
    CREATE (c6:Consulta {id: 6, data: "2023-09-25", hora: "10:00", 
            status: "Realizada", notas: "Melhora nos exames laboratoriais"})
    CREATE (c7:Consulta {id: 7, data: "2023-10-10", hora: "11:00", 
            status: "Realizada", notas: "Exames demonstrando normalização do colesterol"})
    CREATE (c8:Consulta {id: 8, data: "2023-10-25", hora: "09:30", 
            status: "Cancelada", notas: "Paciente não pôde comparecer"})
    """
    tx.run(query)
    print("Consultas criadas com sucesso!")


def create_relationships(tx):
    """Cria os relacionamentos entre entidades - versão corrigida com statements individuais"""

    # --- Nutricionistas atendem Pacientes ---
    rel_queries = [
        """
        MATCH (n:Nutricionista {id: 1}), (p:Paciente {id: 1})
        CREATE (n)-[:ATENDE]->(p)
        """,
        """
        MATCH (n:Nutricionista {id: 1}), (p:Paciente {id: 3})
        CREATE (n)-[:ATENDE]->(p)
        """,
        """
        MATCH (n:Nutricionista {id: 2}), (p:Paciente {id: 2})
        CREATE (n)-[:ATENDE]->(p)
        """,
        """
        MATCH (n:Nutricionista {id: 3}), (p:Paciente {id: 4})
        CREATE (n)-[:ATENDE]->(p)
        """,
        """
        MATCH (n:Nutricionista {id: 3}), (p:Paciente {id: 5})
        CREATE (n)-[:ATENDE]->(p)
        """
    ]

    # --- Nutricionistas criam Planos Alimentares ---
    rel_queries.extend([
        """
        MATCH (n:Nutricionista {id: 1}), (pa:PlanoAlimentar {id: 1})
        CREATE (n)-[:CRIA]->(pa)
        """,
        """
        MATCH (n:Nutricionista {id: 1}), (pa:PlanoAlimentar {id: 2})
        CREATE (n)-[:CRIA]->(pa)
        """,
        """
        MATCH (n:Nutricionista {id: 2}), (pa:PlanoAlimentar {id: 4})
        CREATE (n)-[:CRIA]->(pa)
        """,
        """
        MATCH (n:Nutricionista {id: 3}), (pa:PlanoAlimentar {id: 3})
        CREATE (n)-[:CRIA]->(pa)
        """,
        """
        MATCH (n:Nutricionista {id: 3}), (pa:PlanoAlimentar {id: 5})
        CREATE (n)-[:CRIA]->(pa)
        """
    ])

    # --- Pacientes seguem Planos Alimentares ---
    rel_queries.extend([
        """
        MATCH (p:Paciente {id: 1}), (pa:PlanoAlimentar {id: 1})
        CREATE (p)-[:SEGUE]->(pa)
        """,
        """
        MATCH (p:Paciente {id: 2}), (pa:PlanoAlimentar {id: 4})
        CREATE (p)-[:SEGUE]->(pa)
        """,
        """
        MATCH (p:Paciente {id: 3}), (pa:PlanoAlimentar {id: 2})
        CREATE (p)-[:SEGUE]->(pa)
        """,
        """
        MATCH (p:Paciente {id: 4}), (pa:PlanoAlimentar {id: 3})
        CREATE (p)-[:SEGUE]->(pa)
        """,
        """
        MATCH (p:Paciente {id: 5}), (pa:PlanoAlimentar {id: 5})
        CREATE (p)-[:SEGUE]->(pa)
        """
    ])

    # --- Planos Alimentares incluem Alimentos ---
    rel_queries.extend([
        """
        MATCH (pa:PlanoAlimentar {id: 1}), (a:Alimento {id: 2})
        CREATE (pa)-[:INCLUI]->(a)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 1}), (a:Alimento {id: 3})
        CREATE (pa)-[:INCLUI]->(a)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 1}), (a:Alimento {id: 4})
        CREATE (pa)-[:INCLUI]->(a)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 2}), (a:Alimento {id: 2})
        CREATE (pa)-[:INCLUI]->(a)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 2}), (a:Alimento {id: 5})
        CREATE (pa)-[:INCLUI]->(a)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 2}), (a:Alimento {id: 8})
        CREATE (pa)-[:INCLUI]->(a)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 3}), (a:Alimento {id: 4})
        CREATE (pa)-[:INCLUI]->(a)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 3}), (a:Alimento {id: 6})
        CREATE (pa)-[:INCLUI]->(a)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 4}), (a:Alimento {id: 5})
        CREATE (pa)-[:INCLUI]->(a)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 4}), (a:Alimento {id: 6})
        CREATE (pa)-[:INCLUI]->(a)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 5}), (a:Alimento {id: 5})
        CREATE (pa)-[:INCLUI]->(a)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 5}), (a:Alimento {id: 9})
        CREATE (pa)-[:INCLUI]->(a)
        """
    ])

    # --- Planos Alimentares recomendam Receitas ---
    rel_queries.extend([
        """
        MATCH (pa:PlanoAlimentar {id: 1}), (r:Receita {id: 1})
        CREATE (pa)-[:RECOMENDA]->(r)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 1}), (r:Receita {id: 5})
        CREATE (pa)-[:RECOMENDA]->(r)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 2}), (r:Receita {id: 3})
        CREATE (pa)-[:RECOMENDA]->(r)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 2}), (r:Receita {id: 4})
        CREATE (pa)-[:RECOMENDA]->(r)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 3}), (r:Receita {id: 5})
        CREATE (pa)-[:RECOMENDA]->(r)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 4}), (r:Receita {id: 3})
        CREATE (pa)-[:RECOMENDA]->(r)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 5}), (r:Receita {id: 1})
        CREATE (pa)-[:RECOMENDA]->(r)
        """,
        """
        MATCH (pa:PlanoAlimentar {id: 5}), (r:Receita {id: 3})
        CREATE (pa)-[:RECOMENDA]->(r)
        """
    ])

    # --- Receitas contêm Alimentos ---
    rel_queries.extend([
        """
        MATCH (r:Receita {id: 1}), (a:Alimento {id: 2})
        CREATE (r)-[:CONTEM {quantidade: "100g"}]->(a)
        """,
        """
        MATCH (r:Receita {id: 1}), (a:Alimento {id: 4})
        CREATE (r)-[:CONTEM {quantidade: "50g"}]->(a)
        """,
        """
        MATCH (r:Receita {id: 1}), (a:Alimento {id: 9})
        CREATE (r)-[:CONTEM {quantidade: "5ml"}]->(a)
        """,
        """
        MATCH (r:Receita {id: 2}), (a:Alimento {id: 10})
        CREATE (r)-[:CONTEM {quantidade: "1 unidade"}]->(a)
        """,
        """
        MATCH (r:Receita {id: 3}), (a:Alimento {id: 5})
        CREATE (r)-[:CONTEM {quantidade: "150g"}]->(a)
        """,
        """
        MATCH (r:Receita {id: 3}), (a:Alimento {id: 4})
        CREATE (r)-[:CONTEM {quantidade: "100g"}]->(a)
        """,
        """
        MATCH (r:Receita {id: 3}), (a:Alimento {id: 3})
        CREATE (r)-[:CONTEM {quantidade: "100g"}]->(a)
        """,
        """
        MATCH (r:Receita {id: 4}), (a:Alimento {id: 7})
        CREATE (r)-[:CONTEM {quantidade: "200g"}]->(a)
        """,
        """
        MATCH (r:Receita {id: 4}), (a:Alimento {id: 10})
        CREATE (r)-[:CONTEM {quantidade: "1 unidade"}]->(a)
        """,
        """
        MATCH (r:Receita {id: 4}), (a:Alimento {id: 8})
        CREATE (r)-[:CONTEM {quantidade: "30g"}]->(a)
        """,
        """
        MATCH (r:Receita {id: 5}), (a:Alimento {id: 4})
        CREATE (r)-[:CONTEM {quantidade: "50g"}]->(a)
        """
    ])

    # --- Pacientes consomem Refeições ---
    rel_queries.extend([
        """
        MATCH (p:Paciente {id: 1}), (r:Refeicao {id: 1})
        CREATE (p)-[:CONSOME]->(r)
        """,
        """
        MATCH (p:Paciente {id: 1}), (r:Refeicao {id: 2})
        CREATE (p)-[:CONSOME]->(r)
        """,
        """
        MATCH (p:Paciente {id: 1}), (r:Refeicao {id: 3})
        CREATE (p)-[:CONSOME]->(r)
        """,
        """
        MATCH (p:Paciente {id: 1}), (r:Refeicao {id: 4})
        CREATE (p)-[:CONSOME]->(r)
        """,
        """
        MATCH (p:Paciente {id: 2}), (r:Refeicao {id: 5})
        CREATE (p)-[:CONSOME]->(r)
        """,
        """
        MATCH (p:Paciente {id: 2}), (r:Refeicao {id: 6})
        CREATE (p)-[:CONSOME]->(r)
        """,
        """
        MATCH (p:Paciente {id: 2}), (r:Refeicao {id: 7})
        CREATE (p)-[:CONSOME]->(r)
        """,
        """
        MATCH (p:Paciente {id: 2}), (r:Refeicao {id: 8})
        CREATE (p)-[:CONSOME]->(r)
        """
    ])

    # --- Refeições incluem Alimentos/Receitas ---
    rel_queries.extend([
        """
        MATCH (ref:Refeicao {id: 1}), (r:Receita {id: 4})
        CREATE (ref)-[:INCLUI]->(r)
        """,
        """
        MATCH (ref:Refeicao {id: 2}), (r:Receita {id: 1})
        CREATE (ref)-[:INCLUI]->(r)
        """,
        """
        MATCH (ref:Refeicao {id: 3}), (a:Alimento {id: 1})
        CREATE (ref)-[:INCLUI]->(a)
        """,
        """
        MATCH (ref:Refeicao {id: 3}), (a:Alimento {id: 7})
        CREATE (ref)-[:INCLUI]->(a)
        """,
        """
        MATCH (ref:Refeicao {id: 4}), (r:Receita {id: 3})
        CREATE (ref)-[:INCLUI]->(r)
        """,
        """
        MATCH (ref:Refeicao {id: 5}), (r:Receita {id: 2})
        CREATE (ref)-[:INCLUI]->(r)
        """,
        """
        MATCH (ref:Refeicao {id: 6}), (r:Receita {id: 3})
        CREATE (ref)-[:INCLUI]->(r)
        """,
        """
        MATCH (ref:Refeicao {id: 7}), (a:Alimento {id: 1})
        CREATE (ref)-[:INCLUI]->(a)
        """,
        """
        MATCH (ref:Refeicao {id: 8}), (r:Receita {id: 5})
        CREATE (ref)-[:INCLUI]->(r)
        """
    ])

    # --- Pacientes possuem Medidas Corporais ---
    rel_queries.extend([
        """
        MATCH (p:Paciente {id: 1}), (m:MedidaCorporal {id: 1})
        CREATE (p)-[:POSSUI]->(m)
        """,
        """
        MATCH (p:Paciente {id: 1}), (m:MedidaCorporal {id: 2})
        CREATE (p)-[:POSSUI]->(m)
        """,
        """
        MATCH (p:Paciente {id: 1}), (m:MedidaCorporal {id: 3})
        CREATE (p)-[:POSSUI]->(m)
        """,
        """
        MATCH (p:Paciente {id: 2}), (m:MedidaCorporal {id: 4})
        CREATE (p)-[:POSSUI]->(m)
        """,
        """
        MATCH (p:Paciente {id: 2}), (m:MedidaCorporal {id: 5})
        CREATE (p)-[:POSSUI]->(m)
        """,
        """
        MATCH (p:Paciente {id: 2}), (m:MedidaCorporal {id: 6})
        CREATE (p)-[:POSSUI]->(m)
        """
    ])

    # --- Mensagens entre Pacientes e Nutricionistas ---
    rel_queries.extend([
        """
        MATCH (n:Nutricionista {id: 1}), (msg:Mensagem {id: 1}), (p:Paciente {id: 1})
        CREATE (n)-[:ENVIA]->(msg)-[:PARA]->(p)
        """,
        """
        MATCH (p:Paciente {id: 1}), (msg:Mensagem {id: 2}), (n:Nutricionista {id: 1})
        CREATE (p)-[:ENVIA]->(msg)-[:PARA]->(n)
        """,
        """
        MATCH (n:Nutricionista {id: 1}), (msg:Mensagem {id: 3}), (p:Paciente {id: 1})
        CREATE (n)-[:ENVIA]->(msg)-[:PARA]->(p)
        """,
        """
        MATCH (n:Nutricionista {id: 1}), (msg:Mensagem {id: 4}), (p:Paciente {id: 1})
        CREATE (n)-[:ENVIA]->(msg)-[:PARA]->(p)
        """,
        """
        MATCH (p:Paciente {id: 1}), (msg:Mensagem {id: 5}), (n:Nutricionista {id: 1})
        CREATE (p)-[:ENVIA]->(msg)-[:PARA]->(n)
        """,
        """
        MATCH (n:Nutricionista {id: 2}), (msg:Mensagem {id: 6}), (p:Paciente {id: 2})
        CREATE (n)-[:ENVIA]->(msg)-[:PARA]->(p)
        """
    ])

    # --- Consultas entre Pacientes e Nutricionistas ---
    rel_queries.extend([
        """
        MATCH (p:Paciente {id: 1}), (c:Consulta {id: 1}), (n:Nutricionista {id: 1})
        CREATE (p)-[:AGENDA]->(c)-[:COM]->(n)
        """,
        """
        MATCH (p:Paciente {id: 1}), (c:Consulta {id: 2}), (n:Nutricionista {id: 1})
        CREATE (p)-[:AGENDA]->(c)-[:COM]->(n)
        """,
        """
        MATCH (p:Paciente {id: 1}), (c:Consulta {id: 3}), (n:Nutricionista {id: 1})
        CREATE (p)-[:AGENDA]->(c)-[:COM]->(n)
        """,
        """
        MATCH (p:Paciente {id: 1}), (c:Consulta {id: 4}), (n:Nutricionista {id: 1})
        CREATE (p)-[:AGENDA]->(c)-[:COM]->(n)
        """,
        """
        MATCH (p:Paciente {id: 2}), (c:Consulta {id: 5}), (n:Nutricionista {id: 2})
        CREATE (p)-[:AGENDA]->(c)-[:COM]->(n)
        """,
        """
        MATCH (p:Paciente {id: 2}), (c:Consulta {id: 6}), (n:Nutricionista {id: 2})
        CREATE (p)-[:AGENDA]->(c)-[:COM]->(n)
        """,
        """
        MATCH (p:Paciente {id: 2}), (c:Consulta {id: 7}), (n:Nutricionista {id: 2})
        CREATE (p)-[:AGENDA]->(c)-[:COM]->(n)
        """,
        """
        MATCH (p:Paciente {id: 2}), (c:Consulta {id: 8}), (n:Nutricionista {id: 2})
        CREATE (p)-[:AGENDA]->(c)-[:COM]->(n)
        """
    ])

    # Executar cada query individualmente
    for i, query in enumerate(rel_queries):
        try:
            tx.run(query)
            # Imprimir progresso a cada 10 relacionamentos
            if (i + 1) % 10 == 0:
                print(f"Criados {i + 1} de {len(rel_queries)} relacionamentos...")
        except Exception as e:
            print(f"Erro ao criar relacionamento #{i + 1}: {str(e)}")
            print(f"Query problemática: {query}")

    print(f"Total de {len(rel_queries)} relacionamentos criados com sucesso!")


def load_all_data():
    """Carrega todos os dados no banco Neo4j"""
    if not wait_for_neo4j():
        return False

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        with driver.session() as session:
            # Limpar o banco antes de carregar novos dados
            session.run("MATCH (n) DETACH DELETE n")
            print("Banco de dados limpo com sucesso!")

            # Carregar todos os nós
            session.execute_write(load_nutritionists)
            session.execute_write(load_patients)
            session.execute_write(load_foods)
            session.execute_write(load_recipes)
            session.execute_write(load_diet_plans)
            session.execute_write(load_meals)
            session.execute_write(load_measurements)
            session.execute_write(load_messages)
            session.execute_write(load_appointments)

            # Criar todos os relacionamentos
            session.execute_write(create_relationships)

        print("Todos os dados foram carregados com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        return False
    finally:
        driver.close()


def create_database_dump():
    """Cria um dump do banco de dados"""
    try:
        import datetime
        import subprocess

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"neo4j_dump_{timestamp}.dump"

        # Este comando assume que o Neo4j está em um container chamado diet_app_neo4j
        command = f"docker exec diet_app_neo4j neo4j-admin dump --database=neo4j --to=/var/lib/neo4j/import/{filename}"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(f"Dump criado com sucesso: {filename}")
        print("Para copiar o arquivo para o seu computador, use:")
        print(f"docker cp diet_app_neo4j:/var/lib/neo4j/import/{filename} ./{filename}")

        return True
    except Exception as e:
        print(f"Erro ao criar dump: {str(e)}")
        return False


if __name__ == "__main__":
    if load_all_data():
        # Descomente a linha abaixo se quiser criar um dump automaticamente
        # create_database_dump()
        pass