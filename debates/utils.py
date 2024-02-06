import random
from .models import *

# api key
from django.conf import settings
import openai

openai.api_key = settings.OPENAI_APIKEY


def generate_unique_codes():
    while True:
        code_O = str(random.randint(10000, 99999))
        code_X = str(random.randint(10000, 99999))
        
        # 찬성, 반대측 코드가 서로 다르고, 데이터베이스에도 존재하지 않는지 확인
        if code_O != code_X and not \
            Debate.objects.filter(debate_code_O=code_O).exists() and not \
            Debate.objects.filter(debate_code_X=code_X).exists():
                return code_O, code_X
      

# type 변형
def get_type_of_value(statement_type):
    type_map = {
        '1': '입론',
        '2': '반론1',
        '3': '반론2',
        '4': '반론3',
        '5': '결론',
    }
    return type_map.get(statement_type)

def get_meaning_of_position(position):
    position_map = {
        '0': '찬성',
        '1': '반대'
    }
    return position_map.get(position)
      

# chat gpt에 전송하기        
def send_to_chatgpt(statements, position):
    messages = []
    type = ""
    
    position_value = get_meaning_of_position(position)
    
    for statement in statements:
        statement_type = statement.get('statement_type')
        content = statement.get('content')
        
        statement_type_value = get_type_of_value(statement_type)
        type += statement_type_value
        message = f"{statement_type_value}: {content}"
        messages.append(message)
        messages.append("\n")
        type = ""
        
    prompt = "".join(messages)
    user_content = [
        {
            "role": "user",
            "content": "Please summary the context in Korean.",
            "role": "assistant",
            "content": f"{type} 시간에 작성한 주장들입니다.\
                {position_value} 측의 내용을 요약하면 다음과 같습니다.\
                첫째, 어떠한 주장이 있습니다.\
                둘째, 어떠한 주장이 있습니다.",
            "role": "user",
            "content": f"Please summary {prompt} systematically. \
                Take a deep breath and proceed with confidence."
        }
    ]
    message_to_send = [
        {
            "role": "system",
            "content": "You must professionally summarize what has been conveyed.\
                You are the moderator of the discussion. \
                Therefore, you must systematically summarize the information received from the database. \
                Treat duplicate claims as one. Be sure to answer in Korean. \
                Take a deep breath and do it."
        }
    ]
    message_to_send.extend(user_content)
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=1.0,
        messages=message_to_send
    )
    
    chatgpt_response = response['choices'][0]['message']['content']
    
    return chatgpt_response