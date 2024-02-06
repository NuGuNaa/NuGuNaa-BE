# 데이터 처리
from .models import *
from debates.models import *
from .serializers import *
from debates.serializers import *

# APIView 사용
from rest_framework.views import APIView

# Response 관련
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# 인증 관련
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

# 공공 api 활용
from .utils import *
from .pagination import CustomResultsSetPagination

# 기타 계산
from datetime import datetime


# 청원 리스트 보여주기
class PetitionListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        endpoint = "nvqbafvaajdiqhehi"
        call_national_assembly_api(endpoint)
        
        petitions = Petition.objects.all()
        paginator = CustomResultsSetPagination()
        page = paginator.paginate_queryset(petitions, request, view=self)
        
        if page is not None:
            serializer = PetitionSerializer(page, many=True)
            data = self.filtering_data(serializer.data)
            return paginator.get_paginated_response(data)
        
        serializer = PetitionSerializer(petitions, many=True)
        data = self.filtering_data(serializer.data)
        return Response(data)
    
    def filtering_data(self, data):
        filtered_data = []
        current_date = datetime.now().date()
            
        for item in data:
            petition_id = item['BILL_NO']
            
            try:
                debate = Debate.objects.get(petition_id=petition_id)
                d_day = (debate.debate_date.date() - current_date).days
            except Debate.DoesNotExist:
                d_day = "N/A"
            
            filtered_data.append({
                'BILL_NO': item['BILL_NO'],
                'BILL_NAME': item['BILL_NAME'],
                'PROPOSER': item['PROPOSER'],
                'PROPOSER_DT': item['PROPOSER_DT'],
                'content': item.get('petition_file', {}).get('content', ''),
                "d_day": d_day
            })
        return filtered_data
    
    
# 청원 상세히 보기
class PetitionDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        bill_no = request.GET.get('BILL_NO')
        if not bill_no:
            return Response({
                "error": "잘못된 url 입니다. parameter를 작성해주세요."
            },
            status=status.HTTP_400_BAD_REQUEST)
            
        try:
            petition = Petition.objects.get(BILL_NO=bill_no)
            petition_detail = Petition_Detail.objects.get(BILL_NO=bill_no)
            petition_file = Petition_File.objects.get(BILL_NO=bill_no)
            
            # 청원 상세 정보
            petition_data = {
                'BILL_NO': petition.BILL_NO,
                'BILL_NAME': petition.BILL_NAME,
                'PROPOSER': petition.PROPOSER,
                'APPROVER': petition_detail.APPROVER,
                'PROPOSER_DT': petition.PROPOSER_DT,
                'COMMITTEE_DT': petition.COMMITTEE_DT,
                'CURR_COMMITTEE': petition_detail.CURR_COMMITTEE,
                'LINK_URL': petition_detail.LINK_URL,
                'content': petition_file.content,
                'petition_file_url': petition_file.petition_file_url
            }
            
            # 토론 정보 
            debate_data = {}
            try:
                debate = Debate.objects.get(petition_id=bill_no)
                debate_data = {
                    'member_announcement_date': debate.member_announcement_date,
                    'debate_date': debate.debate_date,
                    'estimated_time': debate.estimated_time,
                    'debate_code_O': debate.debate_code_O,
                    'debate_code_X': debate.debate_code_X
                }
            except Debate.DoesNotExist:
                debate_data = "토론이 아직 생성되지 않았습니다."
            
            # 최종 응답 데이터
            response_data = {
                'petition': petition_data,
                'debate': debate_data
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except (Petition.DoesNotExist, Petition_Detail.DoesNotExist, Petition_File.DoesNotExist):
            return Response({
                "error": "청원을 찾을 수 없습니다."
            },
            status=status.HTTP_404_NOT_FOUND)
            
# 사용자들이 토론 참여 신청하기    
    def post(self, request):        
        petition_id = request.GET.get('BILL_NO', None)
        email = request.data.get('email', None)
        user = User.objects.get(email=email)
        
        data = request.data.copy()
        data['petition_id'] = petition_id
        
        serializer = DebateApplySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            response_data = {
                'petition_id': petition_id,
                # 'email': user.email,
                'email': serializer.data['email'],
                'position': serializer.data['position']
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)