from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content']

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer()
    categories = CategorySerializer(many=True)
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'instructor', 'categories', 'lessons']

class QuizSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'course']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'answers']

class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    course = CourseSerializer()

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course']

class CompletionSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    course = CourseSerializer()
    lesson = LessonSerializer()
    quiz = QuizSerializer()

    class Meta:
        model = Completion
        fields = ['id', 'student', 'course', 'lesson', 'quiz']

class CourseReviewSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    course = CourseSerializer()

    class Meta:
        model = CourseReview
        fields = ['id', 'student', 'course', 'rating', 'comment']

class QuizSubmissionSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    quiz = QuizSerializer()
    answers = AnswerSerializer(many=True)

    class Meta:
        model = QuizSubmission
        fields = ['id', 'student', 'quiz', 'answers']

class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'message', 'recipient']

class CurriculumSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True)

    class Meta:
        model = Curriculum
        fields = ['id', 'name', 'courses']

class ResourceSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Resource
        fields = ['id', 'name', 'url', 'course']

class AnnouncementSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Announcement
        fields = ['id', 'message', 'course']

class AssignmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Assignment
        fields = ['id', 'name', 'description', 'course']

class SubmissionSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    assignment = AssignmentSerializer()

    class Meta:
        model = Submission
        fields = ['id', 'student', 'assignment', 'file_url']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'message', 'author', 'topic']

class PrivateMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    recipient = UserSerializer()

    class Meta:
        model = PrivateMessage
        fields = ['id', 'sender', 'recipient', 'message']

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'name', 'description', 'image_url']

class AchievementSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    badge = BadgeSerializer()

    class Meta:
        model = Achievement
        fields = ['id', 'student', 'badge', 'achievement_date']

class TimedTestSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = TimedTest
        fields = ['id', 'name', 'description', 'course', 'duration_minutes']

class TimedTestSubmissionSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    timed_test = TimedTestSerializer()
    answers = AnswerSerializer(many=True)

    class Meta:
        model = TimedTestSubmission
        fields = ['id', 'student', 'timed_test', 'answers', 'start_time', 'end_time']