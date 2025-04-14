# annex/views.py

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from .models import Annex6a , Annex
from .serializers import Annex6aSerializer, AnnexSerializer
from .services.docx_generator import generate_annex6a_docx_response


class Annex6aViewSet(viewsets.ModelViewSet):
    queryset = Annex6a.objects.all()
    serializer_class = Annex6aSerializer

    @action(detail=True, methods=['get'], url_path='generate-docx')
    def generate_docx(self, request, pk=None):
        annex = self.get_object()
        return generate_annex6a_docx_response(annex)



class AnnexViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin, 
        viewsets.GenericViewSet
    ):
    queryset = Annex.objects.all()
    serializer_class = AnnexSerializer