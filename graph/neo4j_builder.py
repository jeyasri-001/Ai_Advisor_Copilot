from neo4j import GraphDatabase
import os
import json
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
)

def insert_data():
    with open("data/sample_funds.json") as f:
        funds = json.load(f)

    with driver.session() as session:
        for fund in funds:
            session.run("""
                MERGE (f:Fund {name: $name})
                SET f.nav = $nav

                MERGE (c:Category {name: $category})
                MERGE (a:AMC {name: $amc})
                MERGE (r:Risk {level: $risk})

                MERGE (f)-[:BELONGS_TO]->(c)
                MERGE (f)-[:MANAGED_BY]->(a)
                MERGE (f)-[:HAS_RISK]->(r)
            """,
            name=fund["fund_name"],
            category=fund["category"],
            amc=fund["amc"],
            risk=fund["risk"],
            nav=fund["nav"]
            )

    print("✅ Inserted into Neo4j")


if __name__ == "__main__":
    insert_data()