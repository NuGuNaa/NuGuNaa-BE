# 데이터 처리
from .models import *
from .serializers import *

# APIView 사용
from rest_framework.views import APIView

# Response 관련
from rest_framework.response import Response
from rest_framework import status

# 인증 관련
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

# 공공 api 활용
from .utils import call_national_assembly_api
from .pagination import CustomResultsSetPagination


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
            
        for item in data:
            filtered_data.append({
                'BILL_NAME': item['BILL_NAME'],
                'PROPOSER': item['PROPOSER'],
                'PROPOSER_DT': item['PROPOSER_DT'],
                'content': item.get('petition_file', {}).get('content', '')
            })
        return filtered_data
    
    
# 청원 상세히 보기
class PetitionDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        bill_no = request.query_params.get('BILL_NO')
        if not bill_no:
            return Response({
                "error": "잘못된 url 입니다. parameter를 작성해주세요."
            },
            status=status.HTTP_400_BAD_REQUEST)
            
        try:
            petition = Petition.objects.get(BILL_NO=bill_no)
            petition_detail = Petition_Detail.objects.get(BILL_NO=bill_no)
            petition_file = Petition_File.objects.get(BILL_NO=bill_no)
            
            data = {
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
            return Response(data, status=status.HTTP_200_OK)
        
        except (Petition.DoesNotExist, Petition_Detail.DoesNotExist, Petition_File.DoesNotExist):
            return Response({
                "error": "청원을 찾을 수 없습니다."
            },
            status=status.HTTP_404_NOT_FOUND)