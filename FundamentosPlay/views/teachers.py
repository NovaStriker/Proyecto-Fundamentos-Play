from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, ListView)

from ..forms import QuestionToCorrectForm
from ..decorators import teacher_required
from ..forms import BaseAnswerInlineFormSet, QuestionForm, TeacherSignUpForm, QuestionApproveForm
from ..models import Answer, Question,  User, Estado, Dificultad, Student
from django.core.mail import send_mail

#metodo para obtener los numeros de badges
def badges_counter(user):
    enviadas = Question.objects.filter(owner=user,estado__nombre="PA").count()
    aprobadas = Question.objects.filter(owner=user,estado__nombre="AP").count()
    borrador = Question.objects.filter(owner=user, estado__nombre="BD").count()
    porCorregir = Question.objects.filter(owner=user, estado__nombre="PC").count()
    usuariosPA= Student.objects.filter(teacher=user , user__is_active=False).count()
    questionsPA = Question.objects.filter(revisor=user , estado__nombre="PA").count()
    return {"PA":enviadas , "AP":aprobadas, "BD":borrador, "PC":porCorregir, "usersPA":usuariosPA, "questionsPA":questionsPA}


def send_email(para,asunto,mensaje):
    send_mail(
         asunto,
         mensaje,
        'fundamentosplaygame@gmail.com',
        [para],
        fail_silently=False,
    )
#Registro de profesores
class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Profesor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers:question_change_list')



#Lista de perguntas totales
@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionListView(ListView):

    ordering = ('fecha', )
    context_object_name = 'questions'
    template_name = 'FundamentosPlay/teachers/question_change_list.html'


    def get_queryset(self):
        queryset = self.request.user.questions.filter(owner=self.request.user)
        print(queryset)
        return queryset



    def get_context_data(self, **kwargs):
        extra_context ={"counts": badges_counter(self.request.user)}
        context = super(self.__class__, self).get_context_data(**kwargs)
        for key, value in extra_context.items():
            if callable(value):
                context[key] = value()
            else:
                context[key] = value
        return context


#Lista de preguntas por aprobar
@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionApproveList(ListView):

    ordering = ('text', )
    context_object_name = 'to_approve'
    template_name = 'FundamentosPlay/teachers/question_to_approve_list.html'

    def get_queryset(self):
        queryset = Question.objects.filter(revisor__username=self.request.user , estado__nombre="PA")
        return queryset

    def get_context_data(self, **kwargs):
        extra_context ={"counts": badges_counter(self.request.user)}
        context = super(self.__class__, self).get_context_data(**kwargs)
        for key, value in extra_context.items():
            if callable(value):
                context[key] = value()
            else:
                context[key] = value
        return context




#vista para crear  pregunta  sin respuestas

@login_required
@teacher_required
def question_add(request):
    if request.method == 'POST':

        form = QuestionForm(request.user,None ,request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.owner = request.user
            estado =  Estado.objects.get(nombre="BD")
            question.estado =estado
            question.save()
            messages.success(request, 'Ahora podrá agregar  las respuestas y retroalimentaciones')
            return redirect('teachers:question_change', question.pk)
        else:
            messages.error(request, 'Todos los campos son obligatorios')
            form = QuestionForm(request.user,None)
            return render(request, 'FundamentosPlay/teachers/question_add_form.html', {'form': form })
    else:
        form = QuestionForm(request.user,None)

    return render(request, 'FundamentosPlay/teachers/question_add_form.html', {'form': form , 'counts': badges_counter(request.user)})



#vista para editar una pergunta
@login_required
@teacher_required
def question_change(request,  question_pk):

    question = Question.objects.get(pk=question_pk)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        fields=('text', 'is_correct', 'retroalimentacion'),
        formset=BaseAnswerInlineFormSet,

        min_num=2,
        validate_min=True,
        max_num=4,
        validate_max=True
    )
    if request.method == 'POST':

        if(question.estado.nombre =="PC"):
            print("por coregir  post")
            form = QuestionToCorrectForm(request.user, question, request.POST, instance=question)
            print(request.POST)
        else:
            form = QuestionForm(request.user ,question, request.POST, instance=question)
        formset = AnswerFormSet(question,request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.estado = Estado.objects.get(nombre="PA")
            form.save()
            formset.save()
            send_email(question.revisor.email, "Pregunta Recibida",
                       question.owner.username + " Le ha enviado pregunta")
            messages.success(request, 'Pregunta enviada exitosamente!')
            return redirect('teachers:question_change_list')
        else:
            print("el form no es valido")
            print( form.errors)
            return render(request, 'FundamentosPlay/teachers/question_change_form.html', {
                'question': question,
                'form': form,
                'formset': formset,
                'counts': badges_counter(request.user)})
    else:
        if (question.estado.nombre == "PC"):
            form = QuestionToCorrectForm(request.user, question, instance=question)
        else:
            form = QuestionForm(request.user, question, instance=question)
        formset = AnswerFormSet(question,instance=question)
    return render(request, 'FundamentosPlay/teachers/question_change_form.html', {
        'question': question,
        'form': form,
        'formset': formset,
        'counts': badges_counter(request.user)})

#borrar una pregunta
@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    success_url = reverse_lazy('teachers:quiz_change_list')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()



#vista  de  aprobar pregunta
@login_required
@teacher_required
def question_aprove_view(request,  question_pk):
    question = get_object_or_404(Question, pk=question_pk)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct','retroalimentacion'),
        min_num=2,
        validate_min=True,
        max_num=4,
        validate_max=True

    )

    if request.method == 'POST':
        form = QuestionApproveForm(request.POST, instance=question)
        formset = AnswerFormSet(question,request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                question = form.save(commit=False)
                estado = Estado.objects.get(nombre="AP")
                question.estado = estado
                form.save()
                formset.save()

            send_email(question.owner.email, "Pregunta Aprobada",question.revisor.username + " ha aprobado su pregunta")
            messages.success(request, 'Pregunta Aprobada exitosamente!')
            return redirect('teachers:to_approve_list')
    else:
        if(question.revisor == request.user):
            form = QuestionApproveForm(instance=question )
            formset = AnswerFormSet(question,instance=question)
        else:
            raise PermissionDenied

    return render(request, 'FundamentosPlay/teachers/question_approve_form.html', {
        'question': question,
        'form': form,
        'formset': formset,
        'counts': badges_counter(request.user)
    })



#accion de  rechazar pregunta
@login_required
@teacher_required
def question_dimiss(request ,question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    if request.method == 'POST':
        form = QuestionApproveForm(request.POST, instance=question)
        if form.is_valid():
            with transaction.atomic():
                question = form.save(commit=False)
                estado = Estado.objects.get(nombre="PC")
                question.estado = estado
                question.observacion= request.POST.get('observacion',"No se adjuntó observación")
                if(question.observacion!=""):
                    question.save()
                    send_email(question.owner.email, "Pregunta Rechazada",
                        question.revisor.username + " ha rechazado su pregunta y ha añadido la siguiente observación:\n"+
                        question.observacion)
                    messages.success(request, 'Observación enviada exitosamente!')
                else:
                    messages.error(request, 'Debe adjuntar una observación!')
                    return redirect('teachers:question_approve', question.pk)
            return redirect('teachers:to_approve_list')
    print("get dismiss")

#controlador para guardar en borrador
@login_required
@teacher_required
def question_borrador(request ,question_pk):
    question = get_object_or_404(Question, pk=question_pk)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct', 'retroalimentacion'),
        min_num=2,
        validate_min=True,
        max_num=4,
        validate_max=True

    )

    if request.method == 'POST':
        form = QuestionApproveForm(request.POST, instance=question)
        formset = AnswerFormSet(question, request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                question = form.save(commit=False)
                estado = Estado.objects.get(nombre="BD")
                question.estado = estado
                form.save()
                formset.save()
            messages.success(request, 'Pregunta guardada en Borradores')
            return redirect('teachers:question_change_list')



'''
@method_decorator([login_required, teacher_required], name='dispatch')
class QuizResultsView(DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'FundamentosPlay/teachers/quiz_results.html'

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-date')
        total_taken_quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_quizzes': taken_quizzes,
            'total_taken_quizzes': total_taken_quizzes,
            'quiz_score': quiz_score
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()

'''


#Lista de estudiantes por aprobar
@method_decorator([login_required, teacher_required], name='dispatch')
class StudentListView(ListView):
    context_object_name = 'students'
    template_name = 'FundamentosPlay/teachers/student_approve_list.html'
    def get_queryset(self):
        queryset = Student.objects.filter(teacher=self.request.user ,user__is_active=False)
        return queryset

    def get_context_data(self, **kwargs):
        extra_context ={"counts": badges_counter(self.request.user)}
        context = super(self.__class__, self).get_context_data(**kwargs)
        for key, value in extra_context.items():
            if callable(value):
                context[key] = value()
            else:
                context[key] = value
        return context



#accion de  aprobar estudiante
@login_required
@teacher_required
def student_approve(request ,student_pk):
    student = get_object_or_404(User, pk=student_pk)
    if request.method == 'GET':
        student.is_active=True
        student.save()
        messages.info(request, 'Estudiante aprobado exitosamente!')
    return redirect('teachers:students_to_approve')


#accion de  rechazar estudiante
@login_required
@teacher_required
def student_dismiss(request ,student_pk):
    student = get_object_or_404(User, pk=student_pk)
    if request.method == 'GET':
        student.delete()
        messages.info(request, 'Estudiante rechazado exitosamente!')
    return redirect('teachers:students_to_approve')



#Lista de perguntas envaidas
@login_required
@teacher_required
def question_filter(request,filter):
    if(request.method == 'GET'):
        questions = Question.objects.filter(owner=request.user, estado__nombre= filter)
        return render(request, 'FundamentosPlay/teachers/question_change_list.html', {"questions": questions
                                                            , "counts":badges_counter(request.user)})

#Lista de mis estudiantes
@method_decorator([login_required, teacher_required], name='dispatch')
class MyStudentListView(ListView):
    context_object_name = 'students'
    template_name = 'FundamentosPlay/teachers/my_students.html'
    def get_queryset(self):
        queryset = Student.objects.filter(teacher=self.request.user ,user__is_active=True)
        return queryset

    def get_context_data(self, **kwargs):
        extra_context ={"counts": badges_counter(self.request.user)}
        context = super(self.__class__, self).get_context_data(**kwargs)
        for key, value in extra_context.items():
            if callable(value):
                context[key] = value()
            else:
                context[key] = value
        return context

#Lista de perguntas envaidas
@login_required
@teacher_required
def student_progress(request,student_pk):
    if(request.method == 'GET'):
        queryset = Student.objects.filter(teacher=request.user ,user__is_active=True)
        return render(request, 'FundamentosPlay/teachers/students_progress.html', {"students": {queryset}
                                                            , "counts":badges_counter(request.user)})