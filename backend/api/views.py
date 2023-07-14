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
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from django.templatetags.static import static
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
# HTTP_300_MULTIPLE_CHOICES
# HTTP_204_NO_CONTENT
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
        # image_url = request.build_absolute_uri(static('img/Ovrat.PNG'))

        message = render_to_string('reset_password_email.html', {'reset_password_link': reset_password_link, 'img':image_url})
        plain_message = strip_tags(message)
        # send_mail(subjet, message, settings.EMAIL_HOST_USER, [user.email])
        # send_mail('Reset password', message, settings.EMAIL_HOST_USER, [email], fail_silently=True,  content_subtype='html')
        # emails = EmailMessage('Bienvenue sur notre site', message,  settings.EMAIL_HOST_USER,  [email,]   )

        send_mail(
            subject="Reset Password",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            html_message=message,
            # content_subtype='html'
        )

        # emails.content_subtype = 'html'
        # emails.send(fail_silently = False)
	    # emails.send(fail_silently = False)
	    # # Envoyer l'e-mail
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

        return Response({'status': 'Mot de passe changé avec success'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)   
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def course_list(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        course.delete()
        return Response(status=204)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def lesson_list(request):
    if request.method == 'GET':
        lessons = Lesson.objects.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def lesson_detail(request, pk):
    try:
        lesson = Lesson.objects.get(pk=pk)
    except Lesson.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = LessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        lesson.delete()
        return Response(status=204)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def quiz_list(request):
    if request.method == 'GET':
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def quiz_detail(request, pk):
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = QuizSerializer(quiz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        quiz.delete()
        return Response(status=204)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def question_list(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def question_detail(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    # elif:
    #     pass


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def question_detail(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        question.delete()
        return Response(status=204)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def enrollment_list(request):
    if request.method == 'GET':
        enrollments = Enrollment.objects.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def enrollment_detail(request, pk):
    try:
        enrollment = Enrollment.objects.get(pk=pk)
    except Enrollment.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = EnrollmentSerializer(enrollment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        enrollment.delete()
        return Response(status=204)



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token
        token['username'] = user.username
        token['email'] = user.email
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        # Add user information to the response data
        response.data['username'] = user.username
        response.data['email'] = user.email
        userser = User.objects.get(email = user.email)
        userserial = UserSerializers(userser)
        response.data['user'] = userserial.data
        return response