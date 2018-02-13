from _json import make_encoder

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_assistant = models.BooleanField(default=False)
 #   photo = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=30, null=True)


    def __str__(self):
        return self.username

class FichaCompletacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medallaPrincipiante = models.BooleanField(default=False)
    medallaIntermedio = models.BooleanField(default=False)
    medallaExperto = models.BooleanField(default=False)
    principianteFalladas = models.IntegerField(default=0)
    principianteAcertadas = models.IntegerField(default=0)
    intermedioFalladas = models.IntegerField(default=0)
    intermedioAcertadas = models.IntegerField(default=0)
    expertoFalladas = models.IntegerField(default=0)
    expertoAcertadas = models.IntegerField(default=0)

class Estado(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):

        nombre = ""
        if (self.nombre.upper() == "AP"):
            nombre = "Aprobada"
        elif (self.nombre.upper() == "PA"):
            nombre = "Enviada"
        elif (self.nombre.upper() == "BD"):
            nombre = "Borrador"
        elif (self.nombre.upper() == "PC"):
            nombre = "Por Corregir"
        return nombre

    def get_html_badge(self):
        nombre = escape(self.nombre)
        palabras = {"AP": "Aprobada", "PA": "Enviada", "BD": "Borrador","PC":"Por Corregir"}
        colores = {"AP": "green", "PA": "blue", "BD": "gray", "PC": "red"}
        html = '<h4><span class="badge badge-primary" style="background-color: %s">%s</span></h4>' % (
        colores[nombre.upper()], palabras[nombre.upper()])
        return mark_safe(html)


class Dificultad(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField('Contenido', max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    level = models.IntegerField('Nivel')
    Dificultad = models.ForeignKey(Dificultad, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='questions', null=True)
    fecha = models.DateTimeField('Fecha', auto_now=True)
    observacion = models.CharField('Observación', max_length=255, null=True)
    revisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revisor', null=True)
    veces_correcta=models.IntegerField(default=0, auto_created=True)
    veces_incorrecta = models.IntegerField(default=0, auto_created=True)

    class Meta:
        ordering = ['-fecha']
    def __str__(self):
        return self.text[:20] + "..."


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Respuesta', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)
    retroalimentacion = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher", null=True)


    def __str__(self):
        return self.user.username


class Course(models.Model):
    par = models.IntegerField( primary_key=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class LeaderBoard(models.Model):
    leader = models.IntegerField(primary_key=True)


class Player(models.Model):
    unidad = models.IntegerField(primary_key=True)
    leader = models.ForeignKey(LeaderBoard, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=200, default="Nombres y Apellidos")
    foto = models.CharField(max_length=400, default="http://bandera.inquirer.net/files/2016/06/BLIND-ITEM-MALE-0624.jpg") 
    duracion = models.IntegerField(null=False)
    segundos = models.IntegerField(default=0)
    minutos = models.IntegerField(default=0)
    horas = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre+", Unidad "+str(self.unidad)

