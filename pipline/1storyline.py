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



def chatg(prompt):
    client = OpenAI(
        base_url='https://api.openai-proxy.org/v1',
        api_key='sk-82YkLGDNtuV8tE0ZHiFdIrOGnDd92P2yNU0djxk0XPgH9kon',
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

def chatw(prompt):
    count=3
    api=["Bearer sk-c7d2ij232nriaatu","Bearer sk-c7d2if4l6lmg36p6","Bearer sk-c7d2ipuiwlr6tkkl","Bearer sk-c7dpymyf5hoips7y"]

    while(1):
        sleep(3)
        try:
            model = InfiniModel(api_key=api[(count%4)], model='qwen-72b-chat')
            answer = model.call(prompt)
            if len(answer) < 5:
                logger.info(f"Exception chat answer too short:{e}")
                continue
            break
        except Exception as e:
            count+=1
            logger.info(f"Exception when chat to model:{e}")
            continue
    return answer
    

def chat(prompt):
    dashscope.api_key = "sk-0a8460aa09e5499bac02ce91f8028fce"
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


#######################改

    
    theory="""
    1. Exposition: The story begins in a set setting, introducing the main characters and the setting of the story. The main character usually lives in an environment that they consider ordinary or normal, but that environment sets the basis for the development of the story.\n
    2. Rising Action: An event or conflict is introduced in the story that forces the main character out of their comfort zone and begins to face a series of challenges or conflicts. These events move the story forward, gradually increasing the tension and complexity of the story.\n
    3. Climax: This is the most tense and exciting moment in the story when the main characters face their main conflict or challenge. This is often a turning point in the story, where the actions of the main character will determine the final course of the story.\n
    4. Falling Action: After the climax, the story begins to transition to the ending. The main character begins to deal with the aftermath of the climax, conflicts are resolved, and the tension of the story gradually decreases.\n
    5. Denouement or Resolution: the conflict of the story is resolved and all outstanding questions are answered. The fate of the main character and other characters is clarified, and the story reaches a satisfying conclusion. This stage not only resolves the external conflicts of the story, but also shows the inner changes and growth of the main character.\n
    """
    setting='The story is set in a dank and musty basement, with only a small window high up on one wall providing any natural light.\n'

    character="""
    Male Celebrity A: Male Celebrity A is a Hollywood actor in his forties.\n
John Doe: John Doe is a middle-aged man with a lean and athletic build.\n
Valerie Marx: Valerie Marx is a young woman in her early twenties.\n
    """
    outline="""
    1. Valerie Marx wakes up in a dark basement, bound and gagged.\n
   2. John Doe, the serial killer, tells Valerie that she must escape the basement before dawn or else she will become his next trophy.\n
3. Valerie uses her wits to escape the basement and evade John Doe.\n
   4. Valerie makes it to safety and the police catch John Doe.\n"""


##########################
    title="0503"
    
    
    import os

    path = "/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/data/"+title+"/"

    if not os.path.exists(path):
        print("yes")
        os.makedirs(path)
    
    from promptwritting import PROMPT_TEMPLATE_WRITE
    stryline_prompt_t=PROMPT_TEMPLATE_WRITE['storyline']
    stryline_prompt_tempate =ChatPromptTemplate.from_template(template=stryline_prompt_t)
    ps=stryline_prompt_tempate.format_messages(theory=theory,setting=setting,character=character,outline=outline,format=format_instructions)
    storyline= chat(ps[0].content)

    count=1
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
            
    with open("/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/data/"+title+"/"+'test5.txt', 'w') as file:
        
        file.write(storyline)
    
       
