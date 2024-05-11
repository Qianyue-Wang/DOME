# -*- coding: utf-8 -*-
import MindMap
from neo4j import GraphDatabase, basic_auth
import pandas as pd
import operator
import pickle
from prompt import PROMPT_TEMPLATE
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
from http import HTTPStatus
import dashscope
import json



def chat(prompt):
    dashscope.api_key = "sk-f83c448bb0dc4eb787ca98d57dbce394"
    messages = [
        {"role": "system",
             "content": "You are a novelist who specializes in writing science fiction that is logically rigorous and reasonably good"},
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

# uri = "bolt://202.38.247.177:7687"
# username = "neo4j"
# password = "Wangqianyue1"
                    

# driver = GraphDatabase.driver(uri, auth=(username, password), encrypted=False)
# session = driver.session()
# # text="Diane Chambers, a beautiful woman in her early thirties, discovers that her husband, Mark Chambers, has been cheating on her with Karen Johnson, a blonde woman in her early thirties who is also married and has two young children."
# # step=1
# # title="test1"

# # history=MindMap.find_relevant_info(text,step,title,driver)
# # print(history)




# title="test1"
# timestep=1
# text="""
# Diane Chambers, a beautiful woman in her early thirties, discovers that her husband, Mark Chambers, has been cheating on her with Karen Johnson, a blonde woman in her early thirties who is also married and has two young children.
# """
# # input_enlist,input_enembeding=MindMap.get_input_kg_embedding(text,title)
# # enlist,enembedding=MindMap.get_history_entity_embeddings(title)
# # match_kg=MindMap.find_sim_entity(enembedding,enlist,input_enembeding,input_enlist)
# # neighbor_list=MindMap.find_neighbor(match_kg,driver)
# # print(len(neighbor_list))
# temp= [['Diane Chambers', 'has', 'affair,blue eyes,long dark hair'], ['Diane Chambers', 'decides to take revenge', 'husband'], ['Diane Chambers', 'cheats on', 'husband'], ['Diane Chambers', 'discovers', 'husband'], ['Diane Chambers', 'is', 'stay-at-home mom,beautiful woman'], ['Diane Chambers', 'married to', 'Mark Chambers'], ['Mark Chambers', 'is', 'father,businessman'], ['Mark Chambers', 'married to', 'Diane Chambers'], ['Mark Chambers', 'has', 'green eyes,brown hair'], ["discovery of Diane Chambers' affair", 'leads to', 'confrontation'], ['Karen Johnson', 'is', 'mistress,beautiful blonde woman'], ['Karen Johnson', 'married to', 'Mark Chambers'], ['her husband', 'discovers', "Diane Chambers' affair"]]
# senress,triples=MindMap.evaluator(text,temp)
# nei_timeinfo=MindMap.addtime(temp)

# deep_info=MindMap.info_refine(nei_timeinfo)
# neighbor_prompt=""
# for nei in senress:
#                 neighbor_prompt+=(nei+'\n')

# path_prompt=""
# his=path_prompt+'\n'+neighbor_prompt+deep_info
# print(his)

# def data_process_json(text):

#     #将json string 转为元素是dic的list
    
    
#     #q:text的开头和结尾是```json 和```，需要去掉，编写代码实现
#     #a:使用strip()函数去掉
#     text=text.strip("`")
#     text=text.strip("json")
#     text=text.strip(" ")
#     print(text)
  
#     list_object = json.loads(text) 
#     return list_object

# path="/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/data/doc_outputs/annotations/detailed_relevance/doc_docnocontrol_detailedrelevance.csv"
# #读取内容
# df = pd.read_csv(path)
# #找出df中id列中，包含doc/3_的行
# df = df[df['id'].str.contains('doc/3_')]
# print(df)
# #将df中的内容按照id最后的数字进行排序
# df['id'] = df['id'].str.split('_').str[-1].astype(int)
# df= df.sort_values('id')
# print(df['id'])
# event=df['event'].tolist()[4]#对应outline
# print(event)
# passage=df['passage'].tolist()[4]
# print(passage)
# result=df['Does the given event occur in its entirety within the passage?'].tolist()
# print(result)
# print(['yes', 'yes', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'yes', 'yes', 'yes', 'yes'])
# ress=[]
# for e,p in zip(event,passage):
    
#     #分别抽取KG
#     e_kg=MindMap.get_inputkg(e,'event')
#     p_kg=MindMap.get_inputkg(p,'passage')
    
#     result_schema = ResponseSchema(name="result",
#                              description="Choose between 'yes' and 'no' to indicate whether the event occurs in its entirety within the passage.")
#     explain_schema = ResponseSchema(name="explain",
#                                         description="Was a string that describes the reason for the result.")

#     response_schemas = [result_schema,
#                         explain_schema]

#     output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
#     format_instructions = output_parser.get_format_instructions()
   
#     relevance_prompt_t=PROMPT_TEMPLATE['relevance']
#     relevance_prompt_tempate =ChatPromptTemplate.from_template(template=relevance_prompt_t)
#     ps=relevance_prompt_tempate.format_messages(event=e,passage=p,format=format_instructions)
#     res= chat(ps[0].content)
#     print(res)
#     result=data_process_json(res)['result']
#     ress.append(result)
# print(ress)



import re

def data_process_json(text):

    

    
    json_pattern = r"\{.*?\}"
    matches = re.findall(json_pattern, text, re.DOTALL)

    # 假设我们只有一个JSON对象，我们取第一个匹配项
    json_str = matches[0] if matches else None
    print(json_str)

    # 将提取的JSON字符串解析为Python字典
    if json_str:
        #json_data = json.loads(json_str)
        return json_str
    else:
        text

