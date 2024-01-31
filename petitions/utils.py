import requests

# api key 활용
from django.conf import settings

# model에 data 처리
from .models import *
from django.utils.dateparse import parse_date


# petition_file 파일 다운로드 가능하도록 함수 추가로 설정 필요
# content 다운로드 받은 파일의 요약을 chat gpt에게 생성해달라 요청


# api 응답 데이터 db에 저장
def save_api_data_to_db(api_data, endpoint):
    for item in api_data[endpoint][1]['row']:
        # Petition 모델 업데이트 또는 생성
        petition, created = Petition.objects.update_or_create(
            BILL_NO = item['BILL_NO'],
            defaults={
                'BILL_NAME': item['BILL_NAME'],
                'PROPOSER': item['PROPOSER'],
                'PROPOSER_DT': parse_date(item['PROPOSE_DT']),
                'COMMITTEE_DT': parse_date(item['COMMITTEE_DT']),
            }
        )
        
        # Petition_Detail 모델 업데이트 또는 생성
        Petition_Detail.objects.update_or_create(
            BILL_NO = petition,
            defaults={
                'APPROVER': item['APPROVER'],
                'CURR_COMMITTEE': item['CURR_COMMITTEE'],
                'LINK_URL': item['LINK_URL'],
            }
        )
        
        # Petition_File 모델 업데이트 또는 생성
        Petition_File.objects.update_or_create(
            BILL_NO = petition
        )



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
