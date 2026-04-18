from neo4j import GraphDatabase
import os
from difflib import get_close_matches
import random
from dotenv import load_dotenv

load_dotenv()

# Try Streamlit secrets first, fallback to environment variable
try:
    import streamlit as st
    neo4j_uri = st.secrets.get("NEO4J_URI", os.getenv("NEO4J_URI"))
    neo4j_username = st.secrets.get("NEO4J_USERNAME", os.getenv("NEO4J_USERNAME"))
    neo4j_password = st.secrets.get("NEO4J_PASSWORD", os.getenv("NEO4J_PASSWORD"))
except:
    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_username = os.getenv("NEO4J_USERNAME")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    neo4j_uri,
    auth=(neo4j_username, neo4j_password)
)


def get_fund_details(fund_name):
    query = """
    MATCH (f:Fund)
    WHERE toLower(f.name) CONTAINS toLower($name)
    OPTIONAL MATCH (f)-[:BELONGS_TO]->(c:Category)
    OPTIONAL MATCH (f)-[:HAS_RISK]->(r:Risk)
    OPTIONAL MATCH (f)-[:MANAGED_BY]->(a:AMC)
    RETURN f.name as name, f.nav as nav, 
           c.name as category, r.level as risk, a.name as amc
    LIMIT 1
    """

    with driver.session() as session:
        result = session.run(query, name=fund_name).data()

    return result[0] if result else None


def get_nav_history(fund_name):
    query = """
    MATCH (f:Fund)
    WHERE toLower(f.name) CONTAINS toLower($name)
    RETURN f.nav as nav, f.nav_history as nav_history
    LIMIT 1
    """

    with driver.session() as session:
        result = session.run(query, name=fund_name).data()

    if not result:
        return None

    nav = result[0].get("nav", 100)
    history = result[0].get("nav_history")

    # fallback if missing
    if not history:
        history = []
        base = float(nav)

        for _ in range(10):
            base += random.uniform(-2, 2)
            history.append(round(base, 2))

    return history


def get_all_fund_names():
    query = "MATCH (f:Fund) RETURN f.name as name"

    with driver.session() as session:
        result = session.run(query).data()

    return [r["name"] for r in result]


def find_closest_funds(user_input):
    funds = get_all_fund_names()
    return get_close_matches(user_input, funds, n=3, cutoff=0.4)