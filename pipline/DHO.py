# -*- coding: utf-8 -*-

# from dotenv import load_dotenv, find_dotenv
# _ = load_dotenv(find_dotenv()) # read local .env file
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
from logger import *

from http import HTTPStatus
import dashscope
from prompt import PROMPT_TEMPLATE
from openai import OpenAI
from promptwritting import PROMPT_TEMPLATE_WRITE
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
import MEM as MindMap
from neo4j import GraphDatabase, basic_auth
import json
import re
import datetime



def chatg(prompt):
    client = OpenAI(
        base_url='your url',
        api_key='your key',
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a fiction expert, good at writing captivating novels"},
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

# print(chatg("what is machine learning?"))
def data_process_outline(text):
    chapters = text.strip().split("\n\n")

    # 创建一个空字典来存储章节
    chapter_dict = {}

    # 遍历拆分后的章节
    for chapter in chapters:
        # 进一步拆分章节标题和内容
        parts = chapter.split("\n")
        chapter_number = parts[0].split(" ")[1].split(":")[0]  # 提取章节号
        chapter_title = parts[0].split(": ")[1]  # 提取章节标题
        chapter_content = "\n".join(parts[1:])  # 提取章节内容
        # 将章节号、标题和内容存储在字典中
        chapter_dict[chapter_number] = {
            "title": chapter_title,
            "content": chapter_content
        }
    return chapter_dict

def data_process_json(text):
    #将json string 转为元素是dic的list
    
    
    #q:text的开头和结尾是```json 和```，需要去掉，编写代码实现
    #a:使用strip()函数去掉
    text=text.strip("`")
    text=text.strip("json")
    text=text.strip(" ")
    print(text)
  
    list_object = json.loads(text) 
    return list_object

def re_detail_outline(text):
    # 正则表达式来提取相关信息
    pattern = "Outline of chapter \d+:\s*\n(.*?)(?=\s*$)"
    # 在文本中搜索匹配的部分
    match = re.search(pattern, text, re.DOTALL)
    if match:
        # 输出提取到的内容
        print(match.group(1))
    else:
        print("No matching text found.")

def re_story(text):
    # 正则表达式来提取相关信息
    pattern = "Story:\s*\n(.*?)(?=\s*$)"
    # 在文本中搜索匹配的部分
    match = re.search(pattern, text, re.DOTALL)
    if match:
        # 输出提取到的内容
        print(match.group(1))
    else:
        print("No matching text found.")

def re_chapter_outline(text):
    # 正则表达式编译，包括re.DOTALL以使得.可以匹配换行符
    pattern = re.compile(r"- Outline of chapter (\d+):\s*\n\s*(.+?)(?=\n- Outline of chapter |\Z)", re.DOTALL)

    # 使用findall方法查找所有匹配项
    matches = pattern.findall(text)

    # 打印结果
    # for match in matches:
    #     print(f"Chapter {match[0]} outline is:\n{match[1]}\n")
    print(matches[0])
    return matches[0][0],matches[0][1]


def story_writting(chapter,total_content,step,near_info,driver,title):
        
        near_info=last_chapter_story
        chapter_outline_prompt = 'chapter_outline'
        story_prompt = 'write_en'
        
        line_outline_prompt_t=PROMPT_TEMPLATE_WRITE[chapter_outline_prompt]
        content_prompt_t=PROMPT_TEMPLATE_WRITE[story_prompt]

        stage = chapter["stage"]
        volume_outline = chapter["storyline"]
        detail_outline = []
       
        history= MindMap.find_relevant_info(volume_outline,step,title,driver)
        
        po=(ChatPromptTemplate.from_template(line_outline_prompt_t)).format_messages(
                                                                                    volume_outline=volume_outline,
                                                                                   last_chapter=last_chapter_story,
                                                                                   history=history)
            
        c=0
        while(True):
                try:
                    outline = chat(po[0].content) # TODO
                   
                    outlines = re_chapter_outline(outline)
                   
                    if len(outlines[0])>=10 and (outlines[2])>=10 and (outlines[1])>=10:
                        break
                    import time
                    time.sleep(1)
                    
                except:
                    c+=1
                    if c>5:
                        
                        assert RuntimeError(" too many try!!!")


                    print("error")
                    import time
                    time.sleep(1)
                    continue
        for i in outlines:
            
            
            outline=i
            
            detail_outline.append(outline)
            
            
            
            cntent_prompt_tempate =ChatPromptTemplate.from_template(content_prompt_t)
            history= MindMap.find_relevant_info(volume_outline,step,title,driver)
            
            pw=cntent_prompt_tempate.format_messages(
                                                     volume_outline=volume_outline,
                                                     chapter_outline=outline,
                                                     last_chapter=last_chapter_story,
                                                     history=history)
            story_content=chat(pw[0].content) # TODO
            
            last_chapter_story = story_content
            
            MindMap.set_history(story_content,driver,title,step)
            
            total_content.append(story_content)
            path="your path of data"+"/"+title+"/"+str(step)+".txt"
            with open(path, 'w') as f:
                f.write(story_content)
            
        
        return total_content,last_chapter_story
           
      
        

