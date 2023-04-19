from __future__ import annotations
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from pdf2image.pdf2image import convert_from_bytes
from rest_framework.response import Response
from PyPDF2 import PdfReader, PdfWriter
from firebase import firebase_bucket
from rest_framework import status
from io import BytesIO

from app.models import Document


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_page(request, id, num):
    try:
        document = Document.objects.get(pk=id)

        blob = firebase_bucket.blob(
            f'{document.name}_{document.upload_datetime.timestamp()}'
        )

        # Download the blob contents into an in-memory bytes buffer
        pdf_bytes = BytesIO()
        blob.download_to_file(pdf_bytes)
        pdf_bytes.seek(0)

        pdf_reader = PdfReader(pdf_bytes)
        page = pdf_reader.pages[num]

        pdf_writer = PdfWriter()
        pdf_writer.add_page(page)

        page_bytes = BytesIO()
        pdf_writer.write(page_bytes)
        page_bytes.seek(0)

        images = convert_from_bytes(page_bytes.getvalue())
        img_bytes = BytesIO()
        images[0].save(img_bytes, format='PNG')
        img_bytes.seek(0)

        return FileResponse(
            img_bytes, content_type='image/png',
            as_attachment=True, filename=f'{document.name}.png'
        )

    except Document.DoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)
    except IndexError:
        return Response(
            'Page number was not found',
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
