from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from firebase import firebase_bucket
from rest_framework import status

from app.serializers import DocumentSerializer
from app.models import Document


class DocumentEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            user = request.user
            document = user.document_set.get(pk=id)
            serializer = DocumentSerializer(document)
            return Response(serializer.data)

        except Document.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            user = request.user
            document = user.document_set.get(pk=id)

            blob = firebase_bucket.blob(
                f'{document.name}_{document.upload_datetime.timestamp()}'
            )

            blob.delete()
            document.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Document.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
