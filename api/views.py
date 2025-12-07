from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Experimento 
from .serializers import ExperimentoSerializer 

# View para listar (GET) e criar (POST)
class ExperimentoCreate(APIView):
    # Trata a requisição GET (Lista todos os experimentos)
    def get(self, request):
        experimentos = Experimento.objects.all()
        serializer = ExperimentoSerializer(experimentos, many=True) # 'many=True' indica uma lista
        return Response(serializer.data)

    # Trata a requisição POST (Cria um novo experimento)
    def post(self, request):
        serializer = ExperimentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

# View para detalhar (GET), editar (PUT/PATCH) e deletar (DELETE)
class ExperimentoDetalhe(APIView):
    # Trata a requisição GET (Retorna um experimento específico pelo PK)
    def get(self, request, pk):
        # Busca o objeto ou retorna 404 (Not Found)
        experimento = get_object_or_404(Experimento, pk=pk)
        serializer = ExperimentoSerializer(experimento)
        return Response(serializer.data)

    # *Note: O PUT/PATCH/DELETE foram omitidos para manter a concisão do tutorial,
    # mas o ViewSet que sugerimos antes já faria isso automaticamente.