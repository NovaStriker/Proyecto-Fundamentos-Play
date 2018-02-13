from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import student_required
from ..forms import  StudentSignUpForm
from ..models import  Student, User


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Estudiante'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        print("formulario valido")
        user = form.save()
        print("usuario creado")
        messages.success(self.request, 'Cuenta creada con éxito, podrá iniciar sesión cuando su profesor apruebe la cuenta')
        return render(self.request, 'FundamentosPlay/home.html')
def StadisticsView(request):
    return render(request, 'FundamentosPlay/home.html')