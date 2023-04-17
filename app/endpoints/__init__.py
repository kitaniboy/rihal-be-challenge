from __future__ import annotations
from rest_framework.decorators import api_view, permission_classes
from django.core.files.uploadedfile import UploadedFile
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from gensim.summarization import summarize
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from PyPDF2 import PdfReader
from io import BytesIO


from firebase import firebase_bucket
from app.models import Document
from app.serializers import (
    OccurrencesSerializer,
    DocumentSerializer,
    SummarySerializer,
    SearchSerializer,
    TopSerializer,
)
from app.miners import (
    get_pasrsed_sentences,
    keyword_search,
    get_top_words,
)

SENTENCE_DELIMETER = '#$#'


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_document(request: Request):
    try:
        time_now = timezone.now()
        user = request.user
        pdf_file: UploadedFile = request.FILES.get('file')

        if pdf_file is None:
            raise Exception('PDF file was NOT provided')

        blob = firebase_bucket.blob(
            f'{pdf_file.name}_{time_now.timestamp()}'
        )
        blob.upload_from_file(
            pdf_file,
            content_type=pdf_file.content_type
        )

        pdf_file.seek(0)  # Reset the file pointer to the beginning of the file
        pdf_reader = PdfReader(BytesIO(pdf_file.read()))
        sentences = SENTENCE_DELIMETER.join(get_pasrsed_sentences(pdf_reader))

        document = Document(
            user=user,
            name=pdf_file.name,
            upload_datetime=timezone_now,
            number_of_pages=len(pdf_reader.pages),
            size=pdf_file.size,
            sentences=sentences
        )

        document.save()
        return Response(
            {
                'id': document.pk,
                'upload_datetime': document.upload_datetime,
                'number_of_pages': document.number_of_pages,
                'size': document.size,
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            f'Error while processing PDF file: {e}',
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_documents(request):
    documents = Document.objects.all()
    serializer = DocumentSerializer(documents, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def word_search(request):
    serializer = SearchSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    documents_list = []

    for document in Document.objects.all():
        sentences = keyword_search(
            document.sentences,
            serializer.validated_data['keyword']
        )

        if not sentences:
            continue

        documents_list.append({
            'id': document.pk,
            'sentences': sentences
        })

    return JsonResponse(documents_list, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_page(request, id, page_number):
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
        page = pdf_reader.pages[page_number]

    except Document.DoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)
    except IndexError:
        return Response(
            'Page number was not found',
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sentences(request, id):
    try:
        document = Document.objects.get(pk=id)
        sentences = document.sentences.split(SENTENCE_DELIMETER)
        return JsonResponse(sentences, safe=False)

    except Document.DoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request, id):
    try:
        serializer = SummarySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        document = Document.objects.get(pk=id)
        summary = summarize(
            document.sentences.replace(SENTENCE_DELIMETER, '\n'),
            word_count=serializer.validated_data['count']
        )
        return Response(summary)

    except Document.DoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)
