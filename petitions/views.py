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
            return paginator.get_paginated_response(serializer.data)
        
        serializer = PetitionSerializer(petitions, many=True)
        return Response(serializer.data)