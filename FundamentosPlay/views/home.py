from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from ..models import User, Estado, Dificultad


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    '''Estado.objects.all().delete()
    Dificultad.objects.all().delete()
    estado = Estado()
    estado.nombre="AP"
    estado2 = Estado()
    estado2.nombre = "PA"
    estado3 = Estado()
    estado3.nombre = "PC"
    estado4 = Estado()
    estado4.nombre = "BD"
    estado.save()
    estado2.save()
    estado3.save()
    estado4.save()
    d= Dificultad()
    d.name="Principiante"
    d.save()
    d2 = Dificultad()
    d2.name = "Intermedio"
    d2.save()
    d3 = Dificultad()
    d3.name = "Experto"
    d3.save()'''


    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:question_change_list')
        if request.user.is_assistant:
            return redirect('assistants:question_change_list')
        if request.user.is_student and request.user.is_active:
            return render(request, 'FundamentosPlay/home.html')
    return render(request, 'FundamentosPlay/home.html')


@login_required
def view_profile(request, username):
    user = request.user
    if (user.username != username):
        raise PermissionDenied
    try:
        usuario = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Usuario No existe")

    data = {'usuario': usuario}
    return render(request, 'FundamentosPlay/profile.html', data)


def noticias(request):
    return render(request, "FundamentosPlay/noticias.html", {'pagina':'Noticias'})


def informacion(request):
    return render(request, "FundamentosPlay/informacion.html", {'pagina':'Información'})


def leaderboard(request):
    return render(request, "FundamentosPlay/leaderboard.html", {'pagina':'LeaderBoard'})


def faq(request):
    return render(request, "FundamentosPlay/faq.html", {'pagina':'Preguntas Frecuentes'})


def descarga(request):
    return render(request, "FundamentosPlay/descarga.html", {'pagina':'Descarga'})