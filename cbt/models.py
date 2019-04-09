from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
import datetime, os
from django.urls import reverse


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    matric = models.CharField(max_length=25, null=True)

class Session(models.Model):
    name = models.CharField('Session Name', max_length=30)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Semester(models.Model):
    SEMESTER = (
        ('1st Semester', '1st Semester'),
        ('2nd Semester', '2nd Semester')
    )

    name = models.CharField(max_length=30, choices=SEMESTER)
    session = models.ForeignKey('Session', related_name='semester_session', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + self.session.name

class School(models.Model):
    name = models.CharField(max_length=250)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name 

class Setting(models.Model):
    min_choice = models.PositiveIntegerField('Min Number of Options', default=2)
    max_choice = models.PositiveIntegerField('Max Number of Options', default=10)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    


class Department(models.Model):
    name = models.CharField(max_length=250)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name + ' - ' + self.school.name



class Subject(models.Model):
    name = models.CharField('Course Name', max_length=30, unique=True)
    color = models.CharField(max_length=7, default='#007bff')
    code = models.CharField('Course Code', max_length=30)
    unit = models.PositiveIntegerField("Course Unit")
    description = models.TextField('Course Description')
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lecturer')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Course(models.Model):
    name = models.CharField('Course Name', max_length=30, unique=True)
    #color = models.CharField(max_length=7, default='#007bff')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department')
    code = models.CharField('Course Code', max_length=30)
    unit = models.PositiveIntegerField("Course Unit")
    description = models.TextField('Course Description')
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_lecturer')
    semester =models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='course_semster')
    is_published = models.BooleanField(default=False, null=False)
    is_completed = models.BooleanField(default=False, null=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name + ' ' + self.code + ' - ' + self.semester.name + self.semester.session.name
    '''
    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)
    '''

   

    def get_absolute_url(self):
        return reverse('teachers:quiz_change', kwargs={'pk': self.pk})
      
        

class Quiz(models.Model):
   

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_quizzes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_quizzes')
    semester = models.ForeignKey(Semester, related_name='quiz_semester', on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False, null=False)
    maximum_marks = models.DecimalField('Mark Per Questions', default=2, decimal_places=2, max_digits=6)
    duration = models.PositiveIntegerField('Duration of The Quiz', default=60) 
    total_marks = models.DecimalField('The Total Marks', default=10, decimal_places=2, max_digits=6)
    no_of_question = models.PositiveIntegerField('DuratTotal No of Questions', default=50) 
    instructions = models.TextField(default=' ')
    
    
    def __str__(self):
        return self.name


class Details(models.Model):
    

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_details')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_detailss')
    semester = models.ForeignKey(Semester, related_name='course_details', on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False, null=False)
    maximum_marks = models.DecimalField('Mark Per Questions', default=2, decimal_places=2, max_digits=6)
    duration = models.PositiveIntegerField('Duration of The Quiz', default=60) 
    total_marks = models.DecimalField('The Total Marksm Obtainable', default=10, decimal_places=2, max_digits=6)
    no_of_question = models.PositiveIntegerField('Total No of Questions', default=50) 
    instructions = models.TextField(default=' ')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.course.name


    



class Question(models.Model):
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=500)
   
    

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    courses = models.ManyToManyField(Course, through='TakenQuiz')
    #matric  = models.PositiveIntegerField('Matric No', max_length=15)
    interests = models.ManyToManyField(Course, related_name='interested_students')
    department = models.ManyToManyField(Department, related_name='department_students')

   

    def get_unanswered_questions(self, course):
        answered_questions = self.course_answers \
            .filter(answer__question__course=course) \
            .values_list('answer__question__pk', flat=True)
        questions = Course.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username

    
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilepic = models.ImageField(upload_to = 'profile/', blank=True)
    DOB = models.DateField(('Date Of Birth'), default= datetime.date.today)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='student_department')
    level = models.CharField(max_length =30)
    

    def __str__(self):
        return self.user.username

    @property
    def image_url(self):
        if self.profilepic:
            return self.profilepic.url
        else:
            return r"/static/user.png"

   


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='taken_course')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='taken_question')
    selected_choice = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    marks_obtained = models.DecimalField('Marks Obtained', default=0, decimal_places=2, max_digits=6)
    is_correct = models.BooleanField('Was this attempt correct?', default=False, null=False)
    date = models.DateTimeField(auto_now_add=True)

   


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')







