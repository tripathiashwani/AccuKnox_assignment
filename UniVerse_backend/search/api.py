from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from account.models import User
from account.serializers import UserSerializer


@api_view(['POST'])
def search(request):
    data = request.data
    query = data['query']
    print("query:", query)
    
    users = User.objects.filter(
        Q(name__icontains=query) | Q(email__iexact=query)
    )
    
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(users, request)
    users_serializer = UserSerializer(result_page, many=True)
    
    return paginator.get_paginated_response(users_serializer.data)