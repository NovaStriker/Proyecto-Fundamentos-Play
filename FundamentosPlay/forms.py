from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from .models import (Question, Student, User)


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields=('username','first_name','last_name','email','phone',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class AssistantSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','phone',)
    def save(self, commit=True):
        print("ayudante creado")
        user = super().save(commit=False)
        user.is_assistant = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    teacher = forms.ModelChoiceField(
        queryset=User.objects.filter(is_teacher=True),
        required=True
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.is_active = False
        user.save()
        student = Student.objects.create(user=user)
        student.teacher=User.objects.get(username=self.cleaned_data.get('teacher').username)
        print(student.teacher)
        student.save()
        return user




class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text', 'level','Dificultad','revisor',)

    def __init__(self,user,question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['revisor'].queryset = User.objects.filter(is_teacher = True).exclude(username = user.username)
        if(question != None):
            if question.estado.nombre == "AP":
                self.fields['text'].widget.attrs['readonly'] = True
                self.fields['level'].widget.attrs['readonly'] = True
                self.fields['Dificultad'].widget.attrs['readonly'] = True
                self.fields['revisor'].widget.attrs['readonly'] = True


class QuestionToCorrectForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text', 'level','Dificultad','revisor','observacion',)

    def __init__(self,user,question, *args, **kwargs):
        super(QuestionToCorrectForm, self).__init__(*args, **kwargs)
        self.fields['revisor'].queryset = User.objects.filter(is_teacher = True).exclude(username = user.username)
        self.fields['revisor'].widget.attrs['readonly'] = True
        self.fields['observacion'].widget.attrs['readonly'] = True

class QuestionApproveForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text', 'level','Dificultad',)

    def __init__(self, *args, **kwargs):
        super(QuestionApproveForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)







class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):

    def __init__(self,question, *args, **kwargs):
        super(BaseAnswerInlineFormSet, self).__init__(*args, **kwargs)
        if(question != None):
            if question.estado.nombre == "AP":
                for form in self.forms:
                  form.fields['text'].widget.attrs['readonly'] = True
                  form.fields['is_correct'].widget.attrs['readonly'] = True
                  form.fields['retroalimentacion'].widget.attrs['readonly'] = True
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Debe marcar al menos una respuesta correcta.', code='no_correct_answer')
      #  for form in self.forms:
      #      if form.cleaned_data.get('text','') != '':
      #          print("data "+form.cleaned_data.get('text'))
      #          if(form.cleaned_data.get('is_correct') == False):
      #              print("incorrecta")
#
      #              if form.cleaned_data.get('retroalimentacion','') == '':
      #                  print("sin retro")
      #                  raise ValidationError('Las respuestas incorrectas deben tener retroalimentación.', code='no_correct_answer')



