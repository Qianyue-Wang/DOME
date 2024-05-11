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
import MindMap
from neo4j import GraphDatabase, basic_auth
import json
import re
import datetime

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
             "content": "You are a fiction expert, good at writing captivating novels"},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content


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
    # 在文本中搜索匹配的部�?
    match = re.search(pattern, text, re.DOTALL)
    if match:
        # 输出提取到的内容
        print(match.group(1))
    else:
        print("No matching text found.")

def re_story(text):
    # 正则表达式来提取相关信息
    pattern = "Story:\s*\n(.*?)(?=\s*$)"
    # 在文本中搜索匹配的部�?
    match = re.search(pattern, text, re.DOTALL)
    if match:
        # 输出提取到的内容
        print(match.group(1))
    else:
        print("No matching text found.")

def re_chapter_outline(text):
    spattern=re.compile(":")
    res=spattern.split(text)
    
   
    outlines=[res[1],res[2]]
    print(outlines)

    outliness=[]
    outline=""
    for i in outlines:
        outline=""
        sp=re.compile("\n")
        res=sp.split(i)
        ress=[]
        count=0
        
        for i in res:
            print(i)
            #如果长度过短，不保留
            #如果遇到Chapter Outline，不保留
            
            if len(i)<5:
                continue
            if "Chapter Outline" in i:
                continue
            #去除字符串中开头结尾的空格
            temp=i.strip()
            
            
            if count==0:
                count+=1
                continue
            if count==1:
                outline+=("The outline of chapter: "+temp)
                count+=1
            else:
                outline+=(temp)
                count+=1
            
            print(outline)
        outliness.append(outline)
        print(outliness)

    return outliness[0],outliness[1]


if __name__ == '__main__':
    print("begin")
    
    # 获取当前的时分秒
    current_time = datetime.datetime.now()
    time_str_hms = current_time.strftime("%H_%M_%S")  # 格式化为时分�?
    time_str_md = current_time.strftime("%m%d")  # 格式化为时分�?
    title = time_str_md
    
    # 设置日志路径
    import os
    os.makedirs(os.path.join("/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/lzp_test/","log",title),exist_ok=True)
    log_path = os.path.join("/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/lzp_test/","log",title,f"{time_str_hms}_log.txt")
    file_handler = logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    path = "/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/data/"+title+"/"

    if not os.path.exists(path):
        print("yes")
        os.makedirs(path)
    
    # 设置结果文件文件�?
    path = os.path.join("/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/lzp_test/",title)
    os.makedirs(path,exist_ok=True)

    # 设置图数据库
    uri = "bolt://202.38.247.225:7687"
    username = "neo4j"
    password = "Wangqianyue1"
                    
    driver = GraphDatabase.driver(uri, auth=(username, password), encrypted=False)
    session = driver.session()

    theory="""
    1. Exposition: The story begins in a set setting, introducing the main characters and the setting of the story. The main character usually lives in an environment that they consider ordinary or normal, but that environment sets the basis for the development of the story.\n
    2. Rising Action: An event or conflict is introduced in the story that forces the main character out of their comfort zone and begins to face a series of challenges or conflicts. These events move the story forward, gradually increasing the tension and complexity of the story.\n
    3. Climax: This is the most tense and exciting moment in the story when the main characters face their main conflict or challenge. This is often a turning point in the story, where the actions of the main character will determine the final course of the story.\n
    4. Falling Action: After the climax, the story begins to transition to the ending. The main character begins to deal with the aftermath of the climax, conflicts are resolved, and the tension of the story gradually decreases.\n
    5. Denouement or Resolution: the conflict of the story is resolved and all outstanding questions are answered. The fate of the main character and other characters is clarified, and the story reaches a satisfying conclusion. This stage not only resolves the external conflicts of the story, but also shows the inner changes and growth of the main character.\n
    """
    #####
    setting='The story is set in the inner city of a large metropolitan area.\n'

    character="""
    Gary Saunders: Gary Saunders is a teenage boy who lives in the inner city.\n
    Shannon Doyle: Shannon Doyle is a young woman in her early twenties.\n
    Mike Doyle: Mike Doyle is Shannon's father and a successful journalist.\n
    Lena Saunders: Lena Saunders is Gary's mother and a local business owner.\n
    """
    outline="""
    1. Shannon's father, Mike, dies unexpectedly, leaving her determined to follow in his footsteps and become a successful journalist.\n
    2. Shannon lands her first major assignment, a feature on the inner city, but quickly discovers that the ugly reality of life in the city is far different from the dream she imagined.\n
    3. With the help of her new friend, Gary, Shannon comes to understand the harsh realities of life in the inner city and learns that sometimes the truth is much more than just a story.\n
    """

    #####
    # session.run("MATCH (n) DETACH DELETE n")
    # MindMap.set_initial([setting,character,outline],driver,title)
    
    

    import json
    # 从文件读取字�?
    file_name = r"/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/lzp_test/1volume_outline.json"
    with open(file_name, 'r') as f:
        data = json.load(f)

    chapter_dict=data
    from promptwrittinglzplzpshort2 import PROMPT_TEMPLATE_WRITE
    

    chapter_outline_prompt = 'chapter_outline'
    story_prompt = 'write_en'
    logger.info("!"*50)
    logger.info("pain very attention to the setting!")
    #logger.info(f"using [{detail_outline_prompt}] in PROMPT_TEMPLATE_WRITE to generate detail outline")
    #logger.info(f"using [{story_prompt}] in PROMPT_TEMPLATE_WRITE to generate story")
    logger.info("!"*50)
    
    line_outline_prompt_t=PROMPT_TEMPLATE_WRITE[chapter_outline_prompt]
    content_prompt_t=PROMPT_TEMPLATE_WRITE[story_prompt]
    total_content=[]

    
    # 创建文件�?
    file_name = f"{time_str_hms}"  # 例如：file_152301.txt
    path_story = os.path.join("/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/lzp_test/",title,f"{file_name}_story.txt")
    path_detail_outline = os.path.join("/mnt/cephfs/home/wangqianyue/LTG/MindMap-main/lzp_test/",title,f"{file_name}__detail_outline.txt")

    f_story = open(path_story,"a")
    f_detail_outline = open(path_detail_outline,"a")
    step=1
    chapter_index=1
    last_chapter_story = ""
    for chapter in chapter_dict[:]:
        #step2 根据故事线实现动态纲�?(规划故事线实�?)
        # 一个粗纲要固定生成num个细纲要
        stage = chapter["stage"]
        volume_outline = chapter["storyline"]
        detail_outline = []
        # line_outline_prompt_tempate = ChatPromptTemplate.from_template(line_outline_prompt_t)
        # po=line_outline_prompt_tempate.format_messages(rough_outline=volume_outline,history=history,num=i,detail_outline=detail_outline)
        history= MindMap.find_relevant_info(volume_outline,step,title,driver)
    
        po=(ChatPromptTemplate.from_template(line_outline_prompt_t)).format_messages(
                                                                                   volume_outline=volume_outline,
                                                                                   last_chapter=last_chapter_story,
                                                                                   history=history)


                                                                        
            
        c=0
        
        

        while(True):
                try:
                    outline = chat(po[0].content) # TODO
                    
                    
                    chapter1,chapter2 = re_chapter_outline(outline)
                    logger.info(f"after re: {chapter1}\n\n{chapter2}")
                    
                    if chapter1 and chapter2:
                        break
                    import time
                    time.sleep(1)
                    
                except:
                    c+=1
                    if c>5:
                        logger.info("!!"*20)
                        logger.info("too many try!!!")
                        logger.info("!!"*20)
                        assert RuntimeError(" too many try!!!")


                    print("error")
                    import time
                    time.sleep(1)
                    continue
        for i in range(2):
            logger.info("="*20)
            
            if i==0:
                outline=chapter1
            else:
                outline=chapter2
            logger.info(f"outline:{outline}")
            detail_outline.append(outline)
            
            f_detail_outline.write("="*20)
            f_detail_outline.write("\n\n")
            f_detail_outline.write(outline)
            f_detail_outline.write("\n\n")
            logger.info("="*20)
            #对outline的数据处�?
            #step3 根据实现规划，完成写�?
            #调用历史信息检索模块（基于outline)
            cntent_prompt_tempate =ChatPromptTemplate.from_template(content_prompt_t)
            history= MindMap.find_relevant_info(outline,step,title,driver)
            
            pw=cntent_prompt_tempate.format_messages(volume_outline=volume_outline,
                                                     chapter_outline=outline,
                                                     last_chapter=last_chapter_story,
                                                     history=history)
            story_content=chat(pw[0].content) # TODO
            # story_content = re_story(story_content)
            last_chapter_story = story_content
            
            MindMap.set_history(story_content,driver,title,step)
            logger.info("*"*20)
            logger.info(f"content:{story_content}")
            logger.info("*"*20)
            #对content的数据处�?
            total_content.append(story_content)
            
            f_story.write("*"*20)
            f_story.write("\n\n")
            f_story.write(story_content)
            f_story.write("\n\n")
            f_story.write("*"*20)
            
            step+=1
            logger.info(step)
        chapter_index+=1
        # print(chapter_index)
    f_story.close()
    f_detail_outline.close()