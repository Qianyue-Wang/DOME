# -*- coding: utf-8 -*-

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
import MindMap
from neo4j import GraphDatabase, basic_auth
import json
import re
from chatmodel import InfiniModel

# 定义chat函数用于写作流水�?
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


def chatq(prompt):
    dashscope.api_key = "sk-3c4fce7a55f84e6db4ec0f0da4188b05"
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

def chat(prompt):
    while(1):
        try:

            model = InfiniModel(api_key='Bearer sk-c7dpymyf5hoips7y', model='qwen-72b-chat')
            answer = model.call(prompt)
            break
        except:
            continue
    return answer
    

# print(chatg("what is machine learning?"))
def data_process_outline(text):
    chapters = text.strip().split("\n\n")

    # 创建一个空字典来存储章�?
    chapter_dict = {}

    # 遍历拆分后的章节
    for chapter in chapters:
        # 进一步拆分章节标题和内容
        parts = chapter.split("\n")
        chapter_number = parts[0].split(" ")[1].split(":")[0]  # 提取章节�?
        chapter_title = parts[0].split(": ")[1]  # 提取章节标题
        chapter_content = "\n".join(parts[1:])  # 提取章节内容
        # 将章节号、标题和内容存储在字典中
        chapter_dict[chapter_number] = {
            "title": chapter_title,
            "content": chapter_content
        }
    return chapter_dict

def data_process_json(text):

    
    text=text.strip("`")
    text=text.strip(" ")
    text=text.strip("json")
    print(text)
    #list_object = json.loads(text) 
    return list_object
    


def format_constuction():
    plot_schema = ResponseSchema(name="plot",
                             description="Was a string that describes the stage of the story based on the story theory and other provided information.")
    key_schema = ResponseSchema(name="key_events",
                                        description="Was a string that describes the key events of the story based on the story theory and other provided information.")

    response_schemas = [plot_schema,
                        key_schema]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    fine_outline_instructions = output_parser.get_format_instructions()
    
    
    print(fine_outline_instructions)


    return fine_outline_instructions




if __name__ == '__main__':
    
    import os
    log_path = os.path.join("0417en_log.txt")
    file_handler = logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    setting='The story is set in the present day, in a small town.\n'
    theory="""
    1. Exposition: The story begins in a set setting, introducing the main characters and the setting of the story. The main character usually lives in an environment that they consider ordinary or normal, but that environment sets the basis for the development of the story.\n
    2. Rising Action: An event or conflict is introduced in the story that forces the main character out of their comfort zone and begins to face a series of challenges or conflicts. These events move the story forward, gradually increasing the tension and complexity of the story.\n
    3. Climax: This is the most tense and exciting moment in the story when the main characters face their main conflict or challenge. This is often a turning point in the story, where the actions of the main character will determine the final course of the story.\n
    4. Falling Action: After the climax, the story begins to transition to the ending. The main character begins to deal with the aftermath of the climax, conflicts are resolved, and the tension of the story gradually decreases.\n
    5. Denouement or Resolution: the conflict of the story is resolved and all outstanding questions are answered. The fate of the main character and other characters is clarified, and the story reaches a satisfying conclusion. This stage not only resolves the external conflicts of the story, but also shows the inner changes and growth of the main character.\n
    """
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
    title="0417"
    import os


    path = "/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/lzp_test/"+title+"/"
    pathdata="/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/data/"+title+"/"
    path_outline="/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/data/"+title+"/outline.txt"
    

    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(pathdata):
        os.makedirs(pathdata)

    uri = "bolt://202.38.247.177:7687"
    username = "neo4j"
    password = "Wangqianyue1"
                    
    driver = GraphDatabase.driver(uri, auth=(username, password), encrypted=False)
    session = driver.session()
    
    # #断点继续
    session.run("MATCH (n) DETACH DELETE n")
    MindMap.set_initial([setting,character,outline],driver,title)

    import json

    file_name = r"/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/pipline/0417rouge_storyline.json"
    with open(file_name, 'r') as f:
        data = json.load(f)

    chapter_dict=data
    from promptwritting import PROMPT_TEMPLATE_WRITE

    line_outline_prompt_t=PROMPT_TEMPLATE_WRITE['detail_storyline']
    content_prompt_t=PROMPT_TEMPLATE_WRITE['write']
    total_content=[]
    
    import datetime
    # 获取当前的时分秒
    current_time = datetime.datetime.now()
    time_str = current_time.strftime("%H_%M_%S")  # 格式化为时分�?
    # 创建文件�?
    file_name = f"{time_str}"  # 例如：file_152301.txt
    path_story = os.path.join("/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/lzp_test/test.txt")
    path_detail_outline = os.path.join("/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/lzp_test/story_detail_outline.txt")

    f_story = open(path_story,"a")
    f_detail_outline = open(path_detail_outline,"a")
    step=1
    chapter_index=1
    fine_outline_instructions=format_constuction()
    for chapter in chapter_dict:
        #step2 根据故事线实现动态纲�?(规划故事线实�?)
        # 一个粗纲要固定生成三个细纲�?
        stage = chapter["stage"]
        rouge_outline = chapter["storyline"]
        
        detail_outline = []
        for i in range(3):
            logger.info(f"Generating rouge outline {stage}, detail outline {step}:")
            logger.info(f"Chapter {stage}:")
            logger.info(f"Title: {rouge_outline}")
            logger.info(f"Content: {rouge_outline}\n")
            line_outline_prompt_tempate =ChatPromptTemplate.from_template(line_outline_prompt_t)
            history= MindMap.find_relevant_info(rouge_outline,step,title,driver)
            print("history1:",history)
            po=line_outline_prompt_tempate.format_messages(rough_outline=rouge_outline,history=history,num=i,detail_outline=detail_outline,format=fine_outline_instructions)
            count=1
            outline=""
            while(1):
                try:
                    outline= chat(po[0].content) 
                    print(outline)
                    
                    #res=data_process_json(outline) 
                    break
                except:
                    print(count)
                    count+=1
                    continue   
            
            # plot=res['plot']
            # key_event=res['key_events']
            logger.info("="*20)
            logger.info(f"outline:{outline}")
            detail_outline.append(outline)
            
            f_detail_outline.write("="*20)
            f_detail_outline.write("\n\n")
            f_detail_outline.write(outline)
            f_detail_outline.write("="*20)
            f_detail_outline.write("\n\n")
            
            logger.info("="*20)
            
            cntent_prompt_tempate =ChatPromptTemplate.from_template(content_prompt_t)
            
            history= MindMap.find_relevant_info(outline,step,title,driver)
            print("history2:",history)
            #pw=cntent_prompt_tempate.format_messages(plot=plot,key_event=key_event,history=history)
            pw=cntent_prompt_tempate.format_messages(outline=outline,history=history)
            story_content=chat(pw[0].content) #不需要改
            print()
            print("story_content:",story_content)
            print()
            MindMap.set_history(story_content,driver,title,step)
            logger.info("*"*20)
            logger.info(f"content:{story_content}")
            logger.info("*"*20)
            
            
            
            f_story.write("*"*20)
            f_story.write("\n")
            f_story.write(f"Chapter {step}:")
            f_story.write("\n\n")
            f_story.write(story_content)
            f_story.write("*"*20)
            f_story.write("\n\n")
            
            step+=1
            logger.info(step)
        chapter_index+=1
        # print(chapter_index)
    f_story.close()
    f_detail_outline.close()