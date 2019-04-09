from django.urls import include, path

from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.home, name='home'),

    path('students/', include(([
        path('', students.WelcomeListView.as_view(), name='welcome'),
        path('list', students.QuizListView.as_view(), name='quiz_list'),
        path('listcourse', students.CourseListView.as_view(), name='course_list'),
        path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
        path('exam/<int:pk>/', students.take_exam, name='take_exam'),
    ], 'cbt'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.WelcomeListView.as_view(), name='welcome'),
        path('quiz_list', teachers.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('coursedetails/<int:pk>/', teachers.CourseDetailsView.as_view(), name='course_detail'),

        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:course_pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/course/<int:course_pk>/', teachers.course_details, name='details_course'),

        path('quiz/addquestion/<int:course_pk>/', teachers.add_question, name='add_question'),



        path('quiz/<int:course_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'cbt'), namespace='teachers')),
]
