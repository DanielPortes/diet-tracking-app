import os
import time
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# Carregar variáveis de ambiente (opcional)
load_dotenv()

# Configurações de conexão
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:senha123@localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "diet_app")
MAX_CONNECTION_RETRY = 10
RETRY_INTERVAL = 5  # segundos


def wait_for_mongodb():
    """Espera até que o MongoDB esteja pronto para aceitar conexões."""
    client = None
    for i in range(MAX_CONNECTION_RETRY):
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            # Verificar se a conexão está funcionando
            if client is None:
                raise ConnectionFailure("Failed to create MongoDB client")

            # Check if admin exists before trying to access it
            client.admin.command("ping")
            print("Conexão com MongoDB estabelecida com sucesso!")
            return client
        except (ConnectionFailure, OperationFailure) as e:
            print(
                f"Tentativa {i + 1}/{MAX_CONNECTION_RETRY}: MongoDB ainda não está pronto: {str(e)}"
            )
            if client:
                client.close()
            time.sleep(RETRY_INTERVAL)

    print("Não foi possível conectar ao MongoDB após várias tentativas.")
    return None


def clear_database(db):
    """Limpa todas as collections do banco de dados."""
    for collection in db.list_collection_names():
        db[collection].drop()
    print("Banco de dados limpo com sucesso!")


def load_nutritionists(db):
    """Carrega dados de nutricionistas no MongoDB."""
    collection = db.nutritionists

    nutritionists = [
        {
            "_id": 1,
            "nome": "Ana Silva",
            "especialidade": "Nutrição Esportiva",
            "experiencia": 8,
            "email": "ana@nutri.com",
            "telefone": "21-99999-1111",
        },
        {
            "_id": 2,
            "nome": "Carlos Mendes",
            "especialidade": "Nutrição Clínica",
            "experiencia": 5,
            "email": "carlos@nutri.com",
            "telefone": "21-99999-2222",
        },
        {
            "_id": 3,
            "nome": "Mariana Costa",
            "especialidade": "Nutrição Funcional",
            "experiencia": 12,
            "email": "mariana@nutri.com",
            "telefone": "21-99999-3333",
        },
    ]

    collection.insert_many(nutritionists)
    print(f"Inseridos {len(nutritionists)} nutricionistas com sucesso!")


def load_patients(db):
    """Carrega dados de pacientes no MongoDB."""
    collection = db.patients

    patients = [
        {
            "_id": 1,
            "nome": "João Pereira",
            "idade": 35,
            "genero": "M",
            "altura": 178,
            "peso_inicial": 92,
            "email": "joao@email.com",
            "telefone": "21-88888-1111",
            "restricoes": ["Glúten"],
            "alergias": ["Amendoim"],
            "objetivo": "Emagrecimento",
            "nutricionista_id": 1,
        },
        {
            "_id": 2,
            "nome": "Maria Santos",
            "idade": 42,
            "genero": "F",
            "altura": 165,
            "peso_inicial": 78,
            "email": "maria@email.com",
            "telefone": "21-88888-2222",
            "restricoes": ["Lactose"],
            "alergias": [],
            "objetivo": "Controle de colesterol",
            "nutricionista_id": 2,
        },
        {
            "_id": 3,
            "nome": "Pedro Alves",
            "idade": 28,
            "genero": "M",
            "altura": 182,
            "peso_inicial": 75,
            "email": "pedro@email.com",
            "telefone": "21-88888-3333",
            "restricoes": [],
            "alergias": [],
            "objetivo": "Ganho de massa muscular",
            "nutricionista_id": 1,
        },
        {
            "_id": 4,
            "nome": "Lúcia Ferreira",
            "idade": 55,
            "genero": "F",
            "altura": 160,
            "peso_inicial": 85,
            "email": "lucia@email.com",
            "telefone": "21-88888-4444",
            "restricoes": ["Sódio"],
            "alergias": ["Frutos do mar"],
            "objetivo": "Controle de diabetes",
            "nutricionista_id": 3,
        },
        {
            "_id": 5,
            "nome": "Ricardo Gomes",
            "idade": 30,
            "genero": "M",
            "altura": 175,
            "peso_inicial": 88,
            "email": "ricardo@email.com",
            "telefone": "21-88888-5555",
            "restricoes": [],
            "alergias": ["Nozes"],
            "objetivo": "Emagrecimento",
            "nutricionista_id": 3,
        },
    ]

    collection.insert_many(patients)
    print(f"Inseridos {len(patients)} pacientes com sucesso!")


def load_foods(db):
    """Carrega dados de alimentos no MongoDB."""
    collection = db.foods

    foods = [
        {
            "_id": 1,
            "nome": "Maçã",
            "porcao": "1 unidade (150g)",
            "calorias": 95,
            "proteinas": 0.5,
            "carboidratos": 25,
            "gorduras": 0.3,
            "fibras": 4.4,
            "grupo": "Frutas",
        },
        {
            "_id": 2,
            "nome": "Peito de Frango",
            "porcao": "100g",
            "calorias": 165,
            "proteinas": 31,
            "carboidratos": 0,
            "gorduras": 3.6,
            "fibras": 0,
            "grupo": "Carnes",
        },
        {
            "_id": 3,
            "nome": "Arroz Integral",
            "porcao": "100g cozido",
            "calorias": 112,
            "proteinas": 2.6,
            "carboidratos": 23.5,
            "gorduras": 0.9,
            "fibras": 1.8,
            "grupo": "Cereais",
        },
        {
            "_id": 4,
            "nome": "Brócolis",
            "porcao": "100g",
            "calorias": 34,
            "proteinas": 2.8,
            "carboidratos": 6.6,
            "gorduras": 0.4,
            "fibras": 2.6,
            "grupo": "Vegetais",
        },
        {
            "_id": 5,
            "nome": "Salmão",
            "porcao": "100g",
            "calorias": 206,
            "proteinas": 22,
            "carboidratos": 0,
            "gorduras": 13,
            "fibras": 0,
            "grupo": "Peixes",
        },
        {
            "_id": 6,
            "nome": "Lentilha",
            "porcao": "100g cozida",
            "calorias": 116,
            "proteinas": 9,
            "carboidratos": 20,
            "gorduras": 0.4,
            "fibras": 7.9,
            "grupo": "Leguminosas",
        },
        {
            "_id": 7,
            "nome": "Iogurte Natural",
            "porcao": "100g",
            "calorias": 59,
            "proteinas": 3.5,
            "carboidratos": 4.7,
            "gorduras": 3.3,
            "fibras": 0,
            "grupo": "Laticínios",
        },
        {
            "_id": 8,
            "nome": "Aveia",
            "porcao": "30g",
            "calorias": 117,
            "proteinas": 4,
            "carboidratos": 21,
            "gorduras": 2,
            "fibras": 3,
            "grupo": "Cereais",
        },
        {
            "_id": 9,
            "nome": "Azeite",
            "porcao": "1 colher (10ml)",
            "calorias": 90,
            "proteinas": 0,
            "carboidratos": 0,
            "gorduras": 10,
            "fibras": 0,
            "grupo": "Óleos",
        },
        {
            "_id": 10,
            "nome": "Banana",
            "porcao": "1 unidade (120g)",
            "calorias": 105,
            "proteinas": 1.3,
            "carboidratos": 27,
            "gorduras": 0.4,
            "fibras": 3.1,
            "grupo": "Frutas",
        },
    ]

    collection.insert_many(foods)
    print(f"Inseridos {len(foods)} alimentos com sucesso!")


def load_recipes(db):
    """Carrega dados de receitas no MongoDB."""
    collection = db.recipes

    recipes = [
        {
            "_id": 1,
            "nome": "Salada de Frango com Abacate",
            "instrucoes": "Corte o peito de frango em cubos e grelhe. Misture com abacate, tomate e folhas verdes. Tempere com azeite, limão e sal.",
            "tempo_preparo": 20,
            "dificuldade": "Fácil",
            "calorias": 320,
            "ingredientes": [
                {"food_id": 2, "quantidade": "100g"},
                {"food_id": 4, "quantidade": "50g"},
                {"food_id": 9, "quantidade": "5ml"},
            ],
        },
        {
            "_id": 2,
            "nome": "Bowl de Açaí com Frutas",
            "instrucoes": "Misture açaí congelado batido com banana. Adicione granola, frutas frescas e mel.",
            "tempo_preparo": 10,
            "dificuldade": "Fácil",
            "calorias": 450,
            "ingredientes": [{"food_id": 10, "quantidade": "1 unidade"}],
        },
        {
            "_id": 3,
            "nome": "Salmão Grelhado com Legumes",
            "instrucoes": "Grelhe o filé de salmão. Refogue brócolis, cenoura e abobrinha. Sirva com arroz integral.",
            "tempo_preparo": 30,
            "dificuldade": "Médio",
            "calorias": 480,
            "ingredientes": [
                {"food_id": 5, "quantidade": "150g"},
                {"food_id": 4, "quantidade": "100g"},
                {"food_id": 3, "quantidade": "100g"},
            ],
        },
        {
            "_id": 4,
            "nome": "Smoothie Proteico",
            "instrucoes": "Bata no liquidificador iogurte, banana, aveia, pasta de amendoim e mel.",
            "tempo_preparo": 5,
            "dificuldade": "Fácil",
            "calorias": 350,
            "ingredientes": [
                {"food_id": 7, "quantidade": "200g"},
                {"food_id": 10, "quantidade": "1 unidade"},
                {"food_id": 8, "quantidade": "30g"},
            ],
        },
        {
            "_id": 5,
            "nome": "Omelete de Legumes",
            "instrucoes": "Bata 2 ovos, adicione espinafre, tomate e queijo. Cozinhe em frigideira antiaderente.",
            "tempo_preparo": 15,
            "dificuldade": "Fácil",
            "calorias": 280,
            "ingredientes": [{"food_id": 4, "quantidade": "50g"}],
        },
    ]

    collection.insert_many(recipes)
    print(f"Inseridas {len(recipes)} receitas com sucesso!")


def load_diet_plans(db):
    """Carrega dados de planos alimentares no MongoDB."""
    collection = db.dietPlans

    diet_plans = [
        {
            "_id": 1,
            "nome": "Emagrecimento Saudável",
            "descricao": "Plano focado em déficit calórico moderado com alimentos nutritivos",
            "objetivo": "Perda de peso",
            "duracao": 90,
            "calorias_diarias": 1800,
            "macronutrientes": {
                "proteinas": "30%",
                "carboidratos": "40%",
                "gorduras": "30%",
            },
            "nutricionista_id": 1,
            "paciente_id": 1,
            "alimentos_recomendados": [2, 3, 4],
            "receitas_recomendadas": [1, 5],
        },
        {
            "_id": 2,
            "nome": "Ganho de Massa",
            "descricao": "Plano focado em superávit calórico com alta proteína",
            "objetivo": "Hipertrofia",
            "duracao": 120,
            "calorias_diarias": 2800,
            "macronutrientes": {
                "proteinas": "35%",
                "carboidratos": "45%",
                "gorduras": "20%",
            },
            "nutricionista_id": 1,
            "paciente_id": 3,
            "alimentos_recomendados": [2, 5, 8],
            "receitas_recomendadas": [3, 4],
        },
        {
            "_id": 3,
            "nome": "Controle Glicêmico",
            "descricao": "Plano para controle de diabetes com baixo índice glicêmico",
            "objetivo": "Controle de glicemia",
            "duracao": 180,
            "calorias_diarias": 1600,
            "macronutrientes": {
                "proteinas": "25%",
                "carboidratos": "35%",
                "gorduras": "40%",
            },
            "nutricionista_id": 3,
            "paciente_id": 4,
            "alimentos_recomendados": [4, 6],
            "receitas_recomendadas": [5],
        },
        {
            "_id": 4,
            "nome": "Controle de Colesterol",
            "descricao": "Plano para redução de colesterol LDL e aumento de HDL",
            "objetivo": "Saúde cardiovascular",
            "duracao": 90,
            "calorias_diarias": 2000,
            "macronutrientes": {
                "proteinas": "25%",
                "carboidratos": "50%",
                "gorduras": "25%",
            },
            "nutricionista_id": 2,
            "paciente_id": 2,
            "alimentos_recomendados": [5, 6],
            "receitas_recomendadas": [3],
        },
        {
            "_id": 5,
            "nome": "Dieta Anti-inflamatória",
            "descricao": "Plano rico em antioxidantes e ômega-3",
            "objetivo": "Redução de inflamação",
            "duracao": 60,
            "calorias_diarias": 2200,
            "macronutrientes": {
                "proteinas": "20%",
                "carboidratos": "55%",
                "gorduras": "25%",
            },
            "nutricionista_id": 3,
            "paciente_id": 5,
            "alimentos_recomendados": [5, 9],
            "receitas_recomendadas": [1, 3],
        },
    ]

    collection.insert_many(diet_plans)
    print(f"Inseridos {len(diet_plans)} planos alimentares com sucesso!")


def load_meals(db):
    """Carrega dados de refeições no MongoDB."""
    collection = db.meals

    meals = [
        {
            "_id": 1,
            "tipo": "Café da manhã",
            "data": datetime(2023, 10, 18),
            "hora": "08:00",
            "paciente_id": 1,
            "calorias": 320,
            "adesao": "Completa",
            "registro_foto": True,
            "alimentos": [],
            "receitas": [4],
        },
        {
            "_id": 2,
            "tipo": "Almoço",
            "data": datetime(2023, 10, 18),
            "hora": "12:30",
            "paciente_id": 1,
            "calorias": 580,
            "adesao": "Parcial",
            "registro_foto": True,
            "alimentos": [],
            "receitas": [1],
        },
        {
            "_id": 3,
            "tipo": "Lanche",
            "data": datetime(2023, 10, 18),
            "hora": "16:00",
            "paciente_id": 1,
            "calorias": 180,
            "adesao": "Completa",
            "registro_foto": False,
            "alimentos": [1, 7],
            "receitas": [],
        },
        {
            "_id": 4,
            "tipo": "Jantar",
            "data": datetime(2023, 10, 18),
            "hora": "20:00",
            "paciente_id": 1,
            "calorias": 450,
            "adesao": "Completa",
            "registro_foto": True,
            "alimentos": [],
            "receitas": [3],
        },
        {
            "_id": 5,
            "tipo": "Café da manhã",
            "data": datetime(2023, 10, 19),
            "hora": "07:45",
            "paciente_id": 2,
            "calorias": 340,
            "adesao": "Completa",
            "registro_foto": True,
            "alimentos": [],
            "receitas": [2],
        },
        {
            "_id": 6,
            "tipo": "Almoço",
            "data": datetime(2023, 10, 19),
            "hora": "13:00",
            "paciente_id": 2,
            "calorias": 620,
            "adesao": "Completa",
            "registro_foto": True,
            "alimentos": [],
            "receitas": [3],
        },
        {
            "_id": 7,
            "tipo": "Lanche",
            "data": datetime(2023, 10, 19),
            "hora": "15:30",
            "paciente_id": 2,
            "calorias": 200,
            "adesao": "Parcial",
            "registro_foto": False,
            "alimentos": [1],
            "receitas": [],
        },
        {
            "_id": 8,
            "tipo": "Jantar",
            "data": datetime(2023, 10, 19),
            "hora": "19:30",
            "paciente_id": 2,
            "calorias": 380,
            "adesao": "Não realizada",
            "registro_foto": False,
            "alimentos": [],
            "receitas": [5],
        },
    ]

    collection.insert_many(meals)
    print(f"Inseridas {len(meals)} refeições com sucesso!")


def load_measurements(db):
    """Carrega dados de medidas corporais no MongoDB."""
    collection = db.measurements

    measurements = [
        {
            "_id": 1,
            "paciente_id": 1,
            "data": datetime(2023, 9, 15),
            "peso": 92,
            "imc": 29.1,
            "gordura_corporal": 28,
            "medidas": {"cintura": 102, "quadril": 106},
            "pressao": "130/85",
        },
        {
            "_id": 2,
            "paciente_id": 1,
            "data": datetime(2023, 10, 1),
            "peso": 89.5,
            "imc": 28.2,
            "gordura_corporal": 26.8,
            "medidas": {"cintura": 99, "quadril": 105},
            "pressao": "128/83",
        },
        {
            "_id": 3,
            "paciente_id": 1,
            "data": datetime(2023, 10, 15),
            "peso": 87.8,
            "imc": 27.7,
            "gordura_corporal": 25.5,
            "medidas": {"cintura": 97, "quadril": 104},
            "pressao": "125/82",
        },
        {
            "_id": 4,
            "paciente_id": 2,
            "data": datetime(2023, 9, 10),
            "peso": 78,
            "imc": 28.7,
            "gordura_corporal": 32,
            "medidas": {"cintura": 91, "quadril": 110},
            "pressao": "135/88",
        },
        {
            "_id": 5,
            "paciente_id": 2,
            "data": datetime(2023, 9, 25),
            "peso": 77.2,
            "imc": 28.4,
            "gordura_corporal": 31.5,
            "medidas": {"cintura": 90, "quadril": 109},
            "pressao": "132/86",
        },
        {
            "_id": 6,
            "paciente_id": 2,
            "data": datetime(2023, 10, 10),
            "peso": 76.5,
            "imc": 28.1,
            "gordura_corporal": 30.8,
            "medidas": {"cintura": 88, "quadril": 108},
            "pressao": "130/85",
        },
    ]

    collection.insert_many(measurements)
    print(f"Inseridas {len(measurements)} medidas corporais com sucesso!")


def load_messages(db):
    """Carrega dados de mensagens no MongoDB."""
    collection = db.messages

    messages = [
        {
            "_id": 1,
            "de_id": 1,
            "de_tipo": "nutricionista",
            "para_id": 1,
            "para_tipo": "paciente",
            "conteudo": "Como está se sentindo com a nova dieta?",
            "data": datetime(2023, 10, 15),
            "hora": "14:30",
            "lida": True,
        },
        {
            "_id": 2,
            "de_id": 1,
            "de_tipo": "paciente",
            "para_id": 1,
            "para_tipo": "nutricionista",
            "conteudo": "Estou me adaptando bem, mas sinto fome à tarde",
            "data": datetime(2023, 10, 15),
            "hora": "15:45",
            "lida": True,
        },
        {
            "_id": 3,
            "de_id": 1,
            "de_tipo": "nutricionista",
            "para_id": 1,
            "para_tipo": "paciente",
            "conteudo": "Vamos ajustar seu lanche da tarde para resolver isso",
            "data": datetime(2023, 10, 15),
            "hora": "16:20",
            "lida": True,
        },
        {
            "_id": 4,
            "de_id": 1,
            "de_tipo": "nutricionista",
            "para_id": 1,
            "para_tipo": "paciente",
            "conteudo": "Lembrete: sua consulta é amanhã às 14h",
            "data": datetime(2023, 10, 16),
            "hora": "09:00",
            "lida": True,
        },
        {
            "_id": 5,
            "de_id": 1,
            "de_tipo": "paciente",
            "para_id": 1,
            "para_tipo": "nutricionista",
            "conteudo": "Confirmado, estarei lá",
            "data": datetime(2023, 10, 16),
            "hora": "09:15",
            "lida": True,
        },
        {
            "_id": 6,
            "de_id": 2,
            "de_tipo": "nutricionista",
            "para_id": 2,
            "para_tipo": "paciente",
            "conteudo": "Como está se sentindo após a última consulta?",
            "data": datetime(2023, 10, 20),
            "hora": "11:00",
            "lida": False,
        },
    ]

    collection.insert_many(messages)
    print(f"Inseridas {len(messages)} mensagens com sucesso!")


def load_appointments(db):
    """Carrega dados de consultas no MongoDB."""
    collection = db.appointments

    appointments = [
        {
            "_id": 1,
            "nutricionista_id": 1,
            "paciente_id": 1,
            "data": datetime(2023, 9, 15),
            "hora": "14:00",
            "status": "Realizada",
            "notas": "Avaliação inicial e definição de plano alimentar",
        },
        {
            "_id": 2,
            "nutricionista_id": 1,
            "paciente_id": 1,
            "data": datetime(2023, 10, 1),
            "hora": "15:30",
            "status": "Realizada",
            "notas": "Ajustes no plano devido à fome relatada",
        },
        {
            "_id": 3,
            "nutricionista_id": 1,
            "paciente_id": 1,
            "data": datetime(2023, 10, 17),
            "hora": "14:00",
            "status": "Realizada",
            "notas": "Progresso acima do esperado, reforço positivo",
        },
        {
            "_id": 4,
            "nutricionista_id": 1,
            "paciente_id": 1,
            "data": datetime(2023, 11, 1),
            "hora": "16:00",
            "status": "Agendada",
            "notas": "",
        },
        {
            "_id": 5,
            "nutricionista_id": 2,
            "paciente_id": 2,
            "data": datetime(2023, 9, 10),
            "hora": "09:30",
            "status": "Realizada",
            "notas": "Avaliação inicial, paciente com colesterol alto",
        },
        {
            "_id": 6,
            "nutricionista_id": 2,
            "paciente_id": 2,
            "data": datetime(2023, 9, 25),
            "hora": "10:00",
            "status": "Realizada",
            "notas": "Melhora nos exames laboratoriais",
        },
        {
            "_id": 7,
            "nutricionista_id": 2,
            "paciente_id": 2,
            "data": datetime(2023, 10, 10),
            "hora": "11:00",
            "status": "Realizada",
            "notas": "Exames demonstrando normalização do colesterol",
        },
        {
            "_id": 8,
            "nutricionista_id": 2,
            "paciente_id": 2,
            "data": datetime(2023, 10, 25),
            "hora": "09:30",
            "status": "Cancelada",
            "notas": "Paciente não pôde comparecer",
        },
    ]

    collection.insert_many(appointments)
    print(f"Inseridas {len(appointments)} consultas com sucesso!")


def create_mongodb_dump():
    """Cria um dump do banco de dados MongoDB."""
    try:
        import datetime
        import subprocess

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        directory = f"mongodb_dump_{timestamp}"

        # Este comando assume que o MongoDB está em um container chamado diet_app_mongodb
        command = f"docker exec diet_app_mongodb mongodump --username admin --password senha123 --authenticationDatabase admin --db {MONGO_DB} --out /data/db/{directory}"
        subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        print(f"Dump criado com sucesso: {directory}")
        print("Para copiar o dump para o seu computador, use:")
        print(f"docker cp diet_app_mongodb:/data/db/{directory} ./{directory}")

        return True
    except Exception as e:
        print(f"Erro ao criar dump: {str(e)}")
        return False


def load_all_data():
    """Carrega todos os dados no MongoDB."""
    client = wait_for_mongodb()
    if not client:
        return False

    try:
        db = client[MONGO_DB]

        # Limpar o banco antes de carregar novos dados
        clear_database(db)

        # Carregar todos os dados
        load_nutritionists(db)
        load_patients(db)
        load_foods(db)
        load_recipes(db)
        load_diet_plans(db)
        load_meals(db)
        load_measurements(db)
        load_messages(db)
        load_appointments(db)

        print("\nTodos os dados foram carregados com sucesso no MongoDB!")
        return True
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        return False
    finally:
        if client:
            client.close()


if __name__ == "__main__":
    if load_all_data():
        # Descomente a linha abaixo se quiser criar um dump automaticamente
        # create_mongodb_dump()
        pass
