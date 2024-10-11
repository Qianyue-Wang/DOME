# -*- coding: utf-8 -*-
#����premise׫дstoryline������
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
from http import HTTPStatus
import dashscope
from prompt import PROMPT_TEMPLATE
from openai import OpenAI
from promptwritting import PROMPT_TEMPLATE_WRITE
from langchain.chat_models import ChatOpenAI

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

#����������
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
import MindMap
from neo4j import GraphDatabase, basic_auth
import json
from time import sleep
from logger import *
import json
import re
from chatmodel import InfiniModel
import pandas as pd
import os



def chatg(prompt):
    client = OpenAI(
        base_url='your url',
        api_key='your key',
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a novelist who specializes in writing science fiction that is logically rigorous and reasonably safe"},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content



def chat(prompt):
    dashscope.api_key = "your key"
    messages = [
        {"role": "system",
             "content": "You are a novelist who specializes in writing science fiction that is logically rigorous and reasonably safe"},
        {'role': 'user', 'content': prompt}]

    response = dashscope.Generation.call(
        'qwen-72b-chat',
        messages=messages,
        result_format='message',  # set the result is message format.
    )
    if response.status_code == HTTPStatus.OK:
        return response.output["choices"][0].message.content
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        import time
        time.sleep(1)

def data_process_json(text):
    
    text=text.strip("`")
    text=text.strip("json")
    text=text.strip(" ")
    print(text)
  
    list_object = json.loads(text) 
    return list_object



if __name__ == '__main__':

    stage_schema = ResponseSchema(name="stage",
                             description="Was the phase in the development of a story, named after the stage names provided in the novel theory.It is an json object containing all chapter numbers and chatpter summary that belong to it.")
    storyline_schema = ResponseSchema(name="storyline",
                                        description="Was a string that describes the storyline of the stage based on the story theory and other provided information.")

    response_schemas = [stage_schema,
                        storyline_schema]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    print(format_instructions)

    path="path for the story input(csv type)"
    df=pd.read_csv(path)
    #read the csv file by setting ,character,plot requirement
    #we follow the input setting of DOC and RE3,you can refer to https://github.com/yangkevin2/emnlp22-re3-story-generation to get input
    settings=df['setting'].tolist()
    characters=df['character'].tolist()
    plot_requirements=df['plot requirement'].tolist()
    theory="""
    1. Exposition: The story begins in a set setting, introducing the main characters and the setting of the story. The main character usually lives in an environment that they consider ordinary or normal, but that environment sets the basis for the development of the story.\n
    2. Rising Action: An event or conflict is introduced in the story that forces the main character out of their comfort zone and begins to face a series of challenges or conflicts. These events move the story forward, gradually increasing the tension and complexity of the story.\n
    3. Climax: This is the most tense and exciting moment in the story when the main characters face their main conflict or challenge. This is often a turning point in the story, where the actions of the main character will determine the final course of the story.\n
    4. Falling Action: After the climax, the story begins to transition to the ending. The main character begins to deal with the aftermath of the climax, conflicts are resolved, and the tension of the story gradually decreases.\n
    5. Denouement or Resolution: the conflict of the story is resolved and all outstanding questions are answered. The fate of the main character and other characters is clarified, and the story reaches a satisfying conclusion. This stage not only resolves the external conflicts of the story, but also shows the inner changes and growth of the main character.\n
   
"""
    format_instructions=format_instructions

    count=1
    for setting,character,outline in zip(settings,characters,plot_requirements):
        title=str(count)
        path = "your path of data"+"/"+title+"/"

        if not os.path.exists(path):
            print("yes")
            os.makedirs(path)
    
        from promptwritting import PROMPT_TEMPLATE_WRITE
        stryline_prompt_t=PROMPT_TEMPLATE_WRITE['storyline']
        stryline_prompt_tempate =ChatPromptTemplate.from_template(template=stryline_prompt_t)
        ps=stryline_prompt_tempate.format_messages(theory=theory,setting=setting,character=character,outline=outline,format=format_instructions)
        storyline= chat(ps[0].content)

    
        while(1):
            print(storyline)
            if '[' in storyline and ']' in storyline:
                print("storyline is correct")
                break
            else:
                print("try again")
                storyline= chat(ps[0].content)
                count+=1
                if count>5:
                    print("try too many times")
                    break
                
        with open(path+"storyline.txt", 'w') as file:
            
            file.write(storyline)

        #chage text to json object
        json_storyline=data_process_json(storyline)
        #保存json文件
        with open(path+"storyline.json", 'w') as file:
            json.dump(json_storyline, file)


    
       
