import MindMap
import sys
import os
import json
from neo4j import GraphDatabase, basic_auth
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate,LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser


uri = "bolt://202.38.247.177:7687"
username = "neo4j"
password = "Wangqianyue1"
                    

driver = GraphDatabase.driver(uri, auth=(username, password), encrypted=False)
session = driver.session()

session.run("MATCH (n) DETACH DELETE n")

setting='The story is set in the present day, in a small town.\n'
   
character="""
    1.\n
    Full Name: Diane Chambers\n
    Character Portrait: Diane Chambers is a beautiful woman in her early thirties. She has long dark hair and blue eyes. She is married to Mark Chambers and is a stay-at-home mom.\n
    2.\n
    Full Name: Mark Chambers\n
    Character Portrait: Mark Chambers is a successful businessman in his early forties. He is tall and handsome, with brown hair and green eyes. He is married to Diane Chambers and is the father of two young children.\n
    3.\n
    Full Name: Karen Johnson\n
    Character Portrait: Karen Johnson is a beautiful blonde women in her early thirties. She is Mark Chambers' mistress and is also married with two young children.\n
    """
outline="""
    1. Diane Chambers discovers that her husband has been cheating on her with another woman.\n
    2. Diane Chambers decides to take revenge on her husband by having an affair of her own.\n
    3. Diane Chambers' affair is discovered by her husband, leading to a confrontation between the two.\n
    """
title="test"

stage_schema = ResponseSchema(name="chapter",
                                description="Was a string that describes the name of the chapter for a specific storyline.")
storyline_schema = ResponseSchema(name="plan",
                                        description="Was a string that describes the outline or the generation plan for a chapter of the specific episodic long story.")
response_schemas = [stage_schema,
                        storyline_schema]

output_parserp = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions_plan = output_parserp.get_format_instructions()
print(format_instructions_plan)


MindMap.set_initial([setting,character,outline],driver,title)