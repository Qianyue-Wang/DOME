# -*- coding: utf-8 -*-

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
from http import HTTPStatus
import dashscope
from prompt import PROMPT_TEMPLATE
from openai import OpenAI
from promptwrittingw import PROMPT_TEMPLATE_WRITE
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
from logger import *
#导入依赖�?
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
from http import HTTPStatus
import dashscope
from prompt import PROMPT_TEMPLATE
from openai import OpenAI
from promptwritting import PROMPT_TEMPLATE_WRITE
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
import MEM as MindMap
from neo4j import GraphDatabase, basic_auth
import json
import re
from chatmodel import InfiniModel
from time import sleep
import DHO

path="path for the rough outline of a story(json type)"
#read the rough outline of a story

with open(path, 'r') as f:
        chapter_dict = json.load(f)
path_input="path for the story input(csv type)"
#read the story input
df=pd.read_csv(path_input)
settings=df['setting'].tolist()
characters=df['character'].tolist()
outlines=df['outline'].tolist()


count=1
for chapter_outline in chapter_dict:

    title=str(count)
    setting=settings[count]
    character=characters[count]
    outline=outlines[count]

    #初始化数据库
    uri = "your url"
    username = "your name"
    password = "your password"

    driver = GraphDatabase.driver(uri, auth=(username, password), encrypted=False)
    session = driver.session()
    
    
    session.run("MATCH (n) DETACH DELETE n")
    

    MindMap.set_initial([setting,character,outline],driver,title)
    #start to generate the story
    step=1
    near_info=""
    total_content=[]
    for chapter in chapter_outline:

        total_content,near_info=DHO.story_writting(chapter,total_content,step,near_info,driver,title)
        step+=1


    #store the story

    path="path for data"+"/"+title+"_total.txt"
    
    for i in range(len(total_content)):
        with open(path, 'a') as f:
            f.write(total_content[i])
            f.write("\n")
      
        

    
    



    



