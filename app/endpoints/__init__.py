from __future__ import annotations
from django.core.files.uploadedfile import UploadedFile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from PyPDF2 import PdfFileReader
from io import BytesIO

from app.models import Document
from app.serializers import (
    OccurrencesSerializer,
    DocumentSerializer,
    SearchSerializer,
    TopSerializer,
)
from app.miners import (
    get_pasrsed_sentences,
    keyword_search,
    get_top_words,
)


@api_view(['POST'])
def add_document(request):
    pdf_file: UploadedFile = request.FILES.get('file')
    try:
        pdf_reader = PdfFileReader(BytesIO(pdf_file.read()))
        sentences = '\n'.join(get_pasrsed_sentences(pdf_reader))

        document = Document(
            name=pdf_file.name,
            upload_datetime=timezone.now(),
            number_of_pages=pdf_reader.numPages,
            size=pdf_file.size,
            sentences=sentences
        )

        serializer = DocumentSerializer(document)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception:
        return Response(
            'Error while processing PDF file.',
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def list_documents(request):
    documents = Document.objects.all()
    serializer = DocumentSerializer(documents, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def word_search(request):
    serializer = SearchSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    found_sentences = dict()

    for document in Document.objects.all():
        returned_sentences = keyword_search(
            document.sentences,
            serializer.validated_data['keyword']
        )

        if not returned_sentences:
            continue

        found_sentences[document.pk] = returned_sentences

    return JsonResponse(found_sentences, safe=False)


@api_view(['GET'])
def get_page(request, id, page_number):
    try:
        document = Document.objects.get(pk=id)

        pdf_reader = PdfFileReader(smth)
        page = pdf_reader.getPage(page_number)

    except Document.DoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)
    except IndexError:
        return Response(
            'Page number was not found',
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def get_sentences(request, id):
    try:
        document = Document.objects.get(pk=id)
        sentences = document.sentences.split('\n')
        return JsonResponse(sentences, safe=False)

    except Document.DoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_occurrences(request, id):
    try:
        serializer = OccurrencesSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        document = Document.objects.get(pk=id)

        found_sentences = keyword_search(
            document.sentences,
            serializer.validated_data['keyword']
        )

        return JsonResponse(found_sentences, safe=False)

    except Document.DoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_most_common(request, id):
    try:
        serializer = TopSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        document = Document.objects.get(pk=id)

        top_words = get_top_words(
            document.sentences,
            serializer.validated_data['count']
        )

        return JsonResponse(top_words, safe=False)

    except Document.DoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)
