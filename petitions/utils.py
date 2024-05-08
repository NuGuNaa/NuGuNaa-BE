import os
import requests

# api key 활용
from django.conf import settings

# model에 data 처리
from .models import *
from django.utils.dateparse import parse_date

# 파일 관련
import PyPDF2
import openai
import time
from .file_urls import file_urls

openai.api_key = settings.OPENAI_APIKEY


# chat gpt에 파일 text를 입력하여 요약 받기
def get_chatgpt_summary(filename, text):
    prompt = f"{filename}의 내용: {text}"
    user_content = [
        {
            "role": "user",
            "content": "Please summary the context in 1 sentence in Korean.",
            "role": "assistant",
            "content": "이 청원은 무엇에 관한 것입니다.",
            "role": "user",
            "content": f"Please summary {prompt} context easily and shortly in 1 sentence in Korean. \
                You must not exceed the reply in 1 sentence. \
                Take a deep breath and proceed with confidence."
        }
    ]
    
    message_to_send = [
        {
            "role": "system",
            "content": "You are an expert at summarizing received texts. \
                There's a text included in the prompt that needs to be condensed \
                so people can easily understand it. \
                You must summarize the all context in 1 sentences. Do not exceed 1 sentence. \
                Your response must be in Korean, without exception. \
                Take a deep breath and proceed with confidence."
        }
    ]
    message_to_send.extend(user_content)
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=1.0,
        max_tokens=200,
        messages=message_to_send
    )
    
    chatgpt_response = response['choices'][0]['message']['content']

    return chatgpt_response
    

# files 목록에서 해당 청원 원본 파일 찾기
def find_and_extract_text_from_pdf_file(petition_instance, directory_path):
    text = ""
    bill_no = petition_instance.BILL_NO
    file_path = None
    
    for filename in os.listdir(directory_path):
        if str(bill_no) in filename:
            print(filename)
            file_path = directory_path + filename
            break
    
    with open(file_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            text += page.extract_text()
    chatgpt_summary = get_chatgpt_summary(filename, text)
    
    return chatgpt_summary


# petition_file 파일 경로 확인
def save_file_path(bill_no):
    petition_instance = Petition.objects.get(BILL_NO=bill_no)
    directory_path = 'files/'
    
    for url in file_urls:
        url = url.strip()
        if str(bill_no) in url:
            petition_file, created = Petition_File.objects.update_or_create(
                BILL_NO=petition_instance,
                defaults={'petition_file_url': url}
            )
 
            if not petition_file.content:
                content_value = find_and_extract_text_from_pdf_file(petition_instance, directory_path)
                Petition_File.objects.filter(BILL_NO=petition_instance).update(content=content_value)
            break
        time.sleep(0.5)
        

# api 응답 데이터 db에 저장
def save_api_data_to_db(api_data, endpoint):
    for item in api_data[endpoint][1]['row']:
        # Petition 모델 업데이트 또는 생성
        petition, created = Petition.objects.update_or_create( # 만약 청원이 추가될 경우, update_or_update로 수정
            BILL_NO = item['BILL_NO'],
            defaults={
                'BILL_NAME': item['BILL_NAME'],
                'PROPOSER': item['PROPOSER'],
                'PROPOSER_DT': parse_date(item['PROPOSE_DT']),
                'COMMITTEE_DT': parse_date(item['COMMITTEE_DT']),
            }
        )
        
        # Petition_Detail 모델 업데이트 또는 생성
        Petition_Detail.objects.update_or_create( # 만약 청원이 추가될 경우, update_or_update로 수정
            BILL_NO = petition,
            defaults={
                'APPROVER': item['APPROVER'],
                'CURR_COMMITTEE': item['CURR_COMMITTEE'],
                'LINK_URL': item['LINK_URL'],
            }
        )
        
        # Petition_File 모델 업데이트 또는 생성
        # if created:
        #     save_file_path(item['BILL_NO'])
        # else:
        #     Petition_File.objects.get(BILL_NO=petition)
        
        # 청원이 새로 추가된 경우
        save_file_path(item['BILL_NO'])
        
        ### 청원 추가시 하는 활동
        # 1. petitions utils.py에서 get_or_create -> update_or_create
        # 2. save_file_path(item['BILL_NO'])로 수정
        # 3. file_urls.py에 올라온 청원 파일 aws s3에 올리고 링크 받아서 추가하기
        # 4. postman에서 청원 리스트 업데이트
        # 5. postman에서 청원 관련 토론 생성
        # 6. utils.py 코드 다시 돌려놓기


# api에서 데이터 읽어오기
def call_national_assembly_api(endpoint, additional_params=None):
    base_url = "https://open.assembly.go.kr/portal/openapi"
    api_key = settings.PUBLIC_API_KEY
    
    params = {
        'key': api_key,
        'Type': 'json',
        'pIndex': 1,
        'pSize': 30,
    }
    
    if additional_params:
        params.update(additional_params) # 추가 파라미터가 있으면 병합
        
    api_response = requests.get(f"{base_url}/{endpoint}", params=params)
    api_data = api_response.json()
    save_api_data_to_db(api_data, endpoint)