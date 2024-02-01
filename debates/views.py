# 데이터 처리
from .models import *
from petitions.models import *
from .serializers import *

# APIView 사용
from rest_framework.views import APIView

# Response 관련
from rest_framework.response import Response
from rest_framework import status

# 인증 관련
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

# 기타 계산 관련
from datetime import timedelta
from .utils import *


# 토론 기본 정보 등록하기(백엔드에서 미리 작업)
class DebateCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
            
    def post(self, request):
        petition_id = request.query_params.get('BILL_NO')
        if not petition_id:
            return Response({
                "error": "청원 번호(BILL_NO)가 제공되지 않았습니다."
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            petition = Petition.objects.get(BILL_NO=petition_id)
        except Petition.DoesNotExist:
            return Response({
                "error": "청원이 존재하지 않습니다."
            },
            status=status.HTTP_404_NOT_FOUND)
            
        # 이미 Debate 객체가 해당 petition_id로 존재하는지 확인
        if Debate.objects.filter(petition_id=petition_id).exists():
            return Response({
                "error": "해당 청원에 대한 토론이 이미 존재합니다."
            },
            status=status.HTTP_400_BAD_REQUEST)
        
        # 날짜 계산
        member_announcement_date = petition.COMMITTEE_DT + timedelta(days=5)
        debate_date = petition.COMMITTEE_DT + timedelta(days=15)
        
        # 찬성측, 반대측 코드 추출                
        debate_code_O, debate_code_X = generate_unique_codes()
        
        # 토론 정보 자동 생성
        debate = Debate.objects.create(
            member_announcement_date=member_announcement_date,
            debate_date=debate_date,
            petition_id=Petition.objects.get(BILL_NO=petition_id),
            debate_code_O=debate_code_O,
            debate_code_X=debate_code_X
        )
        
        res = Response({
            "member_announcement_date": debate.member_announcement_date,
            "debate_date": debate.debate_date,
            "estimated_time": debate.estimated_time,
            "debate_code_O": debate.debate_code_O,
            "debate_code_X": debate.debate_code_X,
            "petition_id": debate.petition_id.pk
        },
        status=status.HTTP_200_OK)
        
        return res