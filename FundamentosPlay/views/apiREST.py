from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import  Response
from rest_framework import status, viewsets

from ..models import *


class Medallas(viewsets.ModelViewSet):

    def get(self,request,user_id):
        pass

        #serializador = ResultadoSerializer(resultados , many=True)
        #return  Response(serializador.data)

    def post(self):
        pass


class Leader(APIView):

	def get(self, request, id_leader):
		pass
