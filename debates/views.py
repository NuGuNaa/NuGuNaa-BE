# 데이터 처리
from .models import *
from petitions.models import *
from .serializers import *
from django.db.models import F, Q

# APIView 사용
from rest_framework.views import APIView

# Response 관련
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# 인증 관련
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

# 기타 계산 관련
from datetime import timedelta
from .utils import *


# 토론 기본 정보 등록하기(서버에서만 처리 - 관리자용)
class DebateCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
            
    def post(self, request):
        petition_id = request.query_params.get('BILL_NO')
        if not petition_id:
            return Response({
                "error": "잘못된 url 입니다. parameter를 작성해주세요."
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
        member_announcement_date = petition.COMMITTEE_DT + timedelta(days=10)
        debate_date = petition.COMMITTEE_DT + timedelta(days=30)
        
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
    
    
# 토론 신청한 사람 추첨하기(서버에서만 처리 - 관리자용)
class RandomDebateApplyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):        
        petition_id = request.GET.get('BILL_NO')
        position = request.GET.get('position')
        
        # 각 토론에서 찬성/반대 구분하여 사람 리스트 확인
        if petition_id is not None and position is not None:
            debate_applies = Debate_Apply.objects.filter(petition_id=petition_id, position=position)
        else:
            response = {
                "error": "잘못된 url 입니다. parameter를 작성해주세요."
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
        # 랜덤으로 2명 뽑기
        if debate_applies.count() > 2:
            selected_applies = random.sample(list(debate_applies), 2)
        elif debate_applies.count() > 0:
            selected_applies = list(debate_applies)
        else:
            selected_applies = []
        
        # Debate_Apply raffle_check 업데이트
        # 랜덤으로 추첨된 항목들의 raffle_check를 True로 설정
        for apply in selected_applies:
            apply.raffle_check = True
            apply.save()
            
        # 추첨되지 않은 나머지 항목들의 raffle_check를 False로 설정   
        # petition_id와 position이 일치하는데, selected_applies에 포함되지 않은 항목을 찾기
        Debate_Apply.objects.filter(
            petition_id=petition_id, 
            position=position
        ).exclude(
            id__in=[apply.id for apply in selected_applies]
        ).update(raffle_check=False) 
            
        serializer = DebateApplySerializer(selected_applies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
# 사용자 신청 내역 확인하기
class UserDebateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        user_email = request.GET.get('email')
        user = User.objects.get(email=user_email)

        # 해당 사용자의 모든 토론 신청 정보를 가져오기.
        applications = Debate_Apply.objects.filter(email=user).select_related('petition_id').annotate(
            bill_name=F('petition_id__BILL_NAME'),
            debate_code_O=F('petition_id__debate__debate_code_O'),
            debate_code_X=F('petition_id__debate__debate_code_X')
        ).values('bill_name', 'position', 'debate_code_O', 'debate_code_X', 'raffle_check')
        
        # 결과 데이터 구성
        result_data = {
            "results": list(applications)
        }

        return Response(result_data, status=status.HTTP_200_OK)
    
    
# 토론 진행 상황 확인하기
class DebateStatementAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 토론 불러오기
    def get(self, request):
        petition_id = request.GET.get('BILL_NO')
        position = request.GET.get('position')
        
        if not petition_id or not position:
            return Response({
            "error": "잘못된 url 입니다. parameter를 작성해주세요."
            },
            status=status.HTTP_400_BAD_REQUEST)
        
        debate = Debate.objects.get(petition_id=petition_id)
        user = request.user
        
        # 현재 로그인한 사용자의 발언을 조회
        user_statements = Debate_Statement.objects.filter(
            debate_id=debate,
            statement_user__user_email=user,
            position=position,
            is_chatgpt=False,
        ).distinct()

        # ChatGPT의 답변을 조회
        chatgpt_statements = Debate_Statement.objects.filter(
            debate_id=debate,
            is_chatgpt=True
        ).distinct()

        # 두 쿼리셋의 결과를 Python 리스트로 결합
        statements = list(user_statements) + list(chatgpt_statements)

        response_data = [
            {
                "id": statement.id,
                "position": statement.position,
                "content": statement.content,
                "statement_type": statement.statement_type,
                "is_chatgpt": statement.is_chatgpt,
                "email": user.email if not statement.is_chatgpt else "ChatGPT"
            } for statement in statements
        ]
        return Response(response_data, status=status.HTTP_200_OK)
    
    # 토론 입력하기(사용자)
    def post(self, request):
        petition_id = request.GET.get('BILL_NO')
        position = request.GET.get('position')
        type = request.GET.get('type')
        
        if not petition_id or not position or not type:
            return Response({
            "error": "잘못된 url 입니다. parameter를 작성해주세요."
            },
            status=status.HTTP_400_BAD_REQUEST)
            
        content = request.data.get('content')
        
        if content is None:
            return Response({"error": "내용을 입력해주세요."})
        
        debate = Debate.objects.get(petition_id=petition_id)
        user = request.user
        
        debate_statement = Debate_Statement.objects.create(
            debate_id=debate,
            statement_type=type,
            content=content,
            is_chatgpt=False,  # 사용자가 입력한 내용
            position=position
        )
                
        Statement_User.objects.create(
            statement_id=debate_statement,
            user_email=user
        )
        
        response_data = {
            "statement_id": debate_statement.id,
            "content": debate_statement.content,
            "is_chatgpt": debate_statement.is_chatgpt,
            "statement_type": debate_statement.statement_type,
            "email": user.email
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
        
class StatementSummaryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # chat gpt에 입력된 내용 묶어서 전달하기
    def post(self, request):
        petition_id = request.GET.get('BILL_NO')
        position = request.GET.get('position')
        type = request.GET.get('type')
        
        if not petition_id or not position or not type:
            return Response({
            "error": "잘못된 url 입니다. parameter를 작성해주세요."
            },
            status=status.HTTP_400_BAD_REQUEST)
            
        debate = get_object_or_404(Debate, petition_id=petition_id)
            
        statements = Debate_Statement.objects.filter(
            debate_id=debate.id,
            statement_type=type,
            position=position,
            is_chatgpt=False
        ).values('id', 'statement_type', 'content', 'is_chatgpt', 'position')
        
        chatgpt_response = send_to_chatgpt(statements, position)
        
        debate = get_object_or_404(Debate, petition_id=petition_id)
        debate_statement = Debate_Statement.objects.create(
            debate_id = debate,
            content = chatgpt_response,
            is_chatgpt = True,
            statement_type = type,
            position = position
        )
        
        return Response({
            "id": debate_statement.id,
            "statement_type": debate_statement.statement_type,
            "position": debate_statement.position,
            "content": debate_statement.content,
            "is_chatgpt": debate_statement.is_chatgpt
        },
        status=status.HTTP_200_OK)