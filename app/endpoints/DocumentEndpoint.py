from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from app.serializers import DocumentSerializer
from app.models import Document


class DocumentEndpoint(APIView):

    def get(self, request, id):
        try:
            document = Document.objects.get(pk=id)
            serializer = DocumentSerializer(document)
            return Response(serializer.data)

        except Document.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            document = Document.objects.get(pk=id)

            document.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Document.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
