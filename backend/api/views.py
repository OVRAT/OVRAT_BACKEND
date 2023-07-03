from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view , permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
# Create your views here.
from .serializers import *

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializers
    queryset = get_user_model().objects.all()



# Status

# HTTP_200_OK
# HTTP_201_CREATED
# HTTP_202_ACCEPTED
# HTTP_203_NON_AUTHORITATIVE_INFORMATION
# HTTP_204_NO_CONTENT
# HTTP_205_RESET_CONTENT
# HTTP_206_PARTIAL_CONTENT
# HTTP_207_MULTI_STATUS
# HTTP_208_ALREADY_REPORTED
# HTTP_226_IM_USED

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

    return Response()