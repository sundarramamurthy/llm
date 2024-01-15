#Install required libraries
# !pip install pymysql
# !pip install streamlit
# !pip install langchain

#Import libraries
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.llms.openai import OpenAI
# from langchain_openai import OpenAI
from langchain.sql_database import SQLDatabase
import os
import streamlit as st

# Setting up the MY SQL Database Connection
db_conn = SQLDatabase.from_uri("mysql+pymysql://root:root@127.0.0.1/classicmodels")

# Open AI Language Model Configuration
model = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

# Creating SQL Database Toolkit
toolkit = SQLDatabaseToolkit(db=db_conn, llm=model)

# Creating and Running a SQL Agent
agent_executor = create_sql_agent(
    llm=model,
    toolkit=toolkit,
    verbose=False,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
query = [
    "1. Find customers who have made purchases in the may 2003.",
    "2. List the product categories along with the average prices.",
    "3. Calculate the total sales revenue for each product.",
    "4. Retrieve the names of customers who placed orders on weekends.",
    "5. Calculate the average order value for top customer."
]

results = [
    (i, question, agent_executor(question).get("output"))
    if not exception
    else (i, question, f"Error: {exception}")
    for i, (question, exception) in enumerate(
        zip(query, [None] * len(query))
    )
]

for result in results:
    print(f"Question {result[0]+1} : {result[1]}")
    print("Answer : ", result[2])
    print("\n")








