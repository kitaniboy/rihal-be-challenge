from __future__ import annotations
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from gensim.summarization import summarize
from django.utils.timezone import now
from django.http import JsonResponse
from firebase import firebase_bucket
from rest_framework import status
from PyPDF2 import PdfReader
from io import BytesIO

from app.models import Document
from app.serializers import (
    SentencesSerializer,
    DocumentSerializer,
    SummarySerializer,
    SearchSerializer,
    TopSerializer,
)
from app.miners import (
    get_pasrsed_pages_sentences,
    keyword_search,
    get_top_words,
)
from app.constants import (
    PAGE_DELIMETER,
    SPLIT_PATTERN,
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_document(request: Request):
    try:
        time_now = now()
        user = request.user
        pdf_file = request.FILES.get('file')

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
        sentences = PAGE_DELIMETER.join(
            get_pasrsed_pages_sentences(pdf_reader)
        )

        document = Document(
            user=user,
            name=pdf_file.name,
            upload_datetime=time_now,
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
    user = request.user
    documents = user.document_set.all()
    serializer = DocumentSerializer(documents, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def word_search(request):
    user = request.user
    serializer = SearchSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    keyword = serializer.validated_data['keyword']
    documents_list = []

    for document in user.document_set.all():
        occurrences = []

        for page_number, page_sentences in enumerate(document.sentences.split(
            PAGE_DELIMETER
        )):
            sentences = keyword_search(page_sentences, keyword)

            if not sentences:
                continue

            occurrences.append({
                'page_number': page_number,
                'sentences': sentences
            })

        if not occurrences:
            continue

        documents_list.append({
            'id': document.pk,
            'occurrences': occurrences
        })

    return JsonResponse(documents_list, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def word_doc_search(request, id):
    try:
        user = request.user
        document = user.document_set.get(pk=id)
        serializer = SearchSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        keyword = serializer.validated_data['keyword']
        pages_list = []

        for page_number, page_sentences in enumerate(document.sentences.split(
            PAGE_DELIMETER
        )):
            found_sentences = keyword_search(page_sentences, keyword)

            if not found_sentences:
                continue

            pages_list.append({
                'page_number': page_number,
                'sentences': found_sentences
            })

        return JsonResponse(pages_list, safe=False)

    except Document.DoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sentences(request, id):
    try:
        user = request.user
        document = user.document_set.get(pk=id)

        serializer = SentencesSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        start_page = serializer.validated_data['start_page']
        end_page = serializer.validated_data['end_page']

        requested_pages = PAGE_DELIMETER.join(
            document.sentences.split(PAGE_DELIMETER)[start_page:end_page]
        )

        sentences = SPLIT_PATTERN.split(requested_pages)
        return JsonResponse(sentences, safe=False)

    except Document.DoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_most_common(request, id):
    try:
        user = request.user
        document = user.document_set.get(pk=id)
        serializer = TopSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        count = serializer.validated_data['count']
        start_page = serializer.validated_data['start_page']
        end_page = serializer.validated_data['end_page']

        sentences = '\n'.join(
            document.sentences.split(PAGE_DELIMETER)[start_page:end_page]
        )

        top_words = get_top_words(
            SPLIT_PATTERN.sub('\n', sentences),
            count
        )

        return JsonResponse(top_words, safe=False)

    except Document.DoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request, id):
    try:
        user = request.user
        document = user.document_set.get(pk=id)
        serializer = SummarySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        count = serializer.validated_data['count']
        start_page = serializer.validated_data['start_page']
        end_page = serializer.validated_data['end_page']

        sentences = '\n'.join(
            document.sentences.split(PAGE_DELIMETER)[start_page:end_page]
        )

        summary = summarize(
            SPLIT_PATTERN.sub('\n', sentences),
            word_count=count
        )
        return Response(summary)

    except Document.DoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)
