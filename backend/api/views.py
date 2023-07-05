from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view , permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# Create your views here.
from .serializers import *
from .permissions import *


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializers
    queryset = get_user_model().objects.all()



# Status

# HTTP_100_CONTINUE
# HTTP_101_SWITCHING_PROTOCOLS
# HTTP_200_OK
# HTTP_201_CREATED
# HTTP_204_NO_CONTENT
# HTTP_300_MULTIPLE_CHOICES
# HTTP_301_MOVED_PERMANENTLY
# HTTP_302_FOUND
# HTTP_303_SEE_OTHER
# HTTP_304_NOT_MODIFIED
# HTTP_307_TEMPORARY_REDIRECT
# HTTP_400_BAD_REQUEST
# HTTP_401_UNAUTHORIZED
# HTTP_403_FORBIDDEN
# HTTP_404_NOT_FOUND
# HTTP_405_METHOD_NOT_ALLOWED
# HTTP_406_NOT_ACCEPTABLE
# HTTP_409_CONFLICT
# HTTP_410_GONE
# HTTP_500_INTERNAL_SERVER_ERROR
# HTTP_422_UNPROCESSABLE_ENTITY
# HTTP_429_TOO_MANY_REQUESTS
# HTTP_500_INTERNAL_SERVER_ERROR
# HTTP_501_NOT_IMPLEMENTED
# HTTP_502_BAD_GATEWAY
# HTTP_503_SERVICE_UNAVAILABLE
# HTTP_504_GATEWAY_TIMEOUT
# HTTP_505_HTTP_VERSION_NOT_SUPPORTED
# HTTP_507_INSUFFICIENT_STORAGE
# HTTP_509_BANDWIDTH_LIMIT_EXCEEDED
# HTTP_511_NETWORK_AUTHENTICATION_REQUIRED
# HTTP_598_NETWORK_READ_TIMEOUT_ERROR
# HTTP_599_NETWORK_CONNECT_TIMEOUT_ERROR
# HTTP_601_UNKNOWN_ERROR
# HTTP_602_SERVICE_NOT_AVAILABLE
# HTTP_603_SERVICE_DEPENDENCY_ERROR
# HTTP_604_NETWORK_ERROR
# HTTP_605_SERVICE_UNAVAILABLE_RETRY_LATER
# HTTP_606_SERVICE_UNAVAILABLE_RETRY_WITH
# HTTP_607_SERVICE_UNAVAILABLE_RETRY_NOW

# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def register_user_daniel(request):
    # body = request.body
    # username = body.username
    # password = body.password
    # email = body.password 
    # data = UserCreationSerilizer(data = request.body)
    context = {}
    if request.method == "POST":
        context['Message' ] = 'Utilisateur enregister avec succès'
        return Response(context, status = status.HTTP_200_OK)
    
    if request.method == "GET":


        context['Message' ] = 'Utilisateur enregister avec succès'
        return Response(context, status = status.HTTP_200_OK)

    # return JsonResponse('Our API', safe = False)
     

@api_view(['GET', 'POST'])
def api_home(request, *args, **kwargs):
    user = User.objects.all()
    user = request.user or None
    if user != None:
        print(user.username)
   
    serializer = UserSerializers(user)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    instance = request.user
    serializer = UserSerializers(instance)

    if request.method == 'GET':
        return Response(serializer.data)
    
    if request.method == 'POST':
        data = request.data
        data_serialized = UserSerializers(instance, data)
        if data_serialized.is_valid():
            data_serialized.save()
            context = {}
            context['message'] = 'Informations modifiées avec succès'
            context['data'] =  data_serialized.data
            print(context)
            return Response(context)
        else:
            return Response( {"message":'Verifiez tous les champ'} , status  = status.HTTP_304_NOT_MODIFIED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    User = get_user_model()
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if not user.check_password(old_password):
        return Response({'old_password': 'L\'ancien mot de passe ne correspond pas'}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response({'new_password': 'Les deux mots de passent ne correspondent pas'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({'status': 'Mot de passe changé avec succès'}, status=status.HTTP_200_OK)


# User = get_user_model()

# @csrf_exempt
@api_view(['POST'])
def reset_password_get_token(request):
    if request.method == 'POST':
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Aucun utilisateur avec cette adrese mail'}, status=status.HTTP_400_BAD_REQUEST)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_password_link = request.build_absolute_uri(f"/reset-password-confirm/{uid}/{token}/")

        message = render_to_string('reset_password_email.html', {'reset_password_link': reset_password_link})
        # send_mail(subjet, message, settings.EMAIL_HOST_USER, [user.email])
        send_mail('Reset password', message, settings.EMAIL_HOST_USER, [email], fail_silently=True)

        return Response({'status': 'email envoyé'}, status=status.HTTP_200_OK)

    return Response({'error': 'Methode non valide'}, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
@api_view(['POST'])
def reset_password_confirm(request, uidb64, token):
    if request.method == 'POST':
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is None or not default_token_generator.check_token(user, token):
            return Response({'error': 'Token invalide'}, status=status.HTTP_400_BAD_REQUEST)

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return Response({'error': 'Les deux mots de passent de correspondent pas'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        return Response({'status': 'Mot de passe changé avec success'}, status=HTTP_200_OK)

    return Response({'error': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)