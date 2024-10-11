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
import numpy as np
import re
import string
from neo4j import GraphDatabase, basic_auth
import pandas as pd
from collections import deque
import itertools
from typing import Dict, List
import pickle
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize 
import openai
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.cider.cider import Cider
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.meteor.meteor import Meteor
from langchain.llms import OpenAI
import os
from PIL import Image, ImageDraw, ImageFont
import csv
from gensim import corpora
from gensim.models import TfidfModel
from gensim.similarities import SparseMatrixSimilarity
from rank_bm25 import BM25Okapi
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
import sys
from time import sleep
import os
from openai import OpenAI
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
from http import HTTPStatus
import dashscope
from transformers import AutoTokenizer, AutoModel
import torch
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
from langchain.prompts import ChatPromptTemplate
import prompt_KG as prompt
from prompt import PROMPT_TEMPLATE
import time
import operator
from time import sleep





def chatg(prompt):
    """
    chat with GPT-3.5
    """
    client = OpenAI(
        base_url='your url',
        api_key='your key',
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a Knowledge Graph expert and are good at extracting information from the Knowledge Graph. You are helping a user to extract information from the Knowledge Graph."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content


def chat(prompt):
    """
    chat with qwen-72b-chat
    """
    dashscope.api_key = "your key"
    messages = [
        {"role": "system",
             "content": "You are a Knowledge Graph expert and are good at extracting information from the Knowledge Graph. You are helping a user to extract information from the Knowledge Graph."},
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


def chate(prompt):
    """
    chat for evaluation
    """
    dashscope.api_key = "your key"
    messages = [
        {"role": "system",
             "content": "You are a well-formulated writer, who is logical and good at combining common sense thinking."},
        {'role': 'user', 'content': prompt}]
        
    completion= dashscope.Generation.call(
        'qwen-72b-chat',
        messages=messages,
        result_format='message',  # set the result is message format.
    )


    return completion.choices[0].message.content






def find_shortest_path(start_entity_name, end_entity_name,candidate_list,title,driver) -> List[str]:
              
                with driver.session() as session:
                   
                    result = session.run(
                       "MATCH (start_entity:Entity{name:$start_entity_name}), (end_entity:Entity{name:$end_entity_name}) "
                        "MATCH p = (start_entity)-[*..5]->(end_entity) "
                        "WITH p, length(p) AS len "
                        "ORDER BY len ASC "
                        "LIMIT 1 "
                        "RETURN p",
                        start_entity_name=start_entity_name,
                        end_entity_name=end_entity_name
                    )
                    paths = []
                    short_path = 0
                    if result.peek() is None:
                        exist_entity=[]
                        
                    else:
                        for record in result:
                            
                            path = record["p"]
                            entities = []
                            relations = []
                            
                            for i in range(len(path.nodes)):
                                node = path.nodes[i]
                                entity_name = node["name"]
                                entities.append(entity_name)
                                if i < len(path.relationships):
                                    relationship = path.relationships[i]
                                    relation_type = relationship.type
                                    relations.append(relation_type)
                        
                            path_str = ""
                            
                            for i in range(len(entities)):
                                entities[i] = entities[i].replace("_"," ")
                                
                                if entities[i] in candidate_list:
                                    short_path = 1
                                    exist_entity = entities[i]
                                path_str += entities[i]
                                if i < len(relations):
                                    relations[i] = relations[i].replace("_"," ")
                                    path_str += "->" + relations[i] + "->"
                            
                            if short_path == 1:
                                paths = [path_str]
                                break
                            else:
                                paths.append(path_str)
                                exist_entity = {}
                            
                        if len(paths) > 5:        
                            paths = sorted(paths, key=len)[:5]
                

                return paths,exist_entity

def combine_lists(*lists):

    combinations = list(itertools.product(*lists))
    results = []
    for combination in combinations:
        new_combination = []
        for sublist in combination:
            if isinstance(sublist, list):
                #list合并
                new_combination += sublist
            else:
                #sub作为list的
                new_combination.append(sublist)
        results.append(new_combination)
    return results


def get_entity_neighbors(entity_name: str,disease_flag,driver) -> List[List[str]]:
    disease = []
    
    query = """
    MATCH (e:Entity)-[r]->(n)
    WHERE e.name = $entity_name
    RETURN type(r) AS relationship_type,
           collect(n.name) AS neighbor_entities
    """
    session=driver.session()

    result = session.run(query, entity_name=entity_name)

    neighbor_list = []
    for record in result:
        rel_type = record["relationship_type"]
        neighbors = record["neighbor_entities"]
        #扩展邻居节点类型
        #有两种扩展方式，else,记录了延申关�?
        neighbor_list.append([entity_name.replace("_"," "), rel_type.replace("_"," "), 
                                ','.join([x.replace("_"," ") for x in neighbors])
                                ])
        
        

    
    return neighbor_list,disease




def prompt_path_finding(path_input):
    

    template=PROMPT_TEMPLATE['get_path']
    prompt=ChatPromptTemplate.from_template(template)
    p=prompt.format_messages(Path=path_input)
    response_of_KG_path = chate(p[0].content)
    return response_of_KG_path

def prompt_neighbor(neighbor):
    
    template=PROMPT_TEMPLATE['get_neighbor']

    
    prompt=ChatPromptTemplate.from_template(template)
    p=prompt.format_messages(neighbor=neighbor)

    response_of_KG_neighbor = chate(p[0].content)

    return response_of_KG_neighbor

def cosine_similarity_manual(x, y):
   
    dot_product = np.dot(x, y.T)
    norm_x = np.linalg.norm(x, axis=-1)
    norm_y = np.linalg.norm(y, axis=-1)
    sim = dot_product / (norm_x[:, np.newaxis] * norm_y)
    return sim



def prompt_document(question,instruction):
    template = """
    You are an excellent AI doctor, and you can diagnose diseases and recommend medications based on the symptoms in the conversation.\n\n
    Patient input:\n
    {question}
    \n\n
    You have some medical knowledge information in the following:
    {instruction}
    \n\n
    What disease does the patient have? What tests should patient take to confirm the diagnosis? What recommened medications can cure the disease?
    """

    prompt = PromptTemplate(
        template = template,
        input_variables = ["question","instruction"]
    )

    system_message_prompt = SystemMessagePromptTemplate(prompt = prompt)
    system_message_prompt.format(question = question,
                                 instruction = instruction)

    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt,human_message_prompt])
    chat_prompt_with_values = chat_prompt.format_prompt(question = question,\
                                                        instruction = instruction,\
                                                        text={})

    response_document_bm25 = chat(chat_prompt_with_values.to_messages()).content

    return response_document_bm25

def embeddings_entity(df):

    #df = pd.read_csv('/home/wyf/wqy/KGc.csv', names=['head', 'relation', 'tail'])
    model=SentenceTransformer(model_name_or_path='/mnt/cephfs/home/wangqianyue/beg')
    
    #enetity 存储为对应list
    entity_list=[]
    col1_list = df["head"].values.tolist()
    col2_list = df["tail"].values.tolist()
    for i in col1_list:
        entity_list.append(i)
    for i in col2_list:
        entity_list.append(i)
    #entity 对应的 entityembedding
        
    entity_embeddings=model.encode(entity_list, normalize_embeddings=True)
    
    return entity_list,entity_embeddings
def parse_string_to_tuple(s):

    
    
    
  
    s1=(s.split("."))
    if len(s1)==1:
        
        return "no"

    s = (((s.split("."))[1]).strip())[1:-1]
   
    
    # 分割字符串并去除空格

    triple = tuple(map(str.strip, s.split(",")))
    #去除triples中的每个元素中的_
    triple = tuple(map(lambda x: x.replace("_", " "), triple))
    
    tuple_length = len(triple)
    
    if tuple_length<3:
         
         return "no"
    else:
         if tuple_length==3: 
            return triple
         else:
              new_triple=triple[:2]+ tuple(triple[-1])
              if len(new_triple)==3:
                   return new_triple
              

def data_process(text):
    lines = text.strip().split('\n')
    # 按所需格式重排列表
    df = pd.DataFrame(columns=['head', 'relation', 'tail'])
    
    for li in lines:

       
        if li=='':
            continue
        tuple_data = parse_string_to_tuple(li)
        
        if tuple_data=="no":
             continue
        
        
        df.loc[len(df.index)]=tuple_data
    #删除df中有NAN的行
    df = df.dropna()
    
    return df

def get_inputkg(original_input,title):

    
    prompt_template=PROMPT_TEMPLATE['KGC']
    prompt=ChatPromptTemplate.from_template(prompt_template)
    messages = prompt.format_messages(text=original_input)
    res=chat(messages[0].content)
    kg=data_process(res)
    return kg



def get_input_kg_embedding(test,title):
    kg=get_inputkg(test,title)
    enlist,enembedding=embeddings_entity(kg)
    return enlist,enembedding

def storeneo4j(df,driver):
            session=driver.session()
            for index, row in df.iterrows():
                head_name = row['head']
                tail_name = row['tail']
                relation_name = row['relation']

                query = (
                    "MERGE (h:Entity { name: $head_name }) "
                    "MERGE (t:Entity { name: $tail_name }) "
                    "MERGE (h)-[r:`" + relation_name + "`]->(t)"
                )
                session.run(query, head_name=head_name, tail_name=tail_name, relation_name=relation_name)
            


def get_history_triples():
            path="your path to store quadruples(csv type)"
            df = pd.read_csv(path)
            df.columns=['head', 'relation', 'tail']
            return df

def get_history_entity_embeddings(title):
    path="your path to store(pkl type)"
    with open(path, 'rb') as f:  # 打开文件用于二进制读取
            history_dict = pickle.load(f)  # 从文件中读取字典
    hlist=history_dict['entity']
    hembedding=history_dict['embedding']
    
    return hlist,hembedding
    
    
                
       
def set_history_entity_embeddings(df,driver,title,time_step=1,init=True):
    """
    history update
    """
    
    enlist,enembedding=embeddings_entity(df)
    print(enlist)
    #list和embedding存在一个dict,将dict存成pkl
    enlist_time=[]
    for i in enlist:
         ni=(i,time_step)
        
         enlist_time.append(ni)

    
    enlist=enlist_time
    storeneo4j(df,driver)
    df['time']=time_step
    if init:
        #要存第一段信息(实体及嵌入表达信息)
        path="your path to store(pkl type)"
        hlist=enlist
        hembedding=enembedding
        history_dict={
            "entity":enlist,
            "embedding":enembedding
            }
        
        with open(path, 'wb') as f:  # 打开文件用于二进制写入
            pickle.dump(history_dict, f)  # 将字典序列化并写入到文件中
        pathdf="path to store quadruples(csv type) for each chapter"
       
        df.to_csv(pathdf, index=False)
        
             
    else:
        #存在历史信息
        #neo4j增加元素

        path="/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/data/"+title+".pkl"
        with open(path, 'rb') as f:  # 打开文件用于二进制读取
            history_dict = pickle.load(f)  # 从文件中读取字典
        hlist=history_dict['entity']
        hembedding=history_dict['embedding']
        
        hlist=hlist+enlist
        hembedding=np.concatenate((hembedding,enembedding), axis=0)
        history_dict['entity']=hlist
        history_dict['embedding']=hembedding
        
        with open(path, 'wb') as f:  # 打开文件用于二进制写入
            pickle.dump(history_dict, f)  # 将字典序列化并写入到文件中
        if time_step==1:
            pathdf="/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/data/"+title+"/"+str(time_step)+".csv"
            df0=pd.read_csv(pathdf)
            #两个df 合并
            df=pd.concat([df0,df],axis=0)
     
        pathdf="/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/data/"+title+"/"+str(time_step)+".csv"
       
        df.to_csv(pathdf, index=False)
      
    


def find_sim_entity(enembedding,enlist,input_enembeding,input_enlist):
    # enembedding=pd.DataFrame(enembedding)
    # print(enembedding.shape)
    match_kg=[]
    
    for kg_entity in input_enlist:
            
                #来自用户，前面划词，查找对应词的embedding
                keyword_index = input_enlist.index(kg_entity)
                kg_entity_emb = np.array(input_enembeding[keyword_index])
               
                cos_similarities = cosine_similarity_manual(enembedding,kg_entity_emb)[0]
                #基于阈值的查询
                for index, similarity in enumerate(cos_similarities):
                    if similarity >= 0.7:
                        match_kg_i = enlist[index][0].replace("_", " ")
                       
                        match_kg.append(match_kg_i)
                        
    match=[]
    for i in match_kg:
         if i not in match:
              match.append(i)
    
    
    print('match_kg',match)
    return match

def find_path(match_kg,driver,title):

    
    
    if len(match_kg) != 1 or 0:
                #带时间戳的
                start_entity = match_kg[0]
                candidate_entity = match_kg[1:]#相关节点
                
                result_path_list = []
                while 1:
                    flag = 0
                    paths_list = []
                    while candidate_entity != []:
                        end_entity = candidate_entity[0]
                        #依次移除
                        candidate_entity.remove(end_entity)   



                        paths,exist_entity = find_shortest_path(start_entity, end_entity,candidate_entity,title,driver)
                        
                        path_list = []
                        if paths == [''] or paths == []:
                            #没找到path
                            flag = 1
                            if candidate_entity == []:
                                flag = 0
                                break
                            #找下一个
                            start_entity = candidate_entity[0]
                            candidate_entity.remove(start_entity)
                            break
                        else:
                            #找到path
                            for p in paths:
                                #去掉-》，保留路径上的文字信息
                                path_list.append(p.split('->'))
                            if path_list != []:
                                paths_list.append(path_list)
                        
                        if exist_entity != {}:
                            try:
                                candidate_entity.remove(exist_entity)
                            except:
                                continue
                        
                        start_entity = end_entity
                        
                             
                    result_path = combine_lists(*paths_list)
                    
                
                
                    if result_path != []:
                        result_path_list.extend(result_path)                
                    if flag == 1:
                        continue
                    else:
                        break
                
                start_tmp = []
                for path_new in result_path_list:
                
                    if path_new == []:
                        continue
                    if path_new[0] not in start_tmp:
                        start_tmp.append(path_new[0])
                
                if len(start_tmp) == 0:
                        result_path = {}
                        single_path = {}
                else:
                    if len(start_tmp) == 1:
                        result_path = result_path_list[:5]
                    else:
                        result_path = []
                                                  
                        if len(start_tmp) >= 5:
                            for path_new in result_path_list:
                                if path_new == []:
                                    continue
                                if path_new[0] in start_tmp:
                                    result_path.append(path_new)
                                    start_tmp.remove(path_new[0])
                                if len(result_path) == 5:
                                    break
                        else:
                            count = 5 // len(start_tmp)
                            remind = 5 % len(start_tmp)
                            count_tmp = 0
                            for path_new in result_path_list:
                                if len(result_path) < 5:
                                    if path_new == []:
                                        continue
                                    if path_new[0] in start_tmp:
                                        if count_tmp < count:
                                            result_path.append(path_new)
                                            count_tmp += 1
                                        else:
                                            start_tmp.remove(path_new[0])
                                            count_tmp = 0
                                            if path_new[0] in start_tmp:
                                                result_path.append(path_new)
                                                count_tmp += 1

                                        if len(start_tmp) == 1:
                                            count = count + remind
                                else:
                                    break

                    try:
                        single_path = result_path_list[0]
                    except:
                        single_path = result_path_list
                    
    else:
                        result_path = {}
                        single_path = {}            
    print('result_path',result_path)
    return result_path

def find_neighbor(match_kg,driver):
            neighbor_list = []
            neighbor_list_disease = []
            #将match_kg中的每个元素都将下划线替换为空格
            


            
                 
            for match_entity in match_kg:
               
                match_entity = match_entity.replace("_", " ")
                disease_flag = 0
                neighbors,disease = get_entity_neighbors(match_entity,disease_flag,driver)
              
                

                # newnei=[(i,time) for i in neighbors]

                # neighbor_list.extend(newnei)
                neighbor_list.extend(neighbors)

                while disease != []:
                    new_disease = []
                    for disease_tmp in disease:
                        if disease_tmp in match_kg:
                            new_disease.append(disease_tmp)

                    if len(new_disease) != 0:
                        for disease_entity in new_disease:
                            disease_flag = 1
                            neighbors,disease = get_entity_neighbors(disease_entity,disease_flag)
                            neighbor_list.extend(neighbors)
                            
                            # newnei=[(i,time) for i in neighbors]

                            # neighbor_list.extend(newnei)


                    else:
                        for disease_entity in disease:
                            disease_flag = 1
                            neighbors,disease = get_entity_neighbors(disease_entity,disease_flag)
                          
                            neighbor_list.extend(neighbors)
                            # newnei=[(i,time) for i in neighbors]

                            # neighbor_list.extend(newnei)
                neighbor_list.extend(neighbor_list_disease)
            print('neighbor_list',neighbor_list)
            return neighbor_list

def get_prompt_path(result_path,match_kg):
    if len(match_kg) != 1 or 0:
                response_of_KG_list_path = []
                if result_path == {}:
                    response_of_KG_list_path = []
                else:
                    result_new_path = []
                    for total_path_i in result_path:
                        path_input = "->".join(total_path_i)
                        result_new_path.append(path_input)
                    
                    path = "\n".join(result_new_path)
                   
                    response_of_KG_list_path = prompt_path_finding(path)
                    
                    print("response_of_KG_list_path",response_of_KG_list_path)
                    return response_of_KG_list_path
    else:
                response_of_KG_list_path = '{}'


def get_prompt_neighbor(neighbor_list):
        
            neighbor_new_list = []
            for neighbor_i in neighbor_list:
                neighbor = "->".join(neighbor_i)
                neighbor_new_list.append(neighbor)
            neighbor_input = "\n".join(neighbor_new_list[:])
            response_of_KG_neighbor = prompt_neighbor(neighbor_input)
            print("response_of_KG_neighbor",response_of_KG_neighbor)
            return response_of_KG_neighbor

           
def neighbor_filter(neighbor_list):
    sorted_list = sorted(neighbor_list, key=lambda x: x[1])
    keep_list=sorted_list[:5]
    kee_list=[i[0] for i in keep_list]
    return kee_list


def evaluator(outline,triples,title):
    if len(triples)<16:
       
        senress=[]
        score_schema = ResponseSchema(name="score",
                                    description="the number that indicate the quality of the generated content.")
        explaination_schema = ResponseSchema(name="explanation",
                                            description="the string that describes the explaination of the score.")
        response_schemas = [score_schema,explaination_schema]
        output_parsers = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions_score = output_parsers.get_format_instructions()
    
        prompt_templatesen=PROMPT_TEMPLATE["graph2text"]
        promptsen=ChatPromptTemplate.from_template(prompt_templatesen)
        for i in triples:
            ps=promptsen.format_messages(triple=i)
            
            
            c=1
            ress=""
            while(1):
                try:
                    #sleep 1s
                    sleep(c)
                    sen= chate(ps[0].content)
                    #将sen按照:分割
                    #检测sen中是否含:
                    res=[]
                    if ':' in sen:
                        spattern=re.compile(":")

                        res=spattern.split(sen)
                        #去除res[1]开头的换行符
                        res[1]=res[1].lstrip()
                        ress=res[1]
                
                    
                    break
                except:
                    c+=1
                    continue
                
                 
        
            
            senress.append(ress)
        return senress,triples
    else:


        #转句子
        score_schema = ResponseSchema(name="score",
                                    description="An integer that indicate the quality of the generated content.")
        explaination_schema = ResponseSchema(name="explanation",
                                            description="The string that describes the explaination of the score.")
        response_schemas = [score_schema,explaination_schema]
        output_parsers = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions_score = output_parsers.get_format_instructions()
    
        prompt_templatesen=PROMPT_TEMPLATE["graph2text"]
        promptsen=ChatPromptTemplate.from_template(prompt_templatesen)

        #评估
        
        prompt_template=PROMPT_TEMPLATE["evaluate"]
        prompt=ChatPromptTemplate.from_template(prompt_template)
        scores=[]
        senress=[]
        for i in triples:
            ps=promptsen.format_messages(triple=i)
            c=1
            ress=""
            while(1):
                try:
                    sleep(c)
                    sen= chate(ps[0].content)
                    #将sen按照:分割
                    #检测sen中是否含:
                    res=[]
                    if ':' in sen:
                        spattern=re.compile(":")
                        res=spattern.split(sen)
                        res[1]=res[1].lstrip('\n')
                        ress=res[1]
                        break
                    else:
                        print("not good result:",sen)
                        continue
                except:
                    c+=1
                    continue
            print(ress)
                

            
            senress.append(ress)
            #p=prompt.format_messages(outline=outline,triplesentence=ress,format=format_instructions_score)
            print(outline)
            print(ress)
            p=prompt.format_messages(outline=outline,triplesentence=ress)
           
            score=0
            count=4
            
            while 1:
                
                try:

                    res = chate(p[0].content)
                    print("original score result,",res)
                    
                    match = re.search(r'Score: (\d+)', res)
                    print(match)

                    if match:
                            score = match.group(1)
                            print(score)
                            break
                    else:
                            continue
                except:
                    sleep(count%5)
                    count+=1
                    print(count)
                    continue
            print("evaluation result:",int(score))
            dic={"sentence":ress,"outline":outline,"score":int(score)}
            path="/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/data/"+title+"_result.csv"
            with open(path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(dic.values())
            
            
           
            scores.append(int(score))
            #打分结果排序
        ressen=[]
        new_triple=[]
        sorted_list_with_index = sorted(enumerate(scores), key=lambda x: x[1],reverse=True)

        for index, value in sorted_list_with_index[:9]:
                ressen.append(senress[index])
                new_triple.append(triples[index])
        print(ressen)
        print(new_triple)
        return ressen,new_triple



     
def group_by_s2(nei_timeinfo):
    #(en,r,-,-)
    grouped_tuples = {}
    for tpl in nei_timeinfo:
        key = tuple(tpl[:2])
        if key not in grouped_tuples:
            grouped_tuples[key] = []
        grouped_tuples[key].append(tpl)
    res=list(grouped_tuples.values())
    ress=[]
    keep_triple=[]
    for i in res:
        if len(i)==1:
             keep_triple.append(i[0])
        else:
             ress.append(i)
              
    
    return ress,keep_triple


def group_by_s1(nei_timeinfo):
    #(en,r,en,-)
    grouped_tuples = {}
    for tpl in nei_timeinfo:
        key = tuple(tpl[:3])  # 取前两个元素作为键
        if key not in grouped_tuples:
            grouped_tuples[key] = []
        grouped_tuples[key].append(tpl)
    res=list(grouped_tuples.values())
    ress=[]
    keep_triple=[]
    for i in res:
        if len(i)==1:
            keep_triple.append(i[0])
        else:
             ress.append(i)
              
    
    return ress,keep_triple




def group_by_s4(nei_timeinfo):
    #(-,r,en,-)
    grouped_tuples = {}
    for tpl in nei_timeinfo:
        key = tuple(tpl[1:3])  # 取前两个元素作为键
        if key not in grouped_tuples:
            grouped_tuples[key] = []
        grouped_tuples[key].append(tpl)
    res=list(grouped_tuples.values())
    ress=[]
    keep_triple=[]
    for i in res:
        if len(i)==1:
            keep_triple.append(i[0])
        else:
             ress.append(i)
              
    
    return ress,keep_triple


def group_by_s3(nei_timeinfo):
    #(en,-,en,-)
    grouped_tuples = {}
    for tpl in nei_timeinfo:
        key = tuple([tpl[0],tpl[2]])
        if key not in grouped_tuples:
            grouped_tuples[key] = []
        grouped_tuples[key].append(tpl)
    res=list(grouped_tuples.values())
    ress=[]
    keep_triple=[]
    for i in res:
        if len(i)==1:
            keep_triple.append(i[0])
        else:
             ress.append(i)
              
    
    return ress,keep_triple


def trans_s2(s1list):
    ress=""
    for sili in s1list:
        if len(sili)==1:
              continue
        else:
             s1=PROMPT_TEMPLATE['schema1']
             s1_template=ChatPromptTemplate.from_template(s1)
             s1_prompt=s1_template.format_messages(inlist=sili)
             res=chat(s1_prompt[0].content)
             ress+=(res+'\n')
    return ress


def trans_s1(s1list):
    ress=""
    for sili in s1list:
        if len(sili)==1:
              continue
        else:
             s1=PROMPT_TEMPLATE['schema2']
             s1_template=ChatPromptTemplate.from_template(s1)
             s1_prompt=s1_template.format_messages(inlist=sili)
             res=chat(s1_prompt[0].content)
             ress+=(res+'\n')
    return ress



def trans_s4(s1list):
    ress=""
    for sili in s1list:
        if len(sili)==1:
              continue
        else:
             s1=PROMPT_TEMPLATE['schema3']
             s1_template=ChatPromptTemplate.from_template(s1)
             s1_prompt=s1_template.format_messages(inlist=sili)
             res=chat(s1_prompt[0].content)
             ress+=(res+'\n')
    return ress

def trans_s3(s1list):

    ress=""
    for sili in s1list:
        if len(sili)==1:
              continue
        else:
             s1=PROMPT_TEMPLATE['schema4']
             s1_template=ChatPromptTemplate.from_template(s1)
             s1_prompt=s1_template.format_messages(inlist=sili)
             res=chat(s1_prompt[0].content)
             ress+=(res+'\n')
    return ress

def info_refine(nei_timeinfo):
    #挖掘保留下来的三元组间的潜在关系
    ress=""
    print("for s1:")
    res_s1,tri=group_by_s1(nei_timeinfo)
    if res_s1:
        #翻译成自然语言
        res1=trans_s1(res_s1)
        ress=ress+res1+'\n'
        print("get1:",ress)

    if tri:
        print("for s2:")
        res_s2,trii=group_by_s2(tri)
        
        if res_s2:
            res2=trans_s2(res_s2)
            ress=ress+res2+'\n'
            print("get2:",ress)
        if trii:
            print("for s3:")
            res_s3,triii=group_by_s3(trii)
            if res_s3:
                res3=trans_s3(res_s3)
                ress=ress+res3+'\n'
                print("get3:",ress)
            if triii:
                print("for s4:")
                res_s4,triiii=group_by_s4(triii)
                if res_s4:
                    res4=trans_s4(res_s4)
                    ress=ress+res4+'\n'
                    print("get4:",ress)
                    return ress 
                
            
    return ress 



def schema_confict(list,schema):
    s1=PROMPT_TEMPLATE[schema]
    
    #规定输出格式
    stage_schema = ResponseSchema(name="result",
                                description="Was a char chosen from 'Y' or 'N' that describes the judgment result.If the judgment result is 'Y', it means that the two schemas have conflicts. If the judgment result is 'N', it means that the two schemas do not have conflicts.")
    storyline_schema = ResponseSchema(name="explanation",
                                        description="Was a string that describes how do you judge the conflict or conflict-free between the two schemas.")
    response_schemas = [stage_schema,
                        storyline_schema]

    output_parserp = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions_plan = output_parserp.get_format_instructions()
    

    


    s1_template=ChatPromptTemplate.from_template(s1)
    num_Y=0
    for i in list:
            s1_prompt=s1_template.format_messages(inlist=i,format=format_instructions_plan)
            res=chate(s1_prompt[0].content)
            #检查res中是否有字符'N'或者'Y',且不包含/
            check_YN = re.search(r'N|Y', res)
            check_slash = re.search(r'/', res)
            while (check_YN is None) or (check_slash is not None):
                res=chate(s1_prompt[0].content)
                check_YN = re.search(r'N|Y', res)
                check_slash = re.search(r'/', res)

            index = res.find('Y')
            # 如果找到了字符'N'
            if index != -1:
                # 打印字符'N'的位置
                num_Y+=1
            else:
                # 如果没找到字符'N'
                continue
            #统计到num_Y中

            print(res)
    return num_Y

def confict_detection(df):
    
    
    # #将df 转为list
    newlist = [tuple(row.tolist()) for index, row in df.iterrows()]
    # #分组，模式实例化
   

    
    res_s1=group_by_s1(newlist)

    print(res_s1)

    res_s2=group_by_s2(newlist)
    print(res_s2)

    res_s3=group_by_s3(newlist)
    print(res_s3)

    res_s4=group_by_s4(newlist)
    print(res_s4)

    #进一步判断
    
    nums1=schema_confict(res_s1,'s1')
    nums2=schema_confict(res_s1,'s2')
    nums3=schema_confict(res_s1,'s3')
    nums4=schema_confict(res_s4,'s4')

    #统计结果
    total_conflict=nums1+nums2+nums3+nums4

    len_df=df.shape[0]

    num_N=len_df-total_conflict

    re=num_N/len_df
    print(num_N)
    print(len_df)
    return re



    
     
def find_relevant_info(text,step,title,driver):
    #实体抽取
    input_enlist,input_enembeding=get_input_kg_embedding(text,"")
    enlist,enembedding=get_history_entity_embeddings(title)#enlist=enlist_time(是tuple)  #元素为tuple
    #实体match
    match_kg=find_sim_entity(enembedding,enlist,input_enembeding,input_enlist)
    #匹配路径#匹配邻居
    path_prompt=""
    neighbor_prompt=""
    neighbor_list=[]
    result_path_list=[]
    path_prompt=""
    if (step<2):
                
                neighbor_list=find_neighbor(match_kg,driver)

    else:
                result_path_list=find_path(match_kg,driver,title)
                neighbor_list=find_neighbor(match_kg,driver)
                path_prompt=get_prompt_path(result_path_list,match_kg)
    

    
    #相关性过滤，转的句子和保留的三元组

    neighbors,new_neighbors=evaluator(text,neighbor_list,title)
    #基于时间信息的挖掘潜在关联挖掘
    nei_timeinfo=addtime(new_neighbors,title)
    
    deep_info=info_refine(nei_timeinfo)
  
    for nei in neighbors:
                neighbor_prompt+=(nei+'\n')
    if not(path_prompt):
                path_prompt=""
    if not(deep_info):
                deep_info=""
    history=path_prompt+'\n'+neighbor_prompt+'\n'+deep_info
    print(history)
    #信息整合，返回
    return history


def addtime(new_neighbors,title="test1"):
    path="/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/data/"+title+".pkl"
    with open(path, 'rb') as f:  
                history_dict = pickle.load(f)  
    enlist=history_dict['entity']
    
        
    res=[]
   
    for tri in new_neighbors:
            head=tri[0]
            tail=tri[2]
        
            tailpos= [index for value,index  in enlist if  (value in tail)]
            headpos=[index for value,index in enlist if  (value in tail)]
            
        
            for t in tailpos:
                for h in headpos:
                    if t==h:
                        re=tri[:3]
                        if t==0:
                            t=1
                        
                        
                        re.append(t)
                    
                        if re not in res:
                            res.append(re)
   
        
    return res




def set_history(text,driver,chapetr_title,step=1):
    

    
    text_kg=get_inputkg(text,"")
    #这里检查KG提取效果
    print(text_kg)
  
    set_history_entity_embeddings(text_kg,driver,chapetr_title,time_step=step,init=False)  



def set_initial(li,driver,title):
    #初始化一个dataframe,列名为head,relation,tail,time
    df = pd.DataFrame(columns=['head', 'relation', 'tail'])
    for i in li:
        text_kg=get_inputkg(i,"")
        #将text_kg加入到df中
        df=pd.concat([df, text_kg], ignore_index=True)
    print(df)
    #除去df中包含NAN的行
    df = df.dropna()
    print(df)

    set_history_entity_embeddings(df,driver,title,init=True)




    

            




