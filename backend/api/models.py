from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_TYPE  = [
        ('ADMIN','ADMIN'),
        ('SPECIALISTE','SPECIALISTE'),
        ('ENCADREUR','ENCADREUR'),
       
    ]
    role = models.CharField("Rôle", max_length=50, choices = ROLE_TYPE)
    # pass

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Caterory'
        verbose_name_plural = 'Caterories'
class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    categories = models.ManyToManyField(Category, related_name='courses')

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')

class Question(models.Model):
    question_text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

class Answer(models.Model):
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')

class Completion(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='completions')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name='completions')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True, related_name='completions')

class CourseReview(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.FloatField()
    comment = models.TextField()

class QuizSubmission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_submissions')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions')
    answers = models.ManyToManyField(Answer)

class Notification(models.Model):
    message = models.TextField()
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

class Curriculum(models.Model):
    name = models.CharField(max_length=255)
    courses = models.ManyToManyField(Course, related_name='curriculums')

class Resource(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='resources')

class Announcement(models.Model):
    message = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements')

class Assignment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')

class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    file_url = models.URLField()

class Forum(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='forums')

class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='topics')

class Post(models.Model):
    message = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()

class Badge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField()

class Achievement(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='achievements')
    achievement_date = models.DateTimeField(auto_now_add=True)

class TimedTest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timed_tests')
    duration_minutes = models.PositiveIntegerField()

class TimedTestSubmission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timed_test_submissions')
    timed_test = models.ForeignKey(TimedTest, on_delete=models.CASCADE, related_name='submissions')
    answers = models.ManyToManyField(Answer)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
