from django.urls import include, path
from rest_framework import routers

from .views import apiREST
from .views import home, students, teachers ,assistant




urlpatterns = [

    path('', home.home, name='home'),
    path('profile/<str:username>/', home.view_profile, name='profile'),
    path('noticias', home.noticias, name='noticias'),
    path('informacion', home.informacion, name='informacion'),
    path('descarga', home.descarga, name='descarga'),
    path('faq', home.faq, name='faq'),
    path('leaderboard', home.leaderboard, name='leaderboard'),



   #______________________________  URLS PARA  ADMINISTRACIÓN ________________________ no tocar :v
    path('students/', include(([
        path('', students.StadisticsView, name='quiz_list'),
    ], 'FundamentosPlay'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.QuestionListView.as_view(), name='question_change_list'),
        path('question/add/', teachers.question_add, name="question_add"),
        path('question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('question/approve/', teachers.QuestionApproveList.as_view(), name="to_approve_list"),
        path('question/approve/<int:question_pk>/', teachers.question_aprove_view, name='question_approve'),
        path('question/dimiss/<int:question_pk>/', teachers.question_dimiss, name='question_dimiss'),
        path('question/save/<int:question_pk>/', teachers.question_borrador, name='question_borrador'),
        path('question/filter/<str:filter>/', teachers.question_filter, name='question_filter'),
        path('question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
        path('students/', teachers.MyStudentListView.as_view(), name='my_students'),
        path('students/approve', teachers.StudentListView.as_view(), name='students_to_approve'),
        path('students/progress/<int:student_pk>/', teachers.student_progress, name='student_progress'),
        path('students/<int:student_pk>/approve', teachers.student_approve, name='student_approve'),
        path('students/<int:student_pk>/dismiss', teachers.student_dismiss, name='student_dismiss')
    ], 'FundamentosPlay'), namespace='teachers')),





]
