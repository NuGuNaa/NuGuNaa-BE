import random
from .models import *


def generate_unique_codes():
    while True:
        code_O = str(random.randint(10000, 99999))
        code_X = str(random.randint(10000, 99999))
        
        # 찬성, 반대측 코드가 서로 다르고, 데이터베이스에도 존재하지 않는지 확인
        if code_O != code_X and not \
            Debate.objects.filter(debate_code_O=code_O).exists() and not \
            Debate.objects.filter(debate_code_X=code_X).exists():
                return code_O, code_X