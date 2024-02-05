import random
from .models import *

# 이메일 보내기
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.conf import settings
ID = settings.ID
PWD = settings.PASSWORD


def generate_unique_codes():
    while True:
        code_O = str(random.randint(10000, 99999))
        code_X = str(random.randint(10000, 99999))
        
        # 찬성, 반대측 코드가 서로 다르고, 데이터베이스에도 존재하지 않는지 확인
        if code_O != code_X and not \
            Debate.objects.filter(debate_code_O=code_O).exists() and not \
            Debate.objects.filter(debate_code_X=code_X).exists():
                return code_O, code_X
            
            
# def extract_emails_from_selected_applies(selected_applies):
#     email_list = [apply.email.email for apply in selected_applies]
#     return email_list
            
            
def send_email(subject, body, to_email):
    # 이메일 메시지 설정
    msg = MIMEMultipart()
    msg['From'] = 'hyumeesun@naver.com'
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        server = smtplib.SMTP('smtp.naver.com', 587)
        server.starttls()
        server.login(ID, PWD)
        server.sendmail('누구나NuGuNa', to_email, msg.as_string().encode('utf-8'))
        
        success_response = {"message": "이메일 전송 성공!"}
        return success_response
    except Exception as e:
        error = str(e)
        fail_message = f"이메일 전송 실패: {error}"
        fail_response = {"message": fail_message}
        return fail_response
    finally:
        server.quit()