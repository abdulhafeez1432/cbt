from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
import random
from ..decorators import student_required
from ..forms import StudentInterestsForm, StudentSignUpForm, TakeQuizForm, ExamForm
from ..models import Quiz, Student, TakenQuiz, User, Course, Answer, Details, Question


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        messages.success(self.request, 'Student HAs Been Succfull Resigerter!')
        return redirect('student_signup')

@method_decorator([login_required, student_required], name='dispatch')
class WelcomeListView(ListView):
    model = Course
    ordering = ('name', )
    context_object_name = 'course'
    template_name = 'classroom/students/home.html'

 

    def get_queryset(self):
        queryset = Course.objects.all()
        return queryset


def text(request):
    context = {
        'days': [1, 2, 3],
    }
    return render(request, 'classroom/students/days.html', context)
        


@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Student
    form_class = StudentInterestsForm
    template_name = 'classroom/students/interests_form.html'
    success_url = reverse_lazy('students:welcome')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)



@method_decorator([login_required, student_required], name='dispatch')
class CourseListView(ListView):
    model = Course
    ordering = ('name', )
    context_object_name = 'course'
    template_name = 'classroom/students/quiz_list.html'
 
    def get_queryset(self):
        student = self.request.user.student
        student_interests = student.interests.values_list('id', flat=True)
                
        queryset = Course.objects.filter(id__in=student_interests) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
            
        return queryset

        
    
  




@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Course
    ordering = ('name', )
    context_object_name = 'course'
    template_name = 'classroom/students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_interests = student.interests.values_list('pk', flat=True)
        taken_quizzes = student.interest.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('course') \
            .order_by('course__name')
        return queryset


@login_required
@student_required
def take_quiz(request, pk):
    course = get_object_or_404(Course, pk=pk)
    student = request.user.student

    '''
    if student.course.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')
    '''
    total_questions = course.questions.count()
    unanswered_questions = student.get_unanswered_questions(course)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(course).exists():
                    return redirect('students:take_quiz', pk)
                else:
                    correct_answers = student.course_answers.filter(answer__question__quiz=course, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, course=course, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (course.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (course.name, score))
                    return redirect('students:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'classroom/students/take_quiz_form.html', {
        'quiz': course,
        'question': question,
        'form': form,
        'progress': progress
    })



@login_required
@student_required
def take_exam(request, pk):
    course = get_object_or_404(Course, pk=pk)
    student = request.user.student
    question = course.questions.filter()  
    #correct_answers = student.course_answers.filter(answer__question__quiz=course, answer__is_correct=True).count()
    total_questions = course.questions.count()
    choice = Answer.objects.filter()
    marks_obtainable = Details.objects.get(course_id=course)

    

    if request.method == 'POST':

        question_pk = request.POST.getlist('question_pk')
        #question_obj = Question.objects.filter(id=int(question_pk))
        #question_obj = Question.objects.filter(id=question_pk)
        #question_pk = [Question.objects.get(pk=pk) for pk in request.POST.getlist('question_pk')]
        question_pk = [Question.objects.get(pk=pk) for pk in question_pk]
        print(question_pk)


        #choice_pk = [request.POST['choice_pk{}'.format(q)] for q in question_obj]
        choice_pk = [request.POST['choice_pk{}'.format(q)] for q in question_pk]
              
        #print(marks_obtainable.marks_obtained)
        zipped = zip(question_pk, choice_pk)

        for x, y in zipped:
            correct_answers = Answer.objects.filter(question_id=x,  is_correct=True).values("id").first()['id']

            print(x, y, correct_answers)
            if int(y) == int(correct_answers):
                #z = TakenQuiz(student=student, course=course, question=x, selected_choice=y,  marks_obtained=marks_obtainable, is_correct=True)
                print("correct")
            else:
                #z = TakenQuiz(student=student, course=course, question=x, selected_choice=y,  marks_obtained=marks_obtainable, is_correct=False)
                print("Not Correct")
            

    
    return render(request, 'classroom/students/take_exam_form.html', {
        'course': course,
        'question': question,
        'course': course,
        'total_questions': total_questions,
        'choice': choice,
        'marks_obtainable': marks_obtainable

        
    })


    