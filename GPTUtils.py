from openai import OpenAI
import sys

class GPTUtils:
    
    def __init__(self, background_context_str=""):

        #read openai api key
        with open("keys/openai_api_key.txt", 'r') as readfile:
            openai_api_key = readfile.read()
        
        self.client = OpenAI(api_key=openai_api_key)
        
        self.background_context_str = background_context_str
        self.prompt_text = ""

        
    def call_gpt(self, prompt_text="", background_context_str="", call_gpt_turbo=True):
        
        if call_gpt_turbo == True:
            answer_text = self.call_gpt_turbo(prompt_text, background_context_str)
        else:
            answer_text = self.call_gpt_4(prompt_text, background_context_str)
        
        return answer_text
        

    def call_gpt_4(self, prompt_text, background_context_str):

        
        #response = openai.ChatCompletion.create(
        response = self.client.chat.completions.create(
        messages=[{"role": "system", "content": background_context_str},
                {"role": "user", "content": prompt_text}],
        model='gpt-4',
        temperature=0,
        max_tokens=2000,
        frequency_penalty=0,
        presence_penalty=0
        )

        answer_text = response.choices[0].message.content

        return answer_text


    def call_gpt_turbo(self, prompt_text, background_context_str):

        #response = openai.ChatCompletion.create(
        response = self.client.chat.completions.create(
        messages=[{"role": "system", "content": background_context_str},
                  {"role": "user", "content": prompt_text}],
        model='gpt-3.5-turbo',   #gpt-3.5-turbo   #gpt-3.5-turbo-0301  #gpt-4
        temperature=0,
        max_tokens=2000,
        frequency_penalty=0,
        presence_penalty=0
        )

        answer_text = response.choices[0].message.content

        return answer_text