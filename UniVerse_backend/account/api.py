from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import JsonResponse
from notification.utils import create_notification
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm, ProfileForm
from .models import User, FriendshipRequest
from .serializers import UserSerializer,FriendshipRequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.cache import cache





@api_view(['GET'])
def me(request):
    user = request.user
    cached_user = cache.get(f'user_{user.id}')
    
    if not cached_user:
        print('not redis')
        cached_user = UserSerializer(user).data
        cache.set(f'user_{user.id}', cached_user, timeout=60*5)  # Cache for 5 minutes

    return JsonResponse(cached_user)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'
    print(data)
    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        user = form.save()
        user.is_active = True
        form.save()
        
        print("signup validated in api")
    else:
        message = form.errors.as_json()
    print(message)

    return JsonResponse({'message': message})



@api_view(['GET'])
def friends(request, pk):
    cache_key = f'friends_{pk}'
    cached_data = cache.get(cache_key)
    if not cached_data:
        user = User.objects.get(pk=pk)
        requests = []
        if user == request.user:
            requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
            requests = FriendshipRequestSerializer(requests, many=True).data

        friends = user.friends.all()
        cached_data = {
            'user': UserSerializer(user).data,
            'friends': UserSerializer(friends, many=True).data,
            'requests': requests
        }
        cache.set(cache_key, cached_data, timeout=60*5)  # Cache for 5 minutes

    return JsonResponse(cached_data, safe=False)




    
# @api_view(['POST'])
# def send_friendship_request(request, pk):
#     user = User.objects.get(pk=pk)
#     check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
#     check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)
    
#     if not check1 and not check2:
#         friendrequest = FriendshipRequest.objects.create(created_for=user, created_by=request.user)
#         create_notification(request, 'new_friendrequest', friendrequest_id=friendrequest.id)
#         cache.delete(f'friends_{request.user.id}')  
#         cache.delete(f'friends_{user.id}')          
#         return JsonResponse({'message': 'friendship request created'})
#     else:
#         return JsonResponse({'message': 'request already sent'})

@api_view(['POST'])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)
    created_by = request.user

    # Cache key for tracking the request count
    cache_key = f'friend_requests_{created_by.id}'
    request_count = cache.get(cache_key, 0)

    if request_count >= 3:
        return JsonResponse({'message': 'You cannot send more than 3 friend requests within a minute'}, status=429)

    # Check if a friendship request already exists between the users
    check1 = FriendshipRequest.objects.filter(created_for=created_by, created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user, created_by=created_by)
    
    if not check1.exists() and not check2.exists():
        friendrequest = FriendshipRequest.objects.create(created_for=user, created_by=created_by)
        create_notification(request, 'new_friendrequest', friendrequest_id=friendrequest.id)
        
        cache.set(cache_key, request_count + 1, 60)
        
        cache.delete(f'friends_{created_by.id}')
        cache.delete(f'friends_{user.id}')          
        
        return JsonResponse({'message': 'Friendship request created'})
    else:
        return JsonResponse({'message': 'Request already sent'})

@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()
    user.friends.add(request.user)
    user.friends_count += 1
    user.save()
    request_user = request.user
    request_user.friends_count += 1
    request_user.save()
    create_notification(request, 'accepted_friendrequest', friendrequest_id=friendship_request.id)
    
    cache.delete(f'friends_{request.user.id}')  
    cache.delete(f'friends_{user.id}')          
    
    return JsonResponse({'message': 'friendship request updated'})




@api_view(['GET'])
def my_friendship_suggestions(request):
    cache_key = f'friendship_suggestions_{request.user.id}'
    suggestions = cache.get(cache_key)
    
    if not suggestions:
        suggestions = UserSerializer(request.user.people_you_may_know.all(), many=True).data
        cache.set(cache_key, suggestions, timeout=60*5)  # Cache for 5 minutes
    
    return JsonResponse(suggestions, safe=False)



