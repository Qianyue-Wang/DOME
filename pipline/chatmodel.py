
from http import HTTPStatus
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
import openai
import os
import time
import requests
import json

api_key = 'Bearer sk-c7dpymyf5hoips7y'


class Llama2Model():
    def __init__(self, api_key, model, temperature=None, max_tokens=None, top_p=None, seed=None) -> None:
        self.api = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.seed = seed
        self.messages = []
        self.initial_flag = True  # Allows for setting initial input for the bot to speak first
        self.present_list = []  # To store dialogue history with potential for critique
        
    def call(self, content, add_messages = True) -> str:
        # 需要完成的事情：
        # 响应成功时self.messages添加用户输入的内容
        # 响应成功时self.messages添加assistant回复的内容
        # 返回回复内容，只有文本
        
        
        # 定义请求体
        request_body = {
            "query": content,
            "conversation_id": "",
            "history_len": -1,  # 保留全部历史记录，根据需要调整
            "history": self.messages,
            "stream": False,
            "model_name": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "prompt_name": "default"
        }

        # 发送POST请求
        response = requests.post(self.api, json=request_body)

        # 检查响应状态码
        if response.status_code == 200:
            if add_messages:
                self.messages.append({'role': Role.USER, 'content': content})
            res = response.content.decode('utf-8')
            # 移除字符串开始的 "data: " 部分，因为它不是有效的JSON格式
            res_json_str = res.split("data: ", 1)[1]

            # 使用json.loads解析JSON字符串
            res_json = json.loads(res_json_str)

            # 提取 "text" 字段
            text = res_json.get("text", "")
            # print(text)
            if add_messages:
                self.messages.append({'role': Role.ASSISTANT,
                                'content': text})
            # print(1111)
            # print(self.messages)
            return text
        else:
            print("请求失败，状态码:", response.status_code)
            raise 0
        
    def add_system(self, system):
        self.messages = [{'role': Role.SYSTEM, 'content': system}]
    
    
    def add_content(self, content):
        self.messages.append({'role': Role.ASSISTANT, 'content': content})

    def save_prompt(self, dialog,content,response):
        self.present_list.append({"history_talk":dialog, "prompt":content, "response":response})
    
    def clear(self):
        self.messages = []
        self.initial_flag = True


class InfiniModel():
    def __init__(self, api_key, model, temperture=None, max_tokens=None, top_p = None, seed = None) -> None:
        self.api_key = api_key
        self.model = model
        self.temperture = temperture
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.seed = seed
        self.messages = []
        self.initial_flag = True # 对于机器人而言，可根据flag设置初始输入，实现机器人先发言
        self.present_list = []  # 用来存放历史对话（考虑到会增加一些critic的内容，所以单独定义一个）
    
    def call(self, content, add_messages = True,evaluate=False):
        s=""
        if evaluate:
            s="You are a critic and you are evaluating the relevance of the given knowledge and the given description."
        else:
            s="You are a Knowledge Graph expert and are good at extracting information from the Knowledge Graph. You are helping a user to extract information from the Knowledge Graph."

        url = 'https://cloud.infini-ai.com/maas/{}/nvidia/chat/completions'.format(self.model)
        headers = {
                "Content-Type": "application/json",
                "Authorization": self.api_key  
                }
        data = {
        "model": self.model,
        'temperture': self.temperture,
        "messages": self.messages + [{'role': Role.SYSTEM, 'content': s},{'role': Role.USER, 'content': content}],
        }
             
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == HTTPStatus.OK:
            # append result to messages.
            
            if add_messages:
                self.messages.append({'role': Role.USER, 'content': content})     
                       
            message = {'role':  json.loads(response.text)['choices'][0]['message']['role'],
                            'content': json.loads(response.text)['choices'][0]['message']['content']}
            if add_messages:
                self.messages.append(message)
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
        return message['content']
                 
    def add_system(self, system):
        self.messages = [{'role': Role.SYSTEM, 'content': system}]
    
    
    def add_content(self, content):
        self.messages.append({'role': Role.ASSISTANT, 'content': content})

    def save_prompt(self, dialog,content,response):
        self.present_list.append({"history_talk":dialog, "prompt":content, "response":response})
    
    def clear(self):
        self.messages = []
        self.initial_flag = True


class ChatModel():
    def __init__(self, api_key, model, temperture=None, max_tokens=None, top_p = None, seed = None) -> None:
        self.api_key = api_key
        self.model = model
        self.temperture = temperture
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.seed = seed
        self.messages = []
        self.initial_flag = True # 对于机器人而言，可根据flag设置初始输入，实现机器人先发言
        self.present_list = []  # 用来存放历史对话（考虑到会增加一些critic的内容，所以单独定义一个）
    
    def call(self, content):

        self.messages.append({'role': Role.USER, 'content': content})
        response = Generation.call(
            model=self.model,
            api_key= api_key,
            messages=self.messages,
            result_format='message',  # set the result to be "message" format.
        )

        if response.status_code == HTTPStatus.OK:
            # append result to messages.
            self.messages.append({'role': response.output.choices[0]['message']['role'],
                            'content': response.output.choices[0]['message']['content']})
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
        return response.output.choices[0]['message']['content']
                 
    def add_system(self, system):
        self.messages = [{'role': Role.SYSTEM, 'content': system}]
    
    
    def add_content(self, content):
        self.messages.append({'role': Role.ASSISTANT, 'content': content})

    def save_prompt(self, dialog,content,response):
        self.present_list.append({"history_talk":dialog, "prompt":content, "response":response})
    
    def clear(self):
        self.messages = []
        self.initial_flag = True



class GPTModel():
    def __init__(self, api_key, base_url, model, temperature=None, max_tokens=None, top_p=None, frequency_penalty=None, presence_penalty=None, stop_sequences=None, seed=None) -> None:
        openai.api_key = api_key
        openai.api_base = base_url  # 设置基础 URL，如果有需要的话
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop_sequences = stop_sequences
        self.seed = seed
        self.messages = []
        self.initial_flag = True # 对于机器人而言，可根据flag设置初始输入，实现机器人先发言
        self.present_list = []  # 用来存放历史对话（考虑到会增加一些critic的内容，所以单独定义一个）

    def call(self, content, add_messages = True):
        # 此处的实现依赖于您具体想要调用的 API，假设是一个聊天模型
        # self.messages.append({'role': 'user', 'content': content})
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages + [{'role': 'user', 'content': content}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                stop=self.stop_sequences
            )
            if response['choices']:
                
                if add_messages:
                    self.messages.append({'role': 'user', 'content': content})  
                    
                generated_text = response['choices'][0].message.content
                
                if add_messages:
                    self.messages.append({'role': response['choices'][0].message.role,
                                'content': response['choices'][0].message.content})
                    
                return generated_text
            else:
                print("No response generated")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def add_system(self, system):
        self.messages = [{'role': Role.SYSTEM, 'content': system}]
    
    
    def add_content(self, content):
        self.messages.append({'role': Role.ASSISTANT, 'content': content})

    def save_prompt(self, dialog,content,response):
        self.present_list.append({"history_talk":dialog, "prompt":content, "response":response})
    
    def clear(self):
        self.messages = []
        self.initial_flag = True
    


if __name__ == '__main__':
    model = InfiniModel(api_key=api_key, model='llama-2-70b-chat')
    answer = model.call("""Your task is to convert the information represented as a triplet delimited by ''' into natural language.\n

    The triplet is in the form:[entity, their relationship, entity].\n

    Each triplet contains the following elements:\n

    The first element is the entity making the action.\n

    The second element is the action.\n

    The third element is the giving object of the action.\n



    Describe the knowledge in the triplet into natural language in just one sentence.\n

    Your answer should only contain the final converted sentence in natural language.\n


    

    triplet:'''['Diane Chambers', 'decides to have', 'revenge']'''\n


    Your answer:""")
    print(answer)
    
   
    
    
    
    