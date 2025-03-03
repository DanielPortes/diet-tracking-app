import os
import sys
import time
import unittest
from pathlib import Path
from typing import ClassVar

from neo4j import GraphDatabase
from pymongo import MongoClient


class DatabaseSetupTests(unittest.TestCase):
    """Test the setup and connectivity of Neo4j and MongoDB databases."""

    # Define class variables to help mypy understand these are class attributes
    neo4j_uri: ClassVar[str]
    neo4j_user: ClassVar[str]
    neo4j_password: ClassVar[str]
    mongo_uri: ClassVar[str]
    mongo_db: ClassVar[str]

    @classmethod
    def setUpClass(cls):
        """Set up test environment once before all tests."""
        cls.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        cls.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        cls.neo4j_password = os.getenv("NEO4J_PASSWORD", "senha123")

        cls.mongo_uri = os.getenv(
            "MONGO_URI", "mongodb://admin:senha123@localhost:27017/"
        )
        cls.mongo_db = os.getenv("MONGO_DB", "diet_app")

        # Wait for databases to be ready (in CI environment)
        if os.getenv("CI"):
            print("Running in CI environment, waiting for databases...")
            time.sleep(20)

    def test_neo4j_connection(self):
        """Test if we can connect to Neo4j."""
        driver = None
        try:
            driver = GraphDatabase.driver(
                self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password)
            )
            with driver.session() as session:
                result = session.run("RETURN 1 AS num")
                record = result.single()
                # Add null check to handle potential None value
                self.assertIsNotNone(record, "Neo4j connection returned no record")
                if record:  # This check helps mypy understand record is not None
                    self.assertEqual(record["num"], 1, "Neo4j connection test failed")
        except Exception as e:
            self.fail(f"Neo4j connection raised exception: {e}")
        finally:
            if driver:
                driver.close()

    def test_mongodb_connection(self):
        """Test if we can connect to MongoDB."""
        client = None
        try:
            client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            # Test connection with simple command
            self.assertIsNotNone(client, "MongoDB client is None")
            if client:  # This check helps mypy understand client is not None
                result = client.admin.command("ping")
                self.assertEqual(result["ok"], 1.0, "MongoDB connection test failed")
        except Exception as e:
            self.fail(f"MongoDB connection raised exception: {e}")
        finally:
            if client:
                client.close()

    def test_project_files_exist(self):
        """Test if all required project files exist."""
        required_files = [
            "docker-compose.yml",
            "load_data.py",
            "load_mongodb_data.py",
            "load_all_databases.py",
            "requirements.txt",
            "README.md",
        ]

        for file in required_files:
            self.assertTrue(Path(file).exists(), f"Required file {file} does not exist")


class DataLoadingTests(unittest.TestCase):
    """Test data loading and basic queries for both databases."""

    # Define class variables to help mypy understand these are class attributes
    neo4j_uri: ClassVar[str]
    neo4j_user: ClassVar[str]
    neo4j_password: ClassVar[str]
    mongo_uri: ClassVar[str]
    mongo_db: ClassVar[str]

    @classmethod
    def setUpClass(cls):
        """Set up test environment and load data."""
        cls.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        cls.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        cls.neo4j_password = os.getenv("NEO4J_PASSWORD", "senha123")

        cls.mongo_uri = os.getenv(
            "MONGO_URI", "mongodb://admin:senha123@localhost:27017/"
        )
        cls.mongo_db = os.getenv("MONGO_DB", "diet_app")

        # Skip data loading in CI environment as it will be done in workflow
        if not os.getenv("CI"):
            try:
                # Import and run scripts directly
                sys.path.append(".")  # Ensure current directory is in path
                import load_data
                import load_mongodb_data

                load_data.load_all_data()
                load_mongodb_data.load_all_data()
            except Exception as e:
                print(f"Error setting up test data: {e}")
                raise

    def test_neo4j_data_loaded(self):
        """Test if data was loaded correctly in Neo4j."""
        driver = None
        try:
            driver = GraphDatabase.driver(
                self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password)
            )
            with driver.session() as session:
                # Check nutricionistas
                result = session.run("MATCH (n:Nutricionista) RETURN count(n) AS count")
                record = result.single()
                self.assertIsNotNone(record, "Neo4j query returned no record")
                if record:
                    self.assertEqual(record["count"], 3, "Expected 3 nutricionistas")

                # Check pacientes
                result = session.run("MATCH (p:Paciente) RETURN count(p) AS count")
                record = result.single()
                self.assertIsNotNone(record, "Neo4j query returned no record")
                if record:
                    self.assertEqual(record["count"], 5, "Expected 5 pacientes")

                # Check alimentos
                result = session.run("MATCH (a:Alimento) RETURN count(a) AS count")
                record = result.single()
                self.assertIsNotNone(record, "Neo4j query returned no record")
                if record:
                    self.assertEqual(record["count"], 10, "Expected 10 alimentos")

                # Test a relationship
                result = session.run(
                    """
                    MATCH (n:Nutricionista)-[:ATENDE]->(p:Paciente)
                    RETURN count(p) AS count
                """
                )
                record = result.single()
                self.assertIsNotNone(record, "Neo4j query returned no record")
                if record:
                    self.assertTrue(
                        record["count"] > 0,
                        "Expected at least one ATENDE relationship",
                    )
        finally:
            if driver:
                driver.close()

    def test_mongodb_data_loaded(self):
        """Test if data was loaded correctly in MongoDB."""
        client = None
        try:
            client = MongoClient(self.mongo_uri)
            self.assertIsNotNone(client, "MongoDB client is None")
            if client:
                db = client[self.mongo_db]

                # Check collections
                self.assertEqual(
                    db.nutritionists.count_documents({}), 3, "Expected 3 nutritionists"
                )
                self.assertEqual(
                    db.patients.count_documents({}), 5, "Expected 5 patients"
                )
                self.assertEqual(db.foods.count_documents({}), 10, "Expected 10 foods")

                # Test more complex query
                result = db.dietPlans.aggregate(
                    [
                        {
                            "$lookup": {
                                "from": "patients",
                                "localField": "paciente_id",
                                "foreignField": "_id",
                                "as": "paciente",
                            }
                        },
                        {"$match": {"paciente.0": {"$exists": True}}},
                        {"$count": "planos_com_pacientes"},
                    ]
                )

                result_list = list(result)
                self.assertTrue(len(result_list) > 0, "Expected at least one result")
                self.assertTrue(
                    result_list[0]["planos_com_pacientes"] > 0,
                    "Expected at least one diet plan with patient",
                )
        finally:
            if client:
                client.close()


if __name__ == "__main__":
    unittest.main()
